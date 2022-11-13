from tkinter import LEFT, X, BOTTOM
from widget.custom import Toplevel, isDark
from widget.widget import Image, ImageTk, getenv
from tkinter.ttk import Label, Button, Frame

systemroot = getenv("SYSTEMROOT") + "\\System32\\"

class ModuleMessagebox(Toplevel):
	def __init__(self, title, message, click, command = "", font = ("Consolas", 10, "normal"), icontype = "showinfo",resizeable = [False, False]):
		"Init Window"
		super().__init__()
		if icontype == "showinfo":
			self.icon = systemroot + "SecurityAndMaintenance.png"
		elif icontype == "showerror":
			self.icon = systemroot + "SecurityAndMaintenance_Error.png"
		elif icontype == "showwarning":
			self.icon = systemroot + "SecurityAndMaintenance_Alert.png"
		else:
			self.icon = icontype # icontype: type | path

		self.message = message
		self.click = click
		if not command:
			self.command = self.destroy
		self.font = font
		
		if isDark():
			self.change_title_bar(True)
		else:
			self.change_title_bar(False)
			
		self.setup(title, self.icon, resizeable)
		self.load_image()
		self.messagebox_setup()

	def load_image(self):
		self.load = Image.open(self.icon)
		self.load = self.load.resize((55, 55))
		self.image = ImageTk.PhotoImage(self.load)

	def messagebox_setup(self):
		_Picture = Label(self, image = self.image)
		_Picture.pack(side = LEFT, fill = X, padx = 25, pady = 25)
		_Message = Label(self, text = self.message, font = self.font)
		_Message.pack(side = LEFT, fill = X, padx = 10, pady = 10)

		Show = Frame(self)
		Click = Button(Show, text = self.click, command = self.command)
		Click.pack(side = BOTTOM, fill = X)
		Show.pack(side = BOTTOM, fill = X)
		self.mainloop()

def showinfo(title, message, font = ("Consolas", 10, "normal"), command = '', icon = "showinfo"):
	"Show Info"
	ModuleMessagebox(message = message, title = title, click = "OK", command = command, font = font, icontype = icon)

def showwarning(title, message, font = ("Consolas", 10, "normal"), command = '', icon = "showwarning"):
	"Show Warning"
	ModuleMessagebox(message = message, title = title, click = "OK", command = command, font = font, icontype = icon)

def showerror(title, message, font = ("Consolas", 10, "normal"), command = '', icon = "showerror"):
	"Show Error"
	ModuleMessagebox(message = message, title = title, click = "OK", command = command, font = font, icontype = icon)

if __name__ == "__main__":
	showinfo("ModuleMessagebox Test", "ModuleMessagebox Test.\n Showinfo, OK, \"Consolas 10 Normal\"")
