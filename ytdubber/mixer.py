import os
import subprocess
from rich.console import Console

console = Console()

def mix_audio(video_path: str, dubbed_audio_path: str, start_time: int, end_time: int, output_path: str) -> str:
    """
    Usa FFmpeg para embutir o áudio dublado no trecho correto do vídeo.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Ficheiro base não encontrado: {video_path}")
    if not os.path.exists(dubbed_audio_path):
        raise FileNotFoundError(f"Áudio dublado não encontrado: {dubbed_audio_path}")

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Converte para formato HH:MM:SS
    def segundos_para_tempo(segundos):
        h = int(segundos // 3600)
        m = int((segundos % 3600) // 60)
        s = int(segundos % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    start_str = segundos_para_tempo(start_time)
    end_str = segundos_para_tempo(end_time)

    with console.status("[bold green]FFmpeg: A embutir a nova dobragem...", spinner="arc"):
        if video_path.endswith(('.wav', '.mp3', '.webm')) and "video" not in video_path:
            # Caso seja só áudio (tela preta)
            command = [
                'ffmpeg', '-y',
                '-f', 'lavfi', '-i', 'color=c=black:s=1920x1080:r=24',
                '-i', dubbed_audio_path,
                '-c:v', 'libx264', '-tune', 'stillimage',
                '-c:a', 'aac', '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                '-shortest',
                output_path
            ]
        else:
            # Vídeo real - usa os tempos corretos
            command = [
                'ffmpeg', '-y',
                '-ss', start_str,
                '-to', end_str,
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
            raise RuntimeError(f"Erro no FFmpeg: {str(e)}")

    return output_path