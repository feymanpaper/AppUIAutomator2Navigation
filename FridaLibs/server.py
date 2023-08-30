import socket
# 创建一个socket对象，默认TCP套接字
s = socket.socket()
# 绑定端口
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 10021))
# 监听端口
s.listen(5)
print("正在连接中……")

# 建立连接之后，持续等待连接
# 阻塞等待连接
sock,addr = s.accept()
sock.setblocking(False)
print(sock,addr)
# 一直保持发送和接收数据的状态
while 1:
    try:
        text = sock.recv(1024)
        # 客户端发送的数据为空的无效数据
        if len(text.strip()) == 0:
            print("服务端接收到客户端的数据为空")
        else:
            print("收到客户端发送的数据为：{}".format(text.decode()))
    except Exception as e:
        if e.errno == socket.errno.EWOULDBLOCK:
            # 如果没有数据可读，继续等待
            continue
        else:
            # 发生错误，关闭连接
            print("发生错误：", e)
            sock.close()
            break

sock.close()
s.close()