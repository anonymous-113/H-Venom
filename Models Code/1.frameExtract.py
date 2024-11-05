FOLDER_NAME = './'

import os
from os import walk, listdir
import cv2
import shutil
import pandas as pd
from tqdm import tqdm
video_labels = []
target_folder = FOLDER_NAME +'/Alldata/'
folder1 = ["hate_videos","non_hate_videos"]
max_frames_per_video = 100
for subDir in folder1:
  print(subDir)
  for f in tqdm(listdir(FOLDER_NAME + subDir)):

    if(f.split('.')[-1] == 'mp4'):
      # Extracting label of video
      #print(f, FOLDER_NAME + subDir + '/' + f)
      #break
      success, _ = cv2.VideoCapture(FOLDER_NAME + subDir + '/' + f).read()
      if not success:
        print(f)
        continue  
      # Extracting frames from video
      try:
        os.mkdir(os.path.join(target_folder +  f.split('.')[0]))
      except FileExistsError:
        pass
      if os.listdir(os.path.join(target_folder + '/' +  f.split('.')[0])):
        continue
      vidcap = cv2.VideoCapture(FOLDER_NAME + subDir + '/' + f)
      success = True
      count = 0
      while success and count < max_frames_per_video:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*20))
        success,img = vidcap.read()
        if not success:
          break
        cv2.imwrite( target_folder + '/' + f.split('.')[0] + '/' + "frame_{}".format(count) + '.jpg', img)     # save frame as JPEG file
        count = count + 1
