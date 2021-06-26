import {Pipe, PipeTransform} from "@angular/core";
import {DomSanitizer, SafeHtml} from "@angular/platform-browser";
import { TagToHtml } from "../utils/tag-to-html";


@Pipe({
  name: 'colorizeHTML'
})
export class ColorizeHTMLPipe implements PipeTransform {

  constructor(private sanitizer: DomSanitizer) {}

  transform(value: string, args?: any): SafeHtml {
    return TagToHtml.ConvertTagToHTML(value)
  }

}
