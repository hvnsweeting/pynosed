# PyNoSed

Just enough Python for Sysadmin.

Given normal sysadmin jobs, which daily requires using:

- grep
- head
- tail
- cat
- sed
- awk
- uniq
- tr
- cut
- find
- glue all these with bash, some loop, some if/else conditions

Did I miss something?

Those are all de-factor/beloved/popular text manipulate tools that every
sysadmin must proficient with.

But writing python script which calls these tools are just
- un-pythonic - it makes you not look like really know some Python
- create unnecessary subprocess - which cost more resources
- less-portable, depends on these tools version/feature. One run on Linux
might not run on your colleague shiny MacBook.

So let's write all those in Python. It's put aside what you already learned
and used for years on CLI, but I promiss, that is simpler than the back time
you learn those UNIX tools.
