"""
Recall that threads are separate execution paths within a single process. 
As such, they share program code, data and external resources, such as open files. 
Also recall that CPython, the reference and most widely-used Python implementation, 
uses a global interpreter lock (GIL) the consequence of which is that only one thread can 
execute Python code at a time, that is, Python threads run concurrently and not in parallel.

To sum up, the usual use case for threads is to improve the responsiveness of especially user-facing applications by running tasks, 
usually IO, in the background. It is not uncommon to design complex programs as multiple processes some multi others single-threaded 
with interprocess communication (IPC).

The abstraction representing a thread is the threading.Thread class which, similarly to multiprocessing.
Process, allows you to create a new thread in your Python program either by:
    - Subclassing the class and overriding the run() method
    - Passing a callable to the constructor simply by creating a threading.Thread object  
"""

#To illustrate the use of threading.Thread, here’s a multithreaded solution of the Fibonacci series generation exercise from Session 1 (without error checking).
import sys
import threading

def fibonacci(n):
    print("Starting thread:", threading.current_thread().name)
    res = [0]
    a, b = 0, 1
    i = 0
    while i < n:
        a, b = b, a+b
        res.append(a)
        i += 1
    print(res)
    print("Ending thread:", threading.current_thread().name)

if __name__ == "__main__":
    print("Starting thread:", threading.current_thread().name)
    index = int(sys.argv[1])
    thread = threading.Thread(target=fibonacci, args=(index,))
    thread.start()
    thread.join()
    print("Ending thread:", threading.current_thread().name)                







"""
TASK PARALLELISM IN THREADS

Recall that task parallelism involves distributing operations across multiple workers (threads or processes), 
each performing a unique operation on often the same data. In contrast, data parallelism distributes subsets 
of data across multiple workers each performing the same operation. In practice, however, few applications strictly 
follow either data or task parallelism. In most cases, a hybrid of these two strategies is used.

For the purposes of the following exercise, we shall look at the simplest of these synchronization tools, the Event class 
which allows for a thread to signal the occurrence of an event for other threads waiting for it.

The queue standard module provides thread-safe queue objects with similar API and patterns of use to the multiprocessing.
Queue class we encountered during session 2. You may want to review that information to refresh your memory. 

The following program illustrates the use of both Event and Queue objects. A main thread creates a worker thread which waits on an event object. 
Next, the main thread reads some data from the standard input and puts it in the queue. Once data is available, the main thread signals the event 
allowing the worker thread to proceed with reading it from the queue:
"""

import threading
from queue import Queue

def worker(queue, data_ready):
    print("Starting thread:", threading.current_thread().name)    
    data_ready.wait()
    value = queue.get()
    print("got value:", value)
    print("Ending thread:", threading.current_thread().name)

if __name__ == "__main__":   
    print("Starting thread:", threading.current_thread().name)

    queue = Queue()
    data_ready = threading.Event()

    thread = threading.Thread(target=worker, args=(queue, data_ready))
    thread.start()

    value = input("give me some value:")
    queue.put(value)
    data_ready.set()

    thread.join()

    print("Ending thread:", threading.current_thread().name)
