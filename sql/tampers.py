#!/usr/bin/python3

import os
import string
import re

def unicode_encode(payload):

    #Unicode-URL-encodes all characters in a given payload (not processing already encoded)

    retVal = payload

    if payload:
        retVal = ""
        i = 0

        while i < len(payload):
            if payload[i] == '%' and (i < len(payload) - 2) and payload[i + 1:i + 2] in string.hexdigits and payload[i + 2:i + 3] in string.hexdigits:
                retVal += "%%u00%s" % payload[i + 1:i + 3]
                i += 3
            else:
                retVal += '%%u%.4X' % ord(payload[i])
                i += 1

    return retVal



def zeroeunion(payload):

    #Replaces instances of <int> UNION with <int>e0UNION

    return re.sub(r"(?i)(\d+)\s+(UNION )", r"\g<1>e0\g<2>", payload) if payload else payload


def apostrophemask(payload):

    # Replaces apostrophe character (') with its UTF-8 full width counterpart (e.g. ' -> %EF%BC%87)

    return payload.replace('\'', "%EF%BC%87") if payload else payload


def apostrophenullencode(payload):

    # Replaces apostrophe character (') with its illegal double unicode counterpart (e.g. ' -> %00%27)

    return payload.replace('\'', "%00%27") if payload else payload


def appendnullbyte(payload):

    #Appends (Access) NULL byte character (%00) at the end of payload

    return "%s%%00" % payload if payload else payload


def base64encode(payload):

    # Base64-encodes all characters in a given payload

    return encodeBase64(payload, binary=False) if payload else payload


def between(payload):

    #Replaces greater than operator ('>') with 'NOT BETWEEN 0 AND #' and equals operator ('=') with 'BETWEEN # AND #'
    
    retVal = payload

    if payload:
        match = re.search(r"(?i)(\b(AND|OR)\b\s+)(?!.*\b(AND|OR)\b)([^>]+?)\s*>\s*([^>]+)\s*\Z", payload)

        if match:
            _ = "%s %s NOT BETWEEN 0 AND %s" % (match.group(2), match.group(4), match.group(5))
            retVal = retVal.replace(match.group(0), _)
        else:
            retVal = re.sub(r"\s*>\s*(\d+|'[^']+'|\w+\(\d+\))", r" NOT BETWEEN 0 AND \g<1>", payload)

        if retVal == payload:
            match = re.search(r"(?i)(\b(AND|OR)\b\s+)(?!.*\b(AND|OR)\b)([^=]+?)\s*=\s*([\w()]+)\s*", payload)

            if match:
                _ = "%s %s BETWEEN %s AND %s" % (match.group(2), match.group(4), match.group(5), match.group(5))
                retVal = retVal.replace(match.group(0), _)

    return retVal


def binary(payload):

    #Injects keyword binary where possible
    
    retVal = payload

    if payload:
        retVal = re.sub(r"\bNULL\b", "binary NULL", retVal)
        retVal = re.sub(r"\b(THEN\s+)(\d+|0x[0-9a-f]+)(\s+ELSE\s+)(\d+|0x[0-9a-f]+)", r"\g<1>binary \g<2>\g<3>binary \g<4>", retVal)
        retVal = re.sub(r"(\d+\s*[>=]\s*)(\d+)", r"binary \g<1>binary \g<2>", retVal)
        retVal = re.sub(r"\b((AND|OR)\s*)(\d+)", r"\g<1>binary \g<3>", retVal)
        retVal = re.sub(r"([>=]\s*)(\d+)", r"\g<1>binary \g<2>", retVal)
        retVal = re.sub(r"\b(0x[0-9a-f]+)", r"binary \g<1>", retVal)
        retVal = re.sub(r"(\s+binary)+", r"\g<1>", retVal)

    return retVal


def main():
    print(f"\n")
    try:
        while True:
            payload = input("[payload] > ")

            # UNCOMMENT TO USE
            payload = zeroeunion(payload)
            payload = apostrophemask(payload)
            payload = apostrophenullencode(payload)
            payload = between(payload)
            payload = appendnullbyte(payload)
            payload = binary(payload)
            payload = unicode_encode(payload)
            payload = base64encode(payload)


            print(f"Result: {payload}")
            print(f"\n")
    except KeyboardInterrupt:
        print("\nShell terminada.")

if __name__ == "__main__":
    main()
