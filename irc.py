import asyncore, socket
import events
import settings
import re

class Irc(asyncore.dispatcher):    
    def __init__(self, rxq, txq, host="localhost", port=6667, terminator="\n"):
        """
rxq = received messages queue
txq = transmit messages queue
        """
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        host = settings.SERVER if host == "localhost" else host
        port = settings.PORT if port == 6667 else port
        self.connect((host, port))
        self.terminator = terminator
        self.rxq = rxq
        self.txq = txq
        
        self.msg = ""
        
        if settings.DEBUG:
            asyncore.loop(timeout=0)
        else:
            try:
                asyncore.loop(timeout=0)
            except KeyboardInterrupt:
                self.send("QUIT :Forced exit.\n")
                self.close()
        
    def handle_connect(self):
        """
Create connect event
        """
        self.rxq.put(events.Connect())
        
    def handle_close(self):
        """
Create disconnect event.
        """
        self.rxq.put(events.Disconnect())
        
    def handle_read(self):
        """
Parse and create event.
        """
        data = self.msg + self.recv(1024)
        msgs = data.split(self.terminator)
        if not data.endswith(self.terminator):
            self.msg = msgs[-1]
            msgs = msgs[:-1]
        for msg in msgs:
            if settings.DEBUG:
                print "in: " + msg
            if msg:
                self.rxq.put(events.Unknown(raw=msg))
    
    def writable(self):
        """
Looks to see if something is in queue.
        """
        return not self.txq.empty()
    
    def handle_write(self):
        """
Gets items off queue.
        """
        while not self.txq.empty():
            msg_obj = self.txq.get_nowait()
            if settings.DEBUG:
                print "out: " + msg_obj.raw
            self.send("%s\n" % msg_obj.raw)


