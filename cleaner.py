#!/bin/python3

import csv
import sys
import io
import re

# Get the fieldname for a particular column, based on first line
def fieldname(label):
    if re.search(r'^[A-Z][0-9]+(EE|E|I|SN)?$', label):
        return 'SerialNumber'
    elif re.search(r'^\$?([27]5|10{1,4}|50{1,3}|200)$', label):
        return 'Denomination'
    elif re.search(r'^(EE|E|I|SN)$', label):
        return 'Series'
    elif re.search(r'^[0-9]{2}/[0-9]{4}$', label):
        return 'IssueDate'
    else:
        return False

# Get the field names for the first line
def get_fieldnames(line):
    # Generate fieldnames for each column
    fieldnames = [fieldname(field) for field in line]
    # Trust the user if there are >4 columns or header names
    if len(fieldnames) > 4 or not all(fieldnames):
        return line, False
    else:
        return fieldnames, True

# Read a line of CSV in a way proofed against the first line
def clean_read():
    header_line = sys.stdin.readline()
    if not header_line:
        return
    header_reader = csv.reader(io.StringIO(header_line))
    first_line = next(header_reader)
    if len(first_line) < 4:
        raise IndexError('Requires a series, denomination, issue date, and serial number')
    fieldnames, no_header = get_fieldnames(first_line)
    def callback():
        if no_header:
            yield {key: value for key, value in zip(fieldnames, first_line)}
        yield from csv.DictReader(sys.stdin, fieldnames)
    return callback, fieldnames

def clean_write(f):
    writer = None
    def callback(obj):
        nonlocal writer
        if not writer:
            fieldnames = obj.keys()
            writer = csv.DictWriter(f, fieldnames)
        writer.writerow(obj)
    return callback
