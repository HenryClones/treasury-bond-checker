#!/bin/python3

import sys
import random
import scrapehelpers as sh
import time
from cleaner import clean_read, clean_write

# The form URL to submit to
FORM_URL = 'https://www.treasurydirect.gov/BC/SBCPrice'
# The URL listed under the form's action property, may differ
ACTION_URL = 'https://www.treasurydirect.gov/BC/SBCPrice'
# The XPath of the form's hidden inputs
HIDDENS_FORM_XPATH = '//*[@id="content"]/form/fieldset'
# The XPath of a table on the page
TABLE_XPATH = '//*[@id="content"]/form/table'

# Generator to use the form
def use_form(bonds):
    session = sh.FormViewer()
    page = session.initial_page(FORM_URL)
    dom = sh.get_dom(page)
    hiddens = sh.form_hiddens(dom, HIDDENS_FORM_XPATH)
    rand = random.Random()
    for bond in bonds:
        time.sleep(rand.uniform(1, 3))
        page = session.check_bond(ACTION_URL,
            sh.bond_request_data(bond, hiddens))
        dom = sh.get_dom(page)
        hiddens = sh.form_hiddens(dom, HIDDENS_FORM_XPATH)
        yield sh.top_entry(dom, TABLE_XPATH)

# Check bonds from stdin
def check_bonds_from_stdin():
    reader, _ = clean_read()
    writer = clean_write(sys.stdout)
    for bond in use_form(reader()):
        writer(bond)

if __name__ == "__main__":
    check_bonds_from_stdin()
