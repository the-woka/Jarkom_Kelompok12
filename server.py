from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 9000

serverSocket.bind(('localhost', serverPort))

serverSocket.listen(1)

while True:
    print("Server is ready...")
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]

        f = open(filename[1:])

        outputdata = f.read()

        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n")

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i])
        connectionSocket.send("\r\n")

        connectionSocket.close()
    
    except IOError:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n")
        connectionSocket.send("<html><body><h1>404</h1><h3>File Not Found</h3></body></html>\r\n")

        connectionSocket.close()

serverSocket.close()