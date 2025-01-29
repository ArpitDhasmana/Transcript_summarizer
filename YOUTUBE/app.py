import sys
import os
import re
import groq
import markdown
from youtube_transcript_api import YouTubeTranscriptApi
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QLabel,
                             QStatusBar, QTextEdit, QHBoxLayout, QVBoxLayout)
from PyQt6.QtGui import QIcon

def extract_video_id(input_string):
    if re.match(r'https?:\/\/', input_string):
        if 'youtube.com' in input_string:
            match = re.search(r'v=([^&]*)', input_string)
            if match:
                return match.group(1)
        elif 'youtu.be' in input_string:
            match = re.search(r'youtu\.be/([^&]*)', input_string)
            if match:
                return match.group(1)
    return input_string


class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YouTube Transcript Downloader by Arpit')
        self.setWindowIcon(QIcon('transcription.png'))
        self.resize(800, 600)
        self.setStyleSheet('font-size: 15px;')

        self.layout = {}
        self.layout['main'] = QVBoxLayout()
        self.setLayout(self.layout['main'])

        self.init_ui()

    def init_container(self):
        self.button = {}
        self.line_edit = {}
        self.label = {}

    def init_ui(self):
        self.init_container()
        self._add_video_input_section()
        self._add_output_section()
        self._add_button_section()

        self.status_bar = QStatusBar()
        self.layout['main'].addWidget(self.status_bar)

    def _add_video_input_section(self):
        self.layout['video_input'] = QHBoxLayout()
        self.layout['main'].addLayout(self.layout['video_input'])

        self.label['video_id'] = QLabel('Video ID:')
        self.layout['video_input'].addWidget(self.label['video_id'])

        self.line_edit['video_id'] = QLineEdit()
        self.line_edit['video_id'].setFixedWidth(500)
        self.line_edit['video_id'].setPlaceholderText('Enter video ID or URL')
        self.layout['video_input'].addWidget(self.line_edit['video_id'])

        self.layout['video_input'].addStretch()

    def _add_output_section(self):
        self.label['output'] = QLabel('Transcript')
        self.layout['main'].addWidget(self.label['output'])

        self.text_edit = QTextEdit()
        self.layout['main'].addWidget(self.text_edit)

    def _add_button_section(self):
        self.layout['transcript_download'] = QHBoxLayout()
        self.layout['main'].addLayout(self.layout['transcript_download'])

        self.button['download_transcript'] = QPushButton('&Download Transcript')
        self.button['download_transcript'].setFixedWidth(175)
        self.button['download_transcript'].clicked.connect(self.download_transcript)
        self.layout['transcript_download'].addWidget(self.button['download_transcript'])

        self.button['summarize_transcript'] = QPushButton('&Summarize Transcript')
        self.button['summarize_transcript'].setFixedWidth(150)
        self.button['summarize_transcript'].clicked.connect(self.summarize_transcript)
        self.layout['transcript_download'].addWidget(self.button['summarize_transcript'])

        self.layout['transcript_download'].addStretch()

    def download_transcript(self):
        video_id = self.line_edit['video_id'].text()

        if not video_id:
            self.status_bar.showMessage('Please enter a video ID or URL')
            return
        else:
            self.status_bar.clearMessage()

        video_url = extract_video_id(video_id)

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_url)
            transcript_text = '\n'.join([f"{line['text']}" for line in transcript])
            self.text_edit.setPlainText(transcript_text)
        except Exception as e:
            self.text_edit.setText(f"Error: {e}")
            return

    def summarize_transcript(self):
        transcript_text = self.text_edit.toPlainText()
        if not transcript_text:
            self.status_bar.showMessage('Transcript is empty.')
            return
        else:
            self.status_bar.clearMessage()

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the video transcript below into bullet points: \n\n{transcript_text}",
                }
            ],
            model="llama3-8b-8192",
            temperature=0.3
        )

        html_content = markdown.markdown(chat_completion.choices[0].message.content)
        self.text_edit.setHtml(html_content)


if __name__ == "__main__":
    API_KEY = 'YOUR_GROJ_API_KEY'
    client = groq.Client(api_key=API_KEY)

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    app_window = AppWindow()
    app_window.show()

    sys.exit(app.exec())


