import os
import streamlit as st
import whisper
import tempfile
from moviepy.editor import VideoFileClip
import subprocess

st.set_page_config(page_title="Offline AI Video Caption Generator", layout="wide")
st.title("🎬 Offline AI Video Caption Generator (Video + Captions)")

# -------------------------------
# Project-scoped FFmpeg setup
# -------------------------------
ffmpeg_bin = os.path.join(os.path.dirname(__file__), "ffmpeg", "bin", "ffmpeg.exe")
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_bin
os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_bin)

# -------------------------------
# File uploader
# -------------------------------
video_file = st.file_uploader(
    "Upload Video (MP4, MOV, AVI, MKV)", type=["mp4", "mov", "avi", "mkv"]
)

# -------------------------------
# Choose caption language
# -------------------------------
caption_option = st.radio(
    "Choose Caption Language:",
    ("Original Language", "English Translation")
)

# -------------------------------
# Helper function for SRT
# -------------------------------
def format_timestamp(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

if video_file is not None:
    st.video(video_file)

    # Save uploaded video in project folder
    video_path = os.path.join(os.path.dirname(__file__), video_file.name)
    with open(video_path, "wb") as f:
        f.write(video_file.read())

    if st.button("Generate Captions and Burn into Video"):
        st.info("Loading Whisper model...")
        model = whisper.load_model("small")

        st.write("🎧 Extracting audio from video...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            audio_path = temp_audio.name
            clip = VideoFileClip(video_path)
            clip.audio.write_audiofile(audio_path, codec='pcm_s16le', logger=None)
            clip.close()

        st.write("📝 Transcribing audio...")
        task_type = "translate" if caption_option == "English Translation" else "transcribe"
        result = model.transcribe(audio_path, verbose=False, task=task_type)

        # -------------------------------
        # Save captions as SRT
        # -------------------------------
        suffix = "_english" if task_type == "translate" else "_original"
        srt_path = os.path.splitext(video_path)[0] + f"{suffix}.srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(result["segments"], start=1):
                start = format_timestamp(seg["start"])
                end = format_timestamp(seg["end"])
                text = seg["text"].strip()
                f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

        st.success("✅ Captions generated!")

        # -------------------------------
        # Burn captions into video
        # -------------------------------
        st.write("🎞️ Burning captions into video...")
        output_video_path = os.path.splitext(video_path)[0] + f"{suffix}_subtitled.mp4"

        burn_cmd = [
            ffmpeg_bin,
            "-y",
            "-i", video_path,
            "-vf", f"subtitles={srt_path}",
            output_video_path
        ]
        subprocess.run(burn_cmd, check=True)

        st.success("✅ Video with captions created!")

        # -------------------------------
        # Download buttons
        # -------------------------------
        st.download_button(
            "⬇️ Download Captions (.srt)",
            open(srt_path, "rb"),
            file_name=os.path.basename(srt_path)
        )

        st.download_button(
            "⬇️ Download Video with Subtitles (.mp4)",
            open(output_video_path, "rb"),
            file_name=os.path.basename(output_video_path)
        )

        # -------------------------------
        # Previews
        # -------------------------------
        st.write("📋 **Preview of captions (first few lines):**")
        for seg in result["segments"][:5]:
            st.write(f"**{format_timestamp(seg['start'])} → {format_timestamp(seg['end'])}** — {seg['text']}")

        st.write("🎞️ **Preview Video with Captions:**")
        st.video(output_video_path)
