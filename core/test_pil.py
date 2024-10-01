from PIL import Image, ImageDraw, ImageFont
import os

def draw_wrapped_text(draw, text, position, font, fill, max_width):
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
    for line in lines:
        draw.text((position[0], position[1] + y_offset), line, font=font, fill=fill)
        # Use textbbox to calculate the height of the text
        line_bbox = draw.textbbox((0, 0), line, font=font)
        line_height = line_bbox[3] - line_bbox[1]
        y_offset += line_height  # Move down by the height of the line

def draw_justified_text(draw, text, position, font, fill, max_width, line_spacing_ratio=1.4, highlighted_words=None, highlight_color="red"):
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

        # Calculate the height of the current line
        line_bbox = draw.textbbox((0, 0), line, font=font)
        line_height = line_bbox[3] - line_bbox[1]
        y_offset += line_height*line_spacing_ratio  # Move down by the height of the line plus the gap

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

# Example usage
if __name__ == "__main__":
    illustration_image_path = "D:\Study\AIAgent\illustration.jpeg"
    output_path = "image_with_colored_text.jpg"
    create_image_with_text(output_path, illustration_image_path)
