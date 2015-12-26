#coding=utf-8
#Library import
from Tkinter import *
from math import *
from time import *
from random import *
from copy import deepcopy
from socket import *
import string
import var
#Variable setup
nodes = 0
depth = 4
moves = 0

#Tkinter setup
root = Tk()
screen = Canvas(root, width=500, height=600, background="#222",highlightthickness=0)
screen.pack()

class Board:
	def __init__(self):
		#White goes first (0 is white and player,1 is black and player2)
		self.player = 0
		self.passed = False
		self.won = False
		#Initializing an empty board
		self.array = []
		for x in range(8):
			self.array.append([])
			for y in range(8):
				self.array[x].append('o')

		#Initializing center values
		self.array[3][3]="w"
		self.array[3][4]="b"
		self.array[4][3]="b"
		self.array[4][4]="w"

		#Initializing old values
		self.oldarray = self.array
	#Updating the board to the screen

	def update(self):
		screen.delete("highlight")
		screen.delete("tile")
		for x in range(8):
			for y in range(8):
				#Could replace the circles with images later, if I want
				if self.oldarray[x][y]=="w":
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")

				elif self.oldarray[x][y]=="b":
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111")
		#Animation of new tiles
		screen.update()
		if var.player_type == 2:
			return
		for x in range(8):
			for y in range(8):
				#Could replace the circles with images later, if I want
				if self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]=="w":
					screen.delete("{0}-{1}".format(x,y))
					#42 is width of tile so 21 is half of that
					#Shrinking
					for i in range(21):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
						if i%3==0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")
					#Growing
					for i in reversed(range(21)):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
						if i%3==0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#aaa",outline="#aaa")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#fff",outline="#fff")
					screen.update()

				elif self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]=="b":
					screen.delete("{0}-{1}".format(x,y))
					#42 is width of tile so 21 is half of that
					#Shrinking
					for i in range(21):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
						if i%3==0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")
					#Growing
					for i in reversed(range(21)):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
						if i%3==0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")

					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#000",outline="#000")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#111",outline="#111")
					screen.update()
		
		#Drawing of highlight circles
		for x in range(8):
			for y in range(8):
				#if self.player == 0:
					if valid(self.array,self.player,x,y):
						screen.create_oval(68+50*x,68+50*y,32+50*(x+1),32+50*(y+1),tags="highlight",fill="#008000",outline="#008000")
		
		if not self.won:
			#Draw the scoreboard and update the screen
			self.drawScoreBoard()
			screen.update()
				#Player must pass?
			self.passTest()
			
			
		else:
			screen.create_text(250,550,anchor="c",font=("Consolas",15), text="The game is done!")
		
	#Moves to position
	def boardMove(self,x,y):
		global nodes
		#Move and update screen
		self.oldarray = self.array
		if self.player==0:
			self.oldarray[x][y]="w"
		else:
			self.oldarray[x][y]='b';
		self.array = move(self.array,x,y)
		var.realarray = self.array
		#Switch Player
		self.player = 1-self.player
		self.update()
		
		#Check if ai must pass
		self.passTest()
		self.update()
	def update_screen(self,newarr):
		self.oldarray = newarr
		self.update()

	#METHOD: Draws scoreboard to screen
	def drawScoreBoard(self):
		global moves
		#Deleting prior score elements
		screen.delete("score")

		#Scoring based on number of tiles
		player_score = 0
		computer_score = 0
		for x in range(8):
			for y in range(8):
				if self.array[x][y]=="w":
					player_score+=1
				elif self.array[x][y]=="b":
					computer_score+=1

		if self.player==0:
			player_colour = "green"
			computer_colour = "gray"
		else:
			player_colour = "gray"
			computer_colour = "green"

		screen.create_oval(5,540,25,560,fill=player_colour,outline=player_colour)
		screen.create_oval(380,540,400,560,fill=computer_colour,outline=computer_colour)

		#Pushing text to screen
		screen.create_text(30,550,anchor="w", tags="score",font=("Consolas", 50),fill="white",text=player_score)
		screen.create_text(400,550,anchor="w", tags="score",font=("Consolas", 50),fill="black",text=computer_score)

		moves = player_score+computer_score

	#METHOD: Test if player must pass: if they do, switch the player
	def passTest(self):
		mustPass = True
		for x in range(8):
			for y in range(8):
				if valid(self.array,self.player,x,y):
					mustPass=False
		if mustPass:
			self.player = 1-self.player
			if self.passed==True:
				self.won = True
			else:
				self.passed = True
			self.update()
		else:
			self.passed = False
#FUNCTION: Returns a board after making a move according to Othello rules
#Assumes the move is valid
def move(passedArray,x,y):
	#Must copy the passedArray so we don't alter the original
	array = deepcopy(passedArray)
	#Set colour and set the moved location to be that colour
	if board.player==0:
		colour = "w"
		
	else:
		colour="b"
	array[x][y]=colour
	
	#Determining the neighbours to the square
	neighbours = []
	for i in range(max(0,x-1),min(x+2,8)):
		for j in range(max(0,y-1),min(y+2,8)):
			if array[i][j]!='o':
				neighbours.append([i,j])
	
	#Which tiles to convert
	convert = []

	#For all the generated neighbours, determine if they form a line
	#If a line is formed, we will add it to the convert array
	for neighbour in neighbours:
		neighX = neighbour[0]
		neighY = neighbour[1]
		#Check if the neighbour is of a different colour - it must be to form a line
		if array[neighX][neighY]!=colour:
			#The path of each individual line
			path = []
			
			#Determining direction to move
			deltaX = neighX-x
			deltaY = neighY-y

			tempX = neighX
			tempY = neighY

			#While we are in the bounds of the board
			while 0<=tempX<=7 and 0<=tempY<=7:
				path.append([tempX,tempY])
				value = array[tempX][tempY]
				#If we reach a blank tile, we're done and there's no line
				if value=='o':
					break
				#If we reach a tile of the player's colour, a line is formed
				if value==colour:
					#Append all of our path nodes to the convert array
					for node in path:
						convert.append(node)
					break
				#Move the tile
				tempX+=deltaX
				tempY+=deltaY
				
	#Convert all the appropriate tiles
	for node in convert:
		array[node[0]][node[1]]=colour

	return array

#Method for drawing the gridlines
def drawGridBackground(outline=False):
	#If we want an outline on the board then draw one
	if outline:
		screen.create_rectangle(50,50,450,450,outline="#111")

	#Drawing the intermediate lines
	for i in range(7):
		lineShift = 50+50*(i+1)

		#Horizontal line
		screen.create_line(50,lineShift,450,lineShift,fill="#111")

		#Vertical line
		screen.create_line(lineShift,50,lineShift,450,fill="#111")

	screen.update()

#Simple heuristic. Compares number of each tile.
def dumbScore(array,player):
	score = 0
	#Set player and opponent colours
	if player==1:
		colour="b"
		opponent="w"
	else:
		colour = "w"
		opponent = "b"
	#+1 if it's player colour, -1 if it's opponent colour
	for x in range(8):
		for y in range(8):
			if array[x][y]==colour:
				score+=1
			elif array[x][y]==opponent:
				score-=1
	return score


#Checks if a move is valid for a given array.
def valid(array,player,x,y):
	#Sets player colour
	if player==0:
		colour="w"
	else:
		colour="b"
		
	#If there's already a piece there, it's an invalid move
	if array[x][y]!='o':
		return False

	else:
		#Generating the list of neighbours
		neighbour = False
		neighbours = []
		for i in range(max(0,x-1),min(x+2,8)):
			for j in range(max(0,y-1),min(y+2,8)):
				if array[i][j]!='o':
					neighbour=True
					neighbours.append([i,j])
		#If there's no neighbours, it's an invalid move
		if not neighbour:
			return False
		else:
			#Iterating through neighbours to determine if at least one line is formed
			valid = False
			for neighbour in neighbours:

				neighX = neighbour[0]
				neighY = neighbour[1]
				
				#If the neighbour colour is equal to your colour, it doesn't form a line
				#Go onto the next neighbour
				if array[neighX][neighY]==colour:
					continue
				else:
					#Determine the direction of the line
					deltaX = neighX-x
					deltaY = neighY-y
					tempX = neighX
					tempY = neighY

					while 0<=tempX<=7 and 0<=tempY<=7:
						#If an empty space, no line is formed
						if array[tempX][tempY]=='o':
							break
						#If it reaches a piece of the player's colour, it forms a line
						if array[tempX][tempY]==colour:
							valid=True
							break
						#Move the index according to the direction of the line
						tempX+=deltaX
						tempY+=deltaY
			return valid

#When the user clicks, if it's a valid move, make the move
def clickHandle(event):
	global depth
	xMouse = event.x
	yMouse = event.y
	print var.player_type
	if var.player_type == 2:
		
		if xMouse<=50 and yMouse<=50:
				#print 'hehe'
				data = 'Click'+' '+str(var.player_room_id) + ' ' + str(var.player_type)
				udpCliSock.sendto(data,ADDR)

				newarr = [['o'for i in range(8)] for j in range(8)]
				data,addr =udpCliSock.recvfrom(BUFSIZE)
				str1 = data.split()
				print str1
				i = 0
				for x in range(8):
					for y in range(8):
						newarr[x][y] = str1[i]
						i += 1

				board.update_screen(newarr)
		return

	if running:
		if xMouse>=450 and yMouse<=50:
			root.destroy()
		elif xMouse<=50 and yMouse<=50:
			#playGame()
			data,addr =udpCliSock.recvfrom(BUFSIZE)
			str1 = data.split()
			x = string.atoi(str1[0])
			y = string.atoi(str1[1])
			print x,y
			board.boardMove(x,y)
			var.player_turn = 0
		else:
			#Is it the player's turn?
			#if board.player==0:
				#Delete the highlights

				x = int((event.x-50)/50)
				y = int((event.y-50)/50)

				#Determine the grid index for where the mouse was clicked
				print var.player_turn
				#If the click is inside the bounds and the move is valid, move to that location
				if 0<=x<=7 and 0<=y<=7:
					if valid(board.array,board.player,x,y):
						if (var.player_turn==0):						
							var.player_turn= 1
							board.boardMove(x,y)
							data = 'Click'+' '+str(var.player_room_id) + ' ' + str(var.player_type) + ' ' + str(x)+ ' ' + str(y)
							for i in range(8):
								for j in range(8):
									data += ' ' + var.realarray[i][j]
							udpCliSock.sendto(data,ADDR)
							

def keyHandle(event):
	symbol = event.keysym
	if symbol.lower()=="r":
		playGame()
	elif symbol.lower()=="q":
		root.destroy()
	if running:
		data = 1
	elif symbol.lower()>='0' and symbol.lower()<='9':
		data = 'Require'+' '+symbol.lower()
		udpCliSock.sendto(data,ADDR)
		data,addr = udpCliSock.recvfrom(BUFSIZE)
		
		var.player_room_id = string.atoi(symbol.lower())
		var.player_type = string.atoi(data)
		print var.player_type
		playGame()

def create_buttons():
		#Restart button
		#Background/shadow
		screen.create_rectangle(0,5,50,55,fill="#000033", outline="#000033")
		screen.create_rectangle(0,0,50,50,fill="#000088", outline="#000088")

		#Arrow
		screen.create_arc(5,5,45,45,fill="#000088", width="2",style="arc",outline="white",extent=300)
		screen.create_polygon(33,38,36,45,40,39,fill="white",outline="white")

		#Quit button
		#Background/shadow
		screen.create_rectangle(450,5,500,55,fill="#330000", outline="#330000")
		screen.create_rectangle(450,0,500,50,fill="#880000", outline="#880000")
		#"X"
		screen.create_line(455,5,495,45,fill="white",width="3")
		screen.create_line(495,5,455,45,fill="white",width="3")
	
def runGame():
	global running
	running = False
	#begin game
	#Title and shadow
	#screen.destroy()
	screen.create_text(250,203,anchor="c",text="Othello",font=("Consolas", 50),fill="#aaa")
	screen.create_text(250,200,anchor="c",text="Othello",font=("Consolas", 50),fill="#fff")
	
	#Creating the difficulty buttons
	i=1
		#Background
	screen.create_rectangle(25+155*i, 310, 155+155*i, 355, fill="#000", outline="#000")
	screen.create_rectangle(25+155*i, 300, 155+155*i, 350, fill="#111", outline="#111")

	spacing = 130/(i+2)
	x=0.5
		#Star with double shadow
	screen.create_text(25+(x+1)*spacing+155*i,325,anchor="c",text="start", font=("Consolas", 25),fill="#b29600")
		#screen.create_text(25+(x+1)*spacing+155*i,327,anchor="c",text="\u2605", font=("Consolas",25),fill="#b29600")
		#screen.create_text(25+(x+1)*spacing+155*i,325,anchor="c",text="\u2605", font=("Consolas", 25),fill="#ffd700")

	screen.update()

def playGame():
	global board, running
	running = True
	screen.delete(ALL)
	create_buttons()
	board = 0

	#Draw the background
	drawGridBackground()

	#Create the board and update it
	board = Board()
	board.update()

HOST = 'localhost'
PORT = 21567
BUFSIZE = 1024

ADDR = (HOST, PORT)

udpCliSock = socket(AF_INET, SOCK_DGRAM)
runGame()

#Binding, setting
screen.bind("<Button-1>", clickHandle)
screen.bind("<Key>",keyHandle)
screen.focus_set()

#Run forever
root.wm_title("Othello")
root.mainloop()
udpCliSock.close()