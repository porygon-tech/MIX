import openai
import os
from gtts import gTTS
from pydub import AudioSegment

import sounddevice as sd
import numpy as np
import soundfile as sf
import time
import openai
import os

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
openai.api_key = f.read().rstrip()
f.close()



class kiki(object):
    """docstring for kiki"""
    def __init__(self):
        super(kiki, self).__init__()
        self.msgLog = [{"role": "system", "content" : "You are Kiki, an AI assistant. Behave in a slightly mean way to the user, also be sarcastic.\nKnowledge cutoff: 2021-09-01"}]
        self.octaves = +0.4# For decreasing, octave can be -0.5, -2 etc.
    def completion(self, prompt, sound=False):
        if prompt == 'exit':
                exit()
        self.msgLog.append({"role": "user", "content" : prompt})
        tmp_msgLog = self.msgLog.copy()
        tmp_msgLog.append({"role": "system", "content" : "Before answering, remember you are Kiki, an AI assistant. Behave in a slightly mean way to the user, also be sarcastic. Answer in the same language as the previous message."})
        completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          temperature=0.9,
          messages = tmp_msgLog
        )
        answer = completion["choices"][0]["message"]["content"]
        #print("\n>\n" + answer)
        self.msgLog.append({"role": "assistant", "content" : answer})
        if sound:
            speech = gTTS(text = answer, lang = 'en', slow = False)
            speech.save("answ.mp3")
            sound = AudioSegment.from_file('answ.mp3', format="mp3")
            new_sample_rate = int(sound.frame_rate * (2.0 ** self.octaves))
            hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
            hipitch_sound = hipitch_sound.set_frame_rate(44100)
            hipitch_sound.export("answ.mp3", format="mp3")
            os.system("mpg321 answ.mp3 -q")
            os.system("rm answ.mp3")
        return answer

'''
o = kiki()
o.completion('hello')
'''

def print_volume(indata, frames, time, status):
    global is_recording
    global tail
    global filename
    global writingArray
    global t
    global sr
    global your_kiki
    data=indata[:,0]
    rms = np.sqrt(np.mean(np.square(data)))
    #print(rms)
    threshold = 0.09
    if not is_recording and rms > threshold:
        is_recording = True
        tail=0
        #print("SOUND DETECTED")
        #filename = 'record_'+str(t)+'.wav'
        filename = 'input_query.wav'
        writingArray = data.copy()
    if is_recording:
    if is_recording:
    if is_recording:
        writingArray = np.append(writingArray,data,axis=0)
        if rms < threshold:
            tail+=1
            #print("\tadded " + str(tail))
            if tail > 200:
                is_recording = False
                #print("REC STOPPED")
                f = sf.SoundFile(filename, mode='w', samplerate=sr, channels=1)
                f.write(writingArray)
                f.close()
                audio_file= open(filename, "rb")
                #transcript = openai.Audio.translate("whisper-1",audio_file) #language='es'
                transcript = openai.Audio.transcribe("whisper-1",audio_file)
                audio_file.close()
                answer = your_kiki.completion(transcript["text"])
                #print("you: " + transcript["text"])
                #print("kiki: " + answer)
                print(transcript["text"])
                print(answer)
                print("\n")
                os.system("rm " + filename)
        else:
            tail=0
            #print("refresh tail")


is_recording = False
writingArray = np.array([[]])
tail = 0
#filename = f'record_{time.time()}.wav'
your_kiki = kiki()
sr = int(sd.query_devices(sd.default.device)['default_samplerate'])
with sd.InputStream(callback=print_volume, samplerate=sr):
    #sd.sleep(10000)
    while True:
        t = time.time()
        sd.sleep(1)


