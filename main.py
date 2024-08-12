#!/usr/bin/env python3
"""
Converts a Writeaday all-entries.txt to a CSV file, using Daylio's CSV format.
"""

__author__ = "Giuseppe Boccia"
__version__ = "0.1.0"
__license__ = "MIT"


import argparse
import csv
import os
import re
from datetime import datetime


def main(args):
    """ Main entry point of the script """
    check_files(args.input_file, args.output_file)
    print(f"Converting {args.input_file} to {args.output_file}...")

    entries_written = parse_writeaday_txt_to_csv(args.input_file, args.output_file)
    print(f"Done! {entries_written} entries written.")


def check_files(path_in: str, path_out: str) -> None:
    """
    Ensures that input file exists and can be read, and output file can be written
    """
    # Check that input file exists and can be read
    if not os.path.exists(path_in):
        raise FileNotFoundError(f"File not found: \"{path_in}\"")
    if not os.path.isfile(path_in):
        raise IsADirectoryError(f"\"{path_in}\" is not a file")
    if not os.access(path_in, os.R_OK):
        raise PermissionError(f"No read permission for \"{path_in}\"")

    # Check that output file can be written
    if os.path.exists(path_out):
        if not os.path.isfile(path_out):
            raise IsADirectoryError(f"\"{path_out}\" is not a file")
        if not os.access(path_out, os.W_OK):
            raise PermissionError(f"No write permission for \"{path_out}\"")
    else:
        if not os.access(os.path.dirname(path_out), os.W_OK):
            raise PermissionError(f"No write permission for \"{path_out}\"")


def parse_writeaday_txt_to_csv(path_in: str, path_out: str) -> None:
    """
    Reads the input file line by line and converts each Writeaday entry to a CSV line, using Daylio's CSV format.
    In particular:
    - new lines are replaced with <br>
    - date format is converted from MM-DD-YYYY to YYYY-MM-DD
    - time format is converted from AM/PM to 24h
    - double-quote character is replaced with two double-quotes
    """
    entry_count = 0
    with open(path_in, "r", encoding="UTF-8") as file_in, open(path_out, "w", newline="", encoding="UTF-8") as file_out:
        csv_writer = csv.writer(file_out, quoting=csv.QUOTE_MINIMAL)

        # Write header
        csv_writer.writerow(["full_date", "date", "weekday", "time", "mood", "activities", "note_title", "note"])

        current_date = None
        current_time = None
        current_note = None

        for line in file_in:
            line = line.strip()

            if not line:
                # Empty line: write the current entry, then reset time and note variables
                entry_count += write_entry(csv_writer, current_date, current_time, current_note)
                current_time = None
                current_note = None

            elif is_date_line(line):
                # New date: write the current entry, then update the date and reset time and note variables
                entry_count += write_entry(csv_writer, current_date, current_time, current_note)
                current_date = datetime.strptime(line, "%m-%d-%Y")
                current_time = None
                current_note = None

            elif is_time_line(line):
                # New time+entry: write the current entry, then start a new one
                entry_count += write_entry(csv_writer, current_date, current_time, current_note)
                current_time, current_note = parse_time_and_note(line)

            else:
                # Continuation of the current note
                if current_note:
                    current_note += f"<br>{line}"
                else:
                    # This shouldn't happen in a well-formatted file, but just in case:
                    current_note = line

        # Write the last entry
        entry_count += write_entry(csv_writer, current_date, current_time, current_note)
        
    return entry_count


def is_date_line(line: str) -> bool:
    """ Returns True if the given line is a date in the format MM-DD-YYYY """
    date_pattern = r'^\d{2}-\d{2}-\d{4}$'       # Es: 01-01-2024
    return bool(re.match(date_pattern, line))


def is_time_line(line: str) -> bool:
    """ Returns True if the given line starts with a time such as [1:23 PM] """
    time_pattern = r'^\[\d{1,2}:\d{2}\s*[AP][M]\]'    # Es: [1:23 PM] this is a note...
    return bool(re.match(time_pattern, line))


def parse_time_and_note(line: str) -> tuple:
    time_str, *note_parts = line[1:].split('] ')
    time = datetime.strptime(time_str, "%I:%M %p")
    note = '] '.join(note_parts) if note_parts else ""
    return time, note


def write_entry(csv_writer: csv.writer, date: datetime, time: datetime, note: str) -> None:
    """ 
    Writes a single entry to the CSV file if all given fields are present. Otherwise, does nothing.
    Returns 1 if an entry was written, 0 otherwise.
    """
    if date and time and note:
        full_date = date.strftime("%Y-%m-%d")   # Es: 2024-08-12
        date_str = date.strftime("%B %d")       # Es: January 01
        weekday = date.strftime("%A")           # Es: Monday
        time_str = time.strftime("%H:%M")       # Es: 14:30
        csv_writer.writerow([full_date, date_str, weekday, time_str, "", "", "", note])
        return 1

    return 0


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(
        description="Converts a Writeaday all-entries.txt file to a CSV file, using Daylio's CSV format.")

    parser.add_argument("input_file", help="Input .txt file to be converted")
    parser.add_argument("output_file", help="Output .csv file")

    args = parser.parse_args()
    main(args)
