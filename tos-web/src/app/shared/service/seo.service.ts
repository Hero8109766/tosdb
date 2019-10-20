import {ApplicationRef, Injectable} from '@angular/core';
import {NavigationEnd, Router} from "@angular/router";
import {Meta, Title} from "@angular/platform-browser";

@Injectable({
  providedIn: 'root'
})
export class SEOService {

  constructor(private application: ApplicationRef, private meta: Meta, private router: Router, private title: Title) {
    this.router.events.subscribe(async event => {
      if (event instanceof NavigationEnd) {
        let url = event.urlAfterRedirects;
            url = url.indexOf('?') > 0 ? url.slice(0, url.indexOf('?')) : url;
        let urlTitle = 'Tree of Savior - Open-source Database and Skill Simulator';
        let urlDescription = `
          A fan-made and open-source Database & Simulator for Tree of Savior.
          Includes iTOS, jTOS, kTOS and kTEST regions.
        `;

        if (url.indexOf('/simulator') > 0) {
          urlTitle = 'Skill Simulator - Tree of Savior';
          urlDescription = `Plan your builds and share with other players.`;
        }
        /*
        TODO: fix
        if (url.indexOf('/database') > 0) {
          let parts = url.slice(url.indexOf('/database')).split('/').slice(2);
          let dataset = Object.values(TOSDataSet).find(value => TOSDataSetService.toUrl(value) == parts[0]);
          let id = parts.length > 1 ? +parts[1] : null;

          if (id) {
            let entity = await TOSDomainService[TOSDataSetService.toProperty(dataset) + 'ById'](id).toPromise() as TOSEntity;

            urlTitle = entity.Name + ' - ' + TOSDataSetService.toLabel(dataset) + ' - Tree of Savior';
            urlDescription = entity.Description;
          } else {
            urlTitle = TOSDataSetService.toLabel(dataset) + ' - Tree of Savior';
            urlDescription = 'List of ' + TOSDataSetService.toLabel(dataset) + ', with advanced filtering and sorting';
          }

        }
         */
        this.meta.updateTag({ name: 'description', content: urlDescription });
        this.title.setTitle(urlTitle);
      }
    });
  }

}
