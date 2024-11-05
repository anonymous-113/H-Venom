import os
from moviepy.editor import VideoFileClip,AudioFileClip

# Directory where your .mp4 files are located
video_dir = './'

# Directory where you want to save the .wav files
output_dir = './wav_files/'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
i = 1
# Process each .mp4 file in the input directory
for video_file in os.listdir(video_dir):
    if video_file.endswith('.mp4'):
        try:
            video_path = os.path.join(video_dir, video_file)
            
            output_path = os.path.join(output_dir, 'a_hate_'+os.path.splitext(video_file)[0] + '.wav')
            #print(output_path)
            # Load the video clip
            audio_clip = AudioFileClip(video_path)

            # Extract audio from the video clip
            #audio_clip = video_clip.audio

            # Write the audio to a .wav file
            audio_clip.write_audiofile(output_path)

            # Close the video and audio clips
            audio_clip.close()
        except IndexError:
            continue
        #video_clip.close()
        i+=1
        print(f"Converted {video_file} to {os.path.basename(output_path)}")
        print(i)
print("Conversion complete.")
