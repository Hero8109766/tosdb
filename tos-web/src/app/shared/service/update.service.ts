import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Observer } from 'rxjs';
import { InjectorInstance } from 'src/app/app.module';
import {  TOSRegion, TOSRegionService, TOSRegionServiceInitializer, TOSRegionVersion, VERSIONS } from "../domain/tos-region";

const KEY_VERSION = 'version';
const VERSION_HOTFIX = 2;
@Injectable({
    providedIn: 'root'
})
export class UpdateService {

    private readonly region: TOSRegion = TOSRegionService.get();

    constructor() { }

    async updateAvailable(): Promise<boolean> { return await this.getVersionNew() != this.versionOld }
    async updateVersion(clear?: boolean) {
        let version = JSON.parse(localStorage.getItem(KEY_VERSION) || '{}');
        version[this.region] = clear ? '' : await this.getVersionNew();

        localStorage.setItem(KEY_VERSION, JSON.stringify(version));
    }

    async getVersionNew() { return (await TOSRegionServiceInitializer.GetVersion())[this.region].version; }
    async getVersionHuman() { return this.region && (this.region.toString() + ' • ' +  await this.getVersionNew()) }

    private get versionOld(): string { return JSON.parse(localStorage.getItem(KEY_VERSION) || '{}')[this.region]; }

}
