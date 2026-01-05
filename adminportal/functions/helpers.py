import subprocess

import logging
logger = logging.getLogger("django")

def generate_thumbnail(video_path, timestamp, output_path):
    logger.debug(f"Generating thumbnail for {video_path} at {timestamp}s")
    """
    timestamp in seconds (float or int)
    """
    command = [
        "ffmpeg",
        "-ss", str(timestamp),
        "-i", video_path,
        "-frames:v", "1",
        "-q:v", "2",
        output_path,
        "-y"
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        logger.error(f"FFmpeg error: {result.stderr.decode()}")
        raise Exception("Failed to generate thumbnail")
    logger.debug(f"Thumbnail generated at {output_path}")
    return output_path