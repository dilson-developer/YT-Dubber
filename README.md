# 🎥 YT DUBBER CLI

A command-line tool for automatically translating and dubbing YouTube videos, developed in Python for the “Built with Python” Hackathon.

## 🚀 How It Works
1. **Download & Cut:** Downloads the video and extracts the selected segment using `yt-dlp` and `FFmpeg`.
2. **Transcription:** Processes the original audio using the `Whisper` library.
3. **Translation:** Translates the text with technical context using the `Groq` API (Llama 3.1).
4. **Text-to-Speech:** Generates the new dubbing in Portuguese using `Edge-TTS`.
5. **Mixing:** Combines the original video with the new synthesized voice using `FFmpeg`.

## 🛠️ Technologies Used
- Python
- Typer (Command-Line Interface)
- Rich (Terminal Design)
- Groq API (Llama 3.1)
- Whisper & Edge-TTS
- FFmpeg

## 💻 Step-by-Step User Guide

Follow the instructions below to set up the environment and run the tool correctly on your system.

### ⚠️ Important Notice (For Windows users only)
By default, Windows blocks the execution of scripts in PowerShell. If this is the first time you’re running scripts on your system, open PowerShell as **Administrator** and run the following command to enable virtual environments:
```powershell

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

You can type Y (or S) when the system prompts you for confirmation.

1️⃣ Activate the Virtual Environment (venv)

Before running the tool, you need to activate the isolated environment where all dependencies are installed.

If you open the terminal as Administrator and the System32 folder appears, first run:

cd $HOME

Next, navigate to the project folder and activate the environment:

cd C:\Users\cucaz\YT-Dubber
.\venv\Scripts\Activate.ps1

💡 How do you know if it worked? You’ll see the (venv) prefix appear right at the beginning of your terminal’s command line.

2️⃣ Install Project Dependencies
With the virtual environment (venv) properly active, run the command below to install all the necessary libraries from requirements.txt:

PowerShell

pip install -r requirements.txt
3️⃣ How to Run the CLI
The tool works in a completely flexible way using arguments passed directly in the terminal. The basic command follows this structure:

PowerShell

python -m ytdubber.cli “VIDEO_URL” --start START_SECOND --end END_SECOND
🚀 Practical Test Example:
To process a video from second 10 to second 40, run:

PowerShell

python -m ytdubber.cli “[https://www.youtube.com/watch?v=xy-huFH5Ua4](https://www.youtube.com/watch?v=xy-huFH5Ua4)” --start 10 --end 40 --lang pt

YT DUBBER CLI is designed to be a global accessibility tool, offering full support for 15 languages for transcription, translation, and text-to-speech. The pipeline is set up to process:

Portuguese (Brazil)
Portuguese (Portugal)
English
Spanish
French
German
Italian
Dutch
Russian
Chinese (Mandarin)
Japanese
Korean
Arabic
Hindi
Turkish

🛑 Important Precautions When Using (What NOT to Do) To ensure the pipeline runs without interruptions, pay attention to the following system limits:

⏱️ Time Order (--start and --end): The start time (--start) must be earlier than the end time (--end). For example, specifying a start time of 30 seconds and an end time of 10 seconds will cause the system to crash and generate an immediate error in the CLI.

⏳ Video Duration Limit: Since this tool makes calls to external APIs (Groq and Edge-TTS), avoid processing very long clips at once (e.g., 1-hour videos). For quick testing and better performance during the Hackathon, use clips ranging from 30 to 60 seconds.

🔗 URL Format: Be sure to pass the complete YouTube URL enclosed in quotation marks “ ”, ensuring that the terminal does not misinterpret special characters in the link.

📁 Blocked Files: The system has an automatic cleanup mechanism that deletes temporary files from the previous test before starting a new one. Make sure you don’t have any video players (or Windows Media Player itself) open and playing the previously generated video; otherwise, the system won’t be able to delete it and will return an “Access Denied” error.

---
