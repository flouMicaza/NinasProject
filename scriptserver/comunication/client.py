import socket
import json
from scriptserver.comunication.port_dictionary import PortDictionary
from scriptserver.comunication.server import TOTAL_BYTES_BY_MESSAGE


class Client:

    def __init__(self):
        self.udp_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.port_dictionary = PortDictionary()
        self.server_port = 40000

        # socket.rcv() timeout set to 10 secs
        socket.RCVTIMEO = 10000

    def send_submission(self, submission_path, test_path, lang):
        """
        Sends a submission to be tested and returns the results
        :param submission_path: str
        :param test_path: str
        :param lang: 'python2' | 'python3'
        :return: [[passed:int, input:str, expected_output:str, output:str, category:str, err:int], ...]
        err: 0 (no error) | 1 (runtime or compilation error) | 2 (timeout error)
        """
        # Get port from dictionary
        port = self.port_dictionary.get_port()

        if port == -1:
            return ["error", "We are testing too many submissions right now, please try again later."]

        # Pack json submission
        message = json.dumps([port, port, submission_path, test_path, lang]).encode()

        # Send packed message to testing process
        self.udp_sock.sendto(message, ('localhost', self.server_port))

        # Open Socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', port))

        test_data = []
        try:
            # Wait for tester process to open socket
            sock.listen()
            # Accept tester process
            conn, addr = sock.accept()

            # Get tests data
            test_data_str = ""
            done = False
            while not done:
                try:
                    data = conn.recv(TOTAL_BYTES_BY_MESSAGE)

                    if not data:
                        done = True
                    else:
                        test_data_str += data.decode()
                except:
                    done = True

            test_data = json.loads(test_data_str)
        except:
            test_data = ["error", "Error comunicating with the tester server, please try again later."]

        # Close socket
        sock.close()

        # Liberate port in dictionary
        self.port_dictionary.liberate_port(port)

        return test_data
