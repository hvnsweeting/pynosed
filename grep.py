import sys

pattern = sys.argv[1]
files = sys.argv[2:]

for filename in files:
    with open(filename) as f:
        for count, line in enumerate(f, start=1):
            if pattern in line:
                print(count, line, end='')
