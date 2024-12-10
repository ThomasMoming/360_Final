import sys,os
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
        sys.stdout = sys.__stdout__
        print("Standard output restored to console.")

        # # 保存原始 stdout
        # self.original_stdout = sys.stdout
        #
        # # 初始化日志存储
        # self.console_output = StringIO()
        #
        # # 重定向 stdout 到 MultiStream，同时写入到 PyCharm Terminal 和 StringIO
        # sys.stdout = MultiStream(self.original_stdout, self.console_output)
        # print(f"After MultiStream sys.stdout: {type(sys.stdout)}")



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
        # 打包后的环境，使用 sys._MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        full_path = os.path.join(base_path, path)

        # 加载图片
        img = Image.open(full_path)
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
            # ("Log", self.show_log_canvas),
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

    # def show_log_canvas(self):
    #     """
    #     显示或隐藏日志 Canvas
    #     """
    #     if self.log_canvas:  # 如果 log_canvas 已经存在
    #         self.log_canvas.destroy()  # 销毁 Canvas（隐藏日志）
    #         self.log_canvas = None  # 重置 log_canvas 为 None
    #     else:
    #         # 创建新的日志显示区域
    #         self.log_canvas = Canvas(self.master, width=350, height=50, bg="black")
    #         self.log_canvas.place(x=self.status_canvas.winfo_x() - 110, y=self.status_canvas.winfo_y() + 170)
    #
    #         # 更新日志内容
    #         self.update_log()
    #
    # def update_log(self):
    #     """
    #     实时更新日志内容
    #     """
    #     if self.log_canvas:
    #         # 获取完整的日志
    #         logs = self.console_output.getvalue().split("\n")
    #
    #         # 显示最后的 3 行日志
    #         self.log_canvas.delete("all")  # 清除旧内容
    #         for i, log in enumerate(logs[-3:]):  # 保留最后 3 行
    #             self.log_canvas.create_text(
    #                 5, i * 18,  # 设置行间距
    #                 anchor="nw",
    #                 text=log,
    #                 font=("Arial", 10, "bold"),
    #                 fill="white"
    #             )
    #
    #         # 每 500ms 更新一次
    #         self.master.after(500, self.update_log)

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
        sys.stdout = sys.__stdout__
        print("Restored sys.stdout to default in run_assistant_thread.")

        self.assistant_thread = Thread(target=self.run_assistant_thread, daemon=True)
        self.assistant_thread.start()

    def run_assistant_thread(self):
        try:
            sys.stdout = sys.__stdout__
            print("Restored sys.stdout to default in run_assistant_thread.")
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







