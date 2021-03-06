from __future__ import print_function
from clipboard_functions import *
from time import sleep
from time import time
# import pyperclip #Not using pyperclip anymore

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import gspread


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
# CLIENT_SECRET_FILE = '/root/Downloads/client_id.json'
CLIENT_SECRET_FILE = input('Enter the location of the client_id.jason: ')
APPLICATION_NAME = 'UniClip_Python_Client'
CB_DATA_CELL = 'A1'
CB_DATA_TIMESTAMP_CELL = 'B1'
NEW_AUTH = False
DEFAULT_URL = 'https://docs.google.com/spreadsheets/d/1xB6whn__TJZ54bHUq7w9dr2O4NXXp9bi8cRkUFCQUzQ/edit#gid=0' #default sheet URL that every user will need to create one

# TODO making an alarm do the timing, much more efficient. Change the doc link
# 	   Also, change the program so that you don't need any user input after the first use.
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-uniclip-python.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
        # NEW_AUTH = True
    return credentials


class cbdata_plus_time(object):				
	"""New Class that holds clipboard data as well as the time it was created"""
	def __init__(self, cb_data , timestamp):
		super(cbdata_plus_time, self).__init__()
		self.cb_data = cb_data
		self.timestamp = timestamp 
	"""Overloaded some comparison operators, so its easy to compare which clipboard data is newer"""
	def __lt__(self, other):
		return self.timestamp < other.timestamp
	
	def __gt__(self, other):
		return self.timestamp > other.timestamp


credentials=get_credentials()	# First Google login, after this the credentials are stored in documents
gc = gspread.authorize(credentials)
sheet_url = input("Please enter the url of a google sheet:")	#dummy prompt, right now just press enter to go to my default sheet
sheet_url = 'https://docs.google.com/spreadsheets/d/1xB6whn__TJZ54bHUq7w9dr2O4NXXp9bi8cRkUFCQUzQ/edit#gid=0'
# sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1xB6whn__TJZ54bHUq7w9dr2O4NXXp9bi8cRkUFCQUzQ/edit#gid=0')
sh = gc.open_by_url(sheet_url)
worksheet = sh.sheet1

# sh = gc.create('UniClip_Python')
# sh.share('asan@bu.edu', perm_type='user', role='writer')
# if NEW_AUTH:
# 	worksheet.update_acell(CB_DATA_TIMESTAMP_CELL, "'"+str(time()))
# 	worksheet.update_acell(CB_DATA_CELL,"'"+local_get_clipboard())
# 	pass
# val = worksheet.acell('B1').value
worksheet.update_acell(CB_DATA_TIMESTAMP_CELL, "'"+str(time()))		# Set up remote clipboard Google sheet cells to be used as the the database 
worksheet.update_acell(CB_DATA_CELL,"'"+local_get_clipboard())		#
print(local_get_clipboard())	#Debugging outputs
print(time())					#
current_CB = cbdata_plus_time(local_get_clipboard(),time())

while True:		#Infinite loop 
	remote_cb_data = cbdata_plus_time(worksheet.acell(CB_DATA_CELL).value,float(worksheet.acell(CB_DATA_TIMESTAMP_CELL).value))
	if current_CB.cb_data != local_get_clipboard():
		current_CB = cbdata_plus_time(local_get_clipboard(),time())		
		pass
	# if current_CB.cb_data != local_get_clipboard():
	if current_CB.timestamp > remote_cb_data.timestamp:	#if remote clipboard is newer, update local clipboard
		# current_CB.timestamp=time()
		print ("Clipboard Changed Updating Remote Clipboard!")
		worksheet.update_acell(CB_DATA_TIMESTAMP_CELL, "'"+str(current_CB.timestamp))
		worksheet.update_acell(CB_DATA_CELL,"'"+current_CB.cb_data)
		current_CB=remote_cb_data

		pass
	if current_CB.timestamp < remote_cb_data.timestamp: # if local clipboard is newer, update remote clipboard
		current_CB=remote_cb_data
		pass
	# print()
	# if condition to compare timestamps
	# Update remote clipboard here
	# print('this string ->')
	# print(current_CB.cb_data)
	local_set_clipboard(str(current_CB.cb_data))
	# pyperclip.copy(current_CB.cb_data)
	# current_CB = cbdata_plus_time(local_get_clipboard(),time())
	# print (current_CB.cb_data)
	# passn owner for CLIPBO
	sleep(10)			#Checks if the any of the clipboards have changed every 10 seconds. I should do this with a SIGALARM instead of using this
	pass
pass


# print(val)
