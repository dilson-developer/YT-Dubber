import os
import subprocess
from rich.console import Console

console = Console()

def mix_audio(video_path: str, dubbed_audio_path: str, start_time: str, end_time: str, output_path: str) -> str:
    """
    Usa o FFmpeg para embutir o áudio dublado. Se o input for apenas áudio (.wav ou .mp3),
    gera um vídeo com tela preta automaticamente para evitar erros.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Ficheiro base não encontrado em: {video_path}")
    if not os.path.exists(dubbed_audio_path):
        raise FileNotFoundError(f"Áudio dublado não encontrado em: {dubbed_audio_path}")

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with console.status("[bold green]FFmpeg: A processar e a embutir a nova dobragem...", spinner="arc"):
        
        # Se o ficheiro base for apenas áudio, criamos uma tela preta em alta definição (1080p)
        if video_path.endswith(('.wav', '.mp3', '.webm')) and not any(v in video_path for v in ["video", "mp4"]):
            # Como o teu temp_audio.webm atual só tem áudio, criamos a tela preta com a duração do áudio dublado
            command = [
                'ffmpeg', '-y',
                '-f', 'lavfi', '-i', 'color=c=black:s=1920x1080:r=24', # Tela Preta Full HD
                '-i', dubbed_audio_path,
                '-c:v', 'libx264',
                '-tune', 'stillimage',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                '-shortest',
                output_path
            ]
        else:
            # Comando normal de substituição se for um vídeo real
            command = [
                'ffmpeg', '-y',
                '-ss', start_time,
                '-to', end_time,
                '-i', video_path,
                '-i', dubbed_audio_path,
                '-map', '0:v',
                '-map', '1:a',
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-shortest',
                output_path
            ]
        
        try:
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Erro na execução do FFmpeg: {str(e)}")

    return output_path