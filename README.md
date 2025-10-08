# Treasury Bond Checker
## Usage
Takes treasury paper bond serial numbers as a CSV, and returns an output CSV in a similar shape with information from the U.S. Treasury. **Does not redeem bonds, and does not function if used with electronic bonds.**
## Instructions
1. Create a file named .env
2. Add the text `USER_AGENT=` followed by your User Agent---look up how to set it, or this program may be less stable.
3. Run `python check_bond.py`. Then, use one of the following input/output methods
    - Indicate you are done entering with an EOF character
    - Use pipes for I/O
