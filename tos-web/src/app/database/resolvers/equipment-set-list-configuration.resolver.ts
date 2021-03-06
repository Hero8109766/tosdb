import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from "@angular/router";
import {Observable} from "rxjs";
import {Injectable} from "@angular/core";
import {TOSListConfiguration} from "../entity-list/entity-list.component";
import {TableCellTextPipeDefinition} from "../../shared/components/entity-table/pipes/table-cell-text.pipe";
import {TableCellLinkPipeDefinition} from "../../shared/components/entity-table/pipes/table-cell-link.pipe";

@Injectable()
export class EquipmentSetListConfigurationResolver implements Resolve<TOSListConfiguration> {

  static readonly COLUMNS = [
    { label: '$ID',           pipe: new TableCellTextPipeDefinition('$ID'), hideMobile: true },
    { label: 'Name',          pipe: new TableCellTextPipeDefinition('Name'), wide: true },
    { label: 'Items',         pipe: new TableCellLinkPipeDefinition('Link_Items'), class: 'p-1 text-nowrap' }
  ];

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<TOSListConfiguration> | Promise<TOSListConfiguration> | TOSListConfiguration {
    return {
      sortColumn: '$ID',
      tableColumns: EquipmentSetListConfigurationResolver.COLUMNS,
    };
  }
}
