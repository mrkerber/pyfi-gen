import argparse
from dataParser import *
from twitterFunctions import *

parser = argparse.ArgumentParser(description='Generate or Post')
parser.add_argument('-p', '--post', action='store_true')
args = vars(parser.parse_args())

choice_path = choosePath()
id_gen = loadGenerator("data.pickle")

### MAIN FUNCTION ###
def buildPhrase():
    segments = []
    logic_failure = 0
    iteration = 1
    phrase_logical = False
    phrase = ''

    ### POPULATE SEGMENT ARRAY BASED ON CHOICE PATH ###
    for i in range(0,3):
        segments.append(findNewSegment(i))

    ### BUILD PHRASE BY REARRANGING SEGMENTS ###
    phrase = segments[choice_path.index('descriptor')]['segment'] + ' ' +  segments[choice_path.index('subject')]['segment'] + ' ' + segments[choice_path.index('action')]['segment']
    print('BEGIN: 1) ' + segments[0]['segment'] + ' 2) ' + segments[1]['segment'] + ' 3) ' + segments[2]['segment'])

    ### REPLACE SEGMENTS UNTIL PHRASE IS LOGICAL ###
    while not phrase_logical:
        phrase = segments[choice_path.index('descriptor')]['segment'] + ' ' +  segments[choice_path.index('subject')]['segment'] + ' ' + segments[choice_path.index('action')]['segment']
        phrase = phrase.capitalize()

        if logic_failure == 1:
            print('\nUPDATE: 1) ' + segments[0]['segment'] + (' 2) ' + segments[1]['segment']).upper() + ' 3) ' + segments[2]['segment'])
        elif logic_failure == 2:
            print('\nUPDATE: 1) ' + segments[0]['segment'] + (' 2) ' + segments[1]['segment']) + ' 3) ' + segments[2]['segment'].upper())
        logic_failure = determinePhraseLogic(segments)
        if logic_failure > 0:
            segments[logic_failure] = findNewSegment(logic_failure)
            iteration += 1
        else:
            phrase_logical = True

    ### DETERMINE IF PHRASE IS SCIFI RELATED ###
    scifi_related = checkScifiRelated(segments)
    
    ### SAVE PHRASE OUTPUT, IF NOT SCIFI RELATED, RERUN
    saveOutput(phrase, scifi_related)
    if not scifi_related:
        buildPhrase()

### FETCH SEGMENT FROM DATA PARSER ###
def findNewSegment(index):
    segment = ''

    if choice_path[index] == 'descriptor':
        segment = findDescriptor()
    elif choice_path[index] == 'subject':
        segment = findSubject()
    else:
        segment = findAction()

    return segment
 
def determinePhraseLogic(segments):
    logic_failure = 0

    print(segments)

    ### COMPARE FIRST AND SECOND SEGMENT ###
    compatibility_string = compareSegmentAttributes(segments[0], segments[1])
    if compatibility_string  == '':
        print('ERROR: Incompatible(1-2): "' + segments[0]['segment'] + '" WITH "' + segments[1]['segment'] + '"')
        logic_failure = 1
        return logic_failure
    else:
        print('Compatible(1-2): ' + compatibility_string)

    ### COMPARE FIRST AND THIRD SEGMENT ###
    compatibility_string = compareSegmentAttributes(segments[0], segments[2])
    if compatibility_string  == '':
        print('ERROR: Incompatible(1-3): "' + segments[0]['segment'] + '" WITH "' + segments[2]['segment'] + '"')
        logic_failure = 2
        return logic_failure
    else:
        print('Compatible(1-3): ' + compatibility_string)
    
    ### COMPARE SECOND AND THIRD SEGMENT ###
    compatibility_string = compareSegmentAttributes(segments[1], segments[2])
    if compatibility_string  == '':
        print('ERROR: Incompatible(2-3): "' + segments[1]['segment'] + '" WITH "' + segments[2]['segment'] + '"')
        logic_failure = 2
        return logic_failure
    else:
        print('Compatible(2-3): ' + compatibility_string)

    ### IF NOT ISSUES RETURN 0 ###
    return logic_failure

def compareSegmentAttributes(seg_a, seg_b):
    compatibility_string = ''

    if seg_a['anthropomorphic'] == 'Y' and seg_b['anthropomorphic'] == 'Y':
        compatibility_string += 'anthropomorphic '
    if seg_a['emotionable'] == 'Y' and seg_b['emotionable'] == 'Y':
        compatibility_string += 'emotionable '
    if seg_a['technical'] == 'Y' and seg_b['technical'] == 'Y':
        compatibility_string += 'technical '
    if seg_a['locational'] == 'Y' and seg_b['locational'] == 'Y':
        compatibility_string += 'locational '

    return compatibility_string

def checkScifiRelated(segments):
    if (segments[0]['scifi-related'] == 'N' and segments[1]['scifi-related'] == 'N' and segments[2]['scifi-related'] == 'N'):
        return False
    else:
        return True

def saveOutput(phrase, scifi_related):
    if scifi_related:
        f = open('./data/generatedPhrases.txt', 'a')
        f.write(phrase + '\n')
        f.close()
        savePhrase(phrase)
    else:
        f = open('./data/generatedPhrasesNonScifi.txt', 'a')
        f.write(phrase + '\n')
        f.close()

if args['post']:
    postTweet(loadPhrase(id_gen.post_id), id_gen.post_id)
    print('tweeting: ' + loadPhrase(id_gen.post_id))
    id_gen.iteratePost()
else:
    buildPhrase()
    id_gen.iteratePhrase()
    
### SAVE NEW ITERATOR VALUES ###
# print('phrase' + str(id_gen.phrase_id) + ' post' + str(id_gen.post_id))
saveGenerator(id_gen)