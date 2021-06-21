import csv
import logging
import os

from parserlib import constantsmod, globals

import codecs
def parse():
    parse_collections()


def parse_collections():
    logging.debug('Parsing collections...')

    for id in globals.collections:
        obj = globals.collections[id]

        # Add additional fields
        obj['Bonus'] = []
        obj['Link_Items'] = []


def parse_links():
    parse_links_items()


def parse_links_items():
    logging.debug('Parsing items for collections...')

    ies_path = os.path.join(constantsmod.PATH_INPUT_DATA, 'ies.ipf', 'collection.ies')
    ies_file = codecs.open(ies_path,'r','utf-8',errors='replace')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

    for row in ies_reader:
        if row['ClassName'] not in globals.collections_by_name:
            continue

        collection = globals.collections_by_name[row['ClassName']]

        # Parse items
        for i in range(1, 10):
            item_name = row['ItemName_' + str(i)]

            if item_name == '':
                continue

            collection['Link_Items'].append(globals.get_item_link(item_name))

        # Parse bonus
        bonus = row['PropList'].split('/') + row['AccPropList'].split('/')
        bonus = [x for x in bonus if len(x) > 0]

        for i in range(0, len(bonus), 2):
            collection['Bonus'].append([
                parse_links_items_bonus_stat(bonus[i]),   # Property
                int(bonus[i + 1])                         # Value
            ])

    ies_file.close()


def parse_links_items_bonus_stat(stat):
    return {
        'CON_BM': 'CON',
        'DEX_BM': 'DEX',
        'INT_BM': 'INT',
        'MNA_BM': 'SPR',
        'STR_BM': 'STR',

        'CRTATK_BM': 'Critical Attack',
        'CRTMATK_BM': 'Critical Magic Attack',
        'CRTHR_BM': 'Critical Rate',
        'CRTDR_BM': 'Critical Defense',

        'MHP_BM': 'Maximum HP',
        'MSP_BM': 'Maximum SP',
        'RHP_BM': 'HP Recovery',
        'RSP_BM': 'SP Recovery',

        'DEF_BM': 'Defense',
        'MDEF_BM': 'Magic Defense',
        'MATK_BM': 'Magic Attack',
        'PATK_BM': 'Physical Attack',

        'DR_BM': 'Evasion',
        'HR_BM': 'Accuracy',
        'MHR_BM': 'Magic Amplification',  # ???

        'ResDark_BM': 'Dark Property Resistance',
        'ResEarth_BM': 'Earth Property Resistance',
        'ResHoly_BM': 'Holy Property Resistance',

        'MaxSta_BM': 'Stamina',
        'MaxAccountWarehouseCount': 'Team Storage Slots',
        'MaxWeight_Bonus': 'Weight Limit',
        'MaxWeight_BM': 'Weight Limit BM',
    }[stat]