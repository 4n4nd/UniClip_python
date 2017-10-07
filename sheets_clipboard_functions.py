import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('My Project-ae7f5a76cf6f.json', scope)
gc = gspread.authorize(credentials)
sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1AKKlZnKmSTS4rq6NuJcpYYZ-cdQcONGBxK0xMpOmagE/edit#gid=0')
val = sht2.acell('B1').value
print(val)