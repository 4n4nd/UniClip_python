from clipboard_functions import *
from time import sleep

def detect_change_update_CB():
	current_CB = local_get_clipboard()
	while True:
		if current_CB != local_get_clipboard():
			print ("Clipboard Changed Updating Remote Clipboard!")
			# Update remote clipboard here
			current_CB = local_get_clipboard()
			pass
		sleep(1)
		pass
	pass

detect_change_update_CB()