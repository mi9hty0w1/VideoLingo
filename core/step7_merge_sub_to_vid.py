import os, subprocess, time, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.step1_ytdlp import find_video_files
from rich import print as rprint
import cv2
import numpy as np

SRC_FONT_SIZE = 16
TRANS_FONT_SIZE = 18
FONT_NAME = 'Arial'
TRANS_FONT_NAME = 'Arial'
SRC_FONT_COLOR = '&HFFFFFF' 
SRC_OUTLINE_COLOR = '&H000000'
SRC_OUTLINE_WIDTH = 1
SRC_SHADOW_COLOR = '&H80000000'
TRANS_FONT_COLOR = '&H00FFFF'
TRANS_OUTLINE_COLOR = '&H000000'
TRANS_OUTLINE_WIDTH = 1 
TRANS_BACK_COLOR = '&H33000000'

def merge_subtitles_to_video():
    video_files = find_video_files()
    if not video_files:
        print("No video files found in the output directory.")
        return

    video_file = video_files[0]
    subtitle_file = os.path.join('output', 'src_subs.srt')

    if not os.path.exists(subtitle_file):
        print(f"Subtitle file {subtitle_file} not found.")
        return

    output_file = os.path.join('output', 'output_video_with_subs.mp4')

    ffmpeg_cmd = [
        'ffmpeg',
        '-i', video_file,
        '-vf', f"subtitles={subtitle_file}:force_style='FontName={FONT_NAME},FontSize={SRC_FONT_SIZE},PrimaryColour={SRC_FONT_COLOR},OutlineColour={SRC_OUTLINE_COLOR},BorderStyle=3,Outline={SRC_OUTLINE_WIDTH},Shadow=0,MarginV=35'",
        '-c:a', 'copy',
        output_file
    ]

    # Add different parameters based on whether it's macOS or not
    if not macOS:
        ffmpeg_cmd.insert(-2, '-preset')
        ffmpeg_cmd.insert(-2, 'veryfast')

    print("🎬 Start merging subtitles to video...")
    start_time = time.time()
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8')

    try:
        for line in process.stdout:
            print(line, end='')  # Print FFmpeg output in real-time
        
        process.wait()
        if process.returncode == 0:
            print(f"\n[Process completed in {time.time() - start_time:.2f} seconds.]")
            print("🎉🎥 Subtitles merging to video completed! Please check in the `output` folder 👀")
        else:
            print("\n[Error occurred during FFmpeg execution.]")
    except KeyboardInterrupt:
        process.kill()
        print("\n[Process interrupted by user.]")
    except Exception as e:
        print(f"\n[An unexpected error occurred: {e}]")
        if process.poll() is None:
            process.kill()

if __name__ == "__main__":
    merge_subtitles_to_video()