#!/usr/bin/env python3
import socket, sys, os

def main():
    port = int(input("Listen at port #"))

    addrPort = ("10.0.0.21",port)
    addrFamily = socket.AF_INET
    sockType = socket.SOCK_STREAM

    serverSock = socket.socket(addrFamily,sockType)

    if serverSock is None:
        print("could not open socket")
        sys.exit(1)

    serverSock.bind(addrPort) #bind socket to IP address and port # provided
    serverSock.listen(5)
    
    while True:
        print(f'Listening on: {addrPort[0]}:{addrPort[1]}')
        conn, addr = serverSock.accept() #accept connection from client

        print(f'Connection accepted from {addr}')
        
        request = conn.recv(1024).decode('utf-8').split(" ") #request should be in format RETR <file>
        if len(request) == 2 and request[0] == 'RETR':
            reqFile = request[1] #reqFile will be 
        else:
            print("Invalid Request")
            conn.send(("Invalid Request").encode('utf-8')) #if request from client is not valid, return Invalid Request

        print(f'Asking for file {request[1]}')

        try:
            reqFile = open(request[1],'rb') #open file in read and byte mode
            size = os.path.getsize(request[1]) #returns size of file in bytes to calculate frames needed
            frames = framesNeeded(size)

            conn.send((f'File found, total frames to be sent:{frames}').ljust(150).encode('utf-8')) #send number of frames to client
            print(f'Sending the file...')
            for i in range(frames):
                frame = reqFile.read(1000) #read 1000 bytes of data from file to then send to client
                conn.send(frame)
            print(f'Transfer Complete!')
            print(f'Connection closed, see you later!\n')
            
        except:
            print("File not found")
            conn.send(("File not found").encode('utf-8')) #if file cannot be found, return File not found to client

def framesNeeded(size):
    framesNeeded = 0

    if(size % 1000 != 0): #check if file is a multiple of thousand
        framesNeeded = (size//1000) + 1 #if file size is not multiple of thousand, return integer division result plus 1
    else:
        framesNeeded = size//1000

    return framesNeeded

if __name__ == '__main__':
    main()