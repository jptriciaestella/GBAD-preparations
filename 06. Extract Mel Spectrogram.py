import os
import pandas as pd
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
from PIL import Image

def create_melspectrograms(audio_path, output_dir, file_name, segment_length=10):
    # Load audio file
    y_main, sr_main = librosa.load(audio_path, sr=None)

    # Calculate total duration of audio in seconds
    total_duration = librosa.get_duration(y=y_main, sr=sr_main)

    # Calculate total number of segments
    total_segments = int(np.ceil(total_duration / segment_length))

    # Iterate over each segment
    for i in range(total_segments):
        y, sr = librosa.load(audio_path, offset=segment_length * i, duration=segment_length)

        # Extract mel spectrogram of the segment
        mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)

        # Convert to decibels
        mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

        # Create output directory if it does not exist
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{file_name}_{i}.png')

        # Plot mel spectrogram without color bar
        plt.figure(figsize=(8, 6))
        librosa.display.specshow(mel_spectrogram_db, sr=sr, x_axis='time', y_axis='mel')
        plt.axis('off')  # Turn off axis
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)  # Save without padding
        plt.close()

        # Resize image
        img = Image.open(output_path)
        img_resized = img.resize((224, 224))
        img_resized.save(output_path)

# Function to create the dataset
def create_dataset(main_dir, output_dir, segment_length):
    subsets = ['01. Training', '02. Validation', '03. Testing']
    labels = ['FAKE', 'REAL']

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

                # Create the corresponding output directory for mel spectrograms
                output_subset_dir = os.path.join(output_dir, subset, label)

                # Extract and save mel spectrogram for the current file
                create_melspectrograms(file_path, output_subset_dir, file_name, segment_length)

### AUDIO - MAIN
# Directory where the dataset folders are located
main_dir = r'..\Gender-Balanced-Audio-Deepfake-Dataset'

# Directory where the output mel spectrograms will be saved
output_dir = os.path.join(main_dir, 'GBAD Dataset/Extracted (Spectrograms)')

# Length of the audio segments in seconds
segment_length = 5  # for 5 second segment

# Create the dataset
create_dataset(main_dir, output_dir, segment_length)

print(f'Mel spectrograms created and saved in {output_dir}')
