"""
The Python multiprocessing module provides ordinary (sometimes called unnamed) pipes to allow a pair of processes to communicate via the multiprocessing.Pipe() method. 
This method actually returns 2 multiprocessing.Connection objects connected through a pipe which is duplex (two-way) by default.

CAREFUL!!  though ordinary pipes are often used by a pair of process in a parent-child configuration, they could also be used between two child processes created by the same parent.
This is because file descriptors underlying Connection objects used to establish pipe communications are inherited in child processes.
Indeed, the child process is an exact duplicate of the parent process except for few things. 
"""
from multiprocessing import Process, Pipe

def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()    # The Pipe() function returns a pair of connection objects connected by a pipe which by default is duplex (two-way). 
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()