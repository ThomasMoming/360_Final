# from tkinter import Label, Tk
# from tkinter.ttk import Button
# from threading import Thread
# from voice_assistant import VoiceAssistant
# from text_to_speech import TextToSpeech
# import time
#
#
# class VoiceAssistantUI:
#     def __init__(self, master):
#         self.tts = TextToSpeech()
#         """
#         初始化界面组件
#         :param master: 主窗口
#         """
#         self.master = master
#         self.master.title("Voice Assistant")
#         self.master.geometry("400x300")
#
#         # 状态标签
#         self.status_label = Label(master, text="Status: Ready", font=("Helvetica", 14))
#         self.status_label.pack(pady=20)
#
#         # 使用 ttk.Button 代替 tkinter.Button
#         self.start_button = Button(master, text="Start Assistant", command=self.start_assistant)
#         self.start_button.pack(pady=10)
#
#         self.stop_button = Button(master, text="Stop Assistant", command=self.stop_assistant)
#         self.stop_button.pack(pady=10)
#
#         self.activate_button = Button(master, text="Activate Mode", command=self.activate_mode)
#         self.activate_button.pack(pady=10)
#
#         self.silent_button = Button(master, text="Silent Mode", command=self.silent_mode)
#         self.silent_button.pack(pady=10)
#
#         self.exit_button = Button(master, text="Exit", command=self.exit_program)
#         self.exit_button.pack(pady=10)
#
#         # 初始化语音助手
#         self.assistant = VoiceAssistant(wake_word="august")
#         self.assistant_thread = None
#
#     def update_status(self, message):
#         self.master.after(0, self.status_label.config, {"text": message})
#
#     def start_assistant(self):
#         self.update_status("Status: Listening...")
#         self.assistant.is_running = True
#         self.assistant_thread = Thread(target=self.run_assistant_thread, daemon=True)
#         self.assistant_thread.start()
#
#     def run_assistant_thread(self):
#         try:
#
#             time.sleep(10)  # 阻塞 10 秒
#             self.assistant.start()
#         except Exception as e:
#             self.update_status(f"Error: {e}")
#
#     def stop_assistant(self):
#         self.update_status("Status: Stopped")
#         self.assistant.stop()
#
#     def activate_mode(self):
#         self.assistant.is_active = True
#         self.update_status("Status: Activated")
#         self.tts.speak("Active Mode.")
#
#     def silent_mode(self):
#         self.assistant.is_active = False
#         self.update_status("Status: Silent")
#         self.tts.speak("Silent Mode.")
#
#     def exit_program(self):
#         self.master.destroy()



# from tkinter import Label, Tk
# from tkinter.ttk import Button, Style
# from PIL import Image, ImageTk
# from PIL.Image import Resampling
# from threading import Thread
# from voice_assistant import VoiceAssistant
# from text_to_speech import TextToSpeech
# import time
#
#
# class VoiceAssistantUI:
#     def __init__(self, master):
#         self.tts = TextToSpeech()
#         self.text_log = []  # To store the recent text logs
#
#         self.master = master
#         self.master.title("Voice Assistant")
#         self.master.geometry("480x530")
#         self.master.configure(bg=None)
#
#         # Load and resize the images
#         self.initial_image_path = "images/cat.png"  # Initial state image
#         self.cat_image_path = "images/cat_start.png"  # Listening state image
#         self.cat_awake_image_path = "images/cat_awake.png"  # Activated state image
#
#         self.photo_initial = self.load_image(self.initial_image_path, (300, 350))
#         self.photo = self.load_image(self.cat_image_path, (300, 350))
#         self.photo_awake = self.load_image(self.cat_awake_image_path, (300, 350))
#
#         # Load the cat's name as an image
#         name_image = Image.open("images/name.png")
#         name_image = name_image.resize((216, 60), Resampling.LANCZOS)
#         self.name_photo = ImageTk.PhotoImage(name_image)
#
#         # Status label on top of the image
#         self.status_label = Label(master, text="August: Ready", font=("Comic Sans MS", 14), fg="black", width=20)
#         self.status_label.grid(row=1, column=3)
#
#         # Add the image to a label
#         self.image_label = Label(master, image=self.photo_initial)
#         self.image_label.grid(row=1, column=0, rowspan=7,columnspan=3)
#
#         # Display the cat's name as an image
#         self.name_label = Label(master, image=self.name_photo)
#         self.name_label.grid(row=0, column=0, columnspan=4)
#
#         # Define a custom style for buttons
#         self.style = Style()
#         self.style.configure("Custom.TButton",
#                              font=("Comic Sans MS", 12),
#                              relief="flat",
#                              borderwidth=0,
#                              background="white",
#                              activebackground="orange",
#                              foreground="black",
#                              activeforeground="white")
#
#         # Initial visibility state for the additional buttons
#         self.show_buttons = False
#
#         # Buttons
#         self.main_button = Button(master, text="Menu", command=self.toggle_buttons, style="Custom.TButton")
#         self.main_button.grid(row=2, column=3)
#
#         self.start_button = Button(master, text="Start Assistant", command=self.start_assistant, style="Custom.TButton")
#         self.stop_button = Button(master, text="Stop Assistant", command=self.stop_assistant, style="Custom.TButton")
#         self.activate_button = Button(master, text="Activate Mode", command=self.activate_mode, style="Custom.TButton")
#         self.silent_button = Button(master, text="Silent Mode", command=self.silent_mode, style="Custom.TButton")
#         self.exit_button = Button(master, text="Exit", command=self.exit_program, style="Custom.TButton")
#
#         # Pack the additional buttons conditionally
#         self.update_button_visibility()
#
#         # Initialize the voice assistant
#         self.assistant = VoiceAssistant(wake_word="august")
#         self.assistant_thread = None
#
#         self.log_label = Label(master, text="", font=("Comic Sans MS", 14), justify="left", wraplength=420, bg="orange",
#                                fg="black",pady=2)
#         self.log_label.grid(row=8, column=1, columnspan=3, sticky="nsew")  # sticky to make it expand in the whole row
#         self.conversation_label = Label(master, text="Chat", font=("Comic Sans MS", 20, ), justify="left", wraplength=420, bg="orange",
#                                fg="black")
#         self.conversation_label.grid(row=8, column=0,sticky="nsew")
#         # Configure grid row to have the orange background
#         master.grid_rowconfigure(8, weight=1, uniform="row")
#
#         self.update_log_display()
#
#     def load_image(self, path, size):
#         image = Image.open(path)
#         image = image.resize(size, Resampling.LANCZOS)
#         return ImageTk.PhotoImage(image)
#
#     def update_image(self, state="initial"):
#         if state == "initial":
#             new_image = self.photo_initial
#         elif state == "listening":
#             new_image = self.photo
#         elif state == "activated":
#             new_image = self.photo_awake
#         self.image_label.config(image=new_image)
#         self.image_label.image = new_image
#
#     def update_status(self, message):
#         self.master.after(0, self.status_label.config, {"text": message})
#
#     def update_log(self, message, header=""):
#         # Add the new message to the log and update the UI
#         self.text_log.append(f"{message}")
#         if len(self.text_log) > 5:
#             self.text_log.pop(0)  # Keep only the last 5 logs
#         self.log_label.config(text="\n".join(self.text_log))
#
#     def update_log_display(self):
#         # Periodically check for new log messages and update the UI
#         self.master.after(1000, self.update_log_display)
#         if self.assistant and self.assistant.log_messages:
#             latest_message = self.assistant.log_messages[-1]
#             if latest_message not in self.text_log:
#                 self.update_log(latest_message)
#
#     def start_assistant(self):
#         self.update_status("August is listening..")
#         self.update_image(state="listening")
#         self.assistant.is_running = True
#         self.assistant_thread = Thread(target=self.run_assistant_thread, daemon=True)
#         self.assistant_thread.start()
#         self.update_log("August: assistant started")
#
#     def run_assistant_thread(self):
#         try:
#             time.sleep(0.1)  # Block for 10 seconds
#             self.assistant.start()
#         except Exception as e:
#             self.update_status(f"Error: {e}")
#
#     def stop_assistant(self):
#         self.update_status("August: stopped")
#         self.update_image(state="initial")
#         self.assistant.stop()
#         self.update_log("August: assistant stopped")
#
#     def activate_mode(self):
#         self.assistant.is_active = True
#         self.update_status("August: activated")
#         self.update_image(state="activated")
#         self.tts.speak("Active Mode.")
#         self.update_log("August: active mode")
#
#     def silent_mode(self):
#         self.assistant.is_active = False
#         self.update_status("August: silent")
#         self.update_image(state="listening")
#         self.tts.speak("Silent Mode.")
#         self.update_log("August: silent mode")
#
#     def exit_program(self):
#         self.master.destroy()
#         self.update_log("August: program exited")
#
#     def toggle_buttons(self):
#         self.show_buttons = not self.show_buttons
#         self.update_button_visibility()
#
#     def update_button_visibility(self):
#         if self.show_buttons:
#             self.start_button.grid(row=3, column=3)
#             self.stop_button.grid(row=4, column=3)
#             self.activate_button.grid(row=5, column=3)
#             self.silent_button.grid(row=6, column=3)
#             self.exit_button.grid(row=7, column=3)
#         else:
#             self.start_button.grid_forget()
#             self.stop_button.grid_forget()
#             self.activate_button.grid_forget()
#             self.silent_button.grid_forget()
#             self.exit_button.grid_forget()

#---------------------------------------------------------------------------------------------------------
import sys
from tkinter import Label, Canvas, Tk, CENTER
from tkinter.ttk import Button, Style
from threading import Thread
from PIL import Image, ImageTk
from voice_assistant import VoiceAssistant
from text_to_speech import TextToSpeech
from io import StringIO


class VoiceAssistantUI:
    def __init__(self, master):
        self.tts = TextToSpeech()
        """
        初始化界面组件
        :param master: 主窗口
        """
        self.master = master
        self.master.title("Voice Assistant")

        # 隐藏窗口边框
        self.master.overrideredirect(True)

        # 设置透明背景颜色 (Windows 支持全透明)
        self.master.attributes("-transparentcolor", "white")
        self.master.configure(bg="white")  # 背景色设置为透明色

        # 设置窗口始终在最上方
        self.master.attributes("-topmost", True)

        # 设置窗口大小和位置
        self.master.geometry("400x300+400+400")

        # 拖动窗口的初始位置
        self._offset_x = 0
        self._offset_y = 0

        # 图片加载和缩放
        self.cat_image = self.load_and_resize_image("images/cat.png", 125, 225)
        self.cat_awake_image = self.load_and_resize_image("images/cat_awake.png", 125, 225)

        # 图片Canvas
        self.status_canvas = Canvas(self.master, width=125, height=180, bg="white", highlightthickness=0)
        self.status_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)  # 居中放置在窗口正中心
        self.status_canvas.create_image(0, 0, anchor="nw", image=self.cat_image)  # 显示图片

        # 添加可拖动的小圆点
        self.add_drag_point()

        # 添加右上角的控制点
        self.button_visible = False  # 用于切换按钮显示状态
        self.add_control_point()

        # 初始化实时日志显示区域
        self.log_canvas = None

        # 初始化语音助手
        self.assistant = VoiceAssistant(wake_word="august", ui=self)
        self.assistant_thread = None

        # 重定向标准输出到 StringIO
        self.console_output = StringIO()
        sys.stdout = self.console_output

    def load_and_resize_image(self, path, width, height):
        """
        加载图片并等比例缩放为指定宽度和高度
        :param path: 图片路径
        :param width: 缩放后的宽度
        :param height: 缩放后的高度
        :return: Tkinter PhotoImage 对象
        """
        img = Image.open(path)
        img.thumbnail((width, height), Image.LANCZOS)  # 替换 ANTIALIAS 为 LANCZOS
        return ImageTk.PhotoImage(img)

    def add_drag_point(self):
        """
        在图片左上角添加一个小圆点用于拖动窗口
        """
        # 小圆点的 Canvas
        #self.drag_canvas = Canvas(self.master, width=20, height=20, bg="white", highlightthickness=0)

        # 设置小圆点的位置，调整到图片Canvas的左上角
        #self.drag_canvas.place(relx=0.5 - (125 / 2) / 400, rely=0.5 - (225 / 2) / 300 + 0.05, anchor=CENTER)

        # 绘制小圆点
        #self.drag_canvas.create_oval(5, 5, 15, 15, fill="gray")

        # 绑定鼠标事件
        #self.drag_canvas.bind("<Button-1>", self.start_drag)  # 按下鼠标左键
        #self.drag_canvas.bind("<B1-Motion>", self.drag)  # 拖动鼠标

        # 同时绑定到图片 Canvas
        self.status_canvas.bind("<Button-1>", self.start_drag)  # 按下鼠标左键
        self.status_canvas.bind("<B1-Motion>", self.drag)  # 拖动鼠标

    def add_control_point(self):
        """
        在图片右上角添加一个小圆点用于显示/隐藏按钮
        """
        # 小圆点的 Canvas
        self.control_canvas = Canvas(self.master, width=20, height=20, bg="white", highlightthickness=0)

        # 动态获取图片的右上角坐标
        image_width = 125
        relx = 0.5 + (image_width / 2) / 400  # 图片的右上角相对窗口宽度的比例
        rely = 0.5 - (225 / 2) / 300 + 0.05  # 图片的右上角相对窗口高度的比例

        self.control_canvas.place(relx=relx, rely=rely, anchor=CENTER)

        # 绘制小圆点
        self.control_canvas.create_oval(5, 5, 15, 15, fill="gray")

        # 绑定鼠标点击事件
        self.control_canvas.bind("<Button-1>", self.toggle_buttons)

        # 初始化按钮
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        """
        创建按钮并初始设置为隐藏，修改按钮样式
        """
        style = Style()
        style.configure("Custom.TButton", font=("Times New Roman", 10, "bold"), padding=5)
        style.map("Custom.TButton", background=[("active", "#0056b3")])

        button_commands = [
            ("Start", self.start_assistant),
            ("Stop", self.stop_assistant),
            ("Activate", self.activate_mode),
            ("Silent", self.silent_mode),
            ("Exit", self.exit_program),
            ("Log", self.show_log_canvas),
        ]

        for i, (text, command) in enumerate(button_commands):
            button = Button(
                self.master, text=text, command=command, style="Custom.TButton", width=10
            )
            button.place(x=0, y=0)
            button.place_forget()
            self.buttons.append((button, i))

    def toggle_buttons(self, event):
        """
        显示或隐藏按钮
        """
        if self.button_visible:
            for button, _ in self.buttons:
                button.place_forget()
        else:
            control_canvas_x = self.control_canvas.winfo_x()
            control_canvas_y = self.control_canvas.winfo_y()
            for button, index in self.buttons:
                button.place(x=control_canvas_x + 30, y=control_canvas_y + index * 30)
        self.button_visible = not self.button_visible

    def show_log_canvas(self):
        """
        显示或隐藏日志 Canvas
        """
        if self.log_canvas:  # 如果 log_canvas 已经存在
            self.log_canvas.destroy()  # 销毁 Canvas（隐藏日志）
            self.log_canvas = None  # 重置 log_canvas 为 None
        else:
            # 创建新的日志显示区域
            self.log_canvas = Canvas(self.master, width=250, height=50, bg="black")
            self.log_canvas.place(x=self.status_canvas.winfo_x() - 110, y=self.status_canvas.winfo_y() + 170)

            # 更新日志内容
            self.update_log()

    def update_log(self):
        """
        实时更新日志内容
        """
        if self.log_canvas:
            self.log_canvas.delete("all")  # 清除旧内容
            logs = self.console_output.getvalue().split("\n")[-3:]  # 获取最新的 3 行日志
            for i, log in enumerate(logs):
                self.log_canvas.create_text(
                    5,
                    i * 18,  # 增加行间距
                    anchor="nw",
                    text=log,
                    font=("Arial", 10, "bold"),  # 使用更清晰的字体和增大字体大小
                    fill="white"  # 设置文字为白色，与黑色背景对比清晰
                )

            # 每 500ms 更新一次
            self.master.after(500, self.update_log)

    def update_image(self, state="initial"):
        """
        更新显示的图片
        :param state: 图片状态，可以是 "initial" 或 "activated"
        """
        if state == "initial":
            new_image = self.cat_image  # 默认静默状态图片
        elif state == "activated":
            new_image = self.cat_awake_image  # 激活模式图片

        # 清空当前 Canvas 内容并更新图片
        self.status_canvas.delete("all")
        self.status_canvas.create_image(0, 0, anchor="nw", image=new_image)
        self.status_canvas.image = new_image  # 防止图片被垃圾回收


    def start_drag(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def drag(self, event):
        x = self.master.winfo_x() + (event.x - self._offset_x)
        y = self.master.winfo_y() + (event.y - self._offset_y)
        self.master.geometry(f"+{x}+{y}")

    def update_status(self, is_awake):
        image = self.cat_awake_image if is_awake else self.cat_image
        self.status_canvas.delete("all")
        self.status_canvas.create_image(0, 0, anchor="nw", image=image)
        self.status_canvas.image = image

    def start_assistant(self):
        self.update_status(False)
        self.assistant.is_running = True
        self.assistant_thread = Thread(target=self.run_assistant_thread, daemon=True)
        self.assistant_thread.start()

    def run_assistant_thread(self):
        try:
            self.assistant.start()
        except Exception as e:
            print(f"Error: {e}")

    def stop_assistant(self):
        self.update_status(False)
        self.assistant.stop()

    def activate_mode(self):
        self.assistant.is_active = True
        self.update_image(state="activated")  # 更新图片为激活状态
        self.tts.speak("Yes, I am.")

    def silent_mode(self):
        self.assistant.is_active = False
        self.update_image(state="initial")  # 更新图片为静默状态
        self.tts.speak("Silent Mode.")

    def exit_program(self):
        self.master.destroy()







