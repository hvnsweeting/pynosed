import sys

last_line = None
for line in sys.stdin:
    if line != last_line:
        print(line, end='')
    last_line = line
