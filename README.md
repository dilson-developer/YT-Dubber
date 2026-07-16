# 🎥 YT DUBBER CLI v1.1.0

**Uma ferramenta CLI em Python para traduzir e dublar trechos de vídeos do YouTube de forma automática.**

Versão melhorada com **interface visual aprimorada**, correção de bugs importantes e melhor organização do projeto.

---

## 🚀 O que há de novo na v1.1.0

- Interface visual muito mais bonita e profissional (com pipeline steps e comparação de texto lado a lado)
- **Correção crítica** no corte de vídeo com FFmpeg (agora o tempo final está correto)
- Adicionado suporte a arquivo `.env` para configuração de API
- Melhor organização de arquivos temporários
- README e documentação atualizados

---

## 🛠️ Como Funciona

1. **Download & Corte** — Baixa o vídeo e extrai o trecho selecionado usando `yt-dlp` + `FFmpeg`
2. **Transcrição** — Transcreve o áudio com `Whisper` (modelo base)
3. **Tradução** — Traduz o texto usando a API da **Groq** (Llama 3.1)
4. **Text-to-Speech** — Gera a voz dublada com `Edge-TTS`
5. **Mixagem** — Combina o vídeo original com a nova voz usando `FFmpeg`

---

## 🧰 Tecnologias Utilizadas

- Python + Typer + Rich
- yt-dlp + FFmpeg
- OpenAI Whisper
- Groq API (Llama 3.1)
- Edge-TTS

---

## 📦 Instalação e Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/dilson-developer/YT-Dubber.git
cd YT-Dubber

2. Crie o ambiente virtual
Bashpython -m venv venv

3. Ative o ambiente virtual
Windows:
PowerShell.\venv\Scripts\Activate.ps1
Linux / Mac:
Bashsource venv/bin/activate

4. Instale as dependências
Bashpip install -r requirements.txt

5. Configure a chave da Groq (obrigatório)
Crie um arquivo chamado .env na raiz do projeto e coloque sua chave:
envGROQ_API_KEY=sua_chave_da_groq_aqui
Dica: Copie o arquivo .env.example e renomeie para .env

▶️ Como Usar
Bashpython -m ytdubber.cli "URL_DO_YOUTUBE" --start SEGUNDO_INICIAL --end SEGUNDO_FINAL --lang pt

Exemplo prático:
Bashpython -m ytdubber.cli "https://www.youtube.com/watch?v=xy-huFH5Ua4" --start 10 --end 40 --lang pt

🌍 Idiomas Suportados
O projeto suporta 15 idiomas para transcrição, tradução e dublagem:
pt, en, es, fr, de, it, ja, zh, ar, ru, ko, hi, nl, pl, tr

⚠️ Cuidados Importantes

O --start deve ser menor que o --end
Use trechos curtos (30 a 60 segundos) para testes
Coloque a URL entre aspas " "
Feche qualquer player de vídeo antes de rodar (pode dar erro de acesso negado)


📜 Changelog
Veja todas as mudanças da versão: CHANGELOG.md

📄 Licença
Este projeto foi desenvolvido para fins educacionais e de hackathon.

Desenvolvido por @dilson-developer