Date: 2022-07-09
Title: Gambito, a chess App in Rust
Tags: gambito, chess, gtk4, gnome, rust, twitch
Category: blog
Slug: gambito
Gravatar: 8da96af78e0089d6d970bf3760b0e724

## Chess

I've been always interested in Chess, but never learned to play it correctly or
even spent some time playing more than a couple of matches with friends. But
during the COVID lockdown I started to watch people [playing chess][1], and
then I realized that the game is even more fun than I expected.

After that I started to play a bit online and discovered the great online
platform [Lichess][2], that's even [free software][3]. I do not play a lot, but
I discovered that I like a lot the game and I watch chess streamers everyday
and I even followed the [professional competition][4].

So if you don't play chess, give it a try, it's a really nice board game, and a
beauty "video game" that you can play online in a complete free software platform
with a lot of community resources to learn, and even if you are a bad player like me,
you can always enjoy the beauty of the chess watching other people playing.

## Gambito

With this new interesting hobby, I installed the chess application that I found
in gnome. [GNOME Chess][5] is a good application, but then I ask myself, why
not rewrite it in Rust? Okay, it's not a rewrite, it's just a new application,
my idea is not to replace GNOME Chess, but to experiment with Gtk4 and Rust,
and that's the reason I started to work on [Gambito][6], that's just a new
Chess game for GNOME, written in Rust with Gtk4.

<p class="img">
    <img src="/pictures/gambito-screenshot01.png" />
</p>

The first idea was to create a simple app, without widget inheritance or
anything, just draw a board with existing Gtk Widgets, and do the drawing with
CSS and the interaction with drag & drop. And I did that for almost all the
application, but at some point I needed something more specific that I was
unable to do without a new widget. So right now almost everything is done that
way but the marks and arrows, that are custom widgets.

I'm doing almost all the development in live streaming (in Spanish),
[in my twitch account][7], so you can find some of the videos here in my
[youtube channel][8].

<p class="img">
    <img src="/pictures/gambito-screenshot03.png" />
</p>

Right now you can use the application to play against Stockfish or to analyse a
match. At the beginning the idea was to create just a chess game, but right now
I'm thinking more about a chess learning application, so I think I'll work more
in analysis tools, tactic training games, and maybe some good content for
beginners, inside the application, like a tutorial and some kind of assistant with
theory.

And there's a lot of fun things to do, like linking with the Lichess platform,
to be able to watch games in live, play online using the app instead the web
interface, analyze Lichess matches and look for cheaters doing some kind of IA
(yes, there are cheaters using chess engines to win matches in online chess
platforms, I don't know why, but there are people like that).

So I'm getting a lot of fun from the old game Chess, fun playing, fun watching
an fun writing a Chess game.

Have fun!

<p class="img">
    <img src="/pictures/gambito-logo.png" />
</p>

[1]: https://www.twitch.tv/gmhikaru
[2]: https://lichess.org/
[3]: https://github.com/lichess-org
[4]: https://fide.com/
[5]: https://gitlab.gnome.org/GNOME/gnome-chess
[6]: https://gitlab.gnome.org/danigm/gambito
[7]: https://www.twitch.tv/abentogil/
[8]: https://www.youtube.com/c/danigmx/search?query=gambito
