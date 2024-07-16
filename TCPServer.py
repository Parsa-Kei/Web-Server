from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, timeout
from wsgiref.handlers import format_date_time
import time


serverPort = 8080
Socket = socket(AF_INET, SOCK_STREAM)
Socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
Socket.bind(('',serverPort))
Socket.listen(1)
print ('The server is listening')

currentTime = time.time()

while 1:
     try:
          connectionSocket, addr = Socket.accept()
          decodedRequest = connectionSocket.recv(1024).decode()
          request = decodedRequest.split("\n")[0].split()[0]
          print(request)
          if  (request != "GET" and request != "POST"):
               raise Exception("Wrong Header")
          headers = decodedRequest.split('\n')
          filename = decodedRequest[1].split()[0]
          if "If-Modified-Since" not in decodedRequest:
               allHeaders = decodedRequest.split('\n')
               filename = allHeaders[0].split()[1]
               filename = filename.lstrip('/')
               if filename == '':
                    filename = 'test.html'
               f = open(filename)
               content = f.read()
               f.close()
               response = 'HTTP/1.1 200 OK\n\n' + content

          elif headers[0].split()[1] == '/' and filename != '/test.html':
               header = 'HTTP/1.1 404 Not Found\n\n'
               f = open('404.html')
               content = f.read()
               f.close()
               response = header + content

          else:
               resTime = time.time()
               if resTime > currentTime + 1:
                    print ("EXCEPTION: 408")
                    print(addr)
                    header = 'HTTP/1.1 408 Request Timed Out\n\n'
                    f = open('408.html')
                    content = f.read()
                    f.close()
                    response = header + content
               else:
                    allHeaders = decodedRequest.split('\n')
                    filename = allHeaders[0].split()[1]
                    filename = filename.lstrip('/')
                    if filename == '':
                         filename = 'test.html'
                    f = open(filename)
                    content = f.read()
                    f.close()
                    response = 'HTTP/1.1 200 OK\n\n' + content

     except Exception as exception:
          print ("[EXCEPTION] 400")
          print (exception)  
          header = 'HTTP/1.1 400 Bad Request\n\n'
          f = open('400.html')
          content = f.read()
          f.close()
          response = header + content     
     connectionSocket.sendall(response.encode())
     connectionSocket.close()
