from multiprocessing import Process
import events
import settings
from imp import load_source
import os

class Broker(object):
    def __init__(self, rxq, txq):
        """
Imports sub-processes defined in settings and takes their matching regex, type, or function.
Then listens to the queue and spawns processes based upon the match passing the txq.
        """
        self.rxq = rxq
        self.txq = txq
        self.plugins = {}
        self.find_plugins()
        
        try:
            self.start()
        except KeyboardInterrupt:
            pass
            
    def find_plugins(self):
        # core plugins (not optional)
        core_plugins_dir = os.path.join(settings.PLUGINS_DIR, "core")
        for plugin_file in os.listdir(core_plugins_dir):
            plugin_name = plugin_file.rsplit(".", 1)[0]
            plugin_path = os.path.join(core_plugins_dir, plugin_file)
            self.add_plugin(plugin_name, plugin_path)

        # standard plugins (have to be enabled)
        for plugin_name in settings.PLUGINS:
            plugin_path = os.path.join(settings.PLUGINS_DIR, "%s.py" % plugin_name)
            self.add_plugin(plugin_name, plugin_path)
    
    def add_plugin(self, name, path):
        if os.path.isfile(path) and path.endswith(".py"):
            plugin = load_source(name, path)
            self.plugins[name] = {
                'plugin': plugin.process,
                'match': plugin.match
            }

    def start(self):
        while True:
            msg_obj = self.rxq.get()
            if msg_obj.type == events.TYPE_UNKNOWN:
                print "~~~" + msg_obj.raw
                msg_obj.parse()
            # match obj to processes
            for plugin in self.plugins.itervalues():
                if plugin['match'](msg_obj):
                    p = Process(target=plugin['plugin'], args=(self.txq,msg_obj))
                    p.start()
                    # might have to be smarter here and add the processes to a list which gets trimmed when processes complete
