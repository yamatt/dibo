import settings
import events

def match(msg_obj):
    """
The broker first sends the message to this function to see if it may be relevant to the main process.
    """
    if msg_obj.type == events.TYPE_PRIVMSG:
        return True
    elif msg_obj.type == events.NICK:
        return True
    elif msg_obj.type == events.JOIN:
        return True
    elif msg_obj.type == events.PART:
        return True
    elif msg_obj.type == events.QUIT:
        return True
    
def process(q, msg_obj, rxq):
    """
This function is placed in it's own process by the broker and passed the objects it needs to do it's business.
q and msg_obj are only for core functions. Adding stuff to the rxq could cause problems and is often not necessary.
:param q is the Queue that messages are put on to then sent to the server.
:param msg_obj is the message object that was received from the server.
    """
    
    
