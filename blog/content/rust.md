Date: 2017-01-24
Title: Rust
Tags: wadobo, rust, programming
Category: blog
Slug: rust
Gravatar: 8da96af78e0089d6d970bf3760b0e724

## El lenguaje de programación

Llevaba ya algún tiempo escuchando hablar de [Rust][1], en diferentes
círculos. La primera vez que escuché hablar de él fue en un FOSDEM, hace ya
unos años, cuando estaban empezando con servo, pero ahí no le presté
demasiada atención. Luego he visto varios comentarios por diferentes redes
sociales gente a la que sigo y cuya opinión sobre tecnología valoro
bastante y entonces me empezó a llamar más la atención.

Pero realmente lo que me hizo interesarme de verdad por este lenguaje fue
el enlace que me apareció un día en mi firefox. Firefox pone de vez en
cuando mensajes y enlaces en la página de búsqueda por defecto y
hace unos días vi que hablaban de servo y pinché en el enlace.

Y a partir de ahí empecé a leer sobre rust. Me interesó y me leí el
[The Rust Programming Language][2] y me empezó a gustar. La sintaxis, la gestión
de memoria, la compatibilidad con C... Estuve jugando un poco con el
lenguaje, haciendo algunos ejemplos y programando. Y ya que estaba
interesado, también me leí el libro [Why Rust?][3].

## Jugando con Rust

Para aprender a programar con un nuevo lenguaje no basta tan sólo con
leerse la documentación, lo más importante es ponerlo en práctica. Y para
eso, pensé en resolver algunos problemas matemáticos sencillos, y empecé a
resolver problemas de [Project Euler][4] con [rust][5].

Con este proyecto empecé a trastear con la herramienta [Cargo][6], que es
una de las cosas geniales de Rust, estuve tratando con los módulos, la
documentación y los tests. Pero realmente estos problemas son simples
problemas matemáticos, que no requieren de estructuras complejas y de más
de una o dos funciones, por lo que a nivel de programación, no me encontré
con ningún problema, ni estaba viendo lo realmente diferente de Rust con
respecto a otros lenguajes como C o C++.

Así que decidí hacer algo un poco más grande, y ya que estaba, pues hacer
algo útil. Estuve valorando unos días, qué herramienta podría implementar,
y un día, explorando los crates publicados en [crates.io][7], vi que no
había gran cosa sobre lectura de EPUB, así que me decidí a implementar algo
sencillo, ya que había estado trasteando con este formato para integrarlo
en [gnome][8].

Un EPUB no es más que un zip con ficheros XML dentro, por lo que para un
parseo básico se necesitan pocas dependencias. La parte de zip fue fácil,
porque el crate zip provee la lectura básica de ficheros. Donde me encontré
con problemas reales fue a la hora de parsear los XML y sacar la
información del documento.

En un EPUB hay un documento XML donde se especifica toda la información del
libro, los metadatos, una lista de recursos y una lista con los
"capítulos", que no son más que referencias a recursos XML definidos
anteriormente. Mi objetivo era parsear este XML y poder acceder a
diferentes elementos y atributos de forma más o menos fácil. El crate de
XML que usé me daba una forma de parsear un XML, pero de manera secuencial,
no me devolvía ningún tipo de dato con la estructura del árbol XML, así que
me lo implementé.

La implementación es algo sencillo, un nodo, que tiene una lista de nodos
hijos, y que puede tener un padre, para poder recorrerlo arriba y abajo.

Y al implementar esta [estructura en Rust][11] me encontré con el borrow
checker y la gestión de memoria de Rust. Voy recorriendo el XML y creando
los nodos conforme me los voy encontrando, luego hay que añadir el nodo
hijo al padre y referenciar el padre en el hijo. Y eso me costó bastante.
Hasta que finalmente comprendí como va el tema de las referencias en Rust y
la "propiedad" de la memoria y variables. Esto está muy bien explicado en
el libro [Why Rust?][3].

Subí el repo [epub-rs][9] a github y creé el [crate][10] correspondiente,
con la [documentación generada automáticamente][12], que además son tests
unitarios.

## Lo malo de Rust

La sintaxis en algunos casos es demasiado ofuscada, lo que hace a primera
vista sea "feo", el uso de "!" para macros, el "&", "*", "->", "=>", "::",
":", "<<>>", "| |", muchos símbolos de puntuación en el código.

Las conversiones y transformaciones implícitas, hacen que muchas veces no
tengas que poner el "*" pero realmente se esté haciendo la dereferencia y
cosas similares. Viniendo de python, tengo bastante claro que siempre es
mejor explícito que implícito, porque siendo implícito tienes que conocer
al detalle el lenguaje para poder leerlo sin ambigüedad, y siendo
explícito, todo es mucho más coherente, sin tener que conocer detalles
internos.

## Lo bueno de Rust

 * Cargo: Un gestor de paquetes, compilador, generador de documentación,
   etc. Engloba todo lo básico para gestionar cualquier proyecto rust de
   forma fácil.

 * Tests en la documentación: Esto es genial, en python están los
   [doctest][13], pero en Rust esto es lo recomendado para documentar y la
   verdad es que unificar documentación y tests unitarios es lo mejor para
   que la documentación siempre sea coherente con la implementación.

 * Compatibilidad con C gratis: Es trivial que una biblioteca Rust se pueda
   usar desde C y viceversa, por lo que en Rust tienes todo lo de C.

## Conclusiones

Rust es un lenguaje genial. Me he sentido muy cómodo programando en Rust,
en casi todo momento, excepto en las ocasiones en las que me he tenido que
pelear con el borrow checker, pero en teoría eso es lo que le da la
seguridad al lenguaje, así que mejor corregir los problemas en tiempo de
compilación que en lugar de encontrarte con segmentation faul o memory
leaks meses después.

La comunidad que hay alrededor de Rust es bastante impresionante, teniendo
en cuenta es un lenguaje moderno, nacido en 2010, y parece su uso se está
extendiendo rápidamente.

Por lo tanto, y a riesgo de equivocarme estrepitosamente, apostaría a que
Rust será en el corto/medio plazo uno de los lenguajes de programación más
importantes y habrá muchas cosa grandes y pequeñas hechas con Rust,
empezando por firefox.

Principalmente programo en Python y de momento este lenguaje será mi
primera opción a la hora de resolver cualquier problema. Pero Rust no está
tan lejos de Python, por lo que será mi opción siempre que me encuentre con
el problema del rendimiento. En cualquier caso, no descarto reemplazar
Python por Rust como mi lenguaje para "todo" en un futuro, lo que sí tengo
claro es que a día de hoy elegiría Rust por delante de C, C++, java, go y scala.


[1]: http://rust-lang.org
[2]: https://doc.rust-lang.org/book/
[3]: http://www.oreilly.com/programming/free/why-rust.csp
[4]: https://projecteuler.net/
[5]: https://github.com/danigm/rust-euler
[6]: http://doc.crates.io/

[7]: https://crates.io
[8]: https://git.gnome.org/browse/libgepub/

[9]: https://github.com/danigm/epub-rs.git
[10]: https://crates.io/crates/epub

[11]: https://github.com/danigm/epub-rs/blob/master/src/xmlutils.rs#L101
[12]: https://danigm.github.io/epub-rs-doc/epub/index.html

[13]: https://docs.python.org/3.5/library/doctest.html
