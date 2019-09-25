from pydub import AudioSegment
import wave
import contextlib
import speech_recognition  as sr
import pyaudio
import time
import operator
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime 

def mp3_to_wav(audio_file_name):
    if audio_file_name.split('.')[1] == 'mp3':
        sound = AudioSegment.from_mp3(audio_file_name)
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(audio_file_name, format="wav")

def m4a_to_wav(audio_file_name):
  if audio_file_name.split('.')[1] == "m4a":
    sound = AudioSegment.from_file(audio_file_name , "m4a")
    audio_file_name = audio_file_name.split('.')[0] + '.wav'
    sound.export(audio_file_name, format="wav")

def getDuration(audio_file_name : str):
  with contextlib.closing(wave.open(audio_file_name,'r')) as f:
      frames = f.getnframes()
      rate = f.getframerate()
      duration = frames / float(rate)
      return duration

def GetTextFromAudio(file_name : str):
	if file_name[-3:] == 'm4a':
		m4a_to_wav(file_name)
	elif file_name[-3:] == 'mp3':
		mp3_to_wav(file_name)

	exact_file_name = file_name.split(".")[0]

	audio_data = sr.AudioFile(exact_file_name + '.wav')
	time_in_seconds = getDuration(exact_file_name + '.wav')

	r = sr.Recognizer()
	total_data = ""

	with audio_data as source :
	  #time_in_seconds = getDuration(file_name)
	  for i in range(int(int(time_in_seconds)/8)):
	    r.adjust_for_ambient_noise(source , duration=0.1)
	    audio = r.record(source , duration = 8)
	    try :
	      data = r.recognize_google(audio)
	      total_data = total_data + data + " "
	    except :
	      continue

	return total_data

def ProcessTime(timestamp : str):
  timestamp = timestamp[:-7]
  bad_chars = ['-' , ':' , ' ']
  for i in bad_chars : 
    timestamp = timestamp.replace(i, '')
  return timestamp

def GetDict(total_data : str):
	total_data = total_data.lower()

	total_data_2 = total_data.split()

	unqiue_data = list(set(total_data_2))

	unqiue_data_freq = {}

	for i in unqiue_data :
	  unqiue_data_freq[i] = 0

	for i in total_data_2 :
	  unqiue_data_freq[i] += 1 

	sorted_x = sorted(unqiue_data_freq.items(), key=operator.itemgetter(1) , reverse = True)

	return sorted_x

def SaveImage(total_data : str , name : str , timestamp : str):
	timestamp = ProcessTime(timestamp)
	wordcloud = WordCloud(max_words = 50 , stopwords=None , background_color='white').generate(total_data)
	wordcloud.to_file(name + "_" + timestamp + ".png")

def SaveDict(dic : dict , name : str , timestamp : str):
	exDict = {'ExDict' : dic}
	timestamp = ProcessTime(timestamp)
	with open(name + "_" + timestamp + '.txt', 'w') as file:
		file.write(json.dumps(exDict))

def DoEveryThing(name : str , file_path : str):
	now = datetime.now()
	now = str(now)
	total_data = GetTextFromAudio(file_path)
	SaveImage(total_data , name , now)
	Dict = GetDict(total_data)
	SaveDict(Dict , name , now)

#DoEveryThing("Abhilash" , "audio_only.wav")