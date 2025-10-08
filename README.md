# Treasury Bond Checker
## Usage
Takes treasury bond numbers as a CSV, and returns an output CSV in a similar shape with information from the U.S. Treasury. **Does not redeem bonds.**
## Instructions
1. Follow the instructions at the URL to get a U.S. Treasury Marketable Securities Experience API key: https://api-community.fiscal.treasury.gov/s/communityapi/a01Qo00000pDeK7IAK/enterprise-apisustreasurymarketablesecuritiesexperienceapi
2. Create a .env file
3. Write `API_KEY=` followed by your API key.
4. Run `python check_bond.py`. Indicate you are done entering with an EOF character, or use pipes for I/O.
