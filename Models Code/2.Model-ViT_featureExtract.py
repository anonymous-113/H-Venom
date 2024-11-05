
FOLDER_NAME = './'




import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
import torchvision.transforms as transforms
import torch.utils.data as data
import torchvision
from torch.autograd import Variable
#import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.metrics import accuracy_score
from PIL import Image
import pickle
from tqdm import tqdm
from sklearn.metrics import *


# In[4]:


from transformers import ViTFeatureExtractor, ViTModel
from PIL import Image
import requests


# In[ ]:


print(torch.__version__)


# In[5]:


feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224-in21k")
model = ViTModel.from_pretrained("google/vit-base-patch16-224-in21k")


# In[6]:


num_video_features = 5
num_audio_features = 128
num_features = 256

k = 2
epochs = 1
batch_size = 1
learning_rate = 1e-4
log_interval = 1
minFrames = 5
img_x1, img_y1 = 299, 299
img_x2, img_y2 = 224, 224

begin_frame, end_frame, skip_frame = 0, minFrames, 0


# In[7]:


# Detect devices
use_cuda = torch.cuda.is_available()                   # check if GPU exists
device = torch.device("cuda" if use_cuda else "cpu")   # use CPU or GPU
#device = torch.device("cpu") 
device


# In[8]:

'''
import pickle
with open(FOLDER_NAME+'final_allNewData.p', 'rb') as fp:
    allDataAnnotation = pickle.load(fp)

# train, test split

train_list, train_label= allDataAnnotation['train']
val_list, val_label  =  allDataAnnotation['val']
test_list, test_label  =  allDataAnnotation['test']
'''

# In[9]:


allVidList = []
allVidLab = []
'''
allVidList.extend(train_list)
allVidList.extend(val_list)
allVidList.extend(test_list)

allVidLab.extend(train_label)
allVidLab.extend(val_label)
allVidLab.extend(test_label)
'''
import json
with open(FOLDER_NAME+'combined_files_s_a_r.json', 'rb') as fp:
    allDataAnnotation = json.load(fp)


#print(allDataAnnotation.keys())
allVidList , allVidLab = allDataAnnotation.keys(), allDataAnnotation.values()



def read_images(path, selected_folder):
    X = []
    currFrameCount = 0
    videoFrameCount = len([name for name in os.listdir(os.path.join(path, selected_folder))])
    if videoFrameCount <= minFrames:
        for i in range(videoFrameCount):
            image = Image.open(os.path.join(path, selected_folder, 'frame_{}.jpg'.format(i)))

            X.append(image)
            currFrameCount += 1
            if(currFrameCount==minFrames):
                break
        paddingImage = Image.fromarray(np.zeros((100,100)), 'RGB')
        while currFrameCount < minFrames:
            X.append(paddingImage)
            currFrameCount+=1
        #X = torch.stack(X, dim=0)
    else:
        step = int(videoFrameCount/minFrames)
        for i in range(0,videoFrameCount,step):
            image = Image.open(os.path.join(path, selected_folder, 'frame_{}.jpg'.format(i)))
            X.append(image)
            currFrameCount += 1
            if(currFrameCount==minFrames):
                break
        paddingImage = Image.fromarray(np.zeros((100,100)), 'RGB')
        while currFrameCount < minFrames:
            X.append(paddingImage)
            currFrameCount+=1
        #X = torch.stack(X, dim=0)
    return X



# set path
data_image_path = "./Alldata/" 




all_video_features = {}
import numpy as np


from tqdm import tqdm
import os
'''
for folder, label in tqdm(list(zip(allVidList, allVidLab))):
    if os.path.exists("VITF/"+folder+"_vit.p")==True:
        continue
    try:
        #print(data_image_path, folder)
        video = read_images(data_image_path,folder)
        #print(video)
        inputs = feature_extractor(images=video, return_tensors="pt")
        outputs = model(**inputs)
        last_hidden_states = outputs.last_hidden_state
        video_features =[(last_hidden_states[i][0].detach().numpy()) for i in range(0,5)]
        all_video_features[folder] = video_features

        with open("VITF/"+folder+"_vit.p", 'wb') as fp:
            pickle.dump(video_features,fp)

        del video
        del inputs
        del last_hidden_states
    except Exception as e:
        print(e)
        print("Error",folder)
        pass
output_file = "all_video_features.p"
with open(output_file, 'wb') as fp:
    pickle.dump(all_video_features, fp)
'''

model.to(device)

# Dictionary to store all video features
all_video_features = {}

for folder, label in tqdm(list(zip(allVidList, allVidLab))):
    try:
        if os.path.exists("VITF/"+folder+"_vit.p"):
            continue
        
        video = read_images(data_image_path, folder)
        
        # Convert images to tensors and move to CUDA if available
        video_tensors = [transforms.ToTensor()(frame).to(device) for frame in video]
        
        # Extract features using CUDA
        inputs = feature_extractor(images=video_tensors, return_tensors="pt")
        outputs = model(**inputs.to(device))
        last_hidden_states = outputs.last_hidden_state
        
        # Collect all frame features
        video_features = [last_hidden_states[i][0].detach().cpu().numpy() for i in range(minFrames)]
        
        # Store in dictionary
        all_video_features[folder] = video_features
        
        del video
        del inputs
        del last_hidden_states
    
    except Exception as e:
        print(f"Error processing {folder}: {e}")
        continue

# Save all features to a single file using pickle
output_file = "all_video_features.p"
with open(output_file, 'wb') as fp:
    pickle.dump(all_video_features, fp)
