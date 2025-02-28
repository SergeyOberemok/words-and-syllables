from collections.abc import Callable
import pandas as pd

from chunk_syllables_from_word import getSyllablesFrequencies, filterSyllablesFrequenciesByPercentageFrequency
from utilities.files import writeCSV


def getSyllablesFrequenciesFromWords(words: list[str]) -> dict[str, int]:
    lengthsAndPercents = [(5, 30), (4, 15), (3, 50), (2, 50)]
    syllablesFrequencies = dict()

    for syllableLength, minPercentage in lengthsAndPercents:
        temp = getSyllablesFrequencies(words, syllableLength)
        temp = filterSyllablesFrequenciesByPercentageFrequency(temp, minPercentage)
        syllablesFrequencies |= temp

    return syllablesFrequencies

def main():
    words = readDataFrame('../data/lemmas_uniques_60.csv', lambda row: row['lemma'])

    syllablesFrequencies = getSyllablesFrequenciesFromWords(words)

    writeResult('../data/syllables.csv', syllablesFrequencies)
    printResult(syllablesFrequencies)


def readDataFrame(fileName: str, mapper: Callable):
    df = pd.read_csv(fileName)

    return [mapper(row) for index, row in df.iterrows()]


def writeResult(fileName: str, records: dict[str, int]):
    data = [('syllable', 'frequency')] + list(records.items())
    writeCSV(fileName, data)


def printResult(syllablesFrequencies: dict[str, int]):
    print(f'Syllables count is {len(syllablesFrequencies)}')


if __name__ == '__main__':
    main()
