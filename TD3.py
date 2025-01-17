# Ex1: Two-way ordinary pipes 
"""
Write a Python program to take advantage of the bidirectional nature of ordinary pipes for the following situation. 
A parent process prompts the user (you may use the built-in method input() for that) and reads a phrase from the terminal. 
It sends the phrase to its child process which reverses it and sends it back to its parent, the parent displays the reversed phrase. 
First, implement and test the program for a single round-trip communication, then extend it to accept an arbitrary number of communications with a stop phrase or word such as “end”. 
Always make sure to call the close() method on pipe connections once the program is done with them to release resources associated with Connection objects.
"""
import multiprocessing

def child_process(pipe):
    while True:
        # Receive phrase from parent
        phrase = pipe.recv()
        if phrase == "end":
            break
        # Reverse the phrase and send it back
        reversed_phrase = phrase[::-1]
        pipe.send(reversed_phrase)
    pipe.close()

if __name__ == "__main__":
    # Create a bidirectional pipe
    parent_pipe, child_pipe = multiprocessing.Pipe()
    
    # Start the child process
    process = multiprocessing.Process(target=child_process, args=(child_pipe,))
    process.start()
    
    while True:
        # Get input from user
        phrase = input("Enter a sentence (or type 'end' to stop): ")
        # Send the input to the child process
        parent_pipe.send(phrase)
        if phrase == "end":
            break
        # Receive the reversed phrase from the child process
        reversed_phrase = parent_pipe.recv()
        print(f"Reversed phrase: {reversed_phrase}")
    
    # Wait for the child process to finish
    process.join()
    # Close the pipe connections
    parent_pipe.close()
    child_pipe.close()









# Ex2: multi-client echo server 
"""
You have probably guessed that the above echo server does not handle simultaneous connections from multiple clients. 
In this exercise, you are required to extend the server code in order to make this possible so that every client is handled in a separate 
child process created by the server upon receiving an incoming client connection. Ideally, a much lighter multi-threaded model would be 
better suited for the required extension, but you are yet to discover threads !
"""


# Echo server
import socket
from multiprocessing import Process
 
HOST = "localhost"
PORT = 6666

def handle_client(client_socket, address):
    with client_socket:
        print("Connected to client: ", address)
        data = client_socket.recv(1024)
        while len(data):
            client_socket.sendall(data)
            data = client_socket.recv(1024)
        print("Disconnecting from client: ", address)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)                             # listen for more than 1 incoming connection
    print("Server is listening on port", PORT)
    while True:
        client_socket, address = server_socket.accept()
        print("Incoming connection from", address)
        # Create a new process to handle the client
        process = Process(target=handle_client, args=(client_socket, address))
        process.start()
        client_socket.close()  # Close the client socket in the parent process




