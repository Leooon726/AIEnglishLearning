import csv
from datetime import datetime

class VideoInfoCollector:
    def __init__(self, csv_file_path=None):
        # Get the current time for the file name
        if csv_file_path is None:
            self.current_time = str(datetime.now().strftime("%m%d%H%M%S"))
            self.csv_file_path = f"D:\\Study\\AIAgent\\AIEnglishLearning\\output\\info_for_video_generation_{self.current_time}.csv"
        else:
            self.csv_file_path = csv_file_path
        print('VideoInfoCollector csv_file_path:', self.csv_file_path)
        self.header = ['index', 'image_prompt', 'target_words_and_meanings', 'clean_paragraph', 'bold_words', 'clean_translation', 'bold_word_meanings', 'audio_path']
        
        # Initialize the CSV file with header
        with open(self.csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(self.header)

    def write(self, index, image_prompt, target_words_and_meanings, clean_paragraph, bold_words, clean_translation, bold_word_meanings, audio_path):
        # Save the data to the CSV file
        with open(self.csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow([index, image_prompt, target_words_and_meanings, clean_paragraph, bold_words, clean_translation, bold_word_meanings, audio_path])

class VideoInfoReader:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path

    def read(self):
        # Read the CSV file row by row
        with open(self.csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';', quotechar='"')
            header = next(reader)
            for row in reader:
                yield {header[i]: eval(row[i]) if header[i] in ['bold_words', 'bold_word_meanings', 'target_words_and_meanings'] else row[i] for i in range(len(header))}
