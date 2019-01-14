Date: 2019-01-13
Title: GNOME Outreachy mentorship
Tags: gnome, fractal, gtranslator, outreachy
Category: blog
Slug: gnome-outreachy-2018
Gravatar: 8da96af78e0089d6d970bf3760b0e724

The [Outreachy][1] program is a three month internship to work in FOSS. There
are two periods for the outreachy, the first one from December to March and
the other one from May to August. It's similar to the Google Summer Of Code,
but in this case the interns doesn't need to be students.

I proposed some ideas for interts to work on GNOME, with me as a mentor. I
wrote three proposals this time:

 * Extend [Fractal][6] media viewer with video support and explore video
   conference
 * Create [Gtranslator][5] initial integration with Damned Lies
 * [Books][4] : Improve the epub support in gnome-books

There was people interested in all of three projects, but for the Books app
we don't have any real contribution so there was no real applicants.

I've two good proposals for Fractal and for Gtranslator, so I approve both and
the Outreachy people approve these two interts. So we get two new devs working
in GNOME for three months as interns.

This is something great, paid developers working in my proposals is a good
thing, but this implies that I need to do the mentor work for these two interns
during the three months period, so it's more work for me :/

But I think this is a really important work to do to bring more people to the
free software, so I've less time for hacking, but I think it's good, because
the fresh blood can do the hacking and if, after the Outreachy, one of the
interns  continues collaborating with GNOME, that will be more important for
the GNOME project that some new features in one app.

### GNOME Translation Editor

[Teja][2] is the intern working in gtranslator. She is working in the
[Damned Lies][7] integration.

Damned Lies is a web application for GNOME translators. This app provides
updated `.po` file for each GNOME module and language and translators can
download and update that file using the web interface. That web is able to
do the commit to the original repository with the upload version from
translators.

The idea is to provide a simple integration with this platform in the
GNOME Translation Editor app, using the web json API to be able to open `.po`
files from the web directly without the need to download the file and then
open it.

The current API of DL is really simple so we can't implement a real integration
without adding more functionality to this API. So this project requires some
work in the DL app too.

In the future we can improve the integration adding the posibility to upload
the new `.po` after saving to DL so translators doesn't need to go to the
web interface and can do all the translation flow using only the Translation
Editor.

### Fractal

[Maira][3] is the intern working in Fractal. They are working in the initial
video preview widget.

Fractal is a instant messaging app that works over matrix.org. Currently we
support different types of messages, like text, images, audio and files. But
for video we're using the same widget as we're using for files, so you can
download or open, but we've not a preview or inline player.

The main idea of this project is to provide a simple video player using
gstreamer to play the video inside the Fractal app.

This is not an easy task, because we're using Rust in Fractal and we need to
deal with bindings and language stuff, but I think it's doable.

During the internship, Maira is also working fixing some bugs in the audio
player, becuase it uses gstreamer too, so during the code review, Maira
detected some problems and they are fixing it.

[1]: https://www.outreachy.org/
[2]: https://teja.cetinski.eu/blog
[3]: https://mairandom.space/

[4]: https://www.outreachy.org/communities/cfp/gnome/project/books-improve-the-epub-support-in-gnome-books/
[5]: https://www.outreachy.org/communities/cfp/gnome/project/create-gtranslator-initial-integration-with-damned/
[6]: https://www.outreachy.org/communities/cfp/gnome/project/extend-fractal-media-viewer-with-video-support-and/

[7]: https://l10n.gnome.org/
