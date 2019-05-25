Date: 2019-05-05
Title: Kung-fu Master, Blindfolded debugging
Tags: gnome, software, debugging
Category: blog
Slug: blindfolded
Gravatar: 8da96af78e0089d6d970bf3760b0e724

Recently I've been working in the [EOS][1] update. The change is really big
because EOS has some modifications over the upstream code so there are a lot
of commits applied after the last stable upstream commit.

EOS 3.5 was based on gnome 3.26 and we are updating to use the gnome 3.32 so
all the downstream changes done since the last release should be rebased on top
of the new code and during this process we refactor the code and commits using
new tools and remove what's now in gnome upstream.

I've been working in the Hack computer custom functionality that's on top of
the EOS desktop and basically I've been rebasing the code in the shell to
do the Flip to Hack, the Clubhouse, a side component and notification override
to propse hack quests and the wobbly windows effects.

I've been working mainly with gnome shell and updating javascript code to the
new gjs version, but this was a big change and some rare bugs.

Here comes the blindfolded debugging. I've a development system with a lot of
changes and a functionality in the gnome shell that depends on different
projects, applications and technologies.

I don't know the code a lot, because I'm not the one that wrote all of this,
I'm working here since February, so I know a bit how things works, but I'm not
the one who knows everything, there are a lot of rare cases that I don't know
about.

<p class="img">
    <img src="/pictures/blindfolded/kungfu.gif" />
</p>

I've found and fixes several bugs in different projects, that I don't know about
a lot, during this process. How can I do that? If you are a developer that
write code since a few years maybe you've experienced something similar, I'm
calling this the **blindfolded debugging technique**:

> Start to change code without knowing exactly what you're doing, but with a
small feeling that maybe that line is the problem.

This technique is only for experienced programmers, as a kungfu master that
put a blindfold in their eyes to fight against an opponent, the developer that
will be brave enough to try this should have a lot of experience or he will fail.

You're an experienced developer, but you don't know the software that you're
debugging. It doesn't matter. The same way that in a kungfu fight you don't
know your opponent, but almost every fighter has two arms and two legs, so
more or less you'll know that he'll try to punch you or kick you, you've a
clue. As a programmer, every software has an structure, functions, loops...

No matters who wrote that or how old that code is, if you're an experienced
programmer you'll feel the code and without knowing exactly why or how, you
will be able to look at one line and says: *Here you're little buggy friend*.

Maybe I'm only trying to justify my lucky with a story to feel better and
say that I'm not a dumb changing random lines to try to find a bug, but I'm
sure that other developers has this feeling too, that feeling that guides you
to the exact problem but that you're not able to rationalize.

<p class="img">
    <img src="/pictures/blindfolded/fight.gif" />
</p>

I think that this is the experience, the expertise is your body and your
inner brain doing the work meanwhile you don't need to think about it or
know exactly what you are doing.

[1]: https://endlessos.com/
