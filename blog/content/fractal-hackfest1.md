Date: 2018-05-11
Title: Fractal Hackfest, Strasbourg (day 1)
Tags: gnome, rust, programming, fractal, wadobo
Category: blog
Slug: fractal-hackfest1
Gravatar: 8da96af78e0089d6d970bf3760b0e724

Yesterday was the first day in the first [Fractal Hackfest][1]. I'll try to
write an small blog post every day to share the development with the world.

My travel to Strasbourg was not an easy travel because I've to take two
flights to get here from Málaga so a long day travelling.

I met with Mathew from Matrix.org at the London airport because we took the
same flight to here and it was really cool to meet him in person and we
talk a little about the current Matrix situation.

I've met the other Fractal people and collaborators at the event, and it's
great that people from Purism, Matrix, Gnome and the two GSoC students come
here to work together in this great application.

## Barbecue and Banquet

We've spend almost all the day talking about the different uses cases for
the messaging problem and Tobias has come with a proposal for split the
current application in two because the use case is totally different.

We've the first case when you use the app to talk to family, friends and
small groups of people where all conversations are private and you want to
read almost every message there, we call that situation the "Barbecue".

The second case is the one where you use the messaging app to talk in a
public or private room with a lot of people, where you are receiving a lot
of messages but you don't want to follow the full conversation you'll talk
with someone or read a topic conversation, we call this one the "Banquet".

Currently Matrix clients are more oriented to the Banquet use case so
there's a lot of people and communities using it for this. The idea behind
this split is to provide two apps to the user to make both cases possible.

We need to work on this idea but it seems that is the correct way to go.

## Initial Syn speed up

At the afternoon. We've reviewing the current initial sync filter and
detect some points to speedup.

I changed the filter and the initial sync goes a lot faster. I've removed
the member events from the initial sync so there's a lot of less
information to retrieve from the server.

This little change breaks the one to one room name and default avatars
because that name is calculated using the members in the room so I need to
fix that making the name calculation a backend process. So now if a room
has no name, We'll ask for the room member list and when we've that we'll
calculate the room name with the same algorithm, if there're only two
people, we'll use the other person username, if there's three people we'll
use "one and another" and if there're more we'll use "one and others".

## Gnome dinner

We've a good dinner sponsored by the gnome foundation. Thank you so much.

[1]: https://wiki.gnome.org/Hackfests/Fractal2018
