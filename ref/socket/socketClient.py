import socket

print("客户端开启")
# 套接字接口
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 设置ip和端口
host = '169.254.93.228'
port = 32768

try:
    mySocket.connect((host, port))  ##连接到服务器
    print("Connected")
except:  ##连接不成功，运行最初的ip
    print('Offline')

while True:
    # 发送消息
    msg = input("客户端发送:")
    # 编码发送
    mySocket.send(msg.encode("utf-8"))
    print("发送完成")
    if msg == "hello":
        print("你好")
    if msg == "qq":
        mySocket.close()
        print("程序结束\n")
        exit()
print("程序结束\n")