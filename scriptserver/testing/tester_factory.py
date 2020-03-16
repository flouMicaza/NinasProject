from scriptserver.testing.tester_builder import TesterBuilder
from os import listdir
from os.path import isfile, join

"""
Tester factory that uses the Flyweight pattern to avoid creating too many instances of testers for the same problem
"""
class TesterFactory:

    def __init__(self):
        self.tester_dict = {}

    def get_tester(self, path):
        """
        Creates a tester with all the tests in the path directory
        :param path: str
        :return: Tester
        """
        if not path in self.tester_dict.keys():
            test_paths = []
            for f in listdir(path):
                if isfile(join(path, f)) and f[-3:] == ".in":
                    test_paths.append(f)

            tester_build = TesterBuilder()
            for test_path in test_paths:
                tester_build.add_test_with_path(path + test_path)

            self.tester_dict[path] = tester_build.get_tester()
        return self.tester_dict[path]

    def get_tester_json(self, path):
        """
        Creates a tester with all the tests in a json file
        :param path: str
        :return: Tester
        """
        if not path in self.tester_dict.keys():

            tester_build = TesterBuilder()

            try:
                tester_build.add_tests_json(path)
            except:
                return 1

            self.tester_dict[path] = tester_build.get_tester()
        return self.tester_dict[path]