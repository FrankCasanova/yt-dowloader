from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from reporsitory.logic import get_video_info, download_audio, delete_file

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('script:app', host="localhost", port=8000, reload=True)
