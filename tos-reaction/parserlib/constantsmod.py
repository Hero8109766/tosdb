import os

from parserlib.parserr.parser_enums import TOSRegion


class constclass:


    def __init__(self,region):
        self.OUTPUT_ATTRIBUTES = 'attributes'
        self.OUTPUT_BOOKS = 'books'
        self.OUTPUT_CARDS = 'cards'
        self.OUTPUT_COLLECTIONS = 'collections'
        self.OUTPUT_CUBES = 'cubes'
        self.OUTPUT_GEMS = 'gems'
        self.OUTPUT_JOBS = 'jobs'
        self.OUTPUT_EQUIPMENT = 'equipment'
        self.OUTPUT_EQUIPMENT_SETS = 'equipment-sets'
        self.OUTPUT_ITEMS = 'items'
        self.OUTPUT_MAPS = 'maps'
        self.OUTPUT_MONSTERS = 'monsters'
        self.OUTPUT_NPCS = 'npcs'
        self.OUTPUT_RECIPES = 'recipes'
        self.OUTPUT_SKILLS = 'skills'


        self.URL_PATCH = None
        self.URL_PATCH_iTOS = 'http://drygkhncipyq8.cloudfront.net/toslive/patch/'
        self.URL_PATCH_jTOS = 'http://d3bbj7hlpo9jjy.cloudfront.net/live/patch/'
        self.URL_PATCH_kTOS = 'http://tosg.dn.nexoncdn.co.kr/patch/live/'
        self.URL_PATCH_kTEST = 'http://tosg.dn.nexoncdn.co.kr/patch/test/'
        self.URL_PATCH_twTOS = 'http://tospatch.x2game.com.tw/live/patch/'

        self.PATH_INPUT = None
        self.PATH_INPUT_DATA = None
        self.PATH_INPUT_DATA_PATCH = None
        self.PATH_INPUT_DATA_PATCH_URL = None
        self.PATH_INPUT_DATA_PATCH_URL_FULL = None
        self.PATH_INPUT_DATA_REVISION = None
        self.PATH_INPUT_DATA_REVISION_URL = None
        self.PATH_INPUT_DATA_REVISION_URL_FULL = None
        self.PATH_INPUT_RELEASE = None
        self.PATH_INPUT_RELEASE_PATCH = None
        self.PATH_INPUT_RELEASE_PATCH_URL = None
        self.PATH_INPUT_RELEASE_REVISION = None
        self.PATH_INPUT_RELEASE_REVISION_URL = None

        self.PATH_PARSER = os.path.join('..', 'tos-parser')

        self.PATH_UNPACKER = os.path.join('..', 'ipf_unpacker')
        self.PATH_UNPACKER_EXE ="./ipf_unpack"

        self.PATH_BUILD = os.path.join('..', 'tos-build', 'dist')
        self.PATH_BUILD_ASSETS = os.path.join(self.PATH_BUILD, 'assets')
        self.PATH_BUILD_ASSETS_DATA = None
        self.PATH_BUILD_ASSETS_ICONS = os.path.join(self.PATH_BUILD_ASSETS, 'icons')
        self.PATH_BUILD_ASSETS_IMAGES = os.path.join(self.PATH_BUILD_ASSETS, 'images')
        self.PATH_BUILD_ASSETS_IMAGES_MAPS = os.path.join(self.PATH_BUILD_ASSETS_IMAGES, 'maps')
        self.region(region)
        self.REGION=region
    def region(self,region):


        region_str = TOSRegion.to_string(region)

        self.URL_PATCH = self.URL_PATCH_iTOS if region == TOSRegion.iTOS else self.URL_PATCH
        self.URL_PATCH = self.URL_PATCH_jTOS if region == TOSRegion.jTOS else self.URL_PATCH
        self.URL_PATCH = self.URL_PATCH_kTOS if region == TOSRegion.kTOS else self.URL_PATCH
        self.URL_PATCH = self.URL_PATCH_kTEST if region == TOSRegion.kTEST else self.URL_PATCH
        self.URL_PATCH = self.URL_PATCH_twTOS if region == TOSRegion.twTOS else self.URL_PATCH

        self.PATH_INPUT = os.path.join(self.PATH_PARSER, 'input', region_str)
        self.PATH_INPUT_DATA = os.path.join(self.PATH_INPUT, 'data')
        self.PATH_INPUT_DATA_PATCH = os.path.join(self.PATH_INPUT_DATA, 'patch')
        self.PATH_INPUT_DATA_PATCH_URL = self.URL_PATCH + 'partial/data/'
        self.PATH_INPUT_DATA_PATCH_URL_FULL = self.URL_PATCH + 'full/data/'
        self.PATH_INPUT_DATA_REVISION = os.path.join(self.PATH_INPUT, 'data.revision.txt')
        self.PATH_INPUT_DATA_REVISION_URL = self.URL_PATCH + 'partial/data.revision.txt'
        self.PATH_INPUT_DATA_REVISION_URL_FULL = self.URL_PATCH + 'full/data.file.list.txt'
        self.PATH_INPUT_RELEASE = os.path.join(self.PATH_INPUT, 'release')
        self.PATH_INPUT_RELEASE_PATCH = os.path.join(self.PATH_INPUT_RELEASE, 'patch')
        self.PATH_INPUT_RELEASE_PATCH_URL = self.URL_PATCH + 'partial/release/'
        self.PATH_INPUT_RELEASE_REVISION = os.path.join(self.PATH_INPUT, 'release.revision.txt')
        self.PATH_INPUT_RELEASE_REVISION_URL = self.URL_PATCH + 'partial/release.revision.txt'

        self.PATH_BUILD_ASSETS_DATA = os.path.join(self.PATH_BUILD_ASSETS, 'data', region_str.lower())
