import subprocess
import os

SCRIPTS_DIR="scripts"

def match(msg_obj):
    return True
    
def process(q, msg_obj):
    """
Runs a bunch of files from the command line.
    """
    for script in os.listdir(self.SCRIPTS_DIR):
        script_path = os.path.join(self.SCRIPTS_DIR, script)
        if os.path.isfile(script_path):
            subprocess.Popen([script_path, msg_obj.raw])
