Date: 2018-08-09
Title: libgepub + rust
Tags: gnome, rust, libgepub, gnome-books, epub
Category: blog
Slug: libgepub-rust
Gravatar: 8da96af78e0089d6d970bf3760b0e724

In 2010 I was working with evince, the gnome PDF document viewer, trying to
add some accessibility to PDF files. That was really hard, not because GTK+ or
ATK technology but because the PDF format itself. The PDF format is really cool
for printing because you know that the piece of paper will look the same as the
PDF doc, and because it's vector it scales and don't loose quality and files
are smaller than image files, but almost all PDF files have not any metadata for
sections, headings, tablets or so, this depends on the creation tool, but it's
really hard to deal with PDF content text, because you don't know event if the
text that you're reading is really in the same order that you read from the
PDF.

After my fight against the PDF format hell and poppler, I discovered the epub
format that's a really simple format for electronic books. An epub is a zip
with some XML files describing the book index and every chapter is a xhtml and
xhtml is a good format compared to PDF because you can parse easily with any
XML lib and the content is tagged and well structured so you know what's a
heading, what's a paragraph, etc.

So I started to write a simple C library to read epub files, thinking about
add epub support to evince. That's how [libgepub][1] was born. I tried to
[integrate libgepub in evince][2], I've something working, rendering with
webkit, but nothing really useful, because evince needs pages and it's not
easy to split an xhtml file in pages with the same height, because xhtml is
continuous text and it adapts to the page width, so I give up and leave this
branch.

## gnome-books

<center>
    <img src="https://wiki.gnome.org/Apps/Books?action=AttachFile&do=get&target=books-window.png" alt="gnome-books" width="100%"/>
</center>

After some time, I discovered [gnome-books][3], and the idea of epub support
comes to me again. Books has an initial *epub* support, that consists only in
showing in the collection, but when you click on the book, an error message
was shown because there's no epub preview support.

I've libgepub with GIR support and books was written with gjs so it was easy
for me to add an initial support for epub documents using libgepub and
rendering with webkit.

So libgepub is used in a gnome app to render epub documents and for that reason
gnome *depends* on libgepub now.

## Rustifying everything

In 2017 I discover [rust][4] and fell in love with this language, so I wanted
to write some code with rust and I started porting this epub library and I
ended creating the [epub crate][5], that's basically the same implementation
but with rust instead of C, the API is really similar.

After that, I read somewhere that Federico was porting the [librsvg][6]
code to rust, so I thought that I can do the same with libgepub and replace
almost all the C code with this new rust crate.

I copied all the code for autotools to build using cargo and I've copied to
the *glue* code from librsvg and adapt to my own lib. That worked really well
and I was able to remove the core libgepub C code and replace with the new
rust code.

But rust is really new and it was not full supported in all distributions, so
release depending on rust will make the release people's live harder. That's
the reason because I decided to leave the C version for now and wait a little
to make the rust migration.

And here we're, the libgepub has changed a little, some fixes and small changes,
but the main change is that now we're using meson to build instead of autotools,
and it's not easy to integrate a rust+cargo lib in the meson desc. There's a
[PR in meson to support this][7] but it seems that meson devs doesn't like the
idea.

So yesterday I was playing around with meson to get back the rust code working
in libgepub, and was not easy, but now I've a [working build configuration][8]
that works. It's a hack with a custom script to build with cargo, but it's
working so I'm really happy.

## Show me the code

To integrate the rust epub crate in the libgepub C lib I needed to write a
simple cargo project with the *glue* code that converts the rust types to
glib/c types and expose that in a C lib, and that's the [libgepub_internals][9],
that's full of glue rust+glib code like:

```rust
#[no_mangle]
pub extern "C" fn epub_new(path: *const libc::c_char) -> *mut EpubDoc {
    let my_path = unsafe { &String::from_glib_none(path) };
    let doc = EpubDoc::new(my_path);
    let doc = doc.unwrap();
    Box::into_raw(Box::new(doc))
}

#[no_mangle]
pub unsafe extern "C" fn epub_destroy(raw_doc: *mut EpubDoc) {
    assert!(!raw_doc.is_null());
    let _ = Box::from_raw(raw_doc);
}
```

Then, in the `gepub-doc.c`, that's the glib object that expose the GIR API,
I added calls to this functions, defining each function heading that'll be
used from the rust static lib at link time:

```C
// Rust
void      *epub_new(char *path);
void       epub_destroy(void *doc);
void      *epub_get_resource(void *doc, const char *path, int *size);
void      *epub_get_resource_by_id(void *doc, const char *id, int *size);
void      *epub_get_metadata(void *doc, const char *mdata);
void      *epub_get_resource_mime(void *doc, const char *path);
void      *epub_get_resource_mime_by_id(void *doc, const char *id);
void      *epub_get_current_mime(void *doc);
void      *epub_get_current(void *doc, int *size);
void      *epub_get_current_with_epub_uris(void *doc, int *size);
void       epub_set_page(void *doc, guint page);
guint      epub_get_num_pages(void *doc);
guint      epub_get_page(void *doc);
gboolean   epub_next_page(void *doc);
gboolean   epub_prev_page(void *doc);
void      *epub_get_cover(void *doc);
void      *epub_resource_path(void *doc, const char *id);
void      *epub_current_path(void *doc);
void      *epub_current_id(void *doc);
void      *epub_get_resources(void *doc);
guint      epub_resources_get_length(void *er);

gchar     *epub_resources_get_id(void *er, gint i);
gchar     *epub_resources_get_mime(void *er, gint i);
gchar     *epub_resources_get_path(void *er, gint i);
```

And then calling to this functions:

```C
static gboolean
gepub_doc_initable_init (GInitable     *initable,
                         GCancellable  *cancellable,
                         GError       **error)
{
    GepubDoc *doc = GEPUB_DOC (initable);

    g_assert (doc->path != NULL);
    doc->rust_epub_doc = epub_new (doc->path);
    if (!doc->rust_epub_doc) {
        if (error != NULL) {
            g_set_error (error, gepub_error_quark (), GEPUB_ERROR_INVALID,
                         "Invalid epub file: %s", doc->path);
        }
        return FALSE;
    }

    return TRUE;
}
```

To make this work, I needed to add the `libgepub_internals` dependency to the
libgepub meson.build like this:

```
gepub_deps = [
  dependency('gepub_internals', fallback: ['libgepub_internals', 'libgepub_internals_dep']),
  dependency('webkit2gtk-4.0'),
  dependency('libsoup-2.4'),
  dependency('glib-2.0'),
  dependency('gobject-2.0'),
  dependency('gio-2.0'),
  dependency('libxml-2.0'),
  dependency('libarchive')
]
```

This definition looks for the gepub\_internals lib in the libgepub\_internals
subproject with this meson.build:

```
project(
  'libgepub_internals', 'rust',
  version: '3.29.6',
  license: 'GPLv3',
)

libgepub_internals_version = meson.project_version()
version_array = libgepub_internals_version.split('.')
libgepub_internals_major_version = version_array[0].to_int()
libgepub_internals_minor_version = version_array[1].to_int()
libgepub_internals_version_micro = version_array[2].to_int()

libgepub_internals_prefix = get_option('prefix')

cargo = find_program('cargo', required: true)
cargo_vendor = find_program('cargo-vendor', required: false)
cargo_script = find_program('scripts/cargo.sh')
grabber = find_program('scripts/grabber.sh')
cargo_release = find_program('scripts/release.sh')

c = run_command(grabber)
sources = c.stdout().strip().split('\n')

cargo_build = custom_target('cargo-build',
                        build_by_default: true,
                        input: sources,
                        output: ['libgepub_internals'],
                        install: false,
                        command: [cargo_script, '@CURRENT_SOURCE_DIR@', '@OUTPUT@'])

libgepub_internals_lib = static_library('gepub_internals', cargo_build)

cc = meson.get_compiler('c')
th = dependency('threads')
libdl = cc.find_library('dl')

libgepub_internals_dep = declare_dependency(
  link_with: libgepub_internals_lib,
  dependencies: [th, libdl],
  sources: cargo_build,
)
```

I'm using here a custom\_target to build the lib using a custom script that
simply calls to cargo and then copies the result lib to the correct place:

```bash
if [[ $DEBUG = true ]]
then
    echo "DEBUG MODE"
    cargo build --manifest-path $1/Cargo.toml && cp $1/target/debug/libgepub_internals.a $2.a
else
    echo "RELEASE MODE"
    cargo build --manifest-path $1/Cargo.toml --release && cp $1/target/release/libgepub_internals.a $2.a
fi
```

Then I declared the `static_library` and the dependency with
`declare_dependency`. I need to add `threads` and `dl` because the epub crate
depends on it and this works!

I'll need to vendor all dep crates with cargo-vendor for releasing, but I think
that this is working and it's the way to go with libgepub.

## The future of libgepub + rust

Currently, with the libgepub\_internals lib, the `gepub-doc.c` code is
basically to provide a `gobject` and GIR information to be able to work with
epub docs, but the real work is done in Rust. The [gnome-class][10] provides a
simple way to build this `gobject` with rust code, but currently it's not
completed and there's no way to generate GIR, but in the future, it could be
cool to remove the `gepub-doc.c` code and generate all with `gnome-class`.
I can wait until Federico writes the piece of code that I need for this or maybe
I should contribute to `gnome-class` to be able to do this.

Libgepub also provides a widget that inherits from WebkitWebView to render the
book. That widget is written in C to provide GIR data also and we can try to
do the same and use `gnome-class` to write this widget.

But for now, we're really far from this, we need to spend some time improving
`gnome-class` to be able to write all the code in **rust** and expose the
gobject GIR. Meantime we can start to use rust with this **glue** code, and
that's great, because if you've a gobject library and you want to migrate to
rust, you don't need to migrate all the code at once, you can do the same that
librsvg is doing and migrate function by function and that's really cool.

[1]: https://gitlab.gnome.org/GNOME/libgepub
[2]: https://github.com/danigm/evince/tree/epub
[3]: https://wiki.gnome.org/Apps/Books
[4]: https://www.rust-lang.org/
[5]: https://crates.io/crates/epub
[6]: https://gitlab.gnome.org/GNOME/librsvg
[7]: https://github.com/mesonbuild/meson/pull/2617
[8]: https://gitlab.gnome.org/GNOME/libgepub/tree/rust-migration
[9]: https://gitlab.gnome.org/GNOME/libgepub/tree/rust-migration/subprojects/libgepub_internals
[10]: https://gitlab.gnome.org/federico/gnome-class
