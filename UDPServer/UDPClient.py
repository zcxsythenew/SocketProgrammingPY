# TODO: 在这里指定循环次数
times = 10000

# TODO: 在这里指定发送的数据
message = 'LY!'

# TODO: 在这里指定服务器
serverName = '47.101.167.57'

from socket import *
import time

serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

for x in range(1, times + 1):
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    time.sleep(0.01)

clientSocket.close()