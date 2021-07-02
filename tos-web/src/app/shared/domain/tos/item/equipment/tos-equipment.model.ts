import { TOSEntity } from "../../tos-entity.model";
import { TOSItem } from "../tos-item.model";
import {
    ITOSEquipment,
    ITOSEquipmentBonus,
    ITOSEquipmentSet,
    ITOSGoddessAnvilMaterial,
    ITOSItem,
    TOSAttackType,
    TOSClassTree,
    TOSDataSet,
    TOSEquipmentGrade,
    TOSEquipmentGradeService,
    TOSEquipmentMaterial,
    TOSEquipmentType,
    TOSStat,
    TOSStatService
} from "../../tos-domain";
import { TOSDomainService } from "../../tos-domain.service";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

export class TOSEquipment extends TOSItem implements ITOSEquipment {
    constructor(json: TOSEquipment) {
        super(TOSDataSet.EQUIPMENT, json);

        this.$comparators['Grade'] = TOSEquipmentGradeService.comparator;
    }
    get AdditionalOption() {
        let array=[];
        let hascontents=false
        for(let i=1;i<=2;i++){
            let desc=this.$lazyPropertyString('AdditionalOption_'+i.toString())
            
            if(desc=="None"){
                desc=""
            }else{
                hascontents=true
            }
            desc=this.tooltipToHTMLGeneric(desc)
            array.push(desc);
        }
        if(!hascontents){
            return undefined
        }
        return array;
    }

    get Bonus() { return this.$lazyPropertyJSONArray('Bonus', value => new TOSEquipmentBonus(value), (a, b) => TOSStatService.comparator(a.Stat, b.Stat)) }
    get Durability() { return this.$lazyPropertyNumber('Durability') }
    get Grade() { return this.$lazyPropertyEnum('Grade', TOSEquipmentGrade) }

    get IsAnvilAvailable(): boolean { return this.Grade!=TOSEquipmentGrade.GODDESS && (this.AnvilATK(1) > 0 || this.AnvilDEF(1) > 0) && this.AnvilPrice(1) > 0; }
    get IsGoddessAnvilAvailable(): boolean { return this.Grade==TOSEquipmentGrade.GODDESS && this.$lazyPropertyString("Reinforce_Type")=='goddess' && this.Level >=460 }
    get IsTranscendAvailable(): boolean { return this.TranscendPrice(1) > 0; }

    get Link_Set() { return this.$lazyPropertyLink('Link_Set', value => TOSDomainService.equipmentSetsById(value)) as Observable<ITOSEquipmentSet> }

    get Level() { return this.$lazyPropertyNumber('Level') }
    get Material() { return this.$lazyPropertyEnum('Material', TOSEquipmentMaterial) }
    get Potential() { return this.$lazyPropertyNumber('Potential') }
    get RequiredClass() { return this.$lazyPropertyString('RequiredClass') }
    get RequiredLevel() { return this.$lazyPropertyNumber('RequiredLevel') }
    get Sockets() { return this.$lazyPropertyNumber('Sockets') }
    get SocketsLimit() { return this.$lazyPropertyNumber('SocketsLimit') }
    get Stars() { return this.$lazyPropertyNumber('Stars') }
    get Stat_ATTACK_MAGICAL() { return this.$lazyPropertyNumber('Stat_ATTACK_MAGICAL') }
    get Stat_ATTACK_PHYSICAL_MAX() { return this.$lazyPropertyNumber('Stat_ATTACK_PHYSICAL_MAX') }
    get Stat_ATTACK_PHYSICAL_MIN() { return this.$lazyPropertyNumber('Stat_ATTACK_PHYSICAL_MIN') }
    get Stat_DEFENSE_MAGICAL() { return this.$lazyPropertyNumber('Stat_DEFENSE_MAGICAL') }
    get Stat_DEFENSE_PHYSICAL() { return this.$lazyPropertyNumber('Stat_DEFENSE_PHYSICAL') }
    get TypeAttack() { return this.$lazyPropertyEnum('TypeAttack', TOSAttackType) }
    get TypeEquipment() { return this.$lazyPropertyEnum('TypeEquipment', TOSEquipmentType) }
    get Unidentified() { return this.$lazyPropertyBoolean('Unidentified') }
    get UnidentifiedRandom() { return this.$lazyPropertyBoolean('UnidentifiedRandom') }
    get AnvilLimit(){
        return this.$lazyPropertyNumber("MaxReinforcePoint")
    }
    IsUsableBy(classTree: TOSClassTree): boolean {
        let index = Object.values(TOSClassTree).indexOf(classTree);
        return this.RequiredClass[index] == 'T';
    }

    AnvilATK(level: number) {
        let anvilATK = this.$lazyPropertyJSONArray('AnvilATK') as number[];
        return level > 0 && anvilATK && anvilATK[level - 1] || 0;
    }
    AnvilDEF(level: number) {
        let anvilDEF = this.$lazyPropertyJSONArray('AnvilDEF') as number[];
        return level > 0 && anvilDEF && anvilDEF[level - 1] || 0;
    }
    AnvilPrice(level: number) {
        let anvilPrice = this.$lazyPropertyJSONArray('AnvilPrice') as number[];
        return level > 0 && anvilPrice && anvilPrice[level - 1] || 0;
    }
    AnvilPriceTotal(level: number) {
        return Array.from({ length: level + 1 }, (x, i) => this.AnvilPrice(i)).reduce((a, b) => a + b, 0)
    }
    GoddessAnvilPrice(level:number){
        let materials:string[][][]=this.$lazyPropertyJSONArray("GoddessReinforceMaterials")
        let result:TOSGoddessAnvilMaterial[]=[]
        if(level>0){
            for(let i=0;i<materials[level-1].length;i++){
                result.push(new TOSGoddessAnvilMaterial(materials[level-1][i]))
            }
        }
        return result
    }
    GoddessAnvilTotalPrice(level:number){
        let materials:TOSGoddessAnvilMaterial[]=[]
        if(level>0){
            for(let lv=1;lv<=level;lv++){
                let mat=this.GoddessAnvilPrice(lv)
                for(let matindex in mat){
                    let m=mat[matindex]
                    if(materials.some((x)=> m.Material$ID_NAME==x.Material$ID_NAME)){
                        let match=materials.findIndex((x)=> m.Material$ID_NAME==x.Material$ID_NAME)
                        materials[match].Amount+=m.Amount;
                    }else{
                        materials.push(m)
                    }
                }
            }
        }
        return materials
    }
    static GoddessAnvilChance(level:number){
        let table=[
            100,100,100,100,100,80,60,45,30,20,15,10,8,7.5,6,4.5,3,2,1   
        ]
        if(table.length < level){
            return 1.0
        }
        return table[level-1]
    }
    static GoddessAnvilTotalChance(level:number){
        let accumulatedChance=1;
        for(let lv=1;lv<=level;lv++){
            accumulatedChance*=TOSEquipment.GoddessAnvilChance(lv)/100.0
        }
        return accumulatedChance*100.0
    }
    GoddessAnvilTotalPriceByHalfPercent(level:number){
        let chance=TOSEquipment.GoddessAnvilTotalChance(level)
        if(chance>=50.0){
            return this.GoddessAnvilTotalPrice(level);
        }
       
        let accumulatedMaterials:TOSGoddessAnvilMaterial[]=[]
        for(let lv=1;lv<=level;lv++){
            let chance=TOSEquipment.GoddessAnvilChance(lv);
            // number of attempt >= log(1- success rate)/log(1-chance)
            //miss=1-chance
            //succ=0.5
            //https://dskjal.com/statistics/the-probability-of-gacha.html#binominal
            var attempts=1
            if(chance<100){
                attempts=Math.ceil(Math.log10(0.5)/Math.log10(1-chance/100))
            }
            //calc materials
            let mats=this.GoddessAnvilPrice(lv)
            for(var k in mats){
                let index=accumulatedMaterials.findIndex(x=>x.Material$ID_NAME==mats[k].Material$ID_NAME)
                if(index>=0){
                    accumulatedMaterials[index].Amount+=mats[k].Amount*attempts
                }else{
                    let idx=accumulatedMaterials.push(mats[k])
                    accumulatedMaterials[idx-1].Amount*=attempts;
                }
            }

        }
        return accumulatedMaterials
    }

    TranscendATKRatio(level: number) { if(this.Grade==TOSEquipmentGrade.GODDESS)return level*0.03; return level * 0.1; }
    TranscendMDEFRatio(level: number) { if(this.Grade==TOSEquipmentGrade.GODDESS)return level*0.03; return level * 0.1;  }
    TranscendPDEFRatio(level: number) { if(this.Grade==TOSEquipmentGrade.GODDESS)return level*0.03; return level * 0.1;  }
    TranscendPrice(level: number) {
        let transcendPrice = this.$lazyPropertyJSONArray('TranscendPrice') as number[];
        return level > 0 && transcendPrice && transcendPrice[level - 1] || 0;
    }
    TranscendPriceTotal(level: number) {
        for (var sum = 0, i = 1; i <= level; i++)
            sum += this.TranscendPrice(i);

        return sum;
    }

}
export class TOSGoddessAnvilMaterial implements ITOSGoddessAnvilMaterial{
    get Material$(){
        return TOSDomainService.itemsByIdName(this.Material$ID_NAME)
    }

    Material$ID_NAME:string;
    Amount: number;
    constructor(json: string[]) {
        this.Material$ID_NAME=json[0]
        this.Amount=parseInt(json[1])
        
    }
}
export class TOSEquipmentBonus implements ITOSEquipmentBonus {
    Stat: TOSStat;
    Value: number;
    ValueHTML: string;

    constructor(json: string[]) {
        this.Stat = Object.values(TOSStat)[+json[0]];
        this.Value = isNaN(+json[1]) ? null : +json[1];
        this.ValueHTML = isNaN(+json[1]) ? json[1] : null;

        // HotFix: add special bonus' arrows
        if (this.ValueHTML) {
            this.ValueHTML = this.ValueHTML.split('{img green_up_arrow 16 16}').join('<span class="text-success">▲</span> ');
            this.ValueHTML = this.ValueHTML.split('{img red_down_arrow 16 16}').join('<span class="text-danger">▼</span> ');
        }
    }
}

// Note: we can't put this one on a separate class otherwise it generates a circular dependency
export class TOSEquipmentSet extends TOSEntity implements ITOSEquipmentSet {

    constructor(private json: TOSEquipmentSet) {
        super(TOSDataSet.EQUIPMENT_SETS, json);
    }

    get Bonus(): { [key: number]: TOSEquipmentBonus[] } {
        let result = [this.Bonus2, this.Bonus3, this.Bonus4, this.Bonus5, this.Bonus6, this.Bonus7]
            .map(bonusGroup => (bonusGroup || '')
                .split('{nl}')
                .map(bonus => bonus ? new TOSEquipmentBonus([TOSStat.UNKNOWN.toString(), bonus]) : null)
                .filter(bonus => bonus))
            .reduce((result, bonusGroup, i) => {
                if (bonusGroup.length) result[i + 2] = bonusGroup;
                return result;
            }, {});

        return result;
    }
    get Bonus2() { return this.$lazyPropertyString('Bonus2') }
    get Bonus3() { return this.$lazyPropertyString('Bonus3') }
    get Bonus4() { return this.$lazyPropertyString('Bonus4') }
    get Bonus5() { return this.$lazyPropertyString('Bonus5') }
    get Bonus6() { return this.$lazyPropertyString('Bonus6') }
    get Bonus7() { return this.$lazyPropertyString('Bonus7') }
    get Icon(): string { throw new Error('Unsupported operation') }
    get Icon$() { return this.Link_Items.pipe(map(value => value && value[0].Icon)) }
    get Url(): string { throw new Error('Unsupported operation') }
    get Url$() { return this.Link_Items.pipe(map(value => value && value[0].Url)) }

    get Link_Items() { return this.$lazyPropertyLink('Link_Items', value => TOSDomainService.itemsByIdLink(value)) as Observable<ITOSItem[]> }

}
