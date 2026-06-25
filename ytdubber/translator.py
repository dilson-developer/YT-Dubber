import os
from groq import Groq
from rich.console import Console

console = Console()

# Dicionário de línguas suportadas exigido pelo MVP
SUPPORTED_LANGUAGES = {
    "pt": "Português", 
    "en": "English", 
    "es": "Español", 
    "fr": "Français", 
    "de": "Deutsch", 
    "it": "Italiano",
    "ja": "日本語", 
    "zh": "中文", 
    "ar": "العربية", 
    "ru": "Pусский", 
    "ko": "한국어", 
    "hi": "हिन्दी", 
    "nl": "Nederlands", 
    "pl": "Polski", 
    "tr": "Türkçe"
}

def translate(text: str, target_language: str, source_language: str = "auto") -> str:
    """
    Usa a biblioteca 'groq' para chamar o modelo 'llama-3.1-8b-instant' e traduzir o texto.
    Retorna apenas a string traduzida, sem textos extras ou aspas.
    """
    if target_language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Língua alvo '{target_language}' não é suportada. Escolha uma de: {list(SUPPORTED_LANGUAGES.keys())}")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_key_here":
        raise ValueError("GROQ_API_KEY não foi configurada corretamente no ficheiro .env!")

    client = Groq(api_key=api_key)
    target_lang_name = SUPPORTED_LANGUAGES[target_language]

    system_prompt = (
        f"You are an expert translator. Translate the following text to {target_lang_name}. "
        "Return ONLY the direct translation. Do NOT include any explanations, do NOT include quotes, "
        "and do NOT add any extra commentary."
    )

    try:
        with console.status(f"[bold yellow]A comunicar com a API da Groq... Traduzindo para {target_lang_name} via Llama-3.1", spinner="dots"):
            
            # Chamada corrigida com o modelo atual ativo
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",  
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
            )
            
        return completion.choices[0].message.content.strip()

    except Exception as e:
        raise RuntimeError(f"Falha na API da Groq durante a tradução: {str(e)}")

if __name__ == "__main__":
    print("A iniciar o teste do módulo Translator...")
    TEXTO_TESTE = "Hello everyone! Welcome to this tutorial. Today we are going to build an AI application using Python from scratch."
    
    try:
        resultado = translate(TEXTO_TESTE, target_language="pt")
        print("\n" + "="*40)
        print(f"Original: {TEXTO_TESTE}")
        print(f"Tradução Groq: {resultado}")
        print("="*40)
    except Exception as erro:
        print(f"Erro no teste do tradutor: {erro}")