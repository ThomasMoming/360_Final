import pyttsx3


class TextToSpeech:
    def __init__(self):
        """
        文本转语音模块
        """
        self.tts_engine = pyttsx3.init()

    def speak(self, text):
        """
        将文本转换为语音并播放
        """
        print(f"TTS Response: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
