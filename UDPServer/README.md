# 编写程序

## 发送端程序

发送端程序的主要任务是将数据向服务端发送若干次。

尽管我们可以使用C、C++、Java等语言编写Socket程序，但是Python更简洁，并且可以使人更关注网络编程的内容而非编程语言的内容。

以下是Python代码，相应的C++代码及解释位于文末附录。

``` Python
# TODO: 在这里指定循环次数
times = 100

# TODO: 在这里指定发送的数据
message = 'LY!'

# TODO: 在这里指定服务器的地址
serverName = '192.168.60.3'

from socket import *
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

for x in range(0, times):
    clientSocket.sendto(message, (serverName, serverPort))

clientSocket.close()
```

该程序的流程图如下：

```mermaid
flowchat
st=>start: 开始
e=>end: 结束
A=>operation: 定义接收地址和端口
B=>operation: x = 0
C=>operation: 创建套接字
D=>operation: 发送数据
E=>operation: x = x + 1
F=>condition: x = 100?

st->A->B->C->D->E->F
F(yes)->e
F(no)->D
```

下面是对这个程序各个函数的详细说明：

``` Python
clientSocket = socket(AF_INET, SOCK_DGRAM)
```

`socket`函数创建了一个套接字，指明使用的协议组。第一个参数`AF_INET`表示用于IPv4下的网络通信。第二个参数`SOCK_DGRAM`表示数据报式、无连接、定长、不可靠，用于UDP通信。在创建套接字时，并没有指定发送端的端口号，因为这个工作是由操作系统负责的。

``` Python
clientSocket.sendto(message.encode(), (serverName, serverPort))
```

`encode`函数将字符串编码为二进制信息。`sendto`函数将发送目标名（IP地址）、发送目标端口号“贴”在要发送的信息上，然后就将信息发送出去了。

Python中的`sendto`函数接收2~3个参数，其中第2个参数（`flag`）可省略。第1个参数（`data`）接收`bytes`类型的数据，第3个参数（`address`）接收由服务器名、服务器端口组成的元组（`tuple`）。

``` Python
clientSocket.close()
```

`close`函数将套接字关闭，从而进程不能再向网络发送或从网络接收数据。

## 接收端程序

接收端程序的主要任务是接收数据，每收到1个数据包就将累计收到的数字显示在屏幕上。

尽管我们可以使用C、C++、Java等语言编写Socket程序，但是Python更简洁，并且可以使人更关注网络编程的内容而非编程语言的内容。

以下是Python代码，相应的C++代码及解释位于文末附录。

``` Python
from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
num = 1
print('The server is ready to receive')
while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    print(num)
    num = num + 1
```

这个程序是一个死循环程序，直到用户强制将它停止为止。该程序的流程图如下：

```mermaid
flowchat
st=>start: 开始
e=>end: 结束
A=>operation: 定义接收地址和端口
B=>operation: num = 0
C=>operation: 创建套接字
D=>operation: 绑定套接字
E=>inputoutput: 输出“服务器已准备好”
F=>condition: 收到数据？
G=>operation: num = num + 1
H=>inputoutput: 输出 num

st->A->B->C->D->E->F
F(yes)->G->H->F
F(no)->F
```

与发送端程序相比，接收端的程序有一些函数不同。

``` Python
serverSocket.bind(('', serverPort))
```

这个函数显式地将端口12000绑定到套接字，而前面的空字符串`''`则表示任何来源的数据包都将定位到该套接字。

``` Python
message, clientAddress = serverSocket.recvfrom(2048)
```

服务端将从该套接字获取发送端发出的信息和发送端的地址。接收最多2048个字节。

## 测试程序

先从服务端打开程序以准备好接收数据，然后再从客户端打开发送程序。

第一次测试是在电脑的本地机器和虚拟机之间进行。发送100个数据，收到100个数据。

第二次测试也是在本地机器和虚拟机上进行。发送10000个数据，收到8690个数据。

第三次测试仍然在本地机器和虚拟机上进行。这次，在循环内添加了`time.sleep(0.01)`的语句，使得发送10000个数据的时间间隔拉大。“慢慢地”发送10000个数据，收到10000个数据。

第四次测试是从校园网内的电脑发送到阿里云服务器上。发送100个数据，收到100个数据。

第五次测试。发送10000个数据，收到4455个数据。

第六次测试。“慢慢地”发送10000个数据，收到10000个数据。

具体细节交由负责抓包与追踪的组员处理。

## 附录：使用C++进行网络编程

使用C++编写程序，则要麻烦得多，因为需要注意很多语法上的内容。这也是理论课课本第5版使用Java而弃用C++，随后第6版又使用Python而弃用Java进行网络编程的原因。

我在组内是负责编写发送端的Windows程序。接收端的Windows程序交由组员来完成。

发送端程序如下：

``` C++
#pragma comment (lib, "ws2_32.lib")
#include <iostream>
#include <winsock.h>
#include <cstring>

using namespace std;

int main()
{
	int serverPort = 12000;
	int times = 10000;
	const char* message = "LY!";
	WSADATA wsadata;
	if (WSAStartup(MAKEWORD(2, 0), &wsadata) != 0)
	{
		cerr << "WSAStartup failed!" << endl;
		return 0;
	}

	SOCKET clientSocket = socket(AF_INET, SOCK_DGRAM, 0);
	sockaddr_in addr;
	addr.sin_family = AF_INET;
	addr.sin_port = htons(serverPort);
	addr.sin_addr.S_un.S_un_b.s_b1 = 192;
	addr.sin_addr.S_un.S_un_b.s_b2 = 168;
	addr.sin_addr.S_un.S_un_b.s_b3 = 60;
	addr.sin_addr.S_un.S_un_b.s_b4 = 3; // 192.168.60.3

	for (int i = 0; i < times; i++)
	{
		sendto(clientSocket, message, strlen(message), 0, (const sockaddr*)& addr, sizeof(addr));
		// Sleep(10);
	}

	closesocket(clientSocket);
	WSACleanup();
	cout << "Send Completed." << endl;
	return 0;
}
```

与Python代码相比，C++代码不仅语法更加复杂，需要注意头文件和动态库的引用，而且多了一个过程，即：启动Winsock服务（`WSAStartup`）。

此外，C++中指明地址的方式更为复杂。此即问题思考（4），具体内容交由组员来阐述。

## 问题思考：实验过程中遇到的问题和解决方法

> 问题1：调试VirtualBox下的虚拟机时，难以在主机能够访问虚拟机的同时，虚拟机也可以访问外网。

解决方法：上网搜索资料。当VirtualBox采用“仅主机”的方式连接时，通过主机的网络共享及适当的IP配置即可。具体而言，虚拟机的地址为192.168.60.3，虚拟机网卡的地址为192.168.60.1，配置主机使得该网卡共享主机网络，然后在虚拟机中设置网关为虚拟网卡的地址，然后设置子网掩码为24（255.255.255.0）即可。

> 问题2：调试程序时，出现程序报错，或者发送了100个数据之后接收端1个也没收到的情况。

解决办法：首先在程序代码内查错，然后再在网上搜寻解决方案。这个在编程中是很经常出现的状况。