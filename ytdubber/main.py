from dotenv import load_dotenv
import os


load_dotenv()

from rich.console import Console
from ytdubber.ui import display_header, display_status_table, display_success
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
 
        console.print("\n[bold blue][1/5] A descarregar e a preparar média do YouTube...[/bold blue]")
        download_and_cut_audio(url, start_time, end_time) 
        
        
        for ficheiro in possiveis_videos:
            if os.path.exists(ficheiro):
                video_bruto = ficheiro
                break
        

        if not video_bruto or not os.path.exists(video_bruto):
            if os.path.exists(audio_recortado):
                video_bruto = audio_recortado
            else:
                raise FileNotFoundError("Não foi encontrado nenhum ficheiro base na raiz para o FFmpeg processar.")
            

        console.print("[bold cyan][2/5] A transcrever áudio original com o Whisper...[/bold cyan]")
        dados_transcricao = transcribe(audio_recortado)
        texto_original = dados_transcricao["text"]
        console.print(f"[dim]Texto original detetado: {texto_original}[/dim]")
        

        console.print("[bold yellow][3/5] A traduzir texto via API da Groq (Llama 3.1)...[/bold yellow]")
        texto_traduzido = translate(texto_original, target_language=target_lang)
        console.print(f"[dim]Texto traduzido: {texto_traduzido}[/dim]")
        

        console.print("[bold magenta][4/5] A gerar voz sintetizada em Português...[/bold magenta]")
        run_synthesis(texto_traduzido, language=target_lang, output_path=audio_dublado)
        
 
        console.print("[bold green][5/5] FFmpeg: A embutir a nova voz no vídeo final...[/bold green]")
        mix_audio(
            video_path=video_bruto,       
            dubbed_audio_path=audio_dublado,
            start_time=f"00:00:{start_time}", 
            end_time=f"00:00:{end_time - start_time}",
            output_path=video_final
        )
        
        display_success(video_final)
        return video_final

    except Exception as e:
        console.print(f"\n[bold red]Erro no Pipeline:[/bold red] {e}")
        return None

if __name__ == "__main__":

    URL_TESTE = "https://www.youtube.com/watch?v=npQ2IORdlvU"
    run_pipeline(URL_TESTE, start_time=10, end_time=45, target_lang="pt")