from pydub import AudioSegment
import os

def convert_mp3_to_wav(input_dir, output_dir, duration_seconds=300, max_size_mb=25):
    # List all files in the input directory
    files = os.listdir(input_dir)
    
    for file in files:
        if file.endswith(".mp3"):
            mp3_file = os.path.join(input_dir, file)
            audio = AudioSegment.from_mp3(mp3_file)
            
            # Trim the audio to the specified duration (starting from 0 seconds)
            audio = audio[:duration_seconds * 1000]  # Convert seconds to milliseconds
            
            # Calculate the initial file size in bytes
            initial_size_bytes = len(audio.export(format="wav").read())
            
            # Calculate the target bitrate to achieve the desired maximum size
            target_bitrate = int((max_size_mb * 1024 * 1024 * 8) / (initial_size_bytes / 1000))
            
            # Determine output file name based on audio number
            audio_number = int(os.path.splitext(file)[0].split("_")[-1])
            if audio_number > 50:
                wav_file = os.path.join(output_dir, f"{audio_number}-NOT CONVERTED.wav")
            else:
                wav_file = os.path.join(output_dir, f"{audio_number}.wav")
            
            # Export the audio as WAV with the calculated bitrate
            audio.export(wav_file, format="wav", bitrate=f"{target_bitrate}k")
            
            print(f"Converted: {file} -> {os.path.basename(wav_file)} with bitrate: {target_bitrate} kbps")

# Example usage
input_dir = r"..\Gender Balanced Audio Deepfake Dataset\FAKE\Raw TTS"
output_dir = r"..\Gender Balanced Audio Deepfake Dataset\FAKE"
max_size_mb = 25  # Maximum file size in MB

convert_mp3_to_wav(input_dir, output_dir, max_size_mb=max_size_mb)
