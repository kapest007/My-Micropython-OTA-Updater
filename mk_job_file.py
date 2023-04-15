# mk_job_file.py
#
#Erstellt das job.json File

from m5stack import *
from m5ui import *
from uiflow import *
# from json import *
import json

jobs = [
        { 'repo' : 'kapest007/My-Micropython-OTA-Updater',
          'file' : 'ota.py',
          'ziel' : 'boot.py'
        }, 
        { 'repo' : 'kapest007/HOME_Markiese',
          'file' : 'Home_Markiese.py',
          'ziel' : 'main.py'
        }
       ]

print(jobs)

json_jobs = json.dumps(jobs)

print(json_jobs)

f = open('job.json', 'w')
f.write(json_jobs)
f.close()