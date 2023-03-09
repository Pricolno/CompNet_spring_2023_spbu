import socket
import os
import sys 


class HTTPClient:
    
    def __init__(self, host, port, nameFile,
                isSave=False,
                verbose=False,
                verboseData=False):
        self._host = host
        self._port = port 
        self._nameFile = nameFile
        self._isSave = isSave

        self._pathToClientData = "clientData"
        
        self._verbose = verbose
        self._verboseData = verboseData
        if self._verbose:
            print(f"Client start work! connect to=({self._host}, {self._port})")

    def getRequest(self):
        req = f"GET /{self._nameFile} HTTP/1.1\r\n"
        return req

    def getPathToSave(self):
        # res = os.path.join(self._pathToClientData, self._nameFile)
        curDir = os.path.dirname(os.path.abspath(__file__))
        nameFile = self._nameFile.split('/')[-1]
        res = os.path.join(curDir, self._pathToClientData, nameFile).replace("\\","/")
        print(res)
        return res
    

    def parseResponse(self, resp):
        respList = resp.split('\r\n')
        body = ""
        if len(respList) > 3:
            body = "\r\n".join(respList[3:])
        return body

    def run(self):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((self._host, self._port))

        clientSocket.sendall(self.getRequest().encode())
        try:
            resp = clientSocket.recv(10024)
            if self._isSave:
                with open(self.getPathToSave(), 'wb') as f:
                    body = self.parseResponse(resp.decode())
                    f.write(body.encode())
                    print(f"Запрашиваемые данные скачались в {self.getPathToSave()}")
            
            print(f"Запрашиваемые данные=\n{resp.decode()}")
        except Exception as e:
            if self._verbose:
                print(f"Не получилось получить данные :( error=\n{e}")


# py .\client.py 127.0.0.1 65432 data/hello.html

if __name__ == "__main__":
    # HOST = "127.0.0.1"
    # PORT = 65432
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    nameFile = sys.argv[3]
    client = HTTPClient(host=HOST,
                        port=PORT,
                        nameFile=nameFile,
                        isSave=True,
                        verbose=True)
    
    client.run()