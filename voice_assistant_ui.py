from tkinter import Label, Tk
from tkinter.ttk import Button
from threading import Thread
from voice_assistant import VoiceAssistant
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

        # 使用 ttk.Button 代替 tkinter.Button
        self.start_button = Button(master, text="Start Assistant", command=self.start_assistant)
        self.start_button.pack(pady=10)

        self.stop_button = Button(master, text="Stop Assistant", command=self.stop_assistant)
        self.stop_button.pack(pady=10)

        self.activate_button = Button(master, text="Activate Mode", command=self.activate_mode)
        self.activate_button.pack(pady=10)

        self.silent_button = Button(master, text="Silent Mode", command=self.silent_mode)
        self.silent_button.pack(pady=10)

        self.exit_button = Button(master, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=10)

        # 初始化语音助手
        self.assistant = VoiceAssistant(wake_word="august")
        self.assistant_thread = None

    def update_status(self, message):
        self.master.after(0, self.status_label.config, {"text": message})

    def start_assistant(self):
        self.update_status("Status: Listening...")
        self.assistant.is_running = True
        self.assistant_thread = Thread(target=self.run_assistant_thread, daemon=True)
        self.assistant_thread.start()

    def run_assistant_thread(self):
        try:
            self.assistant.start()
        except Exception as e:
            self.update_status(f"Error: {e}")

    def stop_assistant(self):
        self.update_status("Status: Stopped")
        self.assistant.stop()

    def activate_mode(self):
        self.assistant.is_active = True
        self.update_status("Status: Activated")
        self.tts.speak("Active Mode.")

    def silent_mode(self):
        self.assistant.is_active = False
        self.update_status("Status: Silent")
        self.tts.speak("Silent Mode.")

    def exit_program(self):
        self.master.destroy()
