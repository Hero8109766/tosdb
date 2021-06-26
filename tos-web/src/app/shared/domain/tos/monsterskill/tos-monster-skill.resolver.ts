import {Injectable} from "@angular/core";
import {CRUDResolver} from "../../../service/CRUD.resolver";
import {TOSMonsterSkill} from "./tos-monster-skill.model";
import {TOSDataSet} from "../tos-domain";

@Injectable()
export class TOSMonsterSkillResolver extends CRUDResolver<TOSMonsterSkill> {

  constructor() { super(TOSDataSet.MONSTERSKILLS); }

}
