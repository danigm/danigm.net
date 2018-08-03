Date: 2018-08-03
Title: mdl
Tags: gnome, rust, mdl, fractal
Category: blog
Slug: mdl
Gravatar: 8da96af78e0089d6d970bf3760b0e724

The last month I wrote a blog post about the [LMDB Cache database][1] and my
wish to use that in Fractal. To summarize, LMDB is a memory-mapped key-value
database that persist the data to the filesystem. I want to use this in the
Fractal desktop application to replace the current state storage system
(we're using simple json files) and as a side effect we can use this storage
system to share data between threads because currently we're using a big
struct `AppOp` shared with `Arc<Mutex<AppOp>>` and this cause some problems
because we need to share and lock and update the state there.

The main goal is to define an app data model with smaller structs and store
this using LMDB, then we can access to the same data querying the LMDB and we
can update the app state storing to the LMDB.

With this change we don't need to share these structs, we only need to query
to the LMDB to get the data and the work with that, and this should simplify
our code. The other main benefit will be that we'll have this state in the
filesystem by default so when we open the app after close, we'll stay in the
same state.

Take a look to the [gtk TODO example app][6] to view how to use *mdl* with
signals in a real gtk app.

## What is mdl

[mdl][3] is Data model library to share app state between threads and process
and persist the data in the filesystem. Implements a simple way to store
structs instances in a LMDB database and other methods like BTreeMap.

I started to play with the LMDB rust binding and writing some simple tests.
After some simple tests, I decided to write a simple abstraction to hide the
LMDB internals and to provide a simple data storage and to do that I created
the **mdl** crate.

The idea is to be able to define your app model as simple rust structs. LMDB is
a key-value database so every struct instance will have an unique *key* to
store in the cache.

The keys are stored in the cache ordered, so we can use some techniques to
store related objects and to retrieve all objects of a kind, we only need to
build keys correctly, following an scheme. For example, for fractal we can
store rooms, members and messages like this:

 * rooms with key "room:roomid", to store all the room information, title,
   topic, icon, unread msgs, etc.
 * members with key "member:roomid:userid", to store all member information.
 * messages with key "msg:roomid:msgid" to store room messages.

Following this key assignment we can iterate over all rooms by querying all
objects that starts with "room", we can get all members and all messages from
a room.

This have some inconveniences, because we can't query directly an message by
id if we don't know the roomid. If we need that kind of queries, we need to
think about another key assignment or maybe we should duplicate data. key-value
are simple databases so we don't have the power of relational databases.

## Internals

LMDB is fast and efficient, because it's in memory so using this cache won't
add a lot of overhead, but to make it simple to use I've to add some overhead,
so mdl is easy by default and can be tuned to be really fast.

This crate has three main modules with traits to implement:

 * **model**: This contains the `Model` trait that should implement every
   struct that we want to make cacheable.
 * **store**: This contains the `Store` trait that's implemented by all the
   cache systems.
 * **signal**: This contains the `Signaler` trait and two structs that allow
   us to emit/subscribe to "key" signals.

And two more modules that implements the current two cache systems:

 * **cache**: LMDB cache that implements the `Store` trait.
 * **bcache**: BTreeMap cache that implements the `Store` trait. This is a good
   example of other cache system that can be used, this doesn't persist to the
   filesystem.

So we've two main concepts here, the **Store** and the **Model**. The model
is the plain data and the store is the container of data. We'll be able to add
models to the store or to query the store to get stored models. We store our
models as key-value where the key is a `String` and the value is a `Vec<u8>`,
so every model should be serializable.

This serialization is the bigger overhead added. We need to do this because
we need to be able to store this in the LMDB database. Every request will create
a copy of the object in the database, so we're not using the same data. This can
be tuned to use pointers to the real data, but to do that we'll need to use
*unsafe* code and I think that the performance that we'll get with this doesn't
deserve the complexity that this will add.

By default, the `Model` trait has two methods `fromb` and `tob` to serialize
and deserialize using [bincode][4], so any struct that implements the `Model`
trait and doesn't reimplement these two methods should implement `Serialize`
and `Deserialize` from [serde][5].

The signal system is an addition to be able to register callbacks to **keys**
modifications in the **store**, so we can do something when a new objects is
added, modified or deleted from the store. The signaler is optional and we
should use it in a explicit way.

## How to use it

First of all, you should define your data model, the struct that you want to
be able to store in the database:

```rust
#[derive(Serialize, Deserialize, Debug)]
struct A {
    pub p1: String,
    pub p2: u32,
}
```

In this example we'll define a struct called **A** with two attributes, **p1**,
a `String`, and **p2**, an `u32`. We derive `Serialize` and `Deserialize`
because we're using the default `fromb` and `tob` from the `Model` trait.

Then we need to implement the `Model` trait:

```rust
impl Model for A {
    fn key(&self) -> String {
        format!("{}:{}", self.p1, self.p2)
    }
}
```

We only reimplement the `key` method to build a key for every instance of `A`.
In this case our key will be the `String` followed by the number, so for example
if we've something like `let a = A { p1: "myk", p2: 42 };` the key will be
"myk:42".

Then, to use this we need to have a `Store`, in this example, we'll use the
LMDB store that's the struct `Cache`:

```rust
    // initializing the cache. This str will be the fs persistence path
    let db = "/tmp/mydb.lmdb";
    let cache = Cache::new(db).unwrap();
```

We pass the path to the filesystem where we want to persist the cache as the
first argument, in this example we'll persist to "/tmp/mydb.lmdb". When we
ran the program for the first time a directory will be created there. The next
time, that cache will be used with the information from the previous execution.

Then, with this `cache` object we can instantiate an `A` object and store
in the `cache`:

```rust
    // create a new *object* and storing in the cache
    let a = A{ p1: "hello".to_string(), p2: 42 };
    let r = a.store(&cache);
    assert!(r.is_ok());
```

The `store` method will serialize the object and store a copy of that in the
cache.

After the store, we can query for this object from other process, using the
same lmdb path, or from the same process using the cache:

```rust
    // querying the cache by key and getting a new *instance*
    let a1: A = A::get(&cache, "hello:42").unwrap();
    assert_eq!(a1.p1, a.p1);
    assert_eq!(a1.p2, a.p2);
```

We'll get a copy of the original one.

This is the full example:

```rust
extern crate mdl;
#[macro_use]
extern crate serde_derive;

use mdl::Cache;
use mdl::Model;
use mdl::Continue;

#[derive(Serialize, Deserialize, Debug)]
struct A {
    pub p1: String,
    pub p2: u32,
}
impl Model for A {
    fn key(&self) -> String {
        format!("{}:{}", self.p1, self.p2)
    }
}

fn main() {
    // initializing the cache. This str will be the fs persistence path
    let db = "/tmp/mydb.lmdb";
    let cache = Cache::new(db).unwrap();

    // create a new *object* and storing in the cache
    let a = A{ p1: "hello".to_string(), p2: 42 };
    let r = a.store(&cache);
    assert!(r.is_ok());

    // querying the cache by key and getting a new *instance*
    let a1: A = A::get(&cache, "hello:42").unwrap();
    assert_eq!(a1.p1, a.p1);
    assert_eq!(a1.p2, a.p2);
}
```

### Iterations

When we store objects with the same key prefix we can iterate over all of
the objects, because we don't know the full key of all objects.

Currently there's two ways to iterate over all objects with the same prefix
in a `Store`:

 * **all**

This is the simpler way, calling the `all` method we'll receive a `Vec<T>` so
we've all the objects in a vector.

```rust
    let hellows: Vec<A> = A::all(&cache, "hello").unwrap();
    for h in hellows {
        println!("hellow: {}", h.p2);
    }
```

This has a little problem, because if we've a lot of objects, this will use a
lot of memory for the vector and we'll be iterating over all objects twice. To
solve this problems, the `iter` method was created.

 * **iter**

The `iter` method provides a way to call a closure for every object with this
prefix in the key. This closure should return a `Continue(bool)` that will
indicates if we should continue iterating of if we should stop the iteration
here.

```rust
    A::iter(&cache, "hello", |h| {
        println!("hellow: {}", h.p2);
        Continue(true)
    }).unwrap();

```

Using the `Continue` we can avoid to iterate over all the objects, for example
if we're searching for one concrete object.

We're copying every object, but the `iter` method is better than the `all`,
because if we don't copy or move the object from the closure, this copy only
live in the closure scope, so we'll use less memory and also, we only iterate
one. If we use `all`, we'll iterate over all objects with that prefix to build
the vector so if we iterate over that vector another time this will cost more
than the `iter` version.

## Signal system

As I said before, the signal system provide us a way to register callbacks
to key modifications. The signal system is independent of the `Model` and
`Store` and can be used independently:

```rust
extern crate mdl;

use mdl::Signaler;
use mdl::SignalerAsync;
use mdl::SigType;
use std::sync::{Arc, Mutex};
use std::{thread, time}; 

fn main() {
    let sig = SignalerAsync::new();
    sig.signal_loop();
    let counter = Arc::new(Mutex::new(0));

    // one thread for receive signals
    let sig1 = sig.clone();
    let c1 = counter.clone();
    let t1: thread::JoinHandle<_> =
    thread::spawn(move || {
        let _ = sig1.subscribe("signal", Box::new(move |_sig| {
            *c1.lock().unwrap() += 1;
        }));
    });

    // waiting for threads to finish
    t1.join().unwrap();

    // one thread for emit signals
    let sig2 = sig.clone();
    let t2: thread::JoinHandle<_> =
    thread::spawn(move || {
        sig2.emit(SigType::Update, "signal").unwrap();
        sig2.emit(SigType::Update, "signal:2").unwrap();
        sig2.emit(SigType::Update, "signal:2:3").unwrap();
    });

    // waiting for threads to finish
    t2.join().unwrap();

    let ten_millis = time::Duration::from_millis(10);
    thread::sleep(ten_millis);

    assert_eq!(*counter.lock().unwrap(), 3);
}
```

In this example we're creating a `SignalerAsync` that can `emit` signal and
we can `subscribe` a callback to any signal. The `sig.signal_loop();` init the
signal loop thread, that wait for signals and call any subscribed callback when
a signal comes.

```rust
        let _ = sig1.subscribe("signal", Box::new(move |_sig| {
            *c1.lock().unwrap() += 1;
        }));
```

We subscribe a callback to the signaler. The signaler can be cloned and the list
of callbacks will be the same, if you emit a signal in a clone and subscribe in
other clone, that signal will trigger the callback.

Then we're emiting some signals:

```rust
        sig2.emit(SigType::Update, "signal").unwrap();
        sig2.emit(SigType::Update, "signal:2").unwrap();
        sig2.emit(SigType::Update, "signal:2:3").unwrap();
```

All of this three signals will trigger the previous callback because the
subscription works as a *signal starts with*. This allow us to subscribe to
all new room messages insertion if we follow the previous described keys,
subscribing to "msg:roomid" and if we only want to register a callback to
be called only when one message is updated we can subscribe to
"msg:roomid:msgid" and this callback won't be triggered for other messages.

The callback should be a `Box<Fn(signal)>` where signal is the following
struct:

```rust
#[derive(Clone, Debug)]
pub enum SigType {
    Update,
    Delete,
}

#[derive(Clone, Debug)]
pub struct Signal {
    pub type_: SigType,
    pub name: String,
}
```

Currently only `Update` and `Delete` signal types are supported.

### Signaler in gtk main loop

All the UI operations in a gtk app should be executed in the gtk main loop so
we can't use the `SignalerAsync` in a gtk app, because this signaler creates
one thread for the callbacks so all callbacks should implement the `Send` trait
and if we want to modify, for example, a `gtk::Label` in a callback, that
callback won't implement `Send` because `gtk::Label` can't be send between
threads safely.

To solve this problem, I've added the `SignalerSync`. That doesn't launch any
threads and where all operations runs in the same thread, even the callback.
This is a problem if one of your callbacks locks the thread, because this will
lock your interface in a gtk app, so any callback in the sync signaler should
be non blocking.

This signaler should be used in a different way, so we should call from time
to time to the `signal_loop_sync` method, that will check for new signals and
will trigger any subscribed callback. This signaler doesn't have a `signal_loop`
because we should do the loop in our thread.

This is an example of how to run the signaler loop inside a gtk app:

```rust
    let sig = SignalerSync::new();

    let sig1 = sig.clone();
    gtk::timeout_add(50, move || {
        gtk::Continue(sig1.signal_loop_sync())
    });

    // We can subscribe callbacks using the sig here
```

In this example code we're registering a timeout callback, every 50ms this
closure will be called, from the gtk main thread, and the `signal_loop_sync`
will check for signals and call the needed callbacks.

This method returns a `bool` that's false when the signaler stops. You can
stop the signaler calling the `stop` method.

## Point of extension

I've tried to make this crate generic to be able to extend in the future and
provide other kind of cache that can be used changing little code in the apps
that uses **mdl**.

This is the main reason to use traits to implement the store, so the first point
of extension is to add more cache systems, we're currently two, the LMDB and
the BTreeMap, but it would be easy to add more key-value storages, like
memcached, [unqlie][7], mongodb, redis, couchdb, etc.

The signaler is really simple, so maybe we can start to think about new
signalers that uses `Futures` and other kind of callbacks registration.

As I said before, mdl does a copy of the data on every write and on every read,
so it could be cool to explore the implication of these copies in the
performance and try to find methods to reduce this overhead.

[1]: http://danigm.net/lmdb.html
[2]: https://gitlab.gnome.org/danigm/mdl/
[3]: https://crates.io/crates/mdl
[4]: https://crates.io/crates/bincode
[5]: https://crates.io/crates/serde_derive
[6]: https://gitlab.gnome.org/danigm/mdl/blob/master/examples/gtkapp/src/main.rs
[7]: https://crates.io/crates/unqlite