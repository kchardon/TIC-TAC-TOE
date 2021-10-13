from tkinter import *
from PIL import Image, ImageTk
from tkinter_custom_button import TkinterCustomButton
import re

HUGE_NUMBER = 1000000

global best_play
global game

#The position to print the Xs and the Os to print them
pos = {1:(50,120), 2:(178,120), 3:(300,120), 4:(50,247), 5:(178,247), 6:(300,247), 7:(50,365), 8:(178,365), 9:(300,365)}

#The Game GUI
class Game(Tk):
	def __init__(self):
		Tk.__init__(self)

		# Initialization of the board
		self.img_load = ImageTk.PhotoImage(Image.open("img/grid.png"))
		self.img = Label(self, image=self.img_load, borderwidth=0, highlightthickness=0)
		self.img.image = self.img_load
		self.img.pack(side=BOTTOM, pady = 25)

		#Initilize a new state of the game
		global game
		game = State_Game("XOXXO?OX?",True)

		#On click, it plays
		self.bind('<Button-1>', lambda event, arg=self: onclickPlay(event,arg))

	def restartGame(self):
		global game
		self.clear_label_image()
		game = State_Game("?????????",True)
	
	def clear_label_image(self):
		for i in self.winfo_children():
			i.destroy()
		self.img = Label(self, image=self.img_load, borderwidth=0, highlightthickness=0)
		self.img.image = self.img_load
		self.img.pack(side=BOTTOM, pady = 25)


#Get the position of the mouse and return whether or not it's on a case of the board
def getxy(event,root,case):
	x = root.winfo_pointerx() - root.winfo_rootx()
	y = root.winfo_pointery() - root.winfo_rooty()
	if y > 105 and x > 30:
		if y < 227:
			if x < 155 :
				case = 1
			elif (x < 280 and x > 170):
				case = 2
			elif x > 295 and x < 420:
				case = 3
		elif y < 345 and y > 245:
			if x < 155 :
				case = 4
			elif (x < 280 and x > 170):
				case = 5
			elif x > 295 and x < 420:
				case = 6
		elif y > 358 and y < 475:
			if x < 155 :
				case = 7
			elif (x < 280 and x > 170):
				case = 8
			elif x > 295 and x < 420:
				case = 9
	return case

#Plays when the player clicks
def onclickPlay(event,root):
	#Get the clicked case
	global game
	case = None
	case = getxy(event,root,case)
	cross = ImageTk.PhotoImage(Image.open("img/cross.png"))
	circle = ImageTk.PhotoImage(Image.open("img/circle.png"))

	#if it's a clear case and the game is not finished, plays
	if case != None and list(game.state)[case-1] == "?" and not game.game_end():
		#It prints the cross in the selected case
		root.img_cross = Label(root, image=cross, borderwidth=0, highlightthickness=0)
		root.img_cross.image = cross
		root.img_cross.place(x=pos[case][0],y=pos[case][1])

		#Updating the game board
		t = list(game.state)
		t[case-1] = "X"
		game.state = "".join(t)

		game.crosses_turn = False

		#The AI plays only if the game isn't finished
		if not game.game_end():

			#Let the Os play
			new_game = play(game)
			new_case = 0

			#Searching for the play made by the AI
			for i in range(len(list(new_game.state))):
				if list(new_game.state)[i] != list(game.state)[i]:
					new_case = i + 1
					break

			#Printing the O where the AI played
			root.img_circle = Label(root, image=circle, borderwidth=0, highlightthickness=0)
			root.img_circle.image = circle
			root.img_circle.place(x=pos[new_case][0],y=pos[new_case][1])

			#Updating the game state
			game.state = new_game.state
	
	#If the game is finished and the result haven't already be printed, prints it
	if game.game_end() and game.end == 0:
		if game.won("X"):
			txt = Label(root,text="You Won!",bg='#C2C7EA',font=("Forte", 25),fg="#ffffff")
			txt.pack(side=TOP)
			txt2 = Label(root,text="Very Impressive :D",bg='#C2C7EA',font=("Forte", 25),fg="#ffffff")
			txt2.pack(side=TOP)
		elif game.won("O"):
			txt = Label(root,text="Sadly you lose ...",bg='#C2C7EA',font=("Forte", 25),fg="#ffffff")
			txt.pack(side=TOP)
		else:
			txt = Label(root,text="Not bad",bg='#C2C7EA',font=("Forte", 25),fg="#ffffff")
			txt.pack(side=TOP)
			

		replay = TkinterCustomButton(text ="REPLAY",corner_radius=10, hover=True, bg_color ='#C2C7EA', fg_color = '#EBC066', hover_color = '#DDAF4D', width = 150, height = 48, command=lambda: [root.restartGame()])
		replay.place(x=150,y=50)
		game.end = 1



#State of the current game
class State_Game():
	# Initialisation of the Game
	def __init__(self, state, crosses_turn):
		super().__init__()
		self.state = state
		self.crosses_turn = crosses_turn
		self.end = 0

	# Look if c has won
	def won(self, c):
		triples = [self.state[0:3], self.state[3:6], self.state[6:9], self.state[::3], self.state[1::3],
					self.state[2::3], self.state[0] + self.state[4] + self.state[8],
					self.state[2] + self.state[4] + self.state[6]]
		combo = 3 * c
		return combo in triples

	# Look if the game is finished
	def game_end(self):
		if self.won("O") or self.won("X"):
			return True
		for i in self.state:
			if i == "?":
				return False
		return True

	# Generate all the possible children of the current game state
	def generate_children(self):
		children = []
		for match in re.finditer('\?',self.state):
			i = match.start()
			state = list(self.state)
			if self.crosses_turn == True :
				state[i] = 'X'
			else:
				state[i] = 'O'
			children.append(State_Game("".join(state), not self.crosses_turn))
		return children

	# Returns the value of the current game
	def value(self):
		if self.won('X'):
			return 1
		if self.won('O'):
			return -1
		return 0

	# Returns the best move
	def get_best_play(self):
		global best_play
		return best_play


# Let the AI play and returns the new game state
def play(state):
	result = alpha_beta_value(state)
	best_play = state.get_best_play()
	return State_Game(best_play, state.crosses_turn)




# Alpha beta prunning algorithm

def alpha_beta_value(node):
	return min_value(node, -1, 1)

def max_value(node, alpha, beta):
    global best_play
    children = node.generate_children()
    if len(children) == 0 or node.game_end(): 
        return node.value()

    v = -HUGE_NUMBER

    for child in children:
        val = min_value(child, alpha, beta)
        if val > v:
            c = child
            v = val
        alpha = max(alpha, v)
        if alpha >= beta:
            best_play = c.state
            return v
    best_play = c.state
    return v


def min_value(node, alpha, beta):
    global best_play
    children = node.generate_children()
    if len(children) == 0 or node.game_end(): 
        return node.value()

    v = +HUGE_NUMBER

    for child in children:
        val = max_value(child, alpha, beta)
        if val < v:
            c = child
            v = val
        beta = min(beta, v)
        if alpha >= beta:
            best_play = c.state
            return v
    best_play = c.state
    return v






def main():
	app = Game()
	app.title("TIC TAC TOE")
	app.geometry('450x500')
	app.configure(bg='#C2C7EA')
	app.resizable(width=False,height=False)
	app.mainloop()