import { ITOSBuff,TOSDataSet } from "../tos-domain";
import { TOSEntity } from "../tos-entity.model";
export class TOSBuff extends TOSEntity implements ITOSBuff {
    constructor(json: TOSBuff) {
        super(TOSDataSet.BUFFS, json);
    }
    get UserRemove(){
        return this.$lazyPropertyBoolean('UserRemove')
    } 

    get Pages() { return this.$lazyPropertyStringMultiline('Text') }

}
