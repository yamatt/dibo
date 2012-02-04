import string
from time import sleep
from random import randint
from random import choice as choose

import events
import settings

NAME_DELAY=60

def match(msg_obj):
    return msg_obj.command == "433"

def process(q, msg_obj, rxq):
    nick = msg_obj.target.split()
    current_nick = nick[0]
    attempted_nick = nick[1]
    normal_nick_event = events.Nick(name=settings.NAME)
    next_nick = None
    
    if current_nick == "*":
        if attempted_nick == settings.NAME:
            new_nick = settings.NAME_BACKUP_1
        elif attempted_nick == settings.NAME_BACKUP_1:
            new_nick = settings.NAME_BACKUP_2
        else:
            new_nick = generate_random_nick(settings.NAME)

    if next_nick:
        nick_event = events.Nick(name=new_nick)
        q.put(nick_event)
    sleep(NAME_DELAY) 
    q.put(normal_nick_event)    #TODO: this causes multiple nick reset attemps for each nick fail. How to prevent?
    
def generate_random_nick(base_name,max_length=16):
    max_length = max_length - len(base_name)
    chars = string.ascii_lowercase
    digits = string.digits
    selection = chars+digits
    random_string = ''.join(choose(selection) for x in range(randint(max_length)))
    return "%s-%s" % (base_name, random_string)
