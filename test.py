from natural_language_understanding import NaturalLanguageUnderstanding
import pyttsx3
import os
import subprocess
# 测试代码
if __name__ == "__main__":
    # # 指定本地模型路径
    # local_model_path = "./local_model/models--facebook--bart-large-mnli/snapshots/d7645e127eaf1aefc7862fd59a17a5aa8558b8ce"
    # nlu = NaturalLanguageUnderstanding(local_model_path=local_model_path)
    #
    # # 测试输入
    # texts = [
    #     "Please turn on the lights.",
    #     "Can you tell me the weather?",
    #     "Turn off the lights.",
    #     "Play some music.",
    #     "Set an alarm for 7 AM.",
    #     "What time is it now?"
    # ]
    #
    # for text in texts:
    #     intent = nlu.get_intent(text)
    #     print(f"Input: {text}, Intent: {intent}")


    # engine = pyttsx3.init()
    # voices = engine.getProperty('voices')
    # for voice in voices:
    #     print(f"Voice ID: {voice.id}")
    #     print(f"Name: {voice.name}")
    #     print(f"Languages: {voice.languages}")
    #     print("-" * 20)




    def open_discord():
        # 检查仅文件路径是否存在
        Discord_exe_path = r"C:\Users\15694\AppData\Local\Discord\Update.exe"

        if os.path.exists(Discord_exe_path):  # 检查 Update.exe 是否存在
            # 构造完整的启动命令
            command = f'"{Discord_exe_path}" --processStart Discord.exe'
            try:
                # 尝试打开可执行文件
                subprocess.Popen(command, shell=True)
                print("Confirm.")  # 或者调用 TTS
            except Exception as e:
                print(f"Error: Unable to open Discord. {e}")
        else:
            # 文件未找到
            print("Executable file not found.")  # 或者调用 TTS


    # 调用函数测试
    open_discord()


