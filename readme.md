#####🎬 Offline AI Video Caption Generator (Video + Subtitles)#####

Generate captions for videos offline using OpenAI Whisper and burn them directly into your video. This Streamlit app supports multiple languages and can produce English translations.

##Features

Upload video files: MP4, MOV, AVI, MKV

Extract audio and transcribe using Whisper

Generate captions in original language or English translation

Save captions as .srt file (downloadable)

Burn captions into video using project-scoped FFmpeg

Download video with embedded captions

Preview both captions and video inside the app

#Requirements

Python 3.11+

Packages:

pip install streamlit moviepy openai-whisper


FFmpeg binary inside your project folder:

offline_video_ai_generator/
├── main.py
└── ffmpeg/
    └── bin/
        └── ffmpeg.exe

Usage

Clone or download the project.

Ensure FFmpeg binary is in ffmpeg/bin/ffmpeg.exe.

Install dependencies:

pip install streamlit moviepy openai-whisper


Run the app:

streamlit run main.py


In the app:

Upload your video file.

Select Original Language or English Translation for captions.

Click Generate Captions and Burn into Video.

Download both .srt captions and video with captions.

Preview video and captions in the app.

Project Structure
offline_video_ai_generator/
├── app.py                  # Main Streamlit app
├── ffmpeg/                 # FFmpeg folder
│   └── bin/
│       └── ffmpeg.exe
└── README.md

Notes

Fully offline — no internet required after setup

Supports any spoken language → English translation if selected

Uses Whisper small model for a good balance of speed & accuracy

Final .mp4 has captions visibly burned in — compatible with YouTube, presentations, or any media player

License

MIT License – free to use and modify.

Do you want me to do that next?
