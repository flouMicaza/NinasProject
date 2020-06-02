from queue import Queue
from threading import Condition, Thread
import logging


# Syncronization tools
# https://hackernoon.com/synchronization-primitives-in-python-564f89fee732

class Scheduler(Thread):

    def __init__(self, server, process_num=10):
        Thread.__init__(self)

        self.queue = Queue()
        self.server = server

        self.c = Condition()
        self.slave_c = Condition()

        self.available_processes = process_num

    def run(self):
        self.run_next_script()

    def add_process(self):
        self.slave_c.acquire()
        self.available_processes += 1
        self.slave_c.notify_all()
        self.slave_c.release()

    def add_script_to_queue(self, submision_id, script, tester):
        """
        Adds a script with a submission_id and a tester to the queue of scripts to be tested.
        :param submision_id: int
        :param script: Script
        :param tester: Tester
        :return: None
        """
        self.c.acquire()
        self.queue.put((submision_id, script, tester))
        self.c.notify()
        self.c.release()

    def run_next_script(self):
        """
        Runs the next script in the queue, if there is none it waits until there is one.
        :return: None
        """
        #logging.debug("Scheduler: Preparing to Run a new Script...")

        self.c.acquire()
        while self.queue.empty():
            self.c.wait()

        #logging.debug("Scheduler: Getting new Submission...")
        submission_tuple = self.queue.get()
        logging.debug("Scheduler: Got new Submission " + str(submission_tuple[0]))
        self.c.release()

        submission_id = submission_tuple[0]
        script = submission_tuple[1]
        tester = submission_tuple[2]

        self.slave_c.acquire()

        while self.available_processes == 0:
            self.slave_c.wait()

        self.available_processes -= 1
        SchedulerSlave(self.server, self, submission_id, script, tester).start()
        self.slave_c.release()

        self.run_next_script()


class SchedulerSlave(Thread):

    def __init__(self, server, scheduler, submission_id, script, tester):
        Thread.__init__(self)
        self.server = server
        self.scheduler = scheduler
        self.submission_id = submission_id
        self.script = script
        self.tester = tester

    def run(self):
        self.run_script()

    def run_script(self):
        try:
            results = self.tester.test_script(self.script)
        except OSError:
            return self.server.error_slave.add_submission_to_queue(self.submission_id,
                                                                   "Ocurrió un error al compilar tu archivo, "
                                                                   "comprueba con tu tutora que tu código compile y "
                                                                   "vuelve a intentarlo. ")
        except Exception as e:
            return self.server.error_slave.add_submission_to_queue(self.submission_id, "Ocurrió un error al procesar "
                                                                                       "tu código, comprueba con tu "
                                                                                       "tutora que tu código compile "
                                                                                       "y vuelve a intentarlo. ")

        if len(results) > 0:
            self.server.answer_submission(self.submission_id, results)
        else:
            self.server.answer_submission_error(self.submission_id, "No hay tests para este problema. Contacta a tu "
                                                                    "tutora para que arregle este error.")

        self.scheduler.add_process()
