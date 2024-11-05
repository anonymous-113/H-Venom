from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel, AutoModelForMaskedLM, GPT2TokenizerFast, GPT2Model
# Select the needed tokeniser by uncommenting the lines

gpt2_tokenizer = GPT2TokenizerFast.from_pretrained('Xenova/text-embedding-ada-002')
gpt2_model = GPT2Model.from_pretrained('gpt2')
gpt2_model.eval()
#tokenizer = AutoTokenizer.from_pretrained("Hate-speech-CNERG/bert-base-uncased-hatexplain")
#model = AutoModel.from_pretrained("Hate-speech-CNERG/bert-base-uncased-hatexplain")
#model.eval()


#tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
#model = AutoModel.from_pretrained("google-bert/bert-base-uncased")
#model.eval()

# Load GPT-2 tokenizer and model
#gpt2_tokenizer = GPT2TokenizerFast.from_pretrained('Xenova/text-embedding-ada-002')
#gpt2_model = GPT2Model.from_pretrained('gpt2')
#gpt2_model.eval()
from sklearn.model_selection import train_test_split
from qiskit_algorithms.utils import algorithm_globals
import torch
import numpy as np
import pickle
import json
FOLDER_NAME = './'
with open(FOLDER_NAME + 'combined_files_s_a_r.json', 'r') as fp:
    allDataAnnotation = json.load(fp)

# Prepare data
alist, alabel = list(allDataAnnotation.keys()), list(allDataAnnotation.values())
train_features, test_features, train_labels, test_labels = train_test_split(
    alabel, alist, train_size=0.8, random_state=algorithm_globals.random_seed
)




embeddings = []
gpt2_tokenizer.pad_token = gpt2_tokenizer.eos_token

# Generate embeddings for training features
for transcript in train_features:
    text = transcript
    print(text)
    
    inputs = gpt2_tokenizer(text, return_tensors='pt')
    try:
        with torch.no_grad():
            outputs = gpt2_model(**inputs)
            # The embeddings are typically in outputs.last_hidden_state
            embeddings_tensor = outputs.last_hidden_state.mean(dim=1)

            embeddings.append(embeddings_tensor.squeeze().numpy())  # Convert to numpy array
    except:
        embeddings.append(np.zeros(768))
        continue
# Convert list to numpy array if needed
import numpy as np
embeddings_array = np.array(embeddings)
print(embeddings_array.shape)


embeddings = []
#gpt2_tokenizer.pad_token = gpt2_tokenizer.eos_token

# Generate embeddings for test features
for transcript in test_features:
    text = transcript
    #print(text)
    
    inputs = gpt2_tokenizer(text, return_tensors='pt')
    try:
        with torch.no_grad():
            outputs = gpt2_tokenizer(**inputs)
            # The embeddings are typically in outputs.last_hidden_state
            embeddings_tensor = outputs.last_hidden_state.mean(dim=1)
            embeddings.append(embeddings_tensor.squeeze().numpy())  # Convert to numpy array
    except:
        embeddings.append(np.zeros(768))
        continue
# Convert list to numpy array if needed
import numpy as np
embeddings_array_test = np.array(embeddings)
print(embeddings_array_test.shape)


with open('train_embeddings.p', 'wb') as f:
    pickle.dump(embeddings_array, f)

with open('test_embeddings.p', 'wb') as f:
    pickle.dump(embeddings_array_test, f)
