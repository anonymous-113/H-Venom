import os
import pickle
import json

# Directory where your text files are located
text_files_dir = './transcriptions/'

# List to store all transcriptions
transcription_map = {}

# Iterate through each text file
for text_file in os.listdir(text_files_dir):
    #text_file = 'non_hate_video_167.txt'
    if text_file.endswith('.txt'):
        print(text_file)
        # Extract video name from file name
        video_name = os.path.splitext(text_file)[0]
        print(video_name)
        # Read transcription from the text file
        with open(os.path.join(text_files_dir, text_file), 'r') as f:
            transcript = f.read().strip().replace('\n', ' ')
        print(transcript)
        # Store transcription in the dictionary
        transcription_map[video_name] = transcript
        #break

# Save all transcriptions to a pickle file
output_file = 'all__video_vosk_audioMap.json'
with open(output_file, 'w') as f:
    json.dump(transcription_map, f, indent=2)

print(f"All transcriptions saved to {output_file}")
