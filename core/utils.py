import re

def get_clean_text_and_bold_words(text):
    bold_words = re.findall(r'\*\*(.*?)\*\*', text)
    clean_text = re.sub(r'\*\*.*?\*\*', lambda match: match.group(0)[2:-2], text)
    return clean_text, bold_words

if __name__ == "__main__":
    # print(get_clean_text_and_bold_words("**hello** world **python**."))
    print(get_clean_text_and_bold_words("**一二**三四 **五六**."))


