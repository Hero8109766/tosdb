# coding=utf-8
import csv
import logging
import os
import xml.etree.ElementTree as ET

from parserlib import globals
import codecs
from parserlib.parserr.parser_enums import TOSRegion
from parserlib.utils.stringutil import is_ascii

TRANSLATION_PREFIX = '@dicID_^*$'
TRANSLATION_SUFFIX = '$*^'

class Translator:

    def __init__(self,constants):
        self.constants=constants
    def parse(self,region):
        self.clmsgs={}
        self.translations = None
        self.translations = self.parse_translations('English') if region == TOSRegion.iTOS else self.translations
        self.translations = self.parse_translations('Japanese') if region == TOSRegion.jTOS else self.translations
        self.translations = self.parse_translations('Taiwanese') if region == TOSRegion.twTOS else self.translations

        if self.translations:
            self.parse_dictionary(self.translations)
        self.parse_clmsg()

    def parse_dictionary(self,translations):
        logging.debug('Parsing translations dictionary...')
        dictionary_path = os.path.join(self.constants.PATH_INPUT_DATA, 'language.ipf', 'wholedicid.xml')
        dictionary = ET.parse(dictionary_path).getroot()

        # example: <file name="xml\item_Equip.xml">
        for file in dictionary:
            # <data original="없음_helmet" dicid="@dicID_^*$ITEM_20150317_000001$*^"/>
            for data in file:
                key = data.get('original').replace('"', '')
                value = data.get('dicid')
                value_translated = '%s' % data.get('dicid')

                for dicid in value.split(TRANSLATION_SUFFIX):  # Sometimes there are multiple ids in a single entry (as translations are re-used)
                    if TRANSLATION_PREFIX in dicid:
                        dicid = dicid[dicid.index(TRANSLATION_PREFIX) + len(TRANSLATION_PREFIX):]
                        if dicid not in translations:
                            logging.warn('Missing translation for dicid: (%s)', dicid)

                        translation = translations[dicid] if dicid in translations else dicid
                        value_translated = value_translated.replace(TRANSLATION_PREFIX + dicid + TRANSLATION_SUFFIX, translation)

                self.translations[key] = value_translated


    def parse_translations(self,language):
        logging.debug('Parsing translations for %s...', language)
        result = {}

        translation_folder = os.path.join(self.constants.PATH_INPUT_RELEASE, 'languageData', language)

        for translation in os.listdir(translation_folder):
            translation_path = os.path.join(translation_folder, translation)

            if '.tsv' not in translation:
                continue

            with codecs.open(translation_path, 'r','utf-8',errors="replace") as translation_file:
                for row in csv.reader(translation_file, delimiter='\t', quoting=csv.QUOTE_NONE):
                    if len(row) > 1:
                        result[row[0]] = str(row[1])

        return result

    def parse_clmsg(self):

        logging.debug('Parsing clmsgs ...')
        result = {}

        dictionary_path = os.path.join(self.constants.PATH_INPUT_DATA, 'xml_lang.ipf', 'clientmessage.xml')
        dictionary = ET.parse(dictionary_path).getroot()

        # example: <file name="xml\item_Equip.xml">
        for category in dictionary:
            for data in category:
                key = data.get('ClassName')
                value = data.get('Data')
                if key is not None and value is not None:
                    self.clmsgs[key] = self.translate(value)
    def translate(self,key,secondtouch=False):
        try:
            key = str(key.replace('"', ''), 'utf-8')
        except TypeError:
            pass

        # In case the key is already in english, there's no need to translate
        #if is_ascii(key):
        #    return key
        #if not self.translations:
        #    return key

        if not self.translations or (key != '' and key not in self.translations):
            if key not in self.clmsgs:
                # if key != '':
                # logging.warn('Missing translation for key: %s', key)
                return key
            else:
                if key != self.clmsgs[key]:
                    return self.translate(self.clmsgs[key], True)
                else:
                    return key
        elif key=="":
            return ""

        return self.translations[key]
