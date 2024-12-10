import sounddevice as sd
print(f"PortAudio Library Path: {sd._libname}")
import numpy as np
import queue
import os
import sys
import ctypes

class AudioProcessor:
    def __init__(self, sample_rate=16000, block_size=1024, channels=1):
        """
        音频处理模块：负责音频流的捕获和管理
        :param sample_rate: 采样率
        :param block_size: 每次录音处理的帧数
        :param channels: 音频通道数
        """

        # 如果在打包环境下运行，获取动态库路径
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        print(f"Base Path: {base_path}")
        lib_path = os.path.join(base_path, "libportaudio64bit.dll")

        try:
            ctypes.CDLL("libportaudio64bit.dll")
            print("PortAudio library loaded successfully!")
        except Exception as e:
            print(f"Failed to load PortAudio library: {e}")

        self.sample_rate = sample_rate
        self.block_size = block_size
        self.channels = channels
        self.audio_queue = queue.Queue()
        self.audio_buffer = np.zeros((0, channels))  # 初始化缓冲区

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Audio Callback Status: {status}")
        self.audio_queue.put(indata.copy())

    def start_stream(self):
        return sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self.audio_callback
        )
