#!/bin/python3

from bs4 import BeautifulSoup
from lxml import etree
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

    # Safely get the bond data with hiddens from a web form
    def check_bond(self, url, request_data):
        output = self.session.post(url, headers=self.headers, data=request_data)
        return output.content

    # Get initial page, which is added to by forms
    def initial_page(self, url):
        form = self.session.get(url, headers=self.headers)
        return form.content
    
    # Create a session
    def __init__(self, header=None):
        self.session = requests.Session()
        self.headers = self.headers(header)


# Get the DOM of a page
def get_dom(page):
    soup = BeautifulSoup(page, 'html.parser')
    dom = etree.HTML(str(soup))
    print(etree.tostring(dom, pretty_print=True))
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
    COLUMN_LOCATION = '/thead/tr'
    table_head = dom.xpath(xpath + COLUMN_LOCATION)[0]
    return [column.text for column in table_head]

# Get the row of a table at a specified XPath
def table_row(dom, index, xpath):
    TBODY_LOCATION = '/tbody/tr'
    table_body = dom.xpath(xpath)[0]
    print(etree.tostring(table_body, pretty_print=True))
    return [cell.text for cell in table_body[index]]

# Get top entry from a table as a dictionary
def top_entry(dom, xpath):
    return {column: cell for column, cell in
        zip(table_columns(dom, xpath),
        table_row(dom, 0, xpath))}
