import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable, NoTranscriptFound
from transformers import pipeline
from urllib.parse import urlparse, parse_qs
from typing import Optional

# Set page config for better appearance
st.set_page_config(
    page_title="YouTube Video Summarizer",
    page_icon="🎥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_summarizer():
    #Load the summarization model with caching to improve performance
    return pipeline("summarization", model="facebook/bart-large-cnn")

def extract_video_id(video_url):
    #extracting video id
    query = urlparse(video_url).query
    params = parse_qs(query)
    video_id=params.get("v", [None])[0]
    if video_id is None:
        raise ValueError("Invalid YouTube URL: couldn't extract video ID.")
    return video_id

def get_video_transcript(video_id: str) -> str:
    #Get transcript for a YouTube video
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except TranscriptsDisabled:
        st.warning("Subtitles are disabled for this video.")
        return ""
    except VideoUnavailable:
        st.error("The video is unavailable or doesn't exist.")
        return ""
    except NoTranscriptFound:
        st.warning("No transcript found for this video.")
        return ""
    except Exception as e:
        st.error(f"An error occurred while fetching transcript: {str(e)}")
        return ""

def clean_text(text: str) -> str:
    #Clean and preprocess the transcript text
    if not text:
        return ""
        
    # Remove timestamps and special characters
    text = re.sub(r'\[.*?\]|\(.*?\)|\{.*?\}', '', text)
    
    # Remove common filler words
    fillers = r'\b(uh|um|ah|like|you know|actually|basically|literally|I mean)\b'
    text = re.sub(fillers, '', text, flags=re.IGNORECASE)
    
    # Remove unwanted spaces and normalize
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def generate_summary(text: str, max_length: int = 150, min_length: int = 30) -> str:
    #Generate summary using the BART model
    if not text:
        return ""
    
    # Split text into chunks if too long for the model
    chunk_size = 1024
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    summarizer = load_summarizer()
    summaries = []
    
    for chunk in chunks:
        summary = summarizer(
            chunk,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        summaries.append(summary[0]['summary_text'])
    
    return " ".join(summaries)

# Streamlit UI
def main():
    st.title("🎥 YouTube Video Summarizer")
    st.markdown("""
        Enter a YouTube video URL to generate an AI-powered summary.
For best results, use videos with available subtitles or transcripts.
    """)
    
    
    
    video_url = st.text_input(
        "YouTube Video URL:",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed"
    )
    
    if st.button("Summarize") or video_url:
        if not video_url:
            st.warning("Please enter a YouTube URL")
            return
            
        with st.spinner("Processing video..."):
            video_id = extract_video_id(video_url)
            
            if not video_id:
                st.error("Could not extract video ID. Please check the URL.")
                return
                
            raw_text = get_video_transcript(video_id)
            
            if not raw_text:
                st.error("No transcript available for summarization.")
                return
                
            cleaned_text = clean_text(raw_text)
            
            
            
            summary = generate_summary(cleaned_text, max_length=50)
            
            st.subheader("📝 Summary")
            st.success(summary)
            
          
            
            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )
            with col2:
                st.download_button(
                    "Download Transcript",
                    data=cleaned_text,
                    file_name="transcript.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()