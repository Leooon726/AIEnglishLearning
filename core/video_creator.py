from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips, concatenate_audioclips, CompositeAudioClip
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np
from moviepy.config import change_settings

# Specify the path to the ImageMagick binary
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})


class VideoCreator:
    def __init__(self, video_info_dict):
        self.video_info_dict = video_info_dict

    def create_video(self, transition_pause_time=3, fadeout_duration=2):
        # Load the audio and BGM
        audio_clip = AudioFileClip(self.video_info_dict['audio_path'])
        bgm_clip = AudioFileClip(self.video_info_dict['bgm_path']).volumex(0.2)  # Adjust BGM volume as needed
        audio_duration = audio_clip.duration

        # Create silence audio clips with transition_pause_time
        silence_audio = AudioArrayClip(np.zeros((int(transition_pause_time * audio_clip.fps), 2)), fps=audio_clip.fps)

        # Concatenate audio clips with silences
        final_audio_clip = concatenate_audioclips([audio_clip, silence_audio, audio_clip, silence_audio, audio_clip])

        # Apply a fade-out effect to the final audio clip
        final_audio_clip = final_audio_clip.audio_fadeout(fadeout_duration)

        # Create video clips for each keyframe and set the durations
        clip1 = ImageClip(self.video_info_dict['key_frame_1']).set_duration(audio_duration)
        clip1_silence = ImageClip(self.video_info_dict['key_frame_1']).set_duration(transition_pause_time)

        clip2 = ImageClip(self.video_info_dict['key_frame_2']).set_duration(audio_duration)
        clip2_silence = ImageClip(self.video_info_dict['key_frame_2']).set_duration(transition_pause_time)

        clip3 = ImageClip(self.video_info_dict['key_frame_3']).set_duration(audio_duration)
        clip3_silence = ImageClip(self.video_info_dict['key_frame_3']).set_duration(transition_pause_time)

        # Concatenate the video clips
        final_video_clip = concatenate_videoclips([clip1, clip1_silence, clip2, clip2_silence, clip3, clip3_silence])

        # Create a composite audio with the final concatenated audio and the background music
        composite_audio = CompositeAudioClip([final_audio_clip, bgm_clip.set_duration(final_audio_clip.duration)])

        # Apply a fade-out to the BGM if desired
        bgm_clip = bgm_clip.audio_fadeout(fadeout_duration)

        # Set the audio for the final video clip
        final_video_clip = final_video_clip.set_audio(composite_audio)

        # Export the final video
        final_video_clip.write_videofile(self.video_info_dict['output_path'], codec="libx264", fps=24)

        return self.video_info_dict['output_path']
    
# Example usage
if __name__ == "__main__":
    video_info_dict = {
        'index': '1',
        'image_prompt': '帮我生成图片：图片风格为「卡通」，比例为「1:1」，内容描述：萨拉查看了**目录**，看看她想要的书是否有货。然后她看了看**日历**，找一个合适的日子去图书馆。她确保图书馆的开放时间是**有效的**，这样她就不会浪费自己的时间。',
        'target_words_and_meanings': [('catalog', 'n. 目录（册） v. 编目'), ('calendar', 'n. 日历，月历'), ('valid', 'a. 有效的，有根据的；正当的')],
        'clean_paragraph': "Sara checked the catalog to see if the book she wanted was available. Then she looked at the calendar to find a suitable day to go to the library. She made sure the library's opening hours were valid so that she wouldn't waste her time.",
        'bold_words': ['catalog', 'calendar', 'valid'],
        'clean_translation': '萨拉查看了目录，看看她想要的书是否有货。然后她看了看日历，找一个合适的日子去图书馆。她确保图书馆的开放时间是有效的，这样她就不会浪费自己的时间。',
        'bold_word_meanings': ['目录', '日历', '有效的'],
        'audio_path': 'D:\\Study\\AIAgent\\AIEnglishLearning\\output\\output_audio.wav',
        'key_frame_1': 'D:\\Study\\AIAgent\\AIEnglishLearning\\output\\1_key_frame_1.jpeg',
        'key_frame_2': 'D:\\Study\\AIAgent\\AIEnglishLearning\\output\\1_key_frame_2.jpeg',
        'key_frame_3': 'D:\\Study\\AIAgent\\AIEnglishLearning\\output\\1_key_frame_3.jpeg',
        'output_path': 'D:\\Study\\AIAgent\\AIEnglishLearning\\output\\1_video.mp4',
        'bgm_path': 'D:\Study\AIAgent\AIEnglishLearning\static_materials\scott-buckley-reverie(chosic.com).mp3'
    }
    video_creator = VideoCreator(video_info_dict)
    video_path = video_creator.create_video()
    print(video_path)
