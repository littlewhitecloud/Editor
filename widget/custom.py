from os import getcwd, path, chdir
from tkinter import Tk, Toplevel
from winreg import HKEY_CURRENT_USER as hkey, QueryValueEx as getSubkeyValue, OpenKey as getKey
from asset.theme import use_dark_theme, use_light_theme, toggle_theme

# Cut from DarkDetect
def theme():
    valueMeaning = {0: "Dark", 1: "Light"}
    try:
        key = getKey(hkey, "Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize")
        subkey = getSubkeyValue(key, "AppsUseLightTheme")[0]
    except FileNotFoundError:
        return None
    return valueMeaning[subkey]

def isDark():
    if theme() is not None:
        return theme() == 'Dark'

def isLight():
	if theme is not None:
		return theme() == 'Light'

class Tk(Tk):
	def __init__(self):
		super().__init__()
		self.bg = "white"
	
	def follow_system_theme(self):
		if isDark():
			self.change_title_bar(True)
			use_dark_theme()
			bg = "black"
		else:
			self.change_title_bar(False)
			use_light_theme()
		
	def refresh(self):
		"Update Window"
		self.update()
		self.update()

	def setup(self, title, icon, geometry, resizeable = [True, True]):
		"A setup function for self"
		try:
			self.title(title)
			try:
				self.iconbitmap(icon)
			except:
				pass
			try:
				self.geometry(geometry)
			except:
				pass
			self.resizable(width = resizeable[0], height = resizeable[1])
		except:
			pass
	
	def change_title_bar(self, mode):
		from ctypes import windll, c_int, byref, sizeof
		self.update()
		DWMWA_USE_IMMERSIVE_DARK_MODE = 20
		set_window_attribute = windll.dwmapi.DwmSetWindowAttribute
		get_parent = windll.user32.GetParent
		hwnd = get_parent(self.winfo_id())
		rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
		if mode:
			value = 2
		else:
			value = 0
		value = c_int(value)
		set_window_attribute(hwnd, rendering_policy, byref(value), sizeof(value))
		self.update()
		self.update()

	def window_quit(self):
		"Quit Window"
		self.quit()
		exit(0)

class Toplevel(Toplevel):
	def __init__(self):
		super().__init__()
		
	def setup(self, title, icon, resizeable = [True, True]):
		"Setup Window Function"
		self.title(title)
		try:
			self.iconphoto(False, PhotoImage(file = icon))
		except:
			pass
		self.minsize(375, 150)
		self.resizable(width = resizeable[0], height = resizeable[1])
	
	def change_title_bar(self, mode):
		from ctypes import windll, c_int, byref, sizeof
		self.update()
		DWMWA_USE_IMMERSIVE_DARK_MODE = 20
		set_window_attribute = windll.dwmapi.DwmSetWindowAttribute
		get_parent = windll.user32.GetParent
		hwnd = get_parent(self.winfo_id())
		rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
		if mode:
			value = 2
		else:
			value = 0
		value = c_int(value)
		set_window_attribute(hwnd, rendering_policy, byref(value), sizeof(value))
		self.update()
		self.update()
