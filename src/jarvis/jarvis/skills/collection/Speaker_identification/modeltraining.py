import pickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture as GMM 
from featureextraction import extract_features
#from speakerfeatures import extract_features
import warnings
import os


#path to training data
source   = "/src/jarvis/jarvis/skills/collection/Speaker_identification/trainingData/"

#path where training speakers will be saved
dest = "/src/jarvis/jarvis/skills/collection/Speaker_identification/Speakers_models/"

count = 1

features = np.asarray(())

for path in os.listdir(source):    
    
    # read the audio
    sr,audio = read(source + path)
    
    # extract 40 dimensional MFCC & delta MFCC features
    vector   = extract_features(audio,sr)
    
    if features.size == 0:
        features = vector
        
    else:
        features = np.vstack((features, vector))
 
    if count == 1:

        gmm = GMM(n_components = 16, max_iter = 1000, covariance_type='diag',n_init = 3)
        gmm.fit(features)
        
        # dumping the trained gaussian model
        picklefile = path.split("-")[0]+".gmm"
        pickle.dump(gmm,open(dest + picklefile,'wb'))
        print ('+ modeling completed for speaker:',picklefile," with data point = ",features.shape) 
        features = np.asarray(())
        count = 0
    count = count + 1
