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
version = '00.00.027'
date = '17.04.2023'
author = 'Peter Stöck'

# TODO:
# RTC stellen.
# Aufräumen. OTA-Objekte entfernen.
# Für V2: Verzeichnis Wechsel bei MP und Github.



# Versionen:
# 00.00.027:
# Aufräumen implementiert.
#
# 00.00.026:
# sys.exit() zum Programmabruch bei relevanten Fehlern eingeführt.
# Bei elementarem Fehler wird das Programm beendet.
#
# 00.00.025:
# write_log() wurde um mode ergänzt.
# mode = 0 ermöglicht es ohne Timestamp
# einen Log-Eintrag zu erzeugen, wenn
# kein Wlan besteht.
#
# 00.00.024:
# time_out für Wlan Anmeldung.
# Wlan Anmeldung wurde hinter die Funktionsdefinitionen verschoben.
#
# 00.00.023:
# Zeitzone wurde korrigiert.
#
# 00.00.022:
# Log-Einträge wurden überarbeitet.
#
# 00.00.021:
# Der Versionsvergleich wird aus neue_software_holen() entfernt
# und im Hauptprogramm durchgeführt. So lassen sich die
# Log-Einträger besser erzeugen.
#
# 00.00.020:
# Bei erfolgreichen Operationen und Fehlern
# werden logeinträge geschrieben.
#
# 00.00.019:
# Log Eintragungen funktionieren.
#
# 00.00.018:
# NTP zeitstempel implementieren für LOG
# log.txt hinzugefügt.
#
# 00.00.017:
# versionsliste wird geführt!
#
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
import gc
print(gc.mem_free())
import machine
import time
import network
from wlansecrets import SSID, PW                      
import urequests   # aus UIFlow abgeguckt
import json
import ntptime
import sys

lcd.setRotation(3)

FEHLER = '-1'



###########################################
# Funktion zum erzeugen von Log-Einträgen.
# mode = 0 ohne Timestamp
# mode = 1 mit Timestamp
###########################################

def write_log(mode, text):
    try:
        f = open('log.txt', 'a')
        if mode:
            f.write(ntp.formatDatetime('-', ':') + ' - ' + text + '\n')
        else:
            f.write(text + '\n')
        f.close()
    except:
        print('kein Eintrag in logdatei möglich!')
    



##########################################
# Neueste Version bei Github abfragen.
##########################################

def github_version_holen(repo): 
    try:
        req = urequests.request(method='GET', url='https://api.github.com/repos/' + repo + '/releases/latest', headers={'Content-Type': 'text/html', 'User-Agent': 'kapest007'})
        gh_json = json.loads((req.text))  # Die Daten liegen als JSON vor.
        github_version = gh_json['tag_name']
        print(github_version)
        return github_version
    except:
        write_log(1, 'Latest Versionsnummer für ' + job['file'] + ' konnte nicht geholt werden!')
        print('Latest Versionsnummer konnte nicht geholt werden!')
        sauber_machen()
        sys.exit()
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
        write_log(1, 'Lokale Versionsnummer für ' + job['file'] + ' konnte nicht geholt werden!')
        print('Aktuelle Versionsnummer wurde nicht gefunden!')
        sauber_machen()
        sys.exit()
        return FEHLER

##################################################
# Neue Software holen:
##################################################

def software_holen(repo, file_name, ziel_name):
    url = 'https://api.github.com/repos/' + repo + '/contents'
    y = urequests.request(method='GET', url=url, headers={'Content-Type': 'text/html', 'User-Agent': 'kapest007'})
    y_json = json.loads(y.text)
    for x in y_json:
        if x['name'] == file_name :
            file_url = x['download_url']            
    neues_file = urequests.request(method='GET', url=file_url, headers={'Content-Type': 'text/html', 'User-Agent': 'kapest007'})    
    f = open(ziel_name, 'w')
    f.write(neues_file.text)
    f.close()


##########################################
# Wlan einrichten und verbinden:
##########################################

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(SSID, PW)
time_out = 10
while not wlan.isconnected():
    time.sleep(1)
    time_out -= 1
    if time_out == 0:
        write_log(0, 'Wlan nicht gefunden.')
        sauber_machen()
        sys.exit()


print(wlan.ifconfig()[0])
    
##########################################
# Mit NTP verbinden, um Zeitstempel
# für log-Eintragungen holen zu können.
##########################################

ntp = ntptime.client(host='de.pool.ntp.org', timezone=2)
# Es wird GMT angezeigt!!!

##########################################
# RTC starten
##########################################

# wird später implementiert.

###################################################
# Hauptschleife
###################################################

write_log(1, 'Update wird begonnen.')

#############################
# job.json laden
#############################

try:
    f = open('job.json', 'r')
    jobs = json.loads(f.read())
    f.close()
#     write_log('job.json wurde geladen.')
except:
    write_log(1, 'job.json konnte nicht geladen werden.')
    sauber_machen()
    sys.exit()
# Update abbrechen

    print('Job-File nicht gefunden')

############################
# Versionsliste holen
############################

try:
    f = open('current_versions.json', 'r')
    versionsliste = json.loads(f.read())
    f.close()
#     write_log('current_versions.json wurde geladen.')
except:
    write_log(1, 'current_versions.json konnte nicht geladen werden!')
    print('versionsliste konnte nicht geladen werden!')
    sauber_machen()
    sys.exit()

###########################
# Job Loop abarbeiten.
###########################

for job in jobs:        
    github_version = github_version_holen(job['repo'])
    lokale_version = lokale_version_holen(job['file'])
    if github_version > lokale_version:
        software_holen(job['repo'], job['file'], job['ziel'])
        versionsliste[job['file']] = github_version
        write_log(1, job['file'] + ' wurde von ' + lokale_version + ' auf ' + github_version + ' aktualisiert.')
    else:
        write_log(1, job['file'] + ' ist noch aktuell.')

try:
    f = open('current_versions.json', 'w')
    f.write(json.dumps(versionsliste))
    f.close()
#     write_log('aktualisierte current_versions.json wurde gespeichert.')
except:
    write_log(1, 'current_versions.json konnte nicht gespeichert werden!')
    print('current_versions.json konnte nicht gespeichert werden!')
   

write_log(1, 'Updateprozess beendet.')

##################################
# Alle Objekte die nicht mehr
# gebraucht werden entfernen.
##################################

objekts = [machine, time, network, SSID, PW, urequests, json, write_log, github_version_holen,
           lokale_version_holen, software_holen, jobs, json.loads]

def sauber_machen():
    for o in objekts:
        try:
            del(o)
        except:
            pass
   
  
print(gc.mem_free())
# Aufräumen
sauber_machen()
gc.collect()
print(gc.mem_free())
