Date: 2017-04-22
Title: Rust: Rust+C (parte 1), Llamando código Rust desde C
Tags: wadobo, rust, programming, ffi, C
Category: blog
Slug: rust-ffi1
Gravatar: 8da96af78e0089d6d970bf3760b0e724


Rust es un lenguaje cuyo objetivo principal es sustituir o reemplazar
código escrito en C o C++ con código más seguro e igual de eficiente a
nivel de rendimiento.

Sin embargo, no es fácil tomar la decisión de migrar todo un proyecto
escrito en C/C++ a Rust, de la noche a la mañana. En proyectos pequeños o
con poca actividad, quizás sí sea fácil hacer una reescritura completa,
pero en la mayoría de proyectos no es viable.

Sin embargo con Rust se puede hacer una migración incremental, implementar
la nueva funcionalidad en Rust, o implementar tan sólo las partes que
requieran una seguridad extra en la gestión de memoria, y esto es posible
gracias a que Rust se puede integrar muy fácilmente con C y C++ con el
llamado [**ffi** o **Foreign Function Interface**][1].

## Llamando a código Rust desde C

Empecemos por lo más sencillo. Supongamos que tenemos una base de código en
C, y queremos comenzar una migración, reimplementando algunas partes, o
alguna biblioteca interna con Rust. Esto es realmente sencillo siempre y
cuando las funciones Rust sean independientes, ya que se pueden llamar
directamente.

```rust
//lib.rs

#[no_mangle]
pub extern fn suma(a: i32, b: i32) -> i32 {
    println!("sumando dentro de rust {} + {}", a, b);
    a + b
}
```

Para poder acceder desde C a estas funciones debemos añadir algunos
detalles, como el atributo *"#[no_mangle]"*, y el modificador *extern* en
la definición de la función.

Supongamos ahora que tenemos un código en C donde queremos hacer uso de
esta función definida en Rust:

```c
// example1.c

#include <stdio.h>

int suma(int a, int b);

int main(int argc, char **argv) {
    int a = 3, b = 2, s = 0;

    s = suma(a, b);
    printf("%d + %d = %d", a, b, s);
    return 0;
}
```

Como vemos, declaramos la función, *suma* en el código C, pero no añadimos
la implementación, ya que usaremos la implementación Rust.

Para poder compilar este código C, tenemos que tener el código Rust
compilado en forma de [biblioteca compatible][2] con C, podemos hacerlo como
staticlib (.a) o como cdylib (.so).

```bash
$ rustc --crate-type staticlib lib.rs -o librust.a
```

Con esto tenemos el fichero .a compilado con la implementación de la
función suma, ahora tan sólo tenemos que compilar nuestro fichero C para
que haga uso de esta implementación:

```bash
$ gcc -Wl,--gc-sections -lpthread example1.c librust.a -o example1
$ ./example1

sumando dentro de rust 3 + 2
3 + 2 = 5
```

### Devolución de tipos más complejos, structs

Trabajar con enteros es muy *sencillo*, ya que tenemos compatibilidad de
tipos, i32 e int. Sin embargo normalmente tendremos otros tipos más
complejos que querremos pasar a nuestras funciones Rust, o que querremos
devolver.

En Rust se pueden definir estructuras compatibles con C añadiendo un
atributo, al igual que en las definiciones de funciones, pero en este caso
sería *"#[repr(C)]"*.

```rust
use std::slice;
use std::str;

#[repr(C)]
pub struct Dato {
    n: i32,
    cadenac: *const u8,
    cadenarust: String,
    vec: Vec<i32>,
}

#[no_mangle]
pub extern fn dato_crear(n: i32, cadenac: *const u8, l: usize) -> *mut Dato {
    let mut s = unsafe {
        String::from(str::from_utf8(slice::from_raw_parts(cadenac, l)).unwrap())
    };
    s = s + ", desde Rust";
    let v = vec![n, n, n];
    let dato = Dato{n: n, cadenac: cadenac, cadenarust: s, vec: v};

    Box::into_raw(Box::new(dato))
}

#[no_mangle]
pub extern fn dato_print(dato: *mut Dato) {
    unsafe {
        println!("cadena: {}", (*dato).cadenarust);
        println!("vec: {:?}", (*dato).vec);
    }
}

#[no_mangle]
pub extern fn dato_destruir(dato: *mut Dato) {
    unsafe {
        let _ = Box::from_raw(dato);
    }
}
```

En este ejemplo definimos una estructura, **Dato**, que tiene varios
campos, algunos compatibles con C, **n** y **cadenac**, y otros que no,
**cadenarust** y **vec**.

Además definimos una serie de funciones que nos permitirán trabajar con
esta estructura desde C, para la creación **dato\_crear**, para acceder a
elementos Rust del dato **dato\_print** y para liberar la memoria
**dato\_destruir**.

Hay que tener en cuenta que para poder trabajar en C con esta estructura,
en la creación del dato no devolvemos el dato creado, sino un puntero a
este **\*mut Dato** y además, para evitar que Rust elimine la memoria
asociada a esta estructura y podamos acceder desde C, la metemos en un
**Box** y lo convertimos a puntero **into\_raw**.

El meter el dato en un [**Box**][4], lo que hacemos es alojar esta memoria
en el *heap* en lugar de en el *stack*. Luego, usando el
[**into\_raw**][5], Rust se olvida de esta memoria y nos devuelve un
puntero, así que a partir de ahora, nosotros seremos responsables de esta
memoria y tenemos que tener especial cuidado, porque podremos tener *memory
leaks* si no liberamos esto.

Para liberar esta memoria que ahora gestionamos manualmente desde Rust,
podemos utilizar la operación inversa al **into\_raw**, que es el
**from\_raw**, que hace justamente lo contrario, recibe un puntero y nos
devuelve un **Box**, y cuando Rust elimine esta variable, la memoria se
liberará, de ahí el uso de esta función en **dato\_destruir**.

A parte de la creación y destrucción usando **Box**, también se define una
función intermedia en Rust, que hace uso de esta estructura en código Rust,
en este caso, para imprimir la cadena y el vector.

Este código está englobado dentro de un bloque **unsafe**, porque cada vez
que dereferenciamos un puntero, el código es inseguro, y debemos marcarlo
como tal. El código es inseguro, porque el compilador no puede asegurar que
ese puntero que recibimos apunte realmente a memoria válida, y en esas
partes dentro de **unsafe** es donde podríamos encontrarnos los problemas
de **segmentation fault** y demás.


```c
// example2.c

#include <stdint.h>
#include <stdio.h>
#include <string.h>

struct Dato {
    int n;
    char *cadenac;
};

extern struct Dato* dato_crear(int, char*, int);
extern void dato_print(struct Dato*);
extern void dato_destruir(struct Dato*);

int main (int argc, char **argv) {
    int n = 5;
    char *cadena = "Esto es una cadena C";
    struct Dato *dato = dato_crear(n, cadena, strlen(cadena));

    printf("dato: %s\n", dato->cadenac);
    dato_print(dato);

    dato_destruir(dato);
    return 0;
}
```

Desde C es trivial usar esta estructura y estas nuevas funciones que nos
hemos definido. Tan sólo tendríamos que definir una estructura similar en
código C y definir las cabeceras de las funciones. Desde C podemos acceder
a los parámetros de la estructura compatibles.

Un detalle interesante es que en C no definimos todos los parámetros de la
estructura original de Rust, ya que no vamos a acceder a la cadena Rust ni
al vector, esto funciona porque hemos definido los parámetros compatibles
primero y por tanto al acceder a la memoria es completamente compatible la
estructura Rust y la estructura C.

Para la interoperabilidad entre C y Rust, existe un [crate llamado libc][3],
que define una serie de tipos que se pueden usar en Rust cuando se hace una
interfaz hacia C. En los ejemplos no he utilizado el crate libc, pero
sería recomendable si queremos mantener un código compatible con el mayor
número de plataformas.

Todo el código de ejemplo se puede encontrar en [github][6], con un
Makefile para poder compilarlo fácilmente.

[1]: https://doc.rust-lang.org/book/ffi.html
[2]: https://doc.rust-lang.org/reference.html#linkage
[3]: https://doc.rust-lang.org/libc/x86_64-unknown-linux-gnu/libc/#types
[4]: https://doc.rust-lang.org/std/boxed/
[5]: https://doc.rust-lang.org/std/boxed/struct.Box.html#method.into_raw
[6]: https://github.com/danigm/rust-ffi
