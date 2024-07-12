from gtts import gTTS
from pathlib import Path
import os


def text_to_mp3(file_path="test.txt", language="en", app=None):

    """
    Converts text from a text file to an MP3 file.

    Args:
        file_path (str): Path to the text file.
        language (str): Language of the text (default is English).
        app (Flask app): Flask app instance with configuration for upload folder.

    Returns:
        str: Name of the generated MP3 file or error message.
    """
    
    if Path(file_path).is_file() and Path(file_path).suffix == ".txt":
        print(f"[+] Original file {Path(file_path).name}")

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            text = text.replace("\n", "")
        my_text = gTTS(text=text, lang=language, slow=False)
        file_name = Path(file_path).stem
        mp3_file_path = os.path.join(
            app.config["UPLOAD_FOLDER_PDF"], f"{file_name}.mp3"
        )
        my_text.save(mp3_file_path)
        return f"{file_name}.mp3"
    else:
        return "File not exists, or it's not a TXT file"

if __name__=='__main__':
    text_to_mp3()