import re

def validate_time(hhmm: str) -> bool:
    """
    Valida formato HH:MM com horas 0-23 e minutos 0-59.
    """
    if not re.fullmatch(r"\d{2}:\d{2}", hhmm):
        return False
    h, m = map(int, hhmm.split(":"))
    return 0 <= h <= 23 and 0 <= m <= 59

def to_12h(h: int, m: int) -> str:
    """
    Converte hora 24h para 12h com sufixo AM/PM.
    """
    suffix = "AM" if h < 12 else "PM"
    h12 = h % 12
    if h12 == 0:
        h12 = 12
    return f"{h12:02d}:{m:02d} {suffix}"