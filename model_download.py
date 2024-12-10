# from transformers import AutoModelForSequenceClassification, AutoTokenizer
#
# # 模型名称
# model_name = "facebook/bart-large-mnli"
#
# # 下载并保存模型和分词器
# model = AutoModelForSequenceClassification.from_pretrained(model_name, cache_dir="./local_model")
# tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir="./local_model")
#
# print("Model and tokenizer downloaded to ./local_model")


import os
import shutil
import whisper


def download_whisper_model(model_name="base", target_dir="local_model/whisper_model"):
    """
    下载 Whisper 模型到指定文件夹。
    :param model_name: Whisper 模型名称（例如 'base', 'small', 'medium', 'large'）
    :param target_dir: 模型保存的目标目录
    """
    # 创建目标目录
    os.makedirs(target_dir, exist_ok=True)

    # 下载并加载模型
    print(f"Downloading Whisper model: {model_name}")
    model = whisper.load_model(model_name)

    # 获取 Hugging Face 缓存目录路径
    cache_dir = os.path.expanduser("~/.cache/huggingface/hub/models--openai--whisper-{}/snapshots/".format(model_name))
    print(f"Cache directory: {cache_dir}")

    # 检查缓存目录是否存在
    if not os.path.exists(cache_dir):
        print(f"Error: Cache directory '{cache_dir}' does not exist.")
        return

    # 需要的模型文件
    model_files = ["vocab.json", "merges.txt", f"{model_name}.pt", "tokenizer.json"]

    # 复制文件到目标目录
    for root, dirs, files in os.walk(cache_dir):
        for file_name in model_files:
            if file_name in files:
                source_path = os.path.join(root, file_name)
                target_path = os.path.join(target_dir, file_name)
                shutil.copy(source_path, target_path)
                print(f"Copied {file_name} to {target_path}")

    print(f"Whisper model '{model_name}' successfully downloaded to {target_dir}.")


# 调用函数下载模型
download_whisper_model(model_name="base", target_dir="local_model/whisper_model")


