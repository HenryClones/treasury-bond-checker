import random
import requests
import dotenv
import os
import sys
from bs4 import BeautifulSoup
from lxml import etree
import scrapehelpers
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
    header = headers()
    page = initial_page(FORM_URL, headers)
    dom = get_dom(page)
    hiddens = form_hiddens(dom, HIDDENS_FORM_XPATH)
    rand = random.Random()
    for bond in bonds:
        sleep(rand.uniform(1, 3))
        page = check_bond(bond_request_data(bond, hiddens))
        dom = get_dom(page)
        hiddens = form_hiddens(dom, HIDDENS_FORM_XPATH)
        yield top_entry(dom, TABLE_XPATH)

# Check bonds from stdin
def check_bonds_from_stdin():
    reader, fieldnames = clean_read()
    writer = clean_write(sys.stdout, fieldnames)
    for bond in use_form(reader):
        writer(bond)

if __name__ == "__main__":
    check_bonds_from_stdin()
