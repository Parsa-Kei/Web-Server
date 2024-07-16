from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, timeout
import threading
import time
from wsgiref.handlers import format_date_time


def sendThread(connectionSocket, req, addr):
#     print("[THREAD] starting send thread")
     currentTime = time.time()
     try:
          request = req.split("\n")[0].split()[0]
          if  (request != "GET"):
               raise Exception("Wrong Header")
          headers = req.split('\n')
          filename = req[1].split()[0]
          if "If-Modified-Since" not in req:
               allHeaders = req.split('\n')
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
                    allHeaders = req.split('\n')
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


threads = []
serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while 1:
     connectionSocket, addr = serverSocket.accept()
     print("[Receive] Connection Received")
     req = connectionSocket.recv(1024).decode()
     if(len(threads) > 4):
          print("Thread capacity is full other threads must finish before proceeding.")
          threads[0].join()
     newThread = threading.Thread(target=sendThread, args=[connectionSocket, req, addr])
     print("Creating new thread " + newThread.name)
     threads.append(newThread)
     newThread.start()