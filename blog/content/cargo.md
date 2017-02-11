Date: 2017-02-11
Title: Cargo: Dependencias, crates y módulos en Rust
Tags: wadobo, rust, programming, cargo
Category: blog
Slug: cargo
Gravatar: 8da96af78e0089d6d970bf3760b0e724

## Cargo

Rust viene con una herramienta por defecto para gestionar dependencias,
crear proyectos y realizar otras tareas comunes, esta herramienta se llama
*[Cargo][2]*.

Esta herramienta ofrece algo similar a lo que sería *pip* y *virtualenv* en
python, pero además realiza otras tareas como los test y la generación de
documentación.

Por lo tanto Cargo sirve para:

 * Crear nuevos proyectos Rust a partir de templates (**new**, **init**)
 * Compilar el proyecto actual (**run**, **build**, **install**)
 * Gestionar dependencias del proyecto (**search**, **update**)
 * Publicar el proyecto en [crates.io][3] (**publish**)
 * Generar la documentación del proyecto (**doc**)
 * Ejecutar los tests (**test**, **bench**)

Es una herramienta genial que engloba casi todas las utilidades para llevar
un proyecto de forma sencilla. Cuando empecé a trastear con Rust es una de
las cosas que más me gustó, porque te simplifica la vida a la hora de usar
el lenguaje y en *crates.io* cada vez hay más módulos, lo que enriquece a
Rust, ya que puedes encontrar fácilmente bibliotecas para casi todo.

### Creando un proyecto

Con Cargo se pueden crear por defecto dos tipos de proyectos, un ejecutable
o una biblioteca. La diferencia básica es el punto de entrada, por defecto
el fichero *src/main.rs* es el punto de entrada, lo que se ejecuta, para los
proyectos ejecutables, y el fichero *src/lib.rs* es el punto de entrada para
las bibliotecas.

```bash
$ cargo new --bin ejemplo
     Created binary (application) `ejemplo` project
```

Esto nos crea un directorio *ejemplo* con los ficheros básicos:

```bash
$ tree ejemplo
ejemplo/
├── Cargo.toml
└── src
    └── main.rs
```

El comando además de estos ficheros también nos crea, por defecto, un
repositorio git, por lo tanto existen los ficheros ocultos *.git* y
*.gitignore*. Este comportamiento se puede modificar con la configuración
*--vcs*, que puede ser: **git**, **hg** o **none**.

```bash
$ ls -la ejemplo/
total 8
drwxr-xr-x. 4 danigm danigm 120 feb 11 08:59 .
drwxr-xr-x. 3 danigm danigm  60 feb 11 08:59 ..
-rw-r--r--. 1 danigm danigm 117 feb 11 08:59 Cargo.toml
drwxr-xr-x. 6 danigm danigm 180 feb 11 08:59 .git
-rw-r--r--. 1 danigm danigm   7 feb 11 08:59 .gitignore
drwxr-xr-x. 2 danigm danigm  60 feb 11 08:59 src
```

Aparte del vcs, se crean dos ficheros, el fichero *Cargo.toml*, que es el
fichero de configuración, y el fichero *src/main.rs*, que es donde va el
código, el punto de entrada que se usará para generar el binario.

```bash
$ cat ejemplo/Cargo.toml
[package]
name = "ejemplo"
version = "0.1.0"
authors = ["Daniel García Moreno <danigm@wadobo.com>"]

[dependencies]
```

Como vemos en el fichero de configuración por defecto van una serie de
variables básicas con el nombre, la versión y los autores, aunque hay
muchas más cosas que se pueden especificar [aquí][4].

También está aquí el listado de dependencias, que por defecto está vacío,
pero que iremos rellenando según vayamos necesitando módulos externos y
*Cargo* se encargará de descargar esas dependencias y compilarlas por
nosotros.

### Primera ejecución

Una vez creado el proyecto, ejecutarlo es tan fácil como:

```bash
$ cd ejemplo
$ cargo run
   Compiling ejemplo v0.1.0 (file:///tmp/cargo/ejemplo)
    Finished debug [unoptimized + debuginfo] target(s) in 0.38 secs
     Running `target/debug/ejemplo`
Hello, world!
```

Esto compila el proyecto y lo ejecuta, si no ha cambiado, simplemente lo
ejecuta, no se pierde el tiempo compilando.

Como se puede ver, lo que ejecuta es lo que hay dentro del fichero
*src/main.rs*:

```rust
fn main() {
    println!("Hello, world!");
}
```

El comando *run* compila en modo debug, esto quiere decir que no está
optimizado el ejecutable que se genera. Para generar un ejecutable final se
puede usar el comando:

```bash
$ cargo build --release
   Compiling ejemplo v0.1.0 (file:///tmp/cargo/ejemplo)
    Finished release [optimized] target(s) in 0.15 secs
```

Los binarios se generan en el directorio *target*, en su correspondiente
carpeta según sean de *debug* o *release*, **target/debug/ejemplo** y
**target/release/ejemplo**.

## Usando dependencias externas

Como hemos visto antes, el listado de dependencias está vacío por defecto.
Vamos a añadir alguna:

```toml
# fichero Cargo.toml
...
[dependencies]
time = "*"
regex = "0.2"
```

Es muy fácil añadir dependencias, que se pueden buscar con el comando
*cargo search* o directamente en la web [crates.io][3], y además, cargo
soporta una [sintaxis rica][5] para especificar números de versión, además
de poder especificar otras fuentes para descargar las dependencias, por si
son privadas o no están en [crates.io][3].

Si ejecutamos ahora *cargo build*, se descargarán las dependencias y se
compilarán.

```bash
$ cargo build
    Updating registry `https://github.com/rust-lang/crates.io-index`
 Downloading aho-corasick v0.6.2
   Compiling libc v0.2.20
   Compiling utf8-ranges v1.0.0
   Compiling void v1.0.2
   Compiling regex-syntax v0.4.0
   Compiling unreachable v0.1.1
   Compiling memchr v1.0.1
   Compiling time v0.1.36
   Compiling thread-id v3.0.0
   Compiling thread_local v0.3.2
   Compiling aho-corasick v0.6.2
   Compiling regex v0.2.1
   Compiling ejemplo v0.1.0 (file:///tmp/cargo/ejemplo)
    Finished debug [unoptimized + debuginfo] target(s) in 11.35 secs
```

El fichero *Cargo.lock* contiene la información de todas las dependencias
descargadas y su versión, permitiendo así compilaciones exactamente
iguales.

## [Crates][1]

Hemos hablado de dependencias y *crates* y hemos visto cómo *cargo*
gestiona e instala las dependencias de forma sencilla.

*Crate* es como se llaman a las bibliotecas en *Rust*. Traducido
literalmente significa *Cajón*, y se podría decir que un *crate* es un
proyecto Rust completo, un fichero *Cargo.toml* que especifica su nombre,
versión, etc y una serie de ficheros en *src* donde se definen los
diferentes *módulos*.

Para usar un *crate* en nuestro proyecto se usa *extern crate XXX*, así
podemos usar las dependencias que hemos añadido anteriormente, sería algo
similar al *import* de python o al *include* de C o C++.

```rust
extern crate time;

fn main() {
    if let Ok(now) = time::strftime("%c", &time::now()) {
        println!("Hello, world! {}", now);
    }
}
```

En el momento en el que declaramos el *extern crate time* ya es posible
utilizar el módulo time.

Además del uso de *extern crate*, en Rust existe otra palabra clave para
*importar* módulos o funciones externas en el ámbito local, algo similar a
lo que en python se hace con *from X import Y*. En Rust la sintaxis
utilizada es *use*, por ejemplo en nuestro caso podríamos tener:

```rust
extern crate time;

use time::{now, strftime};

fn main() {
    if let Ok(n) = strftime("%c", &now()) {
        println!("Hello, world! {}", n);
    }
}
```

Hemos usado aquí una sintaxis compacta, pero se puede definir uno por línea
o incluso todo a la vez:

```rust
use time::now;
use time::strftime as format_date;
use time::*;
```

## Módulos

Como hemos visto, en Rust las bibliotecas se llaman *crates* y en estas
bibliotecas puede haber diferentes agrupaciones que se llaman *modules*, o
módulos en español. Así que tenemos un cajón que tiene uno o más módulos
dentro.

El módulo por defecto se define en el fichero *src/lib.rs*, donde se pueden
definir directamente funciones, estructuras, etc. o submódulos.

Por defecto en Rust todo es privado, por lo que si queremos que desde fuera
de un módulo se pueda usar algo definido dentro, debemos usar la palabra
clave *pub*.

Podemos definir un par de funciones en un nuevo fichero *src/lib.rs*, para
usar después en *src/main.rs*:

```rust
extern crate time;

pub fn fecha() -> String {
    let mut fecha = String::from("");
    if let Ok(n) = time::strftime("%d/%m/%Y", &time::now()) {
        fecha = n.clone();
    }
    fecha
}

pub fn hora() -> String {
    let mut hora = String::from("");
    if let Ok(n) = time::strftime("%H:%M", &time::now()) {
        hora = n.clone();
    }
    hora
}
```

En nuestro proyecto de ejemplo, tenemos el *crate*, que es el proyecto en
sí, y el módulo por defecto, que es *src/lib.rs*, donde hemos definido dos
funciones públicas, *fecha* y *hora*. Esto lo podemos utilizar en nuestro
ejecutable, exactamente igual que usamos una dependencia externa, con el
uso de *extern crate*.

```rust
extern crate ejemplo;

fn main() {
    println!("fecha: {}", ejemplo::fecha());
    println!("hora: {}", ejemplo::hora());
}
```

## Submódulos

En el ejemplo anterior hemos visto cómo se define el módulo por defecto de
un *crate*, que no es más que el fichero *src/lib.rs*. Pero en cualquier
proyecto que no sea un ejemplo habrá que definir más de un módulo, no puede
estar todo junto en el mismo.

Para definir submódulos en Rust se puede usar **mod**, que sirve
exactamente para definir submódulos:

```rust
// fichero src/lib.rs
pub mod fecha {
    extern crate time;
    pub fn ahora() -> String {
    //...
    }
}

pub mod hora {
    extern crate time;
    pub fn ahora() -> String {
    //...
    }
}
```

En este ejemplo se definen dos módulos, *fecha* y *hora*. La única
diferencia con el caso anterior es que ahora podemos agrupar en módulos las
diferentes funciones que definamos. También hay que tener en cuenta que en
cada módulo en ámbito es diferente, de ahí la necesidad de hacer el
*extern crate time* en los dos módulos, aunque estén en el mismo fichero.

El uso en el *main.rs* sería similar:

```rust
extern crate ejemplo;

fn main() {
    println!("fecha: {}", ejemplo::fecha::ahora());
    println!("hora: {}", ejemplo::hora::ahora());
}
```

### Módulos en ficheros separados

Pero este uso tiene poca utilidad real, normalmente los módulos han de ir
en ficheros separados o incluso en carpetas, creando una jerarquía de
ficheros que simboliza exactamente la jerarquía de los módulos.

En nuestro ejemplo, podemos crear un nuevo fichero con el contenido del
módulo *fecha*, un fichero llamado *src/fecha.rs*.

```rust
// fecha.rs
extern crate time;
pub fn ahora() -> String {
    //...
}
```

Se puede observar que ya no es necesario el uso de *mod*, puesto que al
estar en un fichero separado, es implícito.

Y en el fichero módulo por defecto sólo tendremos que declarar este módulo
como público para que sea accesible desde *main.rs*.

```rust
// lib.rs
pub mod fecha;
pub mod hora;
```

De esta forma ya tenemos nuestros módulos en ficheros diferentes y son
accesibles desde fuera.

Además de ficheros con el nombre del módulo, en Rust se pueden declarar
carpetas, y dentro de esa carpeta debe existir el fichero *mod.rs*, sería
algo similar a los ficheros *__init__.py* en los módulos python.

Podríamos tener una estructura de ficheros tal que así:

```bash
ejemplo/
├── Cargo.toml
└── src
    ├── main.rs
    ├── lib.rs
    ├── fecha.rs
    └── hora
        ├── mod.rs
        ├── local.rs
        └── utc.rs
```

 * **main.rs** es el ejecutable, si estamos hablando de una biblioteca, no
   existiría este fichero.
 * **lib.rs** define el módulo principal, este fichero puede no existir si
   estamos hablando de un crate ejecutable, sin módulos propios.
 * **fecha.rs** un módulo más del proyecto, que para ser accesible debe
   debe estar declarado en el módulo por defecto.
 * **hora** es una carpeta que contiene otro módulo, que al igual que
   *fecha.rs* debe estar definido en *lib.rs* para ser accesible.
 * **mod.rs** definición del módulo *hora*.
 * **local.rs y utc.rs** submódulos de hora, que deben estar definidos en
   *mod.rs* para ser accesibles.

Además del uso de módulos desde fuera, por ejemplo en el *main.rs* o si lo
usamos como dependencia en otro proyecto, pueden existir módulos internos
en el proyecto, que no exportemos como públicos, y que sólo se usen de
manera interna. Por defecto las importaciones son relativas al módulo por
defecto:

```rust
use fecha; // -> importación relativa al módulo actual
use ::fecha; // -> importación absoluta, llevaría a src/fecha.rs
use self::fecha; // -> relativo al módulo actual, por ejemplo no funcionaría
		 // -> si se usara esto dentro de *hora/mod.rs*, aunque sí
		 // -> en otro módulo al nivel de fecha.rs
use super::fecha; // -> con super se puede acceder al módulo padre
```

Con estas declaraciones podemos hacer uso de unos módulos en otros, variará
lo que tengamos que usar según nuestra estructura de ficheros.

También se puede cambiar el nombre de un módulo en una declaración *use*,
para evitar conflictos de nombres, con la palabra reservada *as*:

```rust
extern crate ejemplo;

use ejemplo::fecha::ahora as fecha;
use ejemplo::hora::ahora as hora;

fn main() {
  println!("{} - {}", fecha(), hora());
}
```

La verdad es que el sistema de módulos de *Rust* es muy parecido al de
python, podríamos decir que *self* sería el *from . import* de python y el
super podría ser *from .. import*.


[1]: https://doc.rust-lang.org/book/crates-and-modules.html
[2]: http://doc.crates.io/guide.html
[3]: http://crates.io
[4]: http://doc.crates.io/manifest.html
[5]: http://doc.crates.io/specifying-dependencies.html
