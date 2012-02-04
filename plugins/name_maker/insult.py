import events
from random import choice
commands = ['insult', 'yow', 'woy']

insults = [
    """you fooking loon.""",
    """ya spanna!"""
]

yows = [
    """not a chance buster."""
    """Are you as bored as I am?"""
]

def process(q, msg_obj, command, msg):
    target=msg_obj.target
    if command==self.commands[0]:   #insult
        nick_to = msg
        # check nick for admin rights, exists in channel, etc.
        insult = choice(self.insults)
        msg = "%s %s" % (nick_to, insult)
    elif command=self.commands[1] or command=self.commands[2]: #yow/woy
        msg = choice(self.yows)
        if command==self.commands[2]:
            msg = msg[::-1]
    event = events.PrivMsg(target=target, msg=msg)
    q.put(event)
