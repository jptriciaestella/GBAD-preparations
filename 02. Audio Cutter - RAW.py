from pydub import AudioSegment
import os

def cut_and_compress_audio(input_dir, output_dir, audio_number, start_seconds, end_seconds, max_size_mb, prefix="downloaded_"):
    # Construct input and output file paths
    input_file = os.path.join(input_dir, f"{prefix}{audio_number}.mp3")
    output_file = os.path.join(output_dir, f"{audio_number}.wav")
    
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    
    # Convert start and end times to milliseconds
    start_ms = start_seconds * 1000
    end_ms = end_seconds * 1000
    
    # Cut the audio segment
    cut_segment = audio[start_ms:end_ms]
    
    # Temporary export to calculate initial file size
    temp_file = "temp.wav"
    cut_segment.export(temp_file, format="wav")
    
    # Calculate the initial file size in MB
    initial_size_mb = os.path.getsize(temp_file) / (1024 * 1024)
    
    # Remove the temporary file
    os.remove(temp_file)
    
    # Calculate the necessary bitrate to achieve the desired maximum file size
    duration_seconds = (end_seconds - start_seconds)
    target_bitrate = (max_size_mb * 8 * 1024 * 1024) / duration_seconds  # in bps (bits per second)
    
    # Ensure the bitrate is within reasonable limits
    target_bitrate = max(32000, min(target_bitrate, 320000))  # limits to a reasonable range (32 kbps to 320 kbps)
    
    # Export the cut segment with the calculated bitrate
    cut_segment.export(output_file, format="mp3", bitrate=f"{target_bitrate/1000:.0f}k")
    print(f"Exported: {output_file} with bitrate: {target_bitrate/1000:.0f} kbps")

# Example usage
input_dir = r"..\Gender Balanced Audio Deepfake Dataset\RAW REAL"  # Replace with your input directory of raw unprocessed audios
output_dir = input_dir  # Replace with your output directory if different
audio_number = 100 # Replace with the audio number
start_seconds = 15  # Replace with the start time in seconds
end_seconds = 300 + start_seconds  # Replace with the end time in seconds
max_size_mb = 25  # Maximum file size in MB

cut_and_compress_audio(input_dir, output_dir, audio_number, start_seconds, end_seconds, max_size_mb)