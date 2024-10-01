import csv
import gensim
from word_list_reader import WordListReader

class WordVectorManager:
    def __init__(self, glove_file):
        self.glove_file = glove_file
        self.glove_vectors = None

    def load_glove_vectors(self):
        if self.glove_vectors is None:
            self.glove_vectors = gensim.models.KeyedVectors.load_word2vec_format(self.glove_file, binary=False, no_header=True)

    def get_vector_and_save_to_csv(self, word_dicts, csv_file):
        self.load_glove_vectors()  # Ensure GloVe vectors are loaded
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['index', 'word', 'meaning', 'vector'])
            for word_dict in word_dicts:
                word = word_dict['word']
                if word in self.glove_vectors:
                    vector = self.glove_vectors[word].tolist()
                else:
                    print(f"Word '{word}' not found in GloVe vectors.")
                    vector = None
                writer.writerow([word_dict['index'], word, word_dict['meaning'], vector])

    def load_from_csv(self, csv_file):
        word_dicts = []
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                vector_str = row['vector']
                if vector_str.strip():  # Check if the vector string is not empty
                    row['vector'] = eval(vector_str)  # Convert string representation of list back to list
                else:
                    row['vector'] = []  # Assign an empty list if the vector is empty
                word_dicts.append(row)
        return word_dicts

if __name__ == "__main__":
    word_list_reader = WordListReader('D:\Study\AIAgent\AIEnglishLearning\CET4_700.txt')
    word_list_reader.read_file()
    word_list_reader.get_word_list()
    word_dicts = word_list_reader.get_all()

    glove_file = 'D:\Study\AIAgent\AIEnglishLearning\core\glove.42B.300d.txt'  # Adjust this path if necessary
    manager = WordVectorManager(glove_file)
    csv_file = 'D:\Study\AIAgent\AIEnglishLearning\output\CET4_700_word_vectors.csv'
    manager.get_vector_and_save_to_csv(word_dicts, csv_file)
    loaded_word_dicts = manager.load_from_csv(csv_file)
