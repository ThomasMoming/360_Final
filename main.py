import tkinter as tk
from voice_assistant_ui import VoiceAssistantUI

if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    gui = VoiceAssistantUI(root)  # 初始化界面类
    root.mainloop()