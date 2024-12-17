import socket
from threading import Thread
from cryptography.fernet import Fernet

key = b'KZjNdNlkEktP9JTkHg6NezOdQ_AjrRKwEQ9P0LmSivM='
fernet = Fernet(key)

host = 'localhost'
port = 8080
clients = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(3)
def get_guest():
    return None
def broadcast(msg, sender_conn=None):
    """Gửi tin nhắn đến tất cả các client, trừ người gửi"""
    for client in clients:
        if client != sender_conn:  
            try:
                client.send(msg)
            except Exception as e:
                print(f"Broadcast error: {e}")
                client.close()
                del clients[client]




def handle_clients(conn, addr):
    """Xử lý các client đã kết nối"""
    name = conn.recv(1024).decode("utf-8")  # Nhận tên từ client
    clients[conn] = name
    print(f"{name} has joined from {addr}")
   
    while True:
        try:
            msg = conn.recv(1024).decode("utf-8")
            if not msg:
                break

            if msg == name:
                # message = f"{msg}"
                # encrmsg = fernet.encrypt(msg.encode())
                # "skip đoạn tin nhắn chứa tên ng dùng"
                # broadcast(encrmsg, sender_conn=conn)
                # "gửi đoạn tin nhắn chứa thông tin muốn gửi"
                # broadcast(encrmsg, sender_conn=conn)

                continue  # Bỏ qua tin nhắn chứa tên người dùng

            if msg.lower() == "exit":
                conn.send("Goodbye!".encode("utf-8"))
                conn.close()
                del clients[conn]
                broadcast(f"{name} has left the chat.".encode("utf-8"))
                break

            message = f"{name}: {msg}"
            encrmsg = fernet.encrypt(message.encode())
            print(f"Encrypted message: {encrmsg}")
            broadcast(encrmsg, sender_conn=conn)

        except Exception as e:
            print(f"Error: {e}")
            conn.close()
            del clients[conn]
            broadcast(f"{name} has left the chat.".encode("utf-8"))
            break

def accept_connection():
    """Chấp nhận kết nối mới"""
    while True:
        client_conn, client_addr = sock.accept()
        print(f"New connection from {client_addr}")
        Thread(target=handle_clients, args=(client_conn, client_addr)).start()

if __name__ == "__main__":
    print(f"Server listening on {host}:{port}")
    accept_connection()
