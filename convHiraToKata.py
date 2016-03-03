# coding=utf-8

# Simple script to convert everything in a txt file that is a hiragana character, to a katakana character.
# warning, you need a file named 'hira and kana list.txt'. This code is terrible, you shouldn't need it in the first place,
# but this was also a programming exercise for me.

import os as os
from jcconv import *
from codecs import *

def convDelimFileToList(listInput, delim, newLineChar):
    """
    TOFIX: This code will fail if a delimiter is missing in a line on purpose.


    :type delim: unicode
    :type newLineChar: list
    :type listInput: list
    """
    # find the locations of the escape char so that we can convert this into lines.
    newLineCharLength = len(newLineChar)
    if newLineCharLength == 2:
        newLineList = [x for x, letter in enumerate(listInput) if letter == newLineChar[0] or letter == newLineChar[1]]
    else:
        raise NameError('TOFIX: newLineChar only accepts a string of 2 characters long!')
    # find the number of delims per line
    delimList = [x for x, letter in enumerate(listInput) if letter == delim]
    delimPerLineCount = len([x for x, number in enumerate(delimList) if number < newLineList[0]])

    # get rid of last empty line, if it exists.
    newLineListTemp = newLineList
    newLineList = [x for x in newLineListTemp if x < delimList[-1]]

    colCount = delimPerLineCount + 1    # counts the number of columns
    rowCount = len(newLineList)/2 + 1   # counts the number of columns
    tableList = [[None] * rowCount for i in range(colCount)]    # check comment underneath this line
    # if anyone is revisiting this code, the above code is the best way in python to initialize a
    # multidimensional list. Google up 'python multidimensional list initialization'
    # tableList = [[None] * rowCount] * colCount WILL NOT WORK
    contentCount = rowCount * colCount
    tableContent = [None] * contentCount
    y = 0
    text = []
    # form a list of all of table's content in a single dimension. Each content in one slot of the list
    for x in range(0, len(listInput)):
        if listInput[x] == delim or listInput[x] == newLineChar[0]:
            tableContent[y] = text
            text = []
            y += 1
        elif listInput[x] == newLineChar[1]:
            pass
        else:
            text = text + [listInput[x]]    # python requires you to convert it into a list before you do any
            # silly operations.
    # assign said list to the tableList
    y = 0 #colCount interator
    z = 0 #rowCount iterator
    for x in range(0, contentCount):
        if y == colCount:
            z += 1
            y = 0
        tableList[y][z] = tableContent[x]
        y += 1
    return tableList



def main():
    kanaFile = open('E:\Programming\Python\convHiraToKata\kana table.txt', encoding='utf-8', mode='r')
    kanaTable = convDelimFileToList(kanaFile.read(), u' ', '\r\n')
    fileToConvertHiraToKana = open('E:\Programming\Python\convHiraToKata\Kyoukai no Kanata 02.txt',
                                   encoding='utf-8', mode='r')
    fileToConvertString = fileToConvertHiraToKana.read()
    fileToConvertList = list(fileToConvertString)   # python requires you to convert it into a list --
    # -- before you do any fancy operations
    for x in range(0, len(fileToConvertString)):
        # Get character, search character in lookup table and then convert!
        for y in range(0, len(kanaTable[0])):
            if kanaTable[0][y][0] == fileToConvertString[x]:
                kanaFound = 1
                break
            else:
                kanaFound = 0
        if kanaFound == 1:
            fileToConvertList[x] = kanaTable[1][y][0]
    outputFileName = 'E:\Programming\Python\convHiraToKata\Kyoukai no kanata 02 processed.txt'
    try:
        os.remove(outputFileName)
    except StandardError:
        pass
    fileToConvertOutput = ''.join(fileToConvertList)
    outputFile = open(outputFileName, encoding='utf-8', mode='w')
    outputFile.write(fileToConvertOutput)
    return 0
main()