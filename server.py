#! /usr/bin/env python

import socket
import sys, traceback
import threading
import select
import time

from message import Message, MessageType

SOCKET_LIST=[]
TO_BE_SENT=[]
SENT_BY={}
class Server(threading.Thread):
    def init(self):
        self.daemon = True
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.bind(('',5535))
        self.sock.listen(2)
        SOCKET_LIST.append(self.sock)
        print ("Server started on port 5535")

        handle = self.handle_connections()
        handle.daemon = True    
        handle.start()  

    def run(self):
        while 1:
            read,_,_=select.select(SOCKET_LIST,[],[],0)     
            for sock in read:
                if sock==self.sock:                    
                    sockfd,addr=self.sock.accept()
                    print (str(addr))
                    SOCKET_LIST.append(sockfd)
                    if(len(SOCKET_LIST) == 2):
                        # first to connect
                        sockfd.send(Message(content="a",type=MessageType.FIRST).mount().encode())
                    
                else:
                    try:
                        s=sock.recv(2048)
                        if s=='':
                            print (str(sock.getpeername()))                            
                            continue
                        else:
                            SENT_BY[s]=(str(sock.getpeername()))
                            TO_BE_SENT.append(s)
                    except:
                        print (str(sock.getpeername()))                    
                    
            
    class handle_connections(threading.Thread):
        def run(self):
            while 1:
                _,write,_=select.select([],SOCKET_LIST,[],0)
                for items in TO_BE_SENT:
                    for s in write:
                        try:
                            if(str(s.getpeername()) == SENT_BY[items]):
                                print("Ignoring %s"%(str(s.getpeername())))
                                continue
                            print ("Sending to %s"%(str(s.getpeername())))
                            s.send(items)                                             
                            
                        except:
                            traceback.print_exc(file=sys.stdout)
                    TO_BE_SENT.remove(items)   
                    del(SENT_BY[items])
                


if __name__=='__main__':
    srv=Server()
    srv.init()
    srv.start()
    while(True):
        time.sleep(1)
    
