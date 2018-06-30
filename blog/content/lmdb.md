Date: 2018-06-30
Title: LMDB: Cache database in memory
Tags: gnome, rust, programming, lmdb, cache, fractal
Category: blog
Slug: lmdb
Gravatar: 8da96af78e0089d6d970bf3760b0e724

Some days ago I was in a meeting talking about the E2E implementation for
Fractal, to know the current implementation state and to talk with other
developers. This meeting was promoted by [Puri.sm][1] people, because they
want to use Fractal for the Librem5 phone and they want to have E2E. There's
people working in the E2E and I think we can have this on Fractal at the end
of the year, but this is not what I want to talk about today.

In this meeting there was Fractal developers but we've also other people,
like the [nheko][2] developer, mujx (nheko is a Qt matrix client). During the
meeting, mujx ask us about the cache storage that we're using, because for the
E2E is too important to don't lose any key, because that'll be catastrophic,
you won't be able to read room messages. So it's important to have a
transactional database storage for this information. They are using [LMDB][3],
I didn't know nothing about LMDB so after this meeting I start to about it.

## LMDB

Lightning Memory-Mapped Database Manager (LMDB) is a key-value database, it's
memory mapped so it's fast, and also uses filesystem storage so we've
persistence. This database has transactions so it's safe to read/write from
different threads or process.

In Fractal we're using a simple json file for cache, but this doesn't support
transactions and if the app crash or if something bad happens, we can lose data.
This method is simple, but is slow and insecure, so using LMDB will improve
Fractal in several ways.

But LMDB is in memory and in Fractal we've a lot of interface code sharing the
app state, so we're passing the state between threads with copies and complex
data sharing. This can simplify the interface code because using LMDB for the
application global state will make this state accesible from different threads.

## Testing LMDB

Fractal is written in Rust so I want to write some tests before start to use
this on Fractal. There's a simple [LMDB rust crate][4], and I've been writting
an [example lib][5] to test it.

Basically what I've done is to write a simple trait that you can implement for
simple Rust structs so that struct can be stored and recover from the cache
with a simple method:

```
#[derive(Serialize, Deserialize, Debug)]
struct B {
    pub id: u32,
    pub complex: Vec<String>,
}
impl Cacheable for B {
    fn db() -> &'static str { "TESTDB" }
    fn key(&self) -> String {
        format!("b:{}", self.id)
    }
}
```

The struct should be serializable/deserializable with serde because in this
example I'm using [bincode][7] to convert structs to [u8].

The `Cacheable` trait only have two required methods, the db and the key. The
db is the db name to use to store this struct instances and the key is the
key to use when storing a concrete instance.

With this, we can store in the cache and query from the cache, using the key:

```
let db = &format!("{}-basic", DB);
let mut cache = Cache::new(db).unwrap();

let b = B{ id: 1, complex: vec![] };
let r = b.store(&mut cache);
assert!(r.is_ok());

let b1: B = B::get(&mut cache, "b:1").unwrap();
assert_eq!(b1.id, b.id);
assert_eq!(b1.complex.len(), 0);
b1.complex.push("One string".to_string());
b1.complex.push("Second string".to_string());
b1.store(&mut cache);

let b2: B = B::get(&mut cache, "b:1").unwrap();
assert_eq!(b2.id, b.id);
assert_eq!(b2.complex.len(), 2);
assert_eq!(&b2.complex[0][..], "One string");
```

This is thread safe, so we can read from the cache from different threads and
we'll always get the last version in the database.

LMDB is a key-value database, so we don't have relations. This is not a real
problem for us because we can model the relations in the keys, for example, we
can store Room messages with keys like this "message:ROOMID:messageID" and then
we can iterate over all objects with this prefix: "message:ROOMID" that will
give us all room messages. Something like this should work:

```
let prefix = format!("message:{}", room.id);
Message::iter(&mut cache, &prefix, |m| {
    // m is a Message struct fetched from the database, we can do
    // what we want here
    // ...
    Continue(true)
});
```

## LMDB in Fractal data model

We're thinking about moving the Fractal data model from the AppOp struct to
a new crate, independent of the UI, to simplify the UI code and to be able
to use the same data model from different UIs (we wan't to split fractal in
two different apps), [Julian wrote about this][6].

I think that we can use the LMDB cache to store this new app state that we
want to have and this will simplify a lot our code, because we will share the
same state and this state will be persisted in filesystem.

I'll start to write a new crate for Fractal to start to move all the app state
to this new crate. I think I can write a generic tool to simplify the LMDB use,
maybe I'll publish another crate in crates.io and use that in Fractal, but I
need to think a little more about the pattern to follow.

I write a lot of web code in my day to day work, and I've been working with
react+redux. This LMDB cache thing in Fractal reminds me a lot to the redux
store and I want to follow a similar pattern so we can have only an app state
and only a way to update this state.

[1]: https://puri.sm/
[2]: https://github.com/mujx/nheko
[3]: http://www.lmdb.tech/doc/
[4]: https://crates.io/crates/lmdb
[5]: https://gitlab.gnome.org/danigm/lmdb-rs-tests
[7]: https://crates.io/crates/bincode
[6]: https://blogs.gnome.org/jsparber/2018/06/17/refactor-backend-and-ui/
