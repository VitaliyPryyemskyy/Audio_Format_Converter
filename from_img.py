import pytesseract
from PIL import Image
from gtts import gTTS
from pathlib import Path
import os


def img_to_mp3(image_path="test.jpg", language="en", app=None):

    language_mapping = {
        "en": "eng",
        "uk": "ukr",
        "ru": "rus",
    }
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang=language_mapping.get(language, "eng"))
    tts_language = "en" if language == "eng" else language
    tts = gTTS(text=text, lang=tts_language, slow=False)
    file_name = Path(image_path).stem
    mp3_file_path = os.path.join(app.config["UPLOAD_FOLDER_PDF"], f"{file_name}.mp3")
    tts.save(mp3_file_path)

    return f"{file_name}.mp3"
