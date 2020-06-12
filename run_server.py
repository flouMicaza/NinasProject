import sys
from scriptserver.comunication.server import Server
import os
port = int(os.environ.get('PORT',4000))

args = sys.argv

if len(args) > 2:
    raise Exception(
        "Incorrect number of Arguments, the script can take no arguments or a number of scheduler slave processes as "
        "shown:\n\n python3 <number_of_slave_processes:int>")

if len(args) == 1:
    serv = Server(port)
else:
    serv = Server(port, int(args[1]))

while True:
    serv.receive_msg()
