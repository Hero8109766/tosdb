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
export enum TOSLanguage {
    en = 'en',
    ja = 'ja',
    ko = 'ko',
    zh = 'zh',
    pt = 'pt',
    de = 'de',
    th = 'th',
    ru = 'ru'
}
export let HumanReadableLanguage={
    "en":"English",
    "ja":"Japanese",
    "ko":"Korean",
    "zh":"Taiwanese",
    "pt":"Português",
    "de":"Deutsch",
    "th":"Thai",
    "ru":"Russian",
    
}

export type TOSRegionVersion = { [key in TOSRegion]: { version: string, rebuild: boolean } };
export var VERSIONS: TOSRegionVersion = null;// JSON.parse(document.getElementById('tos-region').innerText);
function SetVersion(version: TOSRegionVersion) {
    VERSIONS = version
}

@Injectable({
    providedIn: 'root'
})
export class TOSRegionServiceInitializer {
    static observer: Observable<TOSRegionVersion>;
    static initializer: any = (() => {
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
    static async GetVersion(): Promise<TOSRegionVersion> {
        if (VERSIONS) {
            return VERSIONS;
        }
        let http = InjectorInstance.get<HttpClient>(HttpClient);
        let data = http.get("/region.json");
        return await (data as Observable<TOSRegionVersion>).toPromise()
    }
}
export namespace TOSRegionService {

    let Region: TOSRegion = null;
    let Language: TOSLanguage = null
    let Tree=null;
    export function getRegion() {
        
        if (Region){
            getTree()
            return Region;
        }
        for (let region of Object.values(TOSRegion))
            if (location.href.indexOf(`/${region.toString().toLowerCase()}/`) > -1)
                return region;
        
        return TOSRegion.iTOS;
    }
    export function getLanguage() {
        if (Language){
            getTree();
            return Language;

        }
            
        for (let lang of Object.values(TOSLanguage))
            if (location.href.indexOf(`/${lang.toString().toLowerCase()}/`) > -1)
                return lang;

        return TOSLanguage.en;
    }
    export function getUrl() {
        return toUrl(getRegion(), getLanguage());
    }

    export function isRebuild(value: TOSRegion) {
        return VERSIONS[value].rebuild;
    }

    export function select(region: TOSRegion, language: TOSLanguage) {
        // Update url
        let regionOld = `/${toUrl(TOSRegionService.getRegion(), TOSRegionService.getLanguage())}/`;
        let regionNew = `/${toUrl(region, language)}/`;
        //console.log('region select', regionOld, regionNew, url)

        location.href = location.href.replace(regionOld, regionNew);
    }

    function toUrl(value: TOSRegion, lang: TOSLanguage): string {
        return value.toString().toLowerCase() + "/" + lang.toString().toLowerCase();
    }

    export function valueOfRegion(param: string): TOSRegion {
        return Object
            .values(TOSRegion)
            .find(value => toUrl(value, TOSRegionService.getLanguage()) == param.toLowerCase());
    }
    export function valueOfLanguage(param: string): TOSLanguage {
        return Object
            .values(TOSLanguage)
            .find(value => toUrl(TOSRegionService.getRegion(), value) == param.toLowerCase());
    }
    export function languageToHumanReadable(param: TOSLanguage): string {
        return HumanReadableLanguage[param]
    }
    export function getTree() {

        Tree= [
            {
                label: TOSRegion.iTOS,
                option: [
                    TOSLanguage.en,
                    TOSLanguage.de,
                    TOSLanguage.pt,
                    TOSLanguage.th,
                    TOSLanguage.ru,
                ],
            }, {
                label: TOSRegion.jTOS,
                option: [
                    TOSLanguage.ja
                ]
            },
            {
                label: TOSRegion.kTOS,
                option: [
                    TOSLanguage.ko
                ]
            },
            {
                label: TOSRegion.kTEST,
                option: [
                    TOSLanguage.ko
                ]
            }, {
                label: TOSRegion.twTOS,
                option: [
                    TOSLanguage.zh
                ]
            }


        ]
        return Tree;
    }

}
