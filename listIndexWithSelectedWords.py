# This script will generate the number of times words from a word list, 
# generated from a text source, appears in a Nayr's Core5000 card.
# For example, if there's 100 words in the word list, and 5 of those words
# appear in a Nayr's Core5k card, the index for that particular card will be 5.
# Nifty, isn't it?

# Prerequisites:
# You need Nayr's Core5000 Anki deck, exported as CSV, for this. It can be easily Googled.
# Also required is a list of words, generated using a software by cb4960 http://forum.koohii.com/post-167827.html#pid167827

import csv


class ListSentenceWithSelectedWords:
    def __init__(self, wordMinCharLength, minWordMatches, wordListCSVPath, ankiNayrsDeckCSVPath,
                 ankiNayrsSentenceColumn, kanaCSVPath):

        # variables initialization. always initialize variables first
        self.wordMinCharLength = wordMinCharLength
        self.minWordMatches = minWordMatches
        self.wordListCSVPath = wordListCSVPath
        self.ankiNayrsDeckCSVPath = ankiNayrsDeckCSVPath
        self.kanaCSVPath = kanaCSVPath
        self.ankiNayrsSentenceColumn = ankiNayrsSentenceColumn

        # functions initialization
        self.processedWordsTuple = self._wordsOfMinLength()
        self.processedWordsTuple = self._checkProcessedWordsTupleForKana()


    def _importRawWordListCSV(self):
        with open(self.wordListCSVPath, newline='\r\n', encoding='utf-8') as csvfile:
            veryRawWordList = csv.reader(csvfile, delimiter='\t')
            rawWordList = []
            for row in veryRawWordList:
                rawWordList.append(row)
        return rawWordList

    def _areWordsInString(self, wordList, inputString):
        return set(wordList).intersection(inputString.split())  # boolean output

    def _wordsOfMinLength(self):
        rawWordList = self._importRawWordListCSV()
        processedWordsList = []
        for row in rawWordList:
            if len(row[1]) >= self.wordMinCharLength:
                processedWordsList += [row[1]]
        processedWordsTuple = tuple(processedWordsList)
        return processedWordsTuple

    def _checkProcessedWordsTupleForKana(self):
        processedWordsList = list(self.processedWordsTuple)
        with open(self.kanaCSVPath, newline='\r\n', encoding='utf-8') as csvfile:
            kanaListCSVObj = csv.reader(csvfile, delimiter=' ')
            kanaList = []
            for kana in kanaListCSVObj:
                kanaList += [kana[0]]
            for kana in kanaListCSVObj:
                kanaList += [kana[1]]
            for kana in kanaList:
                for processedWordsListIndex, word in enumerate(processedWordsList):
                    if kana == word:
                        del processedWordsList[processedWordsListIndex]
        processedWordsTuple = tuple(processedWordsList)
        return processedWordsTuple

    def _importAnkiNayrsDeckCSV(self):
        cardList = []
        with open(self.ankiNayrsDeckCSVPath, newline='\n', encoding='utf-8') as csvfile:
            rawCardList = csv.reader(csvfile, delimiter='\t')
            for row in rawCardList:
                cardList.append(row)
        return cardList


    def outputIndexInTableFormat(self):
        cardList = self._importAnkiNayrsDeckCSV()
        freqIndexOnDeckList = []
        for num, cardRow in enumerate(cardList):
            numberOfMatches = 0
            for x in range(0, self.minWordMatches):
                for wordNum, word in enumerate(self.processedWordsTuple):
                    if word in cardRow[self.ankiNayrsSentenceColumn]:
                        cardRow[self.ankiNayrsSentenceColumn] = cardRow[self.ankiNayrsSentenceColumn].replace(word, '')
                        numberOfMatches += 1
                if x == self.minWordMatches - 1 and numberOfMatches == self.minWordMatches:
                    freqIndexOnDeckList += [num + 1]
        return freqIndexOnDeckList


def main():
    # WCC is a reference to World Class Create. I used World Class Create to generate my deck.
    WCCClass = ListSentenceWithSelectedWords(wordMinCharLength=1,
                                             minWordMatches=5,
                                             wordListCSVPath='E:\Adek\Programming\Python\convHiraToKata\word_freq_report.txt',
                                             ankiNayrsDeckCSVPath='E:\\Adek\\Programming\\Python\\convHiraToKata\\Nayrs_Core5000.txt',
                                             ankiNayrsSentenceColumn=1,
                                             kanaCSVPath='E:\Adek\Programming\Python\convHiraToKata\kana table.txt')
    freqIndex = WCCClass.outputIndexInTableFormat()
    for k, row in enumerate(freqIndex):
        #print(str(k) + ' - ' + str(row))
        print(str(row) + '\t' + str(k + 1))
main()
