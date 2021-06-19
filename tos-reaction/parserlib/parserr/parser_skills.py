import csv
import logging
import math
import os
import re
import codecs
from parserlib import constantsmod, globals
from parserlib.parserr import parser_assets
from parserlib.parserr import parser_translations
from parserlib.parserr.parser_enums import TOSElement, TOSAttackType
from parserlib.parserr.parser_jobs import TOSJobTree
from parserlib.utils import luautilmod
from parserlib.utils.tosenum import TOSEnum

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
    parse_skills_overheats()
    parse_skills_simony()
    parse_skills_stances()


def parse_skills(is_rebuild):
    logging.debug('Parsing skills...')

    LUA_RUNTIME = luautilmod.LUA_RUNTIME
    LUA_SOURCE = luautilmod.LUA_SOURCE

    ies_path = os.path.join(constantsmod.PATH_INPUT_DATA, 'ies.ipf', 'skill.ies')

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
                        obj[key] = parse_skills_lua_source_to_javascript(row, obj[key])
                    else:
                        # Hotfix: similar to the hotfix above
                        logging.warning('[%32s] Deprecated effect [%s] in Effect', obj['$ID_NAME'], effect)
                        obj[key] = None
                else:
                    continue

            # Parse formulas
            if row['CoolDown']:
                obj['CoolDown'] = parse_skills_lua_source(row['CoolDown'])
                obj['CoolDown'] = parse_skills_lua_source_to_javascript(row, obj['CoolDown'])
            if row['SpendSP']:
                obj['SP'] = parse_skills_lua_source(row['SpendSP'])
                obj['SP'] = parse_skills_lua_source_to_javascript(row, obj['SP'])

            globals.skills[obj['$ID']] = obj
            globals.skills_by_name[obj['$ID_NAME']] = obj

    # HotFix: make sure all skills have the same Effect columns (2/2)
    for skill in list(globals.skills.values()):
        for effect in EFFECTS:
            if effect not in skill:
                skill[effect] = None


def parse_skills_lua_source(function):
    LUA_SOURCE = luautilmod.LUA_SOURCE
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
    for line in luautilmod.lua_function_source(LUA_SOURCE[function])[1:-1]:  # remove 'function' and 'end'
        for embed in LUA_EMBEDDED:
            if embed in line:
                result = luautilmod.lua_function_source(LUA_SOURCE[embed]) + result
                break

        result.append(line)

    return result


def parse_skills_lua_source_to_javascript(skill, source):
    result = []
    reinforceAbilName = '"' + skill['ReinforceAbility'] + '"' if 'ReinforceAbility' in skill else None

    for line in source:
        if 'GetSkillOwner(skill)' in line:
            continue
        if 'local reinfabil = ' in line:
            continue
        if 'local reinforceAbilName = ' in line:
            continue
        if 'SCR_GET_SPEND_ITEM_Alchemist_SprinkleHPPotion' in line:
            continue
        if 'SCR_GET_SPEND_ITEM_Alchemist_SprinkleSPPotion' in line:
            continue

        if reinforceAbilName:
            line = line.replace('reinfabil', reinforceAbilName)
            line = line.replace('reinforceAbilName', reinforceAbilName)
            line = line.replace('TryGetProp(skill, "ReinforceAbility")', reinforceAbilName)

        line = line.replace('basicsp', 'basicSP')  # freaking LUA being case insensitive!
        line = line.replace('TryGetProp(hpPotion, "NumberArg1", 0)', '395 // @rjgtav: using Lv 15 Condensed HP Potion')
        line = line.replace('TryGetProp(spPotion, "NumberArg1", 0)', '131 // @rjgtav: using Lv 15 Condensed SP Potion')
        line = line.replace('SCR_CALC_BASIC_DEF(pc)', 'pc.DEF')
        line = line.replace('SCR_CALC_BASIC_MDEF(pc)', 'pc.MDEF')
        line = re.sub(r'TryGetProp\(pc, \"(.+)\"\)', r'pc.\1', line)
        line = re.sub(r'GetAbilityAddSpendValue\(pc, skill\.ClassName, \"(.+)\"\)', '0 // @rjgtav: Attributes aren\'t supported yet', line)  # TODO: support calculating the extra CoolDown/SP caused by attributes

        result.append(line)

    return luautilmod.lua_function_source_to_javascript(result)


def parse_skills_overheats():
    logging.debug('Parsing skills overheats...')

    ies_path = os.path.join(constantsmod.PATH_INPUT_DATA, 'ies.ipf', 'cooldown.ies')
    with codecs.open(ies_path, 'r','utf-8',errors="replace") as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            # We're only interested in overheats
            if row['IsOverHeat'] != 'YES':
                continue

            skill = None

            for obj in list(globals.skills.values()):
                if isinstance(obj['OverHeat'], dict) and row['ClassName'] == obj['OverHeat']['Group']:
                    skill = obj
                    break

            # If skill isn't available, ignore
            if skill is None:
                continue

            skill['OverHeat'] = int(row['MaxOverTime']) / skill['OverHeat']['Value'] if skill['OverHeat']['Value'] > 0 else 0

    # Clear skills with no OverHeat information
    for skill in list(globals.skills.values()):
        if isinstance(skill['OverHeat'], dict):
            skill['OverHeat'] = 0


def parse_skills_simony():
    logging.debug('Parsing skills simony...')

    ies_path = os.path.join(constantsmod.PATH_INPUT_DATA, 'ies.ipf', 'skill_simony.ies')
    with codecs.open(ies_path, 'r','utf-8',errors='replace') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            if int(row['ClassID']) not in globals.skills:
                logging.error('Unknown skill: %d', int(row['ClassID']))
                continue

            skill = globals.skills[int(row['ClassID'])]
            skill['IsEnchanter'] = True
            skill['IsPardoner'] = True
            skill['IsRunecaster'] = True


def parse_skills_stances():
    logging.debug('Parsing skills stances...')

    stance_list = []
    ies_path = os.path.join(constantsmod.PATH_INPUT_DATA, 'ies.ipf', 'stance.ies')

    # Parse stances
    with codecs.open(ies_path, 'r','utf-8',errors='replace') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            stance_list.append(row)

    # Add stances to skills
    # from addon.ipf\skilltree\skilltree.lua :: MAKE_STANCE_ICON
    for skill in list(globals.skills.values()):
        stances_main_weapon = []
        stances_sub_weapon = []

        if skill['RequiredStance']:
            for stance in stance_list:
                index = skill['RequiredStance'].find(stance['ClassName'])

                if index == -1:
                    continue
                if skill['RequiredStance'] == 'TwoHandBow' and stance['ClassName'] == 'Bow':
                    continue
                if 'Artefact' in stance['Name']:
                    continue

                if stance['UseSubWeapon'] == 'NO':
                    stances_main_weapon.append({
                        'Icon': parser_assets.parse_entity_icon(stance['Icon']),
                        'Name': stance['ClassName']
                    })
                else:
                    found = False
                    for stance_sub in stances_sub_weapon:
                        if stance_sub['Icon'] == parser_assets.parse_entity_icon(stance['Icon']):
                            found = True
                            break

                    if not found:
                        stances_sub_weapon.append({
                            'Icon': parser_assets.parse_entity_icon(stance['Icon']),
                            'Name': stance['ClassName']
                        })
        else:
            stances_main_weapon.append({
                'Icon': parser_assets.parse_entity_icon('weapon_All'),
                'Name': 'All'
            })

        if skill['RequiredStanceCompanion'] in [TOSRequiredStanceCompanion.BOTH, TOSRequiredStanceCompanion.YES]:
            stances_main_weapon.append({
                'Icon': parser_assets.parse_entity_icon('weapon_companion'),
                'Name': 'Companion'
            })

        skill['RequiredStance'] = [
            stance for stance in (stances_main_weapon + stances_sub_weapon)
            if stance['Icon'] is not None
        ]


def parse_links(is_rebuild):
    parse_links_gems()
    parse_links_jobs(is_rebuild)


def parse_links_gems():
    logging.debug('Parsing gems for skills...')

    ies_path = os.path.join(constantsmod.PATH_INPUT_DATA, 'ies.ipf', 'item_gem.ies')

    with codecs.open(ies_path, 'r','utf-8',errors='replace') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            skill = row['ClassName'][len('Gem_'):]

            if skill not in globals.skills_by_name:
                continue

            skill = globals.skills_by_name[skill]
            skill['Link_Gem'] = globals.get_gem_link(row['ClassName'])


def parse_links_jobs(is_rebuild):
    logging.debug('Parsing jobs for skills...')

    ies_path = os.path.join(constantsmod.PATH_INPUT_DATA, 'ies.ipf', 'skilltree.ies')

    tree_enchanter = TOSJobTree.SCOUT if is_rebuild else TOSJobTree.WIZARD
    tree_pardoner = TOSJobTree.CLERIC
    tree_runecaster = TOSJobTree.WIZARD
    tree_shinobi = TOSJobTree.SCOUT if is_rebuild else TOSJobTree.WARRIOR

    with codecs.open(ies_path, 'r','utf-8',errors='replace') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            # Ignore discarded skills
            if row['SkillName'] not in globals.skills_by_name:
                continue

            skill = globals.skills_by_name[row['SkillName']]
            skill['Prop_MaxLevel'] = int(row['MaxLevel'])
            skill['Prop_LevelPerGrade'] = int(row['LevelPerGrade']) if 'LevelPerGrade' in row else 0
            skill['Prop_UnlockClassLevel'] = int(row['UnlockClassLevel']) if 'UnlockClassLevel' in row else 0
            skill['Prop_UnlockGrade'] = int(row['UnlockGrade']) if 'UnlockGrade' in row else 0

            job = '_'.join(row['ClassName'].split('_')[:2])
            job_tree = globals.jobs_by_name[job]['JobTree']

            # Fix enchanter, pardoner and shinobi
            skill['IsEnchanter'] = job_tree == tree_enchanter if skill['IsEnchanter'] else False
            skill['IsPardoner'] = job_tree == tree_pardoner if skill['IsPardoner'] else False
            skill['IsRunecaster'] = job_tree == tree_runecaster if skill['IsRunecaster'] else False
            skill['IsShinobi'] = job_tree == tree_shinobi if skill['IsShinobi'] else False
            skill['Link_Job'] = globals.get_job_link(job)


def parse_clean():
    skills_to_remove = []

    # Find which skills are no longer active
    for skill in list(globals.skills.values()):
        if skill['Link_Job'] is None:
            skills_to_remove.append(skill)

    # Remove all inactive skills
    for skill in skills_to_remove:
        del globals.skills[skill['$ID']]
        del globals.skills_by_name[skill['$ID_NAME']]

        skill_id = skill['$ID']

        for attribute in list(globals.attributes.values()):
            attribute['Link_Skills'] = [link for link in attribute['Link_Skills'] if link.entity['$ID'] != skill_id]
        for job in list(globals.jobs.values()):
            job['Link_Skills'] = [link for link in job['Link_Skills'] if link.entity['$ID'] != skill_id]
