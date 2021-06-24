import logging
import os
import shutil
import subprocess
import glob
import constants
from parserr.parser_translations import LANGUAGE, REGION
from utils import fileutil

IPF_BLACKLIST = [
    'animation.ipf',
    'bg_hi.ipf',
    'bg_hi2.ipf',
    'bg_hi3.ipf',
    'bg_lightcell.ipf',
    'bg_texture.ipf',
    'char_hi.ipf',
    'char_texture.ipf',
    'char_texture_low.ipf',
    'deadslice.ipf',
    'decal.ipf',
    'effect.ipf',
    'etc.ipf',
    'item_hi.ipf',
    'item_texture.ipf',
    'item_texture_low.ipf',
    'shader.ipf',
    'sound.ipf',
    'sprite.ipf',
    'SumAni.ipf',
    'templatepc.ipf',
]


def unpack(ipf):
    ipf = os.path.join(constants.PATH_INPUT_DATA_PATCH, ipf)

    unpacker_path=os.path.join(constants.PATH_UNPACKER,constants.region_str,constants.language_str)
    if not os.path.exists(unpacker_path):
        os.makedirs(unpacker_path)
    ipf_extract = os.path.join(unpacker_path, "extract")
    if not os.path.exists(ipf_extract):
        os.makedirs(ipf_extract)
    ipf_revision = os.path.basename(ipf)[:-4]
    logging.debug('Unpacking %s...', ipf)
    tmpname="tmp.ipf"
    extdir = os.path.join(unpacker_path, 'extract2')
    if not os.path.exists(extdir):
        os.makedirs(extdir)
    shutil.copyfile(ipf, os.path.join(unpacker_path, tmpname))
    prevcurdir = os.getcwd()
    os.chdir(unpacker_path)
    # Decrypt and extract ipf file
    subprocess.check_call(
        [constants.PATH_UNPACKER_LIBIPF,  tmpname,"extract2"],
        stdin=None, stdout=None, stderr=None, shell=False
    )

    os.chdir(prevcurdir)
    #fileutil.move_tree(extdir,ipf_extract)

    if os.path.exists(extdir):

        # Make all files lower case
        fileutil.to_lower(extdir)

        # Move extracted IPF files to data directory
        fileutil.move_tree(extdir, constants.PATH_INPUT_DATA)

        # Remove extract directory
        shutil.rmtree(extdir)
    if os.path.exists(extdir):
        shutil.rmtree(extdir)


    # pass 2

    shutil.copyfile(ipf,os.path.join(unpacker_path,tmpname))

    os.chdir(unpacker_path)
    # Decrypt and extract ipf file
    #if ipf_revision not in ['29_001001']:  # HotFix: these specific patches aren't encrypted for some reason
    subprocess.check_call(
        [constants.PATH_UNPACKER_EXE, tmpname, "decrypt"],
        stdin=None, stdout=None, stderr=None, shell=False
    )

    subprocess.check_call(
        [constants.PATH_UNPACKER_EXE,  tmpname, "extract"],
        stdin=None, stdout=None, stderr=None, shell=False
    )
    os.chdir(prevcurdir)

    if os.path.exists(ipf_extract):

        # Make all files lower case
        fileutil.to_lower(ipf_extract)
        abspath=os.path.abspath(constants.PATH_INPUT_DATA)
        os.chdir(ipf_extract)
        for path in glob.glob("**/*.ies",recursive=True):
            shutil.copyfile(path,os.path.join(abspath,path))
        os.chdir(prevcurdir)
        # Remove extract directory
        shutil.rmtree(ipf_extract)