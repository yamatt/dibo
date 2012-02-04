import unittest
from multiprocessing import Queue, Process
from os import path
from imp import load_source
import events
import settings

class TestEvents(unittest.TestCase):
    events_module_path = path.join('..', 'events.py')
    sameple_file = path.join('..','sample data', 'samplemessages')

    def setUp(self):
        self.events_module = load_source('events', self.events_module_path)
        self.base_event = self.events_module.BaseEvent()
        
    def test_parse(self):
        f = open(self.sameple_file, 'r')
        line = f.readline()
        while line:
            line_split = line.split(':', 2)
            parsed = self.base_event._parse(line)
            if line.startswith(':'):
                if len(line_split) == 2:
                    self.assertFalse(parsed['msg'])
                elif len(line_split) == 3:
                    self.assertTrue(parsed['msg'])
            else:
                if len(line_split) == 2:
                  self.assertEquals(parsed['command'], line_split[0])
                elif len(line_split) == 3:
                    pass
            
            line = f.readline()
