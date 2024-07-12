from pytube import YouTube
from pathlib import Path
import os


def download_audio(video_url, app):

    """
    Downloads audio from a YouTube video as an MP3 file.

    Args:
        video_url (str): URL of the YouTube video.
        app (Flask app): Flask app instance with configuration for upload folder.

    Returns:
        str: Name of the downloaded MP3 file.
    """
    
    yt = YouTube(video_url)
    file_name = f"{yt.streams[0].title}.mp3"
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(
        output_path=app.config["UPLOAD_FOLDER_PDF"], filename=file_name
    )
    mp3_file_path = os.path.join(app.config["UPLOAD_FOLDER_PDF"], file_name)
    return file_name


if __name__=='__main__':
    download_audio()