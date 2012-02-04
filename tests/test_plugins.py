import unittest
from multiprocessing import Queue, Process
from os import path
from imp import load_source
import events
import settings

class TestNick_handler(unittest.TestCase):
    nick_handler_module_path = path.join('..', 'plugins', 'core','nick_handler.py')

    def setUp(self):
        self.nick_handler = load_source('nick_handler', self.nick_handler_module_path)
        
    def test_match(self):
        example_433s = [
            """:hybrid7.debian.local 433 * nobody :Nickname is already in use."""
        ]
        for m433 in example_433s:
            event = events.Unknown(raw=m433)
            event.parse()
            self.assertTrue(self.nick_handler.match(event))
            
        example_other_msgs = [
            """PING :hybrid7.debian.local""",
            """:hybrid7.debian.local 372 matt :-                             ircd-hybrid restart."""
        ]
        for msg in example_other_msgs:
            event = events.Unknown(raw=msg)
            event.parse()
            self.assertFalse(self.nick_handler.match(event))

    def test_process(self):
        new_nick_msg = self.get_raw_output(settings.NAME)
        self.assertTrue(settings.NAME_BACKUP_1 in new_nick_msg)
        
        new_nick_msg = self.get_raw_output(settings.NAME_BACKUP_1)
        self.assertTrue(settings.NAME_BACKUP_2 in new_nick_msg)
        
        random_name_test = "%s-" % settings.NAME
        new_nick_msg = self.get_raw_output(settings.NAME_BACKUP_2)
        self.assertTrue(random_name_test in new_nick_msg)
        
        #TODO: needs to test whether it will change the name again
        
    def get_raw_output(self, name):
        mean_433 = """:hybrid7.debian.local 433 * %s :Nickname is already in use."""
        raw_msg = mean_433 % name
        event = events.Unknown(raw=raw_msg)
        event.parse()
        txq = Queue()
        p = Process(target=self.nick_handler.process, args=(txq, event, None)) # rxq is never used
        p.start()
        msg_obj = self.txq.get()
        p.terminate()
        return msg_obj.raw
