import os
import events
from datetime import datetime
try:
    from json import dumps as jsonwrite
except ImportError:
    from simplejson import dumps as jsonwrite

LOG_DIR="../../"
LOG_FILE="%Y%m%%d.log"

def match(msg_obj):
    if msg_obj.TYPE==events.TYPE_PRIVMSG:
        return True
    elif msg_obj.TYPE==events.ACTION:
        return True
    elif msg_obj.TYPE==events.JOIN:
        return True
    elif msg_obj.TYPE==events.PART:
        return True
    elif msg_obj.TYPE==events.NICK:
        return True
    elif msg_obj.TYPE==events.QUIT:
        return True

def process(q, msg_obj):
    now = datetime.now()
    log_file = now.strftime(self.LOG_FILE)
    log_path = os.path.join(self.LOG_DIR, log_file)
    
    event_dict = msg_obj.as_dict()
    json_event = jsonwrite(event_dict)
    
    with open(log_path, 'w') as f:
        f.write(json_event)
    
