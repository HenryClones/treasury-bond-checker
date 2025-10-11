#!/bin/python3

from bs4 import BeautifulSoup
from lxml import html
import requests
import dotenv
import os

class FormViewer:

    # Set headers
    def headers(self, base_object):
        if (hasattr(base_object, 'get') and
            callable(getattr(base_object, 'get')) and
            base_object.get('User-Agent')):
            return base_object
        elif not (hasattr(base_object, 'get') and
            callable(getattr(base_object, 'get'))):
            base_object = {}
        
        dotenv.load_dotenv(override=False)
        user_agent = os.environ.get('USER_AGENT')
        base_object |= {'User-Agent': user_agent}
        headers = base_object | {'Content-Type': 'application/x-www-form-urlencoded'}
        return headers
    
    def add_referer(self):
        self.headers |= {'Referer': self.referer}

    # Safely get the bond data with hiddens from a web form
    def check_bond(self, url, request_data):
        self.add_referer()
        output = self.session.post(url, headers=self.headers, data=request_data)
        self.referer = url
        return output.content

    # Get initial page, which is added to by forms
    def initial_page(self, url):
        self.add_referer()
        form = self.session.get(url, headers=self.headers)
        self.referer = url
        return form.content
    
    # Create a session
    def __init__(self, header=None):
        self.session = requests.Session()
        self.headers = self.headers(header)
        self.referer = ''

# Get the DOM of a page
def get_dom(page):
    soup = BeautifulSoup(page, 'html.parser')
    dom = html.fromstring(str(soup))
    return dom

# Generate the request data for a bond
def bond_request_data(bond_data, hiddens):
    request_data = bond_data | hiddens
    return request_data

# Get form hiddens at a specified XPath
def form_hiddens(dom, xpath):
    hiddens = dom.xpath(xpath)[0]
    return {hidden.get('name'): hidden.get('value') or ''
        for hidden in hiddens
        if hidden.get('type') == 'hidden' and hidden.get('name')}

# Get the columns of a table
def table_columns(dom, xpath):
    COLUMN_LOCATION = '/thead/tr/th'
    table_head = dom.xpath(xpath + COLUMN_LOCATION)
    return [column.text_content() for column in table_head if
        len(column.text_content().strip())]

# Get the row of a table at a specified XPath
def table_row(dom, xpath, index=1):
    TROW_LOCATION = f"/tbody/tr[{index}]"
    table_body = dom.xpath(xpath + TROW_LOCATION)[0]
    return [cell.text_content() for cell in table_body]

# Get top entry from a table as a dictionary
def top_entry(dom, xpath):
    return {column: cell for column, cell in
        zip(table_columns(dom, xpath),
        table_row(dom, xpath))}
