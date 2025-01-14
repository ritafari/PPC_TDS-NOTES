"""
The Python concurrent programming guidelines advice avoiding shared state between processes as much as possible. 
They suggest using pipes and queues (not to be confused with message queues both of which we’ll cover later) instead. 
The reason is that such shared state often has to be manually synchronized to guard against race conditions.

Ways to create and use shared data, the simplest of those are the classes Value and Array, 
defined in the multiprocessing module, which respectively represent scalar and fixed-size array data of predefined type, 
allocated from shared memory. The following program illustrates their use:
"""
from multiprocessing import Process, Value, Array #Value() and Array() are merely wrappers for the underlying data objects which have to be retrieved via the value attribute 
 
def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]
 
if __name__ == '__main__':
    number = Value('d', 0.0)        # 'd' indicates a double precision float
    vector = Array('i', range(10))  # 'i' indicates a signed integer.
    # Shared objects created by Value() and Array() are process and thread-safe by default.
    
    p = Process(target=f, args=(number, vector))
    p.start()
    p.join()
 
    print(number.value)
    print(vector[:])






"""
A second, more advanced way to create shared data is via Python managers,
Managers allow creating data which can be shared between different processes,
Managers support a host of process and thread-safe types such as list, dict
However, this mechanism is slower than Value and Array direct shared memory approach discussed above:
"""
from multiprocessing import Process, Manager
 
def f(d, l):
    d[1] = 'one'
    d['two'] = 2
    l.reverse()
 
if __name__ == '__main__':
    with Manager() as manager: 
    # A context manager: se crea una instancia del Manager que se asigna a la variable manager.
    # A declaración with asegura que el Manager se inicialice correctamente al entrar en el bloque de código y se cierre adecuadamente al salir del bloque
    # Esto es útil para evitar fugas de recursos y asegurar que todos los procesos y recursos asociados con el Manager se limpien correctamente.
        dct = manager.dict()
        lst = manager.list(range(10))
 
        p = Process(target=f, args=(dct, lst))
        p.start()
        p.join()
 
        print(dct)
        print(lst)
"""
Because shared memory segments created in a process are “inherited” by its children, 
it is most natural to use shared state for interprocess communication between processes in parent-child configuration. 
This is the paradigm supported by Value and Array direct shared memory objects and those created and managed by Manager. 
As mentioned in the above, it is still possible to define managers sharing objects between unrelated processes. 
"""







