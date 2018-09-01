Date: 2018-09-01
Title: GIR support in gnome-class
Tags: gnome, rust, gnome-class, GIR
Category: blog
Slug: gnome-class-gir
Gravatar: 8da96af78e0089d6d970bf3760b0e724

Recently I've been working again in the [rust port of libgepub][3], libgepub
is C code, but in the [`rust-migration` branch][4] almost all the real
functionality is done with rust and the `GepubDoc` class is a `GObject` wrapper
around that code.

For this reason I was thinking about to use [`gnome-class`][1] to implement
`GepubDoc`.

Gnome-class is a rust lib to write GObject code in rust that's compatible with
the C binary API so then you can call this new GObject code written with
gnome-class from C. I've worked a little in gnome-class, implementing a
[basic properties support][2].

## GObject Introspection

A great advantage of write GObject code in C is that you can have automatic
bindings using [GObject Introspection][5]. This is great because you only need
to write the C code, write correctly the documentation of the public API and
then you'll get GIR for free, and that means that you can use your lib from
`gjs`, `python` and other automatic bindings.

GIR defines a simple XML document to declare the public API and there is the
meta information needed for bindings, to know how to call the lib functions and
how to convert params and also provides memory management information, for
languages with garbage collector and so. These files are places under
`/usr/share/gir-1.0/` and it looks like this:

```xml
      <method name="get_cover" c:identifier="gepub_doc_get_cover">
        <return-value transfer-ownership="full">
          <doc xml:space="preserve">cover file path to retrieve with
gepub_doc_get_resource</doc>
          <type name="utf8" c:type="gchar*"/>
        </return-value>
        <parameters>
          <instance-parameter name="doc" transfer-ownership="none">
            <doc xml:space="preserve">a #GepubDoc</doc>
            <type name="Doc" c:type="GepubDoc*"/>
          </instance-parameter>
        </parameters>
      </method>
```

This xml is *compiled* to a binary format to be used from bindings and those
compiled gir files are places under `/usr/lib64/girepository-1.0/` with the
`.typelib` extension.

This is great, and the `GepubDoc` class is exported as GIR and indeed it's used
from javascript code in the gnome-books application using this. If we want to
migrate libgepub from C to rust, we need to provide this GIR to don't break
the compatibility in other apps. That's done currently in the rust-migration
branch by hand, creating the `GepubDoc` in C and calling the rust code from
there.

With gnome-class it should be possible to write that `GepubDoc` code in rust
and have the same ABI, but currently gnome-class doesn't generate GIR, that's
a little problem that I can try to solve using my dev skills.

## Adding GIR to gnome-class

So, libgepub is the excuse to start to implement GIR in gnome-class. There's
an [issue][6] in the gitlab with an initial syntax proposal and I started from
that:

```rust
#[generate_gir("foo.gir")]
#[generate_c_header("foo.h")]
gobject_gen! {
    "foo.gir",
    "foo.h",

    class Foo {
        ...
    }

    impl Foo {
        ...
    }
}
```

The first thing to do is to add a way to tell that we want to generate the GIR
file in the class definition. In this proposal, the GIR tag is before the
`gobject_gen` proc-macro, that can't be done, or I don't know how to do that
easily, so I changed to a declaration inside the proc-macro, that's what we're
parsing in gnome-class:

```rust
gobject_gen! {
    #[generate_gir("Counter.gir")]
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
```

With the code insithe de `gobject_gen` I only need to update the parser to
allow this new syntax:

```
named!{parse_gir -> Option<LitStr>,
    option!(do_parse!(
        punct!(#)                               >>
        name: brackets!(do_parse!(
            call!(keyword("generate_gir"))      >>
            name: parens!(syn!(LitStr))         >>
            (name.1)
        )) >>
        (name.1)
    ))
}

impl Synom for ast::Class {
    named!(parse -> Self, do_parse!(
        gir: call!(parse_gir)                                    >>
        call!(keyword("class"))                                  >>
        name: syn!(Ident)                                        >>
        extends: option!(do_parse!(
            punct!(:)                                            >>
            superclass: syn!(Path)                               >>
            // FIXME: interfaces
            (superclass)))                                       >>
        fields: syn!(FieldsNamed)                                >>
        (ast::Class {
            gir,
            name,
            extends,
            fields,
        })
    ));
```

Then, I'm storing the GIR file name in the ast class so I can check if that
field is `None` or `Some` and generate the GIR in that case.

## Generating the XML

The parser was the easier part, we've now the hability to define if we want
to generate the GIR file and we're storing that information in the High-level
Internal Representation (hir).

To generate the XML I've to add a new call before generating the code:

```diff
     let result: Result<proc_macro2::TokenStream> =
-        hir::Program::from_ast_program(&ast_program).and_then(|program| Ok(gen::codegen(&program)));
+        hir::Program::from_ast_program(&ast_program)
+            .and_then(|program| {
+                gen::gir::generate(&program)?;
+                Ok(gen::codegen(&program))
+            });
 
     match result {
         Ok(tokens) => {
```

The [`gir`][8] module generates the XML, iterating over all classes defined in
the program.

The XML isn't really hard to generate, we've almost all the information so we
can iterate over all the class methods and add to the XML. There's some
information that's not really easy to get so I've let some *TODO* in this
initial version, like:

 * Find the parent class name (GObject.Object by default)
 * Get the library version and shared-lib path (lib#CLASSNAME#1.0.0 by default)
 * Get dependencies

So this is not a full featured GIR support, but it's an initial step to get
it, and it *works*, at least with simple examples :D

## Example project

To test that this is working correctly I've created a
[simple example project][7], that uses gnome-class, generates the gir and
has an small script to call the generated code from python.

This is the rust code:

```
gobject_gen! {
    #[generate_gir("Counter.gir")]
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
```

I've a bash script to compile and generate the typelib file from the xml,
generated by gnome-class:

```sh
cargo +nightly build
g-ir-compiler Counter.gir > Counter-1.0.typelib
```

And I've written a test in python using `gi.repository`:

```python
import unittest
from gi.repository import Counter

class TestCounter(unittest.TestCase):

    def test_new(self):
        c = Counter.Counter()
        self.assertEqual(c.get(), 0)

    def test_add(self):
        c = Counter.Counter()
        self.assertEqual(c.add(1), 1)
        self.assertEqual(c.add(3), 4)

    def test_get(self):
        c = Counter.Counter()
        self.assertEqual(c.get(), 0)
        self.assertEqual(c.add(1), 1)
        self.assertEqual(c.get(), 1)

if __name__ == '__main__':
    unittest.main()
```

This is working right now, so we're getting closer to the final goal of having
libgepub written with rust code and have GIR generation.

[1]: https://gitlab.gnome.org/federico/gnome-class
[2]: http://danigm.net/rust-gnome.html
[3]: http://danigm.net/libgepub-rust.html
[4]: https://gitlab.gnome.org/GNOME/libgepub/tree/rust-migration/
[5]: https://gi.readthedocs.io/en/latest/
[6]: https://gitlab.gnome.org/federico/gnome-class/issues/8
[8]: https://gitlab.gnome.org/danigm/gnome-class/tree/gir/src/gen/gir.rs
[7]: https://gitlab.gnome.org/danigm/gnome-class-example/
