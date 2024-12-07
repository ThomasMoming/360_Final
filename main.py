# ----------------------------------------------------------
# test in terminal
# from voice_assistant import VoiceAssistant

# if __name__ == "__main__":
#     assistant = VoiceAssistant(wake_word="august")
#     assistant.start()
# ----------------------------------------------------------


# ----------------------------------------------------------
# one thread, model works, interface doesn't work.
# import tkinter as tk
# from voice_assistant import VoiceAssistant
#
#
# class AssistantGUI:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Voice Assistant")
#         self.master.geometry("400x200")
#
#         self.wake_word = "august"
#
#         # Create the VoiceAssistant instance
#         self.assistant = VoiceAssistant(wake_word=self.wake_word)
#
#         # GUI Components
#         self.label = tk.Label(master, text="Click to start the assistant", font=("Arial", 14))
#         self.label.pack(pady=20)
#
#         self.start_button = tk.Button(master, text="Start Assistant", command=self.start_assistant)
#         self.start_button.pack(pady=10)
#
#         self.quit_button = tk.Button(master, text="Quit", command=master.quit)
#         self.quit_button.pack(pady=10)
#
#     def start_assistant(self):
#         self.label.config(text="Listening for command...")
#         self.assistant.start()
#         # Optionally, add a callback or event to update this label when the assistant finishes or receives a command
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     gui = AssistantGUI(root)
#     root.mainloop()
# ----------------------------------------------------------



# ----------------------------------------------------------
# interface works, model doesn't work
import tkinter as tk
import threading
from voice_assistant import VoiceAssistant


class AssistantGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Voice Assistant")
        self.master.geometry("400x200")

        self.wake_word = "august"

        # Create the VoiceAssistant instance
        self.assistant = VoiceAssistant(wake_word=self.wake_word)

        # GUI Components
        self.label = tk.Label(master, text="Click to start the assistant", font=("Arial", 14))
        self.label.pack(pady=20)

        self.start_button = tk.Button(master, text="Start Assistant", command=self.start_assistant)
        self.start_button.pack(pady=10)

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack(pady=10)

    def start_assistant(self):
        self.label.config(text="Listening for command...")
        # Run the assistant in a separate thread to avoid blocking the GUI
        threading.Thread(target=self.assistant.start, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    gui = AssistantGUI(root)
    root.mainloop()

# ----------------------------------------------------------