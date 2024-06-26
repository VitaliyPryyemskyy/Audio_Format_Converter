import whisper


def voice_recorder(file_path):

    model = whisper.load_model("base")
    result = model.transcribe(file_path)

    transcription_file = file_path.replace(".mp3", ".txt")
    with open(transcription_file, "w") as file:
        file.write(result["text"])

    return transcription_file
