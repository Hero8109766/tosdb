import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { InjectorInstance } from "src/app/app.module";

export enum TOSRegion {
  iTOS = 'iTOS',
  jTOS = 'jTOS',
  kTEST = 'kTEST',
  kTOS = 'kTOS',
  twTOS = 'twTOS',
}

export type TOSRegionVersion = { [key in TOSRegion]: { version: string, rebuild: boolean } };
export var VERSIONS: TOSRegionVersion = null;// JSON.parse(document.getElementById('tos-region').innerText);
function SetVersion(version:TOSRegionVersion){
    VERSIONS=version
}

@Injectable({
    providedIn: 'root'
})
export class TOSRegionServiceInitializer {
    static observer: Observable<TOSRegionVersion>;
    static initializer:any =  (() => {
        TOSRegionServiceInitializer.observer = new Observable<TOSRegionVersion>((observer) => {
            let http = InjectorInstance.get<HttpClient>(HttpClient);
            let data = http.get("/region.json");

            data.subscribe((value) => {
                SetVersion(value as TOSRegionVersion);
                document.getElementById('tos-region').innerText = JSON.stringify(data);
                observer.next(VERSIONS);
                observer.complete();
            });


        });
    })();
    static async GetVersion():Promise<TOSRegionVersion>{
        if(VERSIONS!=null){
            return VERSIONS;
        }
        
        return await TOSRegionServiceInitializer.observer.toPromise();
    }
}
export namespace TOSRegionService {

  let Region: TOSRegion = null;

  export function get() {
    if (Region)
      return Region;

    for (let region of Object.values(TOSRegion))
      if (location.href.indexOf(`/${ toUrl(region) }/`) > -1)
        return region;

    return TOSRegion.iTOS;
  }
  export function getUrl() {
    return toUrl(get());
  }

  export function isRebuild(value: TOSRegion) {
    return  VERSIONS [value].rebuild;
  }

  export function select(region: TOSRegion) {
    // Update url
    let regionOld = `/${ toUrl(TOSRegionService.get()) }/`;
    let regionNew = `/${ toUrl(region) }/`;
    //console.log('region select', regionOld, regionNew, url)

    location.href = location.href.replace(regionOld, regionNew);
  }

  function toUrl(value: TOSRegion): string {
    return value.toString().toLowerCase();
  }

  export function valueOf(param: string): TOSRegion {
    return Object
      .values(TOSRegion)
      .find(value => toUrl(value) == param.toLowerCase());
  }

}
