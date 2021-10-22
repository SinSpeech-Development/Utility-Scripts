"""
Copyright SinSpeech (2021 October)
Department of Computer Science and Engineering,
University of Moratuwa

This Python script is used to generate a lexicon 
to be used in Kaldi recipes for Sinhala ASR.
"""

import os
import re

# Input and Output filenames
words_filename = 'words.txt'
transliteration_filename = 'phones.txt'
outFile = 'lexicon.txt'

# Constant phone symbols required for Kaldi
constant_symbols = ['<UNK> SPN\n', '<SIL> SIL\n']

# Unambiguous phones
two_char_phones = ('ae', 'ae:', 'ri', 'ri:', 'ai', 'au', 'ah',
                    'ng', 'cn', 'jn', 'nj', 'nd', 'nd^', 'mb')
twoCharOk = ['a:', 'ae', 'i:', 'u:', 'e:', 'ai', 'o:', 'au', 'c^', 'cn', 't^', 'd^', 's^']
threeCharOk = ['ae:']

# Ambiguous phones - True if should split
twoCharLook = ['ri', 'ru', 'ng', 'jn', 'nj', 'nd', 'mb'] # Not included ah
sinTwoCharLook = { 
    'ri':{'ඍ':False, 'රි':True}, 
    'ru':{'ෘ':False, 'රු':True}, 
    # 'ah':{'ඃ':False, 'අහ':True}, 
    'ng':{'ඟ':False, 'න්ග':True, 'ණ්ග':True, 'න්ඝ':True, 'ණ්ඝ':True}, 
    'jn':{'ඥ':False, 'ජ්න':True, 'ජ්ණ':True, 'ඣ්න':True, 'ඣ්ණ':True},
    'nj':{'ඦ':False, 'න්ජ':True, 'ණ්ජ':True, 'න්ඣ':True, 'ණ්ඣ':True},
    'nd':{'ඬ':False, 'න්ඩ':True, 'ණ්ඩ':True, 'න්ඪ':True, 'ණ්ඪ':True},
    'mb':{'ඹ':False, 'ම්බ':True, 'ම්භ':True} 
}

threeCharLook = ['ri:', 'ru:', 'nd^']
sinThreeCharLook = {
    'ri:':{'ඎ':False, 'රී':True}, 
    'ru:':{'ෲ':False, 'රූ':True},
    'nd^':{'ඳ':False, 'න්ද':True, 'ණ්ද':True, 'න්ධ':True, 'ණ්ධ':True}
}

'''
Read a file
'''
def read_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.readlines()
    return False

'''
Split the transliterated phone sequence,
if it contains only unambiguous phones
'''
def split_transliteration(transliteration):

    transliteration_cannot_split = any(element in transliteration for element in two_char_phones)

    if transliteration_cannot_split:
        return []
    else:
        char_list = list(transliteration)
        index = 0
        while(True and len(char_list) > 1 ):
            if char_list[index+1] == '^' or char_list[index+1] == ':':
                char_list[index : index+2] = [''.join(char_list[index : index+2])]
            index+=1
            if index == len(char_list) - 1 or index == len(char_list):
                break
        
        return char_list

'''
Check if a phone sequence contains ambiguous 3-char phones,
and returns whether or not it should be split
'''
def lookForThreeChar(i:int, phonetic:str):
    if (i+2) < len(phonetic):
        c = phonetic[i] + phonetic[i+1] + phonetic[i+2]
        if c in threeCharLook:
            return (True, c, i+3)
        elif c in threeCharOk:
            return (False, True, i+3)
    return (False, False, i)

'''
Check if a phone sequence contains ambiguous 2-char phones,
and returns whether or not it should be split
'''
def lookForTwoChar(i:int, phonetic:str):
    if (i+1) < len(phonetic):
        c = phonetic[i] + phonetic[i+1]
        if c in twoCharLook:
            return (True, c, i+2)
        elif c in twoCharOk:
            return (False, True, i+2)
    return (False, False, i+1)

'''
Check in 3-char and 2-char looks in order
'''
def checkInLooks(actual:str):
    looks, result = {}, []
    for t in sinThreeCharLook:
        for c in sinThreeCharLook[t]:
            for m in re.finditer(c, actual):
                looks[m.start()] = sinThreeCharLook[t][c]

    for t in sinTwoCharLook:
        for c in sinTwoCharLook[t]:
            for m in re.finditer(c, actual):
                looks[m.start()] = sinTwoCharLook[t][c]

    for i in sorted(looks):
        result.append(looks[i])
    return result

'''
Analyze a phone sequence - first 3-char ambiguous,
and then 2-char ambiguous, and derive the 
correctly split phone sequence
'''
def split_word(phonetic:str, actual:str):
    looks = checkInLooks(actual)
    counter = 0
    spaced = []
    ch = 0
    while ch < len(phonetic):
        t = lookForThreeChar(ch, phonetic)
        if t[0]:
            if looks[counter]:
                spaced += [t[1][0], t[1][1:]]
                ch = t[2]
            else:
                spaced.append(t[1])
                ch = t[2]
            counter += 1
        else:
            if t[1]:
                spaced.append(phonetic[ch:t[2]])
                ch = t[2]
            else:
                ch = t[2]
                t = lookForTwoChar(ch, phonetic)
                if t[0]:
                    if looks[counter]:
                        spaced += [t[1][0], t[1][1]]
                        ch =t[2]
                    else:
                        spaced.append(t[1])
                        ch = t[2]
                    counter += 1
                else:
                    spaced.append(phonetic[ch:t[2]])
                    ch = t[2]
    return ' '.join(spaced)

### RUNTIME APPLICATION ###

print("Reading input files...")
words_list = read_file(words_filename)

if words_list:
    transliteration_list = read_file(transliteration_filename)

    if transliteration_list:
        print("Processing Unambiguous splits...")
        complete_lexicon_list = []
        incomplete_lexicon_list = []
        for index in range(len(words_list)):
            word = words_list[index].strip()
            transliteration = transliteration_list[index].strip()
            splitted_transliteration = split_transliteration(transliteration)

            if len(splitted_transliteration) > 0:
                transliteration_result = ' '.join(splitted_transliteration)
                complete_lexicon_list.append(word + ' ' + transliteration_result + '\n')
            else:
                incomplete_lexicon_list.append(word + ' ' + transliteration)

        print("Processing Ambiguous splits...")
        incLex = [line.strip().split() for line in incomplete_lexicon_list]
        incSplitList = []
        for row in incLex:
            actual = row[0]
            phonetic = split_word(row[1], actual)
            incSplitList.append(actual + ' ' + phonetic + "\n")

        print("Combining Results...")
        writeList = constant_symbols + complete_lexicon_list + incSplitList

        print(f"Writing result to {outFile} ...")
        f = open(outFile, 'w', encoding='utf-8')
        f.writelines(writeList)
        f.close()

        print("Lexicon Generation Complete!")

    else:
        print(f"Cannot read {transliteration_filename} - Exitting!")
else:
        print(f"Cannot read {words_filename} - Exitting!")
