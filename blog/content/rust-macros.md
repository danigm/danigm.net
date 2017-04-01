Date: 2017-04-01
Title: Rust: Macros
Tags: wadobo, rust, programming, macros
Category: blog
Slug: rust-macros
Gravatar: 8da96af78e0089d6d970bf3760b0e724

Rust tiene un sistema de macros muy potente que hacen que el lenguaje sea
mucho más dinámico y permite reutilizar mucho código.

Una macro no es más que una "función" que define cómo se generará código,
todas las macros se ejecutarán en una primera fase de la compilación,
generando el código final Rust que se compilará realmente. Una macro no se
traduce directamente a código máquina, sino que se expande en código fuente
que luego se compila a código máquina.

Si vienes de C, habrás utilizado macros para definir funciones con un
número de argumentos variables y para eso mismo se pueden usar en Rust,
además de para muchos otros casos de uso.

# Sintaxis

```rust
fn main() {
    println!("Hola!");
}
```

Si has hecho un hola mundo en Rust, ya has usado una macro. El signo de
exclamación que se puede ver tras *println* detona que no es una función
cualquiera, sino que es una macro. Gracias a esta sintaxis podemos
diferenciar fácilmente lo que es una macro de lo que es una función
cualquiera.

# Definición de macros

Una macro se define con la palabra clave **macro_rules!** y contiene una
sintaxis diferente al código normal de Rust.

```rust
macro_rules! imprimir {
    ($($x: expr),*) => {
        {
            $(
                print!("{}, ", $x);
            )*
            println!("");
        }
    };
}

imprimir!("hola", "mundo!"); // -> hola, mundo!,
```

Esta macro lo único que hace es imprimir todos los parámetros que recibe,
separados por comas.

No es muy fácil de entender a primera vista, pero la definición de una
macro se puede dividir en tres partes:

 * Definición
 * Matching / Parámetros
 * Expansión

## Definición

```rust
macro_rules! imprimir {
```

Aquí decimos que vamos a definir una macro llamada imprimir, nada más, así
se comienza la definición de una macro.

## Matching / Parámetros

```rust
    ($($x: expr),*) => {
```

Aquí definimos los parámetros que recibe la macro. Es similar a un match,
por lo que se pueden definir varios match diferentes, por ejemplo:

```rust
macro_rules! mimacro {
    () => { ... };
    ($x: expr) => { ... };
    ($x: expr, $y: expr) => { ... };
}
```

En este ejemplo, se define una macro que puede recibir 0, 1 o 2 parámetros,
y se definiría una expansión diferente para cada uno, en este caso he
omitido la expansión, porque ahora mismo no es relevante.

Si entramos en la definición de cada match, vemos que la definición de los
parámetros de la macro es algo parecida a la definición de los parámetros
de una función, se define un nombre **$x** y tras los dos puntos se define
un tipo **expr**. Hay una serie de tipos definidos que se pueden usar en
las macros:

 * item
 * block
 * stmt
 * pat
 * expr
 * ty
 * ident
 * path
 * tt
 * meta

Hay más información sobre esto en la [documentación de Rust][3].

De momento nosotros hemos usado **expr** en nuestro ejemplo, que define una
expresión, y esto es válido para recibir variables.

También es posible definir un número indeterminado de argumentos, osea,
repetición de argumentos, con la expresión:

```rust
$(...),*
```

Con eso podemos decir que esperamos de 0 a n parámetros, por ejemplo:

```rust
$($x: expr),* // de 0 a n expresiones
$($x: expr, $y: expr),* // de 0 a n pares de expresiones
$($x: expr),+ // de 1 a n expresiones
```

Para más detalle sobre la repetición en macros, se puede consultar la
[sección correspondiente][4] del libro de rust.

## Expansión

Después de definir los parámetros de nuestra macro, lo que realmente nos
interesa es definir la expansión, que es en lo que se va a traducir esa
llamada.

```rust
macro_rules! mimacro {
    () => { println!("sin parámetros"); };
    ($x: expr) => { println!("un parámetro: {}", $x); };
    ($x: expr, $y: expr) => { println!("dos parámetros: {}, {}", $x, $y); };
}

mimacro!(); // sin parámetros
mimacro!(1); // un parámetro: 1
mimacro!(1, "hola"); // dos parámetros: 1, hola
```

En este simple ejemplo se puede ver que entre las llaves escribimos código
Rust directamente, la llamada a la macro se transformará en el código
contenido entre las llaves, dependiendo del matching de los parámetros. Lo
único extraño en este ejemplo es el uso de **$x** y **$y**, que son los
parámetros de la macro y que se pueden usar de esta manera en la definición
de la expansión.

Volvamos al ejemplo inicial ahora:

```rust
macro_rules! imprimir {
    ($($x: expr),*) => {
        {
            $(
                print!("{}, ", $x);
            )*
            println!("");
        }
    };
}

imprimir!("hola", "mundo!"); // -> hola, mundo!,
```

Aquí la expansión es más compleja, en este caso, la llamada se expandirá a
lo siguiente:

```rust
{
    print!("hola, ");
    print!("mundo!, ");
    println!("");
}
```

Las llaves y el **println** son directos, ahí no hay nada extraño, pero las
otras dos líneas se expanden a partir de la repetición de parámetros
definida con **$(...)\***.

Se utiliza una sintáxis similar en la expansión, para iterar sobre todos
los parámetros de entrada:

```rust
$(
    print!("{}, ", $x);
)*
```

Esto hace que se repita lo que ha entre los paréntesis tantas veces como
parámetros haya, además **$x** tendrá el valor del parámetro
correspondiente a cada iteración.

# Ámbito de las macros, importación y exportación

Las macros se expanden al principio de la compilación, por lo tanto no se
ha aplicado la resolución de nombres, las importaciones y demás, así que la
importación de módulos funciona un poco diferente para las macros.

Una macro es visible justo después de su definición en el mismo módulo
donde se define y en todos los módulos hijos de este.

También se puede ampliar esta visiblidad usando el atributo **macro_use**,
con el que podemos hacer visible una macro para el módulo padre.

```rust
#[macro_use]
mod mimodulo;
```

En el [libro][5] se puede ver un ejemplo de código con la visibilidad de
las macros.

```rust
macro_rules! m1 { () => (()) }

// Visible here: `m1`.

mod foo {
    // Visible here: `m1`.

    #[macro_export]
    macro_rules! m2 { () => (()) }

    // Visible here: `m1`, `m2`.
}

// Visible here: `m1`.

macro_rules! m3 { () => (()) }

// Visible here: `m1`, `m3`.

#[macro_use]
mod bar {
    // Visible here: `m1`, `m3`.

    macro_rules! m4 { () => (()) }

    // Visible here: `m1`, `m3`, `m4`.
}

// Visible here: `m1`, `m3`, `m4`.
```
Cuando esta biblioteca se carga con

```rust
#[macro_use]
extern crate testlib;
```
Sólo se importará la macro **m2**.

# Depuración de macros

Las macros se traducen a código Rust, por lo tanto, podemos encontrarnos
con problemas de código no esperados, si tenemos un error en una macro.
Para encontrar estos problemas, se puede usar la opción del compilador
**rustc --pretty expanded** para ver cómo queda el código con las macros
expandidas.

# Ejemplo de macro

En python existen los decoradores, que no son más que funciones que reciben
como parámetro una función y devuelven otra función como salida. Esto se
puede usar para modificar el comportamiento de las funciones, añadiendo
código que se ejecute antes, como comprobaciones de los parámetros,
permisos, etc y es bastante útil para extender el comportamiento de
cualquier función de manera fácil.

Podemos usar las macros para definirnos un *decorador* en Rust, que añada
por ejemplo un mensaje de depuración para saber cuánto tiempo ha tardado
esa llamada.

```rust
use std::time::Instant;

macro_rules! timeit {
    ($f: ident, $($x: ident : $p: ty),*) => {
        |$($x: $p, )*| {
            println!("Llamando a la función...");

            let now = Instant::now();
            let r = $f($($x,)*);
            let elapsed = now.elapsed();

            println!("Finalizado");

            let msecs = (elapsed.as_secs() * 1_000) + (elapsed.subsec_nanos() / 1_000_000) as u64;
            println!("Duración: {} ms", msecs);

            r
        };
    };
}

fn fib(x: i32) -> i32 {
    match x {
        0 => 0,
        1 => 1,
        n => fib(n - 1) + fib(n - 2),
    }
}

let nf = timeit!(fib, x: i32);
let v = nf(40);
println!("{}", v);

// Salida:
// Llamando a la función...
// Finalizado
// Duración: 685 ms
// 102334155
```

En este ejemplo, se recibe un primer parámetro, que es de tipo
identificador, que será el nombre de la función a *decorar*, y luego un
número indefinido de pares, identificador, :, tipo, de tal forma que
definamos los parámetros que recibe esa función.

Luego la macro genera un closure, con esos mismos parámetros, y llama a la
función, parándole todos los parámetros recibidos, se calcula el tiempo que
pasa durante la llamada a la función y finalmente devuelve la respuesta de
esta.

Con este ejemplo se puede ver el uso de diferentes tipos de parámetros para
las macros, como los identificadores o los tipos, además de generar código
que se puede asignar a una variable, en este caso se genera un closure.

# Conclusiones

Las macros son muy potentes, pero no hay que olvidar que complican la
lectura del código y también la depuración del mismo, pudiendo esconder
errores, así que se deben usar con moderación y sólo cuando lo que queremos
hacer no se pueda generalizar con funciones normales, ya que en la mayoría
de los casos será mucho más fácil de depurar si hay algún comportamiento
extraño y además, será mucho más fácil de entender el código.

[1]: https://doc.rust-lang.org/book/macros.html
[2]: https://doc.rust-lang.org/reference.html#macros
[3]: https://doc.rust-lang.org/reference.html#macro-by-example
[4]: https://doc.rust-lang.org/book/macros.html#repetition
[5]: https://doc.rust-lang.org/book/macros.html#scoping-and-macro-importexport
