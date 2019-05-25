Date: 2019-01-26
Title: Timetrack app for GNOME
Tags: gnome, timetrack, python
Category: blog
Slug: timetrack
Gravatar: 8da96af78e0089d6d970bf3760b0e724

This week I started a new small project called [Timetrack][1], you can find
the code in the [gnome gitlab][2].

<p class="img">
    <a href="/pictures/timetrack1.png">
        <img src="/pictures/timetrack1.png" />
    </a>
</p>

This is a simple app to store an activity log in a sqlite database and to
provide useful reports in the future. The main idea is to use this for may day
to day work, so I'll be able to keep track of my working hours and other
activities.

### The need

There's a lot of timetrack applications. There are good web apps and also some
desktop applications. At first, I tried to find a gnome-shell plugin, but I
didn't find any extension that is good for me.

I've had a [custom simple web app][3] to track my time.

<p class="img">
    <a href="/pictures/wadobo-objs.png">
        <img src="/pictures/wadobo-objs.png" />
    </a>
</p>

I've been using this app for a long time, but I don't like to use web apps for
simple tasks so I want something local.

So I tried with some gtk desktop applications, but none of the applications
that I've found looks good to me.

I wanted a simple timetrack app, without any complex stuff, so I thought that it
won't be hard to implement it. So I started with a simple python app based
on the code of [Password Safe][4].

<p class="img">
    <a href="/pictures/timetrack2.png">
        <img src="/pictures/timetrack2.png" />
    </a>
</p>

So I started to code and in two days I had a simple application that *works*.
The applications is now on flathub so it's available for use.

### The functionality

Right now, Timetrack has a limited set of features, but I think I'll improve
the app with new features as soon as I need something. So, the current version
can:

 * Track activity time with a simple button, showing the activity time spent
 * List last activities
 * Edit / Delete activities
 * Simple report by day, week or month
 * Report navigation using a calendar

I've plans to add more functionalities in the near future, like:

 * Report export to plain text and csv
 * Comments for activities
 * Tags for activities
 * Detailed reports
 * Activity Graphs

All of this is stored in a sqlite database, if you install the app using flatpak
you can find the database in this path:
`~/.var/app/net.danigm.timetrack/data/timetrack.sqlite3`.

I've *done* the icon for this app using the gnome-clocks icon and adding some
colors to it.

If you find this app useful, don't hesitate and use it. Any feature request or
bug report is welcome. And of course, all is free software, so if you want to
collaborate, go ahead and send me some Merge Request.

[1]: https://flathub.org/apps/details/net.danigm.timetrack
[2]: https://gitlab.gnome.org/danigm/timetrack
[3]: https://github.com/wadobo/django-objs
[4]: https://gitlab.gnome.org/World/PasswordSafe/
