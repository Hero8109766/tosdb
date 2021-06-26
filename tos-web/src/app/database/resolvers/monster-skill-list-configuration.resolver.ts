import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from "@angular/router";
import { Observable, of } from "rxjs";
import { Injectable } from "@angular/core";
import { TOSListConfiguration } from "../entity-list/entity-list.component";
import { TableCellIconPipeDefinition } from "../../shared/components/entity-table/pipes/table-cell-icon.pipe";
import { TableCellTextPipeDefinition } from "../../shared/components/entity-table/pipes/table-cell-text.pipe";
import { TableCellLinkPipeDefinition } from "src/app/shared/components/entity-table/pipes/table-cell-link.pipe";
import { TableCellNumberPipeDefinition } from "src/app/shared/components/entity-table/pipes/table-cell-number.pipe";
import { TableCellConvertiblePipeDefinition } from "src/app/shared/components/entity-table/pipes/table-cell-convertible.pipe";
import { TOSDomainService } from "src/app/shared/domain/tos/tos-domain.service";
import { ITOSAddBuff, ITOSBuff, TOSDataSet, TOSDataSetService } from "src/app/shared/domain/tos/tos-domain";
import { fromPromise } from "rxjs/internal-compatibility";
import { TOSAddBuff, TOSMonsterSkill } from "src/app/shared/domain/tos/monsterskill/tos-monster-skill.model";
import { map, mergeAll } from "rxjs/operators";
import { TOSUrlService } from "src/app/shared/service/tos-url.service";


@Injectable()
export class MonsterSkillListConfigurationResolver implements Resolve<TOSListConfiguration> {
    static readonly COLUMNS=[
        { label: '', pipe: new TableCellIconPipeDefinition('Icon'), class: 'p-1' },
        { label: '$ID', pipe: new TableCellTextPipeDefinition('$ID'), hideMobile: true },
        { label: 'Used by', pipe: new TableCellLinkPipeDefinition('Link_Monsters'), wide: true },
        { label: 'Description', pipe: new TableCellTextPipeDefinition('Description') },
        { label: 'AOE', pipe: new TableCellNumberPipeDefinition('SkillSR') },
        { label: 'CoolDown', pipe: new TableCellNumberPipeDefinition('CoolDown',x=>{return (x/1000.0).toString()+"sec"}) },
        { label: 'SkillFactor', pipe: new TableCellNumberPipeDefinition('SkillFactor',(v)=>v.toString()+"%") },
        {
            label: 'Buff/Debuffs', pipe: new TableCellConvertiblePipeDefinition('TargetBuffs', (obj) => {
                let arr: Observable<TOSAddBuff[]|TOSAddBuff> = obj
                let p = arr && arr.pipe(
                    map( (v) => {
                        v=Array.isArray(v)?v:[v]
                        return v.map(vv => {
                            if (vv) {
                                try {
                                  
                                
                                        //vv['Url']=TOSUrlService.Route('/database/' + TOSDataSetService.toUrl(TOSDataSet.BUFFS) + '/' + vv.$ID)
                                        return vv
                                    

                                } catch (e) {

                                    return {
                                        Icon: "Orbis.png",
                                        Chance: -1,
                                        Url: "Fail"
                                    }
                                }
                            }
                        }).map(x => x)
                    }
                    ),
                    mergeAll())

                return p
            }, (v) => {
                if (v.Chance < 0) {
                    return "?"
                } else {
                    return v.Chance.toString() + "%"
                }
            }), wide: true
        }
    ]
    static readonly COLUMNS_MONSTERSKILLS_MINI=[
        { label: '', pipe: new TableCellIconPipeDefinition('Icon'), class: 'p-1' },
        
        { label: 'Description', pipe: new TableCellTextPipeDefinition('Description') },
        { label: 'AOE', pipe: new TableCellNumberPipeDefinition('SkillSR') },
        { label: 'CoolDown', pipe: new TableCellNumberPipeDefinition('CoolDown',x=>{return (x/1000.0).toString()+"sec"}) },
        { label: 'SkillFactor', pipe: new TableCellNumberPipeDefinition('SkillFactor',(v)=>v.toString()+"%") },
        {
            label: 'Buff/Debuffs', pipe: new TableCellConvertiblePipeDefinition('TargetBuffs', (obj) => {
                let arr: Observable<TOSAddBuff[]|TOSAddBuff> = obj
                let p = arr && arr.pipe(
                    map( (v) => {
                        v=Array.isArray(v)?v:[v]
                        return v.map(vv => {
                            if (vv) {
                                try {
                                  
                                
                                        //vv['Url']=TOSUrlService.Route('/database/' + TOSDataSetService.toUrl(TOSDataSet.BUFFS) + '/' + vv.$ID)
                                        return vv
                                    

                                } catch (e) {

                                    return {
                                        Icon: "Orbis.png",
                                        Chance: -1,
                                        Url: "Fail"
                                    }
                                }
                            }
                        }).map(x => x)
                    }
                    ),
                    mergeAll())

                return p
            }, (v) => {
                if (v.Chance < 0) {
                    return "?"
                } else {
                    return v.Chance.toString() + "%"
                }
            }), wide: true
        }
    ]
    resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<TOSListConfiguration> | Promise<TOSListConfiguration> | TOSListConfiguration {
        return {
            sortColumn: '$ID',

            tableColumns: MonsterSkillListConfigurationResolver.COLUMNS
        };
    }
}
