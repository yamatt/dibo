import events
import settings

def match(msg_obj):
    return msg_obj.type == events.TYPE_CONNECTED
    
def process(q, msg_obj):
    """
Sends user and nick command and authenticates.
    """
    # recognise 
    user = events.User(name=settings.NAME)
    nick = events.Nick(name=settings.NAME)
    
    q.put(user)
    q.put(nick)
    
    # authenticate
    
    # join auto channels
    channels = events.Join(channels=settings.AUTOJOIN)
    q.put(channels)
