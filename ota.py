# Micropython Script Update Over The Air

# Basierend auf MicroPython OTA Updater
# von Ronald Dehuysser
# https://github.com/rdehuyss/micropython-ota-updater

# Meine Version liegt in boot.py und wird somit bei jedem Neustart aktiv.
# Wenn eine neue Version des Main-Scriptes bei Github vorhanden ist
# wird diese heruntergeladen und als main.py gespeichert.

# Folgende zusätzliche Dateien werden benötigt:
# wlansecrets.py  -  Enthält die Zugangsdaten für das WLAN
# actver.py  - enthält die aktuelle Version (String gemäß Github Tag)

name = 'ota.py'
version = '00.00.038'
date = '18.04.2023'
author = 'Peter Stöck'

# TODO:
# Für V2:
#     Verzeichnis Wechsel bei MP und Github.
#     RTC stellen.



# Versionen:
# 00.00.038:
# Wenn log.txt nicht existiert
# wird sie von write_log() angelegt.
#
# 00.00.037:
# Die dev_config.json wird eingeführt.
# Diese Datei enthält ein Dictionary mit
# config Daten dieses Gerätes.
#
# 00.00.036:
# Es wurde eine feste IP-Adresse (192.168.5.32) eingerichtet.
#
# 00.00.035:
# Es wurde der Code entfernt, der nur zum Testen
# eingebaut wurde.
#
# 00.00.034:
# Aufräumen funktioniert. Gibt 21360 Bytes frei.
#
# 00.00.033:
# Fehlerbehandlung getestet und OK.
#
# 00.00.032:
# Variale abbruch eingeführt. Sorgt für Programmabbruch.
# Variable ntp_ok gibt an, ob NTP zur Verfügung steht.
# Damit erkennt write_log() selbst
# ob ein Datum geschrieben werden kann oder nicht.
#
# 00.00.031:
# Erster commit in Fehlerbehandlung.
#
# 00.00.030:
# Kleiner Versionssprung. Der Versuch das Programm aus
# verschiedenen Stellen bei essentiellen Fehlern mit sys.exit()
# zu verlassen funktionierte. Aber das Aufräumen funktioniert nur
# am Ende, weil alle Objekte die gelöscht werden sollen
# bekannt sein müssen. Dann kann aber nicht schon früher die
# Aufräufunktion ausgeführt werden.
# Deshalb wurde wieder auf diese Version zurückgesetzt mit:
# git reflog um die Nummer zu erhalten und
# git revert ae563be um zurück zu springen.
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
import machine
import time
import network
from wlansecrets import SSID, PW                     
import urequests   # aus UIFlow abgeguckt
import json
import ntptime

lcd.setRotation(3)

FEHLER = '-1'
abbruch = False
ntp_ok = False


###########################################
# Funktion zum erzeugen von Log-Einträgen.
# ntp_ok ersetzt mode.
###########################################

def write_log(text):
    try:
        f = open('log.txt', 'a')
        if ntp_ok == True:
            f.write(ntp.formatDatetime('-', ':') + ' - ' + text + '</br>\n')
        else:
            f.write(text + '\n')
        f.close()
    except:
        f = open('log.txt', 'w')
        if ntp_ok == True:
            f.write(ntp.formatDatetime('-', ':') + ' - ' + text + '\n')
        else:
            f.write(text + '\n')
        f.close()


##########################################
# Geräte Definitionen laden.
##########################################
  
try:
    f = open('dev_config.json','r')
    dc = f.read()
    f.close()
    dev_config = json.loads(dc)
except:
    write_log('dev_config.json konnte nicht geholt werden!')
    abbruch = True  

##########################################
# Neueste Version bei Github abfragen.
##########################################

def github_version_holen(repo):
    global abbruch
    try:
        req = urequests.request(method='GET', url='https://api.github.com/repos/' + repo + '/releases/latest', headers={'Content-Type': 'text/html', 'User-Agent': 'kapest007'})
        gh_json = json.loads((req.text))
        github_version = gh_json['tag_name']
        return github_version
    except:
        write_log('Latest Versionsnummer für ' + job['file'] + ' konnte nicht geholt werden!')
        abbruch = True
        return FEHLER

##################################################
# Aktuelle Version aus current_version.py holen:
##################################################

def lokale_version_holen(file_name):
    global abbruch
    try:
        f = open('current_versions.json','r')
        current_versions = f.read()
        f.close()
        current_versions = json.loads(current_versions)
        current_version = current_versions[0][file_name]
        return current_version
    except:
        write_log('Lokale Versionsnummer für ' + job['file'] + ' konnte nicht geholt werden!')
        abbruch = True
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

# wlan.ifconfig((dev_config[0]['fixIP'], '255.255.255.0', '192.168.5.1', '192.168.5.1'))
wlan.ifconfig(('192.168.5.250', '255.255.255.0', '192.168.5.1', '192.168.5.1'))

wlan.connect(SSID, PW)
time_out = 10
while not wlan.isconnected():
    time.sleep(1)
    time_out -= 1
    if time_out == 0:
        write_log('Wlan nicht gefunden.')
        abbruch = True
        break

write_log('IP: '+ wlan.ifconfig()[0])
    
##########################################
# Mit NTP verbinden, um Zeitstempel
# für log-Eintragungen holen zu können.
##########################################

try:
    ntp = ntptime.client(host='de.pool.ntp.org', timezone=2)
    ntp_ok = True
except:
    pass


##########################################
# RTC starten
##########################################

# wird später implementiert.

###################################################
# Hauptschleife
###################################################

write_log('Update wird begonnen.')

#############################
# job.json laden
#############################

try:
    f = open('jobs.json', 'r')
    jobs = json.loads(f.read())
    f.close()
except:
    write_log('jobs.json konnte nicht geladen werden.')
    abbruch = True

############################
# Versionsliste holen
############################

try:
    f = open('current_versions.json', 'r')
    versionsliste = json.loads(f.read())
    f.close()
#     write_log('current_versions.json wurde geladen.')
except:
    write_log('current_versions.json konnte nicht geladen werden!')
    abbruch = True

###########################
# Job Loop abarbeiten.
###########################

if abbruch == False:
    for job in jobs:
        if abbruch == False:
            github_version = github_version_holen(job['repo'])
            if github_version != FEHLER:
                lokale_version = lokale_version_holen(job['file'])
                if lokale_version != FEHLER:
                    if github_version > lokale_version:
                        software_holen(job['repo'], job['file'], job['ziel'])
                        versionsliste[job['file']] = github_version
                        write_log( job['file'] + ' wurde von ' + lokale_version + ' auf ' + github_version + ' aktualisiert.')
                    else:
                        write_log(job['file'] + ' ist noch aktuell.')
                else:
                    break
            else:
                break
        else:
            break

########################################
# Wenn alle Jobs erledigt sind
# die aktuellen Versionsnummern
# merken.
#########################################

if abbruch == False:
    try:
        f = open('current_versions.json', 'w')
        f.write(json.dumps(versionsliste))
        f.close()
    #     write_log('aktualisierte current_versions.json wurde gespeichert.')
    except:
        write_log('current_versions.json konnte nicht gespeichert werden!')
   
if abbruch == False:
    write_log('Updateprozess erfolgreich beendet.')
else:
    write_log('Updateprozess abgebrochen!')


