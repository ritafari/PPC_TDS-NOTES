#EX1: Prime or not?

"""
We’d like to carry out a primality test on a large number of relatively large integers. A process pool would be ideal for such CPU-bound tasks. 
Write a Python program that generates a number of random integers in the range [103,106] the primality of which is tested by worker processes in a multiprocessing.Pool. 
Submit tasks to the pool by at least one synchronous and one asynchronous method. Experiment with the number of worker processes and the number of generated integers. 
Try to measure execution times of pool calls by calculating the elapsed time in the following manner:

import time
start = time.time()
# some code
end = time.time()
seconds = end - start

Avoid input and output operations (i.e. input() and print()) in execution time measurements. For the primality test itself, you can use the following code:

import math
def is_prime(n):
    if n < 2:
        return (n, False)
    if n == 2:
        return (n, True)
    if n % 2 == 0:
        return (n, False)
 
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return (n, False)
    return (n, True)
"""

import time
import math
import random
import multiprocessing
 
def is_prime(n):
    if n < 2:
        return (n, False)
    if n == 2:
        return (n, True)
    if n % 2 == 0:
        return (n, False)
 
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return (n, False)
    return (n, True)

if __name__ == "__main__":
    indexes = [random.randint(103, 106) for i in range(3)]
 
    with multiprocessing.Pool(processes = 4) as pool:
        start = time.time()
        print("*** Synchronous call in one process")
        result = pool.apply(is_prime, (3,))
        print(result)
 
        print("*** Asynchronous call in one process")
        result = pool.apply_async(is_prime, (3,))
        print(result.get())
 
        print("*** Synchronous map")
        for x in pool.map(is_prime, indexes):
            print(x)
 
        print("*** Asynchronous map")
        for x in pool.map_async(is_prime, indexes).get():
            print(x)
 
        print("*** Deliberate timeout")
        result = pool.apply_async(time.sleep, (5,))

        end = time.time()
        seconds = end - start
        print("Elapsed time: ", seconds)











#EX2: What time is it, again? 
"""
In Exercise 2 of Session 2, we designed client-server programs around System V-style message passing to request and serve current date and time. Both programs were single threaded. What this means for the server in particular, 
is that it cannot serve (read current date/time from system, create and send message) multiple clients at the same time. In this exercise, you will develop the previous server solution so that it handles every client date/time request in a separate thread.

We will tackle this exercise following either the message passing route, or using sockets. You may choose one strategy and leave your partner follow the other so that both strategies are addressed by your team !
"""

#1. Message passing solution
#Client code
import os
import sys
import time
import sysv_ipc
 
key = 666
 
def user():
    answer = 3
    while answer not in [1, 2]:
        print("1. to get current date/time")
        print("2. to terminate time server")
        answer = int(input())
    return answer
 
try:
    mq = sysv_ipc.MessageQueue(key)
except ExistentialError:
    print("Cannot connect to message queue", key, ", terminating.")
    sys.exit(1)
 
t = user()
 
if t == 1:
    pid = os.getpid()
    m = str(pid).encode()
    mq.send(m)
    m, t = mq.receive(type = (pid + 3))
    dt = m.decode()
    print("Server response:", dt)
 
if t == 2:
    m = b""
    mq.send(m, type = 2)
    

#2. Socket solution
#Here’s the code for the client to be used in the socket-based strategy:
import sys
import socket
 
def user():
    answer = 3
    while answer not in [1, 2]:
        print("1. to get current date/time")
        print("2. to terminate time server")
        answer = int(input())
    return answer
 
HOST = "localhost"
PORT = 1789
 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    m = user()
    if m == 1:
        client_socket.send(b"1")
        resp = client_socket.recv(1024)
        if not len(resp):
            print("The socket connection has been closed!")
            sys.exit(1)
        print("Server response:", resp.decode())
    if m == 2:
        client_socket.send(b"2")
 


"""
You are required to develop a socket-based time server that uses a thread pool which services date/time and server termination requests from multiple clients. 
For a proper server termination, you can maintain a global boolean variable to loop on, accepting and servicing incoming connections inside the loop, and set it to 
False when a termination request arrives. Using a non-blocking server socket is necessary in order not to block on the accept call. Here’s a code skeleton to get you started:
"""

"""
import select
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
 
serve = True

# thread handler definitions
 
# socket creation
HOST = "localhost"
PORT = 1789
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

server_socket.setblocking(False)

# Create a thread pool with a specified number of workers
thread_pool = ThreadPoolExecutor(max_workers=4)

 
while serve:
    # very short, 1 second timeout
    readable, writable, error = select.select([server_socket], [], [], 1)
    if server_socket in readable: # if server_socket is ready
        client_socket, address = server_socket.accept() # will return immediately
        # submit request to thread pool
"""


import select
import socket
from concurrent.futures import ThreadPoolExecutor

# Global variable to control the server's main loop
serve = True

def handle_client(client_socket):
    """
    Handles client requests: either provides date/time or terminates the server.
    """
    global serve
    with client_socket:
        try:
            # Receive the client's request
            request = client_socket.recv(1024).decode('utf-8').strip()
            print(f"Received request: {request}")

            if request.lower() == "time":
                # Respond with the current date/time
                from datetime import datetime
                response = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                client_socket.sendall(response.encode('utf-8'))
            elif request.lower() == "terminate":
                # Signal the server to stop and respond to the client
                serve = False
                response = "Server is shutting down..."
                client_socket.sendall(response.encode('utf-8'))
                print("Termination request received. Shutting down server.")
            else:
                # Handle invalid requests
                response = "Invalid request. Use 'time' or 'terminate'."
                client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error handling client: {e}")

# Server configuration
HOST = "localhost"
PORT = 1789

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    server_socket.setblocking(False)  # Non-blocking mode

    print(f"Time server is running on {HOST}:{PORT}...")

    # Create a thread pool to handle client requests
    thread_pool = ThreadPoolExecutor(max_workers=4)

    try:
        while serve:
            # Use select to monitor the server socket
            readable, _, _ = select.select([server_socket], [], [], 1)
            if server_socket in readable:  # New client connection
                client_socket, address = server_socket.accept()
                print(f"Connection established with {address}")
                # Submit the client handler to the thread pool
                thread_pool.submit(handle_client, client_socket)
    except KeyboardInterrupt:
        print("\nServer interrupted by user. Shutting down.")
    finally:
        # Clean up
        thread_pool.shutdown(wait=True)
        print("Server shut down gracefully.")
