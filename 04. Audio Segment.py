from pydub import AudioSegment
import os

def split_and_number_audios(input_folder, output_folder, prefix, start_input_number, end_input_number, start_output_number):
    # Initialize the output file number
    output_file_number = start_output_number

    # Process each input file in the specified range
    for input_number in range(start_input_number, end_input_number + 1):
        # Construct the input file path
        input_file = os.path.join(input_folder, f"{input_number}.wav")
        
        # Load the audio file
        audio = AudioSegment.from_file(input_file)
        
        # Calculate the total duration in milliseconds
        duration_ms = len(audio)
        
        # Define the length of each segment (total duration / 5)
        segment_length_ms = duration_ms // 5
        
        # Iterate through the number of segments (fixed to 5) and export them
        for i in range(5):
            start_time = i * segment_length_ms
            end_time = start_time + segment_length_ms if i < 4 else duration_ms  # Ensure last segment includes any remaining time
            segment = audio[start_time:end_time]
            
            # Define the output filename with custom numbering and prefix
            output_filename = os.path.join(output_folder, f"{output_file_number}{prefix}.wav")
            
            # Export the segment as wav
            segment.export(output_filename, format="wav")
            print(f"Exported: {output_filename}")
            
            # Increment the output file number
            output_file_number += 1

# Example usage
input_folder = r"..\Gender Balanced Audio Deepfake Dataset\Scraps FAKE"  # Replace with your input folder path
output_folder = r"..\Gender Balanced Audio Deepfake Dataset\03. Testing\FAKE"  # Replace with your output folder path
prefix = "-MALE-TTS"  # Replace with your desired prefix
start_input_number = 100  # Replace with the starting input file number
end_input_number = 100 # Replace with the ending input file number
start_output_number = 46 # Replace with your desired starting output number

split_and_number_audios(input_folder, output_folder, prefix, start_input_number, end_input_number, start_output_number)
