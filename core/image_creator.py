from PIL import Image, ImageDraw, ImageFont, ImageColor
import os
from draw_text import DrawChineseText

class ImageCreator:
    def __init__(self, draw_config):
        self.draw_config = draw_config

    def draw_image(self, image, image_path, position=(0, 0), size=None):
        '''
        If size=(100, -1), the image will be resized to match the width of the generated image by keeping the aspect ratio.
        If size=(-1, 100), the image will be resized to match the height of the generated image by keeping the aspect ratio.
        If size=(100, 100), the image will be resized to match the width and height of the generated image.
        '''
        # Load the image to be placed at the top
        top_image = Image.open(image_path)
        
        # Determine the new size based on the provided size parameter
        if size is None:
            new_size = (top_image.width, top_image.height)
        elif size[0] == -1:
            new_size = (int(top_image.width * (size[1] / top_image.height)), size[1])
        elif size[1] == -1:
            new_size = (size[0], int(top_image.height * (size[0] / top_image.width)))
        else:
            new_size = size
        
        top_image = top_image.resize(new_size)  # Use ANTIALIAS for better quality
        image.paste(top_image, position)
        
    def draw_shape(self,image, shape, position, size, fill, alpha=255):
        """
        Draws a specified shape on an image with a given fill color and transparency.
        
        Parameters:
            image: The image to draw on (PIL Image).
            shape: The shape to draw ('rectangle').
            position: The top-left corner of the shape (tuple).
            size: The width and height of the shape (tuple).
            fill: The fill color for the shape (tuple with RGB values).
            alpha: The transparency level (0-255), where 0 is fully transparent and 255 is fully opaque.
        """
        # Convert color string to RGB tuple if necessary
        if isinstance(fill, str):
            rgb = ImageColor.getrgb(fill)  # Convert string color to RGB tuple
            fill_with_alpha = rgb + (alpha,)  # Add alpha value to the tuple
        elif isinstance(fill, tuple):
            if len(fill) == 3:
                fill_with_alpha = fill + (alpha,)  # Add alpha to RGB tuple
            elif len(fill) == 4:
                fill_with_alpha = fill  # Already RGBA
            else:
                raise ValueError("Fill color tuple must be RGB or RGBA.")
        else:
            raise ValueError("Fill color must be a string or a tuple.")
        
        draw = ImageDraw.Draw(image, "RGBA")  # Use RGBA mode to support transparency
        if shape == 'rectangle':
            draw.rectangle([position, (position[0] + size[0], position[1] + size[1])], fill=fill_with_alpha)
        else:
            raise ValueError(f"Unsupported shape: {shape}")

    def draw_text(self, image, text, position, font, font_size, fill, text_box_width, line_height_ratio, padding, highlighted_words):
        # Load the font
        if font == 'msyhbd':
            font_path = os.path.join("c:\\Windows\\Fonts", "msyhbd.ttc")
            font = ImageFont.truetype(font_path, size=font_size)
        else:
            raise ValueError(f"Unsupported font: {font}")
        
        # Convert color string to RGB tuple if necessary
        if isinstance(fill, str):
            fill_color = ImageColor.getrgb(fill)  # Convert string color to RGB tuple
        elif isinstance(fill, tuple):
            if len(fill) == 3 or len(fill) == 4:
                fill_color = fill  # Already RGB or RGBA tuple
            else:
                raise ValueError("Fill color tuple must be RGB or RGBA.")
        else:
            raise ValueError("Fill color must be a string or a tuple.")
        
        # Create the drawing context
        draw = ImageDraw.Draw(image, "RGBA")
        # Adjust text box width based on padding
        text_box_width = text_box_width - padding * 2
        position_after_padding = (position[0] + padding, position[1])
        # Calculate line height based on the given ratio
        sample_char = "汉"  # Use a common Chinese character for height calculation
        line_height = (draw.textbbox((0, 0), sample_char, font=font)[3] - draw.textbbox((0, 0), sample_char, font=font)[1]) * line_height_ratio
        # Use the helper class to draw the Chinese text
        chinese_text_drawer = DrawChineseText(text, font, draw, text_box_width, line_height=line_height, position=position_after_padding, highlighted_words=highlighted_words, fill=fill_color)
        chinese_text_drawer.draw_text(alignment='justify')

    def draw(self):
        image_size = self.draw_config['image_size'] 
        image = Image.new('RGB', image_size, color=self.draw_config['background_color'])
        for operation in self.draw_config['drawing_operations']:
            if operation['type'] == 'draw_image':
                self.draw_image(image, operation['image_path'], operation['position'], operation['size'])
            elif operation['type'] == 'draw_shape':
                alpha = operation['transparent'] if ('transparent' in operation) else 255
                self.draw_shape(image, operation['shape'], operation['position'], operation['size'], operation['fill'], alpha)
            elif operation['type'] == 'draw_text':
                self.draw_text(image, operation['text'], operation['position'], operation['font'], 
                               operation['font_size'], operation['fill'], operation['text_box_width'], 
                               operation['line_height_ratio'], operation['padding'], 
                               operation['highlighted_words'])

        output_path = self.draw_config['output_path']
        image.save(output_path)
        return output_path

def test_draw():
    draw_config = {
        'background_color': 'white',
        'image_size': (1920, 1080),
        'output_path': 'D:\\Study\\AIAgent\\AIEnglishLearning\\output\\test\\image_creator_test.jpeg',
        'drawing_operations': [
            {
                'type': 'draw_image',
                'image_path': 'D:\Study\AIAgent\AIEnglishLearning\output\\1.jpeg',
                'position': (0, 0),
                'size': (1180, -1)
            },
            {
                'type': 'draw_image',
                'image_path': 'D:\Study\AIAgent\AIEnglishLearning\static_materials\header.png',
                'position': (1180, 0),
                'size': (750, -1)
            },
            # {
            #     'type': 'draw_shape',
            #     'shape': 'rectangle',
            #     'position': (0, 1050),
            #     'size': (1080, 1000),
            #     'fill': 'black'
            # },
            {
                'type': 'draw_text',
                'text': '萨拉查看了目录，看看她想要的书是否有货。然后她看了看日历，找一个合适的日子去图书馆。她确保图书馆的开放时间是有效的，这样她就不会浪费自己的时间。',
                'position': (1200, 320),
                'font': 'msyhbd',
                'font_size': 50,
                'fill': 'black',
                'text_box_width': 730,
                'line_height_ratio': 1.5,
                'padding': 20,
                'highlighted_words': ['萨拉', 'World']
            }
        ]
    }
    key_frame_creator = ImageCreator(draw_config)
    path = key_frame_creator.draw()
    print(path)

def draw_ending_image():
    draw_config = {
        'background_color': 'white',
        'image_size': (1080, 1920),
        'output_path': 'D:\\Study\\AIAgent\\AIEnglishLearning\\output\\test\\image_creator_test.jpeg',
        'drawing_operations': [
            {
                'type': 'draw_image',
                'image_path': 'D:\Study\AIAgent\AIEnglishLearning\static_materials\卡通女生图片.jpeg',  
                'position': (-40, -100),
                'size': (1180, -1)
            },
            {
                'type': 'draw_shape',
                'shape': 'rectangle',
                'position': (0, 1250),
                'size': (1080, 300),
                'fill': 'grey',
                'transparent': 178
            },
            {
                'type': 'draw_text',
                'text': '好记性不如烂笔头\n来留言区拼写打卡吧!',
                'position': (0, 1300),
                'font': 'msyhbd',
                'font_size': 70,
                'fill': 'black',    
                'text_box_width': 1080,
                'line_height_ratio': 1.5,
                'padding': 190,
                'highlighted_words': ['']
            }
        ]
    }
    key_frame_creator = ImageCreator(draw_config)
    path = key_frame_creator.draw()
    print(path)

# Example usage
if __name__ == "__main__":
    # test_draw()
    draw_ending_image()
