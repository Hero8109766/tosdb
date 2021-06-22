import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Observer } from 'rxjs';
import { InjectorInstance } from 'src/app/app.module';
import { TOSLanguage, TOSRegion, TOSRegionService, TOSRegionServiceInitializer, TOSRegionVersion, VERSIONS } from "../domain/tos-region";

const KEY_VERSION = 'version';
const VERSION_HOTFIX = 2;
@Injectable({
    providedIn: 'root'
})
export class UpdateService {

    private readonly region: TOSRegion = TOSRegionService.getRegion();
    private readonly language: TOSLanguage = TOSRegionService.getLanguage();

    constructor() { }

    async updateAvailable(): Promise<boolean> { return await this.getVersionNew() != this.versionOld }
    async updateVersion(clear?: boolean) {
        let version = JSON.parse(localStorage.getItem(KEY_VERSION) || '{}');
        version=version || {};
        if(typeof(version[this.region])=="string"){
            //remove
            version[this.region]={}
        }
        if (!version[this.region]){
            version[this.region]={}
        }
        if (!version[this.region][this.language]){
            version[this.region][this.language]={};
        }
        version[this.region][this.language].version = clear ? '' : await this.getVersionNew();

        localStorage.setItem(KEY_VERSION, JSON.stringify(version));
    }

    async getVersionNew() { return (await TOSRegionServiceInitializer.GetVersion())[this.region].version; }
    async getVersionHuman() { return this.region && (this.region.toString() + ' ' + this.language.toString() + ' • ' + await this.getVersionNew()) }

    private get versionOld(): string { 
        let ver= JSON.parse(localStorage.getItem(KEY_VERSION) || '{}')
        
        if(typeof(ver[this.region])=="string"){
            //remove
            ver[this.region]={}
        }
        if (!ver[this.region]){
            ver[this.region]={}
        }
        if (!ver[this.region][this.language]){
            ver[this.region][this.language]={}
        }
        return ver[this.region][this.language].version; 
    
    
    }

}
