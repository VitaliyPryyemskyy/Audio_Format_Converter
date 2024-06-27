# Audio_Format_Converter
Convert Files to MP3 and MP3 to Text


This build on Flask framework  application allows users to convert various file formats to MP3 and vice versa. It includes user authentication and different conversion options, such as PDF, text, images, YouTube videos, and voice recordings to MP3.

## Features
- User Registration and Login
- Convert Files to MP3
  - Supported formats: PDF, text, image, YouTube video
- Convert MP3 or voice recordings to Text

## Prerequisites
- Python 3.x
- PostgreSQL
- pip (Python package installer)
- Bash (for running `build.sh`)

## Installation

1. ### Clone the repository

git clone git@github.com:VitaliyPryyemskyy/Audio_Format_Converter.git

cd mp3-conversion-app

2. ### Configure PostgreSQL in config.py
Update the connection details in config.py with your PostgreSQL username and password.

3. ### Configure Flask application in app.py
Update the following variables in app.py:

UPLOAD_FOLDER and UPLOAD_FOLDER_PDF: Path to directory for storing uploaded files.
app.secret_key: Secret key for Flask session management.

4. ### Run the setup script in terminal
./build.sh

This script creates a virtual environment, installs necessary packages, sets up the database, and launches the application.

5. ### Run the unittests
python -m unittest 