import os
import subprocess
import sys


def split_video(input_file, output_dir, clip_duration):
    os.makedirs(output_dir, exist_ok=True)
    output_pattern = os.path.join(output_dir, "clip_%03d.mp4")
    cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-f",
        "segment",
        "-segment_time",
        str(clip_duration),
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        output_pattern,
    ]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: split_video.py <input_file> <output_dir> <clip_duration>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    clip_duration = int(sys.argv[3])
    split_video(input_file, output_dir, clip_duration)
