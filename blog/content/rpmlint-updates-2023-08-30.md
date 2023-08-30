Date: 2023-08-30
Title: rpmlint updates (August 2023)
Tags: gnome, software, rpmlint, suse, gsoc
Slug: rpmlint-updates-2023-08-30
Gravatar: 7ce0b0e40deeb4f549d2a04b3c5ea3cc
Category: blog

We are at the end of the summer and this means that this year Google Summer of
code is ending.

<p class="img">
  <img src="/pictures/rpmlint-gitg-gsoc-2023.png" />
</p>

The recent changes applied now in the main branch include:

 * Remove usage of `pkg_resource` because it's deprecated.
 * Fix elf binary check with ELF files with a prefix.
 * New check for python packages with multiple .pyc files for different python
   versions.
 * Improve the testing framework (merged the work done during the GSoC 2023)

## Summer of Code 2023 updates

The summer of code is ending and the work done by [Afrid was good enough to be merged][1],
so I merged it the past week.

I'm really happy with the work done during the GSoC program, now we've a more
simple way to define tests for rpmlint checks mocking the rpm, so it's not
always needed to build a fake rpm binary for each new test. This will make a
lot easier to create simple tests, so I hope that we can increase the code
coverage using this [new framework][2].

During this time Afrid has extended the `FakePkg` class, so it's possible now
to define fake metadata and files with fake tags and attributes. It's not
complete and it's not a simple task to replace all the `rpm` binaries used for
tests, because the `Pkg` class and `RPM` tags is a complex thing, but the
current state allow us to replace a lot of them. Afrid has replaced some of the
tests that uses binaries, but in the following months we can continue working
on this and [replace more][3].

After this work, we can now start to use more the `FakePkg` class in tests,
so another task that we can do is to provide some [common fake pkgs][4] to use
in different tests and new checks, so now it's possible to create fake packages
with dynamic random data, so we can extend tests with fuzz testing and maybe
this will help to improve the tool reliability.

<p class="img">
  <img src="/pictures/gsoc.png" />
</p>

## Conclusion

I've participated as mentor several times now in the [summer of code][6], and
[outreachy][7], and almost always was a good experience. With the [gnome foundation][8]
in previous programs and this year with [opensuse][9]. These two communities
are very open to collaboration and makes the whole process really simple, for
me as mentor, and also for the intern.

I want to congratulate Afrid, because it was nice to work with him during this
summer, he has done a great work, not just technically, but communicating,
asking and finding his own solutions without requiring a continuous guidance.

He is very passionate and looks like a nice person, so I hope that he will
continue around the open source, it could be opensuse, rpmlint or any other
community, but this kind of people is what you want to find in any community.

After many years collaborating with different free software communities, it's
amazing that there are so many great people in every project, of course you can
find toxic communities and people, but in my experience, that's usually just
noise, there are a lot of nice people out there, doing a great work, and I'm
happy that young people like Afrid can be part of the free software movement,
because this is what makes the free software great, the people that is
working on it.

So Thanks a lot to Google for another summer of code, thanks to SUSE for
letting me, and encourage me, to mentor, and thanks to all the free software
developers that are out there.

I encourage everyone to participate in this kind of programs, for interns, it's
a good opportunity to learn and to make some money working on free software,
for mentors it's an opportunity to get some help in your project and help
newcomers to be part of the community.

Have a lot of fun!

[1]: https://github.com/rpm-software-management/rpmlint/pull/1101
[2]: https://github.com/rpm-software-management/rpmlint/blob/main/test/README.md
[3]: https://github.com/rpm-software-management/rpmlint/issues/1105
[4]: https://github.com/rpm-software-management/rpmlint/issues/1104
[5]: https://afridhussain.tech/
[6]: https://summerofcode.withgoogle.com/
[7]: https://www.outreachy.org/
[8]: https://www.gnome.org/
[9]: https://www.opensuse.org/
