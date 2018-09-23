import sys

SEPARATOR = ':'


def first_field(line):
    return line.split(SEPARATOR)[0]


files = sys.argv[1:]
for filename in files:
    with open(filename) as f:
        for line in sorted(f, key=first_field, reverse=True):
            print(line, end='')
