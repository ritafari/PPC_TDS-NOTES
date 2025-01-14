import os
import multiprocessing
import time
import signal

#EX1 - FIBONACCI SEQUENCE
"""
Write a Python program that that generates the Fibonacci sequence in the child process. 
The index of the sequence element will be provided at the command line. For example, if 5 is provided, the first six numbers in the Fibonacci sequence will be output by the child process. 
Because the parent and child processes have their own copies of data, it will be necessary for one of them, the child in this case, to output the sequence. 
Make sure that the parent waits for the child process to complete before exiting the program. You may either define a process class by inheriting from multiprocessing.
Process, or define a function and provide it as the target to be executed along with its parameter to multiprocessing.Process().
Put the child process to sleep via time.sleep(n) for n seconds and locate the entries of both processes in the output of the command ps ax, issued in another terminal. 
Call os.getpid() and os.getppid() in the appropriate places to check the process and parent process PIDs respectively and verify with the output of the ps command.
"""
def child_process(n):
    print(f"Child process started with PID {os.getpid()}, Parent PID {os.getppid()}")  #These calls will provide the process ID of the current process and its parent process, respectively. You should print these values from the child process to check them later using the ps ax command.
    print("Calculating Fibonacci sequence:")

    a, b = 0, 1
    for i in range(n):
        print(a)
        a, b = b, a + b

    print(f"Child process sleeping for {n} seconds...")
    time.sleep(n)                                       # you have to import time to use this function
    print("Child process finished.")

if __name__ == "__main__":
    n =int(input("Enter the number of terms for the Fibonacci sequence: "))

    #ensure the number entered is positive, ask until it is positive
    while n < 0:
        print("Please enter a positive number")
        n =int(input("Enter the number of terms for the Fibonacci sequence: "))
    
    if n==0:
        print("No terms to display")
    else:
        print(f"Main process PID: {os.getpid()}")
        process = multiprocessing.Process(target=child_process, args=(n,))
        process.start()
        process.join()
# CAREFUL! the child process had to output the Fibonacci sequence it generated because the parent and child have their own copies of data.





#EX2 - SIGNAL Exchange
"""
Write a Python program to implement the following scenario. A parent process creates a child and waits for its termination. 
After sleeping for 5 seconds, the child process sends a signal to its parent. Upon intercepting the signal, the parent kills its child. 
Make sure to use a user-available signal for child-parent communication. To send a signal to a process given its PID, you can call the method os.kill(). 
Have a look on its documentation.
"""
def child_process_sig():
    print(f"Child process started with PID {os.getpid()}, Parent PID {os.getppid()}")
    print("Child process sleeping for 5 seconds...")
    time.sleep(5)
    print("Child process sending signal to parent...")
    os.kill(os.getppid(), signal.SIGUSR1) #send signal to parent process, SIGUSR1/SIGUSR2 =  user-available signal for child-parent communication
    print("Child process finished.")

def signal_handler(sig, frame):
    print(f"Parent process received signal {sig}. Killing child process.")
    process.terminate()

if __name__ == "__main__":
    print(f"Main process PID: {os.getpid()}")
    process = multiprocessing.Process(target=child_process_sig)
    process.start()
    signal.signal(signal.SIGUSR1, signal_handler) #Allows you to specify a handler for a signal. When the signal is received, the handler is called with two arguments: the signal number and the current stack frame.
    process.join()
    print("Parent process finished.")

