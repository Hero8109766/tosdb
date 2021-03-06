import os

from parserr.parser_enums import TOSRegion, TOSLanguage

OUTPUT_ATTRIBUTES = 'attributes'
OUTPUT_BOOKS = 'books'
OUTPUT_BUFFS = 'buffs'
OUTPUT_CARDS = 'cards'
OUTPUT_COLLECTIONS = 'collections'
OUTPUT_CUBES = 'cubes'
OUTPUT_GEMS = 'gems'
OUTPUT_JOBS = 'jobs'
OUTPUT_EQUIPMENT = 'equipment'
OUTPUT_EQUIPMENT_SETS = 'equipment-sets'
OUTPUT_ITEMS = 'items'
OUTPUT_MAPS = 'maps'
OUTPUT_MONSTERS = 'monsters'
OUTPUT_MONSTER_SKILLS = 'monster_skills'
OUTPUT_NPCS = 'npcs'
OUTPUT_RECIPES = 'recipes'
OUTPUT_SKILLS = 'skills'

COMPARE_WITH_NEET= False

URL_PATCH = None
URL_PATCH_iTOS = 'http://drygkhncipyq8.cloudfront.net/toslive/patch/'
URL_PATCH_jTOS = 'http://d3bbj7hlpo9jjy.cloudfront.net/live/patch/'
URL_PATCH_kTOS = 'http://tosg.dn.nexoncdn.co.kr/patch/live/'
URL_PATCH_kTEST = 'http://tosg.dn.nexoncdn.co.kr/patch/test/'
URL_PATCH_twTOS = 'http://tospatch.x2game.com.tw/live/patch/'

PATH_INPUT = None
PATH_INPUT_DATA = None
PATH_INPUT_DATA_PATCH = None
PATH_INPUT_DATA_PATCH_URL = None
PATH_INPUT_DATA_PATCH_URL_FULL = None
PATH_INPUT_DATA_REVISION = None
PATH_INPUT_DATA_REVISION_URL = None
PATH_INPUT_DATA_REVISION_URL_FULL = None
PATH_INPUT_KTOS = None
PATH_INPUT_DATA_KTOS = None
PATH_INPUT_ITOS = None
PATH_INPUT_DATA_ITOS = None
PATH_INPUT_RELEASE = None
PATH_INPUT_RELEASE_PATCH = None
PATH_INPUT_RELEASE_PATCH_URL = None
PATH_INPUT_RELEASE_PATCH_FULL_URL = None
PATH_INPUT_RELEASE_REVISION = None
PATH_INPUT_RELEASE_REVISION_URL = None
PATH_INPUT_RELEASE_REVISION_FULL_URL = None
PATH_INPUT_RELEASE_FULL_URL=None
PATH_PARSER = os.path.join('..', 'tos-parser')
region_str = None
language_str = None
PATH_UNPACKER = os.path.join('..', 'ipf_unpacker')
PATH_UNPACKER_EXE ="../../ipf_unpack"
#PATH_UNPACKER_UNIPF ="dotnet"
#PATH_UNPACKER_UNIPF2 ="../../tpIpfToolCmd.dll"
PATH_UNPACKER_LIBIPF ="unipf"
PATH_BUILD = os.path.join('..', 'tos-build', 'dist')
PATH_BUILD_ASSETS = os.path.join(PATH_BUILD, 'assets')
PATH_BUILD_ASSETS_DATA = None
PATH_BUILD_ASSETS_ICONS = os.path.join(PATH_BUILD_ASSETS, 'icons')
PATH_BUILD_ASSETS_IMAGES = os.path.join(PATH_BUILD_ASSETS, 'images')
PATH_BUILD_ASSETS_IMAGES_MAPS = os.path.join(PATH_BUILD_ASSETS_IMAGES, 'maps')

def region(region,language):
    global\
        URL_PATCH, \
        PATH_INPUT, \
        PATH_INPUT_DATA, \
        PATH_INPUT_DATA_PATCH, \
        PATH_INPUT_DATA_PATCH_URL, \
        PATH_INPUT_DATA_PATCH_URL_FULL, \
        PATH_INPUT_DATA_REVISION, \
        PATH_INPUT_DATA_REVISION_URL, \
        PATH_INPUT_DATA_REVISION_URL_FULL, \
        PATH_INPUT_KTOS, \
        PATH_INPUT_DATA_KTOS, \
        PATH_INPUT_ITOS, \
        PATH_INPUT_DATA_ITOS, \
        PATH_INPUT_RELEASE, \
        PATH_INPUT_RELEASE_PATCH, \
        PATH_INPUT_RELEASE_PATCH_URL, \
        PATH_INPUT_RELEASE_REVISION, \
        PATH_INPUT_RELEASE_REVISION_URL, \
        PATH_INPUT_RELEASE_REVISION_URL, \
        PATH_INPUT_RELEASE_PATCH_FULL_URL, \
        PATH_INPUT_RELEASE_FULL_URL, \
        PATH_BUILD_ASSETS_DATA, \
        PATH_UNPACKER, \
        region_str, \
        language_str
    region_str = TOSRegion.to_string(region)
    language_str = TOSLanguage.to_string(language)
    URL_PATCH = URL_PATCH_iTOS if region == TOSRegion.iTOS else URL_PATCH
    URL_PATCH = URL_PATCH_jTOS if region == TOSRegion.jTOS else URL_PATCH
    URL_PATCH = URL_PATCH_kTOS if region == TOSRegion.kTOS else URL_PATCH
    URL_PATCH = URL_PATCH_kTEST if region == TOSRegion.kTEST else URL_PATCH
    URL_PATCH = URL_PATCH_twTOS if region == TOSRegion.twTOS else URL_PATCH
    PATH_UNPACKER = os.path.join('..', 'ipf_unpacker')
    PATH_INPUT = os.path.join(PATH_PARSER, 'input', region_str)
    PATH_INPUT_DATA = os.path.join(PATH_INPUT, 'data')
    PATH_INPUT_KTOS = os.path.join(PATH_PARSER, 'input', "kTOS")
    PATH_INPUT_DATA_KTOS = os.path.join(PATH_INPUT_KTOS, 'data')
    PATH_INPUT_ITOS = os.path.join(PATH_PARSER, 'input', "iTOS")
    PATH_INPUT_DATA_ITOS = os.path.join(PATH_INPUT_ITOS, 'data')
    PATH_INPUT_DATA_PATCH = os.path.join(PATH_INPUT_DATA, 'patch')
    PATH_INPUT_DATA_PATCH_URL = URL_PATCH + 'partial/data/'
    PATH_INPUT_DATA_PATCH_URL_FULL = URL_PATCH + 'full/data/'
    PATH_INPUT_DATA_REVISION = os.path.join(PATH_INPUT, 'data.revision.txt')
    PATH_INPUT_DATA_REVISION_URL = URL_PATCH + 'partial/data.revision.txt'
    PATH_INPUT_DATA_REVISION_URL_FULL = URL_PATCH + 'full/data.file.list.txt'
    PATH_INPUT_RELEASE = os.path.join(PATH_INPUT, 'release')
    PATH_INPUT_RELEASE_PATCH = os.path.join(PATH_INPUT_RELEASE, 'patch')
    PATH_INPUT_RELEASE_PATCH_URL = URL_PATCH + 'partial/release/'
    PATH_INPUT_RELEASE_PATCH_FULL_URL =  URL_PATCH + 'full/release/'
    PATH_INPUT_RELEASE_REVISION = os.path.join(PATH_INPUT, 'release.revision.txt')
    PATH_INPUT_RELEASE_REVISION_URL = URL_PATCH + 'partial/release.revision.txt'
    PATH_INPUT_RELEASE_FULL_URL = URL_PATCH + 'full/release.revision.txt'

    PATH_BUILD_ASSETS_DATA = os.path.join(PATH_BUILD_ASSETS, 'data', region_str.lower(),language_str.lower())
