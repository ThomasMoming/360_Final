import whisper
import numpy as np
import warnings
import os
import sys
from transformers import WhisperTokenizer

class SpeechToText:
    def __init__(self, model_name="base", language="en", device="cpu"):
        """
        Whisper 语音转文字模块
        :param model_name: Whisper 模型名称（默认 'base'）
        :param language: 语音语言（默认 'en'）
        :param device: 运行设备（默认 'cpu'）
        """
        # 获取程序运行的基路径，兼容 PyInstaller 打包环境
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        local_model_path = os.path.join(base_path, "local_model", "whisper_model", f"{model_name}.pt")
        tokenizer_dir = os.path.join(base_path, "local_model", "whisper_model")

        print(f"Model path: {local_model_path}")
        print(f"Tokenizer directory: {tokenizer_dir}")

        # 检查模型和分词器目录是否存在
        if not os.path.exists(local_model_path):
            raise FileNotFoundError(f"Whisper model file not found at: {local_model_path}")
        if not os.path.exists(tokenizer_dir):
            raise FileNotFoundError(f"Tokenizer directory not found at: {tokenizer_dir}")

        print(f"Loading Whisper model from: {local_model_path}")
        print(f"Loading Tokenizer from: {tokenizer_dir}")

        # 加载 Whisper 模型
        print(f"Loading model {model_name} with whisper.load_model()...")
        self.model = whisper.load_model(local_model_path, device=device)

        # 加载分词器（从目录加载）
        self.tokenizer = WhisperTokenizer.from_pretrained(tokenizer_dir)

        self.language = language

    def transcribe(self, audio_data, sample_rate=16000):
        """
        使用 Whisper 模型将音频数据转录为文本
        :param audio_data: 输入音频数据，numpy 数组格式
        :param sample_rate: 音频采样率（默认 16000 Hz）
        :return: 转录后的文本
        """
        # 转换音频数据为浮点数
        try:
            audio = audio_data.flatten().astype(np.float32)
        except Exception as e:
            print(f"Error flattening audio data: {e}")
            return ""

        # 检查采样率是否符合 Whisper 要求
        if sample_rate != 16000:
            print(f"Warning: Expected sample rate of 16000 Hz, but got {sample_rate}. Resampling might be needed.")

        # 使用 Whisper 模型进行转录
        try:
            result = self.model.transcribe(audio, language=self.language)
            return result['text'].lower()
        except Exception as e:
            print(f"Error during transcription: {e}")
            return ""
