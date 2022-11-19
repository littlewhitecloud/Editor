from tkinter import *
from ctypes import windll, c_char_p
from ctkutils import Tk, Toplevel


class Window(Toplevel):
	def __init__(self, ):
		super().__init__()
		self.setup("TitleBar", "", "")
		self.overrideredirect(True)

		hwnd = windll.user32.FindWindowW(c_char_p(None), "Titlebar")
		GWL_STYLE = -16
		WS_BORDER = 0x800000
		WS_VISIBLE = 0x10000000
		WS_THICKFRAME = 0x40000
		WS_EX_COMPOSITED 
		windll.user32.SetWindowLongA(hwnd,GWL_STYLE,WS_VISIBLE + WS_THICKFRAME + WS_EX_APPWINDOW)
		self.bind("<ButtonPress-1>", self.dragging)
		self.bind("<ButtonRelease-1>", self.stopping)
		self.bind("<B1-Motion>", self.moving)

		
	def dragging(self, event):
		global x, y
		x = event.x
		y = event.y

	def stopping(self, event):
		x = None
		y = None

	def moving(self, event):
		global x, y
		deltax = event.x - x
		deltay = event.y - y
		self.geometry("+%s+%s" % (self.winfo_x() + deltax, self.winfo_y() + deltay))
		self.update()

a = Window()
a.mainloop()
