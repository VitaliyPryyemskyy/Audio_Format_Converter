from gtts import gTTS
import pdfplumber
from pathlib import Path
import os

    
def pdf_to_mp3(file_path='test.pdf', language='en', app=None):
    if Path(file_path).is_file() and Path(file_path).suffix == '.pdf': 
        print(f'[+] Original file {Path(file_path).name}')
        with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
        text = ''.join(pages)
        text = text.replace('\n', '')
       
        my_audio = gTTS(text=text, lang=language, slow=False)
        file_name = Path(file_path).stem
        mp3_file_path = os.path.join(app.config['UPLOAD_FOLDER_PDF'], f'{file_name}.mp3')
        print(f'[+] MP3 file path: {mp3_file_path}')  
        my_audio.save(mp3_file_path)
        
        return mp3_file_path  
    else:
        return None  
