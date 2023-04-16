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
version = '00.00.014'
date = '15.04.2023'
author = 'Peter Stöck'

# TODO:
# Globale Variablen aus den Funktionen entfernen.
# Versionsnummer aktualisieren.
# RTC stellen.
# log einführen - für remote Fehlermeldungen
# Abbruchbedingung für Wlan Anmeldung
# Aufräumen. OTA-Objekte entfernen.
# Verzeichnis Wechsel bei MP und Github.


# Versionen:
# 00.00.014:
# neue_version_holen in neue_software_holen umbenannt.

# 00.00.013:
# Überflüssigen Code entfernt
#
# 00.00.012:
# job-file implementiert
#
# 00.00.011:
# Code aufgräumt
#
# 00.00.010:
# Neue Version holen als Funktion mit globalen Variablen implementiert.
#
# 00.00.009:
# Lokale Versionsnummer holen als Funktion mit globalen Variablen implementiert.
#
# 00.00.008:
# Versionsnummer von Github holen als Funktion mit globalen Variablen implementiert.
#
# 00.00.007:
# Settings zum bearbeiten von OTA und MAIN eingeführt.
#
# 00.00.006:
# Wichtige Daten in Variablen gepackt.
#
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

def github_version_holen():
    global github_repo, update_file_name, ziel_name, github_version    
    try:
        req = urequests.request(method='GET', url='https://api.github.com/repos/' + github_repo + '/releases/latest', headers={'Content-Type': 'text/html', 'User-Agent': 'kapest007'})
        gh_json = json.loads((req.text))  # Die Daten liegen als JSON vor.
        github_version = gh_json['tag_name']
        print(github_version)
    except:
        print('Latest Versionsnummer konnte nicht geholt werden!')

##################################################
# Aktuelle Version aus current_version.py holen:
##################################################

def lokale_version_holen():
    global github_repo, update_file_name, ziel_name, current_version
    try:
        f = open('current_version.py','r')
        current_version = f.read()
        f.close()
        current_version = current_version.replace("\r\n", "")
        print(current_version)
    except:
        print('Aktuelle Versionsnummer wurde nicht gefunden!')

##################################################
# Wenn vorhanden neue Version holen:
##################################################

def neue_software_holen():
    global github_repo, update_file_name, ziel_name, github_version, current_version
    if github_version > current_version:
        url = 'https://api.github.com/repos/' + github_repo + '/contents'
        y = urequests.request(method='GET', url=url, headers={'Content-Type': 'text/html', 'User-Agent': 'kapest007'})
        y_json = json.loads(y.text)
        for x in y_json:
            if x['name'] == update_file_name :
                file_url = x['download_url']
                
                print(file_url)
                
        neues_file = y = urequests.request(method='GET', url=file_url, headers={'Content-Type': 'text/html', 'User-Agent': 'kapest007'})
        print(neues_file.text)
        
        f = open(ziel_name, 'w')
        f.write(neues_file.text)
        f.close()

###################################################
# Hauptschleife
###################################################

#############################
# job.json laden
#############################

try:
    f = open('job.json', 'r')
    jobs = json.loads(f.read())
    f.close()
except:
    print('Job-File nicht gefunden')
    
for job in jobs:    
    github_repo = job['repo']
    update_file_name = job['file']
    ziel_name = job['ziel']
    github_version_holen()
    lokale_version_holen()
    neue_software_holen()


