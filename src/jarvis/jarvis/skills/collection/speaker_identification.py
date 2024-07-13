import os
import pickle
import numpy as np
from scipy.io.wavfile import read
from jarvis.skills.collection.Speaker_identification.featureextraction import extract_features
#from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")
import time

from jarvis.skills.skill import AssistantSkill
import jarvis

"""
#path to training data
source   = "development_set/"   
modelpath = "speaker_models/"
test_file = "development_set_test.txt"        
file_paths = open(test_file,'r')

"""
class identification(AssistantSkill):
	def testing(voice_transcript, skill):
		print("trying to identify...")
		#path to training data
		source   = "/src/jarvis/jarvis/skills/collection/Speaker_identification/SampleData/"   

		#path where training speakers will be saved
		modelpath = "/src/jarvis/jarvis/skills/collection/Speaker_identification/Speakers_models/"

		gmm_files = [os.path.join(modelpath,fname) for fname in 
			      os.listdir(modelpath) if fname.endswith('.gmm')]
		#print(gmm_files)
		#time.sleep(2)

		#############################################################################
		#Load the Gaussian gender Models
		models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]
		#############################################################################
		speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
			      in gmm_files]

		error = 0
		total_sample = 0.0
		
		# Read the test directory and get the list of test audio files 
		for path in os.listdir(source):   

			total_sample += 1.0
			#print ("Testing Audio : ", path)
			sr,audio = read(source + path)
			vector   = extract_features(audio,sr)
			print(vector)
			time.sleep(6.0)
			log_likelihood = np.zeros(len(models)) 

			for i in range(len(models)):
				gmm    = models[i]  #checking with each model one by one
				scores = np.array(gmm.score(vector))
				log_likelihood[i] = scores.sum()

			winner = np.argmin(log_likelihood)
			print(scores, log_likelihood, winner)
			time.sleep(6.0)
			print ("\tdetected as - ", speakers[winner])
			

			#checker_name = path.split("_")[0]
			#print("cheker", checker_name)
			#time.sleep(5.0)
			#if speakers[winner] != checker_name:
			#	error += 1
			#transcript = "I didn't recognize you."
			#return transcript
			#else:
			transcript = "Hello " + str(speakers[winner])
			jarvis.output_engine.assistant_response(transcript)
			time.sleep(1.0)


