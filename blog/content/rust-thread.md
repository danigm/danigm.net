Date: 2017-04-08
Title: Rust: Concurrencia
Tags: wadobo, rust, programming, threads
Category: blog
Slug: rust-thread
Gravatar: 8da96af78e0089d6d970bf3760b0e724

La programación concurrente es algo básico a día de hoy para poder sacar el
máximo rendimiento a los ordenadores modernos con múltiples cores. Sin
embargo es también de lo más complejo programar cualquier cosa compartiendo
memoria, hay que tener mucho cuidado y añadir semáforos y gestionar
manualmente el acceso a memoria compartida, cualquier despiste puede ser un
gran problema.

[Rust facilita la programación concurrente][1] con las comprobaciones que se
hacen en tiempo de compilación y con la gestión de memoria que realiza, el
sistema de propiedad de la memoria que implementa Rust nos asegura que no
ocurrirán "data race" y esto es válido también para la programación
concurrente, por lo que una vez compilado tenemos la certeza de que la
gestión de la memoria compartida es correcta y que no habrá ningún
"segmentation fault" porque un hilo se ejecute antes que otro y elimine la
memoria compartida, etc.

# Hilos

Empecemos con un ejemplo muy básico con el uso de [hilos en Rust][2] y vayamos
viendo el tratamiento de las variables compartidas según lo complicamos.

```rust
use std::thread;

fn main() {
    thread::spawn(|| {
        println!("Hello from a thread!");
    });
}
```
[ejecutar][20]

En este ejemplo básico creamos un hilo con **thread::spawn**, que recibe un
*closure* y se lanza justo al definirlo. Si ejecutamos este ejemplo no
saldrá nada por pantalla, ya que el proceso inicial termina antes de que el
hilo llegue a ejecutarse e imprimir. Para esperar a que un hilo termine se
puede utilizar el método **join**.

```rust
use std::thread;

fn main() {
    let child = thread::spawn(|| {
        println!("Hello from a thread!");
    });
    let _ = child.join();
}
```
[ejecutar][21]

Podemos lanzar varios hilos dentro de un bucle:

```rust
use std::thread;

fn main() {
    let mut childs = vec![];

    for i in 0..10 {
        let child = thread::spawn(move || {
            println!("Hello from a thread! {}", i);
        });
        childs.push(child);
    }

    for c in childs {
        let _ = c.join();
    }
}
```
[ejecutar][22]

En este ejemplo ya hay varias cosas que hay que explicar, porque empezamos
a *compartir* memoria. Creamos un *Vec* donde metemos todos los hilos para
luego poder hacer un join y esperar a que todos terminen. Dentro del hilo
imprimimos por pantalla el índice de la iteración.

Hemos tenido que añadir **move** en el closure del hilo, ya que si no lo
usamos, el compilador se quejará de que el closure puede vivir más allá de
**i**. Al poner el **move** lo que hacemos es que en lugar de *borrow* se
hace *move* de las variables utilizadas dentro del *closure*, y en este
caso nos permite utilizar **i** dentro del hilo.

Al ser **i** un entero, el **move** nos vale perfectamente, porque se copia
la memoria, y podríamos acceder al valor de **i** después de lanzar el hilo
sin problemas. Sin embargo si queremos compartir un **String**, no sería
posible ya que para el siguiente hilo la cadena se ha movido.

```rust
use std::thread;

fn main() {
    let mut childs = vec![];
    let shared = String::from("Shared string");

    for i in 0..10 {
        let child = thread::spawn(move || {
            println!("Hello from a thread! {} - {}", shared, i);
        });
        childs.push(child);
    }

    for c in childs {
        let _ = c.join();
    }
}
```

```bash
error[E0382]: capture of moved value: `shared`
 --> src/main.rs:9:54
  |
8 |         let child = thread::spawn(move || {
  |                                   ------- value moved (into closure) here
9 |             println!("Hello from a thread! {} - {}", shared, i);
  |                                                      ^^^^^^ value captured here after move
  |
  = note: move occurs because `shared` has type `std::string::String`, which does not implement the `Copy` trait
```

Esto se puede solucionar clonando la cadena antes, y en este caso, no
compartiremos memoria, sino que estamos usando una variable diferente para
cada hilo.

Si queremos compartir realmente una referencia a memoria entre hilos
tenemos que usar los tipos **Arc** y **Mutex** en combinación.

## Arc / Mutex

```rust
use std::thread;
use std::sync::{Arc, Mutex};

fn main() {
    let mut childs = vec![];
    let shared = Arc::new(Mutex::new(String::from("")));

    for i in 0..10 {
        let s = shared.clone();
        let child = thread::spawn(move || {
            println!("In thread {}", i);

            let out = String::from("Thread ") + &i.to_string() + "\n";
            s.lock().unwrap().push_str(&out);
        });
        childs.push(child);
    }

    for c in childs {
        let _ = c.join();
    }

    println!("\nOutput:\n{}", *(shared.lock().unwrap()));
}
```
[ejecutar][23]

En este ejemplo definimos la cadena dentro de un **Mutex** y este dentro de
un **Arc**, así podemos compartir realmente la memoria entre hilos.

**Arc** es un contador de referencias que se puede compartir entre hilos,
por lo tanto, el **clone** no copia la memoria, sino que crea una nueva
referencia.

**Mutex** implementa el bloqueo asociado a la variable en concreto, por lo
tanto para acceder a esta variable es necesario llamar al método **lock**,
que nos asegura que podemos leer o modificar esta variable sin que haya
condiciones de carrera entre hilos.

A diferencia de otros lenguajes, el **Mutex** asociado a los datos hace más
simple el acceso y nos asegura que no hay condiciones de carrera, ya que si
no utilizamos estos tipos e intentamos compartir memoria entre hilos el
compilador se quejará.

# Canales

Además de compartir variables con **Arc/Mutex**, hay otra forma de
comunicar diferentes hilos de forma relativamente sencilla, usando canales.

```rust
use std::thread;
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();
    let mut childs = vec![];

    for i in 0..10 {
        let tx = tx.clone();
        let child = thread::spawn(move || {
            println!("In thread {}", i);

            let out = String::from("Thread ") + &i.to_string();
            tx.send(out).unwrap();
        });
        childs.push(child);
    }

    for c in childs {
        let _ = c.join();
    }

    println!("\nOutput:");
    loop {
        match rx.try_recv() {
            Ok(x) => println!("{}", x),
            Err(_) => break
        }
    }
}
```
[ejecutar][24]

Con **channel** creamos un transmisor, **tx**, y un receptor, **rx**, en
cada hilo, clonamos el transmisor y escribimos ahí nuestra salida, en el
**send** podemos enviar cualquier tipo de dato según se cree el channel, no
se pueden enviar diferentes tipos de datos por el mismo canal.

Usando el receptor se puede leer del canal, en este ejemplo leemos cuando
todos los hilos han terminado, pero el método **recv** se puede usar en
cualquier momento y bloqueará la ejecución hasta que se envíe algo por el
canal.

# Bibliotecas externas

Además de usar los threads básicos de Rust, existen otras muchas
bibliotecas que nos ofrecen otras formas de hacer programación concurrente,
aquí pongo algunos enlaces:

 * [Crossbeam][4]
 * [Rayon][5]
 * [Coroutine-rs][6]
 * [Coiro-rs][7]
 * [Futures][3]

[1]: https://doc.rust-lang.org/book/concurrency.html
[2]: https://doc.rust-lang.org/book/concurrency.html#threads
[3]: https://tokio.rs/docs/getting-started/futures/
[4]: https://github.com/aturon/crossbeam
[5]: https://github.com/nikomatsakis/rayon
[6]: https://github.com/rustcc/coroutine-rs
[7]: https://github.com/zonyitoo/coio-rs


[20]: https://play.rust-lang.org/?code=use%20std%3A%3Athread%3B%0A%0Afn%20main()%20%7B%0A%20%20%20%20thread%3A%3Aspawn(%7C%7C%20%7B%0A%20%20%20%20%20%20%20%20println!(%22Hello%20from%20a%20thread!%22)%3B%0A%20%20%20%20%7D)%3B%0A%7D%0A%20&version=stable&backtrace=0
[21]: https://play.rust-lang.org/?code=use%20std%3A%3Athread%3B%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20child%20%3D%20thread%3A%3Aspawn(%7C%7C%20%7B%0A%20%20%20%20%20%20%20%20println!(%22Hello%20from%20a%20thread!%22)%3B%0A%20%20%20%20%7D)%3B%0A%20%20%20%20let%20_%20%3D%20child.join()%3B%0A%7D&version=stable&backtrace=0
[22]: https://play.rust-lang.org/?code=use%20std%3A%3Athread%3B%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20mut%20childs%20%3D%20vec!%5B%5D%3B%0A%0A%20%20%20%20for%20i%20in%200..10%20%7B%0A%20%20%20%20%20%20%20%20let%20child%20%3D%20thread%3A%3Aspawn(move%20%7C%7C%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20println!(%22Hello%20from%20a%20thread!%20%7B%7D%22%2C%20i)%3B%0A%20%20%20%20%20%20%20%20%7D)%3B%0A%20%20%20%20%20%20%20%20childs.push(child)%3B%0A%20%20%20%20%7D%0A%0A%20%20%20%20for%20c%20in%20childs%20%7B%0A%20%20%20%20%20%20%20%20let%20_%20%3D%20c.join()%3B%0A%20%20%20%20%7D%0A%7D&version=stable&backtrace=0
[23]: https://play.rust-lang.org/?code=use%20std%3A%3Athread%3B%0Ause%20std%3A%3Async%3A%3A%7BArc%2C%20Mutex%7D%3B%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20mut%20childs%20%3D%20vec!%5B%5D%3B%0A%20%20%20%20let%20shared%20%3D%20Arc%3A%3Anew(Mutex%3A%3Anew(String%3A%3Afrom(%22%22)))%3B%0A%0A%20%20%20%20for%20i%20in%200..10%20%7B%0A%20%20%20%20%20%20%20%20let%20s%20%3D%20shared.clone()%3B%0A%20%20%20%20%20%20%20%20let%20child%20%3D%20thread%3A%3Aspawn(move%20%7C%7C%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20println!(%22In%20thread%20%7B%7D%22%2C%20i)%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20let%20out%20%3D%20String%3A%3Afrom(%22Thread%20%22)%20%2B%20%26i.to_string()%20%2B%20%22%5Cn%22%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20s.lock().unwrap().push_str(%26out)%3B%0A%20%20%20%20%20%20%20%20%7D)%3B%0A%20%20%20%20%20%20%20%20childs.push(child)%3B%0A%20%20%20%20%7D%0A%0A%20%20%20%20for%20c%20in%20childs%20%7B%0A%20%20%20%20%20%20%20%20let%20_%20%3D%20c.join()%3B%0A%20%20%20%20%7D%0A%0A%20%20%20%20println!(%22%5CnOutput%3A%5Cn%7B%7D%22%2C%20*(shared.lock().unwrap()))%3B%0A%7D%0A&version=stable&backtrace=0
[24]: https://play.rust-lang.org/?code=use%20std%3A%3Athread%3B%0Ause%20std%3A%3Async%3A%3Ampsc%3B%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20(tx%2C%20rx)%20%3D%20mpsc%3A%3Achannel()%3B%0A%20%20%20%20let%20mut%20childs%20%3D%20vec!%5B%5D%3B%0A%0A%20%20%20%20for%20i%20in%200..10%20%7B%0A%20%20%20%20%20%20%20%20let%20tx%20%3D%20tx.clone()%3B%0A%20%20%20%20%20%20%20%20let%20child%20%3D%20thread%3A%3Aspawn(move%20%7C%7C%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20println!(%22In%20thread%20%7B%7D%22%2C%20i)%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20let%20out%20%3D%20String%3A%3Afrom(%22Thread%20%22)%20%2B%20%26i.to_string()%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20tx.send(out).unwrap()%3B%0A%20%20%20%20%20%20%20%20%7D)%3B%0A%20%20%20%20%20%20%20%20childs.push(child)%3B%0A%20%20%20%20%7D%0A%0A%20%20%20%20for%20c%20in%20childs%20%7B%0A%20%20%20%20%20%20%20%20let%20_%20%3D%20c.join()%3B%0A%20%20%20%20%7D%0A%0A%20%20%20%20println!(%22%5CnOutput%3A%22)%3B%0A%20%20%20%20loop%20%7B%0A%20%20%20%20%20%20%20%20match%20rx.try_recv()%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20Ok(x)%20%3D%3E%20println!(%22%7B%7D%22%2C%20x)%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20Err(_)%20%3D%3E%20break%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%7D%0A&version=stable&backtrace=0
