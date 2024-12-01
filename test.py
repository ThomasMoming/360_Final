from natural_language_understanding import NaturalLanguageUnderstanding

# 测试代码
if __name__ == "__main__":
    # 指定本地模型路径
    local_model_path = "./local_model"
    nlu = NaturalLanguageUnderstanding(local_model_path=local_model_path)

    # 测试输入
    texts = [
        "Please turn on the lights.",
        "Can you tell me the weather?",
        "Turn off the lights.",
        "Play some music.",
        "Set an alarm for 7 AM.",
        "What time is it now?"
    ]

    for text in texts:
        intent = nlu.get_intent(text)
        print(f"Input: {text}, Intent: {intent}")


