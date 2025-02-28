import pandas as pd
from collections.abc import Generator

from divide_word_by_syllables import divideBy
from utilities.files import writeCSV


def divideWordsBySyllables(words, syllables) -> Generator[tuple[str, str], None, None]:
    for word in words:
        yield word, '-'.join(divideBy(word, syllables))


def main():
    wordFrequenciesDf = readDataFrame('../data/words.csv')
    words = [row['word'] for index, row in wordFrequenciesDf.iterrows()]
    syllablesFrequenciesDf = readDataFrame('../data/syllables_sorted.csv')
    syllables = [row['syllable'] for index, row in syllablesFrequenciesDf.iterrows()]

    dividedWords = list(divideWordsBySyllables(words, syllables))

    writeResult('../data/divided_words.csv', dividedWords)
    printResult(dividedWords)


def readDataFrame(fileName: str):
    return pd.read_csv(fileName)


def writeResult(fileName: str, records: list[tuple[str, str]]):
    data = [('word', 'divided')] + records
    writeCSV(fileName, data)


def printResult(dividedWords):
    print(f'Words count is {len(dividedWords)}')


if __name__ == '__main__':
    main()
