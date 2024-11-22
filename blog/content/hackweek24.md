Date: 2024-11-22
Title: Hackweek 24
Tags: gnome, work, suse, opensuse, hackweek
Category: blog
Slug: hackweek24
Gravatar: 7ce0b0e40deeb4f549d2a04b3c5ea3cc

<center>
    <img src="/pictures/hackweek24.png" width="50%"/>
</center>

It's the time for a new [Hack Week][1]. The Hack Week 24 was from
November 18th to November 22th, and I've decided to join the [New openSUSE-welcome][2]
project this time.

The idea of this project is to revisit the existing openSUSE welcome
app, and I've been trying to help here, specifically for the GNOME
desktop installation.

## openSUSE-welcome

<center>
    <img src="/pictures/opensuse-welcome.png" width="100%"/>
</center>

Right now after installing any openSUSE distribution with a graphical
desktop, the user is welcomed on first login with a [custom welcome app][3].

This custom application is a Qt/QML with some basic information and
useful links.

The same generic application is used for all desktops, and for popular
desktops right now exists upstream applications for this purpose, so
we were talking on Monday morning about it and decided to use specific
apps for desktops.

So for GNOME, we can use the [GNOME Tour][4] application.

## gnome-tour

<center>
    <img src="/pictures/gnome-tour.png" width="100%"/>
</center>

GNOME Tour is a simple rust/gtk4 application with some fancy images in
a slideshow.

This application is generic and just shows information about GNOME
desktop, so I created a [fork for openSUSE][5] to do some openSUSE
specific customization and use this application as openSUSE welcome in
GNOME desktop for Tumbleweed and Leap.

<center>
    <img src="/pictures/gnome-tour-opensuse.png" width="100%"/>
</center>

## Desktop patterns, the welcome workflow

After some testing and investigation about the current workflow for
the welcome app:

1. [x11_enhanced][6] pattern recommends opensuse-welcome app.
1. We can add a `Recommends: gnome-tour` to the [gnome pattern][7]
1. The application run using [xdg autostart][8], so gnome-tour package
   should put the file in `/etc/xdg/autostart` and set to hidden on
   close.
1. In the case of having a system with multiple desktops, we can
   choose the specific welcome app using the `OnlyShowIn/NotShowIn`
   [config in desktop file][9]

So I've created a [draft PR][10] to do not show the openSUSE-welcome
app in GNOME, and I've also the [gnome-tour fork][11] in my home OBS
project.

I've been testing this configuration in Tumbleweed with GNOME, KDE and
XFCE installed and it works as expected. The openSUSE-welcome is shown
in KDE and XFCE and the gnome-tour app is only shown in GNOME.

<center>
    <img src="/pictures/gnome-tour-tumbleweed.png" width="100%"/>
</center>

## Next steps

The next steps to have the GNOME Tour app as default welcome for
openSUSE GNOME installation are:

1. Send forked `gnome-tour` package to `GNOME:Next` project in OBS.
1. Add the `Recommends: gnome-tour` to `patterns-gnome` to `GNOME:Next` project in OBS.
1. Make sure that any other welcome application is [not shown in GNOME][10].
1. Review openQA tests that expect opensuse-welcome and adapt for the
   new application.

[1]: https://hackweek.opensuse.org/
[2]: https://hackweek.opensuse.org/projects/opensuse-welcome
[3]: https://github.com/openSUSE/openSUSE-welcome/
[4]: https://gitlab.gnome.org/GNOME/gnome-tour/
[5]: https://github.com/openSUSE/gnome-tour
[6]: https://code.opensuse.org/package/patterns-base/blob/master/f/patterns-base.spec#_861
[7]: https://code.opensuse.org/package/patterns-gnome/blob/master/f/patterns-gnome.spec#_240
[8]: https://specifications.freedesktop.org/autostart-spec/latest/
[9]: https://specifications.freedesktop.org/desktop-entry-spec/latest/recognized-keys.html
[10]: https://github.com/openSUSE/openSUSE-welcome/pull/43
[11]: https://build.opensuse.org/package/show/home:dgarcia:branches:GNOME:Next/gnome-tour
