import { ChangeDetectorRef, Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { TOSEquipment, TOSGoddessAnvilMaterial } from 'src/app/shared/domain/tos/item/equipment/tos-equipment.model';
import { ITOSGoddessAnvilMaterial } from 'src/app/shared/domain/tos/tos-domain';
import { EntityDetailChildComponent } from "../entity-detail-child.component";

@Component({
    selector: 'tos-entity-detail-Enhancement',
    templateUrl: './entity-detail-Enhancement.component.html',
    styleUrls: ['./entity-detail-Enhancement.component.scss']
})
export class EntityDetailEnhancementComponent extends EntityDetailChildComponent implements OnChanges {

    @Input() header: string;

    @Input() anvilLevel: number;
    @Output() anvilLevelChange: EventEmitter<number> = new EventEmitter();
    @Input() goddessAnvilLevel: number;
    @Output() goddessAnvilLevelChange: EventEmitter<number> = new EventEmitter();

    anvilAvailable: boolean;
    anvilBonus: number = 0;
    anvilSilver: number = 0;
    anvilSilverTotal: number = 0;
    
    goddessAnvilAvailable: boolean;
    goddessAnvilBonus: number = 0;
    goddessAnvilMaterial: TOSGoddessAnvilMaterial[];
    goddessAnvilMaterialTotal: TOSGoddessAnvilMaterial[];
    goddessAnvilChance:number=100;

    attributeAvailable: boolean;
    attributeLevel: number = 0;
    attributePoints: number = 0;
    attributeSilver: number = 0;
    attributeSilverTotal: number = 0;

    @Input() transcendLevel: number;
    @Output() transcendLevelChange: EventEmitter<number> = new EventEmitter();

    transcendAvailable: boolean;
    transcendBonus: number = 0;
    transcendShards: number = 0;
    transcendShardsTotal: number = 0;

    constructor(changeDetector: ChangeDetectorRef) { super(changeDetector) }

    ngOnChanges(changes: SimpleChanges) {
        super.ngOnChanges(changes);

        this.anvilAvailable = this.equipment && this.equipment.IsAnvilAvailable;
        this.attributeAvailable = !!this.attribute;
        this.transcendAvailable = this.equipment && this.equipment.IsTranscendAvailable;
        this.goddessAnvilAvailable=this.equipment && this.equipment.IsGoddessAnvilAvailable;
    }

    onAnvilChange(newValue) {
        if (this.anvilLevel == newValue) return;

        this.anvilLevel = newValue;
        this.anvilLevelChange.emit(newValue);

        this.anvilBonus = this.equipment.AnvilDEF(this.anvilLevel) || this.equipment.AnvilATK(this.anvilLevel);
        this.anvilSilver = this.equipment.AnvilPrice(this.anvilLevel);
        this.anvilSilverTotal = this.equipment.AnvilPriceTotal(this.anvilLevel);
    }
    onGoddessAnvilChange(newValue) {
        if (this.goddessAnvilLevel == newValue) return;

        this.goddessAnvilLevel = newValue;
        this.goddessAnvilLevelChange.emit(newValue);

        this.goddessAnvilBonus = this.equipment.AnvilDEF(this.goddessAnvilLevel) || this.equipment.AnvilATK(this.goddessAnvilLevel);
        this.goddessAnvilMaterial = this.equipment.GoddessAnvilPrice(this.goddessAnvilLevel);
        this.goddessAnvilMaterialTotal = this.equipment.GoddessAnvilTotalPriceByHalfPercent(this.goddessAnvilLevel);
        this.goddessAnvilChance=TOSEquipment.GoddessAnvilChance(this.goddessAnvilLevel)
        
    }
    onAttributeChange(newValue) {
        if (this.attributeLevel == newValue) return;

        this.attributeLevel = newValue;
        this.attributePoints = this.attribute.Price(this.attributeLevel);
        this.attributeSilver = this.attributePoints * 1000;
        this.attributeSilverTotal = this.attribute.PriceTotal(this.attributeLevel) * 1000;
    }

    onTranscendChange(newValue) {
        if (this.transcendLevel == newValue) return;

        this.transcendLevel = newValue;
        this.transcendLevelChange.emit(newValue);

        this.transcendBonus = this.equipment.TranscendATKRatio(this.transcendLevel);
        this.transcendShards = this.equipment.TranscendPrice(this.transcendLevel);
        this.transcendShardsTotal = this.equipment.TranscendPriceTotal(this.transcendLevel);
    }

    onWheel(event) { } // Do nothing.. just so the user can use the wheel to control the input

}
