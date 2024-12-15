import pandas as pd
import os
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

def download_and_process_audio(csv_file, output_dir, skip_numbers, prefix):
    # Read URLs from CSV file
    urls = pd.read_csv(csv_file)['url'].tolist()
    
    # Initialize the counters
    input_counter = 1
    output_counter = 1
    
    for url in urls:
        # Check if the current input counter is in the skip list
        if input_counter in skip_numbers:
            input_counter += 1
            continue
        
        # Ensure output_counter skips the numbers in skip_numbers
        while output_counter in skip_numbers:
            output_counter += 1
        
        # Define yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, f'{prefix}{output_counter}.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            try:
                # Download and process the audio
                ydl.download([url])
                print(f"Downloaded and saved: {prefix}{output_counter}.mp3")
                output_counter += 1  # Increment the output counter only after successful download
            except DownloadError as e:
                print(f"Failed to download {url}. Error: {e}")
        
        # Increment the input counter regardless of success
        input_counter += 1

# Example usage
csv_file = r"..\Gender Balanced Audio Deepfake Dataset\urls.csv"  # Replace with your CSV file path containing URLs
output_dir = r'..\Gender Balanced Audio Deepfake Dataset\RAW REAL'  # Replace with your output directory
skip_numbers = [1, 2, 40, 41, 42, 43, 44, 85, 95]  # List of numbers to skip
prefix = 'downloaded_'  # Replace with your desired prefix

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

download_and_process_audio(csv_file, output_dir, skip_numbers, prefix)
