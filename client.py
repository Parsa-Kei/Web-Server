from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import email.utils
from datetime import date
host = "192.168.1.73"
port = 8080
# today = date.today()
# modified_time = email.utils.parsedate(today)
Socket = socket(AF_INET, SOCK_STREAM)
Socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
Socket.connect((host, port))
print("Sending GET request")
req = "GET / HTTP/1.1\n\n"
print(req)
Socket.send(req.encode())
data = Socket.recv(1024)
print(data.decode())
Socket.close()
Socket = socket(AF_INET, SOCK_STREAM)
Socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
Socket.connect((host, port))
print("Sending a conditional GET request")
req = "GET / HTTP/1.1\nIf-Modified-Since:  Sun, 04 Dec 2021 17:23:34 GMT\n\n"
print(req)
Socket.send(req.encode())
data = Socket.recv(1024)
print(data.decode())
Socket.close()
Socket = socket(AF_INET, SOCK_STREAM)
Socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
Socket.connect((host, port))
print("Sending a GET request")
req = "Header: Hello \n\n"
print(req)
Socket.send(req.encode())
data = Socket.recv(1024)
print(data.decode())
Socket.close()
Socket = socket(AF_INET, SOCK_STREAM)
Socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
Socket.connect((host, port))
print("Sending a GET request")
req = "GET /abc.txt HTTP/1.1\n\n"
print(req)
Socket.send(req.encode())
data = Socket.recv(1024)
print(data.decode())
Socket.close()

