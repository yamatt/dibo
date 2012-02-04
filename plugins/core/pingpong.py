import re
import events

ping = re.compile(r'PING :(.*)')

def match(msg_obj):
    if hasattr(msg_obj, 'raw'):
        return bool(ping.match(msg_obj.raw))

def process(q, msg_obj, rxq):
    response = events.PONG(msg_obj.text)
    print "PING/PONG"
    q.put(response)
