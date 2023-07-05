Date: 2021-12-11
Title: Loop: A simple music application
Tags: gnome, software, music, loop
Slug: loop
Gravatar: 8da96af78e0089d6d970bf3760b0e724
Category: blog

In the last year I've seen some [really good musician][1] that performs all
the instruments in a song with just a loop machine, recording each instrument
one by one in tracks and looping.

I was thinking that it should be easy to have a desktop application that does
exactly the same, just some tracks to record some sounds and the playback with
a loop option, and that's what I created during this week.

<p class="img">
    <img src="/pictures/loop.png" />
</p>

The [Loop application][2] is just a simple Gtk4 application that uses gstreamer
to record tracks and then you can play each one at the same with or without
loop option. With that, a good musician could create the base melody of the
song and then sign on top of that. Unfortunately, I'm not a good musician, but
I can use this to play around.

I've just created the [request on flathub][3] to add the application, so if
everything is okay it will be available there soon, so more people can play
with this awesome toy.

Right now it has the basic record, play and loop functionality with just four
tracks, so don't expect to have a professional music app (yet). The recording
and play times are not perfect and there's a delay, that's a known issue, but
I'm planning to fix this issue and add more functionality in the future, like:

 * Make number of tracks configurable
 * Import track from files
 * Add a trim slider per track, to be able to adjust the recorder track to loop
 * Metronome tick and clock to have a visual reference for recording tracks
 * A record button, but export the combination of all tracks and mic to a mp3
   file

And that's all. The logo and design is an initial version done by myself, so if
any designer wants to take a look, all contributions are welcome. And of course
any code contribution is also welcome.

If you use this application and do some good or fun performance, please, ping
me on social networks and let me know.

[1]: https://www.twitch.tv/leonbratt
[2]: https://gitlab.gnome.org/danigm/loop/
[3]: https://github.com/flathub/flathub/pull/2674
