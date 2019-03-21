import socket
import threading
from time import ctime


def send_msg(tcp_socket):
    """获取键盘数据，并将其发送给对方"""
    while True:

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
        # if msg == 1:
        #     print(msg)
        # elif msg == 2:
        #     send_file_2_client()
        if msg:
            print(msg)
        else:
            break


def send_file_2_client(new_client_socket, client_addr):
    data = "please input file name..."
    new_client_socket.send(('[%s]%s' % (ctime(), data)).encode())
    file_name = new_client_socket.recv(1024).decode("utf-8")
    print("The file that client want to download is：%s" % (str(client_addr), file_name))

    file_content = None

    try:
        f = open(file_name, "rb")
        file_content = f.read()
        f.close()
    except Exception as ret:
        print("The file not found" % file_name)

    if file_content:
        new_client_socket.send(file_content)


def main():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(("", 7890))
    tcp_server_socket.listen(128)

    while True:
        print('Waiting for connecting ......')
        # 4. 等待别人的电话到来(等待客户端的链接 accept)
        new_client_socket, client_addr = tcp_server_socket.accept()

        print('Connected from ', client_addr)
        # prompt = "please input your option: 1 is communication; 2 is download file"
        # new_client_socket.send(prompt.encode())

        # option = int(new_client_socket.recv(1024).decode())


        t_recv = threading.Thread(target=recv_msg, args=(new_client_socket,))
        t_recv.start()

        # t_send = threading.Thread(target=send_msg, args=(new_client_socket,))
        # t_send.start()

        # send_file_2_client(new_client_socket, client_addr)
        send_msg(new_client_socket)

        # 关闭套接字
        # 关闭accept返回的套接字 意味着 不会在为这个客户端服务
        new_client_socket.close()
        print("the client is disconnect.......")

    tcp_server_socket.close()


if __name__ == "__main__":
    main()
