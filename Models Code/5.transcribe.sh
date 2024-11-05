#!/bin/bash

# Directory where your videos are located
video_dir="./"

# Directory where you want to save the transcription files
output_dir="./transcriptions/"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Iterate through each video file
for video_file in "$video_dir"/*.mp4; do
    if [[ -f "$video_file" ]]; then
        # Extract video name without extension
        video_name=$(basename "$video_file" .mp4)
        
        # Run vosk-transcribe command
        vosk-transcriber -i "$video_file" -o "${output_dir}${video_name}.txt"

        echo "Transcribed $video_name"
    fi
done

echo "Transcription complete."

