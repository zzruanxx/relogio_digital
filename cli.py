import argparse
import sys
import time
from datetime import datetime
from ascii_art import render
from validation import validate_time, to_12h

def live_clock(ampm: bool, blink: bool, scale: int, color: str | None):
    """
    Executa o relógio ao vivo, atualizando a cada segundo.
    """
    try:
        while True:
            now = datetime.now()
            h, m, s = now.hour, now.minute, now.second
            if ampm:
                base = to_12h(h, m).split()[0]
            else:
                base = f"{h:02d}:{m:02d}"
            if blink and s % 2 == 0:
                base_display = base.replace(":", " ")
            else:
                base_display = base
            art = render(base_display, scale=scale, color=color)
            sys.stdout.write("\033[H\033[2J")
            sys.stdout.write(art + "\n")
            if ampm:
                sys.stdout.write(("AM" if h < 12 else "PM") + "\n")
            sys.stdout.flush()
            time.sleep(1 - (datetime.now().microsecond / 1_000_000))
    except KeyboardInterrupt:
        print("\nEncerrado.")

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
    return parser.parse_args(argv)

def get_display_string(time_str: str, ampm: bool, scale: int, color: str | None) -> str:
    """
    Retorna a string de exibição para um horário dado.
    """
    h, m = map(int, time_str.split(":"))
    if ampm:
        shown = to_12h(h, m).split()[0]
        suffix = "AM" if h < 12 else "PM"
        return render(shown, scale=scale, color=color) + f"\n{suffix}"
    else:
        shown = f"{h:02d}:{m:02d}"
        return render(shown, scale=scale, color=color)

def main(argv: list[str] | None = None) -> str | None:
    """
    Função principal da CLI. Retorna a string de exibição ou None para modo live.
    """
    args = parse_args(argv or sys.argv[1:])

    if args.live:
        live_clock(ampm=args.ampm, blink=args.blink, scale=args.scale, color=args.color)
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