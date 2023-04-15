# Micropython Script Update Over The Air

# Basisierend auf MicroPython OTA Updater
# von Ronald Dehuysser
# https://github.com/rdehuyss/micropython-ota-updater

# Meine Version liegt in boot.py und wird somit bei jedem Neustart aktiv.
# Wenn eine neue Version des Main-Scriptes bei Github vorhanden ist
# wird diese heruntergeladen und als main.py gespeichert.

# Folgende zusätzliche Dateien werden benötigt:
# wlansecrets.py  -  Enthält die Zugangsdaten für das WLAN
# actver.py  - enthält die aktuelle Version (String gemäß Github Tag)

name = 'ota.py'
version = '00.00.005'
date = '12.04.2023'
author = 'Peter Stöck'

# Versionen:
# 00.00.005:
# Das neue File wird jetzt herunter geladen und in main.py gespeichert.
#
# 00.00.004:
# Die Versionsnummer der vorhandenen Version wird geholt.
#
# 00.00.003:
# Versionsnummerabfrage bei Github wurde in try: / except: gesetzt
#
# 00.00.002:
# Die aktuelle Version holen.
# mit der Github-Version vergleichen.
#
# 00.00.001:
# Das Abholen der Daten bei Github funktioniert.
# Das Isolieren der Versionsnummer als String funktioniert!

# Imports

from m5stack import *
from m5ui import *
from uiflow import *
import machine
import time
import network
from wlansecrets import SSID, PW
# import os, gc                      
# from httpclient import HttpClient   # ImportError: can't import name HttpClient 
import urequests   # aus UIFlow abgeguckt
import json


##########################################
# Wlan einrichten und verbinden:
##########################################

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(SSID, PW)

while not wlan.isconnected():
    time.sleep(1)
else:
    lcd.setRotation(3)
    print(wlan.ifconfig()[0])
    

##########################################
# Neueste Version bei Github abfragen:
# hier von kapest007/HOME_Markiese
##########################################

# Der Weg aus UIFlow:
# So funktioniert es: user-agent ist erforderlich!
try:
    req = urequests.request(method='GET', url='https://api.github.com/repos/kapest007/HOME_Markiese/releases/latest', headers={'Content-Type': 'text/html', 'User-Agent': 'kapest007'})
    gh_json = json.loads((req.text))  # Die Daten liegen als JSON vor.
    github_version = gh_json['tag_name']
    print(github_version)
except:
    print('Latest Version konnte nicht geholt werden!')




##################################################
# Aktuelle Version aus current_version.py holen:
##################################################

try:
    f = open('current_version.py','r')
    current_version = f.read()
    f.close()
    current_version = current_version.replace("\r\n", "")
    print(current_version)
except:
    print('Aktuelle Versionsnummer wurde nicht gefunden!')
    
    
if github_version > current_version:
    url = 'https://api.github.com/repos/kapest007/HOME_Markiese/contents'
    y = urequests.request(method='GET', url=url, headers={'Content-Type': 'text/html', 'User-Agent': 'kapest007'})
    y_json = json.loads(y.text)
    for x in y_json:
        if x['name'] == 'Home_Markiese.py':
            file_url = x['download_url']
            
            print(file_url)
            
    neues_file = y = urequests.request(method='GET', url=file_url, headers={'Content-Type': 'text/html', 'User-Agent': 'kapest007'})
    print(neues_file.text)
    
    f = open('main.py', 'w')
    f.write(neues_file.text)
    f.close()
    