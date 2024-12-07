from tkinter import Label, Button
from threading import Thread
from voice_assistant import VoiceAssistant  # 引入语音助手主模块
from text_to_speech import TextToSpeech


class VoiceAssistantUI:
    def __init__(self, master):
        self.tts = TextToSpeech()
        """
        初始化界面组件
        :param master: 主窗口
        """
        self.master = master
        self.master.title("Voice Assistant")
        self.master.geometry("400x300")

        # 状态标签
        self.status_label = Label(master, text="Status: Ready", font=("Helvetica", 14))
        self.status_label.pack(pady=20)

        # 开始按钮
        self.start_button = Button(
            master, text="Start Assistant", command=self.start_assistant, bg="green", fg="white"
        )
        self.start_button.pack(pady=10)

        # 停止按钮
        self.stop_button = Button(
            master, text="Stop Assistant", command=self.stop_assistant, bg="red", fg="white"
        )
        self.stop_button.pack(pady=10)

        # 切换到激活模式按钮
        self.activate_button = Button(
            master, text="Activate Mode", command=self.activate_mode, bg="blue", fg="white"
        )
        self.activate_button.pack(pady=10)

        # 切换到静默模式按钮
        self.silent_button = Button(
            master, text="Silent Mode", command=self.silent_mode, bg="gray", fg="white"
        )
        self.silent_button.pack(pady=10)

        # 退出按钮
        self.exit_button = Button(
            master, text="Exit", command=self.exit_program, bg="black", fg="white")
        self.exit_button.pack(pady=10)

        # 初始化语音助手
        self.assistant = VoiceAssistant(wake_word="august")  # 修改唤醒词为所需值
        self.assistant_thread = None  # 用于运行助手的线程



    def start_assistant(self):
        """
        开始语音助手
        """
        self.status_label.config(text="Status: Listening...")
        self.assistant.is_running = True  # 确保启动时标志为 True
        self.assistant_thread = Thread(target=self.assistant.start, daemon=True)
        self.assistant_thread.start()

    def stop_assistant(self):
        """
        停止语音助手
        """
        self.status_label.config(text="Status: Stopped")
        self.assistant.stop()  # 调用 VoiceAssistant 的 stop 方法

    def activate_mode(self):
        """
        将语音助手切换到激活模式
        """
        self.assistant.is_active = True
        self.status_label.config(text="Status: Activated")
        self.tts.speak("Active Mode.")

    def silent_mode(self):
        """
        将语音助手切换到静默模式
        """
        self.assistant.is_active = False
        self.status_label.config(text="Status: Silent")
        self.tts.speak("Silent Mode.")

    def exit_program(self):
        """
        退出程序
        """
        self.master.destroy()  # 关闭窗口
