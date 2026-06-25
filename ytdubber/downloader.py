import os
import subprocess
from yt_dlp import YoutubeDL
from rich.console import Console

console = Console()

def download_and_cut_audio(url: str, start_time: int, end_time: int):
    """
    Descarrega o vídeo real em formato MP4 do YouTube e extrai um segmento 
    de áudio em formato WAV para alimentar o transcritor (Whisper).
    """
    # Configurações do yt-dlp para descarregar VÍDEO Real (máximo 720p para ser rápido no Hackathon)
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'temp_video.mp4', # Salva diretamente como temp_video.mp4 na raiz
        'noplaylist': True,
        'quiet': True
    }
    
    # 1. Download do Vídeo Bruto
    with console.status("[bold blue][1/2] A descarregar o vídeo completo do YouTube...", spinner="arrow3"):
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
    # 2. Cortar e extrair apenas o áudio desse segmento usando FFmpeg para o Whisper
    with console.status(f"[bold blue][2/2] A extrair áudio do segmento ({start_time}s às {end_time}s) para transcrição...", spinner="clock"):
        audio_recortado = "input_audio2.wav"
        
        # Comando FFmpeg para recortar o vídeo e extrair o áudio em formato WAV de alta qualidade
        command = [
            'ffmpeg', '-y',
            '-ss', str(start_time),
            '-to', str(end_time),
            '-i', 'temp_video.mp4',
            '-vn', # Ignora o vídeo, foca apenas em extrair o áudio
            '-acodec', 'pcm_s16le',
            '-ar', '16000', # Taxa de amostragem ideal para o Whisper (16kHz)
            '-ac', '1',     # Mono canal
            audio_recortado
        ]
        
        try:
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Falha ao extrair áudio com o FFmpeg: {str(e)}")

    return "temp_video.mp4", audio_recortado