class WordListReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.words = []

    def read_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                self.parse_line(line)

    def parse_line(self, line):
        parts = line.split(' ', 2)  # Split the line into three parts
        if len(parts) == 3:
            index, word, meaning = parts
            self.words.append({
                'index': index.strip(),
                'word': word.strip().replace('_', ' '),  # Replace underscores with spaces
                'meaning': meaning.strip()
            })

    def get_all(self):
        return self.words
    
    def get_word_list(self):
        # return a list of words
        return [word['word'] for word in self.words]

if __name__ == "__main__":
    reader = WordListReader('D:\Study\AIAgent\AIEnglishLearning\CET4_700.txt')
    reader.read_file()
    print(reader.get_all()[116])
