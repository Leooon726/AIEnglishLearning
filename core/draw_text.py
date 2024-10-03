from PIL import Image, ImageDraw
import re

class DrawChineseText:
    def __init__(self, article, font, draw, width, line_height, fill="black", position=(0, 0), highlighted_words=None, highlight_color="red"):
        self.width = width
        self.position = position
        self.fill = fill
        self.font = font
        self.line_height = line_height
        self.article = article
        self.draw = draw
        self.highlighted_words = sorted(highlighted_words, key=len, reverse=True) if highlighted_words else []
        self.highlight_color = highlight_color
        self.all_lines = self.split_lines()

    def get_line_height(self):
        return self.draw.textbbox((0, 0), "汉", font=self.font)[3] - self.draw.textbbox((0, 0), "汉", font=self.font)[1]

    def split_text_to_words(self, text):
        '''
        Splits the input text into a list of Chinese characters, English words, spaces, and punctuation,
        without missing any characters from the original string.
        
        Example:
        input: "一二三one two."
        output: ['一', '二', '三', 'one', ' ', 'two', '.']
        '''
        # Match Chinese characters, sequences of English letters, numbers, spaces, punctuation, or any other character
        words = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z0-9]+|\s|.', text)
        return words

    @staticmethod
    def mark_target_words(substrings, target_words):
        '''
        Given a list of substrings and a list of target words, returns a list where 1 indicates the substring is part of a target word and 0 otherwise.
        
        Example:
        substrings = ['一', '二', '三', 'one', ' ', 'two', '.']
        target_words = ['二三', 'one']
        
        Output: [0, 1, 1, 1, 0, 0, 0]
        '''
        # Initialize the result list with all zeros
        result = [0] * len(substrings)

        # Join the substrings into a single string to match target words
        text = ''.join(substrings)
        
        # Keep track of substring boundaries (start and end positions in the combined text)
        boundaries = []
        current_position = 0
        for substring in substrings:
            next_position = current_position + len(substring)
            boundaries.append((current_position, next_position))
            current_position = next_position

        # Loop through each target word
        for target in target_words:
            start = 0
            while start < len(text):
                # Find the target word in the text starting from 'start'
                index = text.find(target, start)
                if index != -1:
                    end = index + len(target)
                    # Check the boundary to find the corresponding indices in the substrings list
                    for i, (start_pos, end_pos) in enumerate(boundaries):
                        # If any part of the target word overlaps with this substring, mark it
                        if start_pos < end and end_pos > index:
                            result[i] = 1
                    start = index + 1  # Move forward to avoid infinite loops
                else:
                    break

        return result

    def split_paragraph_to_lines(self, text):
        words = self.split_text_to_words(text)
        should_be_highlighted = self.mark_target_words(words, self.highlighted_words)

        lines = []
        current_line = []
        sum_width = 0
        # Split the text into characters for Chinese and words for English
        for word in words:
            word_bbox = self.draw.textbbox((0, 0), word, font=self.font)
            width = word_bbox[2] - word_bbox[0]
            
            # Check if the word exceeds the width
            if width > self.width:
                # If the word is too wide, it should be placed on a new line
                if current_line:
                    lines.append(current_line)
                    current_line = []
                    sum_width = 0
                lines.append([word])  # Add the long word as a new line in a list
            elif sum_width + width > self.width:
                # If the word does not fit in the current line, move to the next line
                lines.append(current_line)
                current_line = [word]
                sum_width = width
            else:
                # Add the word to the current line without adding extra space
                current_line.append(word)
                sum_width += width

        if current_line:
            lines.append(current_line)  # Add the remaining line as a list

        # Adjust punctuation placement
        for i, line in enumerate(lines):
            if line and line[0] in '.,!?;：；。！？、，':
                lines[i] = line[1:]
                if i > 0:
                    lines[i-1].append(line[0])  # Append punctuation to the previous line

        # also split |should_be_highlighted| into 2d list as the same structure of |lines|
        highlighted_lines = []
        current_highlighted = []
        highlight_index = 0

        for line in lines:
            current_highlighted = []
            for word in line:
                if highlight_index < len(should_be_highlighted) and should_be_highlighted[highlight_index] == 1:
                    current_highlighted.append(1)
                else:
                    current_highlighted.append(0)
                highlight_index += 1
            highlighted_lines.append(current_highlighted)

        result = {'list_of_words': lines, 'should_be_highlighted': highlighted_lines}
        return result

    def split_lines(self):
        all_lines = []
        for paragraph in self.article.split('\n'):
            lines_of_cur_paragraph = self.split_paragraph_to_lines(paragraph)
            all_lines.append(lines_of_cur_paragraph)
        return all_lines

    def draw_text(self):
        x, y = self.position
        
        for render_dict in self.all_lines:
            line_list = render_dict['list_of_words']
            should_be_highlighted = render_dict['should_be_highlighted']
            for i, line in enumerate(line_list):
                for j, word in enumerate(line):
                    color = self.fill
                    if should_be_highlighted[i][j] == 1:
                        color = self.highlight_color
                    self.draw.text((x, y), word, font=self.font, fill=color)
                    word_bbox = self.draw.textbbox((0, 0), word, font=self.font)
                    word_width = word_bbox[2] - word_bbox[0]
                    x += word_width
            
                y += self.line_height
                x = self.position[0]  # Reset x position for the next line

class DrawEnglishText:
    def __init__(self, draw, font, position, fill, max_width, line_height, highlighted_words=None, highlight_color="red"):
        self.draw = draw
        self.font = font
        self.position = position
        self.fill = fill
        self.max_width = max_width
        self.line_height = line_height
        self.highlighted_words = highlighted_words if highlighted_words else []
        self.highlight_color = highlight_color
    
    def split_words(self, text):
        return text.split(' ')

    def determine_lines(self, words):
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            line_bbox = self.draw.textbbox((0, 0), test_line, font=self.font)
            line_width = line_bbox[2] - line_bbox[0]
            
            if line_width <= self.max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
    
        if current_line:
            lines.append(current_line.strip())
        return lines

    def draw_a_line_left_aligned(self, line, y_offset):
        words_and_punctuations = self.get_words_and_punctuations(line)
        x_offset = self.position[0]
        space_width = self.draw.textbbox((0, 0), " ", font=self.font)[2]
        for j, word in enumerate(words_and_punctuations):
            color = self.highlight_color if word in self.highlighted_words else self.fill
            self.draw.text((x_offset, self.position[1] + y_offset), word, font=self.font, fill=color)
            word_bbox = self.draw.textbbox((0, 0), word, font=self.font)
            word_width = word_bbox[2] - word_bbox[0]
            if self.is_next_word_punctuation(words_and_punctuations, j):
                x_offset += word_width
            else:
                x_offset += word_width + space_width

    def is_next_word_punctuation(self, words_and_punctuations, j):
        if j < len(words_and_punctuations) - 1:
            next_word = words_and_punctuations[j + 1]
            if next_word in '.,!?;：；。！？、，':
                return True
        return False

    def get_words_and_punctuations(self, line):
        words_and_punctuations = []
        current_word = ""
        
        for char in line:
            if char.isalnum():  # Check if the character is part of a word
                current_word += char
            else:
                if current_word:  # If we have a current word, add it to the list
                    words_and_punctuations.append(current_word)
                    current_word = ""
                if char.strip():  # If the character is not a whitespace, add it as punctuation
                    words_and_punctuations.append(char)
        
        if current_word:  # Add the last word if there is one
            words_and_punctuations.append(current_word)
        
        return words_and_punctuations

    def draw_a_line_justified(self, line, y_offset):
        words_in_line = line.split(' ')
        line_bbox = self.draw.textbbox((0, 0), line, font=self.font)
        line_width = line_bbox[2] - line_bbox[0]
        space_width = self.draw.textbbox((0, 0), " ", font=self.font)[2]
        total_spaces = len(words_in_line) - 1
        
        if total_spaces > 0:
            extra_space = (self.max_width - line_width) // total_spaces
        else:
            extra_space = 0

        x_offset = self.position[0]
        words_and_punctuations = self.get_words_and_punctuations(line)
        for j, word in enumerate(words_and_punctuations):
            color = self.highlight_color if word in self.highlighted_words else self.fill
            self.draw.text((x_offset, self.position[1] + y_offset), word, font=self.font, fill=color)
            word_bbox = self.draw.textbbox((0, 0), word, font=self.font)
            word_width = word_bbox[2] - word_bbox[0]
            if self.is_next_word_punctuation(words_and_punctuations, j):
                x_offset += word_width
            else:
                x_offset += word_width + space_width + extra_space

    def draw_words_of_a_line(self, line, y_offset, is_last_line):
        if is_last_line:
            self.draw_a_line_left_aligned(line, y_offset)
        else:
            self.draw_a_line_justified(line, y_offset)
        y_offset += self.line_height
        return y_offset

    def draw_lines(self, lines):
        y_offset = 0
        for i, line in enumerate(lines):
            is_last_line = (i == len(lines) - 1)
            y_offset = self.draw_words_of_a_line(line, y_offset, is_last_line)

    def draw_justified_text(self, text):
        words = self.split_words(text)
        lines = self.determine_lines(words)
        self.draw_lines(lines)

def test_draw_english_text():
    import os
    from PIL import Image, ImageDraw, ImageFont
    
    font_path = os.path.join("c:\\Windows\\Fonts", "msyhbd.ttc")  # Fixed backslash for Windows path
    font = ImageFont.truetype(font_path, size=50)
    image = Image.new('RGB', (1080, 1920), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    highlighted_words = ['advertise', 'advertisement']  # Example highlighted words
    fill = "black"
    line_height = 66
    text = ("In a city, there is a strict code that companies must follow when they advertise. "
            "Their products. Every advertisement has to be approved to make sure it meets the advertise.")
    
    # Create an instance of DrawEnglishText
    draw_english_text = DrawEnglishText(draw, font, (50, 1000), 
                                         fill=fill, 
                                         max_width=1000, 
                                         line_height=line_height, 
                                         highlighted_words=highlighted_words)
    draw_english_text.draw_justified_text(text)  # Call the method to draw the text
    
    output_path = os.path.join("D:\\Study\\AIAgent\\AIEnglishLearning\\output\\test", "test.jpeg")  # Fixed backslash for output path
    image.save(output_path)

def test_draw_chinese_text():
    from PIL import Image, ImageDraw, ImageFont
    import os
    image = Image.new('RGB', (1080, 1920), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    font_path = os.path.join("c:\\Windows\\Fonts", "msyhbd.ttc")  # Fixed backslash for Windows path
    font = ImageFont.truetype(font_path, size=50)
    highlighted_words = ['日历', '图书馆', '萨拉喔', 'advertise', 'advertisement']  # Example highlighted words
    n = DrawChineseText(
        "萨拉查看了目录，看看她想要的书萨拉喔。advertisement, 然后她看了看advertise.日历，找一个合适的日子去图书馆advertisement。她确保图书馆的开放时间是有效的，这样她就不会浪费自己的时间。",
        font=font,
        draw=draw,
        width=1000,
        line_height=66,
        position=(50, 1000),
        highlighted_words=highlighted_words)
    n.draw_text()
    image.save("D:\Study\AIAgent\AIEnglishLearning\output\\test\\test.jpeg")

if __name__ == '__main__':
    # test_draw_english_text()
    test_draw_chinese_text()
    # print(DrawChineseText.mark_target_words(['一', '二', '三', 'one', ' ', 'two', '.'], ['二三', 'one']))