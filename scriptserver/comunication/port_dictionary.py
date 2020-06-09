# -*- coding: utf-8 -*-


from threading import Condition


class PortDictionary:

    def __init__(self):
        """
        Creates a new port dictionary with the ports 40001 to 50000 available
        """
        self.non_used_ports = []
        self.c = Condition()

        for i in range(40001, 50001):
            self.non_used_ports.append(i)

    def get_port(self):
        """
        Gets a port from the list, if there are no ports it returns -1
        :return: int
        """

        port = -1

        self.c.acquire()

        if len(self.non_used_ports) > 0:
            port = self.non_used_ports.pop()

        self.c.release()

        return port

    def liberate_port(self, port):
        """
        Adds a new port to the list
        :param port: int
        """
        self.c.acquire()

        self.non_used_ports.append(port)

        self.c.notify_all()
        self.c.release()
