from PIL import Image, ImageDraw, ImageFont
import os
from image_creator import ImageCreator

class LandscapeKeyFrameCreator:
    def __init__(self, video_info_dict):
        self.video_info_dict = video_info_dict
        if 'illustration_image_base_path' not in self.video_info_dict:   
            self.video_info_dict['illustration_image_base_path'] = f"D:\Study\AIAgent\AIEnglishLearning\output"
        if 'header_image_path' not in self.video_info_dict:
            self.video_info_dict['header_image_path'] = "D:\Study\AIAgent\AIEnglishLearning\static_materials\header.png"
        self.image_width = 1920
        self.image_height = 1080
        if 'key_frame_output_base_path' not in self.video_info_dict:
            self.video_info_dict['key_frame_output_base_path'] = f"D:\Study\AIAgent\AIEnglishLearning\output"
        self.key_frame_output_base_path = self.video_info_dict['key_frame_output_base_path']

    def generate_all_key_frames(self):
        # update the paths to the video_info_dict
        self.video_info_dict['key_frame_1'] = self.create_key_frame_first_page()
        self.video_info_dict['key_frame_2'] = self.create_key_frame_second_page()
        self.video_info_dict['key_frame_3'] = self.create_key_frame_third_page()
        return self.video_info_dict

    def create_draw_config(self, output_image_path,header_image_path,illustration_image_path,plain_paragraph,highlighted_words):
        draw_config = {
                'background_color': 'white',
                'image_size': (self.image_width, self.image_height),
                'output_path': output_image_path,
                'drawing_operations': [
                    {
                        'type': 'draw_image',
                        'image_path': illustration_image_path,
                        'position': (0, 0),
                        'size': (1180, -1)
                    },
                    {
                        'type': 'draw_image',
                        'image_path': header_image_path,
                        'position': (1180, 0),
                        'size': (750, -1)
                    },
                    {
                        'type': 'draw_text',
                        'text': plain_paragraph,
                        'position': (1200, 280),
                        'font': 'msyhbd',
                        'font_size': 40,
                        'fill': 'black',
                        'text_box_width': 730,
                        'line_height_ratio': 1.5,
                        'padding': 30,
                        'highlighted_words': highlighted_words
                    }
                ]
            }
        return draw_config

    def create_key_frame_first_page(self):
        illustration_image_path = os.path.join(self.video_info_dict['illustration_image_base_path'],f"{self.video_info_dict['index']}.jpeg")
        output_image_name = f"{self.video_info_dict['index']}_key_frame_1"
        image_path = f"{self.key_frame_output_base_path}\\{output_image_name}.jpeg"  # Use double backslashes for Windows paths
        draw_config = self.create_draw_config(image_path,self.video_info_dict['header_image_path'],illustration_image_path,self.video_info_dict['clean_paragraph'],self.video_info_dict['bold_words'])
        image_creator = ImageCreator(draw_config)
        image_path = image_creator.draw()
        return image_path
    
    def create_key_frame_second_page(self):
        illustration_image_path = os.path.join(self.video_info_dict['illustration_image_base_path'],f"{self.video_info_dict['index']}.jpeg")
        output_image_name = f"{self.video_info_dict['index']}_key_frame_2"
        image_path = f"{self.key_frame_output_base_path}\\{output_image_name}.jpeg"  # Use double backslashes for Windows paths
        draw_config = self.create_draw_config(image_path,self.video_info_dict['header_image_path'],illustration_image_path,self.video_info_dict['clean_translation'],self.video_info_dict['bold_word_meanings'])
        image_creator = ImageCreator(draw_config)
        image_path = image_creator.draw()
        return image_path
    
    def create_key_frame_third_page(self):
        illustration_image_path = os.path.join(self.video_info_dict['illustration_image_base_path'],f"{self.video_info_dict['index']}.jpeg")
        output_image_name = f"{self.video_info_dict['index']}_key_frame_3"
        image_path = f"{self.key_frame_output_base_path}\\{output_image_name}.jpeg"  # Use double backslashes for Windows paths
        target_words_and_meanings = self.video_info_dict['target_words_and_meanings']
        multiple_line_string = "\n".join([f"{word}   {meaning}" for word, meaning in target_words_and_meanings])
        highlighted_words = [word for word, meaning in target_words_and_meanings]
        draw_config = self.create_draw_config(image_path,self.video_info_dict['header_image_path'],illustration_image_path,multiple_line_string,highlighted_words)
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
        'audio_path': 'D:\Study\AIAgent\AIEnglishLearning\output\cluster1\\0_output_audio.wav',
        'key_frame_output_base_path': 'D:\Study\AIAgent\AIEnglishLearning\output\\test',
        'illustration_image_base_path': 'D:\Study\AIAgent\AIEnglishLearning\output\cluster1',
        'header_image_path': 'D:\Study\AIAgent\AIEnglishLearning\static_materials\header.png'
    }
    key_frame_creator = LandscapeKeyFrameCreator(video_info_dict)
    path = key_frame_creator.create_key_frame_first_page()
    print(path)
    # path = key_frame_creator.create_key_frame_second_page()
    # print(path)
    # path = key_frame_creator.create_key_frame_third_page()
    # print(path)