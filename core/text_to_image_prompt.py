class TextToImagePrompt:
    def __init__(self):
        self.template = "帮我生成图片：图片风格为「卡通」，比例为「1:1」，内容描述：{}"

    def generate_prompt(self, text):
        return self.template.format(text)

if __name__ == "__main__":
    text_to_image_prompt = TextToImagePrompt()
    print(text_to_image_prompt.generate_prompt("我在一个公园里，看到一只小狗在追逐一只蝴蝶。"))
