import argparse

# Funciones para convertir caracteres a diferentes formatos
def to_hex(char):
    return hex(ord(char))

def to_decimal(char):
    return str(ord(char))

def to_octal(char):
    return f"\\{oct(ord(char))[2:].zfill(3)}"

def to_unicode(char):
    return f"\\u{ord(char):04x}"

# Función para procesar un archivo de texto o una cadena
def process_characters(chars, format_func):
    return [format_func(char) for char in chars]

# Main script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert characters to hex, decimal, octal, or unicode.")
    parser.add_argument("input", help="Character or path to a file containing characters")
    parser.add_argument("-f", "--format", choices=["hex", "decimal", "octal", "unicode"], default="hex", help="Output format")
    
    args = parser.parse_args()

    # Determine the conversion function based on user input
    format_func = {
        "hex": to_hex,
        "decimal": to_decimal,
        "octal": to_octal,
        "unicode": to_unicode
    }[args.format]

    # Check if input is a file or a single character
    try:
        with open(args.input, "r") as file:
            characters = file.read()
    except FileNotFoundError:
        characters = args.input  # If file not found, treat input as a single character

    # Process and display the converted characters
    result = process_characters(characters, format_func)
    
    # If the format is decimal, separate by commas; otherwise, use newlines
    if args.format == "decimal":
        print(",".join(result))
    else:
        print("\n".join(result))
