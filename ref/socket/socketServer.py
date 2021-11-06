# encoding: utf-8
import socket
import time
import winsound

print("服务端开启")
# 套接字接口
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 设置IP和端口
host = "169.254.93.228"
port = 32768

mySocket.bind((host, port))
mySocket.listen(2)

reciveTimes=0
datapack=[]
while True:
    # 接收客户端连接
    if reciveTimes==2:
        break
    print("等待连接....")
    client, address = mySocket.accept()
    print("新连接")
    reciveTimes=reciveTimes+1
    print("IP is %s" % address[0])
    print("port is %d\n" % address[1])

    # 读取消息
    msg = client.recv(128)
    # 把接收到的数据进行解码
    #print(msg.decode("utf-8"))
    msg=msg.decode("utf-8")
    data=[float(i) for i in msg.split(",")]
    datapack.append(data.copy())
    client.close()
    print(f"L:{data[0]}\t XC: {data[1]}")

mySocket.close()
winsound.Beep(6000, 2000)
if datapack[0][1]>datapack[1][1]:
    print(f"摆线长度:{datapack[0][0]}")
else:
    print(f"摆线长度:{datapack[1][0]}")





