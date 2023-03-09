import openai
import os
from gtts import gTTS 
'''
python3 -m openai-env
source openai-env/bin/activate
pip3 install openai
pip3 install gtts
pip3 install sounddevice
sudo apt install mpg321
pip3 install pydub

deactivate
'''
#https://platform.openai.com/docs/guides/speech-to-text/quickstart
#https://platform.openai.com/docs/api-reference/audio/create#audio/create-prompt

f = open("api_key.txt", "r")
openai.api_key = f.read()
f.close()


#msgLog =[{"role": "system", "content" : "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01"}]
#msgLog =[{"role": "system", "content" : "You are a butcher in a market. Behave in a mean way to the customer.\nKnowledge cutoff: 2021-09-01"}]
msgLog =[{"role": "system", "content" : "You are an AI assistant. Behave in a slightly mean way to the user, also be sarcastic.\nKnowledge cutoff: 2021-09-01"}]
#msgLog =[{"role": "system", "content" : "You are an AI assistant. Behave in a mean and sarcastic way to the user, and answer in spanish.\nKnowledge cutoff: 2021-09-01"}]


audio_file= open("welcome.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1",audio_file) #language='es'


from pydub import AudioSegment



octaves = +0.4# For decreasing, octave can be -0.5, -2 etc.



'''
audio_file= open("/path/to/file/german.mp3", "rb")
transcript = openai.Audio.translate("whisper-1", audio_file)
'''

while True:
	print("=================================================")
	#capture audio here
	prompt = input()
	#prompt = transcript["text"]
	if prompt == 'exit':
		break

	msgLog.append({"role": "user", "content" : prompt})

	completion = openai.ChatCompletion.create(
	  model="gpt-3.5-turbo", 
	  temperature=0.9,
	  messages = msgLog
	)
	answer = completion["choices"][0]["message"]["content"]

	print("\n>\n" + answer)
	msgLog.append({"role": "assistant", "content" : answer})

	speech = gTTS(text = answer, lang = 'en', slow = False)
	speech.save("answ.mp3")


	sound = AudioSegment.from_file('answ.mp3', format="mp3")
	new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
	hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
	hipitch_sound = hipitch_sound.set_frame_rate(44100)
	hipitch_sound.export("answ.mp3", format="mp3")

	os.system("mpg321 answ.mp3 -q")



	#audio_file= open("answ.mp3", "rb")
	#transcript = openai.Audio.transcribe("whisper-1",audio_file) #language='es'

	#os.system("spd-say \"" + answer + "\"")


os.system("rm answ.mp3")


