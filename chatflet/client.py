import socket
from threading import Thread
import flet as ft

host = 'localhost'
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))


def main(page: ft.Page):
    # Khởi tạo giao diện
    page.title = "Chatroom with Flet"
    page.theme_mode = ft.ThemeMode.LIGHT
    messages = ft.ListView(expand=True, spacing=10)
    input_name = ft.TextField(label="Enter your name", autofocus=True)
    input_message = ft.TextField(label="Enter your message", autofocus=True, expand=True)
    send_button = ft.ElevatedButton("Send", disabled=True)
    
    # Biến để kiểm soát tên người dùng
    user_name = None

    # Hàm xử lý khi nhận tin nhắn
    def receive_message():
        while True:
            try:
                msg = sock.recv(1024).decode("utf-8")
                if msg:
                    page.add(ft.Text(msg))  # Thêm tin nhắn vào giao diện
                    page.update()
            except Exception as e:
                page.add(ft.Text(f"Error: {e}", color="red"))
                page.update()
                sock.close()
                break

    # Hàm gửi tin nhắn
    def send_message(e):
        if input_message.value.strip():
            msg = input_message.value.strip()
            sock.send(msg.encode("utf-8"))
            input_message.value = ""
            page.update()
            if msg.lower() == "exit":
                sock.close()
                page.add(ft.Text("Disconnected from server!", color="red"))
                page.update()

    # Hàm lưu tên người dùng
    def save_name(e):
        nonlocal user_name
        if input_name.value.strip():
            user_name = input_name.value.strip()
            sock.send(user_name.encode("utf-8"))  # Gửi tên đến server
            input_name.disabled = True
            send_button.disabled = False
            page.add(ft.Text(f"Welcome {user_name}!", color="green"))
            page.update()

    # Kết nối giao diện với hành động
    input_name.on_submit = save_name
    send_button.on_click = send_message

    # Thêm các thành phần giao diện vào ứng dụng
    page.add(
        ft.Column([
            ft.Text("Chatroom", style="headlineMedium", weight=ft.FontWeight.BOLD),
            input_name,
            ft.Row([input_message, send_button]),
            ft.Divider(),
            messages,
        ], spacing=20)
    )

    # Bắt đầu luồng nhận tin nhắn
    Thread(target=receive_message, daemon=True).start()


# Chạy ứng dụng Flet
ft.app(target=main)
