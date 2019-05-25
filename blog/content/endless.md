Date: 2019-02-17
Title: I'm a hacker
Tags: gnome, work, endless, hack
Category: blog
Slug: endless
Gravatar: 8da96af78e0089d6d970bf3760b0e724

## I've the strength of the one that fails, trains and returns

Some time ago I wrote [about my interview process][3] trying to get a job at
GNOME. After this blog post was published in the GNOME planet, I received a lot
of comments from the *Great* GNOME community.

This guided me to take a look to the companies that was looking for GNOME
developers and after some interviews I finally get an offer to work on
[Endless][1].

All the process was online, I've been working from home since 2011 and I want
to continue like this. I'm living in Málaga, the south of Spain and I was
looking for a remote job.

I've a very nice interview process, talking with developers that I knew about
from their contributions to free software and these interviews weren't
technical, that's a good thing about the free software contribution and
the community, if someone wants to know my technical skills, he only need to
look to my gitlab or github and he will find a lot of code. These interviews
were personal and with some management questions, to know if I'll fit in the
team and the company.

I did the interview to work directly on the Endless OS, in the desktop team,
but after some interviews I ended in other team, working with the Endless OS
and all GNOME technology, but in the [Hack Computer][2].

## The hack computer

The hack computer is an educational project. The main idea is to provide a
fully functional computer for kids to be their first personal computer and also
provide a way to teach kids to *hack*.

The computer is a usual laptop, with an Endless OS running, and with some extra
applications that try to guide kids to explore, modify and finally hack the
computer learning in the process about GNU/Linux, the code and that any part
of your software can be hacked to make it better, an introduction to the
free software and the great world of open source code that you can modify to
learn, play or simply because you can.

<iframe width="560" height="315" src="https://www.youtube.com/embed/SN7tC4XnGko" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

The way to guide kids to learn is like a video game, with characters that will
appears in your desktop and will guide you with tips and challenges and after
each quest completed the kid will learn something, playing with his computer.

If you like this and want to collaborate, [we're hiring][4].

## Endless OS

The hack computer is built on top of the Endless OS. Endless OS is based on
debian and the desktop is a modified gnome shell, but it's not the usual debian
derivative, it's based on [OSTree][5]. The main difference is that the root
filesystem is read only and updates are managed with ostree, that's like a git
repository.

This kind of Operating System is easier to maintain, because the user *can't*
modify the base system, so this means that he was unable to *break it*. All user
applications are installed via flatpak, so are *independent* of the *OS*
version and because of flathub you can install latests version of apps without
the need to update the full operating system.

This is the way that [Fedora SilverBlue][6] is trying to follow and is a *new*
way to build and distribute GNU/Linux.

<p class="img">
    <a href="/pictures/hack-mount-tree.png">
        <img src="/pictures/hack-mount-tree.png" />
    </a>
</p>

## The end of an Era

I've been working in [Wadobo][7] since 2011. I created that company with two
college friends to try to continue hacking like we were hacking in the Seville
LUG [SUGUS][8] and earn money from that, and we did it for a long time.

<p class="img">
  <img src="/pictures/wadobo-old-2.jpg" />
</p>

We've been working in free software projects and with free software technology,
contributing to the community as much as we can and always trying to free our
work.

<p class="img">
  <img src="/pictures/wadobo-old-1.jpg" />
</p>

We created some projects that grow up and follow its own path, like the
agora voting system, that Edulix (Eduardo Robles) converts in [nvotes][9].

The self employment was a really good experience. I've been doing was I want
for a long time, taking time to contribute to GNOME and other projects when
I need it, because I was the one deciding what I want to do. But in the other
hand, I've been stuck in the local consultancy market for a long time.

<p class="img">
  <img src="/pictures/wadobo-old-3.jpg" />
</p>

I'm not a business man, I'm a developer and I'm based in Spain, where there
is no money inverted in innovation or we was unable to find that money, so we
were doing django web apps for a living and spending some time in our interests
in the extra time we've. So when I found the possibility to work full time in
an innovative project, I've no choice.

We'll try to continue with the **Wadobo** idea, like a group of people
interested in free software and new technologies, maybe this will derive into
a Linux User Group or maybe in the future someone takes the initiative and
build a business around this again.

<p class="img">
  <img src="/pictures/wadobo-old-4.jpg" />
</p>

## Hacking

I'm really happy with this change. Endless OS and the hack computer are really
great projects with a lot of bleeding edge technology and a really great group
of people, and I'm really exited to be able to work with people all around the
world in a project with a global vision.

I don't want to leave the roots I've here with my Wadobo friends and the local
community and local technology ecosystem. This is also related with the Endless
vision. Spain, and here in the south, in Andalucía, we've a technological
breach that we try to fill with free software.

I'll continue working with the Seville University, because they give me a lot
and I think it's a talent pool, we only need to guide those students to the
GNOME community or to other free software communities out there, to *save*
their souls from the privative software and the dark side.

I'll continue supporting initiatives like the [Free Software Contest][10]

<p class="img">
  <a href="http://concursosoftwarelibre.org/">
    <img src="http://concursosoftwarelibre.org/1819/files/images/banners/cusl2_500x455.png" />
  </a>
</p>

By the way, I'll be talking about rust in the Seville University the next
Tuesday 5th of March 2019, if you're in Seville, come to talk with me :D

[1]: https://endlessos.com/
[2]: https://hack-computer.com/
[3]: http://danigm.net/gnome-gtk-developer.html
[4]: https://jobs.lever.co/endless
[5]: https://ostree.readthedocs.io/en/latest/
[6]: https://silverblue.fedoraproject.org/
[7]: https://wadobo.com
[8]: https://sugus.eii.us.es/
[9]: https://nvotes.com/
[10]: http://concursosoftwarelibre.org/
