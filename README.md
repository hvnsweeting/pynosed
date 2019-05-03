# PyNoSed

Just enough Python 3.4+ for Sysadmin.

Given normal sysadmin jobs, which daily requires using:

- cat
- cut
- grep
- uniq
- sort
- head
- tail
- sed
- awk
- tr
- find
- glue all these with bash, some loop, some if/else conditions

Did I miss something?

Those are all de-factor/beloved/popular text manipulate tools that every
sysadmin must proficient with.

But writing python script which calls these tools are just
- creates unnecessary subprocess - which costs more resources
- less-portable, depends on these tools' version/feature. One runs on Linux
  might not run on your colleague shiny MacBook and it gets worse when need
  to run on Windows, too..
- un-pythonic - it makes you not look like really know some Python

So, let's write all those in Python. It's put aside what you already learned
and used for years on CLI, but I promise, that is simpler than the back time
you learnt those UNIX tools.

NOTE: **this tutorial does not target to "reinvent" UNIX tools, or replacing
those tools for daily usage, but as a guide
to archive their features as part of your bigger python application.**

## cat

`cat` a file most of the time is just to have it as input of other command,
and that most of the time is not **right** way to do it.

```sh
$ cat /etc/passwd | grep root
root:x:0:0:root:/root:/bin/bash
```

`cat` is unnecessary as `grep` (and most UNIX commands) accepts files as input

```sh
$ grep root /etc/passwd
root:x:0:0:root:/root:/bin/bash
```

In Python, to `cat` is to open a file, then iterate over lines and print out.

```python
import sys

# sys.argv is same as $@ in bash, sys.argv[1:] is list of passed args
for filename in sys.argv[1:]:
    with open(filename) as f:
        for line in f:
            # end='' to not auto-add newline to output. A file already has newline at the end of each line.
            print(line, end='')
```

Run it

```python
$ python3 cat.py /etc/passwd | grep root
root:x:0:0:root:/root:/bin/bash
```

## grep

`grep` is most common used tool for searching text in files, it has many
options, so clone all `grep` in Python is not trivial task. But just to search
lines that contain a string/pattern is simple.


```sh
$ grep -n root /etc/passwd
1:root:x:0:0:root:/root:/bin/bash
```

```python
import sys

pattern = sys.argv[1]
files = sys.argv[2:]

for filename in files:
    with open(filename) as f:
        for count, line in enumerate(f, start=1):
            if pattern in line:
                print(count, line, end='')
```

The output is almost same:

```sh
$ python3 grep.py root /etc/passwd
1 root:x:0:0:root:/root:/bin/bash
```

## Read from stdin
Most UNIX commands supports read from stdin, and with `bash` pipe `|`, it can
use output of other commands as its input, thus, make a super powerful way to
process text.

```sh
$ cat /etc/passwd | grep root
root:x:0:0:root:/root:/bin/bash
```

```python
# grepstdin.py
import sys

pattern = sys.argv[1]
for line in sys.stdin:
    if pattern in line:
        print(line, end='')
```

Run it:

```sh
$ cat /etc/passwd | python grepstdin.py root
root:x:0:0:root:/root:/bin/bash
```

### Regex - Regular Expression
The reason `grep` is called `grep` because it is **g/re/p** (globally search
a regular expression and print).

You can skip this subsection if you don't know what regex is and come back
later, maybe.

Using `-E` to tell `grep` you would input a regular expression pattern, and
`-o` to display only what matched (not whole line), let's show IPs:

```sh
$ ifconfig | grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}' -o
127.0.0.1
255.0.0.0
10.192.122.2
10.192.122.2
255.255.255.255
10.246.114.252
10.246.115.255
255.255.252.0
```

Python has more powerful `regex` (PCRE) support using standard `re` library.

`grep` regular expression is less powerful than Python - see `man 1 grep`:

> grep understands three different versions of regular expression syntax: “basic” (BRE), “extended” (ERE) and “perl” (PCRE). In GNU grep, there is no difference in available functionality between basic and extended syntaxes. In other implementations, basic regular expressions are less powerful. The following description applies to extended regular expressions; differences for basic regular expressions are summarized afterwards. Perl-compatible regular expressions give additional functionality, and are documented in pcresyntax(3) and pcrepattern(3), but work only if PCRE is available in the system.

```python
# grepregex.py
import re
import sys

for line in sys.stdin:
    # r'pattern' is raw-string, used when writing a regex
    for matched in re.finditer(r'([0-9]{1,3}\.){3}[0-9]{1,3}', line):
        print(matched.group())
```

Output:

```sh
$ ifconfig | python grepregex.py
127.0.0.1
255.0.0.0
10.192.122.2
10.192.122.2
255.255.255.255
192.168.1.117
192.168.1.255
255.255.255.0
```

A big note: though using regular expression works here, it has flaws:
- this looks for number.number.number.number - so passing
`999.999.999.999` still match, even it is not a valid IPv4.
- regex is hard to understand/write/debug.

Using `re` library can help replacing almost every UNIX tool that mainly work with regex:

- grep - to find a pattern
- sed - to replace a pattern
- awk - to find, process and replace a pattern (it actually is a programming language, but general usage is that).

## uniq
uniq - report or omit repeated lines, which can easily do in Python:

```sh
$ echo """abc
> abc
> abc
> def
> gh
> ghk
> abc""" | uniq
abc
def
gh
ghk
abc
```

The duplicated continued lines "abc" is removed.

```python
import sys

last_line = None
for line in sys.stdin:
    if line != last_line:
        print(line, end='')
    last_line = line
```

One common option used is `-c` to count number of occurrences. To implement in
Python by iterating each line and count could be tricky (do try it), but
using standard library `itertools` makes thing trivial:

```python
import itertools
import sys

for line, group in itertools.groupby(sys.stdin):
    dup_count = 0
    for _ in group:
        dup_count = dup_count + 1
    print(dup_count, line, end="")
```

The counting part not using `len` to avoid creating an auxiliary list, thus
saving memory.

## sort
sort helps sorting lines using numerical or lexical order.

```sh
$ sort -n -t: -k3 /etc/passwd | head -3
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
```

show users info ordered by 3rd column (UID number). Or sort by names (column
1):

```sh
$ sort -t1 -r /etc/passwd | head -3
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
whoopsie:x:109:116::/nonexistent:/bin/false
uuidd:x:107:111::/run/uuidd:/bin/false
```

```python
import sys

SEPARATOR = ':'


def first_field(line):
    return line.split(SEPARATOR)[0]

files = sys.argv[1:]

for filename in files:
    with open(filename) as f:
        for line in sorted(f, key=first_field, reverse=True):
            print(line, end='')
```


```sh
$ python sort.py /etc/passwd | head -3
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
whoopsie:x:109:116::/nonexistent:/bin/false
uuidd:x:107:111::/run/uuidd:/bin/false
```

## TODO
- head
- tail
- sed
- awk
- tr
- find
- argparse
- requests & JSON
