import moviepy.editor

def convert_to_mp3(video_file):
    video = moviepy.editor.VideoFileClip(str(video_file))
    audio = video.audio
    audio_file = video_file.with_suffix('.mp3')
    audio.write_audiofile(str(audio_file))
    return audio_file
