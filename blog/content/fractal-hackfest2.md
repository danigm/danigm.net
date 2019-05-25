Date: 2018-05-12
Title: Fractal Hackfest, Strasbourg (day 2)
Tags: gnome, rust, programming, fractal, wadobo
Category: blog
Slug: fractal-hackfest2
Gravatar: 8da96af78e0089d6d970bf3760b0e724

The second day of Fractal hackfest was really productive, we talk about a
lot of topics and takes some important decisions.

<center>
    <p class="img">
    <img src="/pictures/fractal-hackfest2.png" width="100%"/>
    </p>
</center>

## E2E Encryption

The encryption is a needed feature but encryption is hard to do in rooms.
Matrix uses public-key cryptography, for rooms they are using [Megolm][4],
that's a protocol to exchange encrypted messages with more than one and
share that message keys in a one-to-one secure communication.

I don't know a lot about this E2E because for me it's more important to
have the client working with a basic functionality before the encryption.
So you should read the official doc because maybe this that I'm writing
here is completely wrong.

To do all this E2E key sharing, client side encryption and communication,
Riot has three different implementations of the *same* lib, so they have
this code in the JavaScript SDK, the same ported to iOS version in
ObjectiveC and the same ported to Android in Java. Below this lib there's
the libolm that does the real encryption.

For the future it should be a good solution to have only one lib that does
the encryption thing, so we need to push in that direction and maybe
matrix.org and Purism can pay for that work to be done.

From Fractal, we've two options or wait until we've the official E2E
C/C++-lib or something, or try to port the iOS lib to Rust or C to use in
our codebase. I think that the best solution is the first one, in any case,
we'll need to wait some time to view E2E in Fractal.

## Calls

Calls are easy compared to the Encryption thing, the [protocol is well documented][5]
and it's really simple. The hard part here is that the call is implemented
using the webRTC and that is a web protocol... But it seems that there's
something done in this case with GStreamer working with webRTC.

## Multiple accounts

We was talking yesterday about the multiple accounts problem, if we want to
support and in that case what solution we should take.

We've two possible solutions, one is to support multiple accounts at the
same time and a way to change between accounts, and the other one is to
open a window for each account.

At the end we think that the best solution could be to open a separated
window for each account so if you've multiple accounts, at first you should
choose what account you want to open and then from the menu you can open a
new *window* and go to the account selection menu again.

We need to work in the design of this feature and it's not confirmed but I
think that this was the best solution, because it's simple and powerful.

## Communities

Communities are something really new in the Matrix.org protocol and it's
not well documented yet and there's some functionality that is not
implemented so we decide to wait until this functionality is more mature to
view how we can integrate this in Fractal.

Communities today are a group of rooms and a group of people and a full
html description to show in the community *page*. There's other features
like show a *label* for each member of the community or group, so I think
these features are cool. We'll need to support some parts of the
communities protocol soon.

## Google Summer of Code

<center>
    <p class="img">
    <img src="/pictures/fractal-hackfest1.png" width="100%" />
    </p>
</center>

As I said this year we've two students working on Fractal thanks to Google,
as part of the [GNOME organization][6], and both students comes to the
Hackfest so thank you Julian and Eisha for coming and for the work done
before the GSoC and for sure for the work you'll be doing during the
summer.

We're talking about how we'll be organizing, I'm the mentor of both but
we'll have the help from Tobias Bernard and from Alexandre Franke so we'll
have a summer hacking group to improve Fractal a lot.

We'll have a weekly meeting to talk about what we're doing and what to do
in the next week.

For this first week we'll start with two needed features. Julian will be
working in the user preference dialog and Eisha will start to work in the
internationalization (i18n) because it's not easy to use gettext in rust
and we want to translate the app to make it more accessible for everyone in
the world.

## Hacking a bit

In the meantime, between functionality discussion I was working in a way to
use Fractal without SecretService, so if you're using Fractal outside GNOME
or KDE you can configure it to store password and token in a plain text.
We shouldn't store passwords in a clear text file, but I think that this
will simplify the day for many people that wants to use Fractal but don't
want to write the user and password every time.

This is not finished yet, but we'll have this very soon, and with this it's
possible to implement other password & token storage services and make it
configurable, so maybe in the future someone implements the storage for
MacOS or something.

## Holidays

This was my last day in the hackfest, I've the travel back to Spain the
Sunday but I'll do some tourism here so I need to leave the people, they
will continue working the Saturday and the Sunday.

This have been the first Fractal hackfest and it was a great experience, to
meet other people working on it and to talk about the future of the
application. It's really cool that with less than a year project we've now
a big community, so thank you all form coming and see you on GUADEC.

There's a lot of work to do, but we're lucky because we're two students
working in Fractal this summer and the people from [Matrix.org][3] and
[Purism][2] are working with us, so thank you all.

I want to thank again the GNOME foundation and GNOME people for make this
possible and to my company [Wadobo][1], for let me spend some time working
on this great project.

<center>
    <a href="https://wadobo.com">
        <img src="/pictures/wadobo-mini.png" />
    </a>
</center>

[1]: https://wadobo.com
[2]: https://puri.sm/posts/librem5-progress-report-11/
[3]: https://matrix.org/blog/2018/05/11/this-week-in-matrix-2018-05-11/
[4]: https://git.matrix.org/git/olm/about/docs/megolm.rst
[5]: https://matrix.org/docs/spec/client_server/r0.3.0.html#voice-over-ip
[6]: https://summerofcode.withgoogle.com/organizations/5900447454330880/
