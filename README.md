# Micropython OTA Updater für M5Stack Micropython
Dieser OTA-Updater wurde an das M5Stack Micropython angepasst. 
Ursprünglich wollte ich den OTA-Updater von Ronald Dehuysser 
(https://github.com/rdehuyss/micropython-ota-updater) einsetzen, 
musste dann aber feststellen, das die httpclient.py nicht mit dem 
Micropython auf den M5Stack Geräten funktioniert. Deshalb habe ich auf dieser 
Vorlage ein neues Script geschrieben, dass auf den M5Stack Geräten läuft.

Meine Version ist etwas einfacher als die von Ronald Dehuysser. 
Das Script liegt in **boot.py** und wird somit bei jedem Neustart aufgerufen.
Es prüft ob es bei Github eine neuere Version gibt. Wenn das der Fall ist 
wird diese heruntergeladen und als **main.py** gespeichert.

## Folgende zusätzliche Dateien werden benötigt:
**wlansecrets.py**  -  Enthält die Zugangsdaten für das WLAN </br>
**current_version.py**  - enthält die aktuelle Version (String gemäß Github Tag) </br>

# Dieses Projekt ist noch in der Entwicklung! 
## Entwicklungsstand:
Zum jetzigen Zeitpunkt prüft das Script ob es bei Github eine neue Version gibt und lädt diese nach main.py.
Es aktualisiert die Versionsnummer aber noch nicht und funktioniert nur mit dem Repository kapest007/HOME_Markiese.
