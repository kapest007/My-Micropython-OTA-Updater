# Micropython OTA Updater für M5Stack Micropython
Dieser OTA-Updater wurde an das M5Stack Micropython angepasst. 
Ursprünglich wollte ich den OTA-Updater von Ronald Dehuysser 
(https://github.com/rdehuyss/micropython-ota-updater) einsetzen, 
musste dann aber feststellen, das die httpclient.py nicht mit dem 
Micropython auf den M5Stack Geräten funktioniert. Deshalb habe ich auf dieser 
Vorlage ein neues Script geschrieben, dass auf den M5Stack Geräten läuft.

~~Meine Version ist etwas einfacher als die von Ronald Dehuysser. 
Das Script liegt in **boot.py** und wird somit bei jedem Neustart aufgerufen.
Es prüft ob es bei Github eine neuere Version gibt. Wenn das der Fall ist 
wird diese heruntergeladen und als **main.py** gespeichert.~~

# Dieses Projekt ist noch in der Entwicklung! 

## Entwicklungsstand:
Das Script prüft für alle in **job.json** enthaltenen Dateien ob bei Github neue Versionen vorhanden sind. Ist das der Fall, so werden die vorhandenen damit ersetzt. Am Ende werden die hierfür erforderlichen Objekte gelöscht und eine Garbage Collection durchgeführt. Dadurch werden ca. **20kB Speicher** freigegeben.

Die Wlanverbindung gleibt erhalten. Die **IP-Adresse** befindet sich in **wlan.ifconfig[0]**.

# Installation:
Die Dateien<br>
**ota.py<br>
mk_current_versions.py<br>
mk_dev_config.py<br>
mk_job_file.py<br>
wlansecrets.py**<br>
ins Verzeichnis **/flash** des M5-Gerätes kopieren.<br>
In den **mk_... Dateien** die entsprechenden Einträge vornehmen und die Dateien einmal ausführen.

Die Datei **ota.py** in **boot.py** umbenennen.

Wenn jetzt neu gestartet wird, wird zuerst **boot.py** abgearbeitet. Dabei wird die aktuelle Arbeitsdatei nach **main.py** geladen und anschließend ausgeführt.

Von jetzt an wird bei jedem Neustart geprüft, ob neue Versionen der Scripte in **boot.py** und **main.py** bei Github vorhanden sind. Wenn das der Fall ist werden sie automatich upgedatet.

Weitere Informatinen zu den **mk_... Dateien** im Wiki.
