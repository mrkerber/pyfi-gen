import json, random, pickle

file = open('scifiTerms.json')
scifiTerms = json.load(file)
file.close()
# file = open('generatedPhrases.json')
# generatedPhrases = json.load(file)
# file.close()

descriptors = scifiTerms['descriptor']
subjects = scifiTerms['subject']
actions = scifiTerms['action']

def choosePath():
    choices = ['descriptor','subject','action']
    c1 = choices[random.randint(0,(len(choices)-1))]
    choices.remove(c1)
    c2 = choices[random.randint(0,(len(choices)-1))]
    choices.remove(c2)
    c3 = choices[0]
    return [c1,c2,c3]

def findDescriptor():
    return descriptors[random.randint(0,(len(descriptors)-1))]
def findSubject():
    return subjects[random.randint(0,(len(subjects)-1))]
def findAction():
    return actions[random.randint(0,(len(actions)-1))]

def saveGenerator(obj):
    with open("data.pickle", "wb") as data:
        pickle.dump(obj, data, protocol=pickle.HIGHEST_PROTOCOL)
def loadGenerator(file):
    with open(file, "rb") as data:
        return pickle.load(data)
class idGenerator():
    def __init__(self, phrase_id, post_id):
        self.phrase_id = phrase_id
        self.post_id = post_id
    def iteratePhrase(self):
        self.phrase_id += 1
    def iteratePost(self):
        self.post_id += 1

def savePhrase(phrase):
    phrases = []
    with open("generatedPhrases.json", "r+") as data:
        phrases = json.load(data)
    phrases.append(phrase)
    with open("generatedPhrases.json", "r+") as data:
        json.dump(phrases, data)

def loadPhrase(id):
    phrase = ''
    with open("generatedPhrases.json", "r+") as data:
        phrases = json.load(data)
        phrase = phrases[id]
    return phrase


### RECREATE GENERATOR ###
# newPickle = idGenerator(0,0)
# saveGenerator(newPickle)


# id_gen = loadGenerator("data.pickle")
# print(str(id_gen.phraseID) + " phrase0")
# print(id_gen.postID)
# id_gen.iteratePhrase()
# saveGenerator(id_gen)
# id_gen2 = loadGenerator("data.pickle")
# print(str(id_gen2.phraseID) + "phrase1")