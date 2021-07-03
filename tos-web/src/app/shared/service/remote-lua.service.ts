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
import { map } from 'rxjs/operators';

enum LUA_MODE {
    Skill="skill",
    Attribute="ability",
    Ether="!Ether",
    Relic="!Relic",
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

    private static readonly STATS_RUNTIME_BASE = {
        'CON': 1000,
        'DEX': 1000,
        'INT': 1000,
        'MNA': 1000,
        'STR': 1000,
        'Lv':  LEVEL_LIMIT,
        'HR': 1000,
        'MHP': 300000,
        'MSP': 20000,
        'SR': 0,
        'MSPD': 30,
        'MDEF': 30000,
        'DEF': 30000,
        'PATK': 30000,
        'MATK': 30000,
        'MAXATK': 30000,
        'MAXMATK': 30000,
        'MAXPATK': 30000,
        'MAXPATK_SUB': 30000,
        'MINATK': 30000,
        'MINMATK': 30000,
        'MINPATK': 30000,
        'MINPATK_SUB': 30000,
    };

    constructor() { }

    static async evalSkill(build: ITOSBuild, id$:string,element: string, context?: object): Promise<string> {
        return this.eval(build, id$,element, LUA_MODE.Skill,context);
    }
    static async evalAttribute(build: ITOSBuild, id$:string,element: string, context?: object): Promise<string> {
        return this.eval(build, id$,element, LUA_MODE.Attribute,context);
    }
    static async evalRelic(id$:string, mode:string,arg?:any,arg2?:any): Promise<string> {
        return this.evalLua(id$,"item",mode,arg,arg2);
    }
    static async evalEther(id$:string, mode:string,arg?:any,arg2?:any): Promise<string> {
        return this.evalLua(id$,"item",mode,arg,arg2);
    }
    private static async evalLua(id$:string,iestype:string,mode:string,arg?:any,arg2?:any): Promise<string> {
        
    


        //httprequest
        let request = {
            context: {},
            region: TOSRegionService.getRegion().toString(),
            type:iestype.toString(),
            classid:id$,
            mode:mode.toString(),
            arg:arg,
            arg2:arg2
        }
        let http=InjectorInstance.get<HttpClient>(HttpClient);

        let result=http.post(
            TOSUrlService.WORKER_REACTION(),
            request,{responseType:"text"}
        )
   
        return result.pipe(map((x:string)=>{
            let obj:any=JSON.parse(x)
            return obj['result'] as string
         })).toPromise()
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

        jsoncontext.abilities = {}
        for (var key in build.Attributes) {
            let abil = build.Attributes[key]

            jsoncontext.abilities[parseInt(abil.$ID)] = build.attributeLevel(abil)
        }
        for (var key in build.Jobs) {
            jsoncontext.jobs[ parseInt(build.Jobs[key].$ID)] = build.jobCircle(build.Jobs[key]);

            let skills = await build.Jobs[key].Link_Skills.toPromise()
            for (var key in skills) {
                let skill = skills[key];
                jsoncontext.skills[parseInt(skill.$ID)] = build.skillLevel(skill);
            };
        }



        for (var key in RemoteLUAService.STATS_RUNTIME_BASE) {
            jsoncontext.stats[key] = RemoteLUAService.STATS_RUNTIME_BASE[key];
        }

        for (var key in RemoteLUAService.STATS_RUNTIME) {
            jsoncontext.stats[key] = context[key];
        }


        //httprequest
        let request = {
            context: jsoncontext,
            region: TOSRegionService.getRegion().toString(),
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

        return result.pipe(map((x:string)=>{
           let obj:any=JSON.parse(x)
           return obj['result'] as string
        })).toPromise()
        
    }

}
