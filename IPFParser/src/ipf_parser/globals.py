from ipf_parser import constants

assets_icons = {}
assets_icons_used = []

attributes = {}
attributes_by_name = {}
books = {}
books_by_name = {}
cards = {}
cards_by_name = {}
jobs = {}
jobs_by_name = {}
collections = {}
collections_by_name = {}
cubes = {}
cubes_by_name = {}
cubes_by_stringarg = {}
gems = {}
gems_by_name = {}
equipment = {}
equipment_by_name = {}
equipment_sets = {}
equipment_sets_by_name = {}
items = {}
items_by_name = {}
maps = {}
maps_by_name = {}
monsters = {}
monsters_by_name = {}
recipes = {}
recipes_by_name = {}
skills = {}
skills_by_name = {}
translations = {}

all_items_by_name = [
    books_by_name,
    cards_by_name,
    collections_by_name,
    cubes_by_name,
    gems_by_name,
    equipment_by_name,
    items_by_name,
    recipes_by_name
]


def get_attribute_link(name):
    return _get_entity_link(name, attributes_by_name)


def get_book_link(name):
    return _get_entity_link(name, books_by_name)


def get_card_link(name):
    return _get_entity_link(name, cards_by_name)


def get_job_link(name):
    return _get_entity_link(name, jobs_by_name)


def get_collection_link(name):
    return _get_entity_link(name, collections_by_name)


def get_cube_link(name):
    return _get_entity_link(name, cubes_by_name)


def get_gem_link(name):
    return _get_entity_link(name, gems_by_name)


def get_equipment_link(name):
    return _get_entity_link(name, equipment_by_name)


def get_equipment_set_link(name):
    return _get_entity_link(name, equipment_sets_by_name)


def get_item_link(name):
    if name == 'Moneybag1':
        return {
            '$ID': -1,
            '$ID_NAME': None,
            'Icon': 'icon_item_silver',
            'Name': 'Silver'
        }
    else:
        for xx_by_name in all_items_by_name:
            item = _get_entity_link(name, xx_by_name)

            if item is not None:
                return item

        return None


def get_map_link(name):
    return _get_entity_link(name, maps_by_name)


def get_monster_link(name):
    return _get_entity_link(name, monsters_by_name)


def get_recipe_link(name):
    return _get_entity_link(name, recipes_by_name)


def get_skill_link(name):
    return _get_entity_link(name, skills_by_name)


def _get_entity_link(name, collection):
    if name not in collection:
        return None

    collection_path = None
    collection_path = constants.OUTPUT_ATTRIBUTES if collection == attributes_by_name else collection_path
    collection_path = constants.OUTPUT_BOOKS if collection == books_by_name else collection_path
    collection_path = constants.OUTPUT_CARDS if collection == cards_by_name else collection_path
    collection_path = constants.OUTPUT_JOBS if collection == jobs_by_name else collection_path
    collection_path = constants.OUTPUT_COLLECTIONS if collection == collections_by_name else collection_path
    collection_path = constants.OUTPUT_CUBES if collection == cubes_by_name else collection_path
    collection_path = constants.OUTPUT_GEMS if collection == gems_by_name else collection_path
    collection_path = constants.OUTPUT_EQUIPMENT if collection == equipment_by_name else collection_path
    collection_path = constants.OUTPUT_EQUIPMENT_SETS if collection == equipment_sets_by_name else collection_path
    collection_path = constants.OUTPUT_ITEMS if collection == items_by_name else collection_path
    collection_path = constants.OUTPUT_MAPS if collection == maps_by_name else collection_path
    collection_path = constants.OUTPUT_MONSTERS if collection == monsters_by_name else collection_path
    collection_path = constants.OUTPUT_RECIPES if collection == recipes_by_name else collection_path
    collection_path = constants.OUTPUT_SKILLS if collection == skills_by_name else collection_path

    return Link(collection[name], collection_path[:-4])


# Helper class to delay the toString operation
# For example, Recipes only have their name calculated after the parse_links operation
class Link:

    def __init__(self, entity, collection):
        self.entity = entity
        self.collection = collection

    def __getitem__(self, item):
        return self.entity[item]

    def __str__(self):
        return str(self.dict())

    def dict(self):
        return {
            '$ID': self.entity['$ID'],
            '$ID_NAME': self.entity['$ID_NAME'],
            'Icon': self.entity['Icon'],
            'Name': self.entity['Name'],
            'Url': self.collection,
        }

    @staticmethod
    def to_dict(obj, level=2):
        if isinstance(obj, (list,)) and level > 0:
            return Link.to_dict([Link.to_dict(o, level - 1) for o in obj], level - 1)
        if isinstance(obj, (dict,)) and level > 0:
            return Link.to_dict({k: Link.to_dict(v, level - 1) for k, v in obj.iteritems()}, level - 1)
        if isinstance(obj, (Link,)):
            return obj.dict()
        return obj
