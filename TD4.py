# EX1: How much is π ?
"""
A classic approach to estimate π is using the Monte Carlo method which involves randomization. 
This works as follows. Frist, assume a circle of radius equal to 1, inscribed within a square and 
centered on the origin of the Cartesian plane as in the figure above. Next, generate a series of 
random points (x,y) which fall within the coordinates of the square. Some of the generated points will occur within the circle. 
Then π is estimated by:

    π=4×(number of points in circle)/(total number of points)

Write a multithreaded program that creates a separate thread to generate a number of random points. 
The thread will count the number of points that occur within the circle and store the result in a global variable. 
When this thread exits, the main thread will calculate and output the estimated value of π. 
Experiment with the number of random points generated.

Hints:
- To assert that a point (x,y) falls within a circle of radius R, it suffices that x2+y2<=R.
- You can generate random real numbers falling into the interval [0,1) via random.random()
"""

import random
import threading

# Global variables
points_in_circle = 0
total_points = 1000000  # Adjust this value to experiment
lock = threading.Lock() # Lock to ensure thread-safety, synchronize access to shared data

def generate_points():
    global points_in_circle
    for _ in range(total_points):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1:
            with lock:  # Ensure thread-safety
                points_in_circle += 1

def main():
    # Create a thread for point generation
    worker_thread = threading.Thread(target=generate_points)
    # Start the thread
    worker_thread.start()
    # Wait for the thread to complete
    worker_thread.join()
    # Estimate π
    pi_estimate = 4 * points_in_circle / total_points
    print(f"Estimated value of π: {pi_estimate}")

if __name__ == "__main__":
    main()




# EX2: the INSEE office
"""
We would like to calculate the following statistics on numeric data: min, max, median, mean and standard deviation. 
Write a multithreaded program where the main thread creates a number of workers equal to the number of statistics to perform, 
reads data from the terminal and signals data availability to its workers which proceed to calculate and display statistics. 
Do not define 5 different functions to be executed in worker threads, define a single worker function and pass operations as 
function object elements of a queue.Queue argument.


Hints:
- To calculate statistics, use built-in functions min and max, and statistics module functions median, mean and stdev.
- Every thread displays the result of its computation. You may also choose to return computation results to the main thread in a second queue.Queue. In your initial solution, opt for displaying the calculated statistic in the worker thread.
- To read data from the standard input until end-of-file (EOF) is encountered (Ctrl+D on Unix/Linux, Ctrl+Z on Windows), you can use the following code snippet.

data = []
input_str = sys.stdin.read().split()
for s in input_str:
    try:
        x = float(s)
    except ValueError:
        print("bad number", s)
    else:
        data.append(x)    
"""

import sys
import threading
from queue import Queue
import statistics


def worker(data_queue, operation):
    """
    Worker thread function to calculate a statistic from the data.
    - Reads data from the queue.
    - Applies the given operation.
    - Displays the result.
    """
    while True:
        data = data_queue.get()
        if data is None:  # Sentinel value to stop the worker
            break
        result = operation(data)
        print(f"{operation.__name__.capitalize()}: {result}")
        data_queue.task_done()


def stat_main():
    # Read data from standard input
    data = []
    input_str = sys.stdin.read().split()
    for s in input_str:
        try:
            x = float(s)
        except ValueError:
            print(f"bad number: {s}")
        else:
            data.append(x)
    
    # If no valid data is entered, exit early
    if not data:
        print("No valid data entered.")
        return

    # Create a queue to store the data for workers
    data_queue = Queue()

    # List of operations
    operations = [min, max, statistics.median, statistics.mean, statistics.stdev]

    # Create and start a thread for each operation
    threads = []
    for operation in operations:
        thread = threading.Thread(target=worker, args=(data_queue, operation))
        thread.start()
        threads.append(thread)

    # Put the data in the queue for workers
    data_queue.put(data)

    # Wait for workers to finish processing the data
    data_queue.join()

    # Stop all workers by putting None (sentinel) in the queue
    for _ in threads:
        data_queue.put(None)

    # Wait for all threads to terminate
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    stat_main()






