# coding=utf-8
import csv
import logging
import os

import constants
import globals
from parserr import parser_assets
from parserr import parser_translations
from parserr.parser_items_equipment import TOSEquipmentType, TYPE_EQUIPMENT_COSTUME_LIST
from utils.tosenum import TOSEnum
import codecs


def parse():
    parse_buffs('buff.ies')
    parse_buffs('buff_contents.ies')
    parse_buffs('buff_hardskill.ies')
    parse_buffs('buff_mgame.ies')
    parse_buffs('buff_monster.ies')


def parse_buffs(file_name):
    logging.debug('Parsing %s...', file_name)

    ies_path = os.path.join(constants.PATH_INPUT_DATA, "ies.ipf", file_name)
    ies_file = codecs.open(ies_path, 'r','utf-8',errors='replace')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

    for row in ies_reader:

        logging.debug('Parsing buff: %s :: %s', row['ClassID'], row['ClassName'])

        obj = {}
        obj['$ID'] = int(row['ClassID'])
        obj['$ID_NAME'] = row['ClassName']
        obj['Description'] = parser_translations.translate(row['ToolTip']) if 'ToolTip' in row else None
        obj['Icon'] = parser_assets.parse_entity_icon(row['Icon'])
        obj['Name'] = parser_translations.translate(row['Name']) if 'Name' in row else None

        obj['Lv'] = row['Lv']
        obj['ApplyTime'] = float(int(row['ApplyTime']) / 1000) if 'ApplyTime' in row else None
        obj['UpdateTime'] = float(int(row['UpdateTime']) / 1000) if 'UpdateTime' in row else None
        obj['BuffExpUp'] = float(int(row['OverBuff']) / 1000) if 'OverBuff' in row else None
        obj['ShowIcon'] =  row['ShowIcon'] if 'ShowIcon' in row else None
        obj['RemoveBySkill'] = row['RemoveBySkill'] if 'RemoveBySkill' in row else None
        obj['UserRemove'] = row['UserRemove'] if 'UserRemove' in row else None
        obj['UpdateProp'] = row['UpdateProp']if 'UpdateProp' in row else None
        obj['DeadRemove'] = row['DeadRemove']if 'DeadRemove' in row else None
        # obj['Tradability'] = '%s%s%s%s' % (
        #     'T' if row['MarketTrade'] == 'YES' else 'F',    # Market
        #     'T' if row['UserTrade'] == 'YES' else 'F',      # Players
        #     'T' if row['ShopTrade'] == 'YES' else 'F',      # Shop
        #     'T' if row['TeamTrade'] == 'YES' else 'F',      # Team Storage
        # )
        # obj['Type'] = item_type
        # obj['Weight'] = float(row['Weight']) if 'Weight' in row else None
        globals.buffs[obj['$ID']] = obj
        globals.buffs_by_name[obj['$ID_NAME']] = obj

    ies_file.close()

