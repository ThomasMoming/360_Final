# import pyttsx3
#
#
# class TextToSpeech:
#     def __init__(self):
#         """
#         文本转语音模块
#         """
#         self.tts_engine = pyttsx3.init()
#
#     def speak(self, text):
#         """
#         将文本转换为语音并播放
#         """
#         print(f"TTS Response: {text}")
#         self.tts_engine.say(text)
#         self.tts_engine.runAndWait()

import pyttsx3


class TextToSpeech:
    def __init__(self):
        """
        文本转语音模块
        """
        self.tts_engine = pyttsx3.init()
        self.set_english_voice()

    def set_english_voice(self):
        """
        设置语音为英语（Microsoft Zira Desktop - English (United States)）
        """
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            if "Microsoft Zira Desktop" in voice.name:
                self.tts_engine.setProperty('voice', voice.id)
                print(f"Selected English voice: {voice.name}")
                return
        print("No English voice found. Using default voice.")

    def speak(self, text):
        """
        将文本转换为语音并播放
        """
        print(f"TTS Response: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
