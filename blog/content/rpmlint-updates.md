Date: 2023-07-06
Title: rpmlint updates (July 2023)
Tags: gnome, software, rpmlint, suse, gsoc
Slug: rpmlint-updates
Gravatar: 7ce0b0e40deeb4f549d2a04b3c5ea3cc
Category: blog

I'm spending some time every week working in the [rpmlint][2] project.
The tool is very stable and the functionality is well defined,
implemented and tested, so there's no crazy development or a lot of
new functionalities, but as in all the software, there are always bugs
to solve and things to improve.

<p class="img">
  <img src="/pictures/rpmlint-gitg-20230706.png" />
</p>

The recent changes applied now in the main branch include:

 * Update the usage of `rpm` to not use old API.
 * Fixes for `rpmdiff -v`, check for NULL char, special macros in
   comments and spell checking of description in different languages.
 * Move all the metadata from `setup.py` to `pyproject.toml`.
 * Releasing rpmlint as pre-commit hook
 * Improvements to the PythonCheck in the dependency checking.

## Summer of Code 2023 updates

The first month of the Summer of Code has passed and [Afrid][1] is
doing a great job there. We've now a [draft Pull Request][5] with some
initial changes that allow us to mock `rpm` packages in tests so it's
easier to create new tests without the need of creating a binary
package.

The first step done was to extend the existing `FakePkg` class to
allow us to define package files and some package metadata.

Now he's working in replacing all of the `test_python.py` tests that
uses binaries `rpm` to something that doesn't needed.

The idea is to replace as much tests as possible to reduce the number
of rpm binaries and after that, provide helper functions, decorators
and classes to make it easy to write tests, writing less code.

## Roadmap

In any software project there's always room for improvements, fixes
and enhancements. If the project is there for enough time, it's even
more critical to modernize the code to reduce the technical debt.

My plan for 2023 is to improve the tests around rpmlint as much as
possible. First with the GSoC project, making it easier to write more
tests, improving the testing tools that we've. And after the summer,
improving the test coverage.

There's also a tool that shares some of the ideas with rpmlint,
[spec-cleaner][3], it's also written in Python, so the next step,
after the tests improvements will be to take a deep look into the code
of these two tools and try to integrate in some way. Maybe it's
possible to refactor the common code into an external module, maybe we
can bring some ideas from spec-cleaner to rpmlint. Not sure yet, but
that'll be my next step.

Don't forget that this is free software, so you can participate too!
If you find any issue in rpmlint or have an idea to improve it, don't
hesitate and [create a new issue][4].

[1]: https://afridhussain.tech
[2]: https://github.com/rpm-software-management/rpmlint
[3]: https://github.com/rpm-software-management/spec-cleaner
[4]: https://github.com/rpm-software-management/rpmlint/issues
[5]: https://github.com/rpm-software-management/rpmlint/pull/1079
