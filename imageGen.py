import sys
import os
sys.path.append(os.path.abspath('../pyfi-gen'))

import subprocess
from dataParser import *

id_gen = loadGenerator("data.pickle")

phrase = loadPhrase(id_gen.post_id)
img_name = str(id_gen.post_id) + '.jpeg'

# cmdHead = "cmd /c '"
# cmdBody = 'python ./VQGAN-CLIP/generate.py -p "' + phrase + '" -i 2 -o "'
# cmdEnd = img_name + """"'"""

# cmdArgs = ['./VQGAN-CLIP/generate.py', '-p', phrase, '-i', 2, '-o', img_name]

# os.chdir('VQGAN-CLIP')
# print(os.getcwd())

print(phrase)

# cmd = subprocess.run(['python', 'generate.py', '-p', phrase, '-i', '2', '-o', img_name])
# print(cmd.returncode)