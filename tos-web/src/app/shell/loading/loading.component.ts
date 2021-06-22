import { ChangeDetectionStrategy, ChangeDetectorRef, Component, NgZone, OnDestroy, OnInit } from '@angular/core';
import { UpdateService } from "../../shared/service/update.service";
import { LoadingService } from "./loading.service";

@Component({
    changeDetection: ChangeDetectionStrategy.OnPush,
    selector: 'tos-loading',
    templateUrl: './loading.component.html',
    styleUrls: ['./loading.component.scss']
})
export class LoadingComponent implements OnInit, OnDestroy {

    isClearCacheAvailable: boolean;
    isClearCacheAvailableTimeout: any;

    installComplete: boolean;
    installSupported: boolean;

    updateAvailable: boolean
    updateComplete: boolean;
    updateProgress: number = 0;
    updateTotal: number = 0;
    updateVersion: string;
    updateConfirmed=false;

    constructor(
        private changeDetector: ChangeDetectorRef,
        private loading: LoadingService,
        private update: UpdateService,
        private zone: NgZone,
    ) {
        this.loading.updateProgress$.subscribe(value => this.onUpdateProgress(value));
        this.loading.updateComplete$.subscribe(value => this.onUpdateComplete());
        this.loading.installComplete$.subscribe(value => this.onInstallComplete());

        this.installSupported = this.loading.installSupported;
        this.onUpdateAvailable();
    }

    ngOnInit(): void {
        this.zone.runOutsideAngular(() => this.isClearCacheAvailableTimeout = setTimeout(() => {
            this.isClearCacheAvailable = true;
            this.changeDetector.detectChanges();
        }, 5 * 1000
        ));
  
    }

    ngOnDestroy(): void {
        clearTimeout(this.isClearCacheAvailableTimeout);
    }

    onClearCacheClick() {
        this.loading.clear();
    }

    onInstallComplete() {
        this.installComplete = true;
        this.changeDetector.markForCheck();
    }

    async onUpdateAvailable() {
        this.updateAvailable = await this.update.updateAvailable();
        this.updateAvailable && this.changeDetector.markForCheck();
        this.updateVersion = await this.update.getVersionHuman();
        this.updateConfirmed=true;
    }
    onUpdateComplete() {
        this.updateComplete = true;
        this.changeDetector.markForCheck();
    }
    onUpdateProgress(value: number) {
        if (!this.updateAvailable) return;

        this.updateProgress = Math.max(value, 0);
        this.updateTotal = this.loading.updateTotal;
        this.changeDetector.markForCheck();
    }

}
