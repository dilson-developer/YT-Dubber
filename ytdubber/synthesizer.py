import asyncio
from edge_tts import Communicate
from rich.console import Console


console = Console()


VOICES = {
    "pt": "pt-PT-DuarteNeural",    # Português (Portugal)
    "en": "en-US-GuyNeural",       # Inglês (EUA)
    "es": "es-ES-AlvaroNeural",    # Espanhol (Espanha)
    "fr": "fr-FR-HenriNeural",     # Francês
    "de": "de-DE-ConradNeural",    # Alemão
    "it": "it-IT-DiegoNeural",     # Italiano
    "ja": "ja-JP-KeitaNeural",     # Japonês
    "zh": "zh-CN-YunxiNeural",     # Chinês
    "ar": "ar-SA-HamedNeural",     # Árabe
    "ru": "ru-RU-DmitryNeural",    # Russo
    "ko": "ko-KR-InGookNeural",    # Coreano
    "hi": "hi-IN-MadhurNeural",    # Hindi
    "nl": "nl-NL-MaartenNeural",   # Holandês
    "pl": "pl-PL-MarekNeural",     # Polaco
    "tr": "tr-TR-AhmetNeural"      # Turco
}

async def synthesize(text: str, language: str, output_path: str) -> str:
    """
    Função assíncrona que usa a biblioteca edge-tts para sintetizar voz.
    Guarda o áudio em formato MP3 no caminho especificado.
    """

    if language not in VOICES:
        raise ValueError(f"Língua '{language}' não tem uma voz mapeada no sistema. Escolha uma de: {list(VOICES.keys())}")
    
    voice = VOICES[language]
    
    try:
 
        with console.status(f"[bold magenta]A gerar voz sintetizada ({voice})...", spinner="bouncingBall"):
    
            communicate = Communicate(text, voice)
   
            await communicate.save(output_path)
            
        return output_path
        
    except Exception as e:

        raise RuntimeError(f"Falha na rede ou comunicação com o Edge-TTS: {str(e)}")

def run_synthesis(text: str, language: str, output_path: str) -> str:
    """
    3. Função síncrona que serve de ponte, chamando a função async com asyncio.run()
    """
    return asyncio.run(synthesize(text, language, output_path))



if __name__ == "__main__":
    print("A iniciar o teste do módulo Synthesizer (Edge-TTS)...")
    

    TEXTO_TRADUZIDO = "Olá a todos! Bem-vindos a este tutorial. Hoje vamos construir uma aplicação de inteligência artificial usando Python do zero."
    FICHEIRO_SAIDA = "test_output_voice.mp3"
    
    try:
        caminho_gerado = run_synthesis(TEXTO_TRADUZIDO, language="pt", output_path=FICHEIRO_SAIDA)
        print("\n" + "="*40)
        # 4. Confirmação de sucesso
        print(f"Sucesso! Áudio dublado gerado em: {caminho_gerado}")
        print("Dica: Podes abrir a pasta e ouvir o ficheiro para testar a qualidade!")
        print("="*40)
    except Exception as erro:
        print(f"Erro no teste de síntese de voz: {erro}")