Date: 2018-12-12
Title: Fractal December'18 Hackfest (part 1)
Tags: gnome, fractal, hackfest, wadobo, seville
Category: blog
Slug: fractal-december-18-hackfest-1
Gravatar: 8da96af78e0089d6d970bf3760b0e724

## First two days of work

The Tuesday 11th started the [second Fractal Hackfest][4]. I've organized this
hackfest in Seville, the city where I studied computer science and here I've a
lot of friends in the University so is a good place to do it here.

The weather was important too for the hackfest selection, in December
Seville is a good choice because the weather is not too cold, we're having
sunny days.

The first day was a good day, thinking about some relevant issues and planning
what we want to do. We talked about the work needed for the interface split,
about the E2EE support, new features and the need for a new release.

We're having some problems with the internet connection, because the University
has a restricted network policy and we ask for the guess internet connection
the Monday, but we're still waiting.

Meantime we have to thanks to Julian Sparber the hackfest wifi, because
he's using his laptop to stream the eduroam connection.

## Newcomers

The first day we try to promote as a newcomers day, and some people comes.
We've some contributions and I spend some time trying to help people to
introduce to the GNOME community.

## GNOME Foundation sponsored dinner

The [GNOME Foundation][1] payed for a Fractal dev day dinner, so we should
thanks this great dinner to GNOME:

<center>
    <p class="img">
    <img src="/pictures/fractal-seville-hackfest-dinner.jpg" width="100%"/>
    </p>
</center>

We've a good time eating and drinking in the *Coco Verde*. We talk about GNOME,
the desktop, matrix.org and other communication tools.

# Hacking day

Today was a hacking day, so we started to work in the stuff that we talk about
yesterday. We've resolved some minor issues and I started with the
**fractal-backend** crate.

<center>
    <p class="img">
    <img src="/pictures/fractal-seville-hackfest-computer.jpg" width="100%"/>
    </p>
</center>

We talked about move all the app data model and logic to the **fractal-backend**
and leave **fractal-gtk** only as UI management.

We talked about the **LMDB** use to store rooms and messages and we decided
that the best solution should be to use a relational database, because we've
relations and with the key-value thing we'll end creating those relations and
maintaining by hand. In any case, I've this decision in mind and I'm
implementing all this with a trait to hide the storage detail so we can change
easily in the future.

So today I've spend a lot of time implementing this trait and a first
implementation for the **Room** struct. I've decided to use **rusqlite** instead
the **diesel** orm because I want to keep it simple.

I want to finish all the database storage and move the AppOp main loop to the
**fractal-backend** and try to update the **fractal-gtk** to use the backend
instead the AppOp struct to get the rooms and messages. But maybe is a lot of
work, I don't know if I'll be able to finish this before the end of the
hackfest.

<center>
    <p class="img">
    <img src="/pictures/fractal-seville-hackfest-julian.jpg" width="100%"/>
    </p>
</center>

## Thanks

This hackfest is possible because there's a lot of volunteer work and people
helping us. First of all, the Fractal core team that comes *Tobias Bernard*,
*Julian Sparber* and *Alexandre Franke* and of course the *GNOME Foundation*.
And also we've to thank *Alejandro Domínguez*, a newcomer that is doing a really
good job fixing bugs and cleaning some old code.

Then I want to thank the [Linux local group, SUGUS][5] for the help and also
I want to thank to other free software related group [Plan4D][3].

<a href="http://www.plan4d.eu/"><center>
    <p class="img">
    <img src="/pictures/plan4d.jpg"/>
    </p>
</center></a>

Plan4D is giving us some help with the place and cookies, fruits, juices and
some tea.

And finally I want to thank again to my coworkers in [wadobo][2] because they
support me to spend a full work week working in gnome and they also spend some
time helping us to organize all the hackfest stuff.

[1]: https://gnome.org
[2]: https://wadobo.com
[3]: https://www.plan4d.eu
[4]: https://wiki.gnome.org/Hackfests/FractalDecember2018
[5]: https://sugus.eii.us.es/
