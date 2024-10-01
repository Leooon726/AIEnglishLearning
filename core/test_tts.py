import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

class TextToSpeech:
    def __init__(self):
        load_dotenv()
        speech_key = os.getenv('AZURE_SPEECH_KEY')
        speech_region = 'eastasia'
        self.speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        self.speech_config.speech_synthesis_voice_name = 'en-US-EmmaMultilingualNeural'
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)

    def synthesize_speech(self, text, output_path):
        speech_synthesis_result = self.speech_synthesizer.speak_text_async(text).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
            
            # Save the audio data to a file
            audio_data = speech_synthesis_result.audio_data
            with open(output_path, "wb") as audio_file:
                audio_file.write(audio_data)
            print("Audio saved to {}".format(output_path))
            
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")

# Example usage
if __name__ == "__main__":
    tts = TextToSpeech()
    text_input = input("Enter some text that you want to speak > ")
    tts.synthesize_speech(text_input, "output_audio.wav")
    