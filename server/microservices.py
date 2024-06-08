
import bot as bot
import speech_to_text as stt
import text_to_speech as tts

def get_response(data):
    input_type = data['input_type']
    input_prompt = data['input_prompt']
    response = "hello, call the appropriate function here!"

    return response