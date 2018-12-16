Date: 2018-12-16
Title: Fractal December'18 Hackfest (part 2)
Tags: gnome, fractal, hackfest, wadobo, seville
Category: blog
Slug: fractal-december-18-hackfest-2
Gravatar: 8da96af78e0089d6d970bf3760b0e724

The Friday 14th was the last day of the [second Fractal Hackfest][4]. I've not
spend much time writing real code, the Thursday was mainly another hacking day
and I've been able to continue with the **fractal-backend** creation, but
there's a lot of work to do there.

But the hackfest was really productive, we've talked about big issues, project
management, some design ideas, new functionalities, the application refactor,
etc.

<center>
    <p class="img">
    <img src="/static/pictures/fractal-seville-hackfest-2.jpg" width="100%"/>
    </p>
</center>

### GNOME newcomers experience

We talked about how to improve the GNOME newcomers experience and how to
improve the main view of Fractal. I think that Tobias will talk more about this,
he was working in some cool design for this and I think we can start to
implement this new views soon.

### Best practices

We've been developing Fractal in a fast way, without spend a lot of time
thinking about the code quality, maintainability and that stuff. Recently we've
set the **rustfmt** linter in the CI pipeline and we've some tests, but the
Merge Requests process wasn't defined and for example I was pushing directly
to master.

To improve the quality of Fractal we've started a new wiki page to have a list
of [best practices][7] to follow. There we'll add some guidances on how we
should write code and the processes to follow to improve Fractal.

We've decided that we should be more strict with the Merge Request code review
and now, direct push to master is not allowed, all changes will go through the
review process. We should wait at least two days to merge something and have
at least two people that approve the change.

This will slow down the MR process, but will improve the code quality and
will reduce regressions. Any help is welcome, if you're able to test the MR,
you can leave a comment and other reviewers will have more confident in the
change.

We're also working in the code quality using the cargo clippy tool. There's a 
Merge Request waiting for review, so we'll have a better rust source code soon.

### Fractal is now in the GNOME group

The [Fractal][6] project was on the **World** group inside the GNOME gitlab.
Fractal is a GNOME application, the most active developers are GNOME developers
and we try to follow the GNOME Human Interface Guidelines.

Fractal is one of the first new applications that born just during the gitlab
migration so we go through a new process. At first Fractal was in my personal
gitlab under **/danigm/fractal** then we move to the World group under
**/World/fractal** and finally we're in the main GNOME group **/GNOME/fractal**.

### New release 4.0.0

The last release was the 3.30.0, more than three months has passed since this
release and we've a lot of changes so we want to provide a new stable release.

We discuss a bit about the [version number][8] that we should follow and we
decided that we should do use our own version number system, because we want
to release as much as possible, when we've important changes.

We're working in the [4.0.0][9] release, we're stabilizing and fixing important
bugs before the release and maybe we can have the new release during the next
week.

So I've spend the last day looking for bugs and preparing the new release.

### Matrix Live

We've a meeting with the people from Matrix.org to talk about Fractal and the
hackfest. You can view the full interview in youtube:

<iframe width="560" height="315" src="https://www.youtube.com/embed/SgyLHi8zZXQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Friday sponsored lunch

We've a sponsored lunch the Friday 14th, the local group [Plan4D][3] invite
us to a great lunch in the city center.

<a href="http://www.plan4d.eu/"><center>
    <p class="img">
    <img src="/static/pictures/plan4d.jpg"/>
    </p>
</center></a>

After that, I goes back to my home and leave the other people there in Seville
doing some tourism, I've to go back to Málaga.

The hackfest was great and we have done a lot of things. This was the second
Fractal hackfest in 2018, and we meet at the GUADEC too. We've had two GSoC
students and now we've another intern thanks to the outreachy program. There's
a lot of people contributing to Fractal and that's great.

**GNOME is a great community** and I think that Matrix.org and Rust are helping
to this project a lot. The Matrix.org people are supporting us, indeed, Matthew
comes to the first hackfest and I think that the success of Fractal and the
community behind has a lot to thank to the Rust language and to the people
working in the Rust + GNOME integration, Gtk-rs is a great project.

I want to apologize about the network problem during the hackfest. We've been
working all days thank to Julian network sharing, with eduroam, because we
aren't able to have guest access in the university.

The university has a strict internet connection filtering, so only a professor
can ask for a guest connection for events and we do the request too late.

[1]: https://gnome.org
[2]: https://wadobo.com
[3]: https://www.plan4d.eu
[4]: https://wiki.gnome.org/Hackfests/FractalDecember2018
[5]: https://sugus.eii.us.es/
[6]: https://gitlab.gnome.org/GNOME/fractal/
[7]: https://gitlab.gnome.org/GNOME/fractal/wikis/Best-practices-for-Fractal-development
[8]: https://gitlab.gnome.org/GNOME/fractal/issues/350
[9]: https://gitlab.gnome.org/GNOME/fractal/issues/396
