#!/usr/bin/env python3
"""Convert text files between encodings (e.g. latin-1 to UTF-8).

Usage:
    python3 main.py input.txt --from latin-1 --to utf-8 --output out.txt
    python3 main.py input.txt --from utf-8 --to utf-16
    python3 main.py --list
"""
import argparse
import codecs
import sys

COMMON_ENCODINGS = [
    "utf-8", "utf-8-sig", "utf-16", "utf-16-le", "utf-16-be",
    "utf-32", "ascii", "latin-1", "iso-8859-1", "iso-8859-15",
    "windows-1252", "cp1250", "cp1251", "cp437", "shift_jis",
    "euc-jp", "gbk", "big5",
]


def list_encodings():
    print("Common encodings:")
    for name in COMMON_ENCODINGS:
        print(f"  {name}")
    print("\nAny codec name known to Python's codecs module is accepted,")
    print("for example: utf-7, koi8-r, iso-8859-2, mac-roman.")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Convert text files between encodings.")
    parser.add_argument("input", nargs="?",
                        help="input text file (required unless --list)")
    parser.add_argument("--from", dest="source", default="utf-8",
                        help="source encoding (default: utf-8)")
    parser.add_argument("--to", dest="target", default="utf-8",
                        help="target encoding (default: utf-8)")
    parser.add_argument("--output", "-o",
                        help="output file (default: stdout, text mode)")
    parser.add_argument("--errors", default="strict",
                        choices=["strict", "replace", "ignore", "backslashreplace"],
                        help="error handling: strict, replace, ignore or "
                             "backslashreplace (default: strict)")
    parser.add_argument("--list", action="store_true",
                        help="list common encodings and exit")
    args = parser.parse_args(argv)

    if args.list:
        list_encodings()
        return 0
    if not args.input:
        parser.error("input file is required (or use --list)")

    for name in (args.source, args.target):
        try:
            codecs.lookup(name)
        except LookupError:
            print(f"error: unknown encoding: {name}", file=sys.stderr)
            return 1

    try:
        with open(args.input, "rb") as handle:
            raw = handle.read()
    except FileNotFoundError:
        print(f"error: file not found: {args.input}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"error: cannot read {args.input}: {exc}", file=sys.stderr)
        return 1

    try:
        text = raw.decode(args.source, errors=args.errors)
    except UnicodeDecodeError as exc:
        print(f"error: cannot decode as {args.source}: {exc}", file=sys.stderr)
        return 1
    try:
        encoded = text.encode(args.target, errors=args.errors)
    except UnicodeEncodeError as exc:
        print(f"error: cannot encode as {args.target}: {exc}", file=sys.stderr)
        return 1

    if args.output:
        try:
            with open(args.output, "wb") as handle:
                handle.write(encoded)
        except OSError as exc:
            print(f"error: cannot write {args.output}: {exc}", file=sys.stderr)
            return 1
        print(f"Converted {args.input} ({args.source}) -> "
              f"{args.output} ({args.target}), {len(text)} characters")
    else:
        sys.stdout.buffer.write(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
