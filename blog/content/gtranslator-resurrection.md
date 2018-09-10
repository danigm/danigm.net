Date: 2018-09-10
Title: Gtranslator Resurrection
Tags: gnome, gtranslator
Category: blog
Slug: gtranslator-resurrection
Gravatar: 8da96af78e0089d6d970bf3760b0e724

The last week I received a telegram message about [Gtranslator][1], that was
unmaintained for a long time. GNOME translators uses different tools to
translate .po files, Gtranslator is a tool for translator that is integrated
with the GNOME desktop, but with the time, Gtranslator is getting old and there
are several known bugs that never get fixed.

So I decided to go ahead and become the maintainer of Gtranslator with the main
idea of update the interface and fix mayor bugs.

## Why we should care about Gtranslator

PO files are plain text files that can be edited with any text editor, but
there're a lot of tools for translator to simplify the edition of .po files,
these way the program will avoid formatting problems and can also provide some
tools to help in the translation.

There's a lot of tools to edit .po files, so, why we need another application?
why translators can't pick another useful tool if Gtranslator is unmaintained?

The main reason is the same as we've a text editor or the gnome-builder or other
developer tools, because all users want to use applications integrated in the
desktop, so it always will be better for a GNOME user a native GNOME app to edit
.po files than a Qt one or a webpage.

The other reason is that we need to simplify the translators life to have better
and more translations and that can only be done if we're developping the tool
that translator will use, because in the future we can integrate Gtranslator
with the gnome gitlab, or with [Damned Lies][2], to download or upload
translation files.

## What's the plan

Gtranslator has a GNOME 2.0 interface, with toolbar, menus, statusbar and
dockable widgets:

<p style="text-align: center" class="img">
    <a href="/static/pictures/gtranslator1.png">
        <img src="/static/pictures/gtranslator1.png" />
    </a>
</p>

But in the git repo, the main branch was *broken*. Someone starts a big
refactor, in 2015, to try to update the interface to look more like a modern
GNOME 3 application but that refactor never ended so the master branch compiles,
but doesn't do anything. There was a lot of widgets that was half ported to a
modern code.

There's also some [designs][3] to modernize the interface, but the work wasn't
finished.

My plan is to continue that work, modernize the UI, remove all *deprecated* code
and warnings and then continue the development from there.

I don't want to spend a lot of time reworking the whole app to have a new one in
two months, I want to have a functional app as soon as possible, and continue
with a continuous development, improving the UI and the functionality needed by
the translator team.

So the roadmap that I've in mind is:

  1. Fix the current master state
  1. Fix the known bugs
  1. Redesign the interface
  1. Enhance linking with Damned Lies

## What I've done in one week

I started updating the build system, from autotools to meson build, and then
I've added a flatpak manifest file, so now gnome-builder is able to build
Gtranslator using meson and flatpak and it's easier to develop this way.

This build tools modernization is great because with the new gitlab we've now
continuous integration, and that means that the gitlab compiles and generates a
flatpak bundle for each commit, making it easier for testers to test new
functionality or Merge Requests, you only need to download the .flatpak and
install locally, no need to build at all.

<p style="text-align: center" class="img">
    <a href="/static/pictures/gtranslator-gitlab.png">
        <img src="/static/pictures/gtranslator-gitlab.png" />
    </a>
</p>

Then I started to fix the master branch. There was a *project* selector view and
then you go to the translation view. There was only the .ui files and not
working yet, so I reworked that a bit and convert the *project* selector to a
*file* selector for now and then when you select a file, you've almost the same
old interface, but without the menu, toolbar and statusbar.

<p style="text-align: center" class="img">
    <a href="/static/pictures/gtranslator2.png">
        <img src="/static/pictures/gtranslator2.png" />
    </a>
</p>

I've been moving the toolbar icons to the headerbar so we can have the main
functionality working. We've now a functional application.

## Plugins

Gtranslator has a plugin system and has eight plugins, but that plugins was
disabled some time ago. So I've started to recover that functionality but
instead of as plugins, I've started to move the plugins to the core app code.

The only plugin ported currently is the translation memory. I'll take a look to
the other plugins and view if it's desirable to reimplement that or remove that
code.

## What's next

All the statusbar functionality is missing right now, I need to find some place
in the new UI to show that.

I wan't to start as soon as possible to work in a new widget to show messages,
instead of the current table.

The *project* selection part is a bit hard because I need to think about what's
a project in this context. Currently Gtranslator is a .po file editor, but if we
change that to manage *projects* like a group of .po files, I need to think
about how to store that information and the easier way for translator to use the
interface.

So if you've time and want to contribute in this project, go ahead, you can ask
in the #gtranslator IRC channel or talk to me directly. Currently there's no
a lot of issues in the gitlab, but as soon as I get a functional version in
gnome-nightly flatpak repo and some translators starts to use it, we'll have a
lot of things to do.

[1]: https://wiki.gnome.org/Apps/Gtranslator
[2]: https://l10n.gnome.org/
[3]: https://wiki.gnome.org/Design/Apps/Translator
