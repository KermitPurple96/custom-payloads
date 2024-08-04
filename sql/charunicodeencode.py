#!/usr/bin/python3

import os
import string

def unicode_encode(payload):
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

def main():
    print(f"\n")
    try:
        while True:
            payload = input("[payload] >  ")
            result = unicode_encode(payload)
            print(f"Result: {result}")
            print(f"\n")
    except KeyboardInterrupt:
        print("\nShell terminada.")

if __name__ == "__main__":
    main()
