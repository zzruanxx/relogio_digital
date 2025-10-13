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
                    expanded += c * (2 if c.strip() and c not in (" ", ".") else 1 * scale)
                segment = expanded
            rows[i] += segment + "  "
    if scale > 1:
        # Expansão vertical grosseira duplicando linhas intermediárias
        scaled_rows = []
        for line in rows:
            scaled_rows.extend([line] * scale)
        rows = scaled_rows
    return "\n".join(rows)

def colorize(text: str, color: str | None) -> str:
    """
    Aplica cor ANSI ao texto se especificada.
    """
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
    """
    Renderiza o horário em ASCII com escala e cor opcionais.
    """
    art = build_ascii(time_str, scale=scale)
    if color:
        art = "\n".join(colorize(line, color) for line in art.splitlines())
    return art