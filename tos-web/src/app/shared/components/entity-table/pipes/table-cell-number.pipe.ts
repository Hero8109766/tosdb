import { Pipe } from '@angular/core';
import { EntityTablePipeDefinition } from "../entity-table.component";
import { DomSanitizer, SafeHtml } from "@angular/platform-browser";
import { DecimalPipe } from "@angular/common";
import { TableCellPipeBase } from "./table-cell.pipe";
import { Observable, of } from "rxjs";
import { ITOSEntity } from "../../../domain/tos/tos-domain";

@Pipe({
    name: 'tableCellNumber'
})
export class TableCellNumberPipe extends TableCellPipeBase<TableCellNumberPipeDefinition> {

    constructor(private decimal: DecimalPipe, sanitizer: DomSanitizer) { super(sanitizer) }

    transform(row: ITOSEntity, definition: TableCellNumberPipeDefinition): Observable<SafeHtml> {
        let value = row[definition.column]
        value = definition.converter ? definition.converter(value) : this.decimal.transform(value)
        return of(this.sanitizer.bypassSecurityTrustHtml(`
      <span class="text-right">
        ${value}
      </span>
    `));
    }

}

export class TableCellNumberPipeDefinition extends EntityTablePipeDefinition {
    constructor(
        public column: string,
        public converter?: (value: number) => any
    ) { super(column, TableCellNumberPipe); }
}
