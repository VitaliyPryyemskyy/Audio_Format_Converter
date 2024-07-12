import moviepy.editor


def convert_to_mp3(video_file):

    """
    Converts video file to MP3 audio file.

    Args:
        video_file (Path): Path to the video file.

    Returns:
        Path: Path to the generated MP3 file.
    """
    
    video = moviepy.editor.VideoFileClip(str(video_file))
    audio = video.audio
    audio_file = video_file.with_suffix(".mp3")
    audio.write_audiofile(str(audio_file))
    return audio_file

if __name__=='__main__':
    convert_to_mp3()
