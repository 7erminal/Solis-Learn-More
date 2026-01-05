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
        output_path,
        "-y"
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print("FFMPEG STDOUT:", result.stdout)
    if result.returncode != 0:
        logger.error("FFmpeg error: %s", result.stderr.decode())
        logger.error(result.stderr.decode())
        raise Exception("Failed to generate thumbnail")
    logger.info(f"Thumbnail generated successfully {result.stdout.decode()}")
    logger.info(f"Return code: {result.returncode}")
    logger.debug(f"Thumbnail generated at {output_path}")
    return output_path