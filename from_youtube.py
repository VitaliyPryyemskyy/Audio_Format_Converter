from pytube import YouTube
from pathlib import Path
import os

def download_audio(video_url, app):
    yt = YouTube(video_url)
    file_name = f'{yt.streams[0].title}.mp3'
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=app.config['UPLOAD_FOLDER_PDF'], filename=file_name)
    mp3_file_path = os.path.join(app.config['UPLOAD_FOLDER_PDF'], file_name)
    return file_name
