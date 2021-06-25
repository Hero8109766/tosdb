import {
    ChangeDetectionStrategy,
    ChangeDetectorRef,
    Component,
    EventEmitter,
    Input,
    OnChanges,
    Output,
    SimpleChanges,
} from '@angular/core';
import { Sort } from "../../directives/sort.directive";
import { Observable } from "rxjs";
import { Router } from "@angular/router";
import { TableCellLinkPipeDefinition } from "./pipes/table-cell-link.pipe";
import { ITOSEntity } from "../../domain/tos/tos-domain";

@Component({
    changeDetection: ChangeDetectionStrategy.OnPush,
    selector: 'tos-entity-table',
    templateUrl: './entity-table.component.html',
    styleUrls: ['./entity-table.component.scss']
})
export class EntityTableComponent implements OnChanges {

    static readonly ATTRIBUTE_DATA_COLUMN = 'data-column';
    static readonly ATTRIBUTE_DATA_I = 'data-i';
    static readonly ATTRIBUTE_DATA_ROUTER = 'data-router';

    @Input() columns: EntityTableColumn[];
    @Input() data: ITOSEntity[];
    @Input() header: boolean = true;
    @Input() hideMobile: boolean = false;
    @Input() hideTablet: boolean = false;
    @Input() selected: boolean = false;
    @Input() sort: Sort;
    @Output() sortChange: EventEmitter<Sort> = new EventEmitter();
    @Input() themeInvert: boolean = false;

    columnsFiltered: EntityTableColumn[];
    tooltip: ITOSEntity;

    constructor(public changeDetector: ChangeDetectorRef, private router: Router) { }

    ngOnChanges(changes: SimpleChanges): void {
        if (changes.columns && this.columns) {
            this.columnsFiltered = this.columns
                .filter(value =>
                    (!this.hideMobile || this.hideMobile != value.hideMobile) &&
                    (!this.hideTablet || this.hideTablet != value.hideTablet)
                );
        }
        if (changes.data) {
            this.data = this.data && !Array.isArray(this.data) ? [this.data] : this.data;
        }
    }

    onRowMouseClick(event: MouseEvent, row: ITOSEntity) {
        let target = event.target as Element;

        if (target.getAttribute(EntityTableComponent.ATTRIBUTE_DATA_ROUTER)) {
            event.stopPropagation();
            event.stopImmediatePropagation();

            let url = target.getAttribute(EntityTableComponent.ATTRIBUTE_DATA_ROUTER);
            this.router.navigate([url]);
        }
    }
    onRowMouseOver(event: MouseEvent, row: ITOSEntity) {
        let target = event.target as Element;

        if (target.getAttribute(EntityTableComponent.ATTRIBUTE_DATA_COLUMN)) {
            // Show tooltips for linked ITOSEntity lists
            let column = this.columns.find(value => value.pipe.column == target.getAttribute(EntityTableComponent.ATTRIBUTE_DATA_COLUMN));
            let definition = column.pipe as TableCellLinkPipeDefinition;
            let observable = row[definition.column] as Observable<ITOSEntity | ITOSEntity[]>;
            observable.subscribe(value => {
                let array = Array.isArray(value) ? value : [value];
                let entity = array[+target.getAttribute(EntityTableComponent.ATTRIBUTE_DATA_I)];

                this.tooltip = entity;
                this.changeDetector.markForCheck();
            })

        } else {
            this.tooltip = row;
        }

    }
    onRowMouseLeave(event: MouseEvent) {
        this.tooltip = null;
    }

    trackByIndex(index: number, value: ITOSEntity) {
        return index;
    }

}

export interface EntityTableColumn {
    class?: string;

    hideMobile?: boolean;
    hideTablet?: boolean;

    label: string;
    pipe: EntityTablePipeDefinition;
    wide?: boolean;
}

export abstract class EntityTablePipeDefinition {
    protected constructor(public column: string, public pipeClass: any) { }
}
