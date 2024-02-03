Date: 2024-02-03
Title: Where's my python code?
Tags: gnome, work, suse, linux, python
Category: blog
Slug: wheres-my-python-code
Gravatar: 8da96af78e0089d6d970bf3760b0e724

<img src="/pictures/python-logo-master-v3-TM.png" width="100%" />

Python is a interpreted language, so the python code are just text
files with the `.py` extension. For simple scripts it's really easy to
have your files located, but when you starts to use dependencies and
different projects with different requirements the thing starts to get
more complex.

## PYTHONPATH

The Python interpreter uses a list of paths to try to locate python
modules, for example this is what you can get in a modern GNU/Linux
distribution by default:

```python
Python 3.11.7 (main, Dec 15 2023, 10:49:17) [GCC] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> sys.path
['',
 '/usr/lib64/python311.zip',
 '/usr/lib64/python3.11',
 '/usr/lib64/python3.11/lib-dynload',
 '/usr/lib64/python3.11/site-packages',
 '/usr/lib64/python3.11/_import_failed',
 '/usr/lib/python3.11/site-packages']
```

These are the default paths where the python modules are installed. If
you install any python module using your linux packaging tool, the
python code will be placed inside the `site-packages` folder.

So system installed python modules can be located in:

 * `/usr/lib/python3.11/site-packages` for modules that are
   architecture independent (pure python, all `.py` files)
 * `/usr/lib64/python3.11/site-packages` for modules that depends on
   the arquitecture, that's something that uses low level libraries
   and needs to build so there are some `.so` files.

## pip

When you need a new python dependency you can try to install from your
GNU/Linux distribution using the default package manager like
`zypper`, `dnf` or `apt`, and those python files will be placed in the
system paths that you can see above.

But distributions doesn't pack all the python modules and even if they
do, you can require an specific version that's different from the one
packaged in your favourite distribution, so in python it's common to
install dependencies from the [Python Package Index (PyPI)][1].

Python has a tool to install and manage Python packages that looks for
desired python modules in PyPI.

You can install new dependencies with `pip` just like:

```
$ pip install django
```

And that command looks for the `django` python module in the PyPI,
downloads and install it, in your user
`$HOME/.local/lib/python3.11/site-packages` folder if you
use `--user`, or in a global system path like `/usr/local/lib` or
`/usr/lib` if you run pip as root.

But the usage of `pip` directly in the system is something **not
recommended today**, and even [it's disabled][2] in some
distributions, like openSUSE Tumbleweed.

```
[danigm@localhost ~] $ pip install django
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try
    zypper install python311-xyz, where xyz is the package
    you are trying to install.

    If you wish to install a non-rpm packaged Python package,
    create a virtual environment using python3.11 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip.

    If you wish to install a non-rpm packaged Python application,
    it may be easiest to use `pipx install xyz`, which will manage a
    virtual environment for you. Install pipx via `zypper install python311-pipx` .

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

## virtualenvs

Following the current recommendation, the correct way of installing
third party python modules is to use `virtualenvs`.

The `virtualenvs` are just specific folders where you install your
python modules and some scripts that make's easy to use it in
combination with your system libraries so you don't need to modify the
`PYTHONPATH` manually.

So if you've a custom project and want to install python modules you
can create your own virtualenv and use pip to install dependencies
there:

```
[danigm@localhost tmp] $ python3 -m venv myenv
[danigm@localhost tmp] $ . ./myenv/bin/activate
(myenv) [danigm@localhost tmp] $ pip install django
Collecting django
...
Successfully installed asgiref-3.7.2 django-5.0.1 sqlparse-0.4.4
```

So all dependencies are installed in my new virtualenv folder and if I
use the python from the virtualenv it's using those paths, so all the
modules installed there are usable inside that virtualenv:

```
(myenv) [danigm@localhost tmp] $ ls myenv/lib/python3.11/site-packages/django/
apps  contrib  db        forms  __init__.py  middleware   shortcuts.py  templatetags  urls   views
conf  core     dispatch  http   __main__.py  __pycache__  template      test          utils
(myenv) [danigm@localhost tmp] $ python3 -c "import django; print(django.__version__)"
5.0.1
(myenv) [danigm@localhost tmp] $ deactivate
```

With virtualenvs you can have multiple python projects, with different
dependencies, isolated, so you use different dependencies when you
activate your desired virtualenv:

 * activate `$ . ./myenv/bin/activate`
 * deactivate `$ deactivate`

## High level tools to handle virtualenvs

The [venv][3] module is a default Python module and as you can see
above, it's really simple to use, but there are some tools that
provides some tooling around it, to make it easy for you, so usually
you don't need to use `venv` directly.

### pipx

For final python tools, that you are not going to use as dependencies
in your python code, the recommended tool to use is [pipx][4].

<img src="/pictures/pipx_demo.gif" width="100%" />

The tool creates virtualenv automatically and links the binaries so
you don't need to worry about anything, just use as a way to install
third party python applications and update/uninstall using it. The
`pipx` won't mess your system libraries and each installation will use
a different virtualenv, so even tools with incompatible dependencies
will work nicely together in the same system.

### Libraries, for Python developers

In the case of Python developers, when you need to manage dependencies
for your project, there are a lot of nice high level tools for
[managing dependencies][5].

 * [PDM][9]
 * [hatch][7]
 * [micropipenv][8]
 * [pip-tools][10]
 * [pipenv][6]
 * [poetry][11]

These tools provides different ways of managing dependencies, but all
of them relies in the use of `venv`, creating the virtualenv in
different locations and providing tools to enable/disable and manage
dependencies inside those virtualenvs.

For example, `poetry` creates virtualenvs by default inside the
`.cache` folder, in my case I can find all poetry created virtualenvs
in:

```
/home/danigm/.cache/pypoetry/virtualenvs/
```

Most of these tools add other utilities on top of the dependency
management. Just for installing python modules easily you can always
use default `venv` and `pip` modules, but for more complex projects
it's worth to investigate high level tools, because it'll make easy to
manage your project dependencies and virtualenvs.

## Conclusion

There are a lot of python code inside any modern Linux distribution
and if you're a python developer it's possible to have a lot of python
code. Make sure to know the source of your modules and do not mix
different environments to avoid future headaches.

As a final trick, if you don't know where's the actual code of some
python module in your running python script, you can always ask:

```
>>> import django
>>> django.__file__
'/tmp/myenv/lib64/python3.11/site-packages/django/__init__.py'
```

This could be even more complicated if you start to use containers
and different python versions, so keep you dependencies clean and up
to date and make sue that you know **where is your Python code**.

[1]: https://pypi.org/
[2]: https://packaging.python.org/en/latest/specifications/externally-managed-environments/#externally-managed-environments
[3]: https://docs.python.org/3/library/venv.html#module-venv
[4]: https://github.com/pypa/pipx
[5]: https://packaging.python.org/en/latest/tutorials/managing-dependencies/#other-tools-for-application-dependency-management
[6]: https://packaging.python.org/en/latest/key_projects/#pipenv
[7]: https://github.com/pypa/hatch
[8]: https://github.com/thoth-station/micropipenv
[9]: https://github.com/pdm-project/pdm
[10]: https://github.com/jazzband/pip-tools
[11]: https://github.com/python-poetry/poetry
