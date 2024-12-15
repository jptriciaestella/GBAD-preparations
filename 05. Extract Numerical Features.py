import os
import librosa
import numpy as np
import pandas as pd
from tqdm.notebook import tqdm

# Function to extract features from an audio file
def extract_features(file_path, segment_length, file_name):
    try:
        # Load the audio file
        y, sr = librosa.load(file_path)
        # Calculate the number of segments based on the segment length and audio length
        num_segments = int(np.ceil(len(y) / float(segment_length * sr)))

        # Initialize a list to store the features for this file
        features = []

        # Extract features for each segment
        for i in range(num_segments):
            # Calculate start and end frame for the current segment
            start_frame = i * segment_length * sr
            end_frame = min(len(y), (i + 1) * segment_length * sr)
            
            # Extract audio for this segment
            y_segment = y[start_frame:end_frame]

            # Extract features
            chroma_stft = np.mean(librosa.feature.chroma_stft(y=y_segment, sr=sr))
            rms = np.mean(librosa.feature.rms(y=y_segment))
            spec_cent = np.mean(librosa.feature.spectral_centroid(y=y_segment, sr=sr))
            spec_bw = np.mean(librosa.feature.spectral_bandwidth(y=y_segment, sr=sr))
            rolloff = np.mean(librosa.feature.spectral_rolloff(y=y_segment, sr=sr))
            zcr = np.mean(librosa.feature.zero_crossing_rate(y_segment))
            mfccs = librosa.feature.mfcc(y=y_segment, sr=sr)
            mfccs_mean = np.mean(mfccs, axis=1)
            
            # Append the extracted features to the list
            features.append([chroma_stft, rms, spec_cent, spec_bw, rolloff, zcr, *mfccs_mean, file_name])

        return features
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Function to create the dataset
def create_dataset(main_dir, segment_length):
    subsets = ['01. Training', '02. Validation', '03. Testing']
    labels = ['FAKE', 'REAL']
    feature_list = []

    # Iterate over each subset (Training, Validation, Testing)
    for subset in subsets:
        subset_path = os.path.join(main_dir, f'GBAD Dataset/{subset}')
        
        # Iterate over all files in the subset directory
        for label in labels:
            print(f'Processing {label} files in {subset}...')
            label_path = os.path.join(subset_path, label)

            files = os.listdir(label_path)

            # Wrap the files iterable with tqdm to show the progress bar
            for file in tqdm(files, desc=f"{label} Files Progress"):
                file_path = os.path.join(label_path, file)

                # Extract the file name without the extension
                file_name = os.path.splitext(file)[0]

                # Extract the gender from the file name
                _, gender, _ = file_name.split('-')

                # Extract features for the current file
                file_features = extract_features(file_path, segment_length, file_name)

                if file_features:
                    # Append features of all segments along with the label and subset to the dataset
                    for segment_features in file_features:
                        feature_list.append(segment_features + [label, subset, gender])
                    
    # Create a DataFrame with the dataset
    df = pd.DataFrame(feature_list, columns=[
        'chroma_stft', 'rms', 'spectral_centroid', 'spectral_bandwidth', 'rolloff', 'zero_crossing_rate',
        'mfcc1', 'mfcc2', 'mfcc3', 'mfcc4', 'mfcc5', 'mfcc6', 'mfcc7', 'mfcc8', 'mfcc9', 'mfcc10',
        'mfcc11', 'mfcc12', 'mfcc13', 'mfcc14', 'mfcc15', 'mfcc16', 'mfcc17', 'mfcc18', 'mfcc19', 'mfcc20',
        'origin_sample', 'LABEL', 'SUBSET', 'GENDER'
    ])
    
    return df

### AUDIO - MAIN
# Directory where the dataset folders are located
main_dir = r'..\Gender-Balanced-Audio-Deepfake-Dataset'

# Length of the audio segments in seconds
segment_length = 5  # for 5 second segment

# Create the dataset (assuming create_dataset is a function defined elsewhere)
dataset = create_dataset(main_dir, segment_length)

# Ensure the output directory exists
output_dir = os.path.join(main_dir, 'GBAD Dataset')
os.makedirs(output_dir, exist_ok=True)

# Save the dataset to a CSV file
csv_output_path = os.path.join(output_dir, 'gbad_extracted_numerical_features.csv')
dataset.to_csv(csv_output_path, index=False)

print(f'Dataset created and saved to {csv_output_path}')
