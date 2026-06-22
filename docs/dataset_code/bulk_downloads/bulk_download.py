'''
Abacus bulk downloader
'''
import os
import time
import pathlib

import requests

#Add the identifiers of the studies you wish to download
PIDS = ['hdl:11272.1/xxx/xxxxxx']
URL = 'https://abacus.library.ubc.ca'
#You should include a user agent of some kind
#the os.environ will read the value of KEY; you can use whatever you want or
#just put your API in the script, which I would not recommend

#https://www.whatismybrowser.com/detect/what-is-my-user-agent/
HEADER = {'User-agent': 'INSERT USER AGENT',
          'X-Dataverse-key' : os.environ['HE']}


#Note: Abacus and other dataverse repositories may have cybersecurity
#features which may present a page which requires further authentication
#If things are not proceeding as they should, examine the contents
#of info.text to see if other action is required.

for pid in PIDS:
    info = requests.get(f'{URL}/api/datasets/:persistentId',
                headers=HEADER,
						params={'persistentId':pid}, timeout=100)
    files = [{'label': _['dataFile']['filename'], 'fid':_['dataFile']['id']}
             for _ in info.json()['data']['latestVersion']['files']]
    for file in files:
        time.sleep(2) # UBC has anti DDOS measures
        download = requests.get(f'{URL}/api/access/datafile/{file["fid"]}',
                            headers=HEADER, timeout=100)
        dest = pid.replace(':','_').replace('/','_')
        os.makedirs(dest, exist_ok=True)
        with open(pathlib.Path(dest,file['label']), 'wb') as f:
            f.write(download.content)
