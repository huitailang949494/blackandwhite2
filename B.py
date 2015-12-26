from Tkinter import *
import Tkinter
import socket
import struct
import thread

BUF_SIZE = 1024 
server_addr = ('127.0.0.1', 8888)  
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

NameOfTheGame = "黑白棋"
BOARD_SIZE = 8
class board():
    PADDING = 2
    BORDER = 10
    LINE_THICKNESS = 1
    def __init__(self):
        self.root = Tk()
        self.root.title(NameOfTheGame)
        Label(self.root, text='Welcome! Play with ' + username).pack(pady=10)
        self.canvas = Tkinter.Canvas(self.root, height=600, width=600)
        self.canvas.pack()
        width = int(self.canvas["width"])
        height = int(self.canvas["height"])
        self.GRID_SIZE = ([width, height][width > height] - self.BORDER * 2) / (BOARD_SIZE)
        self._drawGround()
        def handler(event, self=self):
            return self.__onClick(event)
        self.canvas.bind('<Button-1>', handler)
        self.myTurn = True
        if (server_color == "white"):
            self.myTurn = True
        else:
            self.myTurn = False
        self.color = server_color

    def _drawGround(self):
        for i in range(0, BOARD_SIZE + 1):
            self.canvas.create_line(
                               self.BORDER,
                               self.BORDER + self.GRID_SIZE * i,
                               self.BORDER + self.GRID_SIZE * BOARD_SIZE,
                               self.BORDER + self.GRID_SIZE * i,
                               width=self.LINE_THICKNESS)
            self.canvas.create_line(
                               self.BORDER + self.GRID_SIZE * i,
                               self.BORDER,
                               self.BORDER + self.GRID_SIZE * i,
                               self.BORDER + self.GRID_SIZE * BOARD_SIZE,
                               width=self.LINE_THICKNESS)
        
    def __onClick(self, event):
        print "我是你上司"
        if self.myTurn:
            pos = self._getPosition(event.x, event.y)
            if self.color == "white":
                self.drawWhite(pos)
            else:
                self.drawBlack(pos)
            self.myTurn = False
            client.sendto(' '.join(map(str,pos)), server_addr)


        else:
            data, addr = client.recvfrom(BUF_SIZE)

            print data

            list = data.split(" ")

            pos = map(int, list)
            print pos
            print "have recived data"
            if (self.color == "black"):
                self.drawWhite(pos)
            else:
                self.drawBlack(pos)

            self.myTurn = True

    def __drawStone(self, position, color):
        xy = self._getCoordination(position)
        return self.canvas.create_oval(xy[0], xy[1], xy[0] + self.GRID_SIZE, xy[1] + self.GRID_SIZE, fill=color)
    
    def _getPosition(self, x, y):
        toGround = lambda x: (x - self.BORDER) / self.GRID_SIZE
        return (toGround(x), toGround(y))
    
    def _getCoordination(self, position):
        toAxis = lambda x: self.GRID_SIZE * x + self.BORDER
        return (toAxis(position[0]), toAxis(position[1]))
            
    def drawWhite(self, pos):
        self.__drawStone(pos, "white")
        
    def drawBlack(self, pos):
        self.__drawStone(pos, "black")
        
    def eventLoop(self):
        self.root.mainloop()


intputname = Tk()
intputname.title("Input Name")
intputname.geometry("300x150");

input_label = Label(intputname, text = "Name: ")
input_label.pack(pady = 10)

name_text = StringVar()
name = Entry(intputname, textvariable = name_text)
name_text.set("")
name.pack(pady = 10)


def on_click():
    client.sendto(name.get(), server_addr)
    intputname.destroy()

Button(intputname, text="Enter", command = on_click).pack(pady = 10)

intputname.mainloop()

data, addr = client.recvfrom(BUF_SIZE) 

list = eval(data)

print data

print list

setroom = Tk()
setroom.title("Set Room")
setroom.geometry("300x300")

room1_label = Label(setroom, text = "Room 1: ")
room1_label.pack(pady = 10)

room1_name = '      vs      ';

num = 0
for (uname, roomid) in list.items():
    if (roomid == "1" and num == 1):
        room1_name += uname
        num = num + 1
    elif (roomid == "1" and num == 0):
        room1_name = uname
        num = num + 1
        room1_name += " vs "
    print num
    print uname
    print room1_name

room1_user = Label(setroom, text = room1_name)
room1_user.pack(pady = 10)

def on_click1():
    client.sendto("1", server_addr)
    setroom.destroy()

Button(setroom, text="Enter", command = on_click1).pack(pady = 10)

room2_label = Label(setroom, text = "Room 2: ")
room2_label.pack(pady = 10)

room2_name = '      vs      ';

num = 0
for (uname, roomid) in list.items():
    if (roomid == "2" and num == 1):
        room2_name += uname
        num = num + 1
    if (roomid == "2" and num == 0):
        room2_name = uname
        num = num + 1
        room2_name += " vs "

room2_user = Label(setroom, text = room2_name)
room2_user.pack(pady = 10)

def on_click2():
    client.sendto("2", server_addr)
    setroom.destroy()

Button(setroom, text="Enter", command = on_click2).pack(pady = 10)

setroom.mainloop()

data, addr = client.recvfrom(BUF_SIZE) 
list = data.split(" ")

username = list[0]
server_color = list[1]

print username
print server_color

ui = board()
ui.eventLoop()

print "1111"









