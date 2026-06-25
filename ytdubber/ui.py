"""
ui.py — Visual interface for YT Dubber CLI
Design: cinema/film theme · amber accent · professional terminal
"""

import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import (
    Progress, SpinnerColumn, BarColumn,
    TextColumn, TimeElapsedColumn, TaskProgressColumn
)
from rich.columns import Columns
from rich.align import Align
from rich.rule import Rule
from rich.padding import Padding
from rich import box

console = Console()

# ── Color palette ────────────────────────────────────────────────────────────
AMBER   = "dark_orange"        # primary accent · cinema subtitle colour
SILVER  = "grey82"             # secondary text
GOLD    = "yellow"             # highlights / success
DIM     = "grey42"             # footers / subtle info
TEAL    = "cyan"               # parameter names
ERROR   = "bold red"
SUCCESS = "bold green"

# ── ASCII Banner ─────────────────────────────────────────────────────────────
BANNER = r"""
 ██╗   ██╗████████╗    ██████╗ ██╗   ██╗██████╗ ██████╗ ███████╗██████╗
 ╚██╗ ██╔╝╚══██╔══╝    ██╔══██╗██║   ██║██╔══██╗██╔══██╗██╔════╝██╔══██╗
  ╚████╔╝    ██║       ██║  ██║██║   ██║██████╔╝██████╔╝█████╗  ██████╔╝
   ╚██╔╝     ██║       ██║  ██║██║   ██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗
    ██║       ██║       ██████╔╝╚██████╔╝██████╔╝██████╔╝███████╗██║  ██║
    ╚═╝       ╚═╝       ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
"""

# ── Pipeline steps ───────────────────────────────────────────────────────────
PIPELINE_STEPS = [
    ("01", "DOWNLOAD",      "yt-dlp   ", "Downloading video from YouTube"),
    ("02", "EXTRACT",       "ffmpeg   ", "Cutting audio segment"),
    ("03", "TRANSCRIBE",    "whisper  ", "Transcribing speech to text"),
    ("04", "TRANSLATE",     "groq llm ", "Translating to target language"),
    ("05", "SYNTHESIZE",    "edge-tts ", "Synthesizing dubbed voice"),
    ("06", "MIX",           "ffmpeg   ", "Replacing audio in video"),
]


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN BANNER
# ─────────────────────────────────────────────────────────────────────────────
def display_header() -> None:
    """Displays the main banner with YT Dubber visual identity."""
    console.print()

    # ASCII banner in amber
    banner_text = Text(BANNER, style=f"bold {AMBER}")
    console.print(Align.center(banner_text))

    # Tagline
    tagline = Text("◈  Dub any YouTube video into any language  ◈", style=f"italic {SILVER}")
    console.print(Align.center(tagline))
    console.print()

    # Separator rule
    console.print(Rule(f"[{DIM}]▸ Built with Python · Hackathon 2026[/{DIM}]", style=DIM))
    console.print()


# ─────────────────────────────────────────────────────────────────────────────
#  CONFIG TABLE
# ─────────────────────────────────────────────────────────────────────────────
def display_config_table(url: str, start: str, end: str, lang: str, lang_name: str = None) -> None:
    """Displays a configuration summary before the pipeline starts."""

    table = Table(
        box=box.SIMPLE_HEAD,
        border_style=DIM,
        show_header=True,
        header_style=f"bold {AMBER}",
        padding=(0, 2),
        expand=False,
    )

    table.add_column("PARAMETER", style=TEAL, no_wrap=True, min_width=18)
    table.add_column("VALUE", style="white")

    # Truncate long URLs
    display_url = url if len(url) <= 55 else url[:52] + "..."

    # Use lang code as fallback if lang_name not provided
    name_display = lang_name if lang_name else lang.upper()

    table.add_row("▸ URL",          display_url)
    table.add_row("▸ Start",        f"[bold white]{start}[/bold white]")
    table.add_row("▸ End",          f"[bold white]{end}[/bold white]")
    table.add_row("▸ Target lang",  f"[bold {GOLD}]{name_display} [{lang.upper()}][/bold {GOLD}]")

    panel = Panel(
        Align.center(table),
        title=f"[bold {AMBER}]◈  JOB CONFIGURATION  ◈[/bold {AMBER}]",
        border_style=AMBER,
        padding=(1, 2),
    )
    console.print(panel)
    console.print()


# Alias — keeps main.py working without changes
# main.py calls: display_status_table(url, start_time, end_time, target_lang)
def display_status_table(url: str, start: int, end: int, lang: str) -> None:
    """Backward-compatible alias for display_config_table."""
    display_config_table(
        url=url,
        start=str(start),
        end=str(end),
        lang=lang,
        lang_name=lang.upper(),
    )


# ─────────────────────────────────────────────────────────────────────────────
#  PIPELINE TRACKER — current step indicator
# ─────────────────────────────────────────────────────────────────────────────
def display_pipeline_step(current_step: int) -> None:
    """
    Renders the full pipeline highlighting the current active step.
    current_step: 1–6
    """
    console.print()
    steps_text = Text()

    for i, (num, name, _, _) in enumerate(PIPELINE_STEPS, start=1):
        if i < current_step:
            # Done
            steps_text.append(f" ✔ {name} ", style=f"dim {SUCCESS}")
            steps_text.append("▸", style=DIM)
        elif i == current_step:
            # Active
            steps_text.append(f" ◉ {name} ", style=f"bold {AMBER}")
            if i < len(PIPELINE_STEPS):
                steps_text.append("▸", style=DIM)
        else:
            # Pending
            steps_text.append(f" ○ {name} ", style=DIM)
            if i < len(PIPELINE_STEPS):
                steps_text.append("▸", style=DIM)

    console.print(Align.center(steps_text))
    console.print()


# ─────────────────────────────────────────────────────────────────────────────
#  SPINNER / STEP PROGRESS
# ─────────────────────────────────────────────────────────────────────────────
def get_progress() -> Progress:
    """Returns an amber-styled Progress object to use as a context manager."""
    return Progress(
        SpinnerColumn(spinner_name="dots2", style=f"bold {AMBER}"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(
            bar_width=36,
            style=DIM,
            complete_style=AMBER,
            finished_style=SUCCESS,
        ),
        TaskProgressColumn(style=SILVER),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    )


def display_step_start(step_num: int) -> None:
    """Prints the header for each pipeline step."""
    num, name, tool, desc = PIPELINE_STEPS[step_num - 1]

    console.print(Rule(style=DIM))
    label  = Text(f"  STEP {num}/{len(PIPELINE_STEPS)}  ", style=f"bold black on {AMBER}")
    title  = Text(f"  {name}", style="bold white")
    detail = Text(f"  via {tool.strip()}  ·  {desc}", style=SILVER)

    console.print(label, title)
    console.print(detail)
    console.print()


# ─────────────────────────────────────────────────────────────────────────────
#  TRANSCRIPTION + TRANSLATION PANEL (side by side)
# ─────────────────────────────────────────────────────────────────────────────
def display_text_comparison(
    original_text: str,
    translated_text: str,
    source_lang: str,
    target_lang: str,
    target_lang_name: str = None,
) -> None:
    """Shows the original text and its translation in side-by-side panels."""

    name_display = target_lang_name if target_lang_name else target_lang.upper()

    original_panel = Panel(
        Text(original_text, style="white", overflow="fold"),
        title=f"[bold {SILVER}]ORIGINAL  [{source_lang.upper()}][/bold {SILVER}]",
        border_style=DIM,
        padding=(1, 2),
    )

    translated_panel = Panel(
        Text(translated_text, style=f"bold {GOLD}", overflow="fold"),
        title=f"[bold {GOLD}]TRANSLATION  [{target_lang.upper()}] {name_display}[/bold {GOLD}]",
        border_style=AMBER,
        padding=(1, 2),
    )

    console.print(Columns([original_panel, translated_panel], equal=True, expand=True))
    console.print()


# ─────────────────────────────────────────────────────────────────────────────
#  SUCCESS
# ─────────────────────────────────────────────────────────────────────────────
def display_success(output_path: str, elapsed: float = None) -> None:
    """Completion panel showing the output file path and optional total time.

    elapsed is optional — main.py calls display_success(path) with no timer.
    """
    console.print()
    console.print(Rule(f"[{SUCCESS}]━━━  DONE  ━━━[/{SUCCESS}]", style="green"))
    console.print()

    content = Text(justify="center")
    content.append("\n  ✔  ", style=SUCCESS)
    content.append("DUBBED VIDEO GENERATED SUCCESSFULLY\n\n", style="bold white")
    content.append("  Output:  ", style=SILVER)
    content.append(f"{output_path}\n", style=f"bold {AMBER}")

    if elapsed is not None:
        mins     = int(elapsed // 60)
        secs     = elapsed % 60
        time_str = f"{mins}m {secs:.1f}s" if mins else f"{secs:.1f}s"
        content.append("  Total time:  ", style=SILVER)
        content.append(f"{time_str}\n", style="white")

    console.print(Panel(
        Align.center(content),
        border_style="green",
        padding=(1, 4),
        title=f"[bold {SUCCESS}]◈  YT DUBBER  ◈[/bold {SUCCESS}]",
    ))
    console.print()
    console.print(Align.center(Text(
        "▸ Open the file above to watch the result  ◂",
        style=DIM
    )))
    console.print()


# ─────────────────────────────────────────────────────────────────────────────
#  ERROR
# ─────────────────────────────────────────────────────────────────────────────
def display_error(message: str, hint: str = "") -> None:
    """Error panel with a clear message and an optional fix hint."""
    content = Text()
    content.append("\n  ✖  ", style=ERROR)
    content.append(f"{message}\n", style="bold white")

    if hint:
        content.append(f"\n  Hint: {hint}\n", style=SILVER)

    console.print(Panel(
        content,
        border_style="red",
        title=f"[{ERROR}]ERROR[/{ERROR}]",
        padding=(0, 2),
    ))
    console.print()


# ─────────────────────────────────────────────────────────────────────────────
#  AVAILABLE LANGUAGES
# ─────────────────────────────────────────────────────────────────────────────
def display_languages(languages: dict) -> None:
    """Displays a table of all supported languages."""
    table = Table(
        box=box.SIMPLE_HEAD,
        border_style=DIM,
        header_style=f"bold {AMBER}",
        padding=(0, 3),
        show_lines=False,
    )
    table.add_column("CODE",             style=TEAL, no_wrap=True, min_width=8)
    table.add_column("LANGUAGE",         style="white")
    table.add_column("VOICE (Edge-TTS)", style=DIM)

    for code, (name, voice) in languages.items():
        table.add_row(code.upper(), name, voice)

    console.print(Panel(
        table,
        title=f"[bold {AMBER}]◈  AVAILABLE LANGUAGES  ◈[/bold {AMBER}]",
        border_style=AMBER,
    ))
    console.print()


# ─────────────────────────────────────────────────────────────────────────────
#  DEMO (python ui.py)
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    DEMO_LANGS = {
        "pt": ("Português",  "pt-PT-DuarteNeural"),
        "en": ("English",    "en-US-GuyNeural"),
        "es": ("Español",    "es-ES-AlvaroNeural"),
        "fr": ("Français",   "fr-FR-HenriNeural"),
        "de": ("Deutsch",    "de-DE-ConradNeural"),
        "it": ("Italiano",   "it-IT-DiegoNeural"),
        "ja": ("日本語",      "ja-JP-KeitaNeural"),
        "zh": ("中文",        "zh-CN-YunxiNeural"),
        "ar": ("العربية",    "ar-SA-HamedNeural"),
        "ru": ("Русский",    "ru-RU-DmitryNeural"),
        "ko": ("한국어",      "ko-KR-InJoonNeural"),
        "hi": ("हिन्दी",     "hi-IN-MadhurNeural"),
        "nl": ("Nederlands", "nl-NL-MaartenNeural"),
        "pl": ("Polski",     "pl-PL-MarekNeural"),
        "tr": ("Türkçe",     "tr-TR-AhmetNeural"),
    }

    display_header()

    # Simulate main.py calling display_status_table (old signature)
    display_status_table("https://youtube.com/watch?v=dQw4w9WgXcQ", 10, 45, "pt")

    for step in range(1, 7):
        display_pipeline_step(step)
        display_step_start(step)

        with get_progress() as progress:
            task = progress.add_task(f"Processing step {step}...", total=100)
            for _ in range(100):
                time.sleep(0.015)
                progress.advance(task)

        time.sleep(0.3)

    console.print()
    display_text_comparison(
        original_text="Welcome back to the channel! Today we're going to explore something really exciting — the world of automatic video dubbing using open-source AI tools.",
        translated_text="Bem-vindo de volta ao canal! Hoje vamos explorar algo realmente empolgante — o mundo da dublagem automática de vídeos usando ferramentas de IA de código aberto.",
        source_lang="en",
        target_lang="pt",
        target_lang_name="Português",
    )

    # Simulate main.py calling display_success with only one argument
    display_success("outputs/dubbed_10_45.mp4")

    display_languages(DEMO_LANGS)
