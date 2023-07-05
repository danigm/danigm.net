Date: 2021-11-15
Title: Endless Orange Week: Hack content creators platform (2)
Tags: hack, endless, orangeweek, work, gnome, software
Slug: hack-content-creators-1
Gravatar: 8da96af78e0089d6d970bf3760b0e724
Category: blog

The past Friday was the last day of the [Endless Orange Week][1]. It was a nice
and fun experience, and even if I was not able to do as much as I wanted, we
were able to make something that "works" in the Hack project.

## The Hack Quest editor

<p class="img">
    <img src="/pictures/clubhouse-custom-quests-1.png" />
</p>

The first step to have custom quests on the Hack app was to complete the
[Ink language][2] support. We started to work on this some time ago, but never
completed the functionality.

I worked on that the first three days, updating the ink library and building
the missing pieces to be able to load quests from random paths. I've
implemented that in a way that the Hack application is able to receive a path
to a `.ink` file, and it's able to build and run the quets.

The Quests are not just the script, but they have some metadata, like title,
subtitle, description, difficulty and the card image to show on the interface.
To solve that I defined a "custom quest bundle format", that's bassically a
folder with:

 * questId
   * quest.jpg
   * metadata.json
   * quest.ink

So I also added the functionality to import a bundle zip file and export with
the quest information.

<p class="img">
    <img src="/pictures/clubhouse-custom-quests-2.png" />
</p>

I created some command line options to use this new functionality:

```
  --play-ink=FULL_INK_FILE_PATH                 Start a custom ink quest.
  --import-quest=PATH_TO_BUNDLE_OR_INK_FILE     Import a custom ink quest.
  --export-quest=CUSTOM_QUEST_ID                Export a custom quest bundle.
```

### Quest creation interface and the Inky Editor

The first idea was to try to provide a full quest creation experience in the
app, but that was too much, so we decided to simplify the way to create quests
and depend on the [Inky editor][3] external tool. Manuel Quiñones took some time
to update the flatpak application with the latests ink version, so we can use
to create custom quests.

The Inky editor provides help about the language, syntax highlighting and a
simple way to test the script, so it's a nice tool. The main problem with this
tool is that it doesn't provide a way to launch it with a file path so it's
not possible to integrate with the Hack app.

<p class="img">
    <img src="/pictures/clubhouse-custom-quests-3.png" />
</p>

So at the end, the Quest creation dialog is just a way to define the metadata
and to select the Quest ink files from your filesystem. How the ink script is
created is a decision to make for the content creator.

### The future

We've no time to complete all we wanted to do, and I didn't create a new
release, so this new functionality is still not there. But we'll try to do a
release soon.

Simon is working on some interface improvements and also on a new tutorial
Quest, so we can introduce the Custom Quest creation tool in the same app.

## The Character editor

The other part of this week planning was the character editor. Joana did a
really nice work designing the application, the initial assets and the user
experience, but I had not too much time to work on the implementation.  So I
spent just one day working on this.

The main idea was to create a new independent app, and then provide a way to
integrate with the Hack application and the custom Quest creation dialog. And
it'll be a simple application so maybe it could be useful or interesting for
other people, it's a fun way to play around and create random faces.

<p class="img">
    <img src="/pictures/avatar-creator-1.png" />
</p>

We just created the application [Avatar Creator][4]. I created a simple python
Gtk4 application and worked a bit on the basic functionality. So right now it
loads a list of svg assets and provide the 3x3 grid. You can click on a grid
cell and then choose what basic image should go there.

<p class="img">
    <img src="/pictures/avatar-creator-2.png" />
</p>

I added the initial set of basic images, created by Joana, to create this funny
robot faces, but the format is simple enough to extend with different "avatar
libraries" in the future.

Right now it's also possible to export to png, so the app is functional, but it
needs a bit more work.

My idea is to work a bit more in the following weeks, when I have some time, on
weekends or holidays and at some point, publish it in flathub. And lets see if
there are more developers interested on this app so it can grow.

The application is simple enough to be a good place for GNOME newcomers and it's
also a fun project to work on. A simple toy app to create faces that could
have some potential, some future ideas:

 * "Smart" random faces generator
 * Configurable grid: Maybe is interesting to make it bigger or smaller to play
   around
 * Programmed simple base image manipulations, like rotation, mirror, color
 * Animation creation, maybe be able to export to gif

## The Endless Orange Week experience

This week was a really nice experience, because we were working in a "personal"
chosen project, that we liked and without the day to day meetings, times
schedules and other related work stuff.

But that was not all. In Endless we've different teams that work mostly
isolated, because we're working on different fields, we've some overlapping,
but we work day to day as small teams, and this week we were all using the same
slack channel to show our progress, and it was nice.

Maybe now that we're not a big organization with a lot of workers, we can do
something like this more often, it's always good to know more about other
coworkers and to learn something that maybe it's not related with your main
project, but it could be interesting.

I'm really happy that we did this Endless Orange Week, it's sad that it ended
too soon, I'm waiting to learn from my coworkers what amazing things they do
during this week and I'm looking forward the next year Orange Week!

[1]: http://danigm.net/hack-content-creators.html
[2]: https://www.inklestudios.com/ink/
[3]: https://flathub.org/apps/details/com.inklestudios.Inky
[4]: https://github.com/endlessm/avatar-creator/
