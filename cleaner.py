import csv
import sys
import io
import re

# Get the fieldname for a particular column, based on first line
def fieldname(label):
    if re.search('^[A-Z][0-9]+(EE|E|I|SN)?$', label):
        return 'SerialNumber'
    elif re.search('^\$?(10|25|50|75|100|200|500|1000|5000|10000)$'):
        return 'Denomination'
    elif re.search('^(EE|E|I|SN)$'):
        return 'Series'
    elif re.search('^[0-9][0-9]/[0-9][0-9][0-9][0-9]$'):
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
            yield first_line
        yield from csv.DictReader(sys.stdin, fieldnames)
    return callback, fieldnames

def clean_write(f):
    return csv.DictWriter(f)
