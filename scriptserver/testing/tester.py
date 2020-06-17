from scriptserver.testing.test import Test
from scriptserver.util import clean_output


class Tester:

    def __init__(self, timeout=3):
        self.tests = []
        self.timeout = timeout

    def add_test(self, test):
        """
        Adds a test to the tests array
        :param test: Test
        :return: None
        """
        self.tests.append(test)

    def add_new_test(self, test_input, test_output, comment=""):
        """
        Creates a tests and adds it to the tests array
        :param test_input: str
        :param test_output: str
        :param comment: str
        :return: None
        """
        self.tests.append(Test(test_input, test_output, comment))

    def set_timeout(self, new_timeout):
        self.timeout = new_timeout

    def test_script(self, script):
        """
        Returns a tuple (passed:bool, test:Test, (output:bytes, error:bytes, killed_by_time:bool))
        where passed is aboolean that represents if the test passed or not, test is the associated test,
        output is the output of the script with the test input, error is the error message from the script
        and killed_by_time is a boolean that tells if the program was killed by the tester timeout
        :param script: Script
        :return: (passed:bool, test:Test, (output:bytes, error:bytes, killed_by_time:bool))
        """
        passed = []
        for test in self.tests:
            out, err, killed_by_time = script.run(test.input, self.timeout)
            out = clean_output(out)
            test_passed = (out == test.output)
            passed.append((test_passed, test, (out, script.process_error(err), killed_by_time)))

        return passed
