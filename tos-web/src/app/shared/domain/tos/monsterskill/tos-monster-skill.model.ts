import { TOSEntity } from "../tos-entity.model";
import {
    ITOSMonsterSkill,
    ITOSMonster,
    TOSAttackType,
    TOSDataSet,
    TOSElement,
    ITOSAddBuff,
    ITOSBuff,
} from "../tos-domain";
import { TOSDomainService } from "../tos-domain.service";
import { RemoteLUAService } from "../../../service/remote-lua.service";
import { from, Observable, of } from "rxjs";
import { fromPromise } from "rxjs/internal-compatibility";
import { map, mergeAll } from "rxjs/operators";
import { observable } from "rxjs";

export class TOSMonsterSkill extends TOSEntity implements ITOSMonsterSkill {

    constructor(dataset:TOSDataSet,json: any) {
        super(TOSDataSet.MONSTERSKILLS, json);
    }
    get CoolDown(): number {return this.$lazyPropertyNumber("CoolDown")}
    get SkillSR(): number {return this.$lazyPropertyNumber("SkillSR")}
    get Element(): TOSElement{return this.$lazyPropertyEnum('Element',TOSElement)}
    
    get SP(): number{return this.$lazyPropertyNumber("SP")}
    get TypeAttack(): TOSAttackType{return this.$lazyPropertyEnum("TypeAttack",TOSAttackType)}
    get SkillFactor(): number{ return this.$lazyPropertyNumber("SkillFactor")}
    get HitCount(): number{ return this.$lazyPropertyNumber("HitCount")}
    get TargetBuffs(): Observable<ITOSAddBuff[]>{return (this.$lazyPropertyBuffsFromJSONArray('TargetBuffs'))}
    get SelfBuffs(): Observable<ITOSAddBuff[]>{return (this.$lazyPropertyBuffsFromJSONArray('SelfBuffs'))}

    get Link_Monsters(): Observable<ITOSMonster[]>{
        
        return this.$lazyPropertyLink('Link_Monsters', value => TOSDomainService.monstersById(value)) as Observable<ITOSMonster[]> 
    }

    private $lazyPropertyBuffsFromJSONArray(name): Observable<ITOSAddBuff[]>{
        let s:any= this.$lazyPropertyJSONArray(name)
        if (s=='None'){
            return of([])
        }
        let o=from(s)
        

        return o.pipe(map(async (x:string)=>{
            let arr=x.split(';')
            let obj={
                Link_Buff:arr[0],
                Duration:arr[1],
                Chance:arr[2],
            }
            let aa= await TOSDomainService.buffsByIdName(obj.Link_Buff).toPromise()

            return new TOSAddBuff(aa,obj)
        }),
        map(x=>{
            return fromPromise(x)
        }),
        mergeAll()) as  Observable<ITOSAddBuff[]>
    }
}


export class TOSAddBuff extends TOSEntity implements ITOSAddBuff {
    get Link_Buff(): Observable<ITOSBuff>{
        return TOSDomainService.buffsByIdName(this.Link_Buff$ID_NAME)
    }
    readonly Link_Buff$ID_NAME:string;
    readonly Duration: number;
    readonly Chance: number;
    constructor(public readonly Buff:ITOSBuff,json){
        super(TOSDataSet.BUFFS,json)
       
        this.Link_Buff$ID_NAME=json['Link_Buff']
        this.Duration=parseFloat(json['Duration']);
        this.Chance=parseInt(json['Chance']);
        
    }
    get UserRemove(): boolean{
        return this.Buff.UserRemove;
    };
    get $ID(): string{
        return this.Buff.$ID;
    }
    get $ID_NAME(): string{
        return this.Buff.$ID_NAME;
    }
    get Description(): string{
        return this.Buff.Description;
    }
    get Icon(): string{
        return this.Buff.Icon
    }
    get Name(): string{
        return this.Buff.Name
    }
    get Selected(): boolean{
        return this.Buff.Selected
    }
    get Url(): string{
        return this.Buff.Url
    }
}