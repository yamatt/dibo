import events
import settings
from multitasking import Process
import os
from imp import load_source

NAME_PLUGIN_PATH = "name_maker"

command = re.compile("(?P<name>%s)[:,]? (?P<command>\w+)(?: (?P<msg>.*))?" % settings.NAME)
plugins = {}

def match (msg_obj):
    if msg_obj.type == events.PRIVMSG:
        return True
    elif msg_obj.type == events.JOIN:
        return True
    elif msg_obj.type == events.PART:
        return True
    elif msg_obj.type == events.NICK:
        return True
    elif msg_obj.type == events.QUIT:
        return True
    
def process(q, msg_obj):
    # manage users and channels
    match = command.match(msg_obj.text)
    # run as process
    command = match.groupdict.get('command')
    msg = match.groupdict.get('msg')
    p = Process(target=plugins[command], args=(q, msg_obj, command, msg))
    p.start()

# get plugins
def load_plugins():
    for file_name in os.listdir(self.NAME_PLUGIN_PATH):
        plugin_name = file_name.rsplit(".",1)[0]
        plugin_path = os.path.join(self.NAME_PLUGIN_PATH, file_name)
        if os.path.isfile(plugin_path) and file_name.endswith(".py"):
            module = load_source(plugin_name, file_path)
            commands = module.commands
            for command in commands:
                if not self.plugins.get(command):
                    self.plugins[plugin_name] = module.process
                else 
                    print "Warning. Name Maker. Plugin name collision"
