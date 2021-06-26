import { ChangeDetectorRef, Pipe } from '@angular/core';
import { EntityTablePipeDefinition } from "../entity-table.component";
import { DomSanitizer, SafeHtml } from "@angular/platform-browser";
import { TableCellPipeBase } from "./table-cell.pipe";
import { Observable, of } from "rxjs";
import { ITOSEntity } from "../../../domain/tos/tos-domain";
import { PercentPipe } from "@angular/common";
import { TimePipe } from "../../../directives/time.pipe";
import { TagToHtml } from 'src/app/shared/utils/tag-to-html';
import { map } from 'rxjs/operators';

@Pipe({
    name: 'tableCellText'
})
export class TableCellTextPipe extends TableCellPipeBase<TableCellTextPipeDefinition> {

    constructor(private percent: PercentPipe, sanitizer: DomSanitizer, private time: TimePipe) { super(sanitizer) }

    transform(entity: ITOSEntity, definition: TableCellTextPipeDefinition, changeDetector: ChangeDetectorRef): Observable<SafeHtml> {
        let html = '';
        let src=entity[definition.column]

        
        let func=(sr)=>{
            if(sr){
                sr=definition.converter ?definition.converter(sr):sr
                let content=TagToHtml.ConvertTagToHTML(sr.toString())
                    
                if (definition.format != null) {
                    
                    switch (definition.format) {
                        case TableCellTextPipeFormat.MULTILINE:
                            html = `<span class="text-multiline">${content}</span>`;
                            break;
                        case TableCellTextPipeFormat.PERCENTAGE:
                            html = `<span>${this.percent.transform(parseFloat(content) / 100, '1.1-5')}</span>`;
                            break;
                        case TableCellTextPipeFormat.QUANTITY:
                            html = `<span>&times; ${content}</span>`;
                            break;
                        case TableCellTextPipeFormat.QUANTITY_RANGE:
                            let quantityMin = entity[definition.column.split('.')[0]];
                            let quantityMax = entity[definition.column.split('.')[1]];

                            if (quantityMin > 0 || quantityMax > 0)
                                if (quantityMax != quantityMin)
                                    html = `<span>&times; ${quantityMin}~${quantityMax}</span>`;
                                else
                                    html = `<span>&times; ${quantityMin}</span>`;
                            break;
                        case TableCellTextPipeFormat.TIME:
                            html = `<span>${this.time.transform(content)}</span>`;
                            break;
                    }
                } else {
                    html = `<span>${content}</span>`;
                }
                return this.sanitizer.bypassSecurityTrustHtml(html)
            }
        }

        //if(src instanceof Observable){
        //    return src.pipe(map(src2=>{
        //        changeDetector.detectChanges();
        //        return func(src2)
        //    }))
        //}else{
            return of(func(src));
        //}
    }

}

export class TableCellTextPipeDefinition extends EntityTablePipeDefinition {
    constructor(
        public column: string,
        public format?: TableCellTextPipeFormat,
        public converter?: (src:any)=>string
    ) { super(column, TableCellTextPipe); }
}

export enum TableCellTextPipeFormat {
    MULTILINE,
    PERCENTAGE,
    QUANTITY,
    QUANTITY_RANGE,
    TIME,
}
