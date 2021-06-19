import logging
import os
import struct
import urllib.request, urllib.error, urllib.parse

from parserlib import constantsmod
from libs import blowfish
from parserlib.patcherr import patcher_pak, patcher_ipf
from parserlib.patcherr.patcher_ipf import IPF_BLACKLIST

CHUNK_SIZE = 128 * 1024 * 1024  # 128MB of Chunk Size


def patch(repatch):
    logging.debug('Patching...')

    # Full patch
    patch_full(
        constantsmod.PATH_INPUT_DATA, constantsmod.PATH_INPUT_DATA_PATCH, constantsmod.PATH_INPUT_DATA_PATCH_URL_FULL, '.ipf', patcher_ipf.unpack,
        constantsmod.PATH_INPUT_DATA_REVISION_URL_FULL,repatch
    )

    # Partial patches
    version_data, version_data_new = patch_partial(
        constantsmod.PATH_INPUT_DATA_PATCH, constantsmod.PATH_INPUT_DATA_PATCH_URL, '.ipf', patcher_ipf.unpack,
        constantsmod.PATH_INPUT_DATA_REVISION, constantsmod.PATH_INPUT_DATA_REVISION_URL,repatch
    )
    version_release, version_release_new = patch_partial(
        constantsmod.PATH_INPUT_RELEASE_PATCH, constantsmod.PATH_INPUT_RELEASE_PATCH_URL, '.pak', patcher_pak.unpack,
        constantsmod.PATH_INPUT_RELEASE_REVISION, constantsmod.PATH_INPUT_RELEASE_REVISION_URL,repatch
    )

    version_new = 'patch_' + str(version_data_new) + '_release_' + str(version_release_new)
    version_old = 'patch_' + str(version_data) + '_release_' + str(version_release)

    return version_old, version_new


def patch_full(patch_destination, patch_path, patch_url, patch_ext, patch_unpack, revision_url,repatch):
    logging.debug('Patching %s...', revision_url)
    revision_list = urllib.request.urlopen(revision_url).read()
    revision_list = revision_decrypt(revision_list)

    for revision in revision_list:
        # Download patch
        patch_name = revision + patch_ext
        patch_file = os.path.join(patch_path, patch_name)
        if (not os.path.exists(os.path.join(patch_destination, patch_name)) or repatch==1  )and patch_name not in IPF_BLACKLIST :
            logging.debug('Lets Downloading %s...', patch_url + patch_name)
            filesize=0
            if os.path.exists(os.path.join(patch_destination, patch_name)):
                filesize = os.path.getsize(os.path.join(patch_destination, patch_name))
            
            patch_process(patch_file, patch_name, patch_unpack, patch_url)


def patch_partial(patch_path, patch_url, patch_ext, patch_unpack, revision_path, revision_url,repatch):
    logging.debug('Patching %s...', revision_url)
    revision_list = urllib.request.urlopen(revision_url).read()
    revision_list = revision_decrypt(revision_list)
    revision_old = revision_txt_read(revision_path)
    revision_new = revision_old

    for revision in revision_list:
        revision = revision.split(' ')[0]
        if constantsmod.COMPARE_WITH_NEET:
            if int(revision)>315941 and patch_ext=='.ipf':
                break

        if (int(revision) > int(revision_old) or repatch==1) and revision not in ['147674']:
            # Process patch
            patch_name = revision + '_001001' + patch_ext
            patch_file = os.path.join(patch_path, patch_name)
            filesize = 0
            if os.path.isfile(patch_file):
                filesize = os.path.getsize(patch_file)
            
            patch_process(patch_file, patch_name, patch_unpack, patch_url)

            # Update revision
            revision_txt_write(revision_path, revision)
            revision_new = revision

    return revision_old, revision_new


def patch_process(patch_file, patch_name, patch_unpack, patch_url):
    # Ensure patch_file destination exists
    if not os.path.exists(os.path.dirname(patch_file)):
        os.makedirs(os.path.dirname(patch_file))
    def request_as_fox(url):
        headers={"User-Agent":"tos"}
        return urllib.request.Request(url,None,headers)

    filesize = 0
    if os.path.exists(patch_file):
        filesize = os.path.getsize(patch_file)

    if not os.path.isfile(patch_file) or filesize==0:
        # Download patch
        logging.debug('Downloading %s ...', patch_url + patch_name)
        patch_response = urllib.request.urlopen(request_as_fox(patch_url + patch_name))

        with open(patch_file, 'wb') as file:
            file.write(patch_response.read())
    else:
        logging.debug("Reusing cache %s...",patch_name)

    if os.path.isfile(patch_file):
        filesize = os.path.getsize(patch_file)

    if filesize == 0:
        logging.warning('Filesize is ZERO %s...', patch_file)
    else:
        pass
    # Extract patch
    patch_unpack(patch_name)

    # Delete patch
    #os.remove(patch_file)


def revision_decrypt(revision):
    # Thanks to https://github.com/celophi/Arboretum/blob/master/Arboretum.Lib/Decryptor.cs
    size_unencrypted = struct.unpack_from('@i', revision, 0)[0]
    size_encrypted = struct.unpack_from('@i', revision, 4)[0]

    revision = [ord(chr(c)) for c in revision]               # Convert to binary
    blowfish.Decipher(revision, 8, size_encrypted)      # Decrypt with blowfish
    revision = [chr(c) for c in revision]            # Convert back to unicode characters

    # Clean and split into a list
    #revision = ''\
    #    .join(revision[8:])\
    #    .encode('ascii', 'ignore')\
    #    .split('\r\n')
    revision = ''\
        .join(revision[8:])\
        .split('\r\n')
    return revision[:-1]


def revision_txt_read(revision_txt):
    if os.path.isfile(revision_txt):
        with open(revision_txt, 'r') as file:
            return file.readline()
    else:
        return 0


def revision_txt_write(revision_txt, revision):
    with open(revision_txt, 'w') as file:
        file.write(revision)
