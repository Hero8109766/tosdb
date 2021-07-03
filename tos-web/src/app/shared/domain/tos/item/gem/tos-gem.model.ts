import { TOSItem } from "../tos-item.model";
import { ITOSGem, ITOSGemBonus, ITOSSkill, TOSDataSet, TOSGemSlot, TOSGemType, TOSStat } from "../../tos-domain";
import { TOSDomainService } from "../../tos-domain.service";
import { Observable, of } from "rxjs";
import { RemoteLUAService } from "src/app/shared/service/remote-lua.service";
import { fromPromise } from "rxjs/internal-compatibility";
import { map } from "rxjs/operators";

export class TOSGem extends TOSItem implements ITOSGem {

    constructor(json: TOSGem) {
        super(TOSDataSet.GEMS, json);
    }

    get BonusBoots() { return this.$lazyPropertyJSONArray('BonusBoots', value => new TOSGemBonus(value)) }
    get BonusGloves() { return this.$lazyPropertyJSONArray('BonusGloves', value => new TOSGemBonus(value)) }
    get BonusSubWeapon() { return this.$lazyPropertyJSONArray('BonusSubWeapon', value => new TOSGemBonus(value)) }
    get BonusTopAndBottom() { return this.$lazyPropertyJSONArray('BonusTopAndBottom', value => new TOSGemBonus(value)) }
    get BonusWeapon() { return this.$lazyPropertyJSONArray('BonusWeapon', value => new TOSGemBonus(value)) }

    get Link_Skill() { return this.$lazyPropertyLink('Link_Skill', value => TOSDomainService.skillsById(value)) as Observable<ITOSSkill> }

    get TypeGem() { return this.$lazyPropertyEnum('TypeGem', TOSGemType) }
    get SpendRP() { return this.$lazyPropertyNumber("SpendRP")}
    
    get RelicGemOption() { return this.$lazyPropertyString("RelicGemOption")}
    get CoolDown() { return this.$lazyPropertyNumber("CoolDown")}
    get RelicReleaseOptionText$() { 
        return fromPromise(RemoteLUAService.evalRelic(this.$ID,"!RelicReleaseOptions",this.RelicGemOption))
    }
    GetRelicOptionByLevelText$(level:number) { 
        return fromPromise(RemoteLUAService.evalRelic(this.$ID,"!RelicByLevel",this.RelicGemOption,level))
    }
    get IsSpendRPPerSec(){
        return this.TypeGem==TOSGemType.MAGENTA
    }
    get IsEther(){
        return this.TypeGem==TOSGemType.ETHER;
    }
    get IsRelic(){
        return this.TypeGem==TOSGemType.CYAN || this.TypeGem==TOSGemType.MAGENTA || this.TypeGem==TOSGemType.BLACK;
    }
    get IsNormalGem(){
        return !this.IsRelic && !this.IsEther 
    }
    GetEtherProp$(level:number){
        if(!this.IsEther){
            return of("Fail")
        }
        return fromPromise(RemoteLUAService.evalEther(this.$ID,"!EtherPropList",level))
    }
    Bonus(level: number): { [key: string]: TOSGemBonus[] } {
        return Object
            .values(TOSGemSlot)
            .reduce((result, slot, i) => {
                if (this['Bonus' + slot])
                    result[slot] = [
                        this['Bonus' + slot][(level - 1) * 2],
                        this['Bonus' + slot][(level - 1) * 2 + 1]
                    ];

                return result;
            }, {})
    }

}

export class TOSGemBonus implements ITOSGemBonus {
    Stat: string | TOSStat;
    Value: number;

    constructor(json: TOSGemBonus) {
        this.Stat = Object.values(TOSStat)[+json.Stat] || json.Stat;
        this.Value = +json.Value;
    }

    toString(): string {
        let string = isNaN(this.Value)
            ? this.Stat as string
            : this.Stat + ' ' + (this.Value > 0 ? '+ ' : this.Value < 0 ? '- ' : '') + Math.abs(this.Value);

        string = string.split('+').join('<span class="text-success">▲</span>');
        if (this.Value < 0) string = string.split('-').join('<span class="text-danger">▼</span>');

        return string;
    }

}
