import { Attribute, Injectable } from '@angular/core';
import { ITOSBuild, TOSStat } from "../domain/tos/tos-domain";
import { TOSDomainService } from "../domain/tos/tos-domain.service";
import { LEVEL_LIMIT } from "../domain/tos/tos-build";
import { Observable } from "rxjs";
import { fromPromise } from "rxjs/internal-compatibility";
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { TOSUrlService } from './tos-url.service';
import { TOSRegionService } from '../domain/tos-region';
import { InjectorInstance } from 'src/app/app.module';

declare enum LUA_MODE {
    Skill="skill",
    Attribute="ability"
};
@Injectable({
    providedIn: 'root'
})
export class RemoteLUAService {

    // Some player stats used by the formulas
    private static readonly STATS_RUNTIME = {
        'CON': TOSStat.CON,
        'DEX': TOSStat.DEX,
        'INT': TOSStat.INT,
        'MNA': TOSStat.SPR,
        'STR': TOSStat.STR,
        'Lv': 'Level',
        'HR': TOSStat.ACCURACY,
        'MHP': TOSStat.HP,
        'MSP': TOSStat.SP,
        'SR': TOSStat.AOE_ATTACK_RATIO,
        'MSPD': TOSStat.MOVEMENT_SPEED,
        'MDEF': TOSStat.DEFENSE_MAGICAL,
        'DEF': TOSStat.DEFENSE_PHYSICAL,
        'PATK': TOSStat.ATTACK_PHYSICAL,
        'MATK': TOSStat.ATTACK_MAGICAL,
        'MAXATK': TOSStat.ATTACK_LIMIT_MAX,
        'MAXMATK': 'Maximum Magic Attack',
        'MAXPATK': 'Minimum Physical Attack',
        'MAXPATK_SUB': 'Maximum Physical Attack (Sub-Weapon)',
        'MINATK': TOSStat.ATTACK_LIMIT_MIN,
        'MINMATK': 'Minimum Magic Attack',
        'MINPATK': 'Minimum Physical Attack',
        'MINPATK_SUB': 'Minimum Physical Attack (Sub-Weapon)',
    };

    constructor() { }

    static async evalSkill(build: ITOSBuild, id$:string,element: string, context?: object): Promise<string> {
        return this.eval(build, id$,element, LUA_MODE.Skill,context);
    }
    static async evalAttribute(build: ITOSBuild, id$:string,element: string, context?: object): Promise<string> {
        return this.eval(build, id$,element, LUA_MODE.Attribute,context);
    }
    private static async eval(build: ITOSBuild,  id$:string,element: string,  type: LUA_MODE,context?: object): Promise<string> {
    
        let dependencies: string[] = [];

        let func: string[] = [];
        // func.push('(function () {');
        let jsoncontext = {
            skills: {},
            abilities: {},
            stats: {},
            jobs: {}
        };

        context = context || {};
        context["ClassName"] = 'PC';
        //context.JobHistoryList = build.Jobs && build.Jobs.map(value => value.$ID);
        context["Lv"] = LEVEL_LIMIT; // TODO: get level from build

        // Initialize context

        // func.push('var pc = ' + JSON.stringify(player) + ';');
        // func.push('var skill = ' + JSON.stringify(skill) + ';');
        // func = func.concat(LUAService.LUA_CONTEXT);

        // Object
        //     .keys(context)
        //     .forEach(key => {
        //         let value = typeof context[key] == 'object' ? JSON.parse(context[key]) : context[key];
        //         func.push('var ' + key + ' = ' + value + ';')
        //     });

        jsoncontext.abilities = {}
        for (var key in build.Attributes) {
            let abil = build.Attributes[key]

            jsoncontext.abilities[abil.$ID] = build.attributeLevel(abil)
        }
        for (var key in build.Jobs) {
            jsoncontext.jobs[build.Jobs[key].$ID] = build.jobCircle(build.Jobs[key]);

            let skills = await build.Jobs[key].Link_Skills
            for (var key in skills) {
                let skill = skills[key];
                jsoncontext.skills[skill.$ID] = build.skillLevel(skill);
            };

        }




        for (var key in RemoteLUAService.STATS_RUNTIME) {
            jsoncontext.stats[key] = context[key];
        }


        //httprequest
        let request = {
            context: jsoncontext,
            region: TOSRegionService.get().toString(),
            type:type.toString(),
            classid:id$,
            mode:element

            
        }
        let http=InjectorInstance.get<HttpClient>(HttpClient);

        let result=http.post(
            TOSUrlService.WORKER_REACTION(),
            request,{responseType:"text"}
        )
        //result: result of value

        // Execute
        //func = func.concat(source);
        //func.push('}())');

        return result.toPromise()
        
    }

}
