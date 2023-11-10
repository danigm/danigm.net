Date: 2023-11-10
Title: Hackweek 23
Tags: gnome, work, suse, opensuse, hackweek
Category: blog
Slug: hackweek23
Gravatar: 7ce0b0e40deeb4f549d2a04b3c5ea3cc

<center>
    <img src="/pictures/hackweek23.png" width="100%"/>
</center>

[Hack Week][1] is the time SUSE employees experiment, innovate & learn
interruption-free for a whole week! Across teams or alone, but always without
limits.

The Hack Week 23 was from November 6th to November 10th, and my project was to
gvie some [love to the GNOME Project][2].

Before the start of the Hack week I asked in the GNOME devs Matrix channel,
what project needs some help and they gave me some ideas. At the end I decided
to work on the [GNOME Calendar][3], more specifically, improving the test suite
and fixing [issues related to timezones][5], DST, etc.

## GNOME Calendar

<center>
    <img src="/pictures/gnome-calendar.png" width="100%"/>
</center>

GNOME Calendar is a [Gtk4 application][6], written in C, that heavily uses the
[evolution-data-server][7] library. It's a desktop calendar application with a
modern user interface that can connect handle local and remote calendars. It's
integrated in the GNOME desktop.

The current gnome-calendar project has some unit tests, using the [GLib testing
framework][8]. But right now there are just a few tests, so the main goal right
now is to increase the number of tests as much as possible, to detect new
problems and regressions.

Testing a desktop application is not something easy to do. The unit tests can
check basic operations, structures and methods, but the user interaction and
how it's represented is something hard to test. So the best approach is to try
replicate user interactions and check the outputs.

A more sophisticated approach could be to start to use the accessibility stack
in tests, so it's possible to verify the UI widgets output without the need of
rendering the app.

With gnome-calendar there's another point of complexity for tests because it
relies on the evolution-data-server to be running, the app communicates with it
using dbus, so to be able to do more complex tests we should mock the
evolution-data-server and we should create fake data for testing.

## My contribution

By the end of the week I've created four [Merge requests][9], three of them
have been merged now, and I'll continue working on this project in the
following weeks/months.

I'm happy with the work that I was able to do during this Hack Week. I've
learned a bit about testing with GLib in C, and a lot about the
evolution-data-server, timezones and calendar problems.

It's just a desktop calendar application, how hard it could be? Have you ever
deal with dates, times and different regions and time zones? It's a nightmare.
There are a lot of edge cases working with dates that can cause problems,
operations with dates in different time zones, changes in dates for daylight
saving, if I've an event created for October 29th 2023 at 2:30 it will happens
two times?

<center>
    <img src="/pictures/gnome-calendar-issues.png" width="100%"/>
</center>

A lot of problems could happen and there are a lot of bugs reported for
gnome-calendar related to this kind of issues, so working on this is not
something simple, it requires a lot of edge case testing and that's the plan,
to cover most of them with automated tests, because any small change could lead
to a bug related to time zones that won't be noticed until someone has an
appointment at a very specific time.

And this week was very productive thanks to the people working on
gnome-calendar. Georges Stavracas reviews my MR very quickly and it was
possible to merge during the week, and Jeff Fortin does a great work with the
issues in gitlab and leading me to most relevant bugs.

So after a week of going deep into the gnome-calendar source code it could be a
pity to just forget about it, so I'll try to keep the momentum and continue
working on this project, of course, I'll have just a few hours per week, but
any contribution is better than nothing. And maybe for the next summer I can
propose a Google Summer of Code project to get an intern working on this full
time.

[1]: https://hackweek.opensuse.org/
[2]: https://hackweek.opensuse.org/23/projects/gnome-love
[3]: https://gitlab.gnome.org/GNOME/gnome-calendar/
[5]: https://gitlab.gnome.org/GNOME/gnome-calendar/-/issues/1093
[6]: https://gtk.org/
[7]: https://gitlab.gnome.org/GNOME/evolution-data-server
[8]: https://docs.gtk.org/glib/testing.html
[9]: https://gitlab.gnome.org/GNOME/gnome-calendar/-/merge_requests?scope=all&state=all&author_username=danigm&label_name%5B%5D=Timezones
