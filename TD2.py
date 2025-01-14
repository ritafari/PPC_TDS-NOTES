# EX1: Shared Memory - FIBONACCI RETURN
"""
In Exercise 1 from Session 1, the child process had to output the Fibonacci sequence it generated because 
the parent and child have their own copies of data. Another approach to designing this program is to establish 
a shared-memory object between the parent and child processes. This technique allows the child to write the contents 
of the sequence to the shared-memory object. The parent can then output the sequence when the child completes. 

Write a Python program to implement this scenario using either the direct shared memory approach or the manager approach. 
You can reuse parts of your solution for the previous exercise.
"""

from multiprocessing import Process, Manager
 
def gen_fibo(n, shared_list):
    """Function to generate Fibonacci sequence and store it in the shared list."""
    a, b = 0, 1
    for i in range(n):
        shared_list.append(a)
        a, b = b, a + b

def main():
    # Define the number of terms in the Fibonacci sequence
    n = int(input("Enter the number of terms for the Fibonacci sequence: "))

    # Create a Manager object to share data between processes
    with Manager() as manager:
        shared_list = manager.list()  # shared list

        # Create a child process to generate the Fibonacci sequence
        child_process = Process(target=gen_fibo, args=(n, shared_list))

        # Start and Join the child process 
        child_process.start() # parent process starts the child process
        child_process.join() # ensuring the child process completes with join(), the parent process accesses and outputs the contents of the shared list.

        # Parent process outputs the Fibonacci sequence 
        print("Fibonacci sequence by child process: ")
        print(list(shared_list))
        
if __name__ == '__main__':
    main()






# Ex2: Message Passing - Is it time yet?
"""
We’d like to implement a time server that creates a message queue and listens on it. 
It understands 2 types of messages, 1 and 2. Messages of type 1 are time requests. 
Upon receiving a time request, the server reads the system clock (see time.asctime()), 
and sends it into the queue as message type 3. A message of type 2 is a termination request. 
Upon receiving it, the server removes the message queue and terminates. 
The client program connects to the message queue, prompts the user for the message type to 
send to the server and communicates with the latter accordingly. Upon receiving a message from 
the server in response to a time request, it displays the message on the terminal. 
Implement the server and the client programs using the message passing facilities of the sysv_ipc module. Test with multiple clients.
"""

#server
import sysv_ipc
import time
 
key = 128
 
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

while True:
    #Receive a message from the queue 
    message, msg_type = mq.receive()
    
    if msg_type == 1:
        #Handle time request (type1)
        current_time = time.asctime()
        print(f"Time request received. Sending time: {current_time}")

        #Send the current time as a message with type 3
        mq.send(current_time.encode(), type=3)

    if msg_type == 2:
        #Handle termination request (type 2)
        print("Termination request received. Removing the messages from queue.")

        #Removing messages from queue
        mq.remove()
        
        #Terminating
        break


    


#client
import sysv_ipc
 
key = 128
 
mq = sysv_ipc.MessageQueue(key)

# Send a time request (message type 1)
mq.send(b"Requesting time", type=1)

message, msg_type = mq.receive() 
if msg_type == 3:
    print(f"Received time: {message.decode()}")

# Send a termination request (message type 2)
mq.send(b"Termination request", type=2)

