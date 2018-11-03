Date: 2018-11-03
Title: GNOME Translation Editor 3.30.0
Tags: gnome, gtranslator
Category: blog
Slug: gnome-translation-editor
Gravatar: 8da96af78e0089d6d970bf3760b0e724

I'm pleased to announce the new [**GNOME Translation Editor**][1] Release.
This is the new release of the well known **Gtranslator**. I talked about
the [**Gtranslator Ressurection**][2] some time ago and this is the result:

<p style="text-align: center" class="img">
    <a href="/static/pictures/gtranslator3.30.png">
        <img src="/static/pictures/gtranslator3.30.png" />
    </a>
</p>

This new release isn't yet in flathub, but [I'm working on it][11] so we'll
have a flatpak version really soon. Meantime you can test using the gnome
nightly flatpak repo.

## New release 3.30.0

This release doesn't add new functionality. The main change is in the code,
and in the interface.

<p style="text-align: center" class="img">
    <a href="/static/pictures/gtranslator1.png">
        <img src="/static/pictures/gtranslator1.png" />
    </a>
</p>

We've removed the toolbar and move the main useful buttons to the headerbar.
We've also removed the statusbar and replaced it with a new widget that shows
the document translation progress.

The plugin system and the dockable window system has been removed to simplify
the code and make the project more maintenable. The only plugin that is
maintained for now is the translation memory, that's now integrated. I'm
planning to migrate other useful plugins, but that's for the future.

Other minor changes that we've made are in the message table, we've removed
some columns and now we only show two, the original message and the translated
one and we use colors and text styles to show fuzzy status and untranslated.

The main work is a full code modernization, now we use meson to build, we've
flatpak integration and this simplify the development because gtranslator know
works by default in Gnome Builder without the need to install development
dependencies.

There's others minor changes like the new look when you open the app without
any file:

<p style="text-align: center" class="img">
    <a href="/static/pictures/gtranslator-open.png">
        <img src="/static/pictures/gtranslator-open.png" />
    </a>
</p>

Or the new language selector that autofill all the profile fields using the
language:

<p style="text-align: center" class="img">
    <a href="/static/pictures/gtranslator-lang.png">
        <img src="/static/pictures/gtranslator-lang.png" />
    </a>
</p>

And for sure we've tried to fix most important bugs:

 * [Search and replace deletes all fuzzy states][3]
 * [Check files before the save][4]
 * [msgctxt should make strings different][5]
 * [Some headers get line breaks and don't follow the right format][6]
 * [And more][7]

## New name and new Icon

<p style="text-align: center" class="img">
    <a href="/static/pictures/gtranslator-icon.png">
        <img src="/static/pictures/gtranslator-icon.png" />
    </a>
</p>

Following the modern GNOME app names, we've renamed the app from Gtranslator
to **GNOME Translation Editor**. Internally we'll continue with the gtranslator
name, so the app is gtranslator, but for the final user the name will be
**Translation Editor**.

And following the [App Icon Redesign Initiative][8] we've a new icon that
follows the new [HIG][9].

## Thanks

I'm not doing this alone. I became the gtranslator maintainer because Daniel
Mustieles push to have a modern tool for GNOME translators, done with gnome
technology and fully functional.

The **GNOME Translation Editor** is a project done by the GNOME community, there
are other people helping with code, documentation, testing, design ideas and
much more and any help is always welcome. If you're insterested, don't hesitate
and come to the [gnome gitlab][10] and collaborate with this great project.

And maybe it's a bit late, but I've publish a project to the [outreachy.org][12],
so maybe someone can work on this as an intern for three months. I'll try to
get more people involved here using following outreachy and maybe GSoC, so if
you're a student, now is the right time to start contributing to be able to be
selected for the next year internship programs.

[1]: https://download.gnome.org/sources/gtranslator/3.30/
[2]: http://danigm.net/gtranslator-resurrection.html
[3]: https://gitlab.gnome.org/GNOME/gtranslator/issues/1
[4]: https://gitlab.gnome.org/GNOME/gtranslator/issues/5
[5]: https://gitlab.gnome.org/GNOME/gtranslator/issues/19
[6]: https://gitlab.gnome.org/GNOME/gtranslator/issues/8
[7]: https://gitlab.gnome.org/GNOME/gtranslator/issues?scope=all&utf8=%E2%9C%93&state=closed
[8]: https://gitlab.gnome.org/GNOME/Initiatives/issues/2
[9]: https://developer.gnome.org/hig/stable/icon-design.html.en
[10]: https://gitlab.gnome.org/GNOME/gtranslator
[12]: https://www.outreachy.org/apply/project-selection/
[11]: https://github.com/flathub/org.gnome.Gtranslator/pull/4
