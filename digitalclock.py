import argparse
import re
import time
import sys
from datetime import datetime

DIGITS = {
    "0": [" __ ",
          "|  |",
          "|__|"],
    "1": ["    ",
          "   |",
          "   |"],
    "2": [" __ ",
          " __|",
          "|__ "],
    "3": [" __ ",
          " __|",
          " __|"],
    "4": ["    ",
          "|__|",
          "   |"],
    "5": [" __ ",
          "|__ ",
          " __|"],
    "6": [" __ ",
          "|__ ",
          "|__|"],
    "7": [" __ ",
          "   |",
          "   |"],
    "8": [" __ ",
          "|__|",
          "|__|"],
    "9": [" __ ",
          "|__|",
          " __|"],
    ":": ["    ",
          "  . ",
          "  . "]
}

def build_ascii(time_str: str, scale: int = 1) -> str:
    """
    Constrói representação ASCII do horário.
    scale: aumenta largura/altura (apenas replicação simples).
    """
    rows = ["", "", ""]
    for ch in time_str:
        if ch not in DIGITS:
            raise ValueError(f"Caractere inválido: {ch}")
        pattern = DIGITS[ch]
        for i in range(3):
            segment = pattern[i]
            if scale > 1:
                # Expansão simples horizontal: duplicar caracteres internos
                expanded = ""
                for c in segment:
                    expanded += c * (2 if c.strip() and c not in (" ", ".") else 1*scale)
                segment = expanded
                # Expansão vertical: repetir linha (exceto separação)
            rows[i] += segment + "  "
    if scale > 1:
        # Expansão vertical grosseira duplicando linhas intermediárias
        scaled_rows = []
        for line in rows:
            scaled_rows.extend([line] * scale)
        rows = scaled_rows
    return "\n".join(rows)

def validate_time(hhmm: str) -> bool:
    if not re.fullmatch(r"\d{2}:\d{2}", hhmm):
        return False
    h, m = map(int, hhmm.split(":"))
    return 0 <= h <= 23 and 0 <= m <= 59

def to_12h(h: int, m: int) -> str:
    suffix = "AM" if h < 12 else "PM"
    h12 = h % 12
    if h12 == 0:
        h12 = 12
    return f"{h12:02d}:{m:02d} {suffix}"

def colorize(text: str, color: str | None) -> str:
    if not color:
        return text
    colors = {
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37",
        "bright": "97"
    }
    code = colors.get(color.lower())
    if not code:
        return text
    return f"\033[{code}m{text}\033[0m"

def render(time_str: str, scale: int = 1, color: str | None = None) -> str:
    art = build_ascii(time_str, scale=scale)
    if color:
        art = "\n".join(colorize(line, color) for line in art.splitlines())
    return art

def live_clock(ampm: bool, blink: bool, scale: int, color: str | None):
    try:
        while True:
            now = datetime.now()
            h, m, s = now.hour, now.minute, now.second
            if ampm:
                base = to_12h(h, m).split()[0]  # HH:MM
            else:
                base = f"{h:02d}:{m:02d}"
            # Piscar dois pontos
            if blink and s % 2 == 0:
                base_display = base.replace(":", " ")
            else:
                base_display = base
            art = render(base_display, scale=scale, color=color)
            # Limpa tela
            sys.stdout.write("\033[H\033[2J")
            sys.stdout.write(art + "\n")
            if ampm:
                sys.stdout.write(("AM" if h < 12 else "PM") + "\n")
            sys.stdout.flush()
            time.sleep(1 - (datetime.now().microsecond / 1_000_000))
    except KeyboardInterrupt:
        print("\nEncerrado.")

def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Relógio digital ASCII.")
    parser.add_argument("time", nargs="?", help="Horário HH:MM para exibir uma vez.")
    parser.add_argument("--live", action="store_true", help="Modo relógio em tempo real.")
    parser.add_argument("--ampm", action="store_true", help="Exibe em 12h (junto com modo live ou entrada valida).")
    parser.add_argument("--blink", action="store_true", help="Pisca os dois pontos no modo live.")
    parser.add_argument("--scale", type=int, default=1, help="Escala (>1 aumenta o tamanho).")
    parser.add_argument("--color", help="Cor ANSI (ex: red, green, yellow, blue, cyan, white, bright).")
    return parser.parse_args(argv)

def main(argv: list[str] | None = None):
    args = parse_args(argv or sys.argv[1:])

    if args.live:
        live_clock(ampm=args.ampm, blink=args.blink, scale=args.scale, color=args.color)
        return

    if not args.time:
        # Fallback input interativo
        entered = input("Digite o horário no formato HH:MM: ").strip()
    else:
        entered = args.time.strip()

    if not validate_time(entered):
        print("Formato/valor inválido. Use HH:MM entre 00:00 e 23:59.")
        sys.exit(1)

    h, m = map(int, entered.split(":"))
    if args.ampm:
        shown = to_12h(h, m).split()[0]
    else:
        shown = f"{h:02d}:{m:02d}"

    print(render(shown, scale=args.scale, color=args.color))
    if args.ampm:
        print("AM" if h < 12 else "PM")

if __name__ == "__main__":
    main()