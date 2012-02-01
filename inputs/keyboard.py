import events

def input(rxq, txq):
    while True:
        command = raw_input('pyrc> ')
        command_parts = command.split()
        parse(command_parts)
        
def parse(commands=["help"]):
    options = structure
    for part in commands:
        if options.get(part):
            option = structure.get(part)
            if len(commands) > options['length']:
                option['process'](commands)
            else:
                print option['help']

def say(commands):
    target = commands[1]
    msg = " ".join(commands[2:])
    events.PrivMsg(target=target, msg=msg)
    
structure = {
    "help": {
        "length": 2048,
        "help": """help printed""",
    },
    "say": {
        "length": 2,
        "help": """say needs more than one argument""",
        "command": say
    }
}
