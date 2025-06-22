# 🎥 YouTube Video Summarizer

A simple, powerful web app built with **Streamlit** that generates AI-powered summaries of YouTube videos. Paste a YouTube URL, and it will extract the subtitles, clean them, and summarize the content using a pretrained language model.

---

##  Features

- Extracts transcripts from YouTube videos using `youtube-transcript-api`
- Cleans and processes messy transcripts (removes fillers, timestamps, etc.)
- Generates natural summaries using the `facebook/bart-large-cnn` model from Hugging Face Transformers
- Download the summary or full transcript as `.txt` files
- Hosted on Streamlit Cloud

---

## Live Demo

 [Streamlit App](https://fida22-yt-video-summarizer-app-tkwxyl.streamlit.app/)

---

## 🖼️ Screenshots

| Input | Summary |
|-------|---------|
| ![Input](https://github.com/fida22/yt_video_summarizer/blob/c771d5721ceb90f6fa86ab1768008b666e80521b/images/Screenshot%20from%202025-06-22%2023-12-13.png) | ![Summary](screenshots/summary.png) |

---

## Tech Stack

- **Frontend & UI**: [Streamlit](https://streamlit.io)
- **Transcript Extraction**: [`youtube-transcript-api`](https://pypi.org/project/youtube-transcript-api/)
- **Summarization**: [`facebook/bart-large-cnn`](https://huggingface.co/facebook/bart-large-cnn) from [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- **Language**: Python 🐍

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/fida22/yt_video_summarizer
cd youtube-video-summarizer
```
### 2.Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app
```bash
streamlit run app.py
```

## How It Works
1. You paste a YouTube URL.
2. The app extracts the video ID.
3. It fetches the video's transcript using youtube-transcript-api.
4. Applies text cleaning: removes timestamps, filler words, and extra whitespace.
5. The cleaned text is sent to the BART model to generate a summary.
6. You can view and download the summary and transcript
