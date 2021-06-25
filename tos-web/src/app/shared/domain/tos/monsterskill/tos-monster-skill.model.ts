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
import { Observable, of } from "rxjs";
import { fromPromise } from "rxjs/internal-compatibility";
import { map } from "rxjs/operators";
import { observable } from "rxjs";

export class TOSMonsterSkill extends TOSEntity implements ITOSMonsterSkill {

    constructor(dataset:TOSDataSet,json: any) {
        super(TOSDataSet.MONSTERSKILLS, json);
    }
    get CoolDown(): number {return this.$lazyPropertyNumber("CoolDown")}
    get Element(): TOSElement{return this.$lazyPropertyEnum('Element',TOSElement)}
    get SP(): number{return this.$lazyPropertyNumber("SP")}
    get TypeAttack(): TOSAttackType{return this.$lazyPropertyEnum("TypeAttack",TOSAttackType)}
    get SkillFactor(): number{ return this.$lazyPropertyNumber("SkillFactor")}
    get HitCount(): number{ return this.$lazyPropertyNumber("HitCount")}
    get TargetBuffs(): Observable<ITOSAddBuff[]>{return of(this.$lazyPropertyBuffsFromJSONArray('TargetBuffs'))}
    get SelfBuffs(): Observable<ITOSAddBuff[]>{return of(this.$lazyPropertyBuffsFromJSONArray('SelfBuffs'))}

    get Link_Monsters(): Observable<ITOSMonster[]>{
        
        return this.$lazyPropertyLink('Link_Monsters', value => TOSDomainService.monstersById(value)) as Observable<ITOSMonster[]> 
    }

    private $lazyPropertyBuffsFromJSONArray(name): ITOSAddBuff[]{
        let s:any= this.$lazyPropertyJSONArray(name)
        if (s=='None'){
            return []
        }
        return s && s.map(x=>{
            let arr=x.split(';')
            let obj={
                Link_Buff:arr[0],
                Duration:arr[1],
                Chance:arr[2],
            }
            
            return new TOSAddBuff(obj)
        });
    }
}


export class TOSAddBuff implements ITOSAddBuff {
    get Link_Buff(): Observable<ITOSBuff>{
        return TOSDomainService.buffsByIdName(this.Link_Buff$ID_NAME)
    }
    readonly Link_Buff$ID_NAME:string;
    readonly Duration: number;
    readonly Chance: number;

    constructor(json:object){

       
        this.Link_Buff$ID_NAME=json['Link_Buff']
        this.Duration=parseFloat(json['Duration']);
        this.Chance=parseInt(json['Chance']);
        
    }
}