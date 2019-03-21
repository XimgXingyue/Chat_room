import socket
import threading
from time import ctime


def send_msg(tcp_socket):
    """获取键盘数据，并将其发送给对方"""
    while True:
        # prompt = "please input your option: 1 is communication; 2 is download file"
        # print(prompt)
        data = input('I>')
        if not data:
            break
        tcp_socket.send(('[%s]%s'%(ctime(), data)).encode())


def recv_msg(tcp_socket):
    """接收数据并显示"""
    while True:
        # 1. 接收数据
        msg = tcp_socket.recv(1024).decode()
        # 3. 显示接收到的数据
        if not msg:
            break
        print(msg)


def main():
    # 1. 创建tcp的套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. 链接服务器
    # tcp_socket.connect(("192.168.33.11", 7890))
    server_ip = input("请输入要链接的服务器的ip:")
    server_port = int(input("请输入要链接的服务器的port:"))
    server_addr = (server_ip, server_port)
    tcp_socket.connect(server_addr)

    t = threading.Thread(target=recv_msg, args=(tcp_socket,))
    t.start()

    send_msg(tcp_socket)

    # 4. 关闭套接字
    tcp_socket.close()


if __name__ == "__main__":
    main()