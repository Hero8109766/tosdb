import { ChangeDetectorRef, Component, Input } from '@angular/core';
import { TOSEquipment } from 'src/app/shared/domain/tos/item/equipment/tos-equipment.model';
import { EntityDetailChildComponent } from "../entity-detail-child.component";

@Component({
    selector: 'tos-entity-detail-Vibora',
    templateUrl: './entity-detail-Vibora.component.html',
    styleUrls: ['./entity-detail-Vibora.component.scss']
})
export class EntityDetailViboraComponent extends EntityDetailChildComponent {

    @Input() divider: boolean;
    @Input() header: boolean;
    get AdditionalOption(): string[] {
        return (this.entity as TOSEquipment).AdditionalOption
    }

    constructor(changeDetector: ChangeDetectorRef) { super(changeDetector) }

}
