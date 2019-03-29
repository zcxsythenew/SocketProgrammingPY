# TODO: 在这里指定循环次数
times = 100

# TODO: 在这里指定发送的数据
message = 'LY!'

from socket import *
serverName = '192.168.56.101'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

for x in range(1, times + 1):
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(int.from_bytes(modifiedMessage, 'big'))

clientSocket.close()