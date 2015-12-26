#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from socket import *
from time import ctime
import string
HOST = '127.0.0.1'
PORT = 21567
BUFSIZE = 1024

ADDR = (HOST,PORT)

udpSerSock = socket(AF_INET, SOCK_DGRAM)
udpSerSock.bind(ADDR)


##初始化部分
room_cnt = [0,0,0,0,0,0,0,0,0,0]
add0 =[0,0,0,0,0,0,0,0,0,0]
add1 =[0,0,0,0,0,0,0,0,0,0]
maparray = [[[None for z in range(10)] for i in range(8)] for j in range(8)]
##


while True:
	print 'wating for message...'
	data, addr = udpSerSock.recvfrom(BUFSIZE)
	#udpSerSock.sendto('[%s] %s'%(ctime(),data),addr)
	print '...received from and retuned to:',addr
	str1 = data.split(' ')
	if str1[0]=='Require':
		room_id = string.atoi(str1[1])
		print room_id
		if (room_cnt[room_id]==0):
			#print 0
			udpSerSock.sendto('0',addr)
			add0[room_id] = addr
			print addr
		elif(room_cnt[room_id]==1):
			#print 1
			udpSerSock.sendto('1',addr)
			add1[room_id] = addr
			print addr
		else:
			#print 2
			udpSerSock.sendto('2',addr)
		room_cnt[room_id] += 1
		print room_cnt[room_id]
	elif str1[0]=='Click':
		player_room_id = string.atoi(str1[1])
		player_type = string.atoi(str1[2])
		if (player_type<=1):
			data = str1[3] + ' ' + str1[4]
			x = string.atoi(str1[3])
			y = string.atoi(str1[4])
			udpSerSock.sendto(data,add0[player_room_id])
			udpSerSock.sendto(data,add1[player_room_id])
			if (player_type == 0):
				maparray[player_room_id][x][y] = 'w'
			else:
				maparray[player_room_id][x][y] = 'b'
		else:
			data=''
			for x in range(8):
				for y in range(8):
					data = data + maparray[player_room_id][x][y] + ' '
			print data
			udpSerSock.sendto(data,addr)

udpSerSock.close()