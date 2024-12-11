import whisper
import numpy as np
import os
import sys
from shutil import copyfile
from transformers import WhisperTokenizer


class SpeechToText:
    def __init__(self, model_name="base", language="en", device="cpu"):
        """
        Whisper Speech-to-Text module with robust file handling.
        """
        # Check if running in PyInstaller environment
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS  # PyInstaller temporary directory
        else:
            base_path = os.path.abspath(".")  # Current working directory for non-frozen

        # Define paths
        local_model_dir = os.path.join(base_path, "local_model", "whisper_model")
        local_model_path = os.path.join(local_model_dir, f"{model_name}.pt")
        mel_filters_source = os.path.join(local_model_dir, "mel_filters.npz")
        multilingual_tiktoken_source = os.path.join(local_model_dir, "multilingual.tiktoken")
        gpt2_tiktoken_source = os.path.join(local_model_dir, "gpt2.tiktoken")

        whisper_assets_dir = os.path.join(os.path.dirname(whisper.__file__), "assets")
        mel_filters_target = os.path.join(whisper_assets_dir, "mel_filters.npz")
        multilingual_tiktoken_target = os.path.join(whisper_assets_dir, "multilingual.tiktoken")
        gpt2_tiktoken_target = os.path.join(whisper_assets_dir, "gpt2.tiktoken")

        print(f"Model path: {local_model_path}")
        print(f"Model directory: {local_model_dir}")
        print(f"Mel filters source path: {mel_filters_source}")
        print(f"Mel filters target path: {mel_filters_target}")
        print(f"Multilingual tiktoken source path: {multilingual_tiktoken_source}")
        print(f"Multilingual tiktoken target path: {multilingual_tiktoken_target}")
        print(f"GPT-2 tiktoken source path: {gpt2_tiktoken_source}")
        print(f"GPT-2 tiktoken target path: {gpt2_tiktoken_target}")

        # Ensure mel_filters.npz exists
        if not os.path.exists(mel_filters_source):
            print(f"{mel_filters_source} not found. Generating...")
            self._generate_mel_filters(mel_filters_source)

        # Ensure multilingual.tiktoken and gpt2.tiktoken exist
        for file_name, source_path, target_path in [
            ("mel_filters.npz", mel_filters_source, mel_filters_target),
            ("multilingual.tiktoken", multilingual_tiktoken_source, multilingual_tiktoken_target),
            ("gpt2.tiktoken", gpt2_tiktoken_source, gpt2_tiktoken_target)
        ]:
            if not os.path.exists(source_path):
                raise FileNotFoundError(f"{file_name} not found at {source_path}.")
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            copyfile(source_path, target_path)
            print(f"{file_name} copied to {target_path}")

        # Check model file existence
        if not os.path.exists(local_model_path):
            raise FileNotFoundError(f"Whisper model file not found at: {local_model_path}")

        # Load Whisper model
        print(f"Loading Whisper model from: {local_model_path}")
        self.model = whisper.load_model(local_model_path, device=device)

        # Load tokenizer
        try:
            print(f"Loading Tokenizer from: {local_model_dir}")
            self.tokenizer = WhisperTokenizer.from_pretrained(local_model_dir)
        except Exception as e:
            raise FileNotFoundError(f"Failed to load tokenizer from {local_model_dir}. Error: {e}")

        self.language = language

    def _generate_mel_filters(self, output_path):
        """
        Generate mel_filters.npz dynamically.
        """
        print("Generating mel_filters.npz...")
        import librosa
        mel_80 = librosa.filters.mel(sr=16000, n_fft=400, n_mels=80)
        mel_128 = librosa.filters.mel(sr=16000, n_fft=400, n_mels=128)
        np.savez_compressed(output_path, mel_80=mel_80, mel_128=mel_128)
        print(f"mel_filters.npz generated at {output_path}")

    def transcribe(self, audio_data, sample_rate=16000):
        """
        Transcribe audio to text using Whisper model.
        """
        try:
            audio = audio_data.flatten().astype(np.float32)
        except Exception as e:
            print(f"Error flattening audio data: {e}")
            return ""

        # Verify sample rate
        if sample_rate != 16000:
            print(f"Warning: Expected sample rate of 16000 Hz, got {sample_rate}. Resampling may be needed.")

        # Transcribe
        try:
            result = self.model.transcribe(audio, language=self.language)
            return result['text'].lower()
        except Exception as e:
            print(f"Error during transcription: {e}")
            return ""
