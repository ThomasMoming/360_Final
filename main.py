import tkinter as tk
from voice_assistant_ui import VoiceAssistantUI
import sys
import time
from threading import Thread
import librosa
import librosa.display



if __name__ == "__main__":
    # 创建主窗口

    # # 定义定时刷新 stdout 的函数
    # def flush_stdout_periodically():
    #     while True:
    #         sys.stdout.flush()
    #         time.sleep(0.5)  # 每隔 0.5 秒刷新一次
    #
    #
    # # 启动刷新线程
    # Thread(target=flush_stdout_periodically, daemon=True).start()
    root = tk.Tk()
    gui = VoiceAssistantUI(root)  # 初始化界面类
    root.mainloop()