Date: 2017-02-25
Title: Rust: Funciones y closures
Tags: wadobo, rust, programming
Category: blog
Slug: rust-funcs
Gravatar: 8da96af78e0089d6d970bf3760b0e724

En Rust se pueden definir [funciones][1], a nivel global, como parte de una
implementación de una estructura o como parte de una interfaz o *trait*,
además, se pueden pasar como parámetros a otras funciones, se puede decir
que una función también define un nuevo tipo.

La estructura de una definición simple es la siguiente:

```rust
fn nombre_funcion(arg1: i32, arg2: &Vec<i32>) -> i64 {
    // cuerpo de la función
}
```

Se usa la palabra clave "*fn*", después va el nombre de la función, que
normalmente se usa notación en minúsculas y con separando palabras con
guión bajo, el llamado "*snake_case*". Entre paréntesis van todos los
argumentos, separados por coma. Después si la función devuelve algo, va el
operador "*->*" y luego se define el tipo de retorno.

Tanto la lista de argumentos como el retorno son opcionales, pudiendo
definir funciones que no reciben argumentos y no devuelven nada:

```rust
fn nombre_funcion() {
    // cuerpo
}
```

Las funciones se pueden definir dentro de cualquier *scope* y serán
visibles sólo durante ese *scope*, por tanto en *Rust* se pueden definir
funciones a nivel global, dentro de una función, o dentro de otro *scope*,
cualquiera. En ese sentido es muy similar a como se pueden definir las
funciones en Python.

## Argumentos

La definición de argumentos en las funciones en Rust no difiere mucho de
otros lenguajes, como C o C++. Se definen como pares,
**identificador: tipo**. El *identificador* es el nombre de la variable, y
como Rust es fuertemente tipado, hay que definir el tipo de todo argumento.
El tipo puede llevar modificadores *&* o *&mut* para modificar la
forma en la que se pasan esas funciones, y el identificador puede llevar el
modificador *mut*, que sería similar al funcionamiento en una asignación
*let*.

```rust
fn add_element(mut a: Vec<i32>) -> Vec<i32> {
        a.push(1);
        a
}

let v = vec![];
let v2 = add_element(v);
println!("{:?}", v2);
```

En este ejemplo se ve cómo se pasa un vector como parámetro, y con el
modificador *mut* es editable dentro de la función, al no llevar
modificadores el tipo, el valor se mueve, por lo que en este ejemplo, *v*
no se puede usar después de la llamada a la función, ya que el propietario
de la memoria pasa a la variable *a* de la función, y luego al devolverse,
se pasa a la variable *v2*. Si no devolviéramos nada en la función, el
vector se liberaría al finalizar la llamada a la función.

El compilador da bastante información en caso de que intentáramos usar *v*
después de la llamada a la función:

```bash
error[E0382]: use of moved value: `v`
 --> src/main.rs:9:27
  |
8 |     let v2 = add_element(v);
  |                   - value moved here
9 |     println!("{:?} {:?}", v, v2);
  |                           ^ value used here after move
  |
  = note: move occurs because `v` has type `std::vec::Vec<i32>`, which does not implement the `Copy` trait
```

Para poder seguir usando *v* lo suyo es pasar el argumento como una
referencia, para hacer un *borrow* en lugar de un *move*.

```rust
fn add_element(v: &mut Vec<i32>, el: i32) {
    v.push(el);
}

let mut v = vec![1,2];
add_element(&mut v, 3);
println!("{:?}", v);
```

Aquí se pasa una referencia *&* editable *mut*, por lo que se hace un
*borrow* de la memoria, durante la llamada, y por tanto, al terminar la
llamada, se puede volver a usar *v*.

## Devolución

El tipo de la devolución de una función, como he explicado antes, se define
con "*->*" y a diferencia de los argumentos, no es necesario especificar
un identificador, sólo el tipo.

En una función en Rust, la última línea, si no termina en "*;*" es lo que
se devuelve, aunque también se puede hacer un *return* explícito, para
que quede más claro o para los *early returns*, por ejemplo, estas dos
definiciones son similares:

```rust
fn f1() -> Vec<i32> {
    let v = vec![];
    v.push(1);
    v.push(2);
    v
}

fn f2() -> Vec<i32> {
    let v = vec![];
    v.push(1);
    v.push(2);
    return v;
}
```

En Rust sólo es posible devolver un elemento, aunque se puede simular la
devolución múltiple devolviendo una tupla y haciendo la asignación con
*patter matching*:

```rust
fn dos_ultimos(v: &mut Vec<i32>) -> (i32, i32) {
    (v[v.len() - 2], v[v.len() - 1])
}

let mut v: Vec<i32> = vec![1,2,3,4,5];
let (x, y) = dos_ultimos(&mut v);
println!("{} {}", x, y);
```

El tipo de devolución, al igual que los argumentos, se *mueven* por
defecto, pero se puede devolver una referencia, *&*, o una referencia
mutable *&mut*, para que sea un *borrow*.

```rust
fn addel(v: &mut Vec<i32>, el: i32) -> &mut Vec<i32> {
    v.push(el);
    v
}

let mut v2 = addel(&mut v, 6);
let v3 = addel(&mut v2, 7);
println!("{:?}", v3);
```

## Tipos genéricos y *traits*

Las funciones también pueden recibir tipos genéricos, para poder definir
funciones que valgan para diferentes tipos:

```rust
fn fn_generica<T, K>(x: T, y: T, z: K) -> K {
    // definición
}

let ret: Vec<i32> = fn_generica(3, 5, vec![1, 2, 3]);
```

En esta función de ejemplo se definen dos tipos genéricos, *T* y *K*, y se
ve el uso en los argumentos, *x* e *y* son de tipo *T* y *z* y el valor de
retorno son de tipo *K*. Esta función acepta cualquier tipo para *T* y *K*,
en el ejemplo se hace la llamada con *T = i32* y *K = Vec&lt;i32>*.

Así tal cual, no se puede hacer gran cosa con sólo tipos completamente
genéricos, se pueden crear estructuras con estos tipos y poco más, porque
al ser completamente genéricos no se puede acceder a ningún atributo o
método de estos tipos.

Para un uso más específico se pueden usar los *traits*, de forma similar a
los tipos genéricos, para poder definir funciones genéricas que hagan uso
de esas interfaces:

```rust
extern crate core;
use core::cmp::Ordering;

fn main() {
    fn mayor<T: Ord>(x: T, y: T) -> T {
        match x.cmp(&y) {
            Ordering::Less => y,
            _ => x
        }
    }
    println!("{:?}", mayor(3, 6));
}
```

También existe una sintaxis más clara, para cuando hay muchos tipos
genéricos, no tener que especificar todos los tipos entre el nombre de la
función y la lista de argumentos, sólo los nombres de los tipos. Para esto
se usa la palabra clave *where*:

```rust
fn mayor<T, K, L, H>(x: T, y: &K, z: &mut L) -> Option<H>
    where T: Ord,
          K: Iterator,
          L: Clone + Debug,
          H: Default {
    // cuerpo de la función
}
```

En esta cabecera de ejemplo se definen cuatro tipos genéricos, el primero
tiene que implementar *Ord*, el segundo *Iterator*, el tercero *Clone* y
*Debug* y el cuarto *Default*.

## Lifetimes

Además de los tipos genéricos, dentro del mayor/menor, *&lt;>*, puede ir
información relativa a los tiempos de vida. El ejemplo típico es una
función que recibe dos referencias y devuelve una referencia, todo del
mismo tipo, el compilador no tiene información suficiente para saber con
qué variable se relaciona la referencia devuelta, por lo que hay que anotar
la función, el mismo compilador te dirá cuando no sea capaz de inferir los
lifetimes:

```rust
fn skip_prefix(x: &str, y: &str) -> &str {
    return x.trim_left_matches(y)
}

println!("{}", skip_prefix("hola", "ho"));
```

```bash
error[E0106]: missing lifetime specifier
 --> src/main.rs:2:41
  |
2 |     fn skip_prefix(x: &str, y: &str) -> &str {
  |                                         ^ expected lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but the signature does not say whether it is borrowed from `x` or `y`
```

Así que es necesario añadir el lifetime:

```rust
fn skip_prefix<'a>(x: &'a str, y: &str) -> &'a str {
    x.trim_left_matches(y)
}

println!("{}", skip_prefix("hola", "ho"));
```

Los lifetimes se definen con letras en minúsculas y con un apóstrofe, en
este ejemplo se define el lifetime *'a*, pero se pueden definir tantos
lifetimes como sean necesarios. En este caso, como devolvemos una subcadena
de *x*, pues tiene que coincidir el *lifetime* de estos dos, si intentamos
definir el lifetime con *y* en lugar de con *x*, el compilador se nos
quejará:

```rust
fn skip_prefix<'a>(x: &str, y: &'a str) -> &'a str {
    return x.trim_left_matches(y)
}
```

```bash
error[E0495]: cannot infer an appropriate lifetime for autoref due to conflicting requirements
 --> src/main.rs:3:18
  |
3 |         return x.trim_left_matches(y)
  |                  ^^^^^^^^^^^^^^^^^
  |
help: consider using an explicit lifetime parameter as shown: fn skip_prefix<'a>(x: &'a str, y: &'a str) -> &'a str
 --> src/main.rs:2:5
  |
2 |       fn skip_prefix<'a>(x: &str, y: &'a str) -> &'a str {
  |  _____^ starting here...
3 | |         return x.trim_left_matches(y)
4 | |     }
  | |_____^ ...ending here
```

Como se puede ver en el mensaje de error, el compilador es bastante
inteligente en este caso y nos da incluso una definición que sería válida
para nuestro caso.

# [Closures][2]

Se pueden definir funciones que reciban una función como parámetro, estas
funciones se llaman *closures* y se definen de forma similar a los tipos
genéricos y los *traits*:

```rust
fn apply<T, K, F>(f: F, x: T) -> K
    where F: Fn(T) -> K {
    f(x)
}
println!("{}", apply(|x: i32| x + 1, 3));
```

En este ejemplo hay dos cosas claves que no he explicado hasta ahora, el
primero es el tipo *F*, que se define como *Fn(T) -> K*, con esta sintaxis
definimos que *F* tiene que ser una función o *closure* que reciba un
parámetro de tipo *T* y devuelva un tipo *K*.

La segunda sintaxis extraña está dentro de la llamada a *apply*, como
primer argumento debe recibir la función de tipo *F* y le pasamos *|x: i32|
x + 1*, que en realidad es esa definición.

Un *closure* se define con las barras verticales, para definir los
argumentos y sus tipos, y después se define el cuerpo de la función,
pudiendo obviar los corchetes cuando es una definición muy simple, como en
el ejemplo.

También se puede asignar un *closure* a una variable para luego pasarlo en
la llamada:

```rust
let c = |x: Vec<i32>| {
    for (i, l) in x.iter().enumerate() {
        if *l == 5 {
            return Some(i);
        }
    }
    None
};
println!("{:?}", apply(c, vec![1,5,3]));
```

En este caso, es lo mismo que definir la función de forma normal y luego
pasarla por parámetro:

```rust
fn c(x: Vec<i32>) -> Option<i32> {
    for (i, l) in x.iter().enumerate() {
        if *l == 5 {
            return Some(i as i32);
        }
    }
    None
};

println!("{:?}", apply(c, vec![1,5,3]));
```

Por lo que asignar *closures* a variables tiene poco sentido, en realidad
son útiles cuando se definen directamente en la llamada, para no tener que
definir una función con nombre para algo que sólo se llamará una vez.

## Move en closures

Cuando se define un *closure* se pueden usar variables que estén en el
ámbito, y por defecto se cogen como *borrow*, por lo que el *closure*
estará ligado a las variables que use.

```rust
let mut num = 5;
let plus_num = |x: i32| x + num;
let y = &mut num;
```

Este código, sacado de la doc de Rust, no compila, porque se intenta hacer
una referencia mutable en la asignación de *y*, cuando ya existe una
referencia a *num* dentro del *closure*.

Para evitar este problema se usa el *move*, que funciona igual que el paso
de argumentos sin modificadores, es decir, para los tipos que implementen
el *trait* copy se copiará el valor, para los demás, se hará *move* de la
propiedad de la memoria.

```rust
let mut num = 5;
let plus_num = move |x: i32| x + num;
let y = &mut num;
```

Un caso típico de *move* en *closure* es cuando se lanza un hilo:

```rust
use std::thread;

fn main() {
    let mut threads: Vec<thread::JoinHandle<()>> = vec![];
    for i in 1..10 {
        let t = thread::spawn(move || {
            println!("Hilo {}", i);
        });
        threads.push(t);
    }

    for t in threads {
        t.join();
    }
}
```

En este ejemplo se lanzan 9 hilos, la variable *i* se usa dentro del
*closure*, que al definirse con *move* será una copia, ya que es un *i32* y
este tipo implementa *Copy*, si no se pone el *move*, el compilador se
quejará, ya que la variable *i* sólo existe en el scope del bucle, y el
otro hilo puede existir más allá del bucle.

## Devolución de closures

También se pueden [devolver closures][3], pero no es algo trivial, hay que
encapsularlas en un *Box* para que se pueda devolver y para evitar los
problemas con la gestión de la memoria de Rust.

[1]: https://doc.rust-lang.org/book/functions.html
[2]: https://doc.rust-lang.org/book/closures.html
[3]: https://doc.rust-lang.org/book/closures.html#returning-closures
