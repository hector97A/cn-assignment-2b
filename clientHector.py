#!/usr/bin/env python3
import socket, sys

def main():
    ip = input("Provide Server IP:")
    port = int(input("Provide Port#:"))
    ipPort = (ip,port) #ask for IP and port # and create tuple to later connect to server
    addrFamily = socket.AF_INET
    sockType = socket.SOCK_STREAM
    clientSock = socket.socket(addrFamily, sockType)

    if clientSock is None: #if socket cannot be created, close program
        print("could not open socket")
        sys.exit(1)
    
    try:
        clientSock.connect(ipPort)
        print("You are now connected! Enter your command now.")
            
        command = input() #ask for request to be sent to server
        if command == "CLOSE": #if command is CLOSE, don't sent anything to server
            sys.exit(1)
        else:
            fileName = command.split(' ')[1]
            clientSock.send(command.encode('utf-8')) #send reuqest to server encoded
            response = clientSock.recv(150).decode('utf-8').strip() #recieve response from server and remove whitespace
            print(response)
            
            if response == 'Invalid Request': #if request is bad, reponse will be invalid request instead of a file
                print("Invalid Request")
            elif response == 'File not found': #if request is good but file could not be found then File not found will be sent
                print("File not found")
            #if file found, get number of frames, create new file with name 
            elif 'File found' in response:
                framesToBeRecieved = int(response.split(":")[1].strip()) 
                #reponse is 'File found, total frames to be sent:{frames}', split by : and cast to int
                try:
                    fileToMake = open(fileName,'xb') #create new file only and open in byte mode

                    for i in range(framesToBeRecieved):
                        fileToMake.write(clientSock.recv(1000)) #for number of frames, 
                    fileToMake.close() #after writing all data to new file, close file
                    print(f'Recieved {fileName}')
                except FileExistsError: #if file already exists, tell user and exit program
                    print("File with that name already exists")
                    sys.exit(1)

    except socket.error: #if client cannot connect to server, exit program
        print("Error occurred and could not communicate with server")
        sys.exit(1)

if __name__ == '__main__':
    main()