#!/usr/bin/env python3
import socket, sys, os, time
import gbnclient, gbnserver

def main():
    port = int(input("Listen at port #"))

    ipPortServer = ("127.0.0.1",port)
    ipPortClient = ("127.0.1.1",8080)
    addrFamily = socket.AF_INET
    sockType = socket.SOCK_DGRAM

    sock = socket.socket(addrFamily, sockType)

    if sock is None:# or sendSock is None: #if socket cannot be created, close program
        print("could not open socket")
        sys.exit(1)


    print(f'Listening on: {ipPortServer[0]}:{ipPortServer[1]}')

    while True:

        sock.bind(ipPortServer)#bind socket to IP address and port provided
        msg,addr = gbnclient.recieveMsgFrom(sock) #wait for message
        decoded = msg.decode()
        print(f'Msg recieved from {addr}: {msg}')
        fileName = decoded.split()[1]

        addr = ipPortClient

        print(f'sending {fileName} to {addr}')
        
        gbnserver.sendFileTo(sock,addr,fileName) #send file to address that requested it

        break

if __name__ == '__main__':
    main()