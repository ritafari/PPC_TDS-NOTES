"""
The multiprocessing.Queue class implements a First-In-First-Out process-safe queue intended for exchanging objects between multiple processes.
multiprocessing.Queue objects are typically used to feed data and tasks (often represented as callables) to a collection of worker processes and to collect results.

Let us turn our attention now to message queues. To illustrate their use, we shall use the following minimal example. An independent process, called the server, 
creates a message queue then reads integers from the terminal sending them into the message queue until zero (0) is read, at which point the server stops input, 
removes the message queue, and terminates. A second independent process, called the client, connects to the message queue created by the server, receives integers 
sent by the latter displaying them on the terminal until it encounters zero (0), at which point it terminates.
"""

# The source code of the server program
import sysv_ipc
 
key = 128
 
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
 
value = 1   #associate integer identifiers with messages, referred to as message types. This allows us to retrieve specific messages from the queue. 
            #If unspecified upon sending, the message type defaults to 1. 
while value:
    try:
        value = int(input())
    except:
        print("Input error, try again!")
    message = str(value).encode()   # encode() method on str objects to convert from str to bytes.
    mq.send(message)    # objects of type bytes.
 
mq.remove()


# And that of the client program.
import sysv_ipc
 
key = 128
 
mq = sysv_ipc.MessageQueue(key)
 
while True:
    message, t = mq.receive()   # objects of type bytes.
    value = message.decode()    # A bytes object converted to str
    value = int(value)          # If unspecified upon receiving, the message type defaults to 0, which translates to retrieving the first message on the queue.
    if value:
        print("received:", value)
    else:
        print("exiting.")
        break

"""
Go ahead and run the two programs in 2 separate terminals. 
Launch a third terminal and issue the command ipcs. 
Examine its output and find the section that lists message queues. 
You should be able to locate the active message queue by its key. 
If something goes wrong and the server program crashes before it had the opportunity to remove the queue, 
you can do that manually by issuing the command ipcrm -Q key, where key is the key that was used to create the message queue in question.
"""




