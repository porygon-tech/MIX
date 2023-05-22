import os
import time 
import pandas as pd
import numpy as np
import re
import openai
#sudo apt-get install xsel

f = open("api_key.txt", "r")
openai.api_key = f.read().strip()
f.close()

def getKwds(txt, top=5):
	txt=re.sub('\W+',' ',txt).strip()
	t = txt.replace("\n", "").replace("-", "")
	#t=re.sub('\\S+','',t)
	t=np.array(t.split(' '))
	t2= np.append('',t)
	if (t.size%2!=0):
		t = np.append(t,'')
	if (t2.size%2!=0):
		t2 = np.append(t2,'')
	#[i.join(i+1) for i in list(t)]
	zp=list(zip(t2, t))
	zp=[x for x in zp if len(x[0])>2 and len(x[1])>2] # get only those pairs in which both words have a length >2
	pairs = list(map(lambda x : ' '.join(x), zp))
	wc=pd.value_counts(t)
	pc=pd.value_counts(pairs)
	#pc=pc.drop(['et al', 'e g', 'i e'])
	searchQuery = ' '.join(pc[:top].index)
	spltt = list(map(lambda x : x.split(' '), list(pc.index)))
	conn = ['the', 'of', 'a', 'to', 'and', '&', 'is', 'in', 'that', 'we', 'for', 'be', 'on', 'as', 'from', 'have', 'has', 'by', 'et', 'or'] 
	hasconnectors = list(map(lambda x : np.any([[c==w for c in conn] for w in x]), spltt))
	#np.any([[c==w for c in conn] for w in spltt[4]])
	#np.any([i == ['et','al'] for i in spltt])
	searchQuery = list(pc[np.logical_not(hasconnectors)].index[:top])
	return searchQuery


msgLogBase =[{"role": "system", "content" : "You are an AI assistant. Please,summarize users input in a brief, understandable paragraph."}]
text = ''
while True:
	newtext = os.popen("xsel -o").read()
	if text != newtext:
		text = newtext
		if text != '':
			os.system('notify-send \"received input\"')

			kwds = '\n'.join(getKwds(text))
			p = int(os.popen("zenity --question --text=\""+kwds+"\n\nSUMMARIZE?\" --width=400 ; YN=$?; echo ${YN}").read().strip())
			if p == 0:
				msgLog = msgLogBase.copy()
				msgLog.append({"role": "user", "content" : text})

				completion = openai.ChatCompletion.create(
				  model="gpt-3.5-turbo", 
				  temperature=0.4,
				  messages = msgLog
				)

				answer = completion["choices"][0]["message"]["content"]
        
				print(answer)
				os.system('zenity --info --text=\"'+ answer +'\" --width=400 ') # --height=300
				time.sleep(2)
		
