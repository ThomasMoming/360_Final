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



from tkinter import Label, Tk
from tkinter.ttk import Button, Style
from PIL import Image, ImageTk
from PIL.Image import Resampling
from threading import Thread
from voice_assistant import VoiceAssistant
from text_to_speech import TextToSpeech
import time


class VoiceAssistantUI:
    def __init__(self, master):
        self.tts = TextToSpeech()
        self.text_log = []  # To store the recent text logs

        self.master = master
        self.master.title("Voice Assistant")
        self.master.geometry("480x530")
        self.master.configure(bg=None)

        # Load and resize the images
        self.initial_image_path = "images/cat.png"  # Initial state image
        self.cat_image_path = "images/cat_start.png"  # Listening state image
        self.cat_awake_image_path = "images/cat_awake.png"  # Activated state image

        self.photo_initial = self.load_image(self.initial_image_path, (300, 350))
        self.photo = self.load_image(self.cat_image_path, (300, 350))
        self.photo_awake = self.load_image(self.cat_awake_image_path, (300, 350))

        # Load the cat's name as an image
        name_image = Image.open("images/name.png")
        name_image = name_image.resize((216, 60), Resampling.LANCZOS)
        self.name_photo = ImageTk.PhotoImage(name_image)

        # Status label on top of the image
        self.status_label = Label(master, text="August: Ready", font=("Comic Sans MS", 14), fg="black", width=20)
        self.status_label.grid(row=1, column=3)

        # Add the image to a label
        self.image_label = Label(master, image=self.photo_initial)
        self.image_label.grid(row=1, column=0, rowspan=7,columnspan=3)

        # Display the cat's name as an image
        self.name_label = Label(master, image=self.name_photo)
        self.name_label.grid(row=0, column=0, columnspan=4)

        # Define a custom style for buttons
        self.style = Style()
        self.style.configure("Custom.TButton",
                             font=("Comic Sans MS", 12),
                             relief="flat",
                             borderwidth=0,
                             background="white",
                             activebackground="orange",
                             foreground="black",
                             activeforeground="white")

        # Initial visibility state for the additional buttons
        self.show_buttons = False

        # Buttons
        self.main_button = Button(master, text="Menu", command=self.toggle_buttons, style="Custom.TButton")
        self.main_button.grid(row=2, column=3)

        self.start_button = Button(master, text="Start Assistant", command=self.start_assistant, style="Custom.TButton")
        self.stop_button = Button(master, text="Stop Assistant", command=self.stop_assistant, style="Custom.TButton")
        self.activate_button = Button(master, text="Activate Mode", command=self.activate_mode, style="Custom.TButton")
        self.silent_button = Button(master, text="Silent Mode", command=self.silent_mode, style="Custom.TButton")
        self.exit_button = Button(master, text="Exit", command=self.exit_program, style="Custom.TButton")

        # Pack the additional buttons conditionally
        self.update_button_visibility()

        # Initialize the voice assistant
        self.assistant = VoiceAssistant(wake_word="august")
        self.assistant_thread = None

        self.log_label = Label(master, text="", font=("Comic Sans MS", 14), justify="left", wraplength=420, bg="orange",
                               fg="black",pady=2)
        self.log_label.grid(row=8, column=1, columnspan=3, sticky="nsew")  # sticky to make it expand in the whole row
        self.conversation_label = Label(master, text="Chat", font=("Comic Sans MS", 20, ), justify="left", wraplength=420, bg="orange",
                               fg="black")
        self.conversation_label.grid(row=8, column=0,sticky="nsew")
        # Configure grid row to have the orange background
        master.grid_rowconfigure(8, weight=1, uniform="row")

        self.update_log_display()

    def load_image(self, path, size):
        image = Image.open(path)
        image = image.resize(size, Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def update_image(self, state="initial"):
        if state == "initial":
            new_image = self.photo_initial
        elif state == "listening":
            new_image = self.photo
        elif state == "activated":
            new_image = self.photo_awake
        self.image_label.config(image=new_image)
        self.image_label.image = new_image

    def update_status(self, message):
        self.master.after(0, self.status_label.config, {"text": message})

    def update_log(self, message, header=""):
        # Add the new message to the log and update the UI
        self.text_log.append(f"{message}")
        if len(self.text_log) > 5:
            self.text_log.pop(0)  # Keep only the last 5 logs
        self.log_label.config(text="\n".join(self.text_log))

    def update_log_display(self):
        # Periodically check for new log messages and update the UI
        self.master.after(1000, self.update_log_display)
        if self.assistant and self.assistant.log_messages:
            latest_message = self.assistant.log_messages[-1]
            if latest_message not in self.text_log:
                self.update_log(latest_message)

    def start_assistant(self):
        self.update_status("August is listening..")
        self.update_image(state="listening")
        self.assistant.is_running = True
        self.assistant_thread = Thread(target=self.run_assistant_thread, daemon=True)
        self.assistant_thread.start()
        self.update_log("August: assistant started")

    def run_assistant_thread(self):
        try:
            time.sleep(0.1)  # Block for 10 seconds
            self.assistant.start()
        except Exception as e:
            self.update_status(f"Error: {e}")

    def stop_assistant(self):
        self.update_status("August: stopped")
        self.update_image(state="initial")
        self.assistant.stop()
        self.update_log("August: assistant stopped")

    def activate_mode(self):
        self.assistant.is_active = True
        self.update_status("August: activated")
        self.update_image(state="activated")
        self.tts.speak("Active Mode.")
        self.update_log("August: active mode")

    def silent_mode(self):
        self.assistant.is_active = False
        self.update_status("August: silent")
        self.update_image(state="listening")
        self.tts.speak("Silent Mode.")
        self.update_log("August: silent mode")

    def exit_program(self):
        self.master.destroy()
        self.update_log("August: program exited")

    def toggle_buttons(self):
        self.show_buttons = not self.show_buttons
        self.update_button_visibility()

    def update_button_visibility(self):
        if self.show_buttons:
            self.start_button.grid(row=3, column=3)
            self.stop_button.grid(row=4, column=3)
            self.activate_button.grid(row=5, column=3)
            self.silent_button.grid(row=6, column=3)
            self.exit_button.grid(row=7, column=3)
        else:
            self.start_button.grid_forget()
            self.stop_button.grid_forget()
            self.activate_button.grid_forget()
            self.silent_button.grid_forget()
            self.exit_button.grid_forget()

