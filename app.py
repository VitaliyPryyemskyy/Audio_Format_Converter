from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    session,
    flash,
    url_for,
)
import psycopg2
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from main import convert_to_mp3
from pdf import pdf_to_mp3
from from_txt import text_to_mp3
from from_img import img_to_mp3
import hashlib
from config import connection
from from_youtube import download_audio
from from_mp3 import new_mp3
from voice_to_txt import voice_recorder

app = Flask(__name__)
app.secret_key = "secret_key"  # Replace 'secret_key' with your actual secret key

UPLOAD_FOLDER = "/home/path_to_project/uploads"  # Replace '/path/to/your/project/' with the actual path to your project
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

UPLOAD_FOLDER_PDF = "/home/path_to_project/uploads_pdf"  # Replace '/path/to/your/project/' with the actual path to your project
app.config["UPLOAD_FOLDER_PDF"] = UPLOAD_FOLDER_PDF


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/handle_form", methods=["GET", "POST"])
def handle_form():
    if request.method == "POST":
        user_login = request.form.get("login", "")
        user_password = request.form.get("password", "")
        confirmation_password = request.form.get("password_confirmation", "")
        if user_password != confirmation_password:
            return f"Passwords do not match! {render_template('form.html')}"
        elif len(user_password) < 8:
            return (
                f"Password must be more than 8 symbols {render_template('form.html')}"
            )
        with connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        "SELECT login FROM converter_users WHERE login = %s",
                        (user_login,),
                    )
                    stored_user = cursor.fetchone()
                    if stored_user:
                        return f"Username exists {render_template('form.html')}"
                    secured_password = hash_password(user_password)
                    cursor.execute(
                        "INSERT INTO converter_users(login, password) VALUES (%s, %s)",
                        (user_login, secured_password),
                    )
                    return (
                        f"Thank you for registration! {render_template('login.html')}"
                    )
                except psycopg2.errors.StringDataRightTruncation:
                    flash("Your username or password is too long")
                    return redirect(url_for("handle_form"))
    return render_template("form.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_login = request.form.get("login", "")
        user_password = request.form.get("password", "")
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, login, password FROM converter_users WHERE login = %s",
                    (user_login,),
                )
                user = cursor.fetchone()
                if user:
                    stored_password = user[2]
                    entered_password_hash = hash_password(user_password)
                    if entered_password_hash == stored_password:
                        session["login"] = user_login
                        return redirect("/choice")
                else:
                    return f"Wrong username or password {render_template('login.html')}"
    return render_template("login.html")


@app.route("/choice")
def choice():
    login = session.get("login")
    return render_template("choice.html", login=login)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    login = session.get("login")
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        audio_file = convert_to_mp3(Path(file_path))
        return f'<a href="/download/{audio_file.name}">Download MP3</a>'
    else:
        return render_template("upload.html", login=login)


@app.route("/download/<filename>", methods=["GET"])
def download_mp3(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"], filename, as_attachment=True
    )


@app.route("/from_pdf", methods=["GET", "POST"])
def upload_pdf():
    login = session.get("login")
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        language = request.form.get("language", "en")
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER_PDF"], filename)
        file.save(file_path)
        my_audio = pdf_to_mp3(file_path, language, app=app)
        return (
            f'<a href="/download_pdf_mp3/{os.path.basename(my_audio)}">Download MP3</a>'
        )
    else:
        return render_template("from_pdf.html", login=login)


@app.route("/download_pdf_mp3/<filename>", methods=["GET"])
def download_pdf_mp3(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER_PDF"], filename, as_attachment=True
    )


@app.route("/from_txt", methods=["GET", "POST"])
def convert_txt():
    login = session.get("login")
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        language = request.form.get("language", "en")
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER_PDF"], filename)
        file.save(file_path)
        my_audio = text_to_mp3(file_path, language, app=app)
        return f'<a href="/download_text_mp3/{os.path.basename(my_audio)}">Download MP3</a>'
    else:
        return render_template("from_txt.html", login=login)


@app.route("/download_text_mp3/<filename>", methods=["GET"])
def download_text_mp3(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER_PDF"], filename, as_attachment=True
    )


@app.route("/from_image", methods=["GET", "POST"])
def convert_image():
    login = session.get("login")
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        language = request.form.get("language", "en")
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER_PDF"], filename)
        file.save(file_path)
        my_audio = img_to_mp3(file_path, language, app=app)
        return f'<a href="/download_image_mp3/{os.path.basename(my_audio)}">Download MP3</a>'
    else:
        return render_template("from_image.html", login=login)


@app.route("/download_image_mp3/<filename>", methods=["GET"])
def download_image_mp3(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER_PDF"], filename, as_attachment=True
    )


@app.route("/from_youtube", methods=["GET", "POST"])
def convert_youtube():
    login = session.get("login")
    if request.method == "POST":
        video_url = request.form.get("video_url", "")
        if not video_url:
            return "No video URL provided"
        audio_file = download_audio(video_url, app=app)
        return f'<a href="/download_youtube_mp3/{os.path.basename(audio_file)}">Download MP3</a>'
    else:
        return render_template("from_youtube.html", login=login)


@app.route("/download_youtube_mp3/<filename>", methods=["GET"])
def download_youtube_mp3(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER_PDF"], filename, as_attachment=True
    )


@app.route("/new_mp3", methods=["GET", "POST"])
def bonus_mp3():
    login = session.get("login")
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER_PDF"], filename)
        file.save(file_path)
        my_text = new_mp3(file_path, app=app)
        return (
            f'<a href="/download_new_txt/{os.path.basename(my_text)}">Download text</a>'
        )
    else:
        return render_template("from_mp3.html", login=login)


@app.route("/download_new_txt/<filename>", methods=["GET"])
def download_new_txt(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER_PDF"], filename, as_attachment=True
    )


@app.route("/from_voice", methods=["GET", "POST"])
def convert_voice():
    login = session.get("login")
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER_PDF"], filename)
        file.save(file_path)
        my_text = voice_recorder(file_path)
        os.remove(file_path)
        return f'<a href="/download_voice_txt/{os.path.basename(my_text)}">Download text</a>'
    else:
        return render_template("from_voice.html", login=login)


@app.route("/download_voice_txt/<filename>", methods=["GET"])
def download_voice_txt(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER_PDF"], filename, as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)
