import socket
import sys
import time
from threading import Thread
from queue import Queue

consumers = {}
consumer_count = 0
event_queue = Queue()

def producer_worker(connection): # Connect to producer and receive user input. Decode and put in queue
    global event_queue
    while True:
        data = connection.recv(1024)
        if not data:
            break
        message = data.decode()
        for char in message:
            event_queue.put(char)
        print("[Events created]")
        print(f"[Remaining events: {event_queue.qsize()}]")
    connection.close()

def consumer_worker(connection, consumer_id): # Connect to consumer
    global consumers, event_queue
    print(f"[consumer {consumer_id} connected]")
    consumers[consumer_id] = connection
    print(f"[{len(consumers)} consumers online]")
    
    while True:
        if not event_queue.empty(): #if the queue has char's state which consumer is decoding and -- queue size.
            message = event_queue.get()
            connection.send(f"Event {message} is processed in consumer {consumer_id}".encode())
            print(f"[Remain events: {event_queue.qsize()}]")
            time.sleep(1)
        else: 
            connection.send("No event in queue".encode())
            time.sleep(1)


def start_server(host, prod_port, cons_port):
    # Producer socket
    producer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    producer_socket.bind((host, prod_port))
    producer_socket.listen(5)
    
    # Consumer socket
    consumer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    consumer_socket.bind((host, cons_port))
    consumer_socket.listen(5)
    
    def accept_producers():
        while True:
            conn, addr = producer_socket.accept()
            print("[Producer connected]")
            producer_thread = Thread(target=producer_worker, args=(conn,))
            producer_thread.start()
    
    def accept_consumers():
        global consumer_count
        while True:
            conn, addr = consumer_socket.accept()
            consumer_count += 1
            worker_thread = Thread(target=consumer_worker, args=(conn, consumer_count))
            worker_thread.start()
    
    Thread(target=accept_producers).start()
    Thread(target=accept_consumers).start()

if __name__ == '__main__': # Accept arguments and reecord ports for the producer and consumer. 
    if len(sys.argv) != 4:
        print("Input must be python3 server.py <host> <producer_port> <consumer_port>")
        sys.exit(1)
    host = sys.argv[1]
    prod_port = int(sys.argv[2])
    cons_port = int(sys.argv[3])
    start_server(host, prod_port, cons_port)