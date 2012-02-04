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
        self.processes=[]
        
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
            self.add_plugin(plugin_name, plugin_path, True)

        # standard plugins (have to be enabled)
        for plugin_name in settings.PLUGINS:
            plugin_path = os.path.join(settings.PLUGINS_DIR, "%s.py" % plugin_name)
            self.add_plugin(plugin_name, plugin_path)
    
    def add_plugin(self, name, path, core=False):
        if os.path.isfile(path) and path.endswith(".py"):
            plugin = load_source(name, path)
            self.plugins[name] = {
                'plugin': plugin.process,
                'match': plugin.match
            }
            if core:
                self.plugins['core'] = True

    def start(self):
        while True:
            msg_obj = self.rxq.get()
            if msg_obj.type > events.TYPE_ADMIN_BROKER:
                self.broker_manage(msg_obj.type)
            else:
                if msg_obj.type == events.TYPE_UNKNOWN:
                    msg_obj.parse()
                # match obj to processes
                for plugin in self.plugins.itervalues():
                    if plugin['match'](msg_obj):
                        if plugin.get('core'):
                            p = Process(target=plugin['plugin'], args=(self.txq,msg_obj,self.rxq))
                        else:
                            p = Process(target=plugin['plugin'], args=(self.txq,msg_obj))
                        p.start()
                        self.processes.append(p)

    def broker_manage(type):
        if type == events.TYPE_ADMIN_BROKER_RELOAD:
            self.plugins={}
            self.find_plugins()
        elif type == events.TYPE_ADMIN_BROKER_FREE_MEMORY:
            new_processes = []
            for process in self.processes:
                process.join(timeout=0)
                if process.is_alive():
                    new_process.append(process)
        elif type == events.TYPE_ADMIN_BROKER_KILL_PROCESSES:
            for process in self.processes:
                process.join(timeout=3)
                if process.is_alive():
                    process.terminate()
