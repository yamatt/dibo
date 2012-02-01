import events
import settings
from multitasking import Process

command = re.compile("%s[:,] (?P<command>\w+) ?(?P<msg>.*)" % settings.NAME)
plugins = {}

def match (msg_obj):
    return (msg_obj.type == events.PRIVMSG and msg_obj.text.startswith(settings.NAME)
    
def process(q, msg_obj):
    # manage users and channels
    match = command.match(msg_obj.text)
    # run as process
    command = match.groupdict.get('command')
    msg = match.groupdict.get('msg')
    plugins[command](q, msg_obj, msg)

# get plugins
