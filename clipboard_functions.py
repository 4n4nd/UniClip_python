import pyperclip	#Library for clipboard manipulation
import os

def local_get_clipboard():
	return pyperclip.paste()
	
def local_set_clipboard(clipboard_data):
	pyperclip.copy(clipboard_data)

# local_set_clipboard("My Name is Khan")
# print (local_get_clipboard())


# pyperclip.copy("hi")
# data = "myman"
# os.system("echo '%s' | pbcopy" % data)
# print (local_get_clipboard())