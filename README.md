# Text Encoding Converter

Convert text files between encodings, for example latin-1 to UTF-8.

## Requirements

- Python 3 (standard library only — no third-party packages)

## Usage

```bash
python3 main.py input.txt --from latin-1 --to utf-8 --output out.txt
python3 main.py input.txt --from utf-8 --to utf-16
python3 main.py --list
```

## Options

| Option | Description |
| --- | --- |
| `--from` | Source encoding (default: `utf-8`) |
| `--to` | Target encoding (default: `utf-8`) |
| `--output`, `-o` | Output file (default: stdout) |
| `--errors` | `strict`, `replace`, `ignore` or `backslashreplace` (default: `strict`) |
| `--list` | List common encodings and exit |

## Example

```bash
$ printf 'caf\xe9\n' > latin.txt
$ python3 main.py latin.txt --from latin-1 --to utf-8 --output utf8.txt
Converted latin.txt (latin-1) -> utf8.txt (utf-8), 5 characters
$ cat utf8.txt
café
```

## License

MIT — see `LICENSE`.
