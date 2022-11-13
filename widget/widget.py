from tkinter import *
from tkinter.ttk import Frame, Scrollbar, Sizegrip
from PIL import Image, ImageTk
from os import getcwd, getenv

# Statusbar Widget.
class StatusBar(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)
		self.labels = {}

	def set_label(self, name, text = "", side= "right", width=0):
		if name not in self.labels:
			label = Label(self, borderwidth=0, anchor="w")
			label.pack(side=side, pady=0, padx=4)
			self.labels[name] = label
		else:
			label = self.labels[name]
		if width != 0:
			label.config(width=width)
		label.config(text=text)

# TextEditor Widget.
class TextEditor(Text):
	def __init__(self, master, **kw):
		Text.__init__(self, master, **kw)
		from idlelib.percolator import Percolator
		from idlelib.colorizer import ColorDelegator, color_config
		
		self.config(tabs=("1c", "2c"))
		self.configure(font=("Cascadia Code", 9, "normal"))
		
		color_config(self)
		Percolator = Percolator(self)
		ColorDelegator = ColorDelegator()
		Percolator.insertfilter(ColorDelegator)

		self.bind("<Control-C>", self.copy)
		self.bind("<Control-V>", self.paste)
		self.bind("<Control-X>", self.cut)
		self.bind("<Control-Z>", self.undo)
		self.bind("<Control-Y>", self.redo)

	# Ctrl Family
	def copy(self):
		"Ctrl-C"
		try:
			self.text.clipboard_clear()
			self.text.clipboard_append(self.text.selection_get())
		except:
			pass

	def cut(self):
		"Ctrl-X"
		self.copy()
		try:
			self.text.delete(SEL_FIRST, SEL_LAST)
		except:
			pass

	def paste(self):
		"Ctrl-V"
		try:
			self.text.insert(SEL_FIRST, self.text.clipboard_get())
			self.text.delete(SEL_FIRST, SEL_LAST)
			return
		except:
			pass
		self.text.insert(INSERT, self.text.clipboard_get())

	def undo(self):
		"Ctrl-Z"
		try:
			self.text.clipboard_clear()
			self.text.clipboard_append(self.text.selection_get())
		except:
			pass

	def redo(self):
		"Ctrl-Y"
		self.text["undo"] = True
		try:
			self.text.edit_redo()
		except:
			pass

# CrossTip Widget.
class CrossTip(Frame):
	def __init__(self, master, type, msg,):
		Label.__init__(self, master)
		systemroot = getenv("SYSTEMROOT") + "\\System32\\"
		
		self.icon = self.image = None
		if type == "showerror":
			self.icon = systemroot + "SecurityAndMaintenance_Error.png"
		elif type == "showwarning":
			self.icon = systemroot + "SecurityAndMaintenance_Alert.png"
		else:
			self.icon = systemroot + "SecurityAndMaintenance.png"
		
		self.load_image()
		self.picture = Label(self, image = self.image)
		self.msg = Label(self, text = msg, height = 1)
		
		self.picture.pack(side = LEFT, fill = X, padx = 5)
		self.msg.pack(side = LEFT, fill = X,padx = 10)
		self.pack(side = TOP, fill = X)
	
	def load_image(self):
		self.load = Image.open(self.icon)
		self.load = self.load.resize((20, 20))
		self.image = ImageTk.PhotoImage(self.load)
