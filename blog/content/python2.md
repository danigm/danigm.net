Date: 2025-01-27 12:00
Title: Python 2
Tags: gnome, work, suse, opensuse
Category: blog
Slug: python2
Gravatar: 7ce0b0e40deeb4f549d2a04b3c5ea3cc

<center>
    <img src="/pictures/python2.png" width="100%"/>
</center>

In 2020, the
[Python foundation declared Python 2 as not maintained anymore][1].

Python 2 is really old, not maintained and should not be used by
anyone in any modern environment, but software is complex and python2
still exists in some modern Linux distributions like Tumbleweed.

The past week the [request to delete Python 2][2] from Tumbleweed was
created and is going through the staging process.

The main package keeping Python 2 around for Tumbleweed was Gimp 2,
that doesn't depends directly on Python 2, but some of the plugins
depends on it. Now that we've Gimp 3 in Tumbleweed, we are able to
finally remove it.

## Python 2

The first version of Python 2 was released around 2000, so it's now 25
years old. That's not true, because software is a living creature, so
as you may know, Python 2 grew during the following years with patch
and minor releases until 2020 that was the final release 2.7.18.

But even when it was maintained until 2020, it was deprecated for a
long time so everyone "should" have time to migrate to python 3.

## Py3K

I started to write python code around the year 2006. I was bored
during a summer internship at my third year of computer science, and I
decided to learn something new. In the following months / years I
heard a lot about the futurist [Python 3000][3], but I didn't worry to
much until it was officially released and the [migration][4] started to be
a thing.

If you have ever write python2 code you will know about some of the
main differences with python3:

 * print vs print()
 * raw_input() vs input()
 * unicode() vs str
 * ...

Some tools appeared to make it easier to migrate from python2 to
python3, and even it was possible to have code compatible with both
versions at the same time using the `__future__` module.

You should have heard about the [six][5] package, 2 * 3 = 6. Maybe the
name should be five instead of six, because it was a Python "2 and 3"
compatibility library.

## Python in Linux command line

When python3 started to be the main python, there were some discussion
about how to handle that in different Linux distributions. The
/usr/bin/python binary was present and everyone expect that to be
python2, so almost everyone decided to keep that relation forever and
distribute python3 as /usr/bin/python3, so you can have both installed
without conflicts and there's no confusion.

But python is an interpreted language, and if you have python code,
you can't tell if it's python2 or python3. The shebang line in the
executable python scripts should point to the correct interpreter and
that should be enough like `#!/usr/bin/python3` will use the python3
interpreter and `#!/usr/bin/python` will use python2.

But this is not always true, some distributions uses python3 in
`/usr/bin/python` like Archlinux or if you create a virtualenv with
python3, the `python` binary points to the python3 interpreter, so a
shebang like `#!/usr/bin/python` could be something valid for a
python3 script.

In any case, the recommended and safest way is to always use `python3`
binary because that way it'll work correctly "everywhere".

## Goodbye

It's time to say goodbye to `python2`, at least we can remove it now
from Tumbleweed. It'll be around for some more time in Leap, but it's
the time to let it go.

[1]: https://www.python.org/doc/sunset-python-2/
[2]: https://build.opensuse.org/request/show/1240106
[3]: https://peps.python.org/pep-3000/
[4]: https://docs.python.org/3.10/library/2to3.html
[5]: https://pypi.org/project/six/
