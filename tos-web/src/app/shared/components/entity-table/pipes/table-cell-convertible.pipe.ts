import { ChangeDetectorRef, Pipe } from '@angular/core';
import { EntityTableComponent, EntityTablePipeDefinition } from "../entity-table.component";
import { DomSanitizer, SafeHtml } from "@angular/platform-browser";
import { Observable, of } from "rxjs";
import { map, mergeAll } from "rxjs/operators";
import { TableCellPipeBase } from "./table-cell.pipe";
import { ITOSEntity } from "../../../domain/tos/tos-domain";

import { fromPromise } from 'rxjs/internal-compatibility';

@Pipe({
    name: 'tableCellConvertible'
})
export class TableCellConvertiblePipe extends TableCellPipeBase<TableCellConvertiblePipeDefinition> {

    constructor(sanitizer: DomSanitizer) { super(sanitizer) }

    transform(row: ITOSEntity, definition: TableCellConvertiblePipeDefinition, changeDetector: ChangeDetectorRef): Observable<SafeHtml> {
        let obj:Observable<object> = row[definition.column]
        let value = definition.converter ? definition.converter(obj) : obj;


        return obj && obj.pipe(
            map(async v => {

                let html: string = '';
                let array:Observable<any>[] = Array.isArray(v) ? v : [v];


                for (let i = 0; i < array.length; i++) {
                    let entity = await array[i].toPromise()

                    let value = definition.transformValue ? definition.transformValue(entity) : null;

                    html +=
                        `<a href="${entity.Url}" class="d-block position-relative mr-1" style="height: 40px; width: 40px">
                     <img height="40" width="40" class="position-absolute" style="top: 0; left: 0"
                          ${EntityTableComponent.ATTRIBUTE_DATA_COLUMN}="${definition.column}"
                          ${EntityTableComponent.ATTRIBUTE_DATA_I}="${i}"
                          ${EntityTableComponent.ATTRIBUTE_DATA_ROUTER}="${entity.Url}"
                          src="${entity.Icon}" />
                    ` + (value != null ? `
                            <span class="position-absolute text-outline text-white"
                                style="bottom: 0; right: 0.25rem; pointer-events: none">${value}</span>
                    ` : '') + `
                        </a>`

                }
                changeDetector.detectChanges();
                return this.sanitizer.bypassSecurityTrustHtml('<span class="d-flex">' + html + '</span>');
            }),
            map(x => fromPromise(x)),
            mergeAll());
    }

}

export class TableCellConvertiblePipeDefinition extends EntityTablePipeDefinition {
    constructor(
        public column: string,
        public converter: (obj: any) => Observable<any>,
        public transformValue?: (value: any) => string,
    ) {
        super(column, TableCellConvertiblePipe);


    }
}
