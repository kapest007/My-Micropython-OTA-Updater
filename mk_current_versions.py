# mk_current_versions.py
# legt die Datei current_versions.json an.
# Diese Datei enthält ein Diktionary mit den
# Dateinamen : aktuelle Version

from m5stack import *
from m5ui import *
from uiflow import *
import json


versionen = {
            'ota.py' : 'v0.0.0',
            'Home_Markiese.py' : 'v0.0.0'
            }

print(versionen)

json_versionen = json.dumps(versionen)

print(json_versionen)

f = open('current_versions.json', 'w')
f.write(json_versionen)
f.close()