import argparse
from dataParser import *
from twitterFunctions import *

parser = argparse.ArgumentParser(description='Generate or Post')
parser.add_argument('-r', '--run', action='store_true')
parser.add_argument('-p', '--post', action='store_true')
parser.add_argument('-n', '--next', action='store_true')
parser.add_argument('-i', '--iterate', action='store_true')
args = vars(parser.parse_args())

choice_path = choosePath()
descriptor_index = choice_path.index('descriptor')
subject_index = choice_path.index('subject')
action_index = choice_path.index('action')
id_gen = loadGenerator("data.pickle")

### MAIN FUNCTION ###
def buildPhrase():
    segments = []
    logic_failure = subject_index
    iteration = 1
    phrase_logical = False
    phrase = ''

    ### POPULATE SEGMENT ARRAY BASED ON CHOICE PATH ###
    for i in range(0,3):
        segments.append(findNewSegment(i))

    ### BUILD PHRASE BY REARRANGING SEGMENTS ###
    phrase = segments[descriptor_index]['segment'] + ' ' +  segments[subject_index]['segment'] + ' ' + segments[action_index]['segment']
    print('BEGIN: 1) ' + segments[0]['segment'] + ' 2) ' + segments[1]['segment'] + ' 3) ' + segments[2]['segment'])

    ### REPLACE SEGMENTS UNTIL PHRASE IS LOGICAL ###
    while not phrase_logical:
        phrase = segments[descriptor_index]['segment'] + ' ' +  segments[subject_index]['segment'] + ' ' + segments[action_index]['segment']
        phrase = phrase.capitalize()

        if logic_failure == descriptor_index:
            print('\nUPDATE: 1) ' + segments[0]['segment'] + (' 2) ' + segments[1]['segment']).upper() + ' 3) ' + segments[2]['segment'])
        elif logic_failure == action_index:
            print('\nUPDATE: 1) ' + segments[0]['segment'] + (' 2) ' + segments[1]['segment']) + ' 3) ' + segments[2]['segment'].upper())
        
        logic_failure = determinePhraseLogic(segments)
        
        if logic_failure != subject_index:
            segments[logic_failure] = findNewSegment(logic_failure)
            iteration += 1
        else:
            phrase_logical = True

    ### DETERMINE IF PHRASE IS SCIFI RELATED ###
    scifi_related = checkScifiRelated(segments)
    
    ### SAVE PHRASE OUTPUT ###
    saveOutput([segments[descriptor_index]['segment'],segments[subject_index]['segment'],segments[action_index]['segment']], scifi_related)
    print(f"\nGENERATED PHRASE: {phrase}")
    ### IF NOT SCIFI RELATED, RERUN ###
    # if not scifi_related:
    #     print(f"\nGENERATED PHRASE: {phrase}")
    #     print("Phrase is not sci-fi related. Rerolling.\n")
    #     buildPhrase()
    # else:
    #     print(f"\nGENERATED PHRASE: {phrase}")


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
    ### SETTING THE LOGIC FAILURE TO POINT AT THE SUBJECT INDICATES THERE IS NO FAILURE ###
    logic_failure = subject_index

    print(segments)

    ### COMPARE DESCRIPTOR AND SUBJECT ###
    compatibility_string = compareSegmentAttributes(segments[descriptor_index], segments[subject_index])
    if compatibility_string  == '':
        print('ERROR: Incompatible(Descriptor|Subject): "' + segments[descriptor_index]['segment'] + '" WITH "' + segments[subject_index]['segment'] + '"')
        logic_failure = descriptor_index
        return logic_failure
    else:
        print('Compatible(Descriptor|Subject): ' + compatibility_string)

    ### COMPARE SUBJECT AND ACTION ###
    compatibility_string = compareSegmentAttributes(segments[subject_index], segments[action_index])
    if compatibility_string  == '':
        print('ERROR: Incompatible(Subject|Action): "' + segments[subject_index]['segment'] + '" WITH "' + segments[action_index]['segment'] + '"')
        logic_failure = action_index
        return logic_failure
    else:
        print('Compatible(Subject|Action): ' + compatibility_string)
    
    # ### PSUEDO CODE FOR COMPARING DESCRIPTOR AND ACTION ###
    # compatibility_string = compareSegmentAttributes(segments[1], segments[2])
    # if compatibility_string  == '':
    #     print('ERROR: Incompatible(2-3): "' + segments[1]['segment'] + '" WITH "' + segments[2]['segment'] + '"')
    #     logic_failure = 2
    #     return logic_failure
    # else:
    #     print('Compatible(2-3): ' + compatibility_string)


    ### IF NO ISSUES RETURN THE INDEX OF THE SUBJECT ###
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
    savePhrase(phrase)
    if scifi_related:
        f = open('./data/generatedPhrases.txt', 'a')
        f.write(str(phrase) + '\n')
        f.close()
    else:
        f = open('./data/generatedPhrasesNonScifi.txt', 'a')
        f.write(str(phrase) + '\n')
        f.close()

if args['post']:
    phraseList = loadPhrase(id_gen.post_id)
    postTweet(phraseList[0] + ' ' + phraseList[1] + ' ' + phraseList[2], id_gen.post_id)
    print('Tweeting: ' + phraseList[0] + ' ' + phraseList[1] + ' ' + phraseList[2])
    id_gen.iteratePost()
elif args['next']:
    try:
        print(loadPhrase(id_gen.phrase_id))
        print(id_gen.phrase_id) 
    except:
        print(f'!ERROR: Phrase ID {id_gen.phrase_id} is out of bounds')
elif args['iterate']:
    id_gen.iteratePhrase()
    print('Phrase location updated')
elif args['run']:
    buildPhrase()
else:
    print('Please supply an argument\n-r: Run Program\n-p: Post Tweet\n-n: Print next post\n-i: iterate phrase ID')
    
### SAVE NEW ITERATOR VALUES ###
# print('phrase' + str(id_gen.phrase_id) + ' post' + str(id_gen.post_id))
saveGenerator(id_gen)

# python generate.py -p "Destructive knight breaks the fourth wall" -o "../pyfi-gen/img/5.png" -i 101 -se 20 -s 512 512