# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: Python [conda env:base] *
#     language: python
#     name: conda-base-py
# ---

from faker import Faker
from textwrap import wrap
from itertools import chain
from functools import reduce
from collections import defaultdict

# ---

fake = Faker()

word = fake.word()


# + active=""
# print(word)
# -

# ---

def flatten(listOfLists: list[list]) -> list:
    return list(chain.from_iterable(listOfLists))


def calculatePercentageOfNumber(percent: int, whole: int) -> int:
    return round((percent / 100) * whole)


# ---

# ## Divide word into syllables for search

# ### Spin word

# #### One spin

def spinWord(word: str) -> str:
    firstLetter = word[0]
    rest = word[1:]
    return ''.join([rest, firstLetter])


# + active=""
# print(word, spinWord(word), spinWord(spinWord(spinWord(spinWord(spinWord(spinWord(word)))))))
# -

# #### Spin around

def spinWordAround(word: str) -> list[str]:
    originalWord = word
    spunList = [originalWord]
    spun = spinWord(word)

    while originalWord != spun:
        spunList.append(spun)
        spun = spinWord(spun)

    return spunList


# + active=""
# print(spinWordAround(word))
# -

# ### Chunk

# #### syllables

def getSyllables(word: str, syllableLength: int) -> list[str]:
    syllables = wrap(word, syllableLength)
    return list(filter(lambda syllable: len(syllable) == syllableLength, syllables))


# + active=""
# print(getSyllables(word, 2))
# -

def getPossibleSyllables(wordSpins, syllableLength):
    for word in wordSpins:
        yield from sorted(getSyllables(word, syllableLength))


# + active=""
# print(list(getPossibleSyllables(spinWordAround('hello'), 3)))
# -

def filterSyllablesByWord(syllables: list[str], word: str) -> list[str]:
    existed = list(filter(lambda syllable: syllable in word, syllables))
    unique = reduce(lambda acc, i: acc + [i] if i not in acc else acc, existed, [])
    return unique


# ### Divide word by Spining and Chunking

def divideIntoSyllables(word: str, syllableLength) -> list[str]:
    wordSpins = spinWordAround(word)
    syllables = getPossibleSyllables(wordSpins, syllableLength)
    unique = filterSyllablesByWord(syllables, word)

    return unique


# + active=""
# print(divideIntoSyllables(word, 5))
# -

# ### Frequencies

# #### Count syllables

def countSyllables(words: list[str], syllableLength: int) -> dict[str, int]:
    syllablesFrequencies = defaultdict(int)
    
    for word in words:
        for syllable in divideIntoSyllables(word, syllableLength):
                syllablesFrequencies[syllable] += 1

    return syllablesFrequencies


# + active=""
# print(countSyllables(fake.words(), 3))
# -

# #### Merge and sort

def getSyllablesFrequencies(words: list[str], syllableLength: int = 2) -> dict[str, int]:
    syllablesFrequencies = countSyllables(words, syllableLength)
    sortedAlphabetically = sorted(syllablesFrequencies)
    sortedByFrequency = sorted(sortedAlphabetically, key=syllablesFrequencies.get, reverse=True)
    syllablesFrequencies = [(syllable, syllablesFrequencies[syllable]) for syllable in sortedByFrequency]
    
    return dict(syllablesFrequencies)


# + active=""
# print(getSyllablesFrequencies(fake.words()))
# -

# #### Filter by percentage

def filterSyllablesFrequenciesByPercentageFrequency(wordsWithFrequencies: dict[str, int], minFrequencyPercentage: int = 0) -> dict[str, int]:
    maxValue = max(wordsWithFrequencies.values())
    minFrequency = calculatePercentageOfNumber(minFrequencyPercentage, maxValue)
    filteredWordsWithFrequencies = filter(lambda wordFrequency: wordFrequency[1] > minFrequency, wordsWithFrequencies.items())
    
    return dict(filteredWordsWithFrequencies)

# + active=""
# print(list(filterSyllablesFrequenciesByPercentageFrequency(getSyllablesFrequencies(fake.words()), 50)))
