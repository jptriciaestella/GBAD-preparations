# GBAD-preparations

This repository contains tools and scripts for preparing and preprocessing audio data for the making of Gender Bias in Audio Deepfake (GBAD) dataset. Each script serves a specific purpose, ranging from downloading audio to extracting numerical and visual features. Below is a detailed description of each file and its functionality.

---

## 1. **Audio Downloader**
- **Purpose**: Downloads audio files from a list of YouTube URLs provided in a CSV file.
- **Input**: CSV file containing YouTube URLs.
- **Output**: Audio files in the specified format downloaded to a local directory (.wav).

---

## 2. **Audio Cutter - RAW**
- **Purpose**: Trims raw audio files (e.g., real recordings) into 5-minute segments based on specified start and end times. The tool helps in isolating high-quality segments without background noise.
- **Additional Feature**: Compresses the output audio files to the desired size (default: 25 MB) for compatibility with Applio application.
- **Input**: Audio files and time parameters (start and end).
- **Output**: Trimmed and compressed audio files (.wav).

---

## 3. **Audio Cutter - TTS**
- **Purpose**: Similar to the RAW audio cutter but designed for Text-to-Speech (TTS) audio files. This script processes multiple files in bulk without requiring start and end time parameters, as TTS audio typically contains only speech without background noise.
- **Additional Feature**: Compresses the output audio files to the desired size (default: 25 MB).
- **Input**: Bulk TTS audio files.
- **Output**: Compressed 5-minute audio files (.wav).

---

## 4. **Audio Segment**
- **Purpose**: Splits 5-minute audio files into smaller 1-minute segments with a standardized naming convention.
- **Input**: 5-minute audio files.
- **Output**: Five 1-minute audio segments per file (.wav).

---

## 5. **Extract Numerical Features**
- **Purpose**: Extracts 26 numerical audio features using the `librosa` library. These features include:
  - Chromagram
  - Root Mean Square (RMS)
  - Spectral Centroid
  - Spectral Bandwidth
  - Spectral Rolloff
  - Zero Crossing Rate
  - The first 20 Mel-Frequency Cepstral Coefficients (MFCCs)
- **Input**: Audio files or segments.
- **Output**: CSV containing the extracted numerical featuresm, with additional information extracted from GBAD Dataset: origin_sample, LABEL (FAKE/REAL), SUBSET (Training/Validation/Testing) serta GENDER (FEMALE/MALE).

---

## 6. **Extract Mel Spectrogram**
- **Purpose**: Generates 224x224 pixel Mel spectrogram images for each audio segment using the `librosa` library. These spectrograms are intended for use in machine learning and deep learning models.
- **Input**: Audio files or segments from the GBAD dataset.
- **Output**: Mel spectrogram images in PNG format.

---

## How to Use
1. Clone this repository:  
   ```bash
   git clone https://github.com/yourusername/GBAD-preparations.git
   cd GBAD-preparations
