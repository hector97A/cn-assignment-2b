from ast import Continue
import timer,udt,packet
import socket
import sys
import time
import _thread
############

SIZE = 1020
WINDOW = 4

lock = _thread.allocate_lock()
base = 0
countDown = timer.Timer(.5)
notDone = True

def set_window(tPackets):
    global base
    return min(WINDOW, tPackets - base)

def sendFileTo(sock,ipPort,fileName):
    global lock
    global base
    global countDown
    global notDone

    try:
        file = open(fileName,'rb')
    except IOError:
        print("Could not open file")
        sys.exit(1)

    packets = []
    seq = 0
    
    totalPacketsSent = 0
    timeouts = 0

    while True: #make packets from given file and store them in a list with an assigned sequence number
        frame = file.read(SIZE)
        if not frame:
            break
        packets.append(packet.make(seq,frame))
        seq += 1
    
    tPackets = len(packets)
    print(f'total of {tPackets} packets to be sent')
    window = set_window(tPackets)
    print(f'Window size of {window}')
    next = 0
    base = 0

    time.sleep(2)
    thread = _thread.start_new_thread(recieve,(sock,))
    #make new thread to begin recieving acks from client
    print(thread)
    #once ready to start transmitting, start timer
    start = time.time()

    while base < tPackets: #while there are still packets that need to be sent, send
        lock.acquire()
        print(f'base: {base}, tPackets:{tPackets}, {base < tPackets}')
        while next < base + window: #if there is enough space in window to send packets, send more
            print(f'sending packet {next} to {ipPort}')
            udt.send(packets[next],sock,ipPort)
            totalPacketsSent += 1
            #print(f'Total packets sent so far {totalPacketsSent}')
            next += 1
        
        #start timer
        if not countDown.running():
            countDown.start()

        while countDown.running() and not countDown.timeout():
            lock.release()
            time.sleep(.05)
            lock.acquire()

        #when a time out occurs
        if countDown.timeout():
            #if a timeout occurs, stop timer and set next packet to be sent back to start of window
            timeouts += 1
            #print(f'Total time outs so far {timeouts}')
            countDown.stop()
            next = base
        else:
            window = set_window(tPackets)
        lock.release()

    #once all packets are send, send empty file to signify EOF
    print("sending end of file packet")
    try:
        for i in range(15): ##send 15 EOF to ensure at least one gets to client 
            udt.send(packet.make_empty(),sock,ipPort)
    finally:
        #end of transmission, log stop time
        stop = time.time()

        print(f'Total time to transmit file with window size {WINDOW}:{stop-start} seconds')
        print(f'Total timeouts with window size {WINDOW}:{timeouts}')
        print(f'Total retransmissions with window size {WINDOW}:{totalPacketsSent-tPackets}')
        file.close()
        notDone = False
        return

def recieve(sock):
    global lock
    global base
    global countDown
    global notDone

    try:
        print(f'Ready to receive acks')
        while notDone:
            #print(f'value of {notDone}')
            rawPkt,addr = udt.recv(sock)
            ack, contents = packet.extract(rawPkt)

            if(ack >= base): #If a newer ack is recieved, advance base one spot
                print(f'acquired ack for packet {base} moving base')
                lock.acquire()
                base = ack + 1
                countDown.stop()
                print(f'new base: {base}')
                lock.release()
                
    finally:
        #print(f'value of notDone is now {notDone}')
        _thread.exit()

def sendMsgTo(sock,ipPort,msg):
    global countDown

    while True:
        pkt = packet.make(0,msg)
        udt.send(pkt,sock,ipPort)

        time.sleep(.1)
        sock.settimeout(.5) #set timeout
        try:
            rawPkt,addr = udt.recv(sock)
            ack, contents = packet.extract(rawPkt)

        except socket.timeout:
            print(f'No ACK, sending msg again')
            pass

        print(f'ACK: {rawPkt}')
        sock.settimeout(None) #remove timeout to return to blocking
        break


if __name__ == 'main':
    ##call send with socket bound to serverIP
    print("")
