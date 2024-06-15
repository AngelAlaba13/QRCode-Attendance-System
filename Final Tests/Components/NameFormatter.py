import re

string = "Name: Angel Kyle L. Alaba Year and Block: 2CSE"

name_pattern = r'Name:\s*(.*?)\s*Year\s*and\s*Block:'
year_block_pattern = r'Year\s*and\s*Block:\s*(\d+)[A-Za-z]*([A-Za-z])$' 

name_match = re.search(name_pattern, string)
if name_match:
    name = name_match.group(1).strip()

year, block = None, None
year_block_match = re.search(year_block_pattern, string)
if year_block_match:
    year = year_block_match.group(1)
    block = year_block_match.group(2)
        
print("Name:", name)
print("Year:", year)
print("Block:", block)