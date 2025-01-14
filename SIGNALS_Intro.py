"""Signals are a useful means for asynchronous communication with processes, and often for interprocess communication as well
Signals are a way to send notifications to a process given its PID. They are used to notify a process that a particular event has occurred.
Careful: signals are available on Unix-like systems only.

SIGTERM is sent to a process to request its proper termination, 
SIGKILL kills a process immediately without allowing it to cleanup its resources, 
SIGINT delivers a keyboard interrupt, an so on. 
Some signals, such as SIGUSR1 and SIGUSR2, are available for users to implement an application-dependent behavior.
"""

# start simple: run those two lines in a terminal
#while True:
#  pass
# and then, in another terminal, run this command
#ps ax
#PID is 21735
#Send a SIGKILL signal to the process with the PID 21735: kill -s SIGKILL 21735




"""You can intercept a signal and decide what to do upon its arrival by defining a signal handler function.
You then install this signal handler for the given signal.
"""
#Let’s develop the above simple program to intercept SIGINT and print a smiley face instead of terminating the program, which is the default behavior upon receiving the signal. The code follows.
import signal
 
def handler(sig, frame):        #A signal handler function can be installed for a given signal via the signal.signal() method. This method can also be used to ignore a signal or to redefine its default behavior. 
    if sig == signal.SIGINT:
        print("}:-)")
 
signal.signal(signal.SIGINT, handler)
 
while True:
    pass


"""a process must be alive for it to be able to receive a signal!!!!!
Without the while loop, the process would have terminated without having the chance of receiving a signal.
"""

