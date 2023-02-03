Date: 2023-01-03
Title: Hackweek 2023
Tags: gnome, work, suse, ink, python
Category: blog
Slug: hackweek22
Gravatar: 7ce0b0e40deeb4f549d2a04b3c5ea3cc

<center>
    <img src="/pictures/hackweek.png" width="50%"/>
</center>

[Hack Week][1] is the time SUSE employees experiment, innovate & learn
interruption-free for a whole week! Across teams or alone, but always without
limits.

This year the Hack Week was this week, the last week of January and for my
first SUSE hack week I decided to work in something funny, [LILS][2].

## Linux Immersive Learning System (LILS)

I don't think that this is a good name, but don't focus on it. The main idea of
this project is to create some basic machinery to be able to write
"interactive" tutorials or games using the [INK language][3].

This is not an original idea, indeed all I've done is something that's
currently working on [EndlessOS][4], and was the main idea behind the dead
project [Hack Computer][5], you can even take a look to the
[Hack app in flathub][6]. But I wanted to work around this, and create
something simpler, from scratch.

I wanted to build something simple, with just Python, and make it simple enough
to be able to build other tools on top. The design is simple, an INK parser,
with a simple game runner. In the INK script you can define *commands*, to do
something special, and wait for events with *listeners*, to wait for an event
in the OS to continue.

With this basic functionality it's possible to build different user interfaces
for different environments. And the original idea was to make the *commands*
and *listeners* something extensible with a simple API, but that's something
that I have not done yet, it's all Python functions without extension point.

The code can be found in [github][7].

## The INK parser

<p class="img">
    <img src="/pictures/inky.png" />
</p>

The most complex part of this project is the INK language parser. The [Ink][8]
parser is free software and there's a Linux version that you can use to parse
and **compile** to *json*, but I wanted to create my own parser with Python.

I've spent most of the Hack Week time fighting with the parser and indeed was
the most challenging and fun part, because I've not worked a lot with parsers
and it's not something easy as pie 😛️.

I remember creating a java compiler long time ago, when I was in the Seville
University, for the Language Processors course. We did that with [ANTLR][9], so
starting from that, and looking for a Python lib, I found the [Lark][10]
project. So if you like regular expressions, writing a grammar is a lot more
FUN.

At the end I was able to support some basic INK language with support for:

 * Text
 * Tag support
 * Options, with suppress text support
 * Knots, Stitches and Diverts
 * Include other .ink files
 * Variable definition and basic operations
 * Knots and Stitches automatic visiting count variables
 * Conditional options using variables

It still fails in some cases, the comments and *TODO* placed in between text is
not detected correctly and there's a lot of complex stuff that's not supported
yet, but with what's supported right now it's possible to create complex
scripts with loops and complex game graphs, so it's good enough to build games
just with it.

## GNOME shell extension

<p class="img">
    <video src="/pictures/lils.mp4" width="100%" autoplay controls loop />
</p>

To integrate with the system I've done a simple [GNOME shell extension][11].
The extension just shows the text as bubbles and options as buttons, it's
really simple and I've no time to make it something ready to be used, but
I was able to make something usable.

To be able to run the *LILS* python library from *gjs* I've created a simple
*dbus* service that exposes the basic *InkScript* class functionality as a dbus
API.

I was thinking about being able to change the desktop background, depending of
the value of a *background* variable in the script and do something similar to
play music and sounds, so it could be a cool *game engine* with some additions.

## SUSE Hack Week

So this Hack week was really fun and I learned a lot. It's really great that
SUSE does things like this, letting us work in different projects for a week,
to learn, to grow or to just explore different paths.

<iframe width="560" height="315" src="https://www.youtube.com/embed/IxscORgeqOY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>


[1]: https://hackweek.opensuse.org/
[2]: https://hackweek.opensuse.org/22/projects/linux-immersive-learning-system-lils
[3]: https://www.inklestudios.com/ink/
[4]: https://www.endlessos.org/
[5]: https://www.hack-computer.com/
[6]: https://flathub.org/apps/details/com.hack_computer.Clubhouse
[7]: https://github.com/danigm/lils
[8]: https://github.com/inkle/ink
[9]: https://www.antlr.org/
[10]: https://github.com/lark-parser/lark
[11]: https://github.com/danigm/lils/tree/master/lils%40danigm.net
