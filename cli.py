import argparse
import sys
import time
import shutil
from datetime import datetime
from ascii_art import render
from validation import validate_time, to_12h

def _compose_time(h: int, m: int, s: int, ampm: bool, seconds: bool, blink: bool) -> tuple[str, str | None]:
    """Retorna (base_display, sufixo_ampm) considerando 12h/24h, segundos e piscar."""
    if ampm:
        suffix = "AM" if h < 12 else "PM"
        hh = h % 12
        if hh == 0:
            hh = 12
        if seconds:
            base = f"{hh:02d}:{m:02d}:{s:02d}"
        else:
            base = f"{hh:02d}:{m:02d}"
    else:
        suffix = None
        if seconds:
            base = f"{h:02d}:{m:02d}:{s:02d}"
        else:
            base = f"{h:02d}:{m:02d}"

    if blink and s % 2 == 0:
        # Pisca apenas o primeiro ':' para enfatizar HH:MM
        base_display = base.replace(":", " ", 1)
    else:
        base_display = base
    return base_display, suffix

def _layout_output(lines: list[str], align: str, border: bool) -> str:
    """Centraliza/aplica borda conforme tamanho do terminal."""
    cols, rows = shutil.get_terminal_size(fallback=(80, 24))
    content_width = max((len(l) for l in lines), default=0)

    # Borda opcional
    framed: list[str]
    if border:
        inner_w = content_width
        top = f"┌{'─' * (inner_w)}┐"
        bottom = f"└{'─' * (inner_w)}┘"
        framed = [top]
        for l in lines:
            pad = " " * (inner_w - len(l))
            framed.append(f"│{l}{pad}│")
        framed.append(bottom)
        lines = framed
        content_width = max(len(l) for l in lines)

    # Alinhamento horizontal
    if align == "center":
        left_pad = max((cols - content_width) // 2, 0)
    else:
        left_pad = 0
    lines = [(" " * left_pad) + l for l in lines]

    # Centralização vertical apenas no modo live
    content_height = len(lines)
    top_pad = max((rows - content_height) // 2, 0)
    return ("\n" * top_pad) + "\n".join(lines)

def live_clock(ampm: bool, blink: bool, scale: int, color: str | None, *, seconds: bool, show_date: bool, align: str, border: bool):
    """
    Executa o relógio ao vivo, atualizando a cada segundo com melhorias de UI.
    """
    try:
        # Esconde cursor
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()
        while True:
            now = datetime.now()
            h, m, s = now.hour, now.minute, now.second
            base_display, suffix = _compose_time(h, m, s, ampm=ampm, seconds=seconds, blink=blink)
            art = render(base_display, scale=scale, color=color)

            lines = art.splitlines()
            art_width = len(lines[0]) if lines else 0
            
            # Adiciona linha em branco para espaçamento
            if suffix or show_date:
                lines.append("")
            
            if suffix:
                # Centraliza AM/PM
                suffix_padding = " " * ((art_width - len(suffix)) // 2)
                lines.append(f"{suffix_padding}{suffix}")
            
            if show_date:
                # Centraliza data
                date_str = now.strftime("%d/%m/%Y")
                date_padding = " " * ((art_width - len(date_str)) // 2)
                lines.append(f"{date_padding}{date_str}")

            frame = _layout_output(lines, align=align, border=border)
            # Limpa e posiciona no topo
            sys.stdout.write("\033[H\033[2J")
            sys.stdout.write(frame)
            sys.stdout.write("\n")
            sys.stdout.flush()
            # Ajusta para sincronizar com o segundo atual
            time.sleep(1 - (datetime.now().microsecond / 1_000_000))
    except KeyboardInterrupt:
        pass
    finally:
        # Restaura cursor e encerra
        sys.stdout.write("\033[?25h\nEncerrado.\n")
        sys.stdout.flush()

def parse_args(argv: list[str]) -> argparse.Namespace:
    """
    Faz o parsing dos argumentos da linha de comando.
    """
    parser = argparse.ArgumentParser(description="Relógio digital ASCII.")
    parser.add_argument("time", nargs="?", help="Horário HH:MM para exibir uma vez.")
    parser.add_argument("--live", action="store_true", help="Modo relógio em tempo real.")
    parser.add_argument("--ampm", action="store_true", help="Exibe em 12h.")
    parser.add_argument("--blink", action="store_true", help="Pisca os dois pontos no modo live.")
    parser.add_argument("--scale", type=int, default=1, help="Escala (>1 aumenta o tamanho).")
    parser.add_argument("--color", help="Cor ANSI.")
    parser.add_argument("--seconds", action="store_true", help="Mostra segundos no modo live.")
    parser.add_argument("--date", action="store_true", help="Mostra a data abaixo da hora no modo live.")
    parser.add_argument("--align", choices=["left", "center"], default="center", help="Alinhamento horizontal no modo live.")
    parser.add_argument("--border", action="store_true", help="Exibe uma borda ao redor do relógio no modo live.")
    return parser.parse_args(argv)

def get_display_string(time_str: str, ampm: bool, scale: int, color: str | None) -> str:
    """
    Retorna a string de exibição para um horário dado.
    """
    h, m = map(int, time_str.split(":"))
    if ampm:
        shown = to_12h(h, m).split()[0]
        suffix = "AM" if h < 12 else "PM"
        art = render(shown, scale=scale, color=color)
        # Centraliza o sufixo AM/PM com o relógio
        art_width = len(art.splitlines()[0])
        suffix_padding = " " * ((art_width - len(suffix)) // 2)
        return art + f"\n{suffix_padding}{suffix}"
    else:
        shown = f"{h:02d}:{m:02d}"
        return render(shown, scale=scale, color=color)

def main(argv: list[str] | None = None) -> str | None:
    """
    Função principal da CLI. Retorna a string de exibição ou None para modo live.
    """
    args = parse_args(argv or sys.argv[1:])

    if args.live:
        live_clock(
            ampm=args.ampm,
            blink=args.blink,
            scale=args.scale,
            color=args.color,
            seconds=args.seconds,
            show_date=args.date,
            align=args.align,
            border=args.border,
        )
        return None

    if not args.time:
        try:
            entered = input("Digite o horário no formato HH:MM: ").strip()
        except EOFError:
            sys.stderr.write("Erro: entrada não fornecida.\n")
            sys.exit(1)
    else:
        entered = args.time.strip()

    if not validate_time(entered):
        sys.stderr.write("Formato/valor inválido. Use HH:MM entre 00:00 e 23:59.\n")
        sys.exit(1)

    return get_display_string(entered, args.ampm, args.scale, args.color)