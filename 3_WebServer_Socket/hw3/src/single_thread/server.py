import socket
import os 

class HTTPServer:
    def __init__(self, host, port, verbose=False):
        self._host = host
        self._port = port 
        self._verbose = verbose

        if self._verbose:
            print(f"Server start work! list=({self._host}, {self._port})")


    def run(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            serverSocket.bind((self._host, self._port))
            serverSocket.listen()

            while True:
                clientSocket, addr = serverSocket.accept()
                if self._verbose:
                    print(f"Connect with client addr={addr}")

                try:
                    nameFile = self.parseRequest(clientSocket)
                except:
                    if self._verbose:
                        print("Пустой запрос от браузера!")
                    clientSocket.close()
                    continue

                # print(nameFile)
                response = self.createResponse(nameFile=nameFile)
                self.sendResponse(clientSocket=clientSocket,
                                    response=response)

                clientSocket.close()

        finally:
            serverSocket.close()
    
    def parseRequest(self, clientSocket):
        reqStr = clientSocket.recv(1024).decode("utf-8") 

        if len(reqStr) == 0:
            raise Exception('parseRequest, len(reqStr) == 0')
        # print(f"Len(req)={len(reqStr)}")
        if self._verbose:
            print(f"req={reqStr}")
        # print(reqStr)

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
            if self._verbose:
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


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 65432

    server = HTTPServer(host=HOST,
                        port=PORT,
                        verbose=True)
    
    server.run()