# Set headers
def headers(base_object=None):
    if (hasattr(base_object, 'get') and
        callable(getattr(base_object, 'get')) and
        base_object.get('User-Agent')):
        return base_object
    elif not (hasattr(base_object, 'get') and
        callable(getattr(base_object, 'get'))):
        base_object = {}
    
    dotenv.load_dotenv(override=False)
    user_agent = os.environ.get('USER_AGENT')
    headers = {'User-Agent': user_agent} if user_agent else None
    return headers

# Safely get the bond data with hiddens from a web form
def check_bond(request_data, headers=None):
    output = requests.post(ACTION_URL, headers=headers, data=request_data)
    return output

# Generate the request data for a bond
def bond_request_data(bond_data, hiddens):
    request_data = bond_data | hiddens
    return request_data

# Get initial page, which is added to by forms
def initial_page(url, headers=None):
    form = requests.get(url, headers=headers)
    return form

# Get the DOM of a page
def get_dom(page):
    soup = BeautifulSoup(page.text, 'html.parser')
    dom = etree.HTML(str(soup))
    return dom

# Get form hiddens at a specified XPath
def form_hiddens(dom, xpath):
    hiddens = dom.xpath(xpath)
    return {hidden.get('name'): hidden.get('value') or ''
        for hidden in hiddens
        if hidden.get('type') == 'hidden' and hidden.get('name')}

# Get the columns of a table
def table_columns(dom, xpath):
    COLUMN_LOCATION = '/thead/tr'
    table_head = dom.xpath(xpath + COLUMN_LOCATION)
    return [column.text for column in table_head]

# Get the row of a table at a specified XPath
def table_row(dom, index, xpath):
    TBODY_LOCATION = '/tbody'
    table_body = dom.xpath(xpath + TBODY_LOCATION)
    try:
        return [cell.text for cell in table[i]]
    except IndexError:
        return []

# Get top entry from a table as a dictionary
def top_entry(dom, xpath):
    return {column: cell for column, cell in
        zip(table_columns(dom, xpath),
        table_row(dom, 0, xpath))}
