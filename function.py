from os import getcwd
from tkinter import HORIZONTAL, RIGHT, LEFT, BOTTOM, Y, X, BOTH, \
						INSERT, \
						Menu
						
from tkinter.filedialog import asksaveasfilename, askopenfilename
from messagebox import showinfo, showerror, showwarning

from widget.widget import StatusBar, TextEditor, CrossTip, \
						Image, ImageTk, \
							Frame, Scrollbar, Sizegrip
from widget.custom import Tk, \
					isDark, isLight

class Editor(Tk):
	def __init__(self):
		"Init Window Self"
		super().__init__()
		self.__newfile__ = """#!/use/bin/env python
# -*- coding: utf-8 -*-
#
# Version : 1.0.1 --rebuild
# Filename : None
# Using : CodeNoteBook
# Autor Xiao_Bai_Yun
# | * Code Auto Create * |"""

		self.asset = "asset\\"
		self.path = "asset\\themes.tcl"
		
		self.encoding = "utf-8"
		self.background = "#0078D7"
		
		self.setups()
		self.mainloop()
		self.update()
	
	def setups(self):
		from windnd import hook_dropfiles
		from sys import argv
		self.setup("Editor", self.asset + "edit.ico", "975x525")
		
		hook_dropfiles(self, func = self.dragged_files)
		
		self.statusbar_setup()
		self.editor_setup()
		self.menu_setup()
		self.bind_setup()
		
		self.new_file()
		self.follow_system_theme()
		try:
			if len(argv) != 1:
				self.open_file(_file = argv[1])
		except:
			showerror("Open File", "File Can't be open")
		CrossTip(self, "showwarning", "The Project is still in preview.")
		#Window(background = "#53BF00")

	# IO
	def open_file(self, event = None,_file = None):
		"Open File"
		if _file == None:
			self.mode = True
		if self.mode:
			_file = askopenfilename(title = "Open File...", filetypes = [("Python Files", "*.py"),("Python Files (no console)", "*.pyw"),("All Files", "*")])
		
		# View File Menu
		self.viewfilemenu.add_command(label = _file)

		self.text.delete("0.0","end")
		self.handle = open(_file, "r", 1024, encoding = self.encoding)
		try:
			for line in self.handle.readlines():
				self.text.insert(INSERT,line)
				self.update()
		except:
			showerror("Read file", "Cannot open file : %s" % _file)
		self.title(_file)
		self.mode = False

	def save_file(self, event = None):
		"Save File"
		self.filepath = self.title()
		if self.filepath == "Editor":
			self.save_as_file()
		else:
			with open(self.filepath, 'w', encoding = self.encoding) as savefile:
				savefile.write(self.text.get("0.0", "end"))
				self.title(self.filepath)

	def save_as_file(self, event = None):
		"Save As File"
		self.filepath = asksaveasfilename(title = "Save as...", filetypes = [("Python Files", "*.py"),("Python Files (no console)", "*.pyw"),("All Files", "*")])
		with open(self.filepath, 'w', encoding = self.encoding) as savefile:
			savefile.write(self.text.get("0.0", "end"))
			self.title(self.filepath)

	def dragged_files(self, _file):
		"Format Dragged File"
		try:
			_file = "\n".join((item.decode("utf-8") for item in _file))
		except:
			_file = "\n".join((item.decode("gbk") for item in _file))
			
		self.open_file(_file = _file)
	
	# Func
	def new_file(self):
		"New File"
		self.text.delete("0.0", "end")
		self.text.insert(INSERT, self.__newfile__)

	# Menu Family
	def clear_menu(self):
		"Clear Menu"
		self.filemenu.delete(4, 6)
		self.viewfilemenu = Menu(self.menubar, tearoff = 0)
		self.filemenu.add_cascade(label = "View File", menu = self.viewfilemenu)
		self.viewfilemenu.add_command(label = "Clear", command = self.clear_menu)
		self.filemenu.add_separator()
		self.filemenu.add_command(label = "Quit", command = self.window_quit)

	# UI
	def editor_setup(self):
		"Editor setup"
		self.textframe = Frame(self)
		self.scrollbarx = Scrollbar(self.textframe,)
		self.scrollbary = Scrollbar(self.textframe, orient = HORIZONTAL)
		self.text = TextEditor(self.textframe, yscrollcommand = self.scrollbarx.set, xscrollcommand = self.scrollbary.set, wrap = "none", insertborderwidth = 0, relief = "flat", bg = self.bg, selectbackground = "grey", undo = True)

		self.scrollbarx.config(command = self.text.yview)
		self.scrollbary.config(command = self.text.xview)
		
		self.scrollbarx.pack(side = RIGHT, fill = Y)
		self.scrollbary.pack(side = BOTTOM, fill = X)
		self.text.pack(fill = BOTH, expand = True)
		self.textframe.pack(side = BOTTOM, fill = BOTH, expand = True)
		
	def statusbar_setup(self):
		statusframe = Frame(self)
		Sizegrip(statusframe).pack(side = RIGHT)
		statusbar = StatusBar(statusframe)

		statusbar.set_label("type", "None", side = LEFT)
		statusbar.set_label("Split","|", side = LEFT)
		statusbar.set_label("import","Imp:", side = LEFT)
		statusbar.set_label("class","Cls: ", side = LEFT)
		statusbar.set_label("func","Func: ", side = LEFT)
		
		statusbar.set_label("line", "Ln: ", side = RIGHT)
		statusbar.set_label("column", "Col: ", side = RIGHT)

		statusbar.pack(side = LEFT, expand = True, fill = X)
		statusframe.pack(side = BOTTOM, fill = X)

	def menu_setup(self):
		"Menu Setup"
		self.menubar = Menu(self)
		self.menubar.config(background='black')
		
		self.filemenu = Menu(self.menubar, tearoff = 0)
		self.viewfilemenu = Menu(self.menubar, tearoff = 0)
		
		self.filemenu.add_command(label = "New File", command = self.new_file)
		self.filemenu.add_command(label = "Open", command = self.open_file)
		self.filemenu.add_command(label = "Save", command = self.save_file)
		self.filemenu.add_command(label = "Save as", command = self.save_as_file)
		self.filemenu.add_cascade(label = "View File", menu = self.viewfilemenu)
		self.viewfilemenu.add_command(label = "Clear", command = self.clear_menu)
		self.filemenu.add_separator()
		self.filemenu.add_command(label = "Quit", command = self.window_quit)
		
		self.editmenu = Menu(self.menubar, tearoff = 0)
		self.editmenu_edit = Menu(self.editmenu, tearoff = 0)
		self.editmenu.add_command(label = "Refresh", command = self.refresh)
		self.editmenu_edit.add_command(label = "Undo", command = self.text.undo)
		self.editmenu_edit.add_command(label = "Redo", command = self.text.redo)
		self.editmenu_edit.add_command(label = "Cut", command = self.text.cut)
		self.editmenu_edit.add_command(label = "Copy", command = self.text.copy)
		self.editmenu_edit.add_command(label = "Paste", command = self.text.paste)
		self.editmenu.add_cascade(label = "Edit", menu = self.editmenu_edit)

		self.menubar.add_cascade(label = "File", menu = self.filemenu, underline = 0)
		self.menubar.add_cascade(label = "Edit", menu = self.editmenu, underline = 0)

		self.config(menu = self.menubar)

	def bind_setup(self):
		self.bind("<Control-KeyPress-s>", self.save_file)
		self.bind("<Control-Shift-KeyPress-S>", self.save_as_file)
		self.bind("<Control-KeyPress-o>", self.open_file)

if __name__ == "__main__":
	from sys import argv
	program = Editor()
	
	try:
		if len(argv) != 1:
			program.open_file(_file = argv[1])
	except:
		showerror("Open File", "File Can't be open")
	program.mainloop()
