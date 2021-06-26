import {
    ActivatedRouteSnapshot,
    CanActivate,
    CanDeactivate,
    Route,
    RouterStateSnapshot,
    UrlMatchResult,
    UrlSegment,
    UrlSegmentGroup
} from "@angular/router";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { TOSRegionService } from "../domain/tos-region";
import { switchMap } from "rxjs/operators";
import { TOSDomainService } from "../domain/tos/tos-domain.service";
import { LoadingService } from "../../shell/loading/loading.service";

@Injectable({
    providedIn: 'root'
})
export class RouteService implements CanActivate, CanDeactivate<any> {

    static UrlMatcher(segments: UrlSegment[], group: UrlSegmentGroup, route: Route): UrlMatchResult {
        let region = segments.length
            ? TOSRegionService.valueOfRegion(segments[0].path)
            : null;
        let language = segments.length
            ? TOSRegionService.valueOfLanguage(segments[1].path)
            : null;
        console.log('UrlMatcher region', region, TOSRegionService.getRegion())
        console.log('UrlMatcher langauge', region, TOSRegionService.getLanguage())
        return (region == null || language==null )&& segments
            ? { consumed: [segments[0]], posParams: { redirect: segments[0] } }
            : null;
    }

    constructor(
        private domain: TOSDomainService,
        private loading: LoadingService,
    ) { }


    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean {
        return this.loading.installComplete$.pipe(switchMap(() => this.loading.updateComplete$));
    }

    canDeactivate(component: any, currentRoute: ActivatedRouteSnapshot, currentState: RouterStateSnapshot, nextState?: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean {
        return this.loading.updateComplete$;
    }

}
