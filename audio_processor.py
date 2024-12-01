import sounddevice as sd
import numpy as np
import queue


class AudioProcessor:
    def __init__(self, sample_rate=16000, block_size=1024, channels=1):
        """
        音频处理模块：负责音频流的捕获和管理
        :param sample_rate: 采样率
        :param block_size: 每次录音处理的帧数
        :param channels: 音频通道数
        """
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
