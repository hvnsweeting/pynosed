import sys

for filename in sys.argv[1:]:
    with open(filename) as f:
        for line in f:
            print(line, end='')
