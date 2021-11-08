Date: 2021-11-08
Title: Endless Orange Week: Hack content creators platform
Tags: hack, endless, orangeweek, work
Slug: hack-content-creators
Gravatar: 8da96af78e0089d6d970bf3760b0e724

This week (Nov 8 – 12) I am participating in Endless Orange Week, a program
where the entire [Endless][1] team engages in projects designed to grow our
collective learning related to our skills, work and mission.

We propose a project, that could be anything, and then work during the whole
week, without distraction. I've choosed to work on the [Hack project][2], that's a
really nice project that needs some love, because since the past year, we have
[other priorities][3], so there's no time to improve the Hack app.

<p class="img">
    <a href="/pictures/clubhouse.png">
        <img src="/pictures/clubhouse.png" />
    </a>
</p>


## The project: Hack content creators platform

The Hack application is a "Quest" launcher, and each Quest is an interactive
learning experience, a guided introduction to some technology or topic.

Quests are just python scripts, with a simple library to expose messages to the
user, ask questions, or wait for desktop events, like launch an application,
focus an application, etc. And all these Quests are inside the application, and
are created by the Hack team and released with a new Hack app flatpak.

The main idea of the project is to provide a simple Quest editor to allow any
Hack user to create and share their our Quests.

To have this Hack content creators platform we'll need:

1. To simplify the way we create Quests, instead of a python script, we'll uses
   a Domain Specific Language, called [Ink][4]. We started to work on this, but
   we never ended the support.
1. To create the interface to be able to import and export custom Quests, that
   could be zip bundles, with the Ink script and some images.
1. To create the interface to write the actual Quests and save or bundle.
1. Create some introductory Quest to explain "how to create your own Quests!".
1. Create an character editor, to be able to "design" new characters for Quests.

### The Quest editor

The Quests will be written using the Ink language, and there's [something done before][5].
The first idea is to just provide a text editor and some helpful information
about the format, and maybe a button to validate. But if there's time we can
use something advanced or even integrate the [Inky][5] editor.

### The Character editor

Each Quest has a main character, and we've five in the Hack app right now, but
it could be great to be able to define new ones for custom Quests. That's the
idea of this part of the project.

The initial idea is to have a library of character parts to combine, and the
editor will allow the user to combine this parts and maybe change colors, to be
able to create unique characters for your Quests.

### The Team

I'm not working alone in this "side" project during the Endless Orange Week,
Simon Schampijer and Joana Filizola will be working on this too, so this is a
big task but we've a great team. Let's see how far we are able to go during
just one week.

### The impact

This is just a project to try to keep alive more time the Hack application,
without a lot of effort or a whole team behind it. We are not able to put more
content there periodically, so if there's a way to create new content easily
and (maybe in the future) a way to publish, it'll be possible to create a
community around the project.

And we have also new possibilities, in the near future, we can add some Hack
content to the Endless Key, and using the Ink language, so this editor could
help to bring more content there easily.

And the final piece, the Character editor, could be an independent application,
a nice simple application that could be used to create your character for your
profile photo, or to generate random character pics.

[1]: https://www.endlessos.org/
[2]: https://www.hack-computer.com/
[3]: https://www.endlessos.org/key
[4]: https://www.inklestudios.com/ink/
[5]: https://flathub.org/apps/details/com.inklestudios.Inky
