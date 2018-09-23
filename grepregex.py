import re
import sys


for line in sys.stdin:
    for matched in re.finditer(r'([0-9]{1,3}\.){3}[0-9]{1,3}', line):
        print(matched.group())
