#!/usr/bin/env python3
import socket, sys, time
import gbnclient, gbnserver

def main():
    ip = input("Provide Server IP:")
    port = int(input("Provide Port#:"))
    ipPortServer = (ip,port)
    ipPortClient = ('127.0.1.1',8080)
    addrFamily = socket.AF_INET
    sockType = socket.SOCK_DGRAM

    sock = socket.socket(addrFamily, sockType)

    if sock is None: #if socket(s) cannot be created, close program
        print("could not open socket")
        sys.exit(1)
    
    sock.bind(ipPortClient)

    command = input(">") #ask for request to be sent to server
    
    try:
        if command == "CLOSE": #if command is CLOSE, don't sent anything to server
            sys.exit(1)
        else:
            fileName = command.split()[1]
            encoded = str.encode(command) #encode command into bytes to send to server
            
            gbnserver.sendMsgTo(sock,ipPortServer,encoded) #send command to server


            gbnclient.recieveFileFrom(sock,fileName) #recieve file from server
            sys.exit(0)

        
    except socket.error: #if client cannot connect to server, exit program
        print("Error occurred and could not communicate with server")
        sys.exit(1)

if __name__ == '__main__':
    main()