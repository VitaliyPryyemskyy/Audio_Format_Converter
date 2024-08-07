import whisper
import warnings
import os
from pathlib import Path

warnings.filterwarnings(
    "ignore", message="FP16 is not supported on CPU*", category=UserWarning
)


def new_mp3(file_path="test.mp3", app=None):

    """
    Transcribes speech from an MP3 file to a text file.

    Args:
        file_path (str): Path to the MP3 file.
        app (Flask app): Flask app instance with configuration for upload folder.

    Returns:
        str: Name of the generated text file or error message.
    """
    
    if Path(file_path).is_file() and Path(file_path).suffix == ".mp3":
        print(f"[+] Original file {Path(file_path).name}")
        model = whisper.load_model("base")
        result = model.transcribe(file_path)

        file_name = Path(file_path).stem
        txt_file_path = os.path.join(
            app.config["UPLOAD_FOLDER_PDF"], f"{file_name}.txt"
        )
        result_text = result["text"]

        with open(txt_file_path, "w") as txt_file:
            txt_file.write(result_text)

        return f"{file_name}.txt"
    else:
        return "File not exists, or it's not an MP3 file"

if __name__=='__main__':
    new_mp3()