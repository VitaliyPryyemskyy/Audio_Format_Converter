import whisper


def voice_recorder(file_path):

    """
    Transcribes speech from an audio file to a text file.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        str: Path to the generated text file.
    """
    
    model = whisper.load_model("base")
    result = model.transcribe(file_path)

    transcription_file = file_path.replace(".mp3", ".txt")
    with open(transcription_file, "w") as file:
        file.write(result["text"])

    return transcription_file

if __name__=='__main__':
    voice_recorder()