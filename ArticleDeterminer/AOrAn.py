import json

with open('ArticleDeterminer/ipa-dict.json', encoding='utf-8') as file:
    ipa_dict = json.load(file)

phonetic_vowels = 'iɪeɛæaɑɔʌoʊuɚ'

def determineArticle(word):
    try:
        phonetic_spelling = ipa_dict[word.lower()]
        initial_sound = phonetic_spelling[0]
    except:
        print('lookup failed')
        first_letter = word[0]
        if first_letter in 'aeiou':
            return 'An'
        else:
            return 'A'

    if initial_sound in phonetic_vowels:
        return 'An'
    else:
        return 'A'