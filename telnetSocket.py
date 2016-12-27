# Echo server program
import socket
import threading
import datetime
import time

class telnetSocket():
    """
    Establish a socket connection usable through telnet to monitor a process
    by relaying messages from the process.   when the user makes a telnet (or other)
    socket connection, the class will relay the message to the client.
    Follow Instructions to get started.  
    """
    ###open a connection with telnet
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    
    estConnection  = True ##run the thread loop to establish a socket connection
    keepConnection = True ##keep thread loop alive with current connection
    upLink         = False ##true if connection established through telnet

    fmtString      ="%Y-%m-%d %H:%M:%S.%f" #datestring format
    message        = "Going well" ##message we want send to telnet

    def __init__(self, msg="Going well" ):
        self.message=msg
        
    
    def estConn(self):
        """
        method to establish the socket connection and receive data from telnet
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.HOST, self.PORT))
        s.listen(1)
        self.socket=s   ##establish a socket to connect to 

        ##come back up here to restablish connection
        while self.estConnection:
            print 'waiting for connection'
            conn, addr = s.accept()
            self.conn=conn
            self.addr=addr
            print 'Connected by', addr
            self.upLink=True
            while self.keepConnection:  ##keep connection open
                data = conn.recv(1024)  ##this will block the conn
                if not data:
                    print 'connection closed'
                    self.upLink=False
                    break
                else:
                    self.data=data  ##data received from telnet if any
                print data
            #conn.sendall(data)   #return data string for old sytle testing
            conn.close()
        s.close()
        
    def startSocketThread(self):
        """
        run socket through a thread in order to allow parallel operation
        """
        self.t1 = threading.Thread(target=self.estConn,args=())

    def relayMessages(self,*msg):
        """
        relay the messages to the socket if a connection is made
        """
        if len(msg)>0:
            self.message=msg
        myTime=datetime.datetime.now()
        mus=myTime.microsecond/1000.00
        timeString=datetime.datetime.strftime(myTime,self.fmtString)
        if self.upLink:
            self.conn.send("[%s] %s \n"%(timeString,self.message))
        else:
            pass #do nothing. do not send the message to the socket




if __name__=='__main__':
    import telnetSocket
    m1= telnetSocket.telnetSocket()
    m1.startSocketThread()
    m1.t1.start()
    ##now nc localhost 50007
    ##or telnet localhost 50007
    m1.relayMessages()  ##will relay messages to telnet as long as connected
    m1.conn.send("hi")  ##send message to socket even if not connected

    ##after close
    m1.keepConnection=False
    m1.estConnection =False
    m1.t1.join()
