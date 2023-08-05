Date: 2023-08-05
Title: Python in openSUSE Tumbleweed
Tags: software, suse, tumbleweed, gnome
Slug: python-tw
Gravatar: 7ce0b0e40deeb4f549d2a04b3c5ea3cc
Category: blog

[openSUSE Tumbleweed][1] is a rolling release distribution, so it's
ideal for developers and users that like to have the bleeding edge
software.

It's also really "stable" to be a rolling release, from time
to time you can find a broken package because of one package is
updated and another one is not compatible yet, but it's something that
doesn't happen too often thanks to [openqa tests][4], so you don't
need to worry about a breaking system.

<p class="img">
  <img src="/pictures/python-tw.png" />
</p>

You can find the [Python interpreter][2] and a lot of [python modules][5]
in every Linux distribution, but Tumbleweed does an interesting thing
for Python.

## Default Python version (python3 -> python-3.11)

If you don't worry about the python version, you can just rely on
`python3`. In Tumbleweed `python3` is not a real package, but the
default python version provides `python3`, so depending on when you
install `python3` you will get a different package, if you install
it today (August 2023) you'll get `python311`.

In your system you'll have the `/usr/bin/python3` binary that points
to the default python, so you don't need to worry about the current
version, you'll have there the default Python version for the
operating system.

In addition to the Python interpreter, you can find in the
distribution a lot of python modules, but again you can use the
default version, so, for example, if you want to install `poetry`, you
just use `zypper install python3-poetry` and that will install
the real package `python311-poetry`.

## Multiple python versions (3.8, 3.9, 3.10, 3.11)

Besides the default Python, in Tumbleweed you can also find other
supported Python interpreters. Right now you can find all the Python
versions currently supported by the Python Foundation, from 3.8 to
3.11.

For Python 3.8 you'll only find the interpreter, because the python
modules are not built anymore, but for all the other versions you can
find almost the same modules.

All python modules that provide binaries uses the
`update-alternatives`, so you can configure in your system the version
that you want to use as default. For example, if you want to use the
`3.9` version of `poetry`, having installed different versions you can
decide what `/usr/bin/poetry` points to:

```
$ sudo zypper in python311-poetry python39-poetry
$ sudo update-alternatives --config poetry
```

`/usr/bin/python3` is a link provided by the default python package,
so you can't modify with `update-alternatives`, so if you want to use
a different python version, make sure to do the correct call with the
full name `python3.9`, and use the correct shebang in your python
scripts, for example `#!/usr/bin/env python3.9`.

## What happens when default changes?

This way of distributing Python interpreter and modules is useful,
because you don't need to update your software to work with the latest
Python version, if your software requires another version, you can just
install and continue using it, even on a bleeding-edge distribution
like Tumbleweed.

But this method has some problems. When the default Python interpreter
is changed in the distribution, all packages that depends on `python3`
will be updated, and that works correctly. But if you have installed
some python module using the `python3` prefix, that package, and all
dependencies, is not updated automatically.

For example, if you installed `python3-poetry` when `python3.10` was
the default system, and then the distribution updates the system
Python to `python3.11`, you don't get the `python311-poetry` package
by default, you'll need to install it again. This could break you
software, because if you use `python3` and the dependencies are not
updated, you'll find that some dependencies are not installed after
updating.

For that reason, when the default python is changed in Tumbleweed, if
you've software that rely on `python3` you should make sure to install
dependencies again by hand. And also you can do a cleanup and remove
all old version packages that you don't need anymore.

If you just want the latest version you can just do all at once with a
simple script like this:

```
#!/bin/bash
# up-py-tw.sh

FROM=$1
TO=$2

if [ $# -lt 2 ]
then
    echo "Usage:   up-py-tw.sh FROM TO"
    echo "example: up-py-tw.sh 310 311"
    exit 0
fi

echo "Updating python packages from $FROM to $TO"

OLDP=$(zypper -q search -i python${FROM}-* | tail --lines +4 | cut --delimiter \| --fields 2)
NEWP=$(echo $OLDP | sed "s/python${FROM}/python${TO}/g")

sudo zypper in $NEWP
sudo zypper rm $OLDP
```

You should verify what will be installed and what will be removed to
make sure that just the python related packages are removed. It's
possible that other packages depend on a python version that's older
than the system one and that's okay.

## Beta version (3.12.0b4)

In Tumbleweed, right now you can find all the supported Python
versions, but it's not just that. At this moment you can also find the
beta version of the next Python interpreter.

```
$ sudo zypper in python312
```

So if you are adventurous and want to test some new feature in the
next Python release, you can do it with the version provided there.
This version could also be used by openSUSE packagers to test the
packages before the Python version is released so it allow us to
prepare everything for the release and it could be in the distribution
earlier and more tested.

## Development

All this multiple python versions is done at distribution level and
usually there's only one source package that produces the
`python39-foo`, `python310-foo` and `python311-foo`. The source
package is usually called `python-foo` and can be found in the
[Python devel project][6].

These packages spec uses the python-rpm-macros to generate all the
versions from one source. If you're a packager you can find more
information on the openSUSE wiki about [Python Packaging][7].

[1]: https://www.opensuse.org/#Tumbleweed
[2]: https://www.python.org/
[3]: https://build.opensuse.org/project/show/devel:languages:python:Factory
[4]: https://openqa.opensuse.org/group_overview/1
[5]: https://pypi.org/
[6]: https://build.opensuse.org/project/show/devel:languages:python
[7]: https://en.opensuse.org/openSUSE:Packaging_Python
