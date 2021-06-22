import csv
import logging
import math
import os
import re
import codecs
import constants
import globals
from parserr import parser_assets
from parserr import parser_translations
from parserr.parser_enums import TOSElement, TOSAttackType
from parserr.parser_jobs import TOSJobTree
from utils import luautil
from utils.tosenum import TOSEnum

EFFECT_DEPRECATE = {
    'SkillAtkAdd': 'SkillFactor'
}


class TOSRequiredStanceCompanion(TOSEnum):
    BOTH = 0
    NO = 1
    SELF = 2
    YES = 3

    @staticmethod
    def value_of(string):
        return {
            'BOTH': TOSRequiredStanceCompanion.BOTH,
            '': TOSRequiredStanceCompanion.NO,
            'SELF': TOSRequiredStanceCompanion.SELF,
            'YES': TOSRequiredStanceCompanion.YES,
        }[string.upper()]


EFFECTS = []


def parse(is_rebuild):
    parse_skills(is_rebuild)


def parse_skills(is_rebuild):
    logging.debug('Parsing skills...')

    LUA_RUNTIME = luautil.LUA_RUNTIME
    LUA_SOURCE = luautil.LUA_SOURCE

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'skill.ies')

    with codecs.open(ies_path, 'r','utf-8',errors="replace") as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            # Ignore 'Common_' skills (e.g. Bokor's Summon abilities)
            if row['ClassName'].find('Common_') == 0:
                continue

            obj = {}
            obj['$ID'] = int(row['ClassID'])
            obj['$ID_NAME'] = row['ClassName']
            obj['Description'] = parser_translations.translate(row['Caption'])
            obj['Icon'] = parser_assets.parse_entity_icon(row['Icon'])
            obj['Name'] = parser_translations.translate(row['Name'])

            obj['Effect'] = parser_translations.translate(row['Caption2'])
            obj['Element'] = TOSElement.value_of(row['Attribute'])
            obj['IsShinobi'] = row['CoolDown'] == 'SCR_GET_SKL_COOLDOWN_BUNSIN' or (row['CoolDown'] and 'Bunshin_Debuff' in LUA_SOURCE[row['CoolDown']])
            obj['OverHeat'] = {
                'Value': int(row['SklUseOverHeat']),
                'Group': row['OverHeatGroup']
            } if not is_rebuild else int(row['SklUseOverHeat'])  # Re:Build overheat is now simpler to calculate
            obj['Prop_BasicCoolDown'] = int(row['BasicCoolDown'])
            obj['Prop_BasicPoison'] = int(row['BasicPoison'])
            obj['Prop_BasicSP'] = int(math.floor(float(row['BasicSP'])))
            obj['Prop_LvUpSpendPoison'] = int(row['LvUpSpendPoison'])
            obj['Prop_LvUpSpendSp'] = float(row['LvUpSpendSp'])
            obj['Prop_SklAtkAdd'] = float(row['SklAtkAdd'])
            obj['Prop_SklAtkAddByLevel'] = float(row['SklAtkAddByLevel'])
            obj['Prop_SklFactor'] = float(row['SklFactor'])
            obj['Prop_SklFactorByLevel'] = float(row['SklFactorByLevel'])
            obj['Prop_SklSR'] = float(row['SklSR'])
            obj['Prop_SpendItemBaseCount'] = int(row['SpendItemBaseCount'])
            obj['RequiredStance'] = row['ReqStance']
            obj['RequiredStanceCompanion'] = TOSRequiredStanceCompanion.value_of(row['EnableCompanion'])
            obj['RequiredSubWeapon'] = row['UseSubweaponDamage'] == 'YES'

            obj['CoolDown'] = None
            obj['IsEnchanter'] = False
            obj['IsPardoner'] = False
            obj['IsRunecaster'] = False
            obj['Prop_LevelPerGrade'] = -1  # Remove when Re:Build goes global
            obj['Prop_MaxLevel'] = -1
            obj['Prop_UnlockGrade'] = -1  # Remove when Re:Build goes global
            obj['Prop_UnlockClassLevel'] = -1
            obj['SP'] = None
            obj['TypeAttack'] = []
            obj['Link_Attributes'] = []
            obj['Link_Gem'] = None
            obj['Link_Job'] = None

            # Parse TypeAttack
            if row['ValueType'] == 'Buff':
                obj['TypeAttack'].append(TOSAttackType.BUFF)
            if row['ClassType'] is not None:
                obj['TypeAttack'].append(TOSAttackType.value_of(row['ClassType']))
            if row['AttackType'] is not None:
                obj['TypeAttack'].append(TOSAttackType.value_of(row['AttackType']))

            obj['TypeAttack'] = list(set(obj['TypeAttack']))
            obj['TypeAttack'] = [attack for attack in obj['TypeAttack'] if attack is not None and attack != TOSAttackType.UNKNOWN]

            # Add missing Description header
            if not re.match(r'{#.+}{ol}(\[.+?\]){\/}{\/}{nl}', obj['Description']):
                header = ['[' + TOSAttackType.to_string(attack) + ']' for attack in obj['TypeAttack']]

                header_color = ''
                header_color = '993399' if TOSAttackType.MAGIC in obj['TypeAttack'] else header_color
                header_color = 'DD5500' if TOSAttackType.MELEE in obj['TypeAttack'] else header_color
                header_color = 'DD5500' if TOSAttackType.MISSILE in obj['TypeAttack'] else header_color

                if obj['Element'] != TOSElement.MELEE:
                    header.append('[' + TOSElement.to_string(obj['Element']) + ']')

                obj['Description'] = '{#' + header_color + '}{ol}' + ' - '.join(header) + '{/}{/}{nl}' + obj['Description']

            # Parse effects
            for effect in re.findall(r'{(.*?)}', obj['Effect']):
                if effect in EFFECT_DEPRECATE:
                    # Hotfix: sometimes IMC changes which effects are used, however they forgot to properly communicate to the translation team.
                    # This code is responsible for fixing that and warning so the in-game translations can be fixed
                    logging.warning('[%32s] Deprecated effect [%s] in Effect', obj['$ID_NAME'], effect)

                    effect_deprecate = effect
                    effect = EFFECT_DEPRECATE[effect]

                    obj['Effect'] = re.sub(r'\b' + re.escape(effect_deprecate) + r'\b', effect, obj['Effect'])

                if effect in row:
                    key = 'Effect_' + effect

                    # HotFix: make sure all skills have the same Effect columns (1/2)
                    if key not in EFFECTS:
                        EFFECTS.append('Effect_' + effect)

                    if row[effect] != 'ZERO':
                        obj[key] = parse_skills_lua_source(row[effect])
                        #obj[key] = parse_skills_lua_source_to_javascript(row, obj[key])
                    else:
                        # Hotfix: similar to the hotfix above
                        logging.warning('[%32s] Deprecated effect [%s] in Effect', obj['$ID_NAME'], effect)
                        obj[key] = None
                else:
                    continue

            # Parse formulas
            if row['CoolDown']:
                obj['CoolDown'] = parse_skills_lua_source(row['CoolDown'])
                #obj['CoolDown'] = parse_skills_lua_source_to_javascript(row, obj['CoolDown'])
            if row['SpendSP']:
                obj['SP'] = parse_skills_lua_source(row['SpendSP'])
                #obj['SP'] = parse_skills_lua_source_to_javascript(row, obj['SP'])

            globals.skills[obj['$ID']] = obj
            globals.skills_by_name[obj['$ID_NAME']] = obj

    # HotFix: make sure all skills have the same Effect columns (2/2)
    for skill in list(globals.skills.values()):
        for effect in EFFECTS:
            if effect not in skill:
                skill[effect] = None


def parse_skills_lua_source(function):
    LUA_SOURCE = luautil.LUA_SOURCE
    LUA_EMBEDDED = [
        'SCR_ABIL_ADD_SKILLFACTOR',
        'SCR_ABIL_ADD_SKILLFACTOR_TOOLTIP',
        'SCR_Get_SpendSP',
        'SCR_REINFORCEABILITY_TOOLTIP',
    ]

    result = []

    if function not in LUA_SOURCE:
        logging.warn('Unknown LUA function: %s', function)
        return result

    # Replace embedded function calls with their source code
    for line in luautil.lua_function_source(LUA_SOURCE[function])[1:-1]:  # remove 'function' and 'end'
        for embed in LUA_EMBEDDED:
            if embed in line:
                result = luautil.lua_function_source(LUA_SOURCE[embed]) + result
                break

        result.append(line)

    return result

