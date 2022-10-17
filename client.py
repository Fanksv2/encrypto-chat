#! /usr/bin/env python

from email import message
from platform import processor
import socket
import sys
import time
import threading
import select
import traceback
from cryptography.hazmat.primitives.asymmetric import rsa
from message import Message, MessageType

from message_processor import MessageProcessor

HOST = "localhost"         
PORT = 5535

private_key = rsa.generate_private_key(65537, 2048)
public_key = private_key.public_key()

class Server(threading.Thread):
    def __init__(self, processor):
        threading.Thread.__init__(self)

        self.receive = processor.socket
        self.processor = processor

    def run(self):
        lis=[]
        lis.append(self.receive)
        while 1:
            read,_,_=select.select(lis,[],[])
            for item in read:
                try:
                    s = item.recv(2048)
                    if s!='':
                        message = Message(raw=s.decode())
                        valid = message.unmount()
                        if(valid == True):
                            self.processor.process(message)

                except ConnectionResetError:
                    print("Server Closed")
                    exit()

class Client(threading.Thread):    
    def connect(self,host,port):
        self.sock.connect((host,port))

    def client(self,host,port,msg):               
        sent = self.sock.send(msg)           
        #print "Sent\n"

    def run(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        try:
            name=input("Nickname: ")
        except EOFError:
            print ("Error")
            return 1

        print ("Connecting\n")
        self.connect(HOST,PORT)

        print ("Connected\n")
        receive=self.sock

        message_processor = MessageProcessor(receive)
        srv = Server(message_processor)
        srv.daemon=True
    
        print ("Starting service")
        srv.start()
        while 1:            
            #print "Waiting for message\n"
            msg=input('>>')
            if msg=='exit':
                break
            if msg=='':
                continue
            
            content = (name + ": " + msg)
            message_processor.send_simple_message(content)
        return(1)
        
if __name__=='__main__':
    print ("Starting client")
    cli=Client()    
    cli.start()

# comment for test code in web