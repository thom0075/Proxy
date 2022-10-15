import sys
import socket
import argparse
import threading

HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])
    #for i in range 255, checks if len(i) == 3 and if there is a printable char
    #available prints it else prints a dot (.)

def hexDMP(src, lenght=16):
    if type(src) == "bytes":
        src = src.decode()
    results = []
    for i in range(0, len(src), lenght):
        word = str(src[i:i+lenght])
        printable_char = word.translate(HEX_FILTER)
        hexa = " ".join(f"{ord(c):02x}" for c in word)
        hexawidth = lenght*2
        results.append(f"{i:04x} {hexa:<{hexawidth}} {printable_char}")  
        #4 characters-wide field for i, left aligned space to print
        # hex no., translated chars.

        for line in results:
            print(line)

    return results

def receive_from(connection):
    receive_buffer = b""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            receive_buffer+=data
    except Exception as e:
        print(f"[X] {e}")
    return receive_buffer

def handle_proxy(client_connection, dest_connection, dest_port, recv_first):
    #create a socket to send data
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #connects to the remote host
    remote_socket.connect((dest_connection, dest_port))
    if recv_first:
        dest_buffer = receive_from(remote_socket)
        hexDMP(dest_buffer)
        if dest_buffer:
            print(f"[*] Received {len(dest_buffer)} bytes from remote.")
    while True:
        local_buffer = receive_from(client_connection)

        if len(local_buffer):
            print(f"[*] Received {len(local_buffer)} bytes from local.")
            hexDMP(local_buffer)
            remote_socket.send(local_buffer)

        dest_buffer = receive_from(remote_socket)
        print(f"[*] Received {len(dest_buffer)} bytes from remote.")

        if len(dest_buffer):
            client_connection.send(dest_buffer)
            print(f"[*] Sent {len(dest_buffer)} bytes to local.")
            hexDMP(dest_buffer)

        if not len(dest_buffer) or not len(local_buffer):
            print("[X] No more data to transfer. Closing connections...")
            remote_socket.close()
            client_connection.close()
            break

def proxy_Server(local_addr, local_port, dest_connection, dest_port, recv_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_addr, local_port))
        print("[*] Server bind successful.")

    except Exception as e:
        print(f"[X] {e}")
        sys.exit(0)
    server.listen(5)

    while True:
        client_sock, addr = server.accept()
        print(f"[*] Received a connection from: {addr[0]}, port: {addr[1]}")
        proxy_thread = threading.Thread(target = handle_proxy, args=(client_sock,
         dest_connection, dest_port, recv_first))
        proxy_thread.start()

def main():
    parser = argparse.ArgumentParser(description="Python3 proxy")

    parser.add_argument("-s", "--server", type=str, required=True, help="Server's IPv4 address")
    parser.add_argument("-p", "--Sport", type=int, required=True, help="Server's port")
    parser.add_argument("-d", "--dest", type=str, required=True, help="Destination address/domain")
    parser.add_argument("-D", "--Dport", type=int, required=True, help="Destination's port")
    parser.add_argument("-r", "--rfirst", type=bool, required=True, help="Receive first flag")

    args = parser.parse_args()

    proxy_Server(args.server, args.Sport, args.dest, args.Dport, args.rfirst)

if __name__ == "__main__":
    main()