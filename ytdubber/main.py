from dotenv import load_dotenv
import os
import tempfile
import shutil

temp_dir = "temp"
if not os.path.exits(temp_dir):
    os.makedirs(temp_dir)

audio_recortado = os.path.join(temp_dir, "input_audio.wav")
audio_dublado = os.path.join(temp_dir, "temp_voice_mp3")
video_final = f"outputs/dubbed_{start_time}_{end_time}.mp4"


load_dotenv()

from rich.console import Console
from ytdubber.ui import display_pipeline_step, display_step_start, display_text_comparison
from ytdubber.ui import display_header, display_status_table, display_success, display_pipeline_step, display_step_start, display_text_comparison
from ytdubber.downloader import download_and_cut_audio
from ytdubber.transcriber import transcribe
from ytdubber.translator import translate
from ytdubber.synthesizer import run_synthesis
from ytdubber.mixer import mix_audio

console = Console()

def run_pipeline(url: str, start_time: int, end_time: int, target_lang: str):
    display_header()
    display_status_table(url, start_time, end_time, target_lang)
    

    ficheiros_temporarios = [
        "temp_video.mp4", 
        "temp_audio.webm", 
        "temp_audio.webm.webm", 
        "input_audio2.wav", 
        "temp_voice.mp3"
    ]
    for f in ficheiros_temporarios:
        if os.path.exists(f):
            try:
                os.remove(f)
            except Exception:
                pass  



    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    

    audio_recortado = "input_audio2.wav"  
    audio_dublado = "temp_voice.mp3"     
    video_final = f"outputs/dubbed_{start_time}_{end_time}.mp4"
    

    possiveis_videos = ["temp_video.mp4", "temp_audio.webm", "temp_audio.webm.webm"]
    video_bruto = None

    try:
 
        # === ETAPA 1: Download ===
        display_pipeline_step(1)
        display_step_start(1)
        console.print("[bold blue]A descarregar e preparar o vídeo do YouTube...[/bold blue]")
        download_and_cut_audio(url, start_time, end_time)

        # === ETAPA 2: Transcrição ===
        display_pipeline_step(2)
        display_step_start(2)
        console.print("[bold cyan]A transcrever áudio com Whisper...[/bold cyan]")
        dados_transcricao = transcribe(audio_recortado)
        texto_original = dados_transcricao["text"]

        # === ETAPA 3: Tradução ===
        display_pipeline_step(3)
        display_step_start(3)
        console.print("[bold yellow]A traduzir texto via Groq...[/bold yellow]")
        texto_traduzido = translate(texto_original, target_language=target_lang)

        # === Mostrar comparação lado a lado ===
        display_text_comparison(
            original_text=texto_original,
            translated_text=texto_traduzido,
            source_lang=dados_transcricao.get("language", "auto"),
            target_lang=target_lang
        )

        # === ETAPA 4: Síntese de voz ===
        display_pipeline_step(4)
        display_step_start(4)
        console.print("[bold magenta]A gerar voz sintetizada...[/bold magenta]")
        run_synthesis(texto_traduzido, language=target_lang, output_path=audio_dublado)

        # === ETAPA 5: Mixagem ===
        display_pipeline_step(5)
        display_step_start(5)
        console.print("[bold green]FFmpeg: A embutir a nova voz no vídeo...[/bold green]")
        
        mix_audio(
            video_path=video_bruto,       
            dubbed_audio_path=audio_dublado,
            start_time=start_time, 
            end_time=end_time,
            output_path=video_final
        )
        
        display_success(video_final)
        return video_final

    except Exception as e:
        console.print(f"\n[bold red]Erro no Pipeline:[/bold red] {e}")
        return None
