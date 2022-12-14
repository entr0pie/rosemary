
import ipaddress
import subprocess
import threading
import argparse

class bcolors:
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
    INFO = '\033[177m'
                                                               
def ping_host_group(group, verbose):
    for addr in group:
        ping = subprocess.Popen(
            ["ping", "-c", "1", str(addr)],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        out, error = ping.communicate()
        if verbose:
            print(f"{b.INFO}[*]{b.ENDC} Trying {addr}")
        
        if "100% packet loss" not in out.decode():
            print(f"{b.OKGREEN}[!]{b.ENDC} {addr} ")
        
        if args.output:
            file = open(args.output, 'a')
            file.write(addr + '\n')
            file.close()



parser = argparse.ArgumentParser(description="Tool for finding devices on a local network (ICMP)")
parser.add_argument("-N", "--network", type=str, required=True, help="Network range with suffix (eg. 192.168.10.0/24)")
parser.add_argument("-T", "--threads", type=int, required=False, help="Number of threads")
parser.add_argument("-v", "--verbose", action='store_true', help="Show tried IP's")
parser.add_argument("--nocolor", action='store_true')
parser.add_argument("-o", "--output", type=str, required=False, help="Output to an local file")
args = parser.parse_args()

b = bcolors()

if args.nocolor:
    b.HEADER = ''
    b.ENDC = ''
    b.OKCYAN = ''
    b.INFO = ''
    b.OKGREEN = ''
    b.BOLD = ''

print("\nRosemary by entr0pie (https://github.com/entr0pie/rosemary)\n")

network = args.network
print(f"{b.OKCYAN}[!]{b.ENDC} NETWORK: {network}")

network = ipaddress.IPv4Network(network)

threads = args.threads

if threads == None:
    threads = 2

print(f"{b.OKCYAN}[!]{b.ENDC} THREADS: {threads}")
print(f"{b.OKCYAN}[*]{b.ENDC} Searching...\n")

if args.output:
    file = open(args.output, 'a')
    file.write("# Rosemary by entr0pie (https://github.com/entr0pie/rosemary)")

range_ip = network.num_addresses // threads

per_thread = [0]
 
for th in range(threads):
    per_thread.append(range_ip + range_ip * th)

if range_ip % threads != 0:
    per_thread[-1] += range_ip % threads

interval_thread = []
for pt in range(1, len(per_thread)):
    interval_thread.append((per_thread[pt - 1], per_thread[pt]))

pos_address = []

for addr in network:
    pos_address.append(str(addr))

for it in interval_thread:
    group = []
    for i in range(it[0], it[1]):
        group.append(pos_address[i])
    
    threading.Thread(target=ping_host_group, args=(group, args.verbose)).start()
