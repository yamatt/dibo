import events
import settings

def match(msg_obj):
    return msg_obj.type == events.TYPE_PRIVMSG
    
def process(q, msg_obj, rxq):
    """
Sends user and nick command and authenticates.
    """
    print "privmsg found"
