"""
	Automatically parse Kindle notes markdown.
"""
import argparse
import shutil
import hashlib
from os import path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup Kindle Notes")
    parser.add_argument(
        "-f",
        "--clipping-file",
        type=str,
        help="Location of the kindle notes",
        required=True,
    )
    parser.add_argument(
        "-d",
        "--destination",
        type=str,
        required=True,
        help="Where to copy over the notes",
    )
    args = parser.parse_args()

    if not path.isdir(args.destination):
        print(f"'{args.destination}' does not exist")
        exit(1)
    print(f"Parsing notes from {args.clipping_file} to {args.destination}")
    with open(args.clipping_file) as f:
        notes = f.read()

    notes = notes.split("==========")
    print("Found %d notes" % len(notes))
    for note in notes:
        m = hashlib.md5()
        m.update(bytes(note, "utf-8"))
        file_name = f"{m.hexdigest()}.md"
        file_path = path.join(args.destination, file_name)

        if "<You have reached the clipping limit for this item>" in note:
            print("Note is incomplete, skipping")
            continue

        if path.exists(file_path):
            print(f"Path already exists, skipping '{file_path}'")
        else:
            print(f"Writing content to '{file_path}'")
            with open(file_path, "w") as out_f:
                out_f.write(note)
