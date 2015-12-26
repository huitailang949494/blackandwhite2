#coding=utf-8
import socket

BUF_SIZE = 1024 
server_addr = ('127.0.0.1', 8888)  
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
server.bind(server_addr) 


addr2name = {} 
name2addr = {}
name2room = {}
name2name = {}

while True :
    print "waitting for data"
    data, client_addr = server.recvfrom(BUF_SIZE) 
    print 'Connected by', client_addr, ' Receive Data : ', data

    if (addr2name.has_key(client_addr) == False):
    	addr2name[client_addr] = data
    	name2addr[data] = client_addr
        server.sendto(str(name2room), client_addr)
    elif (len(data) == 1):
    	username = addr2name[client_addr]
    	name2room[username] = data
    	for (uname, room) in  name2room.items():
    		if (uname != username and room == data):
    			addr1 = name2addr[uname]
    			addr2 = name2addr[username]
    			name2name[uname] = username
    			name2name[username] = uname
    			server.sendto(username + " white", addr1)
    			server.sendto(uname + " black", addr2)
    else:
        username = addr2name[client_addr]
        uname = name2name[username]
        addr = name2addr[uname]
        server.sendto(data, addr)

    print name2room

server.close()