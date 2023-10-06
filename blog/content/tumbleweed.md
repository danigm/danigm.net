Date: 2023-10-06
Title: One year of Tumbleweed
Tags: gnome, work, suse, openSUSE, tumbleweed, linux, distribution
Category: blog
Slug: tumbleweed
Gravatar: 8da96af78e0089d6d970bf3760b0e724

<p class="img">
    <a target="_blank" href="https://www.opensuse.org/#Tumbleweed">
        <img src="/pictures/tumbleweed.png" />
    </a>
</p>

More than a year has passed since I switched to [openSUSE Tumbleweed][1]
Linux distribution, in both, my work computer (for obvious reasons)
and in my personal computer and I can say that I'm really happy with
the change.

Tumbleweed is a [rolling release][2] distribution, and in this kind of
distributions there are a lot of changes every week, if you want the
latest software, this kind of distribution is the way to go. But with
high update frequency you are exposed to some kind of instability,
it's impossible to have the latest changes without some broken program
here and there, because not everyone is able to follow upstream
changes without some weeks or months to update.

## My distro history

I've been always a Linux user, since I get my first computer at 2003.
In those days I was using a [debian][3] base distribution called
[knoppix][4]. Then I switched to [ubuntu][5] when it appeared around 2004.
But at that time I was a computer science student and I was exploring
the whole free software and Linux ecosystem, so I was changing my
distribution every time that I found a new one.

Like a lot of distro-hoppers, at some point I landed at [ArchLinux][6]
and there I discovered the rolling release concept. And that was my
home for some time, it was nice to have the latest available software
just after the release.

At some point I bough a new computer and it was too new to work
correctly with the kernel distributed in ArchLinux, so I tried
different distributions and at that moment [Fedora][7] was the distro
that works without too much complications with that computer, so I
picked that one.

In 2019 I started to work at Endless and at that time I should try the
[EndlessOS][8], so I played a bit with [the dual boot][9], having
Fedora and EndlessOS at the same time. That was the first time that I
get in contact with immutable distributions, something that's getting
more popular everyday, but this distributions rely a lot on containers
(flatpak, podman) and, even being something that could work, as a
software engineer, I don't feel comfortable enough needing a container
with another distribution to do something that could be in my system.

In 2022 I started to [work at SUSE][10] and for the first time I tried
the openSUSE distribution until today.

## The Tumbleweed

Today I've three different computers with Tumbleweed running. One for
work, Thinkpad T14s, one for personal usage, Dell inspiron 5490, and
another one as a personal media server, Libre computer [La-frite][11].

The best thing of having Tumbleweed for me is that I get the latest
**GNOME** as soon as it's released. And another big thing for this
distribution is how easy it's to fix something upstream thanks to the
[Open Build Service][12], but I work everyday with that, so I'm
biased. For sure, any other community distribution has different ways
to contribute, but I find this one easy enough.

Even being a rolling release distro, Tumbleweed doesn't break a lot. I
can't say that it's stable, because the API of everything is broken
everyday, but the [distribution is tested][13] for every release and
at least some level of package compatibility check is done. That makes
Tumbleweed a good distribution and I can update without fearing some
weird package breakage.

I usually update my work and personal laptops once a week, and
la-frite not so often, maybe every 6 months.

With the default installation, Tumbleweed uses btrfs with snapshots,
and it's really easy to go back and forward using the
[snapper tool][14]. So it's really easy to go back to a good state if
the distribution is broken for some reason, and wait for a fix.

## The problems that I found during this year

 * Some problems with the NVidia graphic card in my Dell laptop, some
   times the kernel and the driver were not working correctly. I had
   to use snapper to get the NVidia working again, but fixed a few
   days later.
 * Currently I'm having some random crashes because some bug with
   [amdgpu][15] and wayland and mutter, but it's not too annoying for
   me to go back, so I didn't use snapper this time and I'm facing
   this random crashes waiting for the fix.

## Long live the Tumbleweed

So far so good. Tumbleweed is a nice distribution that I'm enjoying.
It's not getting in the way and I can find almost anything that I need
for work, programming, gaming, media, etc. I'm really happy with this
distribution and it's the perfect distribution for people like me,
that want to have the latest things.

I know that there are other openSUSE flavors that are interesting,
like the [immutable ones][16], [Leap][17] or the latest one
[Slowroll][17], but Tumbleweed is the one for me.

[1]: https://www.opensuse.org/#Tumbleweed
[2]: https://en.wikipedia.org/wiki/Rolling_release
[3]: https://www.debian.org/
[4]: https://www.knopper.net/knoppix/index-en.html
[5]: https://ubuntu.com/
[6]: https://archlinux.org/
[7]: https://fedoraproject.org/
[8]: https://www.endlessos.org/
[9]: https://danigm.net/endlessos-dual-boot.html
[10]: https://danigm.net/suse.html
[11]: https://libre.computer/products/aml-s805x-ac/
[12]: https://build.opensuse.org/project/show/openSUSE:Factory
[13]: https://openqa.opensuse.org/group_overview/1
[14]: https://en.opensuse.org/openSUSE:Snapper_Tutorial
[15]: https://bugzilla.suse.com/show_bug.cgi?id=1215695
[16]: https://en.opensuse.org/Portal:Aeon
[17]: https://en.opensuse.org/openSUSE:Slowroll
