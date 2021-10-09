from tkinter import *
from PIL import Image, ImageTk
from tkinter_custom_button import TkinterCustomButton
import game
from game import *

class Home(Tk):
	def __init__(self):
		Tk.__init__(self)

		img_load = ImageTk.PhotoImage(Image.open("img/titre.png"))
		img = Label(self, image=img_load)
		img.image = img_load
		img.pack(side=TOP,pady=60)

		img_load = ImageTk.PhotoImage(Image.open("img/bar.png"))
		img = Label(self, image=img_load, borderwidth=0, highlightthickness=0)
		img.image = img_load
		img.pack(side=TOP)

		play = TkinterCustomButton(text ="PLAY",corner_radius=10, hover=True, bg_color ='#C2C7EA', fg_color = '#EBC066', hover_color = '#DDAF4D', width = 150, height = 48, command=lambda: [self.onClick_Play()])
		play.pack(side=TOP, pady=90)


		self.bind(play, lambda: onClick_Play(self))

	def onClick_Play(self):
		Home.destroy(self)
		game.main()

	



if __name__ == "__main__":
	app = Home()
	app.title("TIC TAC TOE")
	app.geometry('450x500')
	app.configure(bg='#C2C7EA')
	app.resizable(width=False,height=False)
	app.mainloop()