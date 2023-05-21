# mk_json.py
#
# Dieses Programm erzeugt eine Reihe von Jason-Files
# die in einem Projekt erforderlich sind.
#
# Die Daten werden in Listen mit Dictionaries geschrieben.
# Der Variablenname entspricht dem Filenamen.
# Es wird automatisch .jason angehängt.
# Alle diese Listen lommen in eine Liste, die dann iteriert wird.
#
filename = 'mk_json.py'
version = "v00.00.000"
date = "20.05.2023"
author = "Peter Stoeck"

###############################################
# imports
###############################################

from m5stack import *
from m5ui import *
from uiflow import *
import json

###############################################
# Daten aufbereiten
###############################################

'''
var_name = [
            {
                key: value,
                key: value
            }
           ]
'''

current_versions = [
            {
                'ota.py': 'v00.00.000',
                'Markiese.py': 'v00.00.000'
            }
           ]

jobs = [
            {
                'repo' : 'kapest007/My-Micropython-OTA-Updater',
                'file' : 'ota.py',
                'ziel' : 'boot.py'
            }, 
            {
                'repo' : 'kapest007/Markiese',
                'file' : 'Markiese.py',
                'ziel' : 'main.py'
            }
            
           ]

dev_config = [
            {
                "dev_typ": "M5ATOM Lite",
                "dev_name": "Markiese",
                "fixIP": "192.168.5.250"
            }
           ]

wlan_secrets = [
                {
                    'Kapest_Fritz': 'Milan987',
                    'Attraktor': 'blafablafa'
                }
            ]

###############################################
# Daten Liste aufbereiten
###############################################

jfile_liste =  {'current_versions': current_versions,
               'jobs': jobs,
               'dev_config': dev_config,
                'wlan_secrets': wlan_secrets
                }
              

for jfile in jfile_liste.items():
    f = open(jfile[0] +'.json', 'w')
    f.write(json.dumps(jfile[1]))
    f.close()
    
###############################################
# Index.htm und www/ anlegen
###############################################
indexdatei = '<h1>Index.htm von {}</br>IP: {}</h1>'.format(dev_config[0]["dev_name"], dev_config[0]["fixIP"])

try:
    os.mkdir('www')
except:
    pass

f = open('./www/index.htm', 'w')
f.write(indexdatei)
f.close()