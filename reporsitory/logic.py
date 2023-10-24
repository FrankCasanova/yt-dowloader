import yt_dlp
import subprocess
import asyncio
import os
from typing import Awaitable, Dict


def get_video_info(url: str) -> Dict[str, str]:
    """
    Retrieves information about a video from a given URL.
    Args:
        url: The URL of the video.
    Returns:
        Information about the video.
    """
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
    return info


def download_audio(url: str, audio_path: str) -> None:
    """
    Downloads audio from a given URL and saves it to a specified path.
    Args:
        url: The URL of the audio file to be downloaded.
        audio_path: The path where the downloaded audio file will be saved.
    Returns:
        None
    """
    command = (
        f"yt-dlp -x --audio-format mp3 --ffmpeg-location "
        f"C:/Users/frank/Downloads/ffmpeg-2023-10-18-git-e7a6bba51a-essentials_build/bin/ffmpeg.exe -o {audio_path} {url}"
    )
    subprocess.call(command, shell=True)
    

async def delete_file(audio_path: str) -> Awaitable[None]:
    """
    Deletes a file at the specified audio path.
    Args:
        audio_path (str): The path to the audio file to be deleted.
    """
    await asyncio.sleep(10)
    if os.path.exists(audio_path):
        os.remove(audio_path)
