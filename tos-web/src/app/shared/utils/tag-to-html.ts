export namespace TagToHtml {

    export function ConvertTagToHTML(tagcontainstext:string):string{
        if (tagcontainstext == null) return null;

        let description = tagcontainstext
        let regexColor = /{(#.+?)}(.+?){\/}/g;
        let match: RegExpExecArray;

        while (match = regexColor.exec(description)) {
            if (match[2].indexOf('speedofatk')) // TODO: No longer available in Re:Build
            match[2] = match[2].replace('{img tooltip_speedofatk}', ' <img src="assets/images/skill_attackspeed.png" /> ');

            description = description.replace(match[0], match[2].indexOf('[') != -1
            ? `<span class="p-1 rounded text-white" style="background: ${ match[1] }; line-height: 2">${ match[2] }</span>`
            : `<span class="font-weight-bold" style="color: ${ match[1] };">${ match[2] }</span>`
            );
        }
        
        description = description.split('{img green_up_arrow 16 16}').join('<span class="text-success">▲</span> ');
        description = description.split('{img red_down_arrow 16 16}').join('<span class="text-danger">▼</span> ');
        description = description.split('{img green_down_arrow 16 16}').join('<span class="text-success">▼</span> ');
        description = description.split('{img red_up_arrow 16 16}').join('<span class="text-danger">▲</span> ');

        let regexBraceRemover = /\{.*?\}/g;
        description=description.replace(regexBraceRemover,"")
        
        return description
            .replace(/{\/}|{ol}/g, '');
    }
}
