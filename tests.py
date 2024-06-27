import unittest
from app import app, hash_password
import hashlib
import os


class AppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_handle_form_get(self):
        response = self.app.get("/handle_form")
        self.assertEqual(response.status_code, 200)

    def test_login_get(self):
        response = self.app.get("/login")
        self.assertEqual(response.status_code, 200)

    def test_choice_without_login(self):
        response = self.app.get("/choice")
        self.assertEqual(response.status_code, 200)

    def test_hash_password(self):
        password = "password123"
        hashed = hash_password(password)
        self.assertEqual(hashed, hashlib.sha256(password.encode()).hexdigest())

    def test_upload_file_get(self):
        response = self.app.get("/upload")
        self.assertEqual(response.status_code, 200)

    def test_upload_file_no_file(self):
        response = self.app.post("/upload", data={})
        self.assertIn(b"No file part", response.data)

    def test_upload_file_no_filename(self):
        response = self.app.post("/upload", data={"file": (open(__file__, "rb"), "")})
        self.assertIn(b"No selected file", response.data)

    def test_upload_pdf_get(self):
        response = self.app.get("/from_pdf")
        self.assertEqual(response.status_code, 200)

    def test_upload_pdf_no_file(self):
        response = self.app.post("/from_pdf", data={})
        self.assertIn(b"No file part", response.data)

    def test_from_txt_get(self):
        response = self.app.get("/from_txt")
        self.assertEqual(response.status_code, 200)

    def test_from_image_get(self):
        response = self.app.get("/from_image")
        self.assertEqual(response.status_code, 200)

    def test_convert_image_no_file(self):
        response = self.app.post("/from_image", data={})
        self.assertIn(b"No file part", response.data)

    def test_convert_image_no_filename(self):
        response = self.app.post(
            "/from_image", data={"file": (open(__file__, "rb"), "")}
        )
        self.assertIn(b"No selected file", response.data)

    def test_convert_youtube_get(self):
        response = self.app.get("/from_youtube")
        self.assertEqual(response.status_code, 200)

    def test_convert_youtube_no_url(self):
        response = self.app.post("/from_youtube", data={})
        self.assertIn(b"No video URL provided", response.data)

    def test_bonus_mp3_get(self):
        response = self.app.get('/new_mp3')
        self.assertEqual(response.status_code, 200)

    def test_bonus_mp3_no_file(self):
        response = self.app.post('/new_mp3', data={})
        self.assertIn(b'No file part', response.data)

    def test_convert_voice_get(self):
        response = self.app.get('/from_voice')
        self.assertEqual(response.status_code, 200)

    def test_convert_voice_no_file(self):
        response = self.app.post('/from_voice', data={})
        self.assertIn(b'No file part', response.data)
