Date: 2017-04-30
Title: Rust: Rust+C (parte 2), Llamando código C desde Rust
Tags: wadobo, rust, programming, ffi, C
Category: blog
Slug: rust-ffi2
Gravatar: 8da96af78e0089d6d970bf3760b0e724

En el [artículo anterior][2] hablamos sobre la integración de Rust con C,
sobre cómo llamar a código Rust desde C. Este artículo es la segunda parte
sobre integración de Rust con C, donde veremos cómo hacer la operación
inversa, llamar código C desde Rust.

Esto puede ser muy útil si tenemos librerías de terceros que tenemos que
usar, así podemos hacer un wrapper en Rust fácilmente. En cuanto a
rendimiento no es muy útil, ya que en Rust se puede escribir código tan
eficiente o más que en C.

## Llamando a código C desde Rust

Supongamos que tenemos una función en C, que queremos llamar desde nuestro
código en Rust:

```c
#include <stdio.h>


void repeat(char *str, int n) {
    int i;

    for (i=0; i<n; i++) {
        printf("%s\n", str);
    }
}
```

En el [primer artículo][2] se habla sobre cómo pasar tipos de datos más
complejos, de momento, para este ejemplo tenemos tipos básicos, como un
puntero a char y un int, que se traducen en Rust como **\*const u8** y **i32**.

Esta función la podemos llamar desde nuestro código Rust de la siguiente
manera:

```rust
extern crate libc;

#[link(name = "cffi")]
extern {
    fn repeat(s: *const u8, n: i32);
}

fn main() {
    unsafe {
        repeat("Salida desde C\0".as_ptr(), 5);
    }
}
```

Lo primero a resaltar de este código Rust es el atributo "link". Esto le
dice al compilador de Rust que tiene que enlazar con la biblioteca libcffi.
La otra cosa que hay que tener en cuenta es el uso de unsafe. Cuando
llamamos a una función en C, siempre tendremos que usar usanfe, porque ese
código no está controlado por el compilador Rust y por tanto no podemos
considerarlo seguro.

Si queremos limitar el uso de unsafe, la práctica recomendada es la
creación de una interfaz segura:

```rust
extern crate libc;

#[link(name = "cffi")]
extern {
    fn repeat(s: *const u8, n: i32);
}

fn safe_repeat(s: &str, n: i32) {
    let st = String::from(s) + "\0";
    unsafe {
        repeat(st.as_ptr(), n);
    }
}

fn main() {
    unsafe {
        repeat("Salida desde C\0".as_ptr(), 5);
    }

    safe_repeat("Safe", 10);
}
```

Para este ejemplo podemos convertir la cadena a una cadena de C, terminada
en \0, además de ocultar la función no segura.

## Compilando código C con Cargo

Para compilar código C utilizando Cargo se puede utilizar el [crate gcc][3],
que ofrece una interfaz Rust para llamar a gcc, en combinación con el
script de compilación [build.rs][4], que es llamado por cargo por defecto antes
de compilar.

Por ejemplo, si tenemos un fichero 'lib.c' y queremos que se compile cuando
ejecutamos **cargo build**, sólo tenemos que añadir lo siguiente a los ficheros
build.rs y Cargo.toml:

```
# Cargo.tolm
...
[build-dependencies]
gcc = "0.3"
...
```

```rust
/// build.rs
extern crate gcc;

fn main() {
    gcc::compile_library("libcffi.a", &["src/lib.c"]);
}
```

Todo el código de ejemplo se puede encontrar en [github][6].

## Integración con otros lenguajes

Esta integración con C tan sencilla por parte de Rust nos permite utilizar
el gran catálogo de bibliotecas que hay en C. Pero además de esto, dado que
C es el lenguaje común entre casi todos los lenguajes modernos, podemos
llamar a código Rust fácilmente desde casi cualquier lenguaje, simplemente
creando una interfaz C y compilando a una biblioteca en formato C.

Hay un [repositorio en github][5] donde se pueden encontrar una serie de
ejemplos sencillos de integración de Rust con Python, Perl, Ruby, Haskell,
etc.

[1]: https://doc.rust-lang.org/book/ffi.html
[2]: http://danigm.net/rust-ffi1.html
[3]: https://crates.io/crates/gcc
[4]: http://doc.crates.io/build-script.html

[5]: https://github.com/alexcrichton/rust-ffi-examples
[6]: https://github.com/danigm/rust-ffi
