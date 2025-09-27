# GitHub PR Body Formatter

This directory contains tools for formatting and viewing GitHub pull request body content.

## Files

- `body.json` - Original file containing line-separated JSON strings with PR body content
- `body.txt` - Formatted, human-readable version of the PR bodies
- `pretty_print_body.py` - Python script to convert and format the JSON data

## Usage

### View formatted PR bodies
The easiest way is to simply open `body.txt` in any text editor. This file contains all PR bodies formatted for easy reading.

### Convert and format files
The script now supports both JSON and TXT input formats:

```bash
# Auto-convert (detects format automatically)
python pretty_print_body.py --convert

# Convert specific files
python pretty_print_body.py input.json output.txt
python pretty_print_body.py body.txt processed_body.txt

# Just print to console (auto-detects format)
python pretty_print_body.py body.json  # Shows JSON content
python pretty_print_body.py body.txt   # Shows TXT content

# Force a specific input format
python pretty_print_body.py --format json my_data.dat
python pretty_print_body.py --format txt my_data.dat
```

### Options
```bash
python pretty_print_body.py --help
```

## Supported Input Formats

### JSON Format
- **Line-separated JSON strings** (like the original `body.json`)
- **Proper JSON arrays** with string elements
- **Auto-detection** based on file extension or content

### TXT Format  
- **Pre-formatted text files** (like `body.txt`)
- **Any text content** that needs processing or reformatting
- **Auto-detection** for easy processing

## Why TXT format is better than JSON for this data

The original `body.json` file had several issues:
1. **Not valid JSON** - Contains multiple JSON strings on separate lines rather than a proper JSON array
2. **Hard to read** - Escape characters like `\r\n` make the content difficult to read
3. **Misleading extension** - The `.json` extension suggests proper JSON format

The `.txt` format provides:
- ✅ **Human readable** - Properly formatted markdown with line breaks
- ✅ **Easy to search** - Simple text format works with any editor
- ✅ **Clear structure** - Each PR body is numbered and separated
- ✅ **Correct encoding** - Escape characters are properly decoded
- ✅ **Format flexibility** - Can handle both JSON and TXT inputs

## Sample Output

```
[1] ──────────────────────────────────────────────────────────────────────
## PR Checklist

Please check if your PR fulfills the following requirements:

- [x] The commit message follows our guidelines: https://refine.dev/docs/guides-concepts/contributing/#commit-convention

## What is the new behavior?

docs: update rest data provider docs
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)