import sys

pattern = sys.argv[1]
for line in sys.stdin:
    if pattern in line:
        print(line, end='')
