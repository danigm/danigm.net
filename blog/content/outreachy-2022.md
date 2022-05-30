Date: 2022-05-30
Title: GNOME Outreachy 2022
Tags: gnome, outreachy, gtranslator, gtk4
Category: blog
Slug: outreachy-2022
Gravatar: 8da96af78e0089d6d970bf3760b0e724

## GNOME Translation Editor, Road to Gtk4

It's time to move to Gtk4. That could be an easy task for new project or for
small projects without a lot of custom widgets, but [gtranslator][1] is old and
the migration will require some time.

Some time ago I did the [Gtk2 to Gtk3][2] migration. It was fun and during the
journey we redesigned a bit the interface, but the internals didn't change a
lot. Now we can do the same, migrate to Gtk4 and also update the User
Interface.

Thankfully, I'm not alone this time, the GNOME community is there to help. A
couple of months ago, [Maximiliano][3] started a series of commits to prepare
the project to the Gtk4 migration, and today starts the Outreachy program and
we've a great intern to work in this. [Afshan Ahmed Khan][4] will be working
during this summer in the GNOME Translation Editor migration to Gtk4.

## Outreachy

The [Outreachy][5] program provides internship to work in Free and Open Source
Software. This year I've proposed the "Migrate GNOME Translation Editor to Gtk4"
project and we had a lot of applicants. We had some great contributions during
the application phase, and at the end Afshan was selected.

We've now an initial [intern blog post][6] and he is working now in the first
step, trying to build the project with Gtk4. It's not a simple task, because
gtranslator uses a lot of inheritance and there's a lot of widgets in the
project.

## User Interface redesign?

Once we've the project working with Gtk4 and libadwaita we can start to think
about user interface improvements, and all the collaboration here is welcome,
so if some designer or translator want to help, don't hesitate to take a look
to the [current interface][7] and propose some ideas in the [corresponding task][8]

[1]: https://gitlab.gnome.org/GNOME/gtranslator
[2]: https://danigm.net/gtranslator-resurrection.html
[3]: https://gitlab.gnome.org/GNOME/gtranslator/-/commits/master?author=msandova
[4]: https://www.outreachy.org/alums/2022-05/
[5]: https://www.outreachy.org/
[6]: https://dev.to/redoca2k/beginning-outreachy-journey-with-gnome-o8j
[7]: https://flathub.org/apps/details/org.gnome.Gtranslator
[8]: https://gitlab.gnome.org/GNOME/gtranslator/-/issues/159
