"""
Python process creation and associated tools of IPC and synchronization are defined in the standard module multiprocessing. 
Central to this module is the Process class defining the process abstraction along with its attributes and operations represented as methods. 
Process allows you to create a new process in your Python program via 2 methods:

    1- Implementing the algorithm that you need to execute as a function and passing its name along with its arguments to the constructor of Process, or
    2- Subclassing Process and defining its run() method to implement your algorithm.
"""


# Exemple of the 1st method
from multiprocessing import Process
 
def greet(name):
    print("Hello,", name, "!")
 
if __name__ == "__main__": #mandatory: ensures that certain code runs only when the script is executed directly, not when it's imported. 
    p = Process(target=greet, args=("Kitty",))
    p.start() #Start the process’s activity. This must be called at most once per process object. It arranges for the object’s run() method to be invoked in a separate process.
    p.join() #If the optional argument timeout is None (the default), the method blocks until the process whose join() method is called terminates. If timeout is a positive number, it blocks at most timeout seconds.

# Exemple of the 2nd method
from multiprocessing import Process
 
class Greet(Process):
    def __init__(self, name):
        super().__init__() #When you subclass the Process class, in your constructor you must first invoke the constructor of the parent class, hence the line super().__init__().
        self.name = name
    def run(self): #Method representing the process’s activity.
        print("Hello,", self.name, "!")
 
if __name__ == "__main__": #mandatory
    p = Greet("Kitty")
    p.start() #Start the process’s activity. This must be called at most once per process object. It arranges for the object’s run() method to be invoked in a separate process.
    p.join()
    p.join() #If the optional argument timeout is None (the default), the method blocks until the process whose join() method is called terminates. If timeout is a positive number, it blocks at most timeout seconds.





# To understand better the Process class, we will see the following example:
#!/usr/bin/env python
import os

# A very, very simple process.
if __name__ == "__main__":
    print(f"Hi! I'm process {os.getpid()}")
"""Will produce the following outcome:
Hi! I'm process 12345
"""



# Now, let's see the following example:
#!/usr/bin/env python
import os
import multiprocessing

def child_process():
    print(f"Hi! I'm a child process {os.getpid()}")

if __name__ == "__main__":
    print(f"Hi! I'm process {os.getpid()}")
    # Here we create a new instance of the Process class and assign our `child_process` function to be executed.
    process = multiprocessing.Process(target=child_process)
    # We then start the process
    process.start()
    # And finally, we join the process. This will make our script to hang and wait until the child process is done.
    process.join()
"""Will produce the following outcome:
[r0x0d@fedora ~]$ python /tmp/tmp.iuW2VAurGG/scratch.py
Hi! I'm process 144078
Hi! I'm a child process 144079

CAREFUL888 if you don't use the process.join() to wait for your child process to execute and finish,
then any other subsequent code that point will actually execute and may become a bit harder to synchronize your workflow.
"""



# Creating multiple chid processes: 
#!/usr/bin/env python
import os
import multiprocessing

def child_process(id):
    print(f"Hi! I'm a child process {os.getpid()} with id#{id}")

if __name__ == "__main__":
    print(f"Hi! I'm process {os.getpid()}")
    list_of_processes = []

    # Loop through the number 0 to 10 and create processes for each one of
    # them.
    for i in range(0, 10):
        # Here we create a new instance of the Process class and assign our
        # `child_process` function to be executed. Note the difference now that
        # we are using the `args` parameter now, this means that we can pass
        # down parameters to the function being executed as a child process.
        process = multiprocessing.Process(target=child_process, args=(i,))
        list_of_processes.append(process)

    for process in list_of_processes:
        # We then start the process
        process.start()

        # And finally, we join the process. This will make our script to hang
        # and wait until the child process is done.
        process.join()
"""Will produce the following outcome:
[r0x0d@fedora ~]$ python /tmp/tmp.iuW2VAurGG/scratch.py
Hi! I'm process 146056
Hi! I'm a child process 146057 with id#0
Hi! I'm a child process 146058 with id#1
Hi! I'm a child process 146059 with id#2
Hi! I'm a child process 146060 with id#3
Hi! I'm a child process 146061 with id#4
Hi! I'm a child process 146062 with id#5
Hi! I'm a child process 146063 with id#6
Hi! I'm a child process 146064 with id#7
Hi! I'm a child process 146065 with id#8
Hi! I'm a child process 146066 with id#9
"""





