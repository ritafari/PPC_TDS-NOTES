"""
Sockets are among the most widely used communication primitives. Within the same computer, other IPCs could be used and might be more efficient, 
but when it comes to cross-platform communication or to connecting machines over a network, sockets are often the only way to go.

Let’s first establish some background and terminology before jumping into technical details. A client socket is a two-way communication 
endpoint. A server socket behaves like a switchboard operator, it listens for incoming connections and produces a client socket upon receiving 
a connection from another client socket. After creating the client socket, the server socket goes back to listening. 
The two client sockets are free to communicate, they are identical structures as far as sockets are concerned, in other words, 
this is a peer-to-peer communication, and it is up to the designer to establish the exchange protocol. To illustrate, a client application, 
such as your browser, uses only client sockets, web servers it communicates with use both server and client sockets.

Under the hood, sockets are files, as such they possess a file descriptor known by the process that created them. 
A socket used for a TCP connection can be seen as a structure of 5 attributes:
the file descriptor of the socket
local_addr : a local address tuple (local_ip_address, port)
remote_addr: a remote address tuple (remote_ip_address, port)
the type of the socket (e.g. SOCK_STREAM)
the family of the socket (e.g. INET)

Several families and types of sockets exist. In this tutorial, we will address the INET family for communication over IPv4 using the SOCK_STREAM type for TCP connections. 
Other types of sockets do exist, SOCK_DIAG for instance is used for UDP connections. However, SOCK_STREAM sockets over IPv4 are the most common due to their better behavior and performance.
"""

# Socket creation is quite easy:
# The socket just created is not connected to anything yet, the local_addr tuple is set to default values and the remote_addr tuple does not exist. Two operations are now possible:
import socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# We can connect the socket to a host via a name or an IP address (e.g 45.231.12.6), thus creating a client socket :
my_socket.connect(("www.python.org", 80)) # which protocol port number is this ? ;-)

# Or, we can bind the socket to an address and have it listen for incoming messages, thus creating a server socket :
my_socket.bind(("localhost", 1312))
my_socket.listen(5)
client_socket, address = my_socket.accept()






# Echo server
import socket
 
HOST = "localhost"
PORT = 6666
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    client_socket, address = server_socket.accept()
    with client_socket:
        print("Connected to client: ", address)
        data = client_socket.recv(1024)
        while len(data):
            client_socket.sendall(data)
            data = client_socket.recv(1024)
        print("Disconnecting from client: ", address)




# client
import socket
 
HOST = "localhost"
PORT = 6666
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    m = input("message> ")
    while len(m):
        client_socket.sendall(m.encode())
        data = client_socket.recv(1024)
        print("echo> ", data.decode())
        m = input("message> ")
 


"""
Several points to note :

Sockets both on client and server side are created using context management, that is in a with statement. 
This makes sure that close() is called on the socket implicitly at the end of the with block to free underlying resources, 
even in the case of a premature termination of the program due to an error for example.

Communication is performed via socket methods recv(n) and sendall(data):
recv(n) : receives data from the socket returning a bytes object of length n at most
sendall(data) : send data, a bytes object, to a connected socket
When recv() returns a message of length 0, it indicates that the other side has closed the connection. In this example, client sockets are kept alive for communication. However many protocols, such as HTTP, use a socket for a single exchange. An HTTP client sends a request for a page, receives data detecting the end of transfer when it receives 0 bytes, then discards the communication socket.
Be aware that there is another commonly-used socket method to send data, send(data), which may end up not sending all data at once, especially with long messages on high-load systems. This method returns the number of bytes actually sent. Programs are responsible for checking that all data has been sent, and if not, they need to make sure that remaining data is delivered. For an illustration on how to use the send(data) method, have a look on the method MySocket.mysend defined in the Socket How-To.
By default, and unless otherwise specified, Python sockets are blocking, that is, the accept() method will block awaiting incoming connections and recv() will block if there is no data to read from the socket. We will address non-blocking sockets in session 5.
Run the server and client code in a pair of terminals. Can you connect a second client to the server while it is already communicating with a client ? Why ?
"""
