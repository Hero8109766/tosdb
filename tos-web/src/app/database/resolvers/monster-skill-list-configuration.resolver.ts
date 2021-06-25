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
    resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<TOSListConfiguration> | Promise<TOSListConfiguration> | TOSListConfiguration {
        return {
            sortColumn: '$ID',

            tableColumns: [
                { label: '', pipe: new TableCellIconPipeDefinition('Icon'), class: 'p-1' },
                { label: '$ID', pipe: new TableCellTextPipeDefinition('$ID'), hideMobile: true },
                { label: 'Used by', pipe: new TableCellLinkPipeDefinition('Link_Monsters'), wide: true },
                { label: 'Description', pipe: new TableCellTextPipeDefinition('Description') },
                { label: 'SkillFactor', pipe: new TableCellNumberPipeDefinition('SkillFactor') },
                {
                    label: 'Buff/Debuffs', pipe: new TableCellConvertiblePipeDefinition('TargetBuffs', (obj) => {
                        let arr: Observable<object[]> = obj
                        let p = arr.pipe(
                            map(async (v) => {
                                return v.map(vv=>{
                                    if (vv) {
                                        try {
                                            let vv = new TOSAddBuff(v)
                                            return vv.Link_Buff.pipe(map((buff)=>{
                                                
                                                buff.Url=TOSUrlService.Route('/database/' + TOSDataSetService.toUrl(TOSDataSet.BUFFS) + '/' + buff.$ID)
                                                return {
                                                    Icon: buff.Icon,
                                                    Chance: vv.Chance,
                                                    Url:TOSUrlService.Route('/database/' + TOSDataSetService.toUrl(TOSDataSet.BUFFS) + '/' + buff.$ID)
                                                }
                                            }));
                                            
                                        } catch (e) {
    
                                            return of({
                                                Icon: "Orbis.png",
                                                Chance: -1,
                                                Url:"Fail"
                                            })
                                        }
                                    }
                                }).map(x=>x)
                            }
                            ),
                            map(x => fromPromise(x)),
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
        };
    }
}
