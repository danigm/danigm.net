Date: 2024-05-22
Title: Python 3.13 Beta 1
Tags: gnome, work, suse, linux, python
Category: blog
Slug: python313-beta1
Gravatar: 8da96af78e0089d6d970bf3760b0e724

<img src="/pictures/python-logo-master-v313-TM.png" width="100%" />

Python [3.13 beta 1 is out][1], and I've been working on the openSUSE
Tumbleweed package to get it ready for the release.

## Installing python 3.13 beta 1 in Tumbleweed

If you are adventurous enough to want to test the python 3.13 and you
are using openSUSE Tumbleweed, you can give it a try and install the
current devel package:

```sh
# zypper addrepo -p 1000 https://download.opensuse.org/repositories/devel:languages:python:Factory/openSUSE_Tumbleweed/devel:languages:python:Factory.repo
# zypper refresh
# zypper install python313
```

## What's new in Python 3.13

Python interpreter is pretty stable nowadays and it doesn't change too
much to keep code compatible between versions, so if you are writing
modern Python, your code should continue working whit this new
version. But it's actively developed and new versions have cool new
functionalities.

1. [New and improved interactive interpreter][3], colorized prompts,
   multiline editing with history preservation, interactive help with
   `F1`, history browsing with `F2`, paste mode with `F3`.
1. A set of performance improvements.
1. Removal of many deprecated modules: aifc, audioop, chunk, cgi,
   cgitb, crypt, imghdr, mailcap, msilib, nis, nntplib, ossaudiodev,
   pipes, sndhdr, spwd, sunau, telnetlib, uu, xdrlib, lib2to3.

## Enabling Experimental JIT Compiler

The python 3.13 version will arrive with an [experimental functionality][2]
to improve performance. We're building with the
`--enable-experimental-jit=yes-off` so it's disabled by default but it
can be enabled with a virtualenv before launching:

```
$ PYTHON_JIT=1 python3.13
```

## Free-threaded CPython

The python 3.13 has another build option to disable the Global
Interpreter Lock (`--disable-gil`), but we're not enabling it because
in this case it's not possible to keep the same behavior. Building
with `disabled-gil` will break compatibility.

In any case, maybe it's interesting to be able to provide another
version of the interpreter with the GIL disabled, for specific cases
where the performance is something critical, but that's something to
evaluate.

We can think about having a `python313-nogil` package, but it's not
something trivial to be able to have `python313` and `python313-nogil`
at the same time in the same system installation, so I'm not planning
to work on that for now.

[1]: https://www.python.org/downloads/release/python-3130b1/
[2]: https://docs.python.org/3.13/whatsnew/3.13.html#experimental-jit-compiler
[3]: https://docs.python.org/3.13/whatsnew/3.13.html#a-better-interactive-interpreter
