import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {RouteService} from "./shared/service/route.service";
import {ROUTES_DATABASE} from "./database/database.route";
import {ROUTES_SKILL_SIMULATOR} from "./skill-simulator/skill-simulator.route";
import {HomeModule} from "./home/home.module";
import {DatabaseModule} from "./database/database.module";
import {SkillSimulatorModule} from "./skill-simulator/skill-simulator.module";
import {WelcomeComponent} from "./home/welcome/welcome.component";
import {PatreonComponent} from "./home/patreon/patreon.component";

const ROUTES_APP: Routes = [
  {
    path: 'database',
    children: ROUTES_DATABASE,
  },
  {
    path: 'home',
    canActivate: [RouteService],
    canDeactivate: [RouteService],
    component: WelcomeComponent,
  },
  {
    path: 'patreon',
    canActivate: [RouteService],
    canDeactivate: [RouteService],
    component: PatreonComponent,
  },
  {
    path: 'simulator',
    children: ROUTES_SKILL_SIMULATOR,
  },
  {
    path: '**',
    redirectTo: 'home',
  },
];

const ROUTES_REGION: Routes = [
  {
    path: '',
    redirectTo: '/itos/en/home',
    pathMatch: 'full'
  },
  {
    path: 'itos/en',
    canActivate: [RouteService],
    canDeactivate: [RouteService],
    children: ROUTES_APP,
  },
  {
    path: 'itos/de',
    canActivate: [RouteService],
    canDeactivate: [RouteService],
    children: ROUTES_APP,
  },
  {
    path: 'itos/pt',
    canActivate: [RouteService],
    canDeactivate: [RouteService],
    children: ROUTES_APP,
  },
  {
    path: 'itos/th',
    canActivate: [RouteService],
    canDeactivate: [RouteService],
    children: ROUTES_APP,
  },
  {
    path: 'itos/ru',
    canActivate: [RouteService],
    canDeactivate: [RouteService],
    children: ROUTES_APP,
  },
  {
    path: 'jtos/ja',
    canActivate: [RouteService],
    canDeactivate: [RouteService],
    children: ROUTES_APP,
  },
  
   {
    path: 'ktest/ko',
    children: ROUTES_APP,
    canActivate: [RouteService],
    canDeactivate: [RouteService],
  },
  {
    path: 'ktos/ko',
    children: ROUTES_APP,
    canActivate: [RouteService],
    canDeactivate: [RouteService],
  },
  {
    path: 'twtos/zh',
    children: ROUTES_APP,
    canActivate: [RouteService],
    canDeactivate: [RouteService],
  },
  {
    matcher: RouteService.UrlMatcher,
    redirectTo: '/itos/:redirect',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [
    DatabaseModule,
    HomeModule,
    SkillSimulatorModule,
    RouterModule.forRoot(ROUTES_REGION, {
      anchorScrolling: 'enabled',
      //enableTracing: true,
      onSameUrlNavigation: 'ignore',
      scrollPositionRestoration: 'disabled' // Note: as of angular 6.1, when 'enabled', we can't disable it for specific routes (e.g. the simulator)
    })
  ],
  exports: [RouterModule],
})
export class AppRoutingModule { }
