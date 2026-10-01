#!/usr/bin/env python3
"""
Batch File Renamer
A simple command-line utility to batch rename files with prefixes, suffixes,
text replacement, and a safe dry-run preview mode.
"""

import argparse
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Batch rename files in a specified directory."
    )
    parser.add_argument(
        "directory", type=str, help="Path to the target directory containing files"
    )
    parser.add_argument(
        "-p", "--prefix", type=str, default="", help="Add a prefix to filenames"
    )
    parser.add_argument(
        "-s", "--suffix", type=str, default="", help="Add a suffix to filenames (before extension)"
    )
    parser.add_argument(
        "-f", "--find", type=str, default="", help="Text to search for and replace"
    )
    parser.add_argument(
        "-r", "--replace", type=str, default="", help="Replacement text"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without actually renaming files",
    )
    return parser.parse_args()


def rename_files(args):
    target_dir = Path(args.directory)

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Error: Directory '{target_dir}' does not exist or is not a valid folder.")
        return

    files = [f for f in target_dir.iterdir() if f.is_file()]

    if not files:
        print(f"No files found in '{target_dir}'.")
        return

    print(f"\nProcessing {len(files)} file(s) in '{target_dir}':\n" + "-" * 40)

    renamed_count = 0
    for file_path in files:
        original_name = file_path.name
        stem = file_path.stem
        suffix = file_path.suffix

        # Apply text replacement if requested
        if args.find:
            stem = stem.replace(args.find, args.replace)

        # Apply prefix and suffix
        new_stem = f"{args.prefix}{stem}{args.suffix}"
        new_name = f"{new_stem}{suffix}"

        if original_name == new_name:
            continue

        new_path = file_path.with_name(new_name)

        print(f"Original: {original_name}  -->  New: {new_name}")

        if not args.dry_run:
            file_path.rename(new_path)
        
        renamed_count += 1

    print("-" * 40)
    if args.dry_run:
        print(f"Dry run complete. {renamed_count} file(s) would be renamed.")
    else:
        print(f"Successfully renamed {renamed_count} file(s).")


def main():
    args = parse_arguments()
    rename_files(args)


if __name__ == "__main__":
    main()
