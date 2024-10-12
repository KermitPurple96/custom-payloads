import argparse
import html  

def to_hex(char):
    return hex(ord(char))

def to_decimal(char):
    return str(ord(char))

def to_octal(char):
    return f"\\{oct(ord(char))[2:].zfill(3)}"

def to_unicode(char):
    return f"\\u{ord(char):04x}"

def to_html(char):
    return html.escape(char)
    
def process_characters(chars, format_func):
    return [format_func(char) for char in chars]

def interpret_separator(separator):
    return separator.encode().decode('unicode_escape')

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Convert characters to hex, decimal, octal, unicode, or HTML.")
    parser.add_argument("input", help="Character or path to a file containing characters")
    parser.add_argument("-f", "--format", choices=["hex", "decimal", "octal", "unicode", "html"], default="hex", help="Output format")
    parser.add_argument("-s", "--separator", default="\n", help="Separator between characters in the output")

    args = parser.parse_args()

    format_func = {
        "hex": to_hex,
        "decimal": to_decimal,
        "octal": to_octal,
        "unicode": to_unicode,
        "html": to_html
    }[args.format]

    try:
        with open(args.input, "r") as file:
            characters = file.read()
    except FileNotFoundError:
        characters = args.input 

    separator = interpret_separator(args.separator)
    result = process_characters(characters, format_func)
    print(separator.join(result))


