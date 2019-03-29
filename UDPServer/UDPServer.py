# 该脚本将接收UDP数据，并在屏幕上显示收到的个数
# 用 Ctrl+C 终止

from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
num = 1
print('The server is ready to receive')
while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    serverSocket.sendto(num.to_bytes(4, 'big'), clientAddress)
    print(num)
    num = num + 1