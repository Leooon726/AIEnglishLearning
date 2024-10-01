from moviepy.editor import ImageClip, TextClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from moviepy.audio.fx.all import audio_loop
from moviepy.config import change_settings

# Specify the path to the ImageMagick binary
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

# Create a text clip
def create_text_clip(text, duration=5, fontsize=70, color='white'):
    txt_clip = TextClip(text, fontsize=fontsize, color=color)
    txt_clip = txt_clip.set_duration(duration).set_position('center')
    return txt_clip

# Create an image clip
def create_image_clip(image_path, duration=5):
    img_clip = ImageClip(image_path).set_duration(duration)
    return img_clip
    
def create_video(audio_path, image_path, output_path):
    # Create text and image clips
    image_clip = create_image_clip(image_path)
    
    # Load the audio file
    audio_clip = AudioFileClip(audio_path)
    
    # Loop the audio to play twice
    audio_clip = audio_loop(audio_clip, nloops=2)
    
    # Set the duration of the image clip to match the audio duration
    image_clip = image_clip.set_duration(audio_clip.duration)
    
    # Combine text and image clips (example: 5 seconds of text followed by image)
    final_clip = concatenate_videoclips([image_clip])
    
    # Set the audio to the final clip
    final_clip = final_clip.set_audio(audio_clip)
    
    # Export the final video
    final_clip.write_videofile(output_path, codec="libx264", fps=24)

# Example usage
if __name__ == "__main__":
    image_path = "D:\Study\AIAgent\image.jpg"
    audio_path = "D:\Study\AIAgent\iaudio.wav"
    output_path = "output_video.mp4"
    
    create_video(audio_path, image_path, output_path)
