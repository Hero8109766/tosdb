import csv
import logging
import os

from parserlib import constantsmod, globals
import codecs

def parse():
    parse_cubes()


def parse_cubes():
    logging.debug('Parsing cubes...')

    for id in globals.cubes:
        obj = globals.cubes[id]

        # Add additional fields
        obj['Link_Items'] = []


def parse_links():
    parse_links_items()


def parse_links_items():
    logging.debug('Parsing items for cubes...')

    ies_path = os.path.join(constantsmod.PATH_INPUT_DATA, 'ies.ipf', 'reward_indun.ies')
    ies_file = codecs.open(ies_path,'r','utf-8',errors='replace')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

    for row in ies_reader:
        if row['Group'] not in globals.cubes_by_stringarg:
            continue

        cube = globals.cubes_by_stringarg[row['Group']]
        cube['Link_Items'].append(globals.get_item_link(row['ItemName']))

    ies_file.close()
