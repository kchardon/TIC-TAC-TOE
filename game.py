from tkinter import *
from PIL import Image, ImageTk
from tkinter_custom_button import TkinterCustomButton


class Game(Tk):
	def __init__(self):
		Tk.__init__(self)
		img_load = ImageTk.PhotoImage(Image.open("grid.png"))
		img = Label(self, image=img_load, borderwidth=0, highlightthickness=0)
		img.image = img_load
		img.pack(side=BOTTOM, pady = 25)

		self.bind('<Button-1>', getxy)

def getxy(event):
	x = event.x
	y = event.y
	if y < 125:
		if x < 130:
			print(1)
		elif (x < 255):
			print(2)
		elif x > 265:
			print(3)
	elif y < 230:
		if x < 130:
			print(4)
		elif (x < 255):
			print(5)
		elif x > 265:
			print(6)
	elif y > 250:
		if x < 130:
			print(7)
		elif (x < 255):
			print(8)
		elif x > 265:
			print(9)





def main():
	app = Game()
	app.title("TIC TAC TOE")
	app.geometry('450x500')
	app.configure(bg='#C2C7EA')
	app.mainloop()