from PIL import Image, ImageDraw, ImageFont
import os
from .draw_chinese_text import DrawChineseText

def draw_justified_text(draw, text, position, font, fill, max_width, line_height, highlighted_words=None, highlight_color="red"):
    if highlighted_words is None:
        highlighted_words = []
    
    # Break the text into lines that fit within the specified width
    lines = []
    words = text.split(' ')
    current_line = ""

    for word in words:
        # Check the width of the line with the next word added
        test_line = current_line + word + " "
        line_bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = line_bbox[2] - line_bbox[0]
        
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "  # Start a new line with the word
    
    # Append the last line
    if current_line:
        lines.append(current_line.strip())

    # Draw each line of wrapped text
    y_offset = 0
    for i, line in enumerate(lines):
        # If it's the last line, left-align it
        if i == len(lines) - 1:
            words_in_line = line.split(' ')
            x_offset = position[0]
            for word in words_in_line:
                color = highlight_color if word in highlighted_words else fill
                draw.text((x_offset, position[1] + y_offset), word, font=font, fill=color)
                word_bbox = draw.textbbox((0, 0), word, font=font)
                word_width = word_bbox[2] - word_bbox[0]
                x_offset += word_width + draw.textbbox((0, 0), " ", font=font)[2]  # Space between words
        else:
            # Justify the line by distributing the extra space between words
            words_in_line = line.split(' ')
            line_bbox = draw.textbbox((0, 0), line, font=font)
            line_width = line_bbox[2] - line_bbox[0]
            space_width = draw.textbbox((0, 0), " ", font=font)[2]  # Width of a single space
            total_spaces = len(words_in_line) - 1
            
            # Calculate the amount of extra space to distribute
            if total_spaces > 0:
                extra_space = (max_width - line_width) // total_spaces
            else:
                extra_space = 0

            # Draw each word, with the extra space distributed
            x_offset = position[0]
            for j, word in enumerate(words_in_line):
                color = highlight_color if word in highlighted_words else fill
                draw.text((x_offset, position[1] + y_offset), word, font=font, fill=color)
                word_bbox = draw.textbbox((0, 0), word, font=font)
                word_width = word_bbox[2] - word_bbox[0]
                x_offset += word_width + space_width + extra_space

        y_offset += line_height

# Create an image with a background color
def create_image_with_text(output_path, image_path, width=1080, height=1920, background_color=(0, 0, 0)):
    # Create a blank image with the specified background color
    image = Image.new('RGB', (width, height), color=background_color)
    
    # Load the image to be placed at the top
    top_image = Image.open(image_path)
    top_image = top_image.resize((width, int(top_image.height * (width / top_image.width))))  # Resize to match the width of the generated image
    
    # Paste the top image onto the background
    image.paste(top_image, (0, 0))
    
    # Create a white rectangle under the top image
    rectangle_height = 1000  # Height of the rectangle
    rectangle_position = (0, top_image.height - 100)  # Position right below the top image
    draw = ImageDraw.Draw(image)
    draw.rectangle([rectangle_position, (width, rectangle_position[1] + rectangle_height)], fill="white")
    
    # Initialize drawing context
    draw = ImageDraw.Draw(image)
    
    # Load a font that supports Chinese characters
    font_path = os.path.join("c:\Windows\Fonts", "msyhbd.ttc")
    font = ImageFont.truetype(font_path, size=50)
    
    # Draw text with different colors and auto wrap
    text1 = "I was at the terminal waiting for my vehicle. Suddenly, I saw a funny wagon pass by. It looked like it was carrying a lot of toys. I wondered where it was going."

    draw_justified_text(draw, text1, (50, top_image.height - 80), font, fill="black", max_width=width - 100, highlighted_words=['terminal'])  # Adjusted y position
    
    # Save the image
    image.save(output_path)

class KeyFrameCreator:
    def __init__(self, video_info_dict):
        self.video_info_dict = video_info_dict
        self.illustration_image_path = f"D:\Study\AIAgent\AIEnglishLearning\output\{self.video_info_dict['index']}.jpeg"
        self.header_image_path = "D:\Study\AIAgent\AIEnglishLearning\output\header.png"
        self.image_width = 1080
        self.image_height = 1920
        font_path = os.path.join("c:\Windows\Fonts", "msyhbd.ttc")
        self.font = ImageFont.truetype(font_path, size=50)

    def generate_all_key_frames(self):
        # update the paths to the video_info_dict
        self.video_info_dict['key_frame_1'] = self.create_key_frame_first_page()
        self.video_info_dict['key_frame_2'] = self.create_key_frame_second_page()
        self.video_info_dict['key_frame_3'] = self.create_key_frame_third_page()
        return self.video_info_dict

    def draw_image(self, image, image_path, position=(0, 0)):
        # Load the image to be placed at the top
        top_image = Image.open(image_path)
        top_image = top_image.resize((self.image_width, int(top_image.height * (self.image_width / top_image.width))))  # Resize to match the width of the generated image
        
        # Paste the top image onto the background
        image.paste(top_image, position)

    def draw_rectangle(self, image, position=(0, 0), width=1080, height=1000):
        # Create a white rectangle at the specified position
        draw = ImageDraw.Draw(image)  # Use the instance's image
        draw.rectangle([position, (position[0] + width, position[1] + height)], fill="white")

    def create_key_frame_first_page(self):
        output_image_name = f"{self.video_info_dict['index']}_key_frame_1"
        image = Image.new('RGB', (self.image_width, self.image_height), color=(0, 0, 0))
        image_path = f"D:\Study\AIAgent\AIEnglishLearning\output\{output_image_name}.jpeg"
        # lay the header image, illustration image, and the white rectangle.
        self.draw_image(image, self.header_image_path, (0, 0))
        self.draw_image(image, self.illustration_image_path, (0, 400))  # Position below the header image
        self.draw_rectangle(image, (0, 1400), 1080, 1000)
        # add the text.
        highlighted_words = self.video_info_dict['bold_words']
        draw = ImageDraw.Draw(image)
        line_height = (draw.textbbox((0, 0), "A", font=self.font)[3] - draw.textbbox((0, 0), "A", font=self.font)[1])*1.4
        draw_justified_text(draw, self.video_info_dict['clean_paragraph'], (50, 1430), self.font, fill="black", max_width=self.image_width - 100, line_height=line_height, highlighted_words=highlighted_words)  # Adjusted y position
        # return the created image path.
        image.save(image_path)
        return image_path
    
    def create_key_frame_second_page(self):
        output_image_name = f"{self.video_info_dict['index']}_key_frame_2"
        image = Image.new('RGB', (self.image_width, self.image_height), color=(255, 255, 255))
        image_path = f"D:\Study\AIAgent\AIEnglishLearning\output\{output_image_name}.jpeg"
        # lay the header image, illustration image, and the white rectangle.
        self.draw_image(image, self.header_image_path, (0, 0))
        self.draw_image(image, self.illustration_image_path, (0, 400))  # Position below the header image
        self.draw_rectangle(image, (0, 1400), 1080, 1000)
        # add the text.
        highlighted_words = self.video_info_dict['bold_word_meanings']
        draw = ImageDraw.Draw(image)
        line_height = (draw.textbbox((0, 0), "汉", font=self.font)[3] - draw.textbbox((0, 0), "汉", font=self.font)[1])*1.4
        chinese_text_drawer = DrawChineseText(self.video_info_dict['clean_translation'], self.font, draw, self.image_width - 100, line_height=line_height, position=(50,1430), highlighted_words=highlighted_words)
        chinese_text_drawer.draw_text()
        # return the created image path.
        image.save(image_path)
        return image_path
    
    def create_key_frame_third_page(self):
        output_image_name = f"{self.video_info_dict['index']}_key_frame_3"
        image = Image.new('RGB', (self.image_width, self.image_height), color=(255, 255, 255))
        image_path = f"D:\Study\AIAgent\AIEnglishLearning\output\{output_image_name}.jpeg"
        # lay the header image, illustration image, and the white rectangle.
        self.draw_image(image, self.header_image_path, (0, 0))
        self.draw_image(image, self.illustration_image_path, (0, 400))  # Position below the header image
        self.draw_rectangle(image, (0, 1400), 1080, 1000)

        # Convert the list of tuples to a multiple line string.
        target_words_and_meanings = self.video_info_dict['target_words_and_meanings']
        multiple_line_string = "\n".join([f"{word}   {meaning}" for word, meaning in target_words_and_meanings])
        highlighted_words = [word for word, meaning in target_words_and_meanings]
        draw = ImageDraw.Draw(image)
        line_height = (draw.textbbox((0, 0), "汉", font=self.font)[3] - draw.textbbox((0, 0), "汉", font=self.font)[1])*1.4
        chinese_text_drawer = DrawChineseText(multiple_line_string, self.font, draw, self.image_width - 100, line_height=line_height, position=(50,1430), highlighted_words=highlighted_words)
        chinese_text_drawer.draw_text()
        # return the created image path.
        image.save(image_path)
        return image_path

# Example usage
if __name__ == "__main__":
    # illustration_image_path = "D:\Study\AIAgent\illustration.jpeg"
    # output_path = "image_with_colored_text.jpg"
    # create_image_with_text(output_path, illustration_image_path)
    video_info_dict = {
        'index': '1',
        'image_prompt': '帮我生成图片：图片风格为「卡通」，比例为「1:1」，内容描述：萨拉查看了**目录**，看看她想要的书是否有货。然后她看了看**日历**，找一个合适的日子去图书馆。她确保图书馆的开放时间是**有效的**，这样她就不会浪费自己的时间。',
        'target_words_and_meanings': [('catalog', 'n. 目录（册） v. 编目'), ('calendar', 'n. 日历，月历'), ('valid', 'a. 有效的，有根据的；正当的')],
        'clean_paragraph': "Sara checked the catalog to see if the book she wanted was available. Then she looked at the calendar to find a suitable day to go to the library. She made sure the library's opening hours were valid so that she wouldn't waste her time.",
        'bold_words': ['catalog', 'calendar', 'valid'],
        'clean_translation': '萨拉查看了目录，看看她想要的书是否有货。然后她看了看日历，找一个合适的日子去图书馆。她确保图书馆的开放时间是有效的，这样她就不会浪费自己的时间。',
        'bold_word_meanings': ['目录', '日历', '有效的'],
        'audio_path': 'D:\\Study\\AIAgent\\AIEnglishLearning\\output\\output_audio.wav'
    }
    key_frame_creator = KeyFrameCreator(video_info_dict)
    # path = key_frame_creator.create_key_frame_first_page()
    # print(path)
    # path = key_frame_creator.create_key_frame_second_page()
    # print(path)
    path = key_frame_creator.create_key_frame_third_page()
    print(path)