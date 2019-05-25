Date: 2018-04-26
Title: GNOME 💙 Rust Hackfest in Madrid
Tags: gnome, rust, programming, gnome-class, wadobo
Category: blog
Slug: rust-gnome
Gravatar: 8da96af78e0089d6d970bf3760b0e724

The last week was the [GNOME 💙 Rust hackfest][1] in Madrid. I was there,
only for the first two days, but was a great experience to meet the people
working with Rust in GNOME a great community with a lot of talented people.

The event was in the [OpenShine][2] office, that was a great place and the
OpenShine people was very friendly too so thank you very much to OpenShine
for support this kind of events.

## What I did during the Hackfest

I arrive at 10:30, more or less, and there are some people there, but two
or three comes after the lunch, so the first morning we started to work,
each one in their project.

I've some patches for [Fractal][3] to review and I was working on the glade
file splitting. After that I downloaded the [gnome-class][4] code and
started to read and try to understand the code because I want to help in
the gnome-class development during the Hackfest.

After the lunch, the missing people from the morning was there so we did an
official "Hackfest presentation" everyone did a little presentation about
his work and what want to do during the event.

Gnome-class was the main project to join GNOME and Rust, and it's still in
a early alpha stage so Federico give us a little talk about what's
gnome-class and its parts.

<p class="img">
    <a href="/pictures/madrid-whiteboard.jpg">
        <img src="/pictures/madrid-whiteboard.jpg" />
    </a>
</p>

## Gnome-class

Gnome-class is basically a *compiler* that translate custom syntax to
*Gobject* binary compatible Rust code. Using the [proc-macro][5],
gnome-class parses a *Gobject* like declaration and creates all the Rust
code needed to use the *Glib* so we can have binary code that can be called
from *C* or from *Rust*. With this we can do Object Oriented programming in
Rust using the *Gobject* library and types.

So we've [three parts in gnome-class][6], the parser, the High-level
Internal Representation (HIR) and the code generation.

```
gobject_gen! {
    class Counter {
      f: Cell<u32>,
    }

    impl Counter {
        pub fn add(&self, x: u32) -> u32 {
            self.get_priv().f.set(self.get() + x);
            self.get()
        }

        pub fn get(&self) -> u32 {
            self.get_priv().f.get()
        }
    }
}

#[test]
fn test() {
    let c: Counter = Counter::new();

    println!("Counter has value: {}", c.get());

    c.add(2);
    c.add(20);
    assert_eq!(c.get(), 22);

    println!("Counter has value: {}", c.get());
}
```

This is Rust code with gnome-class, here we're creating a new *Class*
called `Counter` with two public methods, then we've a test that use this.
Behind this code, gnome-class generates a lot of ugly code with pointers
and so to make all of this C-Compatible and generate all the needed binary
using the *GObject* data scheme.

## My work in gnome-class

[Properties][7] declaration was not supported in gnome-class so took that
[task][8]. There was a [proposed syntax][9] and I started to work in the
parser to try to support that syntax and convert all the relevant
information into a Rust struct in the HIR tree.

To parse that I needed to learn [syn][10] that's a parser based in
[nom][11]. That was not easy, but there's a lot of code in gnome-class so I
can read and learn from that and at the end of the day I had a working
properties parser.

The second day I continue with my work and started to generate code. Here I
have more problems because the code generated is too low level and I didn't
now much about the *GObject* internals so I was playing around types
conversions.

I've to go just after the lunch, but during the back to home train trip I
was able to create a [Merge Request][12] with all the work I've done.

I've work to do during the week so I can't continue working on properties
support in gnome-class. But this week I've more time and I've been working
to complete the code generation, so now we've this test working:

```rust
#![feature(proc_macro)]

extern crate gobject_gen;

#[macro_use]
extern crate glib;
use gobject_gen::gobject_gen;

use std::cell::Cell;

gobject_gen! {
    class ClassWithProps {
        p: Cell<u32>,
        p2: Cell<u32>,
    }

    impl ClassWithProps {
        pub fn get(&self) -> u32 {
            self.get_priv().p.get() +
            self.get_priv().p2.get()
        }

        property MyProp: T where T: u32 {
            get(&self) -> T {
                let private = self.get_priv();
                return private.p.get();
            }

            set(&self, value: T) {
                let mut private = self.get_priv();
                private.p.set(value);
            }
        }

        property Prop2: T where T: u32 {
            get(&self) -> T {
                let private = self.get_priv();
                return private.p2.get();
            }

            set(&self, value: T) {
                let mut private = self.get_priv();
                private.p2.set(value);
            }
        }
    }
}

#[test]
fn test_props() {
    let obj: ClassWithProps = ClassWithProps::new();
    assert_eq!(obj.get(), 0);

    assert_eq!(obj.get_property_prop2(), 0);
    obj.set_property_prop2(42);
    assert_eq!(obj.get(), 42);
    assert_eq!(obj.get_property_prop2(), 42);

    obj.set_property_myprop(58);
    assert_eq!(obj.get_property_myprop(), 58);
}
```

## My first GNOME hackfest

This was my first GNOME hackfest. I've been in different GUADECs and other
events with GNOME devs, but this was the first time that I travel to work
on a specific *project* and not just to meet the people and view talks from
the distance.

It was a great experience. Rust is really new in the desktop development,
but there's a lot of people working so it's great.

<p class="img">
    <a href="/pictures/madrid-food.jpg">
        <img src="/pictures/madrid-food.jpg" />
    </a>
</p>

The next milestone is the [Fractal Hackfest][14], we'll be in Strasbourg
four days working.

I want to thank all the great GNOME community that makes collaboration
so easy, it's a great community.

Currently all of my work on this is voluntary so I need to thank my
coworkers at [Wadobo][13], because I'm spending some work time in this. I
can do this because my company is great.

<center>
    <a href="https://wadobo.com">
        <img src="/pictures/wadobo-mini.png" />
    </a>
</center>

[1]: https://wiki.gnome.org/Hackfests/Rust2018#Reports
[2]: https://www.openshine.com/
[3]: https://gitlab.gnome.org/World/fractal
[4]: https://gitlab.gnome.org/federico/gnome-class
[5]: https://doc.rust-lang.org/unstable-book/language-features/proc-macro.html
[6]: https://federico.pages.gitlab.gnome.org/gnome-class/
[7]: https://developer.gnome.org/gobject/stable/gobject-properties.html
[8]: https://gitlab.gnome.org/federico/gnome-class/issues/2
[9]: https://gitlab.gnome.org/federico/gnome-class/blob/master/gobject-notes/syntax.md
[10]: https://crates.io/crates/syn
[11]: https://crates.io/crates/nom
[12]: https://gitlab.gnome.org/federico/gnome-class/merge_requests/9
[13]: https://wadobo.com
[14]: https://wiki.gnome.org/Hackfests/Fractal2018
