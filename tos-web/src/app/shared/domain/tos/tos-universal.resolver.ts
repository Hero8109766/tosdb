import { Injectable } from "@angular/core";
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from "@angular/router";
import { Observable, of } from "rxjs";
import { CRUDResolver } from "../../service/CRUD.resolver";
import { TOSDataSet } from "./tos-domain";
import { TOSEntity } from "./tos-entity.model";
import { TOSUniversal } from "./tos-universal.model";

@Injectable()
export class TOSUniversalResolver implements Resolve<TOSUniversal> {
    public static readonly PARAM_ID: string = 'id';
    constructor() {  }
    resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): TOSUniversal | Observable<TOSUniversal> | Promise<TOSUniversal> {
        if (route.params[TOSUniversalResolver.PARAM_ID]){
            let ent:TOSUniversal=new TOSUniversal(undefined,{
                $ID:route.params[TOSUniversalResolver.PARAM_ID]
            });
            return of(ent)
        }
        return null
    }

}
