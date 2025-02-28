from utilities.files import readLines, writeCSV
from words_extraction_from_text import getWordsFrequenciesFromLines


def main():
    lines = readLines('../data/text')

    wordsFrequencies = getWordsFrequenciesFromLines(lines)

    writeResult(list(wordsFrequencies.items()))
    printResult(wordsFrequencies)


def writeResult(records: list[tuple[str, int]]):
    data = [('word', 'frequency')] + records
    writeCSV('../data/words', data)


def printResult(wordsFrequencies: dict[str, int]):
    print(f'Unique words are {len(wordsFrequencies)}')
    print(f'Total words are {sum(wordsFrequencies.values())}')


if __name__ == '__main__':
    main()
