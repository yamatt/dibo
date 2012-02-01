import settings
from time import sleep

def match(msg_obj):
    return msg_obj.command == "433"

def process(q, msg_obj):
    # get attempted nick
    # check for more nicks
    # there is another nick available
        # set username to temporary one
    # there is no nicks available
        # quit
    pass
    
