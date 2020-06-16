from subprocess import Popen, PIPE, TimeoutExpired, call, STDOUT, run
from ..util import *
script_dict = {}


class Script:

    def __init__(self, path):
        self.path = path

    def get_process(self):
        """
        Creates a new subprocess to run the script and returns it
        :return: Subprocess
        """
        pass

    def run(self, test_input, timeout):
        """
        Runs a script with some input and a timeout in seconds and returns what's in stdout, an error code and if it was
        killed because of the timeout
        :param test_input: str
        :param timeout: int
        :return: str, str, bool
        """
        p = self.get_process()
        if test_input != '':
            p.stdin.write(test_input)

        killed_by_time = False
        try:
            out, err = p.communicate(timeout=timeout)
            err = p.returncode
        except TimeoutExpired:
            p.kill()
            out, err = p.communicate()
            err = p.returncode
            killed_by_time = True

        return out, err, killed_by_time

    def process_error(self, err):
        # No Error
        if err >= 0:
            return 0
        # Error
        else:
            return 1


script_dict["python3"] = lambda path: (Python3Script(path))
class Python3Script(Script):

    def __init__(self, path):
        Script.__init__(self, path)

    def get_process(self):
        return Popen(['python3', self.path], stdin=PIPE, stdout=PIPE, stderr=PIPE)


script_dict["python2"] = lambda path: (Python2Script(path))
class Python2Script(Script):

    def __init__(self, path):
        Script.__init__(self, path)

    def get_process(self):
        return Popen(['python', self.path], stdin=PIPE, stdout=PIPE, stderr=PIPE)


script_dict["cpp"] = lambda path: (CppScript(path))
class CppScript(Script):

    def __init__(self,path):
        Script.__init__(self,path)

    def get_process(self):
        try:
            file_name = get_file_name(self.path)
            # Con run puedo tomar el output y el error que se genere. Para trabajo futuro.
            a = run(['g++','-std=c++11',self.path,'-o',file_name])
            print(a)

        except Exception as e:
            print("Excepcion porque esta malooooo en script",e) #TODO: Revisar que exception quiero mostras y como lidiar con ellas.

        return Popen(['./' + file_name], stdin=PIPE, stdout=PIPE, stderr=PIPE)