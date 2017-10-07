import pyperclip	#Library for clipboard manipulation

def local_get_clipboard():
	return pyperclip.paste()
	
def local_set_clipboard(clipboard_data):
	pyperclip.copy(clipboard_data)

local_set_clipboard("My Name is Khan")
print (local_get_clipboard())