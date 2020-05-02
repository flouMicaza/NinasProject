from scriptserver.testing.tester import Tester
import json


class TesterBuilder():

    def __init__(self):
        self.tester = Tester()

    def set_timeout(self, new_timeout):
        self.tester.set_timeout(new_timeout)
        return self

    def add_tests_json(self, path):
        """
        Adds all the tests in a test file to the builder's tester
        :param path: str
        :return: TesterBuilder
        """
        with open(path, 'r') as f:
            datastore = json.load(f)

        for test_dict in datastore: #Aquí es donde se generan los test, tengo que modificar para que reciba mi nueva info.
            self.tester.add_new_test(test_dict["Input"].encode(), test_dict["Output"].encode(), test_dict["Comment"], test_dict["Test Type"])

    def add_test_with_path(self, path):
        """
        Adds a test using 3 file paths
        :param path: str
        :return: TesterBuilder
        """
        in_file = open(path + ".in", "r")
        out_file = open(path + ".out", "r")
        info_file = open(path + ".info", "r")

        input = in_file.read().encode()
        output = out_file.read().encode()
        info = info_file.read()

        self.tester.add_new_test(input, output, info)

        return self

    def get_tester(self):
        return self.tester
