from gtts import gTTS
from pathlib import Path
import os

def text_to_mp3(file_path='test.txt', language='en', app=None):
    if Path(file_path).is_file() and Path(file_path).suffix == '.txt': 
        print(f'[+] Original file {Path(file_path).name}')
       
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            text = text.replace('\n', '')
        my_text = gTTS(text=text, lang=language, slow=False)
        file_name = Path(file_path).stem
        mp3_file_path = os.path.join(app.config['UPLOAD_FOLDER_PDF'], f'{file_name}.mp3')
        my_text.save(mp3_file_path)
        return f'{file_name}.mp3'
    else:
        return 'File not exists, or it\'s not a TXT file'
    
