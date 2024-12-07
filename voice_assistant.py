import numpy as np
import string
from audio_processor import AudioProcessor
from speech_to_text import SpeechToText
from natural_language_understanding import NaturalLanguageUnderstanding
from text_to_speech import TextToSpeech


class VoiceAssistant:
    def __init__(self, wake_word="august", silent_word="december"):
        """
        主助手模块：整合各功能模块
        """
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
            print(f"Transcribed Text: {transcript}")

            # 静默状态：只检测唤醒词
            if not self.is_active:
                if self.wake_word in transcript:
                    print("Wake word detected! Switching to active state.")
                    self.tts.speak("Yes, I am.")
                    self.is_active = True
                return  # 静默状态下不进行 NLU 分析

            # 激活状态：处理用户意图
            if self.is_active:
                # 检测结束标志符
                if self.silent_word in transcript:
                    print("Silent word detected! Switching to silent state.")
                    self.tts.speak("Silent mode.")
                    self.is_active = False
                    return

                # 移除结束标志符，确保干净的输入
                transcript = transcript.replace(self.silent_word, "").strip()

                # 跳过空文本处理
                if not transcript:
                    print("Transcript is empty. Skipping NLU.")
                    return

                self.respond_to_user(transcript)
        except Exception as e:
            print(f"Error processing audio: {e}")

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
            if intent == "turn on the light":
                self.tts.speak("Turning on the light.")
            elif intent == "turn off the light":
                self.tts.speak("Turning off the light.")
            elif intent == "weather report":
                self.tts.speak("Today's weather is sunny with a high of 25 degrees.")
            elif intent == "play music":
                self.tts.speak("Playing your favorite music now.")
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


