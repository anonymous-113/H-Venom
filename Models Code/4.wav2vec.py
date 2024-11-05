import librosa
import torch
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2Model
from umap import UMAP
import os
import numpy as np
import json
# Set the device to CUDA if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
folder_path = "./wav_files"
model_name = "facebook/wav2vec2-large-xlsr-53"
embeddings = {}
feature_extractor = Wav2Vec2FeatureExtractor(do_normalize=True).from_pretrained(model_name)
model = Wav2Vec2Model.from_pretrained(model_name).to(device)
# Process each audio file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".wav"):  # Check if the file is a WAV file
        file_path = os.path.join(folder_path, file_name)
        base_name, _ = os.path.splitext(file_name)
# Load the audio file
        input_audio, sample_rate = librosa.load(file_path, sr=16000)

# Initialize the feature extractor and model



# Prepare the audio input for the model
        inputs = feature_extractor(input_audio, return_tensors="pt", sampling_rate=sample_rate )
        input_values = inputs.input_values.to(device)  # Move input values to CUDA

# Perform inference
        try:
                with torch.no_grad():
                        outputs = model(input_values)
                        last_hidden_state = outputs.last_hidden_state.cpu().numpy()

                # Compute the mean of the last hidden state across time steps to create a fixed-size embedding
                mean_embedding = np.mean(last_hidden_state, axis=1)  # Shape: (1, hidden_size)
                
                # Reduce dimensionality of the embeddings
                #umap = UMAP(n_components=40, n_neighbors=16, random_state=40)
                #final_embedding = umap.fit_transform(mean_embedding.reshape(1, -1))
                print(mean_embedding.shape)
        # The following line is incorrect because `extract_features` does not exist. Use `last_hidden_state` instead.
        # Print the flattened last hidden state tensor
                embeddings[base_name] = mean_embedding.tolist()[0]
                print(embeddings[base_name])
                json_file_path = os.path.join(folder_path, 'embeddings.json')
                with open(json_file_path, 'w') as json_file:
                        json.dump(embeddings, json_file, indent=4)
        except:
                continue
