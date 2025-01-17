"""
PROCESS POOLS & DATA PARALLELISM
--------------------------------
Recall that the principal aim behind creating process and thread pools is to avoid the overhead of 
creating individual processes and threads and limiting their numbers thus improving the use of system resources. 
Python provides 2 APIs for process and thread pools:
1- the Pool class defined in the module multiprocessing for synchronous and asynchronous execution,
2- the concurrent.futures module providing both thread and process pools for asynchronous execution with identical API.

To summup: A Pool object manages a pool of worker processes. It allows for parallel execution of tasks and provides various methods for process-based parallelism. 

The Pool class represents a pool of worker processes. It has methods which allow tasks to be submitted to the worker processes in a few different ways. 
The fibonacci() function below returns a tuple consisting of the index it has received and the corresponding Fibonacci series element it has calculated. 
Notice that the Pool object is used in a context manager, that is, in a with ... as ... statement. 
"""
import time
import random
import multiprocessing
 
def fibonacci(n):
    print(multiprocessing.current_process().name)
    a, b = 0, 1
    i = 0
    while i < n:
        a, b = b, a+b
        i += 1
    return (n, a)
 
if __name__ == "__main__":
    indexes = [random.randint(0, 100) for i in range(10)] #Generates a list of 10 random integers between 0 and 100. These integers will serve as input for the fibonacci function in various multiprocessing operations.
 
    with multiprocessing.Pool(processes = 4) as pool:   #Creates a pool with 4 worker processes. The with statement ensures proper cleanup of the pool after execution.
        print("*** Synchronous call in one process")
        result = pool.apply(fibonacci, (10,))   #apply runs the fibonacci function in one of the worker processes. This call is synchronous, meaning the main program waits for the result before moving on.
        print(result)
 
        print("*** Asynchronous call in one process")
        result = pool.apply_async(fibonacci, (10,)) #apply_async also runs the fibonacci function in a worker process but does so asynchronously: The main program can continue executing while the worker processes the task. The result is accessed later using result.get().
        print(result.get())
 
        print("*** Synchronous map")
        for x in pool.map(fibonacci, indexes): # map distributes the indexes list across the worker processes, with each process handling one element at a time. It is synchronous, so the main program waits until all tasks are completed.
            print(x)
 
        print("*** Asynchronous map")
        for x in pool.map_async(fibonacci, indexes).get(): #Similar to above, but asynchronous.
            print(x)
 
        print("*** Deliberate timeout")
        result = pool.apply_async(time.sleep, (5,)) #Executes time.sleep(5) asynchronously.
                                                    #Attempts to retrieve the result with a timeout=1 seconds.
                                                    #Since the task takes longer than the timeout, this will raise a multiprocessing.TimeoutError.
        print(result.get(timeout=1))


"""
SUMMARY
Method	        Description	                                                                                 Blocking
apply	        Runs a function in a worker process and returns the result.	                                 Yes
apply_async	    Runs a function asynchronously and retrieves the result later with .get().	                 No
map	            Applies a function to all elements in an iterable, distributing the tasks among workers.	 Yes
map_async	    Similar to map, but asynchronous. Retrieve results with .get().	                             No
"""








"""
THREAD POOLS & TASK PARALLELISM
--------------------------------
The concurrent.futures module provides a ThreadPoolExecutor class for managing a pool of worker threads.
Everything that we mention about ThreadPoolExecutor also applies to ProcessPoolExecutor.

A ThreadPoolExecutor object can be instantiated with a maximum number of worker threads. Tasks can be submitted to a ThreadPoolExecutor object in two manners, 
either via its map() method which applies a function to iterables, or via its submit() method which schedules a function call and returns a Future object 
representing its execution. The following example illustrates both task submission methods through the above Fibonacci series generation example, this time 
implemented as a thread pool. Execute the example and peruse the documentation to make sure that you understand each of the ways in which the pool is used.
"""

import random
import concurrent.futures
 
def fibonacci(n):
    a, b = 0, 1
    i = 0
    while i < n:
        a, b = b, a+b
        i += 1
    return (n, a)
 
if __name__ == "__main__":
    indexes = [random.randint(0, 100) for i in range(10)]
 
    with concurrent.futures.ThreadPoolExecutor(max_workers = 3) as executor:    # Manages a pool of threads for concurrent execution of tasks. The max_workers parameter specifies the number of worker threads (3 in this case).
        print("Results returned via asynchronous map:")
        for result in executor.map(fibonacci, indexes):     #The map method distributes the elements of the indexes list to worker threads. Each thread runs the fibonacci function for one element.
                                                            #This call is blocking, meaning the main program waits for all threads to complete.
                                                            #The results are returned in the same order as the input indexes.
            print(result)
 
        print("Results returned as Future objects as they complete:")
        futures = [executor.submit(fibonacci, index) for index in indexes]      #Submit schedules the fibonacci function for execution and returns a Future object for each task.
                                                                                #These Future objects allow for asynchronous monitoring of the task’s status and retrieving results.
                                                                                #Tasks are executed in the order they are submitted, but as_completed retrieves results in the order tasks finish, which may differ.
                                                                                #The main program does not block while tasks execute; it processes results as they complete.
        for future in concurrent.futures.as_completed(futures):                 #as_completed returns an iterator that yields completed Future objects as they finish.
            print(future.result())

#Explanation of ThreadPoolExecutor
#The ThreadPoolExecutor is part of the concurrent.futures module and provides methods for managing thread-based parallelism. 


"""
Comparison of executor.map and submit/as_completed
---------------------------------------------------
Feature	                executor.map	                                                                submit with as_completed
Task                    Scheduling	Tasks are scheduled and executed in order of the input list.	    Tasks are submitted individually.
Result Retrieval	    Results are retrieved in the same order as inputs.	                            Results are retrieved as tasks complete.
Blocking	            Blocks until all tasks are completed.	                                        Non-blocking; can process results as they become available.
Use Case	            When the order of results matches input order is required.	                     When order of results doesn’t matter or early results are needed.


Summary of ThreadPoolExecutor Usage in Script
--------------------------------------------
Task Execution:
executor.map distributes tasks synchronously among threads.
submit allows asynchronous task execution, with results retrieved in completion order using as_completed.
Worker Threads:
Up to max_workers threads execute tasks concurrently.
Efficiency:
Suitable for lightweight or I/O-bound tasks.
This script showcases two powerful approaches to concurrent execution using ThreadPoolExecutor.
"""