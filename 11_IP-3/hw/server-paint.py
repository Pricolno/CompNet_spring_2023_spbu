import tkinter as tk

import socket
import pickle

from utils import Positon

# graphics
X, Y = 0, 0 
HEIGHT, WEIGHT = 700, 500
HEIGHT_PAD, WEIGHT_PAD = 300, 300
BRUSH_SIZE = 5
BRUSH_COLOR = 'black'

# sockets
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


class ServerPaint(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        # set global params
        self.brush_size = BRUSH_SIZE
        self.brush_color = BRUSH_COLOR

        self.setUI()


    def setUI(self):
 
        self.parent.title("CompNet: Remote Paint Server")  # Устанавливаем название окна
        self.pack(fill=tk.BOTH, expand=1)  # Размещаем активные элементы на родительском окне
 
        self.columnconfigure(6, weight=1) # Даем седьмому столбцу возможность растягиваться, благодаря чему кнопки не будут разъезжаться при ресайзе
        self.rowconfigure(2, weight=1) # То же самое для третьего ряда
 
        self.canv = tk.Canvas(self, bg="white")  # Создаем поле для рисования, устанавливаем белый фон
        self.canv.grid(row=2, column=0, columnspan=7,
                       padx=5, pady=5, sticky=tk.E+tk.W+ tk.S+ tk.N)  # Прикрепляем канвас методом grid. Он будет находится в 3м ряду, первой колонке, и будет занимать 7 колонок, задаем отступы по X и Y в 5 пикселей, и заставляем растягиваться при растягивании всего окна
        # handler for left-motion
        # self.canv.bind("<B1-Motion>", self.draw)


        color_lab = tk.Label(self, text="Color: ") # Создаем метку для кнопок изменения цвета кисти
        color_lab.grid(row=0, column=0, padx=6) # Устанавливаем созданную метку в первый ряд и первую колонку, задаем горизонтальный отступ в 6 пикселей
 
        red_btn = tk.Button(self, text="Red", width=10, 
                            #command=lambda: self.set_color("Red")
                            ) # Создание кнопки:  Установка текста кнопки, задание ширины кнопки (10 символов)
        red_btn.grid(row=0, column=1) # Устанавливаем кнопку первый ряд, вторая колонка
 
        # Создание остальных кнопок повторяет ту же логику, что и создание
        # кнопки установки красного цвета, отличаются лишь аргументы.
 
        green_btn = tk.Button(self, text="Green", width=10,
                              #ommand=lambda: self.set_color("Green")
                            )
        
        green_btn.grid(row=0, column=2)
 
        blue_btn = tk.Button(self, text="Blue", width=10,
                             #command=lambda: self.set_color("Blue")
                             )
        blue_btn.grid(row=0, column=3)
 
        black_btn = tk.Button(self, text="Black", width=10,
                              #command=lambda: self.set_color("Black")
                              )
        black_btn.grid(row=0, column=4)
 
        white_btn = tk.Button(self, text="White", width=10,
                              #command=lambda: self.set_color("White")
                              )
        white_btn.grid(row=0, column=5)
 
 
        size_lab = tk.Label(self, text="Brush size: ") # Создаем метку для кнопок изменения размера кисти
        size_lab.grid(row=1, column=0, padx=5)
        one_btn = tk.Button(self, text="Two", width=10, 
                            #command=lambda: self.set_brush_size(1)
                            )
        one_btn.grid(row=1, column=1)
 
        two_btn = tk.Button(self, text="Five", width=10,
                            #command=lambda: self.set_brush_size(2)
                            )
        two_btn.grid(row=1, column=2)
 
        five_btn = tk.Button(self, text="Seven", width=10,
                             #command=lambda: self.set_brush_size(5)
                             )
        five_btn.grid(row=1, column=3)
 
        seven_btn = tk.Button(self, text="Ten", width=10, 
                              #command=lambda: self.set_brush_size(7)
                              )
        seven_btn.grid(row=1, column=4)
 
        ten_btn = tk.Button(self, text="Twenty", width=10,
                            #command=lambda: self.set_brush_size(10)
                            )
        ten_btn.grid(row=1, column=5)
 
        twenty_btn = tk.Button(self, text="Fifty", width=10, 
                               #command=lambda: self.set_brush_size(20)
                               )
        twenty_btn.grid(row=1, column=6, sticky=tk.W)

    def draw(self, event):
        # will do only remote draw

        #self.send_data_to_server()

        self.canv.create_oval(event.x - self.brush_size,
                            event.y - self.brush_size,
                            event.x + self.brush_size,
                            event.y + self.brush_size,
                            fill=self.brush_color, outline=self.brush_color)
    
    def draw_xy(self, pos: Positon):
        # will do only remote draw

        #self.send_data_to_server()

        self.canv.create_oval(pos.x - self.brush_size,
                            pos.y - self.brush_size,
                            pos.x + self.brush_size,
                            pos.y + self.brush_size,
                            fill=self.brush_color, outline=self.brush_color)
        
    def set_color(self, new_color):
        self.brush_color = new_color
    
    def set_brush_size(self, new_size):
        self.brush_size = new_size





def main():
    # init tk
    root = tk.Tk()
    root.geometry(f"{HEIGHT}x{WEIGHT}+{HEIGHT_PAD}+{WEIGHT_PAD}")
    app = ServerPaint(root)

    
    # socket logic
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    
    print("Wait client :)")
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")
    
    def socket_get_info():
        nonlocal app
        
        
        data = conn.recv(10240)
        #print(f"socket_get_info:data=\n{data}")
        pos = pickle.loads(data)
        print(f"socket_get_info:pos=\n{pos}")
        app.draw_xy(pos)
        
        app.after(10, socket_get_info)


    app.after(0, socket_get_info)
    app.mainloop()  






if __name__ == "__main__":
    print("Start program!")

    main()    

    print("Stoped program.")