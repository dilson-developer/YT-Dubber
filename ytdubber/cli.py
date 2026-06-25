import typer
from ytdubber.main import run_pipeline
from ytdubber.ui import display_header, display_error

# Inicializa a aplicação Typer
app = typer.Typer(
    name="yt-dubber",
    help="YT DUBBER CLI - Tradutor e Dobrador Automático de Vídeos do YouTube",
    add_completion=False
)

@app.command()
def dub(
    url: str = typer.Argument(..., help="A URL completa do vídeo do YouTube que desejas dobrar."),
    start: int = typer.Option(0, "--start", "-s", help="O segundo inicial para o corte do vídeo."),
    end: int = typer.Option(30, "--end", "-e", help="O segundo final para o corte do vídeo."),
    lang: str = typer.Option("pt", "--lang", "-l", help="A língua alvo para a dobragem (ex: pt, es, fr).")
):
    """
    Executa o pipeline completo de dobragem de um vídeo do YouTube.
    """
    # Validação: mostra o banner antes de exibir o erro para manter a identidade visual
    if start >= end:
        display_header()
        display_error(
            "O tempo inicial (--start) deve ser menor que o tempo final (--end).",
            hint=f"Recebido: --start {start}  --end {end}  →  {start} >= {end}"
        )
        raise typer.Exit(code=1)

    # A partir daqui, main.py assume todo o output visual via ui.py:
    #   display_header(), display_status_table(), display_pipeline_step(),
    #   display_step_start(), display_text_comparison(), display_success() / display_error()
    resultado = run_pipeline(url=url, start_time=start, end_time=end, target_lang=lang)

    if not resultado:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
