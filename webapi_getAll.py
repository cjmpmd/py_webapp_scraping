
import requests, os, urllib3
from dotenv import load_dotenv
from webapi_getAll_caser import start as starti
load_dotenv()

mode = 2
headers = {'Content-Type': 'application/json'}
url = urllib3(os.getenv('API_SELECT'))  # Replace with your actual Laravel API URL
response = requests.get(url, headers=headers)
response = response.json()

print('Total cases: '+str(len(response)))
ttf = len(response)
tt = 1
for fid in response:
    print('------------------------------------------------------------------------------------')
    print('------------------------------------------------------------------------------------')
    print(' ## Case No.: '+str(tt)+'/'+str(ttf)+ ' ID: '+str(fid))
    print('------------------------------------------------------------------------------------')
    tt = tt + 1
    starti(mode,fid)
    print('')