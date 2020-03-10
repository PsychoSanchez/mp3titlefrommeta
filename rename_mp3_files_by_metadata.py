from os import listdir, rename
from os.path import isfile, join, dirname, realpath, splitext
import re

import eyed3


UNKNOWN = 'Unknown'

execFolder = dirname(realpath(__file__))
execFolderfiles = [f for f in listdir(
    execFolder) if isfile(join(execFolder, f))]


def replaceForbiddenSymbolsFromFileName(filename):
    return re.sub(r"(<|>|:|\"|\/|\\|\||\?|\*)", '', filename)


def renameMp3AudioFile(audioFileTag, oldFileName):
    if (audioFileTag.artist == None or audioFileTag.artist == '') and (audioFileTag.title == None or audioFileTag.title == ''):
        print(oldFileName + ' was not renamed. No metadata.')
        return

    artist = (UNKNOWN if audioFileTag.artist ==
              None else audioFileTag.artist)

    title = (UNKNOWN if audioFileTag.title ==
             None else audioFileTag.title)

    newFileName = replaceForbiddenSymbolsFromFileName(
        artist + ' - ' + title)

    renameFileRecursively(oldFileName, newFileName)


def renameFileRecursively(oldFileName, newFileName, tryNumber=0):
    try:
        targetFileName = newFileName + '.mp3'

        if tryNumber > 0:
            targetFileName = newFileName + '(' + str(tryNumber) + ')' + '.mp3'

        rename(join(execFolder, oldFileName), join(
            execFolder, targetFileName))
    except FileExistsError:
        renameFileRecursively(oldFileName, newFileName, tryNumber + 1)
        pass


for fileName in execFolderfiles:
    (_, ext) = splitext(fileName)

    if ext != '.mp3':
        continue

    audioFile = eyed3.load(fileName)

    if audioFile != None and audioFile.tag != None:
        renameMp3AudioFile(audioFile.tag, fileName)
