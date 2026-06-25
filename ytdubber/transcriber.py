import os
import whisper
from rich.console import Console

# Inicializa o console do Rich para mensagens bonitas
console = Console()

def transcribe(audio_path: str, language: str = None) -> dict:
    """
    Carrega o modelo Whisper 'base' localmente e transcreve o ficheiro WAV.
    Retorna um dicionário com: {"text": str, "language": str, "segments": list}
    """
    # 1. Tratamento de erro: Verifica se o ficheiro de áudio existe
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"O ficheiro de áudio não foi encontrado em: {audio_path}")

    try:
        # 2. Mostra o spinner animado do Rich durante o carregamento e transcrição
        with console.status("[bold cyan]A carregar o modelo Whisper 'base' e a transcrever o áudio... (Isto corre localmente)", spinner="earth"):
            
            # Carrega o modelo "base" (faz download automático na primeira execução)
            model = whisper.load_model("base")
            
            # Executa a transcrição
            # Se language for passada (ex: 'en'), o Whisper força essa língua. Se for None, ele deteta automaticamente.
            result = model.transcribe(audio_path, language=language)
            
        # 3. Organiza o retorno exatamente como pedido no guião do MVP
        return {
            "text": result.get("text", "").strip(),
            "language": result.get("language", ""),
            "segments": result.get("segments", [])
        }

    except Exception as e:
        # Tratamento de erro caso o áudio esteja corrompido ou falte memória
        raise RuntimeError(f"Erro ao processar a transcrição com o Whisper: {str(e)}")

# --- TESTE LOCAL INDEPENDENTE ---
if __name__ == "__main__":
    # Caminho do áudio que gerámos na Fase 1
    # Como o script corre dentro de ytdubber/, precisamos de apontar para a raiz ou testar a partir da raiz
    TEST_AUDIO = "input_audio.wav"
    
    if os.path.exists(TEST_AUDIO):
        print("🎵 Ficheiro de teste encontrado! A iniciar o teste do Whisper...")
        try:
            dados_transcricao = transcribe(TEST_AUDIO)
            print("\n" + "="*40)
            print(f"Língua Detetada: {dados_transcricao['language']}")
            print(f"Texto Transcrito:\n{dados_transcricao['text']}")
            print("="*40)
        except Exception as erro:
            print(f"Erro no teste: {erro}")
    else:
        print(f"Para testar, garante que o ficheiro '{TEST_AUDIO}' está na raiz do projeto.")