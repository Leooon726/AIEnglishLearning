from PIL import Image, ImageDraw

class DrawChineseText:
    def __init__(self, article, font, draw, width, line_height, position=(0, 0), highlighted_words=None):
        self.width = width
        self.position = position
        self.font = font
        self.line_height = line_height
        self.article = article
        self.draw = draw
        self.all_lines = self.split_lines()
        self.highlighted_words = highlighted_words if highlighted_words else []

    def get_line_height(self):
        return self.draw.textbbox((0, 0), "汉", font=self.font)[3] - self.draw.textbbox((0, 0), "汉", font=self.font)[1]

    def get_lines(self, text):
        lines = []
        current_line = ""
        sum_width = 0
        
        for char in text:
            line_bbox = self.draw.textbbox((0, 0), char, font=self.font)
            width = line_bbox[2] - line_bbox[0]
            sum_width += width
            
            if sum_width > self.width:
                lines.append(current_line)
                current_line = char
                sum_width = width
            else:
                current_line += char
            
        if current_line:
            lines.append(current_line)
        
        # Adjust punctuation placement
        for i, line in enumerate(lines):
            if line and line[0] in '.,!?;：；。！？、，':
                lines[i] = line[1:]
                if i > 0:
                    lines[i-1] += line[0]
        return lines

    def split_lines(self):
        all_lines = []
        for paragraph in self.article.split('\n'):
            lines_of_cur_paragraph = self.get_lines(paragraph)
            all_lines += lines_of_cur_paragraph
        return all_lines

    def draw_text(self):
        x, y = self.position
        for single_line in self.all_lines:
            i = 0
            while i < len(single_line):
                # Check if any highlighted word matches the current substring
                match_found = False
                for word in self.highlighted_words:
                    if single_line[i:i+len(word)] == word and len(word) > 1:
                        # Highlight the entire word
                        self.draw.text((x, y), word, fill=(255, 0, 0), font=self.font)
                        word_width = sum(self.draw.textbbox((0, 0), char, font=self.font)[2] - self.draw.textbbox((0, 0), char, font=self.font)[0] for char in word)
                        x += word_width
                        i += len(word)
                        match_found = True
                        break

                # If no word match, draw character by character
                if not match_found:
                    single_char = single_line[i]
                    self.draw.text((x, y), single_char, fill=(0, 0, 0), font=self.font)
                    x += self.draw.textbbox((0, 0), single_char, font=self.font)[2] - self.draw.textbbox((0, 0), single_char, font=self.font)[0]
                    i += 1
            
            # Move to the next line
            y += self.line_height
            x = self.position[0]  # Reset x position for the next line

if __name__ == '__main__':
    image = Image.new('RGB', (1080, 1920), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    highlighted_words = ['萨拉', '图书馆']  # Example highlighted words
    n = DrawChineseText(
        "萨拉查看了目录，看看她想要的书是否有货。然后她看了看日历，找一个合适的日子去图书馆。她确保图书馆的开放时间是有效的，这样她就不会浪费自己的时间。",
        draw,
        1000, (50, 1000), highlighted_words=highlighted_words)
    n.draw_text()
    image.save("D:\Study\AIAgent\AIEnglishLearning\output\\test.jpeg")