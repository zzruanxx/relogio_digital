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

def display_time(time_str):
    rows = ["", "", "]
    for char in time_str:
        if char in DIGITS:
            digit = DIGITS[char]
            for i in range (3):
                rows[i] += digit[i] + "  "
      
     else:
         raise ValueError(f"Caractere invalido no horário: {char}")
         
         for row in rows:
             print(row)
    
    def main():
        time_input = input("Digite o horário no formato HH:MM (24h ou 12h): ").strip()
        
        if not (":" in time_input and len(time_input.split(":")) == 2):
            print("Formato inválido. Use HH:MM.")
            return
    
    for char in time_input:
        if char not in DIGITS and char != ":"
        print("Caractere inválido no horario.")
        return
    
    display_time(time_input)
    
    if __name__ == "__main__":
        main()