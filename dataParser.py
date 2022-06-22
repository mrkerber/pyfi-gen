import json, random

file = open('scifiTerms.json')
scifiTerms = json.load(file)
file.close()

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



