Date: 2017-03-18
Title: Rust: Documentación
Tags: wadobo, rust, programming
Category: blog
Slug: rust-doc
Gravatar: 8da96af78e0089d6d970bf3760b0e724

He hablado en este blog sobre casi todas las partes importantes de Rust, he
puesto muchos ejemplos de código y con esta información, cualquiera podría
empezar a escribir código que funcione. Pero a la hora de hacer algo de
verdad, de escribir una biblioteca o un programa que pueda ser usado por
otra persona o mantenido en un futuro es imprescindible la documentación y
por supuesto los tests unitarios.

Podemos escribir código sin documentación y sin tests, pero mantener ese
código es mucho más difícil y que otra persona lo use también, ya que si no
está debidamente documentado tendrá que irse al código y entender qué es lo
que hace cada función.

Rust ofrece por defecto una forma de documentar y de implementar tests
bastante simple, además, la norma de un buen código Rust requiere que todo
método público esté documentado, por lo que si seguimos esta norma,
tendremos un código más mantenible. El tener la documentación y los tests
tan bien definidos desde el inicio ha provocado que la mayoría de las
bibliotecas existentes a día de hoy estén bien documentadas y tengan una
serie de tests definidos, y todo ello va junto con el código fuente
siempre.

La documentación en Rust se genera a partir de comentarios en el código,
comparado con python, sería algo similar a los docstrings. Se escribe en
formato Markdown y con herramientas como cargo se pueden generar la
documentación en html fácilmente.

## [Documentando][1]

Los comentarios de documentación en Rust no son iguales que los comentarios
normales de código. Los comentarios normales son similares a los
comentarios en C, pero se definen otros comentarios definidos con **///** y
con **//!**, que sí son documentación.

La diferencia entre **//!** y **///** es que el primero se documenta el
elemento que lo engloba, mientras que el segundo documenta el elemento que
viene justo después. Normalmente se usa el primero para documentar módulos,
ya que se suele escribir ese comentario al principio del fichero, y las
estructuras y métodos se documentan con **///** poniendo la documentación
justo antes de la implementación.

### Generando la documentación con cargo

Con **cargo** se puede generar la documentación muy fácilmente, simplemente
hay que lanzar el comando **cargo doc** y esto generará toda la
documentación en HTML en el directorio **target/doc**

```bash
$ cargo doc
$ ls target/doc
```

### Documentación de módulos

Si tenemos un módulo definido en un fichero, se puede documentar tal que
así:

```rust
/// Módulo de ejemplo para explicar cómo funciona la documentación
/// en Rust.
pub mod ejemplo {
    ...
}
```

Sin embargo, normalmente los módulos se definen en ficheros independientes
y la documentación se suele poner al principio de cada módulo:

```rust
//! Módulo de ejemplo para explicar cómo funciona la documentación
//! en Rust.

fn funcion() {
    ...
}
...
```

### Secciones en la documentación

En la documentación se pueden definir diferentes secciones, para separar la
documentación y que se muestre de manera diferente. Estas secciones se
definen como encabezados Markdown (**# Examples**), y lo que viene debajo
pertenece a esa sección.

Estas son las secciones especiales que se definen en Rust:

 * **Panics**, si pueden ocurrir errores que no son recuperables, osea, que
   terminan la ejecución.

 * **Errors**, cuando se devuelve un *Result*, es conveniente documentar
   qué tipos de errores se pueden devolver y cuando.

 * **Safety**, esto es más raro de encontrar, pero si una función es
   *unsafe* es conveniente explicar el porqué.

 * **Examples**, esto es lo más común y recomendable en todo método. Aquí
   se pueden definir ejemplos de código, que además funcionarán como tests
   unitarios.

No es obligatorio, pero sí recomendable el rellenar cada una de estas
secciones, siempre y cuando tenga sentido, en la documentación de tus
métodos, ya que facilitará la tarea a futuros usuarios.

## Tests en la documentación

Como hemos visto, la sección **Examples** sirve para definir ejemplos de
código que se verán en la documentación, bien formateados, pero que además
sirven como tests unitarios.

```rust
/// Comprueba si un número es mayor que 3
///
/// Se devuelve verdadero si *x* es mayor que 3,
/// en otro caso se deuvelve falso.
///
/// # Examples
///
/// Ejemplo básico
///
/// ```
/// use geometry::mayor3;
/// assert_eq!(mayor3(2), false);
/// assert_eq!(mayor3(3), false);
/// assert_eq!(mayor3(4), true);
/// ```
///
/// Más ejemplos
///
/// ```
/// use geometry::mayor3;
/// let mut n = 1;
/// assert_eq!(mayor3(n), false);
/// while !mayor3(n) {
///     n += 1;
/// }
/// assert_eq!(n, 4);
/// ```
pub fn mayor3(x: i32) -> bool {
    x > 3
}
```

En este ejemplo se puede ver cómo se documenta una función, con un par de
ejemplos.

Podemos ver cómo quedaría esta documentación en el HTML generado:

<p class="img">
    <img src="/pictures/rust-doc-1.png" />
</p>

### Ejecutando los tests con cargo

Como he comentado anteriormente, los ejemplos de código definidos en la
documentación también hacen la función de tests unitarios. Para ejecutar
los tests tan sólo hay que usar la herramienta **cargo test**:

```bash
$ cargo test
    Finished debug [unoptimized + debuginfo] target(s) in 0.0 secs
     Running target/debug/deps/geometry-d942cf2b29083ab0

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured

   Doc-tests geometry

running 2 tests
test mayor3_0 ... ok
test mayor3_1 ... ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured
```

Si eres buen observador, habrás visto que en los tests se mete la
importación del módulo en concreto, **use geometry::mayor3**, esto es así
porque para ejecutar los tests de la documentación, lo que hace cargo es
crear un nuevo fichero rust con ese código, y lo mete todo dentro de un
**fn main**, si no está definido. Por lo tanto, todo el código que se
escriba en un test ha de estar como si estuviera en un fichero
independiente.

En ocasiones no queremos mostrar en la documentación todas las
importaciones, o definiciones, sólo la parte importante, pero si hacemos
eso, los tests no funcionarán. Para esos casos, se puede comenzar cada
línea de código a ocultar en la documentación con *#*, de tal forma que se
ejecutará en los tests, pero no aparecerá en la documentación, por ejemplo:

```rust
/// ```
/// # use geometry::mayor3;
/// let mut n = 1;
/// assert_eq!(mayor3(n), false);
/// # while !mayor3(n) {
/// #     n += 1;
/// # }
/// # assert_eq!(n, 4);
/// ```
pub fn mayor3(x: i32) -> bool {
...
```

Con esta documentación, el test seguiría siendo el mismo, pero sólo se
muestra en la documentación generada lo que no está "*comentado*", quedando
tal que así:

<p class="img">
    <img src="/pictures/rust-doc-2.png" />
</p>

## Extra: Esconder la documentación en vim

Con la documentación y los tests incluidos, los ficheros de código se
vuelven muy grandes rápidamente y navegar por ellos se vuelve un poco
complejo.

Creo que viene muy bien que la documentación y el código estén en el mismo
fichero, y juntos, ya que si se cambia el código no nos olvidaremos de
cambiar la documentación y por tanto es mucho más fácil mantener esta
documentación consistente. Además para cualquiera que lea el código, y no
sea un desarrollador avanzado, le vendrá muy bien esa documentación.

Sin embargo, cuando ya conoces un código y estás modificando un fichero
cualquiera, tener que navegar por todo el fichero con tantos comentarios,
es un poco engorroso, normalmente quieres ocultar esos comentarios para
centrarte en el código.

Para ello tengo definido en el vim una función para que agrupe los
comentarios con **fold**:

```vim
setlocal foldmethod=expr
setlocal foldexpr=GetRustFold(v:lnum)

function! IndentLevel(lnum)
    return indent(a:lnum) / &shiftwidth
endfunction

function! GetRustFold(lnum)
    if getline(a:lnum) =~? '\v^\s*$'
        return '-1'
    endif

    let this_indent = IndentLevel(a:lnum)

    if getline(a:lnum) =~? '^\s*///.*$'
        if this_indent == '0'
            return '1'
        endif
        return this_indent
    endif

    if getline(a:lnum) =~? '^\s*//!.*$'
        if this_indent == '0'
            return '1'
        endif
        return this_indent
    endif

    return '0'
endfunction
```

Por ejemplo, si abro el fichero de **string.rs**:

<p class="img">
    <img src="/pictures/rust-doc-3.png" />
</p>

Y puedo desplegar o contraer los comentarios a mi gusto con **za**.

## Conclusiones

Hay muchas cosas sobre documentación en Rust que no he comentado por aquí y
que se pueden encontrar en la documentación oficial. Lo que he contado es
lo básico y la forma más sencilla de empezar a documentar y a probar el
código.

Como ejemplo de documentación más completa, se puede mirar cualquier
*crate* de Rust, en [github][3] hay mucho código Rust, que está documentado
de esta manera. Por ejemplo la [biblioteca para leer epubs][2] que yo mismo
he implementado define la documentación y los tests de esta forma.

Y como resultado de la documentación, pues se puede mirar la
[documentación de std de *Rust*][4], por ejemplo, se puede mirar el
[código de String][6] y comparar con la [documentación html][5].

[1]: https://doc.rust-lang.org/book/documentation.html
[2]: https://github.com/danigm/epub-rs/blob/master/src/doc.rs
[3]: https://github.com
[4]: https://doc.rust-lang.org/std/
[5]: https://doc.rust-lang.org/std/string/struct.String.html
[6]: https://github.com/rust-lang/rust/blob/master/src/libcollections/string.rs
