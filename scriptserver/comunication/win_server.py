from subprocess import Popen, PIPE
from scriptserver.comunication.server import Server
from scriptserver.testing.script import Script

script_dict2 = {}

class WinServer(Server):

    def __init__(self, port, scheduler_slaves=10):
        Server.__init__(self, port, scheduler_slaves)
        self.script_dict = script_dict2


script_dict2["python3"] = lambda path: (Python3ScriptWin(path))
class Python3ScriptWin(Script):

    def __init__(self, path):
        Script.__init__(self, path)

    def get_process(self):
        return Popen(['py', '-3', self.path], stdin=PIPE, stdout=PIPE, stderr=PIPE)


script_dict2["python2"] = lambda path: (Python2ScriptWin(path))
class Python2ScriptWin(Script):

    def __init__(self, path):
        Script.__init__(self, path)

    def get_process(self):
        return Popen(['py', '-2', self.path], stdin=PIPE, stdout=PIPE, stderr=PIPE)