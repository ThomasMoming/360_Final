import whisper
import sounddevice as sd
import numpy as np
import queue


class RealTimeTranscriber:
    def __init__(self, model_name="base", language="en", sample_rate=16000, block_size=1024, channels=1):
        """
        初始化实时语音转文字类
        :param model_name: Whisper 模型名称（如 tiny, base, small, medium, large）
        :param language: 语言代码（如 "en" 表示英语，"zh" 表示中文）
        :param sample_rate: 采样率（默认 16000，Whisper 推荐）
        :param block_size: 每次录音处理的帧数
        :param channels: 声道数量（默认 1，单声道）
        """
        self.model = whisper.load_model(model_name)  # 加载指定大小的 Whisper 模型
        self.language = language  # 转录语言
        self.sample_rate = sample_rate  # 采样率
        self.block_size = block_size  # 每次处理的帧数
        self.channels = channels  # 声道数
        self.audio_queue = queue.Queue()  # 队列，用于存储音频数据
        self.audio_buffer = np.zeros((0, channels))  # 初始化音频缓冲区

    def audio_callback(self, indata, frames, time, status):
        """
        音频流回调函数，实时接收音频数据
        :param indata: 捕获的音频数据
        :param frames: 当前音频数据的帧数
        :param time: 音频时间信息
        :param status: 当前音频流状态
        """
        if status:  # 如果有状态（如错误），打印信息
            print(status, flush=True)
        self.audio_queue.put(indata.copy())  # 将音频数据放入队列

    def process_audio(self):
        """
        处理缓冲区中的音频，并使用 Whisper 模型进行转录
        """
        # 从缓冲区获取音频并转换为 Whisper 格式
        audio_to_process = self.audio_buffer.flatten().astype(np.float32)
        # 使用 Whisper 转录
        result = self.model.transcribe(audio_to_process, language=self.language)
        print(f"Transcribed Text: {result['text']}")  # 打印转录结果
        # 清空缓冲区
        self.audio_buffer = np.zeros((0, self.channels))

    def start(self):
        """
        启动实时语音转文字功能
        """
        try:
            print("Starting real-time transcription...")
            # 打开音频输入流
            with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, callback=self.audio_callback):
                while True:
                    # 获取队列中的音频数据并追加到缓冲区
                    data = self.audio_queue.get()
                    self.audio_buffer = np.append(self.audio_buffer, data, axis=0)

                    # 如果缓冲区超过 5 秒音频长度，进行转录
                    if len(self.audio_buffer) > self.sample_rate * 5:
                        print("Processing audio...")
                        self.process_audio()

        except KeyboardInterrupt:
            print("\nStopping transcription...")
        except Exception as e:
            print(f"An error occurred: {e}")


# 示例用法
if __name__ == "__main__":
    # 创建转录器实例，选择模型 "base"，语言为英语
    transcriber = RealTimeTranscriber(model_name="base", language="en")
    transcriber.start()
