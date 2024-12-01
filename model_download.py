from transformers import AutoModelForSequenceClassification, AutoTokenizer

# 模型名称
model_name = "facebook/bart-large-mnli"

# 下载并保存模型和分词器
model = AutoModelForSequenceClassification.from_pretrained(model_name, cache_dir="./local_model")
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir="./local_model")

print("Model and tokenizer downloaded to ./local_model")
