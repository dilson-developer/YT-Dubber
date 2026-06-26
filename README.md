# 🎥 YT DUBBER CLI

██╗   ██╗████████╗    ██████╗ ██╗   ██╗██████╗ ██████╗ ███████╗██████╗
 ╚██╗ ██╔╝╚══██╔══╝    ██╔══██╗██║   ██║██╔══██╗██╔══██╗██╔════╝██╔══██╗
  ╚████╔╝    ██║       ██║  ██║██║   ██║██████╔╝██████╔╝█████╗  ██████╔╝
   ...

   ◈  Dubla qualquer vídeo do YouTube para qualquer língua  ◈

───────────── ▸ Built with Python · Hackathon 2026 ─────────────

╭──────────── ◈  CONFIGURAÇÃO DO JOB  ◈ ───────────╮
│  ▸ URL         https://youtube.com/watch?v=...    │
│  ▸ Início      0:30                               │
│  ▸ Língua      Português [PT]                     │
╰───────────────────────────────────────────────────╯

 ✔ DOWNLOAD ▸ ◉ EXTRACT ▸ ○ TRANSCRIBE ▸ ○ TRANSLATE ▸ ○ MIX
  ETAPA 02/6  EXTRACT · via ffmpeg
  [████████████████████] 100%  0:00:01

Um tradutor e dobrador automático de vídeos do YouTube em linha de comando, desenvolvido em Python para o Hackathon "Built with Python".

## 🚀 Como Funciona
1. **Download & Corte:** Descarrega o vídeo e extrai o trecho selecionado usando `yt-dlp` e `FFmpeg`.
2. **Transcrição:** Processa o áudio original com a biblioteca `Whisper`.
3. **Tradução:** Traduz o texto com contexto técnico usando a API da `Groq` (Llama 3.1).
4. **Síntese de Voz:** Gera a nova dobragem em português com o `Edge-TTS`.
5. **Mixagem:** Junta o vídeo original com a nova voz sintetizada usando o `FFmpeg`.

## 🛠️ Tecnologias Utilizadas
- Python
- Typer (Interface de Linha de Comando)
- Rich (Design do Terminal)
- Groq API (Llama 3.1)
- Whisper & Edge-TTS
- FFmpeg

## 💻 Como Executar

## 💻 Guia de Uso Passo a Passo

Siga as instruções abaixo para configurar o ambiente e executar a ferramenta corretamente no seu sistema.

### ⚠️ Aviso Prévio Importante (Apenas para utilizadores Windows)
Por padrão, o Windows bloqueia a execução de scripts no PowerShell. Se esta for a primeira vez que executa scripts no seu sistema, abra o PowerShell como **Administrador** e execute o seguinte comando para permitir a ativação de ambientes virtuais:
```powershell

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Pode digitar Y (ou S) quando o sistema solicitar a confirmação.

1️⃣ Ativar o Ambiente Virtual (venv)

Antes de rodar a ferramenta, precisa de ativar o ambiente isolado onde todas as dependências estão instaladas.

Caso abra o terminal como Administrador e apareça a pasta System32, execute primeiro:

cd $HOME

De seguida, navegue até à pasta do projeto e ative o ambiente:

cd C:\Users\cucaz\YT-Dubber
.\venv\Scripts\Activate.ps1

💡 Como saber se funcionou? Verá o prefixo (venv) aparecer logo no início da linha de comandos do seu terminal.

2️⃣ Instalar as Dependências do Projeto
Com o ambiente virtual (venv) devidamente ativo, execute o comando abaixo para instalar todas as bibliotecas necessárias do requirements.txt:

PowerShell

pip install -r requirements.txt
3️⃣ Como Executar a CLI
A ferramenta funciona de forma totalmente flexível através de argumentos passados diretamente no terminal. O comando básico segue a seguinte estrutura:

PowerShell

python -m ytdubber.cli "URL_DO_VIDEO" --start SEGUNDO_INICIAL --end SEGUNDO_FINAL
🚀 Exemplo Prático de Teste:
Para processar um vídeo do segundo 10 até ao segundo 40, execute:

PowerShell

python -m ytdubber.cli "[https://www.youtube.com/watch?v=xy-huFH5Ua4](https://www.youtube.com/watch?v=xy-huFH5Ua4)" --start 10 --end 40 --lang pt

🛑 Cuidados Importantes ao Usar (O que NÃO fazer)Para garantir que o pipeline rode sem interrupções, preste atenção aos seguintes limites do sistema:

⏱️ Ordem dos Tempos (--start e --end): O tempo inicial (--start) tem de ser obrigatoriamente menor que o tempo final (--end). Por exemplo, pedir para começar no segundo 30 e terminar no 10 vai travar o sistema e gerar um erro imediato na CLI.

⏳ Limite de Duração do Vídeo: Como esta ferramenta faz chamadas a APIs externas (Groq e Edge-TTS), evite processar trechos muito longos de uma só vez (ex: vídeos de 1 hora). Para testes rápidos e melhor performance no Hackathon, utilize cortes de 30 a 60 segundos.

🔗 Formato da URL: Certifique-se de passar a URL completa do YouTube entre aspas " ", garantindo que o terminal não interprete caracteres especiais do link de forma errada.

📁 Ficheiros Bloqueados: O sistema possui um mecanismo de limpeza automática que apaga os ficheiros temporários do teste anterior antes de começar um novo. Certifique-se de que não tem nenhum player de vídeo (ou o próprio Windows Media Player) aberto a reproduzir o vídeo gerado anteriormente, caso contrário o sistema não conseguirá apagá-lo e dará erro de "Acesso Negado".

---
