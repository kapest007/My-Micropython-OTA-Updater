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
version = '00.00.016'
date = '16.04.2023'
author = 'Peter Stöck'

# TODO:
# Versionsnummer aktualisieren.
# RTC stellen.
# log einführen - für remote Fehlermeldungen
# Abbruchbedingung für Wlan Anmeldung
# Aufräumen. OTA-Objekte entfernen.
# Verzeichnis Wechsel bei MP und Github.
# Globale Variablen aus den Funktionen entfernen.


# Versionen:
# 00.00.016:
# Die Parameterübergabe bei den Funktionen wurde überarbeitet.
# Globale Variablen wurden elemeniert.
# Konstante FEHLER eingeführt.
#
# 00.00.015:
# Die Versionen der Programme werden nun
# In current_versions.json in einem
# Diktionaty mit den aktuellen Versionsnummern
# gespeichert:
# Mit update_file_name aus jobs.json als Key.
#
# 00.00.014:
# neue_version_holen in neue_software_holen umbenannt.
#
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

FEHLER = '-1'

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

def github_version_holen(repo): 
    try:
        req = urequests.request(method='GET', url='https://api.github.com/repos/' + repo + '/releases/latest', headers={'Content-Type': 'text/html', 'User-Agent': 'kapest007'})
        gh_json = json.loads((req.text))  # Die Daten liegen als JSON vor.
        github_version = gh_json['tag_name']
        print(github_version)
        return github_version
    except:
        print('Latest Versionsnummer konnte nicht geholt werden!')
        return FEHLER

##################################################
# Aktuelle Version aus current_version.py holen:
##################################################

def lokale_version_holen(file_name):
    try:
        f = open('current_versions.json','r')
        current_versions = f.read()
        f.close()
        current_versions = json.loads(current_versions)
        current_version = current_versions[file_name]
        print(current_version)
        return current_version
    except:
        print('Aktuelle Versionsnummer wurde nicht gefunden!')
        return FEHLER

##################################################
# Wenn vorhanden neue Version holen:
##################################################

def neue_software_holen(gh_version, loc_version, repo, file_name, ziel_name):
    if gh_version > loc_version:
        url = 'https://api.github.com/repos/' + repo + '/contents'
        y = urequests.request(method='GET', url=url, headers={'Content-Type': 'text/html', 'User-Agent': 'kapest007'})
        y_json = json.loads(y.text)
        for x in y_json:
            if x['name'] == file_name :
                file_url = x['download_url']
                
                print(file_url)
                
        neues_file = urequests.request(method='GET', url=file_url, headers={'Content-Type': 'text/html', 'User-Agent': 'kapest007'})
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
    # Hier fehlt noch eine Reaktion !!

###########################
# Job Loop
###########################

for job in jobs:    
    
    github_version = github_version_holen(job['repo'])
    if github_version != FEHLER:
        lokale_version = lokale_version_holen(job['file'])
        if lokale_version != FEHLER:
            neue_software_holen(github_version, lokale_version, job['repo'], job['file'], job['ziel'])


