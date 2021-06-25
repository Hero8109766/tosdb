import copy
import csv
import glob
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
import xml.etree.ElementTree as ET

xml_skills={}

def parse():
    globals.monster_skills = {}
    globals.monster_skills_by_name = {}
    parse_monster_skills_skillbytool()
    parse_monster_skills()
def parse_monster_skills_skillbytool():
    global xml_skills
    logging.debug('Parsing Monster Skill by Tool...')
    xml_pattern = os.path.join(constants.PATH_INPUT_DATA, 'skill_bytool.ipf', 'mon_*.xml')
    for path in glob.glob(xml_pattern):

        try:
            with codecs.open(path,'r',encoding='utf-8',errors='replace') as f:
                root=ET.parse(f)
            # toolskill -> skill
            for skill in root.iter("Skill"):

                obj={}
                obj["ClassName"]=skill.get("Name")
                obj["TargetBuffs"]=[]
                obj["SelfBuffs"] = []

                # skill -> resultlist
                for resultlist in skill.iter("ResultList"):
                    # resultlist -> toolscp
                    for toolscp in resultlist.iter("ToolScp"):
                        scp=toolscp.get("Scp")
                        if scp=="S_R_TGTBUFF":
                            elems=list(toolscp.iter())
                            # targetbuff
                            #buff={}
                            #buff["Link_Buff"]=globals.get_buff_link(elems[0].get("Str"))
                            #buff["Duration"] = int(elems[3].get("Num"))/1000.0
                            #buff["Chance"] = int(elems[5].get("Chance"))
                            buff=[
                                 elems[1].get("Str"),str(int(elems[4].get("Num"))/1000.0),str(elems[6].get("Num"))
                            ]
                            obj["TargetBuffs"].append(';'.join(buff))

                xml_skills[obj['ClassName']] = obj
        except ET.ParseError as e:
            logging.warning("Parse error:"+str(e))

def parse_monster_skills():
    logging.debug('Parsing Monster Skills...')


    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'skill_mon.ies')

    with codecs.open(ies_path, 'r','utf-8',errors="replace") as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            # Ignore 'Common_' skills (e.g. Bokor's Summon abilities)
            if row['ClassName'].find('Common_') == 0:
                continue

            obj = {}
            obj['$ID'] = int(row['ClassID'])
            obj['$ID_NAME'] = row['ClassName']
            obj['Description'] = ''#parser_translations.translate(row['Caption'])
            obj['Icon'] = parser_assets.parse_entity_icon(row['Icon'])
            obj['Name'] = parser_translations.translate(row['ClassName'])   # dont use Name
            obj['Link_Monsters']=[]
            matcher=re.match(r'Mon_(?P<ClassName>.*)_(Skill|Attack)',row['ClassName'])
            if(matcher):
                obj['Link_Monsters']= obj['Link_Monsters'] or []
                obj['Link_Monsters'].append(
                   matcher['ClassName']
                )
            #obj['Effect'] = parser_translations.translate(row['Caption2'])
            obj['Element'] = TOSElement.value_of(row['Attribute'])
            #obj['IsShinobi'] = row['CoolDown'] == 'SCR_GET_SKL_COOLDOWN_BUNSIN' or (row['CoolDown'] and 'Bunshin_Debuff' in LUA_SOURCE[row['CoolDown']])
            #obj['OverHeat'] = {
            #    'Value': int(row['SklUseOverHeat']),
            #    'Group': row['OverHeatGroup']
            #} if not is_rebuild else int(row['SklUseOverHeat'])  # Re:Build overheat is now simpler to calculate
            obj['Prop_BasicCoolDown'] = int(row['BasicCoolDown'])
            #obj['Prop_BasicPoison'] = int(row['BasicPoison'])
            obj['Prop_BasicSP'] = int(math.floor(float(row['BasicSP'])))
            #obj['Prop_LvUpSpendPoison'] = int(row['LvUpSpendPoison'])
            #obj['Prop_LvUpSpendSp'] = float(row['LvUpSpendSp'])
            #obj['Prop_SklAtkAdd'] = float(row['SklAtkAdd'])
            #obj['Prop_SklAtkAddByLevel'] = float(row['SklAtkAddByLevel'])
            #obj['Prop_SklFactor'] = float(row['SklFactor'])
            #obj['Prop_SklFactorByLevel'] = float(row['SklFactorByLevel'])
            obj['Prop_SklSR'] = float(row['SklSR'])
            #obj['Prop_SpendItemBaseCount'] = int(row['SpendItemBaseCount'])
            #obj['RequiredStance'] = row['ReqStance']
            #obj['RequiredStanceCompanion'] = TOSRequiredStanceCompanion.value_of(row['EnableCompanion'])
            #obj['RequiredSubWeapon'] = row['UseSubweaponDamage'] == 'YES'

            obj['CoolDown'] = None
            #obj['IsEnchanter'] = False
            #obj['IsPardoner'] = False
            #obj['IsRunecaster'] = False
            #obj['Prop_LevelPerGrade'] = -1  # Remove when Re:Build goes global
            #obj['Prop_MaxLevel'] = -1
            #obj['Prop_UnlockGrade'] = -1  # Remove when Re:Build goes global
            #obj['Prop_UnlockClassLevel'] = -1
            #obj['SP'] = None
            obj['TypeAttack'] = []
            #obj['Link_Attributes'] = []
            #obj['Link_Gem'] = None
            #obj['Link_Job'] = None

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

            luaobj=copy.copy(row)
            luaobj['Level']=1
            # Parse formulas
            if row['CoolDown']:
                obj['CoolDown'] = int(row['BasicCoolDown'])
            if row['SkillFactor']:
                obj['SkillFactor'] =float(row['SklFactor'])
            if row['SklSR']:
                obj['SkillSR'] = float(row['SklSR'])
            #if row['HitCount']:
            #    obj['HitCount'] = parse_skills_lua_source(row['HitCount'])(luaobj)
            #if row['SpendSP']:
            #    obj['SP'] = parse_skills_lua_source(row['SpendSP'])(luaobj)

            obj['TargetBuffs']=[]
            obj['SelfBuffs'] =[]

            if row['ClassName'] in xml_skills:
                data=xml_skills[row['ClassName']]
                obj['TargetBuffs']=[]
                obj['SelfBuffs']=[]
                for v in data['TargetBuffs']:
                    obj['TargetBuffs'].append(v)
                for v in data['SelfBuffs']:
                    obj['SelfBuffs'].append(v)
            globals.monster_skills[obj['$ID']] = obj
            globals.monster_skills_by_name[obj['$ID_NAME']] = obj

def parse_links():

    logging.debug('Parsing MonsterSkills <> Monster...')

    # monsterskill <> monster
    for monster in list(globals.monster_skills.values()):
        links=None
        if monster['Link_Monsters']:
            links = []
            for v in monster['Link_Monsters']:
                if v in globals.monsters_by_name:
                    mnst=globals.monsters_by_name[v]
                    mnst['Link_MonsterSkills'].append(globals.get_monster_skills_link(mnst))
                    globals.monsters_by_name[v]=mnst
                    globals.monsters[mnst['$ID']]=mnst

                    link=globals.get_monster_link(v)
                    links.append(link)
        monster['Link_Monsters']=links
        globals.monster_skills[monster['$ID']] = monster
        globals.monster_skills_by_name[monster['$ID_NAME']] = monster



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

    # # Replace embedded function calls with their source code
    # for line in luautil.lua_function_source(LUA_SOURCE[function])[1:-1]:  # remove 'function' and 'end'
    #     for embed in LUA_EMBEDDED:
    #         if embed in line:
    #             result = luautil.lua_function_source(LUA_SOURCE[embed]) + result
    #             break
    #
    #     result.append(line)

    return luautil.lua_function_reference(function)

