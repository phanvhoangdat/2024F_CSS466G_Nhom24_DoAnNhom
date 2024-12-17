import socket
from threading import Thread

host = 'localhost'
port = 8080
clients = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(3)

def handle_clients(conn, addr):
    """Xử lý các client đã kết nối"""
    conn.send("Please enter your name: ".encode("utf-8"))  # Gửi yêu cầu nhập tên
    name = conn.recv(1024).decode("utf-8")  # Nhận tên từ client
    clients[conn] = name
    print(f"{name} has joined from {addr}")

    welcome = f"Welcome {name}! Type 'exit' to leave the chat."
    conn.send(welcome.encode("utf-8"))
    broadcast(f"{name} has joined the chat!".encode("utf-8"))

    while True:
        try:
            msg = conn.recv(1024)
            if msg.decode("utf-8").lower() == "exit":
                conn.send("Goodbye!".encode("utf-8"))
                conn.close()
                del clients[conn]
                broadcast(f"{name} has left the chat.".encode("utf-8"))
                break
            else:
                broadcast(msg, prefix=f"{name}: ")
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
            del clients[conn]
            break


def broadcast(msg, prefix=""):
    """Gửi tin nhắn đến tất cả các client"""
    for client in clients:
        try:
            client.send(prefix.encode("utf-8") + msg)
        except Exception as e:
            print(f"Broadcast error: {e}")

def accept_connection():
    """Chấp nhận kết nối mới"""
    while True:
        client_conn, client_addr = sock.accept()
        print(f"New connection from {client_addr}")
        Thread(target=handle_clients, args=(client_conn, client_addr)).start()

if __name__ == "__main__":
    print(f"Server listening on {host}:{port}")
    accept_connection()
