import re
from datetime import datetime

TYPE_UNKNOWN = 1000
TYPE_CONNECTED = 1001
TYPE_DISCONNECTED = 1002

TYPE_PRIVMSG = 2001
TYPE_ACTION = 2002
TYPE_NOTICE = 2003

TYPE_JOIN=3001
TYPE_PART=3002
TYPE_QUIT=3003

TYPE_INFO=4001
TYPE_PING=4002
TYPE_PONG=4003
TYPE_USER=4004
TYPE_NICK=4005

TYPE_ADMIN=9000
TYPE_ADMIN_BROKER=9100
TYPE_ADMIN_BROKER_RELOAD=9101
TYPE_ADMIN_BROKER_FREE_MEMORY=9102
TYPE_ADMIN_BROKER_KILL_PROCESSES=9103

class BaseEvent(object):
    def __init__(self, **kwargs):
        self.created = datetime.now()
        self.type=TYPE_UNKNOWN
        self.command = kwargs.get('command', "")
        self.source = kwargs.get('source', "")
        self.target = kwargs.get('target', "")
        self.msg = kwargs.get('msg', "")
        self.raw = kwargs.get('raw', "")
        
    def parse(self):
        """
Uses regex to determine event type, participants and messages.
        """
        if self.raw and self.type == TYPE_UNKNOWN:
            msg_match = self._parse(self.raw)
            
            msg_data = msg_match.groupdict()
            self.command = msg_data.get('command')
            self.source = msg_data.get('source')
            self.target = msg_data.get('target')
            self.msg = msg_data.get('msg')
                
            if self.command.upper() == "PING":
                self.type = TYPE_PING
            elif self.command.upper() == "PRIVMSG":
                if self.msg.startswith("\x01ACTION"):
                    self.type = TYPE_ACTION
                else:
                    self.type = TYPE_PRIVMSG
            elif self.command.upper() == "NOTICE":
                self.type = TYPE_NOTICE
            elif self.command.upper() == "JOIN":
                self.type = TYPE_JOIN
            elif self.command.upper() == "PART":
                self.type = TYPE_PART
            elif self.command.upper() == "NICK":
                self.type = TYPE_NICK
            elif self.command.upper() == "QUIT":
                self.type = TYPE_QUIT
                
    def _parse(self,raw):
        raw_parts = raw.split(':', 2)
        
        command = ""
        source = ""
        target = ""
        msg = ""
        
        if raw.startswith(':'):
            args = raw_parts[1].split()
            source = args[0]
            command = args[1]
            target = " ".join(args[2:])
            print len(raw_parts)
            if len(raw_parts) == 3:
                msg = raw_parts[2]
        else:
            command = raw_parts[0]
            if len(raw_parts) == 3:
                msg = raw_parts[2]
                args = raw_parts[1].split()
                source = args[0]
                targets = " " .join(args[1:])
            elif len(raw_parts) == 2:
                msg = raw_parts[1]
            
        return {
            'command': command,
            'source': source,
            'target': target,
            'msg': msg
        }
            
            
                
    def as_dict(self):
        return {
            'created': self.created.isoformat(),
            'type': self.type,
            'source': self.source,
            'command': self.command,
            'target': self.target,
            'message': self.msg
        }

class Unknown(BaseEvent):
    def __init__(self, **kwargs):
        BaseEvent.__init__(self, **kwargs)
        
class Connect(BaseEvent):
    def __init__(self):
        BaseEvent.__init__(self)
        self.type = TYPE_CONNECTED
        
class Disconnect(BaseEvent):
    def __init__(self):
        BaseEvent.__init__(self)
        self.type = TYPE_DISCONNECTED
        
class Join(BaseEvent):
    def __init__(self, **kwargs):
        BaseEvent.__init__(self)
        self.type = TYPE_JOIN
        self.target = self.msg
        if kwargs.get('channels'):
            self.raw = "JOIN %s" % ",".join(kwargs.get('channels'))
        
class Part(BaseEvent):
    def __init__(self, **kwargs):
        BaseEvent.__init__(self)
        self.type = TYPE_PART
        if kwargs.get('channels'):
            self.raw = "PART %s" % ",".join(kwargs.get('channels'))

class Quit(BaseEvent):
    def __init__(self, **kwargs):
        BaseEvent.__init__(self)
        self.type = TYPE_QUIT
        self.raw = "QUIT %s" % kwargs.get('msg', "Goodbye cruel world")
        
class PrivMsg(BaseEvent):
    def __init__(self, **kwargs):
        BaseEvent.__init__(self)
        self.type = TYPE_PRIVMSG
        if kwargs.get('target') and kwargs.get('msg'):
            self.raw = "PRIVMSG %s :%s" % (kwargs.get('target'), kwargs.get('msg'))
        
class Action(BaseEvent):
    def __init__(self, **kwargs):
        BaseEvent.__init__(self)
        self.type = TYPE_ACTION
        if kwargs.get('target') and kwargs.get('msg'):
            self.raw = "PRIVMSG %s :\x01ACTION %s\x01" % (kwargs.get('target'), kwargs.get('msg'))
        
class Notice(BaseEvent):
    def __init__(self, **kwargs):
        BaseEvent.__init__(self)
        self.type = TYPE_NOTICE
        if kwargs.get('to') and kwargs.get('msg'):
            self.raw = "NOTICE %s :%s" % (kwargs.get('target'), kwargs.get('msg'))
        
class Ping(BaseEvent):
    def __init__(self, **kwargs):
        BaseEvent.__init__(self)
        self.type=TYPE_PING
        
class Pong(BaseEvent):
    def __init__(self, **kwargs):
        BaseEvent.__init__(self)
        self.type=TYPE_PONG
        if kwargs.get('msg'):
            self.raw = "PONG :%s" % kwargs.get('msg')
            
class User(BaseEvent):
    def __init__(self, **kwargs):
        BaseEvent.__init__(self)
        self.type=TYPE_USER
        if kwargs.get('name'):
            name = kwargs.get('name')
            self.raw = "USER %s" % " ".join([name, name, name, name])
            
class Nick(BaseEvent):
    def __init__(self, **kwargs):
        BaseEvent.__init__(self)
        self.type=TYPE_NICK
        if kwargs.get('name'):
            self.raw = "NICK %s" % kwargs.get('name')
