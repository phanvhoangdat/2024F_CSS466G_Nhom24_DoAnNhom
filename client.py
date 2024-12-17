import socket
import threading
import flet as ft
import datetime
from server import get_guest
from cryptography.fernet import Fernet

key = b'KZjNdNlkEktP9JTkHg6NezOdQ_AjrRKwEQ9P0LmSivM='
fernet = Fernet(key)



host = 'localhost'
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))


                
'''
Shades of blue include cyan, navy, turquoise, 
aqua, midnight blue, sky blue, royal blue, and aquamarine.
The base blue color's hex value in HTML is #0000FF.
'''

class UserClient(ft.Column):
    def __init__(self):
        super().__init__()
        self.message = []
        self.name_iput = ft.TextField(
            hover_color="#7CB9E8",
            width=200,
            hint_text="Enter your Name",
            color="white",
            border_color="#7CB9E8",
            border_radius=10,
            hint_style=ft.TextStyle(color="white"),
            multiline=True,
            min_lines=1,
            max_lines=1,
            bgcolor="#7CB9E8"
        )

        self.option_select = ft.IconButton(
            ft.icons.MENU,
            icon_color="white",
            bgcolor="#7CB9E8"
        )
        self.notifcation_box_drop = ft.AlertDialog(
            modal= True,
            title=ft.Text("Notification"),
            content=ft.Container(
                ft.Row(
                    [
                        ft.Text(
                            "Limited 5000 keywords"
                        )
                    ]
                )
            ),
            actions=[
                ft.TextButton("Close",on_click=self.close_notification)
            ]

            
        )
        self.option_controls = ft.AlertDialog(
            
        )
        self.icons_stack = ft.Container(
            ft.Row(
                [
                    ft.IconButton()
                ]
            )
        )
        self.guest_symbol = ft.Container(
            image_src="https://img.tripi.vn/cdn-cgi/image/width=700,height=700/https://gcs.tripi.vn/public-tripi/tripi-feed/img/474076nOK/avatar-tik-tok-cute-cho-con-gai_103844352.jpg",
            image_fit=ft.ImageFit.COVER,
            height=40,
            width=40,
            bgcolor="blue",
            border_radius=50,
            border=ft.border.BorderSide(1,"grey")
        )
        self.avt_symbol = ft.Container(
            image_src="https://cdn2.fptshop.com.vn/unsafe/800x0/avatar_cute_5_b048382047.jpg",
            image_fit=ft.ImageFit.COVER,
            height=40,
            width=40,
            bgcolor="blue",
            border_radius=50,
            border=ft.border.BorderSide(1,"grey")
        )
        self.guestname = ft.Text(color="white",weight="bold")
        self.username = ft.Text(color="white",weight="bold")
        self.send_msg_btn = ft.IconButton(
            ft.icons.SEND,
            bgcolor="white",
            icon_color="#7CB9E8",
            on_click=self.append_message,
        )
        self.attachment_btn = ft.IconButton(
            ft.icons.ATTACHMENT,
            bgcolor="#7CB9E8",
            icon_color="white"
        )

        self._text_field = ft.TextField(
            hover_color="#7CB9E8",
            hint_text="Enter your message ...",
            color="white",
            border_color="#7CB9E8",
            border_radius=10,
            hint_style=ft.TextStyle(color="white"),
            multiline=True,
            min_lines=1,
            max_lines=1,
            bgcolor="#7CB9E8"
        )

        self._message_bar = ft.Container(
            ft.Row(
                [
                    self.attachment_btn,
                    self._text_field,
                    self.send_msg_btn
                ]
            ),
            bgcolor="#7CB9E8",
            border_radius=30
        )

        self._chat_column = ft.Column(
            [

            ],
            width=1000,
            height=650,
            scroll=ft.ScrollMode.HIDDEN
        )

        self._message_room = ft.Container(
            self._chat_column,
            height=640,
            width=1500
        )

        self._message_box = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                           
                            self.avt_symbol,
                            self.name_iput,
                            self._message_bar,
                            
                        ],
                    )
                ]
            ),
            padding=ft.padding.only(top=12,left=50),
            height=75,
            bgcolor="#ADD8E6",
            margin=ft.margin.only(left=-20,right=-20)
        )
        self.controls = [
            self._message_room,
            self._message_box,
            self.notifcation_box_drop,
        ]
    

    def open_notification(self,e):
        self.notifcation_box_drop.open = True
        self.update()

    def close_notification(self,e):
        self.notifcation_box_drop.open = False
        self.update()

    def receive_message(self):
        '''Nhận thông tin đoạn chat
        gồm người chat đối diện và tin nhắn của họ'''
        while True:
           

            # Nhận và giải mã tin nhắn
            msg = sock.recv(1024).decode()
            try:
                decrypt_msg = fernet.decrypt(msg.encode()).decode()  # Giải mã tin nhắn
            except Exception as e:
                print(f"Decryption error: {e}")
                decrypt_msg = msg  
            
            '''Lưu tin nhắn đã giải mã'''
            self.message.append(decrypt_msg)
    

            if decrypt_msg:
                self._chat_column.controls.append(
                    ft.Container(
                        ft.Row(
                            [
                                self.guest_symbol,
                                ft.Column(
                                    [
                                        
                                        ft.TextField(
                                            value=f"{decrypt_msg}",
                                            color="white",
                                            multiline=True,
                                            border_color="blue",
                                            border_radius=15,
                                            disabled=True,
                                            bgcolor="blue",
                                        ),
                                        ft.Text(
                                            value=f"{datetime.datetime.today()}",
                                            italic=True,
                                            size=10
                                        )
                                    ]
                                )
                            ]
                        ),
                        width=1000
                    )
                )
                self._chat_column.update()


            
            
        
            

    def append_message(self,e):
        '''Nếu như ko nhập tên vào thì 
        client sẽ ko tiếp nhận thông tin và nhập
        tin nhắn'''
        if self.name_iput.value == "":
            return None
        
        '''Nếu tin nhắn ko có gì sẽ trả về none'''
        if self._text_field.value == "":
            return None

        '''Nếu tin nhắn vượt quá 3000 kí tự sẽ h
        hiện thông báo'''
        if len(self._text_field.value) > 3000:
            self.open_notification(e)
        else:

            self.save_username(e)
            '''Lưu thông tin người dùng'''
            message = self._text_field.value
            '''Gửi tin nhán từ thanh nhập'''
            sock.send(message.encode("utf-8"))
            print(message)

            '''Thêm tin nhắn vào đoạn chat'''
            self._chat_column.controls.append(
                    
                    ft.Container(
                        ft.Row(
                            [
                                self.avt_symbol,
                                
                                ft.Column(
                                    [
                                        
                                        ft.TextField(
                                            value=f"{self.username.value}: {message}",
                                            color="white",
                                            multiline=True,
                                            border_color="#7CB9E8",
                                            border_radius=15,
                                            disabled=True,
                                            bgcolor="#7CB9E8",
                                            
                                        ),
                                        ft.Text(
                                            value=f"{datetime.datetime.today()}",
                                            italic=True,
                                            size=10
                                        )
                                    ]
                                )
                            ]
                        ),
                        width=1000
                    )        
                )
        
        self._text_field.value = ""
        '''trả thanh nhập tin nhắn về rỗng
        sau khi nhập'''
        self.update()

    def save_username(self,e):
        '''nhận thông tin người gửi từ thanh nhập'''
        self.username.value = self.name_iput.value
        if self.username.value:
            sock.send(self.username.value.encode("utf-8"))
            self.update()
        '''lưu tên ngươi gửi'''


def main(page:ft.Page):
    
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.COFFEE,color="white"),
        title=ft.Text("ESSPRESSO",color="white"),
        bgcolor="#ADD8E6",
        
    )
    client = UserClient()
    page.add(client)
    '''phân luồng chạy cho chức năng nhận 
    tin nhắn từ người dùng '''
    threading.Thread(target=client.receive_message,daemon=True).start()
    page.theme_mode = ft.ThemeMode.LIGHT
    page.update()

if __name__ == "__main__":
    
    ft.app(target=main)
