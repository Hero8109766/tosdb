import {ChangeDetectorRef, Component, Input} from '@angular/core';
import {EntityDetailChildComponent} from "../entity-detail-child.component";

@Component({
  selector: 'tos-entity-detail-OptDesc',
  templateUrl: './entity-detail-OptDesc.component.html',
  styleUrls: ['./entity-detail-OptDesc.component.scss']
})
export class EntityDetailOptDescComponent extends EntityDetailChildComponent {

  @Input() divider: boolean;
  @Input() header: boolean;

  constructor(changeDetector: ChangeDetectorRef) { super(changeDetector) }

}
