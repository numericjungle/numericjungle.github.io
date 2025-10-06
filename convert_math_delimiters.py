#!/usr/bin/env python3
r"""
Jekyll Math Delimiter Converter

This script converts LaTeX delimiters in Markdown files:
- \( ... \) to $ ... $
- \[ ... \] to $$ ... $$

Usage: python convert_math_delimiters.py [directory]
  If no directory is specified, it processes the '_posts' directory
  Backups are stored in the '_drafts' directory
"""

import os
import sys
import re
import shutil
from pathlib import Path


def convert_square_bracket_blocks(content):
    """Convert bracket-wrapped display math into $$ blocks."""
    pattern = re.compile(r'\n[ \t]*\[\n(.*?)[ \t]*\n[ \t]*\]\n', re.DOTALL)
    changes = 0

    def _replace(match):
        nonlocal changes
        inner = match.group(1)
        if '\\' not in inner:
            return match.group(0)
        changes += 1
        stripped = inner.strip('\n')
        return '\n$$\n' + stripped + '\n$$\n'

    return pattern.sub(_replace, content), changes


def convert_inline_parentheses(content):
    """Wrap inline math like (\\mathcal{L}) with $...$ while keeping parentheses."""
    length = len(content)
    result = []
    changes = 0
    i = 0
    in_inline = False
    in_display = False

    while i < length:
        char = content[i]

        if char == '$' and (i == 0 or content[i - 1] != '\\'):
            if i + 1 < length and content[i + 1] == '$':
                in_display = not in_display
                result.append('$$')
                i += 2
                continue
            else:
                in_inline = not in_inline
                result.append('$')
                i += 1
                continue

        if char == '(' and not in_inline and not in_display:
            prev = content[i - 1] if i > 0 else '\n'
            if not (prev.isalnum() or prev in {'_', '$'}):
                depth = 1
                k = i + 1
                contains_newline = False

                while k < length and depth > 0:
                    current = content[k]
                    if current == '\n':
                        contains_newline = True
                    if current == '(':
                        depth += 1
                    elif current == ')':
                        depth -= 1
                    k += 1

                if depth == 0 and not contains_newline:
                    inner = content[i + 1:k - 1].strip()
                    if '$' not in inner and any(sym in inner for sym in ('\\', '_', '^')):
                        result.append('($' + inner + '$)')
                        i = k
                        changes += 1
                        continue

        result.append(char)
        i += 1

    return ''.join(result), changes

def convert_file(file_path, backup_dir):
    """Convert math delimiters in a single file and backup to specified dir"""
    if not file_path.suffix.lower() in ['.md', '.markdown']:
        return 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = 0

    # Convert bracket-based display math
    content, bracket_changes = convert_square_bracket_blocks(content)
    changes += bracket_changes

    # Convert \[ ... \] to $$ ... $$
    # Using a regex pattern that handles newlines and spaces
    pattern = re.compile(r'\\\[([\s\S]*?)\\\]')
    content, count1 = pattern.subn(r'$$\1$$', content)
    changes += count1
    
    # Convert \( ... \) to $ ... $
    pattern = re.compile(r'\\\(([\s\S]*?)\\\)')
    content, count2 = pattern.subn(r'$\1$', content)
    changes += count2

    # Convert inline parentheses-based math
    content, inline_changes = convert_inline_parentheses(content)
    changes += inline_changes

    # Only write the file if changes were made
    if content != original:
        print(f"Converting {file_path} ({changes} changes)")
        
        # Create backup of original file
        backup_path = os.path.join(backup_dir, file_path.name)
        
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        
        # Create backup
        shutil.copy2(file_path, backup_path)
        print(f"  Original backed up to {backup_path}")
        
        # Write the modified content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return changes
    
    return 0

def process_directory(directory, backup_dir):
    """Process all markdown files in a directory"""
    total_changes = 0
    total_files = 0
    
    for item in os.listdir(directory):
        file_path = Path(os.path.join(directory, item))
        
        # Skip hidden files
        if item.startswith('.'):
            continue
            
        # Process the file if it's a markdown file
        if file_path.is_file():
            changes = convert_file(file_path, backup_dir)
            if changes > 0:
                total_changes += changes
                total_files += 1
    
    return total_files, total_changes

def main():
    """Main entry point for the script"""
    # Default directories
    posts_dir = '_posts'
    drafts_dir = '_drafts'
    
    # Use command line argument if provided
    if len(sys.argv) > 1:
        posts_dir = sys.argv[1]
    
    # Check if posts directory exists
    if not os.path.isdir(posts_dir):
        print(f"Error: Directory '{posts_dir}' not found.")
        sys.exit(1)
    
    print(f"Converting math delimiters in '{posts_dir}'...")
    print(f"Backups will be stored in '{drafts_dir}'")
    
    files_changed, total_changes = process_directory(posts_dir, drafts_dir)
    
    print(f"Conversion complete! {files_changed} files changed with {total_changes} total delimiter conversions.")
    if files_changed > 0:
        print(f"Backups stored in '{drafts_dir}'")

if __name__ == "__main__":
    main()
