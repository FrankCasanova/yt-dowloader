from fastapi import FastAPI
from fastapi.responses import FileResponse
import yt_dlp
import subprocess
import asyncio
import time
import os
from typing import Awaitable, Dict

app = FastAPI()

@app.post("/convert")
async def convert_video(url: str) -> FileResponse:
    """
    Convert a video from the given URL to an audio file and return the audio file as a response.
    Parameters:
        url (str): The URL of the video to convert.    
    Returns:
        FileResponse: The audio file as a FileResponse object.
    Raises:
        FileNotFoundError: If the video file could not be found.
        Exception: If an error occurs during the conversion process.
    """
    
    loop = asyncio.get_event_loop()
    audio_path = f"temp/audio.mp3"
    info_task = loop.run_in_executor(None, get_video_info, url)
    download_task = loop.run_in_executor(None, download_audio, url, audio_path)
   
    await asyncio.gather(info_task, download_task)
    title = info_task.result().get('title', 'audio')
    
    
    audio_file = FileResponse(audio_path, media_type="audio/mp3", headers={"Content-Disposition": f'attachment; filename="{title}.mp3"'})
    
    loop.create_task(delete_file(audio_path))
    
    return audio_file

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
    await asyncio.sleep(0.5)
    if os.path.exists(audio_path):
        os.remove(audio_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('script:app', host="localhost", port=8000, reload=True)
