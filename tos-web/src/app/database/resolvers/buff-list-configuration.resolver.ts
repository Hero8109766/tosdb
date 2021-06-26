import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from "@angular/router";
import { Observable } from "rxjs";
import { Injectable } from "@angular/core";
import { TOSListConfiguration } from "../entity-list/entity-list.component";
import { TableCellIconPipeDefinition } from "../../shared/components/entity-table/pipes/table-cell-icon.pipe";
import { TableCellTextPipeDefinition, TableCellTextPipeFormat } from "../../shared/components/entity-table/pipes/table-cell-text.pipe";
import { TableCellNumberPipe, TableCellNumberPipeDefinition } from "src/app/shared/components/entity-table/pipes/table-cell-number.pipe";

@Injectable()
export class BuffListConfigurationResolver implements Resolve<TOSListConfiguration> {
    static readonly COLUMNS =  [
        { label: '', pipe: new TableCellIconPipeDefinition('Icon'), class: 'p-1' },
        { label: '$ID', pipe: new TableCellTextPipeDefinition('$ID'), hideMobile: true },
        { label: 'Name', pipe: new TableCellTextPipeDefinition('Name'), wide: true },
        { label: 'Description', pipe: new TableCellTextPipeDefinition('Description'), wide: true },
    ];

    static readonly COLUMNS_ADDBUFF =  [
        { label: '', pipe: new TableCellIconPipeDefinition('Icon'),class: 'p-1'},
        { label: '$ID', pipe: new TableCellTextPipeDefinition('$ID'), hideMobile: true },
        { label: 'Name', pipe: new TableCellTextPipeDefinition('Name'), wide: true },
        { label: 'Duration', pipe: new TableCellTextPipeDefinition('Duration',undefined,(x)=>"Duration: "+x+"s"), wide: false },
        { label: 'Chance', pipe: new TableCellTextPipeDefinition('Chance',undefined,(x)=>"Chance: "+x+"%"), wide: false },
    ];


    resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<TOSListConfiguration> | Promise<TOSListConfiguration> | TOSListConfiguration {
        return {
            sortColumn: '$ID',

            tableColumns:BuffListConfigurationResolver.COLUMNS
        };
    }
}
