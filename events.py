import re

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

class BaseEvent(object):
    message_match = re.compile(r"^(?:[:@](?P<source>[\S]+) )?(?P<command>[\S]+)(?: (?P<target>(?:[^:\s][\S]* ?)*))?(?: ?:(?P<msg>.*))?$")
    def __init__(self, **kwargs):
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
            print self.raw
            msg_match = self.message_match.match(self.raw)
            msg_data = msg_match.groupdict()
            self.command = msg_data.get('command')
            self.source = msg_data.get('source')
            self.target = msg_data.get('target')
            self.msg = msg_data.get('msg')
        if self.command.lower() == "PING":
            self.type = TYPE_PING
        elif self.command.lower() == "PRIVMSG":
            if self.msg.startswith("\x01ACTION"):
                self.type = TYPE_ACTION
            else:
                self.type = TYPE_PRIVMSG
        elif self.command.lower() == "NOTICE":
            self.type = TYPE_NOTICE
        elif self.command.lower() == "JOIN":
            self.type = TYPE_JOIN
        elif self.command.lower() == "PART":
            self.type = TYPE_PART
        elif self.command.lower() == "QUIT":
            self.type = TYPE_QUIT

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
        self.type = TYPE_ACTOIN
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
