import argparse
import html  # Importa el módulo para manejar la codificación HTML

# Funciones para convertir caracteres a diferentes formatos
def to_hex(char):
    return f"&#x{ord(char):x};"  # Formato hexadecimal: &#x6F;

def to_decimal(char):
    return f"&#{ord(char)};"  # Formato decimal: &#111;

def to_octal(char):
    return f"\\{oct(ord(char))[2:].zfill(3)}"

def to_unicode(char):
    return f"\\u{ord(char):04x}"

def to_html(char):
    return html.escape(char)  # Convierte el carácter a su entidad HTML

# Función para procesar un archivo de texto o una cadena
def process_characters(chars, format_func):
    return [format_func(char) for char in chars]

# Función para interpretar secuencias de escape
def interpret_separator(separator):
    return separator.encode().decode('unicode_escape')

# Main script
if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Convert characters to hex, decimal, octal, unicode, or HTML.")
    parser.add_argument("input", help="Character or path to a file containing characters")
    parser.add_argument("-f", "--format", choices=["hex", "decimal", "octal", "unicode", "html"], default="hex", help="Output format")
    parser.add_argument("-s", "--separator", default="\n", help="Separator between characters in the output")

    args = parser.parse_args()

    # Determine the conversion function based on user input
    format_func = {
        "hex": to_hex,
        "decimal": to_decimal,
        "octal": to_octal,
        "unicode": to_unicode,
        "html": to_html
    }[args.format]

    # Check if input is a file or a single character
    try:
        with open(args.input, "r") as file:
            characters = file.read()
    except FileNotFoundError:
        characters = args.input  # If file not found, treat input as a single character

    # Interpret the separator for escape sequences
    separator = interpret_separator(args.separator)

    # Process and display the converted characters
    result = process_characters(characters, format_func)

    # Use the specified separator to join the results
    print(separator.join(result))
