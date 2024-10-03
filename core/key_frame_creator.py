from PIL import Image, ImageDraw, ImageFont
import os
from .image_creator import ImageCreator

class KeyFrameCreator:
    def __init__(self, video_info_dict):
        self.video_info_dict = video_info_dict
        self.illustration_image_path = f"D:\Study\AIAgent\AIEnglishLearning\output\{self.video_info_dict['index']}.jpeg"
        self.header_image_path = "D:\Study\AIAgent\AIEnglishLearning\static_materials\header.png"
        self.image_width = 1080
        self.image_height = 1920
        font_path = os.path.join("c:\Windows\Fonts", "msyhbd.ttc")
        self.font = ImageFont.truetype(font_path, size=50)
        if 'key_frame_output_base_path' not in self.video_info_dict:
            self.video_info_dict['key_frame_output_base_path'] = f"D:\Study\AIAgent\AIEnglishLearning\output"
        self.key_frame_output_base_path = self.video_info_dict['key_frame_output_base_path']

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

    def draw_common_part(self, image):
        # Draw the header image, illustration image, and the white rectangle.
        self.draw_image(image, self.header_image_path, (0, 0))
        self.draw_image(image, self.illustration_image_path, (0, 250))  # Position below the header image
        self.draw_rectangle(image, (0, 1250), self.image_width, 1000)  # Use instance's image_width

    def create_key_frame_first_page(self):
        output_image_name = f"{self.video_info_dict['index']}_key_frame_1"
        image_path = f"{self.key_frame_output_base_path}\\{output_image_name}.jpeg"  # Use double backslashes for Windows paths
        draw_config = {
                'background_color': 'white',
                'image_size': (self.image_width, self.image_height),
                'output_path': image_path,
                'drawing_operations': [
                    {
                        'type': 'draw_image',
                        'image_path': self.header_image_path,
                        'position': (0, 0),
                        'size': (self.image_width, -1)
                    },
                    {
                        'type': 'draw_image',
                        'image_path': self.illustration_image_path,
                        'position': (0, 250),
                        'size': (self.image_width, -1)
                    },
                    {
                        'type': 'draw_shape',
                        'shape': 'rectangle',
                        'position': (0, 1250),
                        'size': (1080, 1000),
                        'fill': 'white'
                    },
                    {
                        'type': 'draw_text',
                        'text': self.video_info_dict['clean_paragraph'],
                        'position': (0, 1270),
                        'font': 'msyhbd',
                        'font_size': 50,
                        'fill': 'black',
                        'text_box_width': self.image_width,
                        'line_height_ratio': 1.4,
                        'padding': 70,
                        'highlighted_words': self.video_info_dict['bold_words']
                    }
                ]
            }
        image_creator = ImageCreator(draw_config)
        image_path = image_creator.draw()
        return image_path
    
    def create_key_frame_second_page(self):
        output_image_name = f"{self.video_info_dict['index']}_key_frame_2"
        image_path = f"{self.key_frame_output_base_path}\\{output_image_name}.jpeg"  # Use double backslashes for Windows paths
        draw_config = {
                'background_color': 'white',
                'image_size': (self.image_width, self.image_height),
                'output_path': image_path,
                'drawing_operations': [
                    {
                        'type': 'draw_image',
                        'image_path': self.header_image_path,
                        'position': (0, 0),
                        'size': (self.image_width, -1)
                    },
                    {
                        'type': 'draw_image',
                        'image_path': self.illustration_image_path,
                        'position': (0, 250),
                        'size': (self.image_width, -1)
                    },
                    {
                        'type': 'draw_shape',
                        'shape': 'rectangle',
                        'position': (0, 1250),
                        'size': (1080, 1000),
                        'fill': 'white'
                    },
                    {
                        'type': 'draw_text',
                        'text': self.video_info_dict['clean_translation'],
                        'position': (0, 1270),
                        'font': 'msyhbd',
                        'font_size': 50,
                        'fill': 'black',
                        'text_box_width': self.image_width,
                        'line_height_ratio': 1.4,
                        'padding': 70,
                        'highlighted_words': self.video_info_dict['bold_word_meanings']
                    }
                ]
            }
        image_creator = ImageCreator(draw_config)
        image_path = image_creator.draw()
        return image_path
    
    def create_key_frame_third_page(self):
        output_image_name = f"{self.video_info_dict['index']}_key_frame_3"
        image_path = f"{self.key_frame_output_base_path}\\{output_image_name}.jpeg"  # Use double backslashes for Windows paths
        target_words_and_meanings = self.video_info_dict['target_words_and_meanings']
        multiple_line_string = "\n".join([f"{word}   {meaning}" for word, meaning in target_words_and_meanings])
        highlighted_words = [word for word, meaning in target_words_and_meanings]
        draw_config = {
                'background_color': 'white',
                'image_size': (self.image_width, self.image_height),
                'output_path': image_path,
                'drawing_operations': [
                    {
                        'type': 'draw_image',
                        'image_path': self.header_image_path,
                        'position': (0, 0),
                        'size': (self.image_width, -1)
                    },
                    {
                        'type': 'draw_image',
                        'image_path': self.illustration_image_path,
                        'position': (0, 250),
                        'size': (self.image_width, -1)
                    },
                    {
                        'type': 'draw_shape',
                        'shape': 'rectangle',
                        'position': (0, 1250),
                        'size': (1080, 1000),
                        'fill': 'white'
                    },
                    {
                        'type': 'draw_text',
                        'text': multiple_line_string,
                        'position': (0, 1270),
                        'font': 'msyhbd',
                        'font_size': 50,
                        'fill': 'black',
                        'text_box_width': self.image_width,
                        'line_height_ratio': 1.4,
                        'padding': 70,
                        'highlighted_words': highlighted_words
                    }
                ]
            }
        image_creator = ImageCreator(draw_config)
        image_path = image_creator.draw()
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
        'audio_path': 'D:\\Study\\AIAgent\\AIEnglishLearning\\output\\output_audio.wav',
        'key_frame_output_base_path': 'D:\\Study\\AIAgent\\AIEnglishLearning\\output\\test'
    }
    key_frame_creator = KeyFrameCreator(video_info_dict)
    path = key_frame_creator.create_key_frame_first_page()
    print(path)
    path = key_frame_creator.create_key_frame_second_page()
    print(path)
    path = key_frame_creator.create_key_frame_third_page()
    print(path)