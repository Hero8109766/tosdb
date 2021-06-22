# coding=utf-8
import csv
import logging
import os
import xml.etree.ElementTree as ET

import constants
import globals
import codecs
from parserr.parser_enums import TOSRegion, TOSLanguage
from utils.stringutil import is_ascii

TRANSLATION_PREFIX = '@dicID_^*$'
TRANSLATION_SUFFIX = '$*^'
REGION=None
LANGUAGE=None
def parse(region,language):
    global REGION,LANGUAGE
    REGION=region
    LANGUAGE=language
    translations = None

    if TOSLanguage.ko!=language:
        translations=parse_translations(TOSLanguage.to_full_string(language))
        #translations = parse_translations('English') if region == TOSRegion.iTOS else translations
        #translations = parse_translations('Japanese') if region == TOSRegion.jTOS else translations
        #translations = parse_translations('Taiwanese') if region == TOSRegion.twTOS else translations

    if translations:
        parse_dictionary(translations)
    parse_clmsg()

def parse_dictionary(translations):
    logging.debug('Parsing translations dictionary...')
    dictionary_path = os.path.join(constants.PATH_INPUT_DATA, 'language.ipf', 'wholedicid.xml')
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

            globals.translations[key] = value_translated


def parse_translations(language):
    logging.debug('Parsing translations for %s...', language)
    result = {}

    translation_folder = os.path.join(constants.PATH_INPUT_RELEASE, 'languageData', language)

    for translation in os.listdir(translation_folder):
        translation_path = os.path.join(translation_folder, translation)

        if '.tsv' not in translation:
            continue

        with codecs.open(translation_path, 'r','utf-8',errors="replace") as translation_file:
            for row in csv.reader(translation_file, delimiter='\t', quoting=csv.QUOTE_NONE):
                if len(row) > 1:
                    result[row[0]] = str(row[1])

    return result

def parse_clmsg():
    global globals
    logging.debug('Parsing clmsgs ...')
    result = {}

    dictionary_path = os.path.join(constants.PATH_INPUT_DATA, 'xml_lang.ipf', 'clientmessage.xml')
    dictionary = ET.parse(dictionary_path).getroot()

    # example: <file name="xml\item_Equip.xml">
    for category in dictionary:
        for data in category:
            key = data.get('ClassName')
            value = data.get('Data')
            if key is not None and value is not None:
                globals.clmsgs[key] = translate(value)


def translate(key,secondtouch=False):

    try:
        key = str(key.replace('"', ''), 'utf-8')
    except TypeError:
        pass

    # In case the key is already in english, there's no need to translate
    #if not secondtouch  and is_ascii(key) and REGION==TOSRegion.iTOS:
    #    return key
    if not globals.translations:
        return key

    if (key == '' or key not in globals.translations):
        if  key not in globals.clmsgs:
           # if key != '':
               # logging.warn('Missing translation for key: %s', key)
            return key
        else:
            if key!=globals.clmsgs[key]:
                return translate(globals.clmsgs[key],True)
            else:
                return key
    return globals.translations[key]
