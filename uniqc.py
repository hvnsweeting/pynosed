import itertools
import sys

for line, group in itertools.groupby(sys.stdin):
    dup_count = 0
    for _ in group:
        dup_count = dup_count + 1
    print(dup_count, line, end="")
