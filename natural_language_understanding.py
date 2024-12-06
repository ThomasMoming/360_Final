from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer


class NaturalLanguageUnderstanding:
    def __init__(self, local_model_path="./local_model/models--facebook--bart-large-mnli/snapshots/d7645e127eaf1aefc7862fd59a17a5aa8558b8ce"):
        """
        自然语言理解模块：使用本地 Zero-shot Classification 模型
        """
        # 加载本地模型和分词器
        self.tokenizer = AutoTokenizer.from_pretrained(local_model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(local_model_path)

        # 使用本地模型和分词器创建 Zero-shot Classification pipeline
        self.classifier = pipeline(
            "zero-shot-classification",
            model=self.model,
            tokenizer=self.tokenizer
        )

    def get_intent(self, text):
        """
        预测用户意图
        :param text: 用户输入文本
        :return: 预测的意图标签
        """
        # 检查输入是否为空
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty.")

        # 定义预设的意图标签
        candidate_labels = [
            "turn on the light",
            "turn off the light",
            "weather report",
            "play music",
            "set an alarm",
            "check the current time"
        ]

        # 检查候选标签是否为空
        if not candidate_labels:
            raise ValueError("Candidate labels cannot be empty.")

        # 使用 Zero-shot Classification 模型进行预测
        result = self.classifier(text, candidate_labels)
        print(f"Classification Result: {result}")

        # 返回最高分对应的意图
        return result['labels'][0]
