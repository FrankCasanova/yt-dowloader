from fastapi import FastAPI
from fastapi.responses import FileResponse
import yt_dlp
import subprocess
import asyncio
import time
import os

app = FastAPI()

@app.post("/convert")
async def convert_video(url: str):
    loop = asyncio.get_event_loop()

    # Descargar el audio usando yt-dlp y obtener el título del video
    audio_path = "temp/audio.mp3"
    info_task = loop.run_in_executor(None, get_video_info, url)
    download_task = loop.run_in_executor(None, download_audio, url, audio_path)

    # Esperar a que se completen las tareas de descarga y obtención de información
    await asyncio.gather(info_task, download_task)

    title = info_task.result().get('title', 'audio')

    # Retornar el archivo de audio
    audio_file = FileResponse(audio_path, media_type="audio/mp3", headers={"Content-Disposition": f'attachment; filename="{title}.mp3"'})
    
    # Eliminar el archivo después de 30 segundos
    loop.create_task(delete_file(audio_path))
    
    return audio_file

def get_video_info(url):
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
    return info

def download_audio(url, audio_path):
    command = f"yt-dlp -x --audio-format mp3 --ffmpeg-location C:/Users/frank/Downloads/ffmpeg-2023-10-18-git-e7a6bba51a-essentials_build/bin/ffmpeg.exe -o {audio_path} {url}"
    subprocess.call(command, shell=True)

async def delete_file(audio_path):
    await asyncio.sleep(30)
    if os.path.exists(audio_path):
        os.remove(audio_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('script:app', host="localhost", port=8000, reload=True)