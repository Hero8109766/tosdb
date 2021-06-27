import { AfterViewInit, ChangeDetectionStrategy, ChangeDetectorRef, Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from "@angular/router";
import { TOSItem } from "../../shared/domain/tos/item/tos-item.model";
import { TOSEntity } from "../../shared/domain/tos/tos-entity.model";
import { TOSEquipment, TOSEquipmentSet } from "../../shared/domain/tos/item/equipment/tos-equipment.model";
import { TOSBook } from "../../shared/domain/tos/item/book/tos-book.model";
import { TOSCollection } from "../../shared/domain/tos/item/collection/tos-collection.model";
import { TOSMonster } from "../../shared/domain/tos/monster/tos-monster.model";
import { TOSRecipe } from "../../shared/domain/tos/item/recipe/tos-recipe.model";
import { Subscription } from "rxjs";
import { TOSCube } from "../../shared/domain/tos/item/cube/tos-cube.model";
import { TOSCard } from "../../shared/domain/tos/item/card/tos-card.model";
import { TOSGem } from "../../shared/domain/tos/item/gem/tos-gem.model";
import { EntityDetailClassIconGradeComponent } from "../../shared/components/entity-detail/entity-detail-ClassIconGrade/entity-detail-ClassIconGrade.component";
import { TOSAttribute } from "../../shared/domain/tos/attribute/tos-attribute.model";
import { TOSSkill } from "../../shared/domain/tos/skill/tos-skill.model";
import { TOSDatabaseBuild } from "../../shared/domain/tos/tos-build";
import { TOSJob } from "../../shared/domain/tos/job/tos-job.model";
import { AttributeListConfigurationResolver } from "../resolvers/attribute-list-configuration.resolver";
import { CollectionListConfigurationResolver } from "../resolvers/collection-list-configuration.resolver";
import { GemListConfigurationResolver } from "../resolvers/gem-list-configuration.resolver";
import { ItemListConfigurationResolver } from "../resolvers/item-list-configuration.resolver";
import { JobListConfigurationResolver } from "../resolvers/job-list-configuration.resolver";
import { SkillListConfigurationResolver } from "../resolvers/skill-list-configuration.resolver";
import { RecipeListConfigurationResolver } from "../resolvers/recipe-list-configuration.resolver";
import { MonsterListConfigurationResolver } from "../resolvers/monster-list-configuration.resolver";
import { CubeListConfigurationResolver } from "../resolvers/cube-list-configuration.resolver";
import { EquipmentSetListConfigurationResolver } from "../resolvers/equipment-set-list-configuration.resolver";
import { TOSRegionService } from "../../shared/domain/tos-region";
import { TOSMap } from "../../shared/domain/tos/map/tos-map.model";
import { ITOSEntity, TOSDataSet } from "../../shared/domain/tos/tos-domain";
import { MapListConfigurationResolver } from "../resolvers/map-list-configuration.resolver";
import { TOSMonsterSkill } from 'src/app/shared/domain/tos/monsterskill/tos-monster-skill.model';
import { MonsterSkillListConfigurationResolver } from '../resolvers/monster-skill-list-configuration.resolver';
import { BuffListConfigurationResolver } from '../resolvers/buff-list-configuration.resolver';
import { TOSDomainService } from 'src/app/shared/domain/tos/tos-domain.service';
import { TOSUrlService } from 'src/app/shared/service/tos-url.service';
import { fromPromise } from 'rxjs/internal-compatibility';
import { TOSDomainRepository } from 'src/app/shared/domain/tos/tos-domain.repository';

@Component({
    changeDetection: ChangeDetectionStrategy.OnPush,
    selector: 'app-universal',
    templateUrl: './universal.component.html',
    styleUrls: ['./universal.component.scss']
})
export class UniversalComponent implements OnDestroy, OnInit,AfterViewInit {
    

    private subscriptionRoute: Subscription;

    constructor(protected changeDetector: ChangeDetectorRef, private route: ActivatedRoute, private router: Router) { }
    async ngOnInit() {
        
        
        this.onInit();
    }

    protected onInit() { }
    protected onDestroy() { }

    ngOnDestroy() {
        this.onDestroy();
        this.subscriptionRoute && this.subscriptionRoute.unsubscribe();
    }

    ngAfterViewInit() {
        this.subscriptionRoute = this.route.data.subscribe(({ response })=>{
            setTimeout(async ()=>{
                await this.redirect(response);
                this.onInit();
                this.changeDetector.markForCheck();
    
            },0.5)
         
        });
    }

    async redirect(data:ITOSEntity){
        let fn=async ()=>{
            return await TOSDomainService.itemsById(data.$ID).toPromise() ||
            await TOSDomainService.booksById(data.$ID).toPromise() ||
            await TOSDomainService.equipmentById(data.$ID).toPromise() ||
            await TOSDomainService.gemsById(data.$ID).toPromise()
               
        }

        let result= await fn()
        if(result){
            this.router.navigateByUrl(TOSUrlService.Route("database/"+result['Dataset']+"/"+data.$ID))
        }
    }
}
