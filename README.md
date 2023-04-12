# Micropython OTA Updater
Hier entsteht ein Programm zum Update von Micropython Scripte über Wlan.
Basisierend auf dem MicroPython OTA Updater von Ronald Dehuysser
https://github.com/rdehuyss/micropython-ota-updater.

Meine Version liegt in **boot.py** und wird somit bei jedem Neustart aktiv.
Wenn eine neue Version des Main-Scriptes bei Github vorhanden ist
wird diese heruntergeladen und als **main.py** gespeichert.

## Folgende zusätzliche Dateien werden benötigt:
**wlansecrets.py**  -  Enthält die Zugangsdaten für das WLAN </br>
**current_version.py**  - enthält die aktuelle Version (String gemäß Github Tag) </br>

## Entwicklungsverlauf:
Ich entwickle das Programm für den Einsatz mit M5Stack-Geräten. Hier konkret mit einem M5Stick C Plus.
Offenbar hat das Micropython von 5Stack Probleme mit httpclient.py von Ronald Dehuysser. 
Deshalb versuche ich jetzt den Internetzugang mit den M5Stack spezifischen Möglichkeiten zu realisieren.
Die Version von latest von Github zu holen klappt jetzt.