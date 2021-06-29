import {
    ChangeDetectionStrategy,
    ChangeDetectorRef,
    Component,
    Input,
    OnChanges,
    OnDestroy,
    SimpleChanges
} from '@angular/core';
import { EntityDetailChildComponent } from "../entity-detail-child.component";
import { Observable, Subscription } from "rxjs";
import { ITOSBuild, ITOSSkill } from "../../../domain/tos/tos-domain";
import { faBolt, faTint, faWeightHanging } from "@fortawesome/free-solid-svg-icons";
import { faClock } from "@fortawesome/free-regular-svg-icons";
import { InjectorInstance } from 'src/app/app.module';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';

@Component({
    changeDetection: ChangeDetectionStrategy.OnPush,
    selector: 'tos-entity-detail-MarketPrice',
    templateUrl: './entity-detail-MarketPrice.component.html',
    styleUrls: ['./entity-detail-MarketPrice.component.scss']
})
export class EntityDetailMarketPriceComponent extends EntityDetailChildComponent {
    @Input() divider: boolean;
    @Input() header: string;
    
    public server1007:string='';
    public server1008:string='';
    


    constructor(changeDetector: ChangeDetectorRef) { super(changeDetector); }

    async ngOnInit(){
        this.server1007=await this.marketPrice(1007)
        this.server1008=await this.marketPrice(1008)
        this.changeDetector.detectChanges()
    }

    public async marketPrice(server: number): Promise<string> {
        let http = InjectorInstance.get<HttpClient>(HttpClient);
        let host = "https://tosmarket.mochisuke.jp"
        //host = "http://localhost:5000"
        const httpOptions = {
            headers: new HttpHeaders({
                'Access-Control-Allow-Origin': '*',
            })
        };
        let x = await http.get(`${host}/clsid/?s=${server}&c=${this.entity.$ID}`,httpOptions).toPromise()

        if (!x || !x['minPrice']) {
            return 'n/a'
        }
        return EntityDetailMarketPriceComponent.numberWithCommas(x['minPrice'])

    }
    static numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
}
