import numpy as np
import string
from audio_processor import AudioProcessor
from speech_to_text import SpeechToText
from natural_language_understanding import NaturalLanguageUnderstanding
from text_to_speech import TextToSpeech
import os
import subprocess
import webbrowser
import requests


class VoiceAssistant:
    def __init__(self, wake_word="august", silent_word="december", ui=None):
        """
        主助手模块：整合各功能模块
        """
        self.ui = ui
        self.wake_word = wake_word.lower()
        self.silent_word = silent_word.lower()
        self.audio_processor = AudioProcessor()
        self.stt = SpeechToText()
        self.nlu = NaturalLanguageUnderstanding()
        self.tts = TextToSpeech()
        self.audio_buffer = np.zeros((0, self.audio_processor.channels))  # 初始化音频缓冲区

        # 状态控制
        self.is_active = False  # 初始状态为静默状态
        self.is_running = False  # 控制主循环是否运行


    def process_audio(self):
        """
        处理音频数据，执行唤醒词检测或意图解析
        """
        try:
            audio_to_process = self.audio_buffer.flatten().astype(np.float32)
            transcript = self.stt.transcribe(audio_to_process).strip()  # 去除多余空格
            print(f"STT: {transcript}")

            # 静默状态：只检测唤醒词
            if not self.is_active:
                if self.wake_word in transcript:
                    print("Wake word detected")
                    if self.ui:
                        self.ui.update_image(state="activated")  # 更新图片为激活模式
                        self.ui.activate_mode()  # 切换到激活模式
                    #self.tts.speak("Yes, I am.")
                    self.is_active = True
                return  # 静默状态下不进行 NLU 分析

            # 激活状态：处理用户意图
            if self.is_active:
                # 检测结束标志符
                if self.silent_word in transcript:
                    print("Silent word detected")
                    if self.ui:
                        self.ui.update_image(state="initial")  # 更新图片为静默模式
                        self.ui.silent_mode()  # 切换到静默模式
                    #self.tts.speak("Silent mode.")
                    self.is_active = False

                    return

                # 移除结束标志符，确保干净的输入
                transcript = transcript.replace(self.silent_word, "").strip()

                # 跳过空文本处理
                if not transcript:
                    print("Empty,Skip NLU.")
                    return

                self.respond_to_user(transcript)
        except Exception as e:
            print(f"Error processing audio: {e}")

    def find_and_open_executable(executable_name):
        """
        在所有本地硬盘中查找指定的可执行文件并打开它。

        :param executable_name: 需要查找的可执行文件名，例如 "Bilibili.exe"
        :return: 文件路径（如果找到），否则返回 None
        """
        try:
            # 获取所有硬盘的根目录
            drives = [f"{chr(65 + i)}:/" for i in range(26) if os.path.exists(f"{chr(65 + i)}:/")]

            # 遍历所有硬盘，查找文件
            for drive in drives:
                for root, dirs, files in os.walk(drive):
                    if executable_name in files:
                        return os.path.join(root, executable_name)  # 返回找到的文件路径
            return None  # 如果未找到文件，返回 None
        except Exception as e:
            print(f"Error while searching for the executable: {e}")
            return None

    def get_weather(self):
        """
        基于 IP 自动定位并获取实时天气信息，使用 Weatherstack API。
        :return: 天气描述字符串
        """
        try:
            # 使用 IP 定位服务获取城市
            ip_api_url = "http://ip-api.com/json/"
            ip_response = requests.get(ip_api_url)
            ip_response.raise_for_status()  # 如果请求失败，抛出异常
            location_data = ip_response.json()

            # 获取城市名称
            city = location_data.get("city", "Vancouver")  # 如果无法获取城市，使用默认值
            print(f"Detected City: {city}")  # 调试输出

            # 使用 Weatherstack API 获取天气
            api_key = "03a9fbf6ffd74371c0009e1865545f30"  # 替换为你的 Weatherstack API 密钥
            api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"

            # 请求天气数据
            weather_response = requests.get(api_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            # 检查是否成功返回数据
            if "current" in weather_data:
                temperature = weather_data["current"]["temperature"]
                description = weather_data["current"]["weather_descriptions"][0]
                city_name = weather_data["location"]["name"]

                # 返回格式化的天气信息
                return f"The current weather in {city_name} is  {temperature}°C."
            else:
                # 如果没有找到数据，返回错误消息
                return f"Unable to fetch weather information for {city}."
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return "Unable to fetch weather information at the moment."

    def respond_to_user(self, transcript):
        """
        解析用户意图并执行操作
        """
        try:
            # 清理命令文本
            command = transcript.replace(self.wake_word, "").replace(self.silent_word, "").strip()
            command = command.translate(str.maketrans("", "", string.punctuation))  # 移除标点
            intent = self.nlu.get_intent(command)

            # 调试输出
            print(f"Transcript: {transcript}")
            print(f"Cleaned Command: {command}")
            print(f"Detected Intent: {intent}")

            # 根据意图执行操作
            if intent == "Wechat":
                    Discord_path = r"D:\微信\WeChat\WeChat.exe"
                    # 检查文件是否存在
                    if os.path.exists(Discord_path):
                        # 尝试打开可执行文件
                        subprocess.Popen(Discord_path, shell=True)
                        self.tts.speak("Confirm.")
                    else:
                        # 文件未找到
                        self.tts.speak("Executable file.")

                    # executable_name = "Bilibili.exe"
                    # bilibili_path = self.find_and_open_executable(executable_name)  # 调用封装函数
                    #
                    # if bilibili_path:
                    #     try:
                    #         # 打开找到的文件
                    #         subprocess.Popen(bilibili_path, shell=True)
                    #         self.tts.speak("Confirm.")
                    #     except Exception as e:
                    #         # 如果打开失败
                    #         self.tts.speak("Unable open.")
                    #         print(f"Error open: {e}")
                    # else:
                    #     # 未找到文件
                    #     self.tts.speak("Executable file")

            elif intent == "weather report":
                self.tts.speak("Confirm.")
                weather_info = self.get_weather()  # 自动获取当地天气
                self.tts.speak(weather_info)
            elif intent == "Canvas":
                self.tts.speak("Confirm.")
                try:
                    # 指定要打开的链接
                    canvas_url = "https://canvas.sfu.ca/"
                    # 使用 webbrowser 模块在默认浏览器中打开链接
                    webbrowser.open(canvas_url)
                except Exception as e:
                    # 如果发生错误，进行语音播报并打印错误信息
                    self.tts.speak("Error open.")
                    print(f"Error open: {e}")
            elif intent == "GoSFU":
                self.tts.speak("Confirm.")
                try:
                    # 指定要打开的链接
                    canvas_url = "https://sims.erp.sfu.ca/psc/csprd/EMPLOYEE/SA/s/WEBLIB_SFU.ISCRIPT1.FieldFormula.IScript_CASSignin?&"
                    # 使用 webbrowser 模块在默认浏览器中打开链接
                    webbrowser.open(canvas_url)
                except Exception as e:
                    # 如果发生错误，进行语音播报并打印错误信息
                    self.tts.speak("Error open.")
                    print(f"Error open: {e}")
            elif intent == "outlook":
                self.tts.speak("Confirm.")
                try:
                    # 指定要打开的链接
                    canvas_url = "https://outlook.office365.com/mail/"
                    # 使用 webbrowser 模块在默认浏览器中打开链接
                    webbrowser.open(canvas_url)
                except Exception as e:
                    # 如果发生错误，进行语音播报并打印错误信息
                    self.tts.speak("Error open.")
                    print(f"Error open: {e}")
            else:
                self.tts.speak("Unauthorized Command.")
        except Exception as e:
            print(f"Error responding to user: {e}")

    def start(self):
        """
        启动语音助手
        """
        print("Starting voice assistant...")
        self.is_running = True
        try:
            with self.audio_processor.start_stream():
                while self.is_running:
                    if not self.audio_processor.audio_queue.empty():
                        data = self.audio_processor.audio_queue.get()
                        self.audio_buffer = np.append(self.audio_buffer, data, axis=0)

                        # 根据当前状态调整缓冲区时长
                        buffer_duration = 2 if not self.is_active else 5
                        if len(self.audio_buffer) > self.audio_processor.sample_rate * buffer_duration:
                            self.process_audio()
                            self.audio_buffer = np.zeros((0, self.audio_processor.channels))  # 清空缓冲区
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print(f"Error in voice assistant main loop: {e}")

    def stop(self):
        """
        停止语音助手
        """
        self.is_running = False
        self.is_active = False
        print("Voice assistant stopped.")


# import numpy as np
# import string
# from audio_processor import AudioProcessor
# from speech_to_text import SpeechToText
# from natural_language_understanding import NaturalLanguageUnderstanding
# from text_to_speech import TextToSpeech
#
# class VoiceAssistant:
#     def __init__(self, wake_word="august", silent_word="december"):
#         self.wake_word = wake_word.lower()
#         self.silent_word = silent_word.lower()
#         self.audio_processor = AudioProcessor()
#         self.stt = SpeechToText()
#         self.nlu = NaturalLanguageUnderstanding()
#         self.tts = TextToSpeech()
#         self.audio_buffer = np.zeros((0, self.audio_processor.channels))  # Initialize audio buffer
#         self.is_active = False  # Initial state: silent mode
#         self.is_running = False  # Control whether the main loop is running
#         self.log_messages = []  # Log storage
#
#     def add_log(self, message):
#         self.log_messages.append(message)
#         if len(self.log_messages) > 5:
#             self.log_messages.pop(0)
#
#     def process_audio(self):
#         try:
#             audio_to_process = self.audio_buffer.flatten().astype(np.float32)
#             transcript = self.stt.transcribe(audio_to_process).strip()  # Remove extra spaces
#             if transcript is None or len(transcript) == 0:
#                 print("Transcript is none or empty")
#             else:
#                 self.add_log(f"User: {transcript}")
#             print(f"Transcribed Text: {transcript}")
#             print(self.log_messages)
#
#             if not self.is_active:
#                 if self.wake_word in transcript:
#                     self.add_log("Wake word detected! Switching to active state.")
#                     print("Wake word detected! Switching to active state.")
#                     self.tts.speak("Yes, I am.")
#                     self.add_log("August: Yes, I am")
#                     self.is_active = True
#                 return  # In silent mode, only detect wake word
#
#             if self.is_active:
#                 if self.silent_word in transcript:
#                     self.add_log("Silent word detected! Switching to silent state.")
#                     print("Silent word detected! Switching to silent state.")
#                     self.tts.speak("Silent mode.")
#                     self.is_active = False
#                     return
#
#                 transcript = transcript.replace(self.silent_word, "").strip()
#                 if not transcript:
#                     print("Transcript is empty. Skipping NLU.")
#                     return
#
#                 self.respond_to_user(transcript)
#         except Exception as e:
#             self.add_log(f"Error processing audio: {e}")
#
#     def respond_to_user(self, transcript):
#         try:
#             command = transcript.replace(self.wake_word, "").replace(self.silent_word, "").strip()
#             command = command.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
#             intent = self.nlu.get_intent(command)
#
#             print(f"Transcript: {transcript}")
#             print(f"Cleaned Command: {command}")
#             print(f"Detected Intent: {intent}")
#
#             if intent == "turn on the light":
#                 self.tts.speak("Turning on the light.")
#                 self.add_log("August: Turning on the light")
#             elif intent == "turn off the light":
#                 self.tts.speak("Turning off the light.")
#                 self.add_log("August: Turning off the light")
#             elif intent == "weather report":
#                 self.tts.speak("Today's weather is sunny with a high of 25 degrees.")
#                 self.add_log("August: Today's weather is sunny with a high of 25 degrees.")
#             elif intent == "play music":
#                 self.tts.speak("Playing your favorite music now.")
#                 self.add_log("August: Playing your favorite music now.")
#             else:
#                 self.tts.speak("Sorry, I don't understand.")
#                 self.add_log("August: sorry, I don't understand.")
#         except Exception as e:
#             self.add_log(f"Error responding to user: {e}")
#
#     def start(self):
#         # self.add_log("Starting voice assistant...")
#         self.is_running = True
#         print("Starting voice assistant...")
#
#         try:
#             with self.audio_processor.start_stream():
#                 while self.is_running:
#                     if not self.audio_processor.audio_queue.empty():
#                         data = self.audio_processor.audio_queue.get()
#                         self.audio_buffer = np.append(self.audio_buffer, data, axis=0)
#                         buffer_duration = 2 if not self.is_active else 5
#                         if len(self.audio_buffer) > self.audio_processor.sample_rate * buffer_duration:
#                             self.process_audio()
#                             self.audio_buffer = np.zeros((0, self.audio_processor.channels))  # Clear buffer
#         except KeyboardInterrupt:
#             self.stop()
#         except Exception as e:
#             self.add_log(f"Error in voice assistant main loop: {e}")
#
#     def stop(self):
#         self.is_running = False
#         self.is_active = False
#         # self.add_log("Voice assistant stopped.")
#         print("Stopping voice assistant...")