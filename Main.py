import streamlit as st
import os
import io
import google.generativeai as genai
from moviepy import VideoFileClip
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key=API_KEY)

# Function to extract audio from video using in-memory data
def extractingAudio(video_bytes, audio_path="temp_audio.wav"):
    try:
        with open("temp_video.mp4", "wb") as f:
            f.write(video_bytes)
        
        video_clip = VideoFileClip("temp_video.mp4")
        video_clip.audio.write_audiofile(audio_path, codec='pcm_s16le')
        
        # Explicitly close the video clip to release the file lock
        video_clip.close()
        
        os.remove("temp_video.mp4")  # Clean up temporary video file
        return True
    except Exception as e:
        st.error(f"Failed to extract audio: {e}")
        return False

# Function to extract transcript from audio
def extractingTranscript(audio_path, chunk_length_ms=300000):
    #transcribe audio
    try:
        audio = AudioSegment.from_wav(audio_path)
        transcript = []
        model = genai.GenerativeModel('models/gemini-1.5-flash')

        for i in range(0, len(audio), chunk_length_ms):
            chunk = audio[i:i + chunk_length_ms]
            chunk_byte = io.BytesIO()
            chunk.export(chunk_byte, format="wav")
            chunk_byte.seek(0)
            
            audio_file = genai.upload_file(chunk_byte, mime_type="audio/wav")
            
            prompt_part = [
                "Please provide a precise and complete transcription of this audio.",
                audio_file
            ]
            
            response = model.generate_content(prompt_part)
            transcript.append(response.text)
            
        return " ".join(transcript)
    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return None

# Function to generate summary
def generateSummary(transcript, summary_length="a concise summary"):

    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        prompt = f"Please provide {summary_length} of the following text:\n\n{transcript}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None

# Main Streamlit app function
def main():
    st.set_page_config(
        page_title="Video Summarizer",
        page_icon="🎬",
        layout="centered"
    )

    # UI elements
    st.title("🎬 Video to Text Summarizer")
    st.markdown("Uplaod video that you want to Transcribe and Translate.")

#file uploader 
    uploaded_file = st.file_uploader(
        "Upload a video file (.mp4)",
        type=['mp4']
    )

    if uploaded_file:
        st.video(uploaded_file)
        if st.button("Start Processing"):
            audio_file_path = "temp_audio.wav"
            
            with st.spinner("Extracting audio from video..."): #while processing
                video_bytes = uploaded_file.read()
                if not extractingAudio(video_bytes, audio_file_path):
                    st.error("Processing failed. Please try a different video.")
                    return

            st.success("Audio extraction complete!")
            
            with st.spinner("Generating transcript..."):
                full_transcript = extractingTranscript(audio_file_path)
            
            if not full_transcript:
                st.error("Transcript generation failed.")
            else:
                st.success("Transcription complete!")
                
                with st.expander("Show Transcript"): #expander for showing the transcript
                    st.markdown("---")
                    st.subheader("📝 Full Transcript")
                    st.write(full_transcript)
                
                with st.spinner("Generating summary..."):
                    summary = generateSummary(full_transcript, "a 3-bullet-point summary of the key takeaways")
                
                if summary:
                    st.success("Summary generation complete!")
                    with st.expander("Show Summary"):
                        st.markdown("---")
                        st.subheader("🔍 Summary")
                        st.markdown(summary)
                
                os.remove(audio_file_path) # Clean up temporary audio file

if __name__ == "__main__":
    main()
