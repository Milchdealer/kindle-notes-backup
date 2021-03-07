"""
	Automatically backup Kindle notes to Joplin
"""
import argparse
import shutil
from datetime import datetime

import requests

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup Kindle Notes")
    parser.add_argument(
        "-f", "--clipping-file", type=str, help="Location of the kindle notes"
    )
    parser.add_argument(
        "-d",
        "--backup-destination",
        type=str,
        help="Where to copy over the notes for backup",
    )
    parser.add_argument(
        "-t", "--joplin-token", type=str, help="Jopling API token"
    )
    parser.add_argument(
        "-n",
        "--joplin-note-id",
        type=str,
        help="Jopling note Id to write the content into",
    )
    parser.add_argument(
        "-p",
        "--joplin-notebook-parent-id",
        type=str,
        help="Identifier of the notebook, in case a new note should be created"
        ", then it will be put here",
    )

    args = parser.parse_args()

    print(
        f"Copying over file from '{args.clipping_file}' to "
        f"'{args.backup_destination}'"
    )
    shutil.copy(args.clipping_file, args.backup_destination)

    print("Sending contents of file to Joplin")
    params = {"token": args.joplin_token}
    parent_id = (
        args.joplin_notebook_parent_id
        if args.joplin_notebook_parent_id
        else None
    )
    title = "Kindle Notes: %s" % datetime.now().isoformat()
    with open(args.backup_destination) as f:
        data = {
            "title": title,
            "parent_id": parent_id,
            "body": f.read(),
        }
    if args.joplin_note_id:
        print("Updating existing note '%s'" % args.joplin_note_id)
        res = requests.put(
            f"http://127.0.0.1:41184/notes/{args.joplin_note_id}",
            json=data,
            params=params,
        )
    else:
        print("Creating new note '%s'" % title)
        res = requests.post(
            "http://127.0.0.1:41184/notes", json=data, params=params
        )
    print(res.status_code)
