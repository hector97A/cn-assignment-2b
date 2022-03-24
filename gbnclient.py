import udt,packet
import sys
from threading import Thread
###########

ack = str.encode("ACK") ##endoded file that can be reused when sending ack messages

def recieveFileFrom(sock,filename):
    try:
        file = open(filename,'wb')
    except IOError:
        print("Could not open File")
        sys.exit(1)
    
    exp = 0
    while True:
        rawPkt, addr = udt.recv(sock) #recieve a packet from socket
        seq,contents = packet.extract(rawPkt) #extract sequence number and contents from raw packet

        if rawPkt == b'': #if we recieve end of file packet, assume that all packets have been recieved and stop recieving packets
            #print(rawPkt)
            #print(f'recieved empty packet')
            break
        
        #print(seq)
        if seq == exp:#if the packet recieved is the correct packet, make ack packet, 
                      #send, write new data to file, and increase expected packet to next.
            print(f'sending ack for pkt {seq}')
            newPkt = packet.make(exp,ack)
            udt.send(newPkt,sock,addr)
            exp += 1
            print(f'Next expected packet is {exp}')
            file.write(contents)
        else:# ack recieved but not for the packet that was expected, sending ack of previous in order packet
            print(f'out of order packet {seq} expected {exp}, sending {exp-1} as ack')
            newpkt = packet.make(exp-1,ack)
            udt.send(newpkt,sock,addr)
    print("Finished recieving file")
    file.close()

def recieveMsgFrom(sock):
    msg = b""
    #print(f'msg is currently:{msg}')
    exp = 0
    while True:
        rawPkt, addr = udt.recv(sock)
        if rawPkt == b'': #if we recieve end of file packet, assunme that all packets have been recieved and stop recieving packets
            break
        #extract packet contents to get sequence number and actual contents of packet
        seq,contents = packet.extract(rawPkt)
        
        if seq == exp:
            #if the packet re recieve is the next in order packet, send ack
            newPkt = packet.make(exp,ack)
            udt.send(newPkt,sock,addr)
            exp += 1
            msg = msg + contents
            print(f'msg is currently:{msg}')
            print(f'Correct packet recieved, sending ack with value {exp}')
            break
        else:
            newpkt = packet.make(exp-1,ack)
            udt.send(newpkt,sock,addr)
            print(f'Wrong packet recieved, Sending ack with value {exp}')
    print(f'msg is {msg}')
    return msg, addr

if __name__ == 'main':
    print("")