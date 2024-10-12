import argparse

def to_hex(char):
    return hex(ord(char))

def to_decimal(char):
    return ord(char)

def to_octal(char):
    return f"\\{oct(ord(char))[2:].zfill(3)}"

def to_unicode(char):
    return f"\\u{ord(char):04x}"

def process_characters(chars, format_func):
    return [format_func(char) for char in chars]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert characters to hex, decimal, octal, or unicode.")
    parser.add_argument("input", help="Character or path to a file containing characters")
    parser.add_argument("-f", "--format", choices=["hex", "decimal", "octal", "unicode"], default="hex", help="Output format")
    
    args = parser.parse_args()

    format_func = {
        "hex": to_hex,
        "decimal": to_decimal,
        "octal": to_octal,
        "unicode": to_unicode
    }[args.format]

    try:
        with open(args.input, "r") as file:
            characters = file.read()
    except FileNotFoundError:
        characters = args.input

    result = process_characters(characters, format_func)
    print(f"\n".join(result))
