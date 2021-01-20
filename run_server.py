import sys
from scriptserver.comunication.server import Server
import os


args = sys.argv

if len(args) > 3:
    raise Exception(
        "Incorrect number of Arguments, the script can take no arguments or a number of scheduler slave processes as or the max output length "
        "shown:\n\n python3 run_server.py <number_of_slave_processes:int> <output_len:int>\n")

if len(args) == 1:
    serv = Server(40000)
elif len(args) == 2:
    serv = Server(40000, int(args[1]))
else:
    serv = Server(40000,int(args[1]),int(args[2]))

while True:
    serv.receive_msg()
