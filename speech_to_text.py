import whisper
import numpy as np


class SpeechToText:
    def __init__(self, model_name="base", language="en"):
        """
        Whisper 语音转文字模块
        """
        self.model = whisper.load_model(model_name)
        self.language = language

    def transcribe(self, audio_data):
        """
        使用 Whisper 模型将音频数据转录为文本
        """
        result = self.model.transcribe(audio_data.flatten().astype(np.float32), language=self.language)
        return result['text'].lower()
