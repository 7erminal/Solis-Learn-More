import subprocess

import logging
logger = logging.getLogger(__name__)

def generate_thumbnail(video_path, timestamp, output_path):
    logger.info("Generating thumbnail")
    """
    timestamp in seconds (float or int)
    """
    command = [
        "ffmpeg",
        "-ss", str(timestamp),
        "-i", video_path,
        "-frames:v", "1",
        "-q:v", "2",
        "-y",
        output_path
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print("FFMPEG STDOUT:", result.stdout)
    logger.error(f"FFMPEG STDERR: {result.stderr}")
    if result.returncode != 0:
        logger.error("FFmpeg error: %s", result.stderr)
        logger.error(result.stderr)
        raise Exception("Failed to generate thumbnail")
    logger.info(f"Thumbnail generated successfully {result.stdout}")
    logger.info(f"Return code: {result.returncode}")
    logger.debug(f"Thumbnail generated at {output_path}")
    return output_path