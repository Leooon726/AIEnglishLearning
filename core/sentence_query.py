from .ark_model_completion import ArkModelCompletion
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ParagraphGenerator:
    def __init__(self, model=None, use_reflection=True):
        self.model = model if model else ArkModelCompletion()
        self.use_reflection = use_reflection
        logging.info("ParagraphGenerator initialized.")

    def get_target_words_from_target_words_and_meanings(self, target_words_and_meanings):
        target_words = [word for word, _ in target_words_and_meanings]
        return target_words

    def generate(self, target_words_and_meanings):
        target_words = self.get_target_words_from_target_words_and_meanings(target_words_and_meanings)
        logging.info(f"Generating paragraph with target words: {target_words}")
        original_english_paragraph = self.generate_original_paragraph(target_words, target_words_and_meanings)

        if self.use_reflection:
            reflection_response = self.reflect_on_paragraph(original_english_paragraph, target_words)
        else:
            reflection_response = original_english_paragraph
        return reflection_response, self.translate(reflection_response, target_words)

    def generate_original_paragraph(self, target_words, target_words_and_meanings):
        logging.info("Generating original paragraph.")
        system_content = (
            "你是一个美国作家，擅长根据给定的单词列表，写出合理优美且可以作为英语学习材料的文段。"
            "当用户提供[目标单词列表]，你需要给出一个英语文段，所有[目标单词列表]的单词都需要用上。"
            "要求：\n"
            "1. 单词在文段中的用法，需要和[单词释义]中一致； \n"
            "2. 内容需要轻松有趣；\n"
            "3. 需要有画面感，涉及到场景和动作；\n"
            "4. 有故事性，需要涉及特定人物；\n"
            "5. 文义需要简单易懂，合乎逻辑；\n"
            "6. 文段中所有目标单词都需要加粗，如果目标单词用到多次，每次都需要加粗；\n"
            "7. 除了目标单词，其余的单词要尽量地简单，句式也要尽量地简单；\n"
            "8. 给出的文段不要有无效句子。\n"
            "9. 避免使用第一、二人称，尽量用具体的人名和事物代替‘I’、‘you’、‘he’等\n"
            "10. 句子之间需要过渡自然，必要的时候使用过渡词 \n"
            "举例：\n"
            "user: 目标单词：geology, geometry, seminar, principle\n 单词释义： geology: n. 地质学, geometry: n. 几何学, seminar: n. 研讨会, principle: n. 原则\n"
            "response: One day, I attended a **seminar** about **geology**. The speaker explained the complex principles of different rock formations. I was really fascinated. And then, I started to think about how these geological structures relate to the concepts in **geometry**. It was an interesting experience to connect these two fields. \n\n"
        )

        word_and_meaning_str = ', '.join([f'{word}: {meaning}' for word, meaning in target_words_and_meanings])
        user_content = f"目标单词：{', '.join(target_words)} \n单词释义：{word_and_meaning_str}"
        response = self.model.query_model(system_content, user_content)
        logging.info("Original paragraph generated.")
        return response

    def reflect_on_paragraph(self, original_paragraph, target_words):
        logging.info("Reflecting on the original paragraph.")
        reflection_system_content = (
            "反思[原始文段]，\n"
            "任务：\n"
            "1. 指出[原始文段]中不合乎逻辑的部分。\n"
            "2. 指出对文意没有帮助的冗余的句子。\n"
            "3. 重新修改得到新的文段。\n"
            "4. 检查[目标单词]是否都有加粗，没有的话需要补上。\n"
            "要求：\n"
            "1. [目标单词]都需要被使用到。\n"
            "2. 文段中需要涉及具体的人物，有故事情节。\n"
            "举例：\n"
            "user: 目标单词：\n"
            "原始文段： One day, Tom saw some people doing **illegal** business on the street. "
            "He immediately reported it to the government. The government then took measures to **prohibit** such activities "
            "and made a series of regulations to **regulate** the market order. They not only set up clear signs to remind "
            "people not to engage in illegal actions but also strengthened supervision. "
            "Thanks to these efforts, the situation in the city improved significantly.\n"
            "response: [反思] ：1. 'Thanks to these efforts, the situation in the city improved significantly.' 既没有用到目标单词，也没有增加文段的故事性，所以可以去掉。\n"
            "2. 'engage in illegal actions'中illegal没有加粗。\n\n"
            "[更正]： One day, Tom saw some people doing **illegal** business on the street. "
            "He immediately reported it to the government. The government then took measures to **prohibit** such activities "
            "and made a series of regulations to **regulate** the market order. They not only set up clear signs to remind "
            "people not to engage in **illegal** actions but also strengthened supervision."
        )

        reflect_user_content = f"目标单词：{', '.join(target_words)} \n原始文段： {original_paragraph}"
        result = self.model.query_model(reflection_system_content, reflect_user_content)
        reflection_part, improved_part = result.split("[更正]：") if "[更正]：" in result else (result, "")
        logging.info("Reflection completed: %s", reflection_part)
        return improved_part

    def translate(self, paragraph, target_words):
        logging.info("Translating paragraph to Chinese.")
        system_content = (
            "将[英语文段]翻译成中文得到[中文文段]，对[中文文段]中对应的[目标单词]词语加粗。\n"
            "举例：\n"
            "user: [英语文段] John lives in a peaceful suburb. Every morning, he takes the subway to his office. "
            "After getting off the subway, he has to walk along a busy avenue. This has become a daily routine "
            "that John is quite accustomed to.\n"
            "[目标单词] avenue, suburb, subway\n"
            "response: 约翰住在一个宁静的**郊区**。每天早晨，他都会乘坐**地铁**去办公室。"
            "下了**地铁**后，他需要沿着一条繁忙的**大道**步行。这已经成为了约翰习以为常的日常。\n"
        )

        user_content = f"[英语文段]: {paragraph}\n[目标单词]: {', '.join(target_words)}"
        response = self.model.query_model(system_content, user_content)
        logging.info("Translation completed.")
        return response

if __name__ == "__main__":
    ark_model = ArkModelCompletion()
    paragraph_generator = ParagraphGenerator(ark_model)
    target_words_and_meanings = [('catalog', 'n. 目录（册） v. 编目'), ('calendar', 'n. 日历，月历'), ('valid', 'a. 有效的，有根据的；正当的')]
    paragraph, translation = paragraph_generator.generate(target_words_and_meanings)
    print(paragraph,'\n\n', translation)
    # step by step testing
    # target_words = paragraph_generator.get_target_words_from_target_words_and_meanings(target_words_and_meanings)
    # print(target_words)
    # original_english_paragraph = paragraph_generator.generate_original_paragraph(target_words, target_words_and_meanings)
    # print("Original English Paragraph:", original_english_paragraph)
    
