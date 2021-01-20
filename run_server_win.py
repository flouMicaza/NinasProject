import sys
from scriptserver.comunication.win_server import WinServer

args = sys.argv

if len(args) > 3:
    raise Exception(
        "Incorrect number of Arguments, the script can take no arguments or a number of scheduler slave processes as or the max output length"
        "shown:\n\n python3 run_server_win.py <number_of_slave_processes:int> <output_len:int>\n")

if len(args) == 1:
    serv = WinServer(40000)
if len(args) == 2:
    serv = WinServer(40000, int(args[1]))
else:
    serv = WinServer(40000, int(args[1]), int(args[2]))

while True:
    serv.receive_msg()
