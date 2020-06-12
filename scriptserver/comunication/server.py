# -*- coding: utf-8 -*-


import socket
import json
from threading import Condition, Thread
from queue import Queue
from scriptserver.testing.tester_factory import TesterFactory
from scriptserver.testing.script import script_dict
from scriptserver.testing.scheduler import Scheduler
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-9s) %(message)s', )

CATEGORY_BYTE_LEN = 100
STD_BYTE_LEN = 300
TOTAL_BYTES_BY_MESSAGE = 2048


class Server:

    def __init__(self, port, scheduler_slaves=10):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.public_host = '186.11.79.106'
        print(self.public_host, "las variables",port)
        self.socket.bind((self.public_host, port))

        self.sub_id_to_port_dict = {}

        self.tester_factory = TesterFactory()

        self.scheduler = Scheduler(self, scheduler_slaves)

        # starts thread that runs the function run_next_script of the scheduler
        self.scheduler.start()

        self.error_slave = ErrorSlave(self)
        self.error_slave.start()

        self.script_dict = script_dict

    def receive_msg(self):
        print("Waiting for message")
        data, addr = self.socket.recvfrom(1024)
        decoded_data = json.loads(data.decode())
        # print("Received Message")
        # print("Received:", decoded_data)

        port = decoded_data[0]
        submission_id = decoded_data[1]
        path_script = decoded_data[2]
        path_tester = decoded_data[3]
        lang = decoded_data[4]

        self.sub_id_to_port_dict[submission_id] = port

        tester = self.tester_factory.get_tester_json(path_tester)
        if tester == 1:
            return self.error_slave.add_submission_to_queue(submission_id,
                                                            "Invalid or corrupted tests file. Please contact a "
                                                            "teacher of assistant of the course of this assignment to "
                                                            "fix this error.")
        script = self.script_dict[lang](path_script)

        # print("Sending data to scheduler...")
        self.scheduler.add_script_to_queue(submission_id, script, tester)
        # print("Data sent to scheduler.")

    def answer_submission(self, submission_id, results):
        # logging.debug("Answering Submission " + str(submission_id))

        reply_arr = []

        #Procesamiento de los test. Aquí se define el array que le entrega al cliente.
        for result in results:
            # Unpack info
            passed = int(result[0])  # 1 byte
            test = result[1]
            test_input = test.input.decode()[:STD_BYTE_LEN]  # STDLEN bytes
            expected_output = test.output.decode()[:STD_BYTE_LEN]  # STDLEN bytes
            actual_output = result[2][0].decode()[:STD_BYTE_LEN]  # STDLEN bytes
            comment = test.get_comment()[:CATEGORY_BYTE_LEN]  # CATLEN bytes
            err = result[2][1]  # 1 byte
            timeout = result[2][2]

            if timeout:
                err = 2


            # Create reply as a json bytes object
            reply_arr.append([passed, test_input, expected_output, comment, err, actual_output])

            # print("Sent:", reply_message)
        reply_message = json.dumps(["success", reply_arr]).encode()

        # Open TCP socket with the port associated to the submission ID
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect(('172.16.0.2', self.sub_id_to_port_dict[submission_id]))
            sock.sendall(reply_message)
            logging.debug("Successfuly Sent Response " + str(submission_id))
        except ConnectionRefusedError:
            logging.debug("Failed Sending Response " + str(submission_id) + ": Connection with django process lost")
        except ConnectionResetError:
            logging.debug("Failed Sending Response " + str(submission_id))
        except:
            logging.debug("Failed Sending Response " + str(submission_id) + ": Unknown Error")

        # Close socket
        sock.close()

    def answer_submission_error(self, submission_id, error):
        # logging.debug("Answering Submission " + str(submission_id) + " with error")

        reply_message = json.dumps(["error", error]).encode()

        # Open TCP socket with the port associated to the submission ID
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect(('172.16.0.1', self.sub_id_to_port_dict[submission_id]))
            sock.sendall(reply_message)
            logging.debug("Successfuly Sent Error Response " + str(submission_id))
        except ConnectionRefusedError:
            logging.debug(
                "Failed Sending Error Response " + str(submission_id) + ": Connection with django process lost")
        except ConnectionResetError:
            logging.debug("Failed Sending Error Response " + str(submission_id))
        except:
            logging.debug("Failed Sending Error Response " + str(submission_id) + ": Unknown Error")

        # Close socket
        sock.close()


class ErrorSlave(Thread):

    def __init__(self, server):
        Thread.__init__(self)
        self.server = server
        self.queue = Queue()
        self.c = Condition()

    def add_submission_to_queue(self, submision_id, error):
        self.c.acquire()
        self.queue.put((submision_id, error))
        self.c.notify()
        self.c.release()

    def run(self):
        self.answer_next_submission()

    def answer_next_submission(self):
        self.c.acquire()
        while self.queue.empty():
            self.c.wait()

        submission_tuple = self.queue.get()
        self.c.release()

        self.server.answer_submission_error(submission_tuple[0], submission_tuple[1])

        self.answer_next_submission()
