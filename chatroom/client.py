import socket
from threading import Thread

host = 'localhost'
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

def receive_message():
    """Luồng để nhận tin nhắn từ server"""
    while True:
        try:
            msg = sock.recv(1024).decode("utf-8")
            if msg:
                print(msg)
        except Exception as e:
            print(f"Error receiving message: {e}")
            sock.close()
            break

def send_message():
    """Luồng để gửi tin nhắn đến server"""
    while True:
        try:
            msg = input("")  # Nhập tin nhắn từ bàn phím
            sock.send(msg.encode("utf-8"))
            if msg.lower() == "exit":
                print("You have left the chat.")
                sock.close()
                break
        except Exception as e:
            print(f"Error sending message: {e}")
            sock.close()
            break

# Nhập tên người dùng trước khi khởi động luồng
name = input("Please enter your name: ")
sock.send(name.encode("utf-8"))

# Tạo các luồng gửi và nhận
Thread(target=receive_message).start()
Thread(target=send_message).start()
