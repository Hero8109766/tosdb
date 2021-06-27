import { TOSEntity } from "./tos-entity.model";
import { TOSDomainService } from "./tos-domain.service";
import { RemoteLUAService } from "../../service/remote-lua.service";
import { from, Observable, of } from "rxjs";
import { fromPromise } from "rxjs/internal-compatibility";
import { map, mergeAll } from "rxjs/operators";
import { observable } from "rxjs";
import { ITOSEntity, TOSDataSet } from "./tos-domain";

export class TOSUniversal extends TOSEntity implements ITOSEntity {

    constructor(dataset:TOSDataSet,json: any) {
        super(undefined, json);
        this.$json=json
    }
    
}