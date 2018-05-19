Date: 2018-05-19
Title: Stickers in Riot
Tags: gnome, rust, programming, fractal
Category: blog
Slug: stickers-in-riot
Gravatar: 8da96af78e0089d6d970bf3760b0e724

Yesterday I read a [blog post][1] about the new Riot.im Stickers. This is
not a matrix.org feature, it's implemented as a widget, when you send an
sticker you're sending a new event with the type "m.sticker", which is
similar to the "m.image" event.

<center>
    <p class="img">
    <img src="/static/pictures/stickers.gif" width="100%"/>
    </p>
</center>

The matrix.org protocol is flexible so this is a good example of how to add
new features to the clients that uses matrix without the need to change the
protocol.

This is not a core feature because you can send images, but I think this is
great and add a simple way to show reactions for the users, so as I was
reading I thought that we can add this to [Fractal][2], so I started to
read how we can add support for this.

## Reading the doc

The first thing to implement a feature is to read the specifications or the
technical documentation so we can know what is needed... But there's no
[documentation yet about Stickers or widgets yet][3].

This is a problem because we can't implement a feature if we don't know
what we should do. But free software give us a great opportunity when this
happens, we've the [Riot][4] source code so we can look at the code and
learn what they are doing.

## Reading the code

Riot web is a javascript application that uses AJAX to communicate with
different server APIs so the first thing that I did to start to understand
the stickers thing was to open the firefox debugger and view how riot is
communicating with the server.

From here I've learned that for stickers riot is asking to the
scalar.vector.im server. But I don't understand the whole thing with the
requests because riot does a lot of request to different APIs and I can't
isolate the stickers thing easily.

To fill my understanding gap I go to the [matrix-js-sdk][5] and
[matrix-react-sdk][6] and I did a quick grep to the source code looking for
the API calls that I've view in firefox. With this I can understand the
full stickers process.

## Writing an example

To say that I know how this is working, it's not enough the code reading.
To make sure that I've understood the whole process I need to write a
simple program that does all the process and then I can say that I
understand this.

So I started to write a [simple python script][7] using requests. This
simple script does the request to the server and list all the stickers json
so I can say that I'm able to communicate with the API.

## Stickers in Fractal

After this small research I'm able to implement an initial sticker support
for Fractal. I'll try to add a simple way to show and use stickers and a
way to render stickers in the messages history.

If there's no secret problems we'll have a basic stickers support in
Fractal soon.

[1]: https://medium.com/@RiotChat/stickers-are-here-introducing-riot-im-0-15-for-web-desktop-284c32b93acc
[2]: https://wiki.gnome.org/Apps/Fractal
[3]: https://github.com/matrix-org/matrix-doc/issues/1236
[4]: https://github.com/vector-im/riot-web
[5]: https://github.com/matrix-org/matrix-js-sdk
[6]: https://github.com/matrix-org/matrix-react-sdk
[7]: https://github.com/danigm/matrix-stickers-example
