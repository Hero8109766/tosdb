import {
    ITOSItem,
    ITOSMap,
    ITOSMonster,
    ITOSMonsterLinkItem,
    ITOSMonsterLinkMap,
    ITOSMonsterLinkMonsterSkill,
    ITOSMonsterSkill,
    TOSDataSet,
    TOSElement,
    TOSEquipmentMaterial,
    TOSMonsterRace,
    TOSMonsterRank,
    TOSMonsterRankService,
    TOSMonsterSize,
    TOSMonsterSizeService,
    TOSMonsterType
} from "../tos-domain";
import { TOSDomainService } from "../tos-domain.service";
import { Observable } from "rxjs";
import { fromPromise } from "rxjs/internal-compatibility";
import { TOSEntity, TOSEntityLink } from "../tos-entity.model";

export class TOSMonster extends TOSEntity implements ITOSMonster {

    constructor(dataset: TOSDataSet, json: TOSMonster) {
        super(TOSDataSet.MONSTERS, json);

        this.$comparators['Rank'] = TOSMonsterRankService.comparator;
        this.$comparators['Size'] = TOSMonsterSizeService.comparator;

        this.Selected = this.Type != TOSMonsterType.MONSTER;
    }

    get Armor() { return this.$lazyPropertyEnum('Armor', TOSEquipmentMaterial) }
    get Element() { return this.$lazyPropertyEnum('Element', TOSElement) }
    get EXP() { return this.$lazyPropertyNumber('EXP') }
    get EXPClass() { return this.$lazyPropertyNumber('EXPClass') }
    get Level() { return this.$lazyPropertyNumber('Level') }
    get Race() { return this.$lazyPropertyEnum('Race', TOSMonsterRace) }
    get Rank() { return this.$lazyPropertyEnum('Rank', TOSMonsterRank) }
    get Size() { return this.$lazyPropertyEnum('Size', TOSMonsterSize) }
    get Stat_CON() { return this.$lazyPropertyNumber('Stat_CON') }
    get Stat_DEX() { return this.$lazyPropertyNumber('Stat_DEX') }
    get Stat_INT() { return this.$lazyPropertyNumber('Stat_INT') }
    get Stat_SPR() { return this.$lazyPropertyNumber('Stat_SPR') }
    get Stat_STR() { return this.$lazyPropertyNumber('Stat_STR') }
    get Stat_HP() { return this.$lazyPropertyNumber('Stat_HP') }
    get Stat_SP() { return this.$lazyPropertyNumber('Stat_SP') }
    get Stat_ATTACK_MAGICAL_MAX() { return this.$lazyPropertyNumber('Stat_ATTACK_MAGICAL_MAX') }
    get Stat_ATTACK_MAGICAL_MIN() { return this.$lazyPropertyNumber('Stat_ATTACK_MAGICAL_MIN') }
    get Stat_ATTACK_PHYSICAL_MAX() { return this.$lazyPropertyNumber('Stat_ATTACK_PHYSICAL_MAX') }
    get Stat_ATTACK_PHYSICAL_MIN() { return this.$lazyPropertyNumber('Stat_ATTACK_PHYSICAL_MIN') }
    get Stat_DEFENSE_MAGICAL() { return this.$lazyPropertyNumber('Stat_DEFENSE_MAGICAL') }
    get Stat_DEFENSE_PHYSICAL() { return this.$lazyPropertyNumber('Stat_DEFENSE_PHYSICAL') }
    get Stat_Accuracy() { return this.$lazyPropertyNumber('Stat_Accuracy') }
    get Stat_Evasion() { return this.$lazyPropertyNumber('Stat_Evasion') }
    get Stat_CriticalDamage() { return this.$lazyPropertyNumber('Stat_CriticalDamage') }
    get Stat_CriticalDefense() { return this.$lazyPropertyNumber('Stat_CriticalDefense') }
    get Stat_CriticalRate() { return this.$lazyPropertyNumber('Stat_CriticalRate') }
    get Stat_BlockPenetration() { return this.$lazyPropertyNumber('Stat_BlockPenetration') }
    get Stat_BlockRate() { return this.$lazyPropertyNumber('Stat_BlockRate') }
    get Type() { return this.$lazyPropertyEnum('Type', TOSMonsterType) }

    get Link_Items() { return this.$lazyPropertyLink('Link_Items', value => this.TOSMonsterLinkItem(value)) as Observable<TOSMonsterLinkItem[]> }
    get Link_Maps() { return this.$lazyPropertyLink('Link_Maps', value => this.TOSMonsterLinkMap(value)) as Observable<TOSMonsterLinkMap[]> }
    get Link_MonsterSkills(): Observable<ITOSMonsterLinkMonsterSkill[]> {
        return this.$lazyPropertyLink('Link_MonsterSkills',
            value => this.TOSMonsterLinkMonsterSkill(value)) as Observable<ITOSMonsterLinkMonsterSkill[]>
    }

    private TOSMonsterLinkItem(value: TOSMonsterLinkItem): Observable<TOSMonsterLinkItem> {
        return fromPromise((async () => {
            let object = new TOSMonsterLinkItem(value);
            object.Item = await TOSDomainService.itemsByIdLink(object.Item.$ID).toPromise();

            return object;
        })());
    }
    private TOSMonsterLinkMap(value: TOSMonsterLinkMap): Observable<TOSMonsterLinkMap> {
        return fromPromise((async () => {
            let object = new TOSMonsterLinkMap(value);
            object.Map = await TOSDomainService.mapsById(object.Map.$ID).toPromise();

            return object;
        })());
    }
    private TOSMonsterLinkMonsterSkill(value: string): Observable<TOSMonsterLinkMonsterSkill> {
        return fromPromise((async () => {
            let object = new TOSMonsterLinkMonsterSkill();
            object.MonsterSkill = await TOSDomainService.monster_skillsById(value).toPromise();

            return object;
        })());
    }

}

export class TOSMonsterLinkItem extends TOSEntityLink<ITOSItem> implements ITOSMonsterLinkItem {
    Chance: number;
    Item: ITOSItem;
    Quantity_MAX: number;
    Quantity_MIN: number;

    constructor(json: TOSMonsterLinkItem) {
        super();

        this.Chance = +json.Chance;
        this.Item = json.Item;
        this.Quantity_MAX = +json.Quantity_MAX;
        this.Quantity_MIN = +json.Quantity_MIN;
    }

    get Link() { return this.Item }

}

export class TOSMonsterLinkMap extends TOSEntityLink<ITOSMap> implements ITOSMonsterLinkMap {
    Map: ITOSMap;
    Population: number;
    TimeRespawn: number;

    constructor(json: TOSMonsterLinkMap) {
        super();

        this.Map = json.Map;
        this.Population = +json.Population;
        this.TimeRespawn = +json.TimeRespawn;
    }

    get Link() { return this.Map }

}
export class TOSMonsterLinkMonsterSkill extends TOSEntityLink<ITOSMonsterSkill> implements ITOSMonsterLinkMonsterSkill {
    MonsterSkill: ITOSMonsterSkill;

    constructor(json?: TOSMonsterLinkMonsterSkill) {
        super();
        if(json)
            this.MonsterSkill = json.MonsterSkill;
    }

    get Link() { return this.MonsterSkill }
    
    get CoolDown() { return this.Link.CoolDown }
    get SkillSR() { return this.Link.SkillSR }
    get SkillFactor() { return this.Link.SkillFactor }
    get TargetBuffs() { return this.Link.TargetBuffs }
    get SelfBuffs() { return this.Link.SelfBuffs }

}
