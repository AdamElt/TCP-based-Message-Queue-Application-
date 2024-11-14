import socket
import sys

def producer_start(host, port):
    # Building on base template's socket setup
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.connect((host, port))
    print("Connected, producer")
    
    # Extended from base template's input loop
    while True:
        events = input()  # Kept original variable name from template
        if events:
            sc.send(events.encode())
            print(f"{len(events)} events are created")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Input must be python3 producer.py <host> <port>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    producer_start(host, port)