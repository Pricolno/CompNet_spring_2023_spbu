import socket
import os 
import threading
from queue import Queue
import sys

import time

class HTTPServer:
    def __init__(self, host, port, concurrencyLevel,
                  verbose=False,
                  verboseData=False):
        self._host = host
        self._port = port 
        self._concurrencyLevel = concurrencyLevel
        self._verbose = verbose
        self._verboseData = verboseData
        self._q = Queue()
        if self._verbose:
            print(f"Server start work! list=({self._host}, {self._port})")


    def run(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            serverSocket.bind((self._host, self._port))
            serverSocket.listen()

            serverSocket.setblocking(False)

            while True:
                clientSocket, addr = None, None
                try:
                    clientSocket, addr = serverSocket.accept()
                    clientSocket.setblocking(False)
                    self._q.put((clientSocket, addr))
                    if self._verbose:
                        print(f"Connect with client addr={addr}")
                except BlockingIOError:
                    # Нету соединений
                    pass
                    

                if not self._q.empty() and threading.active_count() < self._concurrencyLevel:
                    curClientSocket, addr = self._q.get()
                    # self.processClient(curClientSocket)
                    
                    curThread = threading.Thread(target=self.processClient, args=(curClientSocket, addr))
                    curThread.start()
                else:
                    if self._verbose and addr is not None:
                        print(f"Для запроса от (ip, addr)={addr} нету места. Ждёт своей очереди. \
Активны {threading.active_count()} / {self._concurrencyLevel}. \
В очереди {self._q.qsize()}.")

        finally:
            serverSocket.close()
    
    def processClient(self, clientSocket, addr):
        if self._verbose:
            print(f"Запрос от (ip, addr)={addr} принят на обработку. \
Активны {threading.active_count()} / {self._concurrencyLevel}. \
В очереди {self._q.qsize()}.")

        time.sleep(3)
        try:
            nameFile = self.parseRequest(clientSocket, addr)

            response = self.createResponse(nameFile=nameFile)
            self.sendResponse(clientSocket=clientSocket,
                                response=response)

        except:
            if self._verbose:
                print("Пустой запрос от браузера!")
            
        if self._verbose:
            print(f"Запрос от (ip, addr)={addr} выполнен! \
Активны {threading.active_count() - 1} / {self._concurrencyLevel}. \
В очереди {self._q.qsize()}.")
        clientSocket.close()



    def parseRequest(self, clientSocket, addr):
        try:
            reqStr = clientSocket.recv(1024).decode("utf-8") 
        except ConnectionError:
            print(f"Client suddenly closed while receiving from {addr}")
            clientSocket.close()
            return None
        except BlockingIOError:
            # No data received
            pass
            
            

        if len(reqStr) == 0:
            raise Exception('parseRequest, len(reqStr) == 0')
        if self._verboseData:
            print(f"req={reqStr}")

        reqList = reqStr.split("\r\n")  

        if len(reqList) < 2:
            raise Exception("Not GET HTTP request! (len(reqList) < 2)")
    
        reqGet = reqList[0].split(' ')
        typeReq = reqGet[0]

        if typeReq != "GET":
            raise Exception('Not GET HTTP request! (len(typeReq) != "GET")')
        nameFile = reqGet[1]

        return nameFile

    def createResponse(self, nameFile):
        # content_type = 'text/plain; charset=utf-8'
        content_type = 'text/html; charset=utf-8'
        
        nameFile = nameFile[1:]
        curDir = os.path.dirname(os.path.abspath(__file__))
        pathToFile = os.path.join( 
            curDir,
            nameFile
        )          
        # print(f"pathToFile={pathToFile}")
        if os.path.exists(pathToFile):
            file = open(nameFile, mode='rb')
            body = file.read()
            file.close()

            status, statusStr = 200, 'OK'
            headers = {'Content-Type': content_type,
                        'Content-Length': len(body)
                        }
            response = {
                'status' : status,
                'statusStr' : statusStr,
                'headers' : headers,
                'body' : body
            }
            return response
        else:
            status, statusStr = 404, 'Not found'
            body = b'404 Not Found'
            headers = {'Content-Type': content_type,
                        'Content-Length': len(body)
                        }
            response = {
                'status' : status,
                'statusStr' : statusStr,
                'headers' : headers,
                'body' : body
            }
            return response

    def sendResponse(self, clientSocket, response):
        socketFile = clientSocket.makefile('wb')
        # send status
        statusRaw = f"HTTP/1.1 {response['status']} {response['statusStr']}"
        socketFile.write(statusRaw.encode())
        socketFile.write(b'\r\n')

        # send header
        if 'headers' in response:
            if self._verboseData:
                print(f"Response={response['headers']}")
            for key, value in response['headers'].items():
                headerRaw =  f'{key}: {value}\r\n'
                socketFile.write(headerRaw.encode())
        socketFile.write(b'\r\n')

        # send body
        if 'body' in response:
            socketFile.write(response['body'])
        
        socketFile.flush()
        socketFile.close()  

# py .\server.py 127.0.0.1 65432

if __name__ == "__main__":
    # HOST = "127.0.0.1"
    # PORT = 65432
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    server = HTTPServer(host=HOST,
                        port=PORT,
                        concurrencyLevel=3,
                        verbose=True)
    
    server.run()