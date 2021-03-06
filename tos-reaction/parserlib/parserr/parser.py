import gc
import json
import logging
import os
import unicodecsv as csv
from parserlib import constantsmod, globals
from parserlib.parserr import parser_translations, parser_items_books, \
    parser_items_gems, parser_monsters, parser_skills
from parserlib.parserr import parser_items_cubes, parser_items_cards, parser_items_equipment, parser_jobs, \
    parser_items_recipes, parser_attributes, parser_items, parser_assets, parser_items_equipment_sets, \
    parser_items_collections
from parserlib.utils import luautilmod


def csv_write(data, dataset):
    # Clean data
    for row in range(len(data)):
        for col in data[row]:
            cell = data[row][col] = globals.Link.to_dict(data[row][col])

            # Clean lists and convert to JSON
            if isinstance(cell, list):
                cell = [x for x in cell if x is not None]

                # Sort list, in case it's a Link list
                if len(cell) > 0 and isinstance(cell[0], globals.Link):
                    cell.sort()

                data[row][col] = json.dumps(cell, sort_keys=True) if len(cell) > 0 else None
            elif isinstance(cell, dict):
                data[row][col] = json.dumps(cell, sort_keys=True)

    # Ensure destination directory exists
    if not os.path.exists(constantsmod.PATH_BUILD_ASSETS_DATA):
        os.makedirs(constantsmod.PATH_BUILD_ASSETS_DATA)

    # Get keys from a complete entity
    keys = None

    for row in data:
        if keys is None or len(keys) < len(list(row.keys())):
            keys = list(row.keys())
    for k in range(len(data)):
         for kk,vv in data[k].items():
             data[k][kk]=str(vv)

    # Write to CSV
    file = open(os.path.join(constantsmod.PATH_BUILD_ASSETS_DATA, dataset + '.csv'), 'wb')
    if keys is not None:

        writer = csv.DictWriter(
            file,
            delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=sorted(list(map(lambda x:x,keys)))
        )
        writer.writeheader()
        writer.writerows(sorted(data, key=lambda k: k['$ID']))
    file.close()


def parse(region, is_rebuild, is_version_new):
    # Initialize LUA environment
    luautilmod.init()

    # Parse assets (Note: we start by processing assets as they use a ton of RAM)
    parser_assets.parse(region, is_version_new)
    parser_jobs.parse_jobs_images(region, is_version_new)
    #parser_maps.parse_maps_images(region, is_version_new)
    parser_translations.parse(region)

    # Garbage collect...
    logging.debug('Garbage collect...')
    gc.collect()

    # Parse data (1/2) - attributes + items + items_gems + jobs + skills
    logging.debug('Parsing data (1/2)...')
    parser_attributes.parse()
    parser_items.parse()
    parser_items_gems.parse(is_rebuild)
    parser_jobs.parse(is_rebuild)
    parser_skills.parse(is_rebuild)

    # Garbage collect...
    logging.debug('Garbage collect...')
    gc.collect()

    # Parse links (1/2) - attributes + items + items_gems + jobs + skills
    logging.debug('Parsing links (1/2)...')
    parser_attributes.parse_links()
    parser_items_gems.parse_links()
    parser_jobs.parse_links()
    parser_skills.parse_links(is_rebuild)

    parser_attributes.parse_clean()
    parser_skills.parse_clean()

    # Garbage collect...
    logging.debug('Garbage collect...')
    gc.collect()

    # Write CSVs (1/2) - attributes + jobs + skills
    logging.debug('Writing CSVs (1/2)...')
    csv_write(list(globals.attributes.values()), constantsmod.OUTPUT_ATTRIBUTES)
    csv_write(list(globals.jobs.values()), constantsmod.OUTPUT_JOBS)
    csv_write(list(globals.skills.values()), constantsmod.OUTPUT_SKILLS)

    globals.attributes = None
    globals.attributes_by_name = None
    globals.jobs = None
    globals.jobs_by_name = None
    globals.skills = None
    globals.skills_by_name = None

    # Garbage collect...
    logging.debug('Garbage collect...')
    gc.collect()

    # Parse data
    logging.debug('Parsing data (2/2)...')
    parser_items_books.parse()
    parser_items_cards.parse()
    parser_items_collections.parse()
    parser_items_cubes.parse()
    parser_items_equipment.parse()
    parser_items_equipment_sets.parse()
    parser_items_recipes.parse()
    #parser_maps.parse(region, is_version_new)
    parser_monsters.parse()

    # Garbage collect & Destroy LUA...
    logging.debug('Garbage collect...')
    luautilmod.destroy()
    gc.collect()

    # Parse links (2/2)
    logging.debug('Parsing links (2/2)...')
    parser_items.parse_links()
    parser_items_cards.parse_links()
    parser_items_collections.parse_links()
    parser_items_cubes.parse_links()
    parser_items_equipment.parse_links()
    parser_items_equipment_sets.parse_links()
    parser_items_recipes.parse_links()
    #parser_maps.parse_links()
    parser_monsters.parse_links()

    # Garbage collect...
    logging.debug('Garbage collect...')
    gc.collect()

    # Write CSVs (2/2)
    logging.debug('Writing CSVs (2/2)...')
    csv_write(list(globals.books.values()), constantsmod.OUTPUT_BOOKS)
    csv_write(list(globals.cards.values()), constantsmod.OUTPUT_CARDS)
    csv_write(list(globals.collections.values()), constantsmod.OUTPUT_COLLECTIONS)
    csv_write(list(globals.cubes.values()), constantsmod.OUTPUT_CUBES)
    csv_write(list(globals.equipment.values()), constantsmod.OUTPUT_EQUIPMENT)
    csv_write(list(globals.equipment_sets.values()), constantsmod.OUTPUT_EQUIPMENT_SETS)
    csv_write(list(globals.gems.values()), constantsmod.OUTPUT_GEMS)
    csv_write(list(globals.items.values()), constantsmod.OUTPUT_ITEMS)
    csv_write(list(globals.maps.values()), constantsmod.OUTPUT_MAPS)
    csv_write(list(globals.monsters.values()), constantsmod.OUTPUT_MONSTERS)
    csv_write(list(globals.npcs.values()), constantsmod.OUTPUT_NPCS)
    csv_write(list(globals.recipes.values()), constantsmod.OUTPUT_RECIPES)
