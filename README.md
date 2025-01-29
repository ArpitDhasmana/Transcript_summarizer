# YouTube Transcript Downloader & Summarizer  

This Python-based GUI application allows users to extract and summarize transcripts from YouTube videos. It is built using PyQt6 for the interface and integrates the YouTube Transcript API and LLaMA 3 (via Groq API) for transcript retrieval and summarization.  

## Features  
- 🎥 **Download YouTube Transcripts**: Extracts the full transcript of a given YouTube video.  
- 📄 **Summarize Transcripts**: Uses LLaMA 3 AI to generate a concise bullet-point summary.  
- 🖥️ **User-Friendly Interface**: Simple and intuitive PyQt6-based GUI.  


## Usage  
1. Enter a YouTube video ID or URL.  
2. Click "Download Transcript" to fetch the video transcript.  
3. Click "Summarize Transcript" to generate a summary using AI.  

## Dependencies  
- Python 3.8+  
- PyQt6  
- YouTube Transcript API  
- Groq API (for AI-based summarization)  
- Markdown  

## API Configuration  
Replace `API_KEY` in `main.py` with your Groq API key.  

## License  
This project is open-source under the MIT License.  
