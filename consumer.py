import socket
import sys
import time

def consumer_start(host, port):
    # Building on base template's socket setup
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.connect((host, port))
    print("Connected, consumer")
    
    # Extended from base template's receive loop
    while True:
        try:
            msg = sc.recv(1024).decode()  # Kept original variable name from template
            print(msg)
            time.sleep(1)  # Maintained from template
        except:
            break
    sc.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Input must be python3 consumer.py <host> <port>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    consumer_start(host, port)