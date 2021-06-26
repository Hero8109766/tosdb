import {
    ChangeDetectionStrategy,
    ChangeDetectorRef,
    Component,
    Input,
    OnChanges,
    OnDestroy,
    SimpleChanges
} from '@angular/core';
import { EntityDetailChildComponent } from "../entity-detail-child.component";
import { Subscription } from "rxjs";
import { ITOSBuild, ITOSSkill } from "../../../domain/tos/tos-domain";
import { faBolt, faTint, faWeightHanging } from "@fortawesome/free-solid-svg-icons";
import { faClock } from "@fortawesome/free-regular-svg-icons";

@Component({
    changeDetection: ChangeDetectionStrategy.OnPush,
    selector: 'tos-entity-detail-MonsterSkill',
    templateUrl: './entity-detail-MonsterSkill.component.html',
    styleUrls: ['./entity-detail-MonsterSkill.component.scss']
})
export class EntityDetailMonsterSkillComponent extends EntityDetailChildComponent {
    @Input() divider: boolean;
    @Input() header: string;
    constructor(changeDetector: ChangeDetectorRef) { super(changeDetector); }

}
