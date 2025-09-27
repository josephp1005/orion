#!/usr/bin/env python3
"""
Convert and Pretty Print GitHub PR Bodies
This script can handle both JSON and TXT input formats:
- JSON: Line-separated JSON strings or proper JSON arrays
- TXT: Already formatted PR bodies (like body.txt)
Can output to console or save to a file.
"""

import json
import sys
import re
from pathlib import Path

def detect_file_format(file_path):
    """
    Detect whether the input file is JSON or TXT format.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: 'json' or 'txt'
    """
    file_extension = Path(file_path).suffix.lower()
    
    # If extension is clear, use it
    if file_extension == '.json':
        return 'json'
    elif file_extension == '.txt':
        return 'txt'
    
    # If unclear, try to detect from content
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            first_line = file.readline().strip()
            
        # Check if first line looks like JSON
        if first_line.startswith('"') or first_line.startswith('{') or first_line.startswith('['):
            return 'json'
        else:
            return 'txt'
    except:
        # Default to json for backward compatibility
        return 'json'

def pretty_print_txt_file(file_path):
    """
    Read and pretty print a TXT file that's already formatted.
    Can also reformat and clean up the display.
    
    Args:
        file_path (str): Path to the TXT file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print("=" * 80)
        print(f"FORMATTED PR BODIES FROM: {file_path}")
        print("=" * 80)
        print()
        
        # If it looks like our formatted file, extract just the PR bodies
        if "GitHub Pull Request Bodies" in content:
            # Split by the numbered entries
            entries = re.split(r'\n\[\d+\] ─+\n', content)
            
            # Skip the header (first entry)
            pr_entries = entries[1:] if len(entries) > 1 else entries
            
            print(f"Found {len(pr_entries)} PR body entries:")
            print()
            
            for i, entry in enumerate(pr_entries):
                if entry.strip():
                    print(f"[{i + 1}] " + "─" * 70)
                    print(entry.strip())
                    print()
        else:
            # Just print the content as-is
            print(content)
        
        print("=" * 80)
        print("END OF TXT DATA")
        print("=" * 80)
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def pretty_print_json_file(file_path):
    """
    Read and pretty print a JSON file with proper formatting.
    Handles both proper JSON arrays and line-separated JSON strings.
    
    Args:
        file_path (str): Path to the JSON file
    """
    try:
        # First, try to read as a single JSON object
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
        
        print("=" * 80)
        print(f"PRETTY PRINTED JSON FROM: {file_path}")
        print("=" * 80)
        print()
        
        # Try to parse as single JSON first
        try:
            data = json.loads(content)
            print("Detected: Single JSON object/array")
            print()
            
            # If it's a list, enumerate and print each item
            if isinstance(data, list):
                print(f"Found {len(data)} items in the JSON array:")
                print()
                
                for i, item in enumerate(data):
                    print(f"[{i + 1}] " + "─" * 70)
                    if isinstance(item, str):
                        # Decode escape characters and format the string nicely
                        decoded_text = item.encode().decode('unicode_escape')
                        print(decoded_text)
                    else:
                        print(json.dumps(item, indent=2, ensure_ascii=False))
                    print()
            
            # If it's a dict, pretty print it
            elif isinstance(data, dict):
                print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # If it's a single string, decode it
            elif isinstance(data, str):
                decoded_text = data.encode().decode('unicode_escape')
                print(decoded_text)
            
            # For other types, just print as JSON
            else:
                print(json.dumps(data, indent=2, ensure_ascii=False))
        
        except json.JSONDecodeError:
            # If single JSON parsing fails, try line-by-line parsing
            print("Detected: Line-separated JSON strings")
            print()
            
            lines = content.split('\n')
            valid_lines = [line.strip() for line in lines if line.strip()]
            
            print(f"Found {len(valid_lines)} JSON lines:")
            print()
            
            for i, line in enumerate(valid_lines):
                try:
                    json_obj = json.loads(line)
                    print(f"[{i + 1}] " + "─" * 70)
                    
                    if isinstance(json_obj, str):
                        # Decode escape characters and format the string nicely
                        decoded_text = json_obj.encode().decode('unicode_escape')
                        print(decoded_text)
                    else:
                        print(json.dumps(json_obj, indent=2, ensure_ascii=False))
                    print()
                    
                except json.JSONDecodeError as e:
                    print(f"[{i + 1}] ─── INVALID JSON ───")
                    print(f"Error: {e}")
                    print(f"Raw content: {line[:100]}...")
                    print()
        
        print("=" * 80)
        print("END OF JSON DATA")
        print("=" * 80)
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{file_path}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def convert_txt_to_txt_file(input_file, output_file):
    """
    Process and clean up an existing TXT file, creating a new formatted version.
    
    Args:
        input_file (str): Path to the input TXT file
        output_file (str): Path to the output text file
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        output_lines = [
            "GitHub Pull Request Bodies (Processed)",
            "=" * 60,
            "",
            f"This file was processed from: {Path(input_file).name}",
            f"Processing date: {sys.modules['datetime'].datetime.now().strftime('%Y-%m-%d %H:%M:%S') if 'datetime' in sys.modules else 'Unknown'}",
            ""
        ]
        
        # If it looks like our formatted file, extract and reformat the PR bodies
        if "GitHub Pull Request Bodies" in content:
            # Split by the numbered entries
            entries = re.split(r'\n\[\d+\] ─+\n', content)
            
            # Skip the header (first entry)
            pr_entries = entries[1:] if len(entries) > 1 else entries
            
            for i, entry in enumerate(pr_entries):
                if entry.strip():
                    output_lines.append(f"[{i + 1}] " + "─" * 70)
                    output_lines.append(entry.strip())
                    output_lines.append("")
        else:
            # Just add the content as-is with some formatting
            output_lines.append("Content:")
            output_lines.append("─" * 70)
            output_lines.append(content)
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(output_lines))
        
        print(f"Successfully processed {input_file} to {output_file}")
        
    except Exception as e:
        print(f"Error during TXT processing: {e}")
        sys.exit(1)

def convert_to_txt_file(input_file, output_file=None, input_format=None):
    """
    Convert a file to a readable text file.
    Handles both JSON and TXT input formats.
    
    Args:
        input_file (str): Path to the input file (JSON or TXT)
        output_file (str): Path to the output text file (optional)
        input_format (str): Force input format ('json' or 'txt'), or None to auto-detect
    """
    # Auto-detect format if not specified
    if input_format is None:
        input_format = detect_file_format(input_file)
    
    # Set default output file
    if output_file is None:
        input_path = Path(input_file)
        if input_format == 'txt':
            output_file = input_path.parent / f"{input_path.stem}_processed.txt"
        else:
            output_file = input_path.parent / f"{input_path.stem}.txt"
    
    print(f"Detected format: {input_format.upper()}")
    print(f"Converting {input_file} -> {output_file}")
    print()
    
    # Handle based on input format
    if input_format == 'txt':
        convert_txt_to_txt_file(input_file, output_file)
    elif input_format == 'json':
        convert_json_to_txt_file(input_file, output_file)
    else:
        print(f"Error: Unsupported format '{input_format}'")
        sys.exit(1)

def convert_json_to_txt_file(input_file, output_file):
    """
    Convert a JSON file to a readable text file.
    
    Args:
        input_file (str): Path to the input JSON file
        output_file (str): Path to the output text file
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read().strip()
        
        output_lines = [
            "GitHub Pull Request Bodies",
            "=" * 50,
            "",
            "This file contains the body text from various GitHub pull requests, formatted for readability.",
            ""
        ]
        
        # Parse line-separated JSON strings
        lines = content.split('\n')
        valid_lines = [line.strip() for line in lines if line.strip()]
        
        for i, line in enumerate(valid_lines):
            try:
                json_obj = json.loads(line)
                
                output_lines.append(f"[{i + 1}] " + "─" * 70)
                
                if isinstance(json_obj, str):
                    # Decode escape characters and format the string nicely
                    decoded_text = json_obj.encode().decode('unicode_escape')
                    output_lines.append(decoded_text)
                else:
                    output_lines.append(json.dumps(json_obj, indent=2, ensure_ascii=False))
                
                output_lines.append("")
                
            except json.JSONDecodeError as e:
                output_lines.append(f"[{i + 1}] ─── INVALID JSON ───")
                output_lines.append(f"Error: {e}")
                output_lines.append(f"Raw content: {line[:100]}...")
                output_lines.append("")
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(output_lines))
        
        print(f"Successfully converted JSON to TXT")
        print(f"Processed {len(valid_lines)} PR body entries")
        
    except Exception as e:
        print(f"Error during JSON conversion: {e}")
        sys.exit(1)

def pretty_print_file(file_path):
    """
    Pretty print a file, auto-detecting the format.
    
    Args:
        file_path (str): Path to the file
    """
    file_format = detect_file_format(file_path)
    
    if file_format == 'json':
        pretty_print_json_file(file_path)
    elif file_format == 'txt':
        pretty_print_txt_file(file_path)
    else:
        print(f"Error: Unsupported file format '{file_format}'")
        sys.exit(1)

def main():
    """Main function to handle command line arguments and run the converter."""
    
    # Default files in the same directory as this script
    script_dir = Path(__file__).parent
    default_json_file = script_dir / "body.json"
    default_txt_file = script_dir / "body.txt"
    
    # Try to find a default file
    if default_txt_file.exists():
        default_file = default_txt_file
    elif default_json_file.exists():
        default_file = default_json_file
    else:
        default_file = default_json_file  # fallback
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print("GitHub PR Body Formatter")
            print("=" * 30)
            print()
            print("This tool can handle both JSON and TXT input formats:")
            print("  • JSON: Line-separated JSON strings or proper JSON arrays")
            print("  • TXT:  Already formatted PR bodies (like body.txt)")
            print()
            print("Usage:")
            print(f"  python {Path(__file__).name}")
            print(f"  python {Path(__file__).name} <input_file> [output_file]")
            print(f"  python {Path(__file__).name} --convert [input_file]")
            print(f"  python {Path(__file__).name} --format json|txt <input_file>")
            print()
            print("Options:")
            print("  --convert        Convert to .txt file instead of printing to console")
            print("  --format FORMAT  Force input format (json|txt) instead of auto-detecting")
            print("  -h, --help       Show this help message")
            print()
            print("Examples:")
            print(f"  python {Path(__file__).name} body.json")
            print(f"  python {Path(__file__).name} body.txt")
            print(f"  python {Path(__file__).name} --convert body.json")
            print(f"  python {Path(__file__).name} --format txt my_file.dat")
            print(f"  python {Path(__file__).name} input.json output.txt")
            return
        elif sys.argv[1] == '--convert':
            # Handle --convert with optional file argument
            file_path = sys.argv[2] if len(sys.argv) > 2 else str(default_file)
            convert_to_txt_file(file_path)
            return
        elif sys.argv[1] == '--format':
            # Handle --format option
            if len(sys.argv) < 4:
                print("Error: --format requires format type and input file")
                print("Usage: python pretty_print_body.py --format json|txt <input_file>")
                sys.exit(1)
            format_type = sys.argv[2].lower()
            if format_type not in ['json', 'txt']:
                print("Error: Format must be 'json' or 'txt'")
                sys.exit(1)
            file_path = sys.argv[3]
            output_file = sys.argv[4] if len(sys.argv) > 4 else None
            
            if output_file:
                convert_to_txt_file(file_path, output_file, format_type)
            else:
                if format_type == 'json':
                    pretty_print_json_file(file_path)
                else:
                    pretty_print_txt_file(file_path)
            return
        else:
            file_path = sys.argv[1]
    else:
        file_path = str(default_file)
    
    # Check if output file is specified
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Verify input file exists
    if not Path(file_path).exists():
        print(f"Error: File '{file_path}' does not exist.")
        print()
        print("Available files in current directory:")
        script_dir = Path(file_path).parent
        for ext in ['*.json', '*.txt']:
            files = list(script_dir.glob(ext))
            if files:
                for f in files:
                    print(f"  • {f.name}")
        print()
        print("Usage:")
        print(f"  python {Path(__file__).name} <input_file> [output_file]")
        print(f"  python {Path(__file__).name} --convert [input_file]")
        print(f"  python {Path(__file__).name} --help")
        sys.exit(1)
    
    # If output file is specified, convert to txt
    if output_file:
        convert_to_txt_file(file_path, output_file)
    else:
        # Otherwise, print to console (auto-detect format)
        pretty_print_file(file_path)

if __name__ == "__main__":
    main()