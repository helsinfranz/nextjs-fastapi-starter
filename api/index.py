from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from yt_dlp import YoutubeDL
from typing import Dict, Optional

app = FastAPI()

# Define a Pydantic model for the request body
class VideoUrlRequest(BaseModel):
    url: str

def get_video_audio_urls(video_url: str) -> Dict[str, Optional[str]]:
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': 'm4a/bestvideo+bestaudio/best'
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        
        video_url = None
        audio_url = None
        
        # Extracting video URL
        if 'requested_formats' in info_dict:
            for f in info_dict['requested_formats']:
                if f['vcodec'] != 'none':
                    video_url = f['url']
                if f['vcodec'] == 'none' or f['acodec'] != 'none':
                    audio_url = f['url']
        else:
            # Single file containing both video and audio
            video_url = info_dict['url']
        
        result = {}
        if video_url:
            result['video'] = video_url
        if audio_url:
            result['audio'] = audio_url
        
        return result

@app.post('/api/getVideoAudioUrls')
async def get_video_audio(request: VideoUrlRequest):
    video_url = request.url
    
    if not video_url:
        raise HTTPException(status_code=400, detail="URL parameter is missing")
    
    result = get_video_audio_urls(video_url)
    return result
