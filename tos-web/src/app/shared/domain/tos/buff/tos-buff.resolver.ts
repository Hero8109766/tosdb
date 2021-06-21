import {Injectable} from "@angular/core";
import { CRUDResolver } from "src/app/shared/service/CRUD.resolver";
import { TOSDataSet } from "../tos-domain";
import { TOSBuff } from "./tos-buff.model";

@Injectable()
export class TOSBuffResolver extends CRUDResolver<TOSBuff> {

  constructor() { super(TOSDataSet.BUFFS); }


}
