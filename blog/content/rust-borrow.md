Date: 2017-02-4
Title: Rust: Introducción a la gestión de memoria
Tags: wadobo, rust, programming
Category: blog
Slug: rust-borrow
Gravatar: 8da96af78e0089d6d970bf3760b0e724

## Gestión de memoria sin recolector de basura

Una de las características principales de Rust es la seguridad de la
memoria, que se comprueba en tiempo de compilación, sin recolector de
basura.

En teoría, con **Rust** no es *posible* que ocurra un *segmentation fault*,
porque no hay manera de que se acceda a una posición de memoria inválida y
además, tampoco es *posible* que haya *memory leaks*, y esto se verifica en
tiempo de compilación, por lo que no es necesario un recolector de basura y
por lo tanto, el rendimiento es similar al de lenguajes como **C**.

Esto se consigue en Rust con el concepto de **propiedad** de la definición
de las variables.

## Concepto de propiedad de la memoria ([ownership][1])

En **Rust** cada declaración de variable asigna la propiedad de el valor a
esa variable, así cuando la variable sale del ámbito, la memoria se libera.

Para garantizar la seguridad de la memoria sólo puede existir un
propietario de una zona de memoria, porque si no, el compilador no sabe
cuándo debe liberar esa memoria y podría existir en el tiempo una variable
apuntando a una zona de memoria inválida.

```rust
fn foo() {
    let v = vec!(1, 2, 3);
}
```

Por ejemplo, esta asignación crea un vector en memoria con tres elementos,
y asigna la propiedad de ese vector a la variable *v*. Como está dentro de
la función *foo*, esa variable existirá hasta el final de esa función, y
cuando se sale de la función, se elimina de la memoria el vector.

### Mover, copiar y clonar (Copy, Clone)

#### Mover

Como he comentado antes, Rust se asegura de que una zona de memoria sólo es
propiedad de una única variable, para poder asegurar en tiempo de
compilación que no se accede a memoria liberada.

```rust
let v = vec!(1, 2, 3);
let v2 = v;
```

¿Qué ocurre entonces en este caso? Tenemos el vector cuyo propietario es *v*,
pero declaramos otra variable, *v2* a la que le asignamos el valor de *v*,
por lo tanto, tendríamos dos variables apuntando a la misma zona de
memoria. Pero este caso lo resuelve *Rust* con el **movimiento** del valor,
osea, la propiedad pasa de *v* a *v2* en esta asignación, asegurando así
que sólo hay un propietario de ese valor, y por tanto, el vector se
eliminará cuando *v2* salga del ámbito.

Pero claro, esto podría crear inconsistencias, porque si *v2* se elimina
antes que *v*, hay un instante de tiempo en el que tenemos a alguien
apuntando a una zona no válida de memoria. Y esto lo resuelve el compilador
no dejándote acceder a *v*:

```rust
let v = vec!(1, 2, 3);
let v2 = v;
println!("v[0] is: {}", v[0]);
// error: use of moved value: `v`
// println!("v[0] is: {}", v[0]);
//                         ^
```
[ejecutar][20]

No podemos acceder al vector usando *v*, después de haber movido el valor,
porque ya no es el propietario. En este caso sólo podríamos acceder con *v2*.

Esto también ocurre cuando se pasa la variable a una función:

```rust
fn take(v: Vec<i32>) {
    // lo que ocurre aquí dentro no es relevante
}
fn main() {
    let v = vec!(1, 2, 3);
    take(v);
    println!("v[0] is: {}", v[0]);
}
```
[ejecutar][21]

Esto nos dará el mismo error, en este caso, la propiedad pasa de la
variable *v* declarada en el ámbito de *main* al atributo *v* declarado en
la función *take*. Por lo tanto, el vector se eliminará después de la
llamada a *take*, se ha movido el valor, así que si el compilador nos
dejara acceder a *v[0]*, tendríamos acceso a memoria ya liberada, de ahí la
importancia de la propiedad en *Rust*, nos asegura que la memoria se libera
y que no hay ninguna variable apuntando a donde no debe en ningún momento.

#### Copiar

Sin embargo, esto no ocurre con los tipos básicos, ya que en lugar de
*moverse*, estos se *copian*. Existe un *[trait][4]* llamado *Copy*, que
implementan los tipos básicos y que hace que en lugar de mover los valores
en una asignación se haga una copia completa. Por lo tanto todo tipo que
implemente *Copy* se copiará y por tanto nos permite asignar a diferentes
variables, porque realmente son zonas de memoria distintas e
independientes.

```rust
fn double(x: i32) -> i32 {
    x * 2
}

fn main() {
    let v = 2;
    let v2 = double(v);
    println!("v: {}, v2: {}", v, v2);
    // v: 2, v2: 4
}
```
[ejecutar][22]

En este caso, podemos acceder al valor de *v* en el *println* porque el
tipo *i32* implementa *Copy*, por lo tanto en la llamada a *double* se
copia el valor, no se mueve, *x* existe sólo durante el ámbito de *double*
y tiene el valor *2* copiado de *v*, ambas son accesibles en sus diferentes
ámbitos en independientes.

#### Clonar

Existe otra forma de copiar variables en Rust, en lugar de *copiar* lo que
hacemos es *clonar*. Es básicamente lo mismo salvo que el copiado es
implícito y el clonado es explícito. Además, en Rust no está permitido
reimplementar el copiado, siempre será una copia literal de memoria, sin
embargo, el clonado sí que se puede reimplementar y hacer un copiado más
ligero o ejecutar cualquier código para gestionar el tipo.

```rust
fn take(v: Vec<i32>) {
    // lo que pase aquí es irrelevante
}

fn main() {
    let v = vec!(1, 2, 3);
    take(v.clone());
    println!("v[0]: {}", v[0]);
    // v[0]: 1
}
```
[ejecutar][23]

Volviendo al ejemplo anterior, donde la llamada a una función movía el
vector y por tanto lo hacía inaccesible, podemos solucionarlo usando clone,
ya que el tipo *Vec* implementa *[Copy][5]*, así en la función *take*
tenemos una copia del vector, son dos vectores diferentes.

## Tomar prestado y referencias ([borrow][2])

Con el copiado y el clonado, podemos hacer uso de las diferentes variables
en llamadas a métodos y demás, pero esto no es nada eficiente si tenemos
estructuras de datos grandes, ya que estamos copiando constantemente y no
nos permite modificar una variable dentro de una función, todo cambio
debería hacerse en valor de devolución, si queremos añadir un elemento a un
vector, tendríamos que copiar el vector, añadir el elemento y devolver el
nuevo vector, en lugar de añadirlo directamente.

```rust
fn addone(mut w: Vec<i32>, element: i32) -> Vec<i32> {
    w.push(element);
    w
}

fn main() {
    let v = vec!(1, 2, 3);
    let v2 = addone(v.clone(), 4);
    println!("{:?}", v);
    println!("{:?}", v2);
}
```
[ejecutar][24]

Para evitar copiar el vector, en *Rust* existen las referencias "**&**".
Cuando se crea una referencia a un valor, en lugar de mover o copiar ese
valor, tenemos realmente dos variables apuntando a la misma zona de
memoria. Sin embargo, hemos dicho que esto no es posible si queremos
mantener la seguridad de la memoria... Y para solucionar esto, el concepto
que añade *Rust* es el de **borrowing** o tomar prestado.

Una zona de memoria sólo tiene un propietario, pero puede que alguna otra
variable quiera acceder a esa zona de memoria, por lo tanto la pide
prestada, "**borrow**", y ya es como si en ese momento fuera el
propietario.

```rust
let v = vec!(1, 2, 3);
let v2 = &v;
println!("v[0]: {}, v2[0]: {}", v[0], v2[0]);
```

En este caso, tenemos que la variable *v2* es una referencia a *v* y por
tanto lo que hace es pedir prestado el vector, haciendo accesible tanto a
*v* como *v2*.

Estas referencias son inmutables, lo que no nos permite modificar la zona
de memoria, por lo tanto, podemos *Rust* nos permite tener tantas
referencias inmutables como queramos a una zona de memoria, siempre y
cuando estas referencias no estén en un ámbito superior al propietario, es
decir, que no pueden existir las referencias más allá que el propietario,
ya que cuando el propietario salga del ámbito, la memoria se liberará.

Para poder modificar los valores por referencia hay que hacer uso de las
referencias mutables "**&mut**". A diferencia de las referencias
inmutables, sólo está permitido que exista una referencia mutable para un
valor determinado. Esto es así para evitar que una zona de memoria sea
modificada por dos variables a la vez.

No sólo no es posible tener más de una referencia mutable a un valor, sino
que una vez que se hace una referencia mutable, no es posible hacer ninguna
referencia inmutable, es decir, que mientras que exista una referencia
mutable no puede existir ninguna otra referencia.

```rust
let mut x = 5;
{
    let y = &mut x;
    *y += 1;
}
println!("{}", x);
```
[ejecutar][25]

En este ejemplo se puede ver el uso de una referencia mutable. Para que el
compilador no se queje en la llamada a *prinlnt*, hay que añadir las
llaves, que crean un ámbito nuevo. La variable *y* sólo existe en ese
ámbito, por lo tanto, al salir nos permite llamar a *println* con *x*.

El "\*" se usa en este ejemplo para hacer una derreferencia explícita y
poder modificar realmente el valor que estamos referenciando y no la
referencia en sí, ya que y no es realmente del tipo *i32*, sino que es del
tipo *&mut i32*.

Con las referencias mutables podemos simplificar el ejemplo anterior de
añadir un elemento a un vector:

```rust
fn addone(w: &mut Vec<i32>, element: i32) {
    w.push(element);
}

fn main() {
    let mut v = vec!(1, 2, 3);
    addone(&mut v, 4);
    println!("{:?}", v);
}
```
[ejecutar][26]

En este caso no es necesario añadir las llaves para crear un ámbito nuevo
para la referencia mutable, ya que ésta sólo existe en el ámbito de la
función *addone*, por lo tanto, después de la llamada no existe ninguna
referencia a *v* y por tanto esta es accesible de nuevo.

## Tiempo de vida ([lifetimes][3])

No voy a entrar en detalle con respecto a los tiempos de vida de las
variables, en este artículo introductorio, pero sí voy a comentar lo básico
para saber qué significa y cómo se usa.

Cuando se hace una referencia, tenemos dos variables apuntando a una misma
zona de memoria, y como he comentado anteriormente, una referencia no puede
existir más allá que el propietario de la memoria.

Normalmente el compilador es capaz de determinar la vida de las variables y
las referencias para asegurarse de que esta regla se cumple, pero hay
ocasiones en las que el compilador no es capaz de determinar si una
referencia dura más o menos, por lo que hay que especificarlo.

Esto se da normalmente en definiciones de funciones que reciben varias
referencias y devuelven otra referencia. El compilador no sabe a cuál
parámetro de entrada está ligada esta referencia, por lo que hay que
especificarlo con una nueva sintaxis:

```rust
fn skip_prefix<'a, 'b>(line: &'a str, prefix: &'b str) -> &'a str {
    // ...
  line
}

let line = "lang:en=Hello World!";
let lang = "en";

let v;
{
    let p = format!("lang:{}=", lang);  // -+ `p` comes into scope.
    v = skip_prefix(line, p.as_str());  //  |
}                                       // -+ `p` goes out of scope.
println!("{}", v);
```
[ejecutar][27]

En este ejemplo se definen dos tiempos de vida, en la declaración de
*skip_prefix*, *a* y *b*. La primera referencia tiene el ámbito *a* y la
segunda el ámbito *b*, y se devuelve una referencia que tiene el ámbito
*a*. Si no definimos los tiempos de vida, el compilador se quejará, porque
no sabría a qué refiere el valor de retorno.

El tiempo de vida también puede ser necesario definirlo en estructuras que
tengan referencias. Normalmente no te tienes que preocupar de esto hasta
que el compilador no se queje, si no es capaz de inferir los tiempos de
vida te lo dirá y tendrás que especificarlo en el código.

## Uso básico de referencias, Rc/RefCell y Arc/Mutex

Debido a las restricciones del uso de memoria de *Rust* la gestión de
referencias, los tiempos de vida y demás nos pueden complicar un poco la
vida. Sin embargo existen unos tipos que nos permiten hacer uso de
*referencias* de una forma mucho más simple y manteniendo la seguridad de
memoria que nos ofrece *Rust* en tiempo de compilación, estoy hablando de
*Rc* y *RefCell*.

## [Cell y RefCell][6], tipos mutables a través de referencias

Como hemos visto antes, sólo puede haber una referencia mutable a un valor,
los tipos *Cell* y *RefCell* nos permiten modificar valores con una
referencia no mutable, por lo que podemos tener varias referencias a un
*Cell* y en cualquier momento editar el contenido.

*Cell* sólo es compatible con los tipos que soporta *Copy*, en otro caso
hay que utilizar *RefCell*. Con *Cell* podemos modificar o acceder al
contenido llamando a los métodos *set* y *get*, con *RefCell* tenemos que
hacer un *borrow_mut()* para obtener una referencia mutable.

```rust
use std::cell::Cell;
use std::cell::RefCell;

fn main() {
    let v = 1;
    let v2 = Cell::new(v);
    v2.set(3);
    println!("v: {}, v2: {}", v, v2.get());

    // RefCell
    let v3 = RefCell::new(5);
    {
        let mut v4 = v3.borrow_mut();
        *v4 = 7;
        println!("v4: {}", *v4);
    }
    let v5 = v3.borrow();
    println!("v3: {}, v5: {}", *v3.borrow(), *v5);
}
```
[ejecutar][28]

Lo realmente interesante de este ejemplo es el uso de *RefCell*, ya que con
*Cell* tenemos una copia, lo único extra que tenemos es que nos evitamos el
*mut* en la declaración de *v2*.

En un *RefCell* podemos hacer tantos *borrow* como queramos, pero sólo
puede existir un *borrow_mut* en el ámbito, ya que estamos en las mismas,
la función *borrow* fallará si existe un *borrow_mut*, de ahí las llaves de
este ejemplo, para añadir un nuevo ámbito para *v4*.

Estos tipos no nos ofrecen nada extraordinario, porque este mismo código lo
podemos tener con referencias básicas con algo así:

```rust
let mut v3 = 5;
{
    let mut v4 = &mut v3;
    *v4 = 7;
    println!("v4: {}", *v4);
}
let v5 = &v3;
println!("v3: {}, v5: {}", v3, *v5);
```

Estos tipos son útiles en combinación con los tipos *Rc*.

## [Rc][7], punteros con contador de referencias

El tipo *Rc<T\>* nos ofrece una propiedad compartida del valor de tipo *T*.
Podemos llamar la función *clone* para crear una nueva referencia al mismo
valor en memoria. El propio tipo se encarga de decrementar el número de
referencias cuando salen del ámbito y de liberar la memoria cuando ya no
hay ninguna referencia.

*Rc* no permite editar los valores, ya que las referencias no son mutables.
Para poder editar los valores compartidos con un *Rc*, se puede usar en
combinación con *RefCell*.

```rust
use std::rc::Rc;
use std::cell::RefCell;

fn main() {
    let v = Rc::new(RefCell::new(vec!(1, 2, 3)));
    let v1 = v.clone();
    v1.borrow_mut().push(4);
    println!("v: {:?}", v.borrow());
}
```
[ejecutar][29]

En este ejemplo se puede ver cómo tenemos una referencia compartida al
vector, que además es editable a través de *borrow_mut*. En la declaración
de *v1* se llama a *clone*, pero realmente no se copia la memoria del
vector, la edición en la línea siguiente modifica el vector original.

Como he comentado antes, no es posible tener más de un *borrow_mut* en el
mismo ámbito, en este caso, como el *borrow_mut* no se asigna a ninguna
variable, sólo existe en esa línea, por lo que el *borrow* que hay en el
*print* funcionará.

Con el uso de *Rc* se pueden crear ciclos, con tipos que se referencian a
sí mismos y para evitar estos ciclos existe otro tipo que es *Weak*, que es
una referencia, pero que no cuenta a la hora de eliminar el valor de
memoria, por lo tanto pueden existir referencias tipo *Weak* que apunten a
memoria ya liberada, y por esto el tipo *Weak* no se derreferencia
automáticamente, hay que llamar al método *upgrade* que devuelve un
*Option<Rc\>*, y si la memoria ya se ha liberado será *None*.

## [Arc y Mutex][8], Rc y RefCell pero thread-safe

La combinación *Rc<RefCell<T\>\>* nos permite tener varias referencias a la
misma zona de memoria, y modificarla, pero no es posible pasar estos tipos
entre hilos. *Rust* ofrece un par de tipos similares, pero que sí son
*thread-safe*, lo que quiere decir que nos asegura que no hay *data race*,
es decir, que la memoria siempre es consistente, aunque usemos diferentes
hilos para leer y modificar estas variables.

Para esto podemos usar la combinación *Arc<Mutex<T\>\>* que se usa de forma
similar a *Rc<RefCell\>*, pero que nos asegura que es seguro usar entre
diferentes hilos:

```rust
use std::sync::{Arc, Mutex};

fn main() {
    let v = Arc::new(Mutex::new(vec!(1,2,3)));
    let v1 = v.clone();
    v1.lock().unwrap().push(4);
    println!("v[3]: {}", v.lock().unwrap()[3]); // -> 4
}
```
[ejecutar][30]

En este ejemplo no hay ningún hilo, pero vale como ejemplo, similar al
ejemplo anterior. Aquí hay que hacer el *unwrap* después del *lock*, porque
esta llamada puede fallar, en este ejemplo no se controlan los errores,
pero en código de producción no se debería hacer el *unwrap* directamente,
sino que se debería controlar el *Result* que devuelve, si es del tipo *Ok*
o *Err*.

[1]: https://doc.rust-lang.org/book/ownership.html
[2]: https://doc.rust-lang.org/book/references-and-borrowing.html
[3]: https://doc.rust-lang.org/book/lifetimes.html
[4]: https://doc.rust-lang.org/book/traits.html
[5]: https://doc.rust-lang.org/std/clone/trait.Clone.html
[6]: https://doc.rust-lang.org/std/cell/index.html
[7]: https://doc.rust-lang.org/std/rc/
[8]: https://doc.rust-lang.org/std/sync/struct.Arc.html

[20]: https://play.rust-lang.org/?code=%23%5Ballow(unused_variables)%5D%0A%23%5Ballow(dead_code)%5D%0Afn%20main()%20%7B%0A%20%20%20%20let%20v%20%3D%20vec!(1%2C%202%2C%203)%3B%0A%20%20%20%20let%20v2%20%3D%20v%3B%0A%20%20%20%20println!(%22v%5B0%5D%20is%3A%20%7B%7D%22%2C%20v%5B0%5D)%3B%0A%7D%0A&version=stable&backtrace=0
[21]: https://play.rust-lang.org/?code=%23%5Ballow(unused_variables)%5D%0A%23%5Ballow(dead_code)%5D%0A%0Afn%20take(v%3A%20Vec%3Ci32%3E)%20%7B%0A%20%20%20%20%2F%2F%20Lo%20que%20pase%20aqu%C3%AD%20no%20es%20relevante%0A%7D%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20v%20%3D%20vec!(1%2C%202%2C%203)%3B%0A%20%20%20%20take(v)%3B%0A%20%20%20%20println!(%22v%5B0%5D%20is%3A%20%7B%7D%22%2C%20v%5B0%5D)%3B%0A%7D%0A&version=stable&backtrace=0
[22]: https://play.rust-lang.org/?code=%23%5Ballow(unused_variables)%5D%0A%23%5Ballow(dead_code)%5D%0A%0Afn%20double(x%3A%20i32)%20-%3E%20i32%20%7B%0A%20%20%20%20x%20*%202%0A%7D%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20v%20%3D%202%3B%0A%20%20%20%20let%20v2%20%3D%20double(v)%3B%0A%20%20%20%20println!(%22v%3A%20%7B%7D%2C%20v2%3A%20%7B%7D%22%2C%20v%2C%20v2)%3B%0A%7D%0A&version=stable&backtrace=0
[23]: https://play.rust-lang.org/?code=%23%5Ballow(unused_variables)%5D%0A%23%5Ballow(dead_code)%5D%0A%0Afn%20take(v%3A%20Vec%3Ci32%3E)%20%7B%0A%20%20%20%20%2F%2F%20lo%20que%20pase%20aqu%C3%AD%20es%20irrelevante%0A%7D%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20v%20%3D%20vec!(1%2C%202%2C%203)%3B%0A%20%20%20%20take(v.clone())%3B%0A%20%20%20%20println!(%22v%5B0%5D%3A%20%7B%7D%22%2C%20v%5B0%5D)%3B%0A%7D%0A&version=stable&backtrace=0
[24]: https://play.rust-lang.org/?code=%23%5Ballow(unused_variables)%5D%0A%23%5Ballow(dead_code)%5D%0A%0Afn%20addone(mut%20w%3A%20Vec%3Ci32%3E%2C%20element%3A%20i32)%20-%3E%20Vec%3Ci32%3E%20%7B%0A%20%20%20%20w.push(element)%3B%0A%20%20%20%20w%0A%7D%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20v%20%3D%20vec!(1%2C%202%2C%203)%3B%0A%20%20%20%20let%20v2%20%3D%20addone(v.clone()%2C%204)%3B%0A%20%20%20%20println!(%22%7B%3A%3F%7D%22%2C%20v)%3B%0A%20%20%20%20println!(%22%7B%3A%3F%7D%22%2C%20v2)%3B%0A%7D%0A&version=stable&backtrace=0
[25]: https://play.rust-lang.org/?code=fn%20main()%20%7B%0Alet%20mut%20x%20%3D%205%3B%0A%7B%0A%20%20%20%20let%20y%20%3D%20%26mut%20x%3B%0A%20%20%20%20*y%20%2B%3D%201%3B%0A%7D%0Aprintln!(%22%7B%7D%22%2C%20x)%3B%0A%7D
[26]: https://play.rust-lang.org/?code=fn%20addone(w%3A%20%26mut%20Vec%3Ci32%3E%2C%20element%3A%20i32)%20%7B%0A%20%20%20%20w.push(element)%3B%0A%7D%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20mut%20v%20%3D%20vec!(1%2C%202%2C%203)%3B%0A%20%20%20%20addone(%26mut%20v%2C%204)%3B%0A%20%20%20%20println!(%22%7B%3A%3F%7D%22%2C%20v)%3B%0A%7D&version=stable&backtrace=0
[27]: https://play.rust-lang.org/?code=fn%20main()%20%7B%0Afn%20skip_prefix%3C%27a%2C%20%27b%3E(line%3A%20%26%27a%20str%2C%20prefix%3A%20%26%27b%20str)%20-%3E%20%26%27a%20str%20%7B%0A%20%20%20%20%2F%2F%20...%0A%20%20line%0A%7D%0A%0Alet%20line%20%3D%20%22lang%3Aen%3DHello%20World!%22%3B%0Alet%20lang%20%3D%20%22en%22%3B%0A%0Alet%20v%3B%0A%7B%0A%20%20%20%20let%20p%20%3D%20format!(%22lang%3A%7B%7D%3D%22%2C%20lang)%3B%20%20%2F%2F%20-%2B%20%60p%60%20comes%20into%20scope.%0A%20%20%20%20v%20%3D%20skip_prefix(line%2C%20p.as_str())%3B%20%20%2F%2F%20%20%7C%0A%7D%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%2F%2F%20-%2B%20%60p%60%20goes%20out%20of%20scope.%0Aprintln!(%22%7B%7D%22%2C%20v)%3B%0A%7D&version=stable&backtrace=0
[28]: https://play.rust-lang.org/?code=%23%5Ballow(unused_variables)%5D%0A%23%5Ballow(dead_code)%5D%0A%0Ause%20std%3A%3Acell%3A%3ACell%3B%0Ause%20std%3A%3Acell%3A%3ARefCell%3B%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20v%20%3D%201%3B%0A%20%20%20%20let%20v2%20%3D%20Cell%3A%3Anew(v)%3B%0A%20%20%20%20v2.set(3)%3B%0A%20%20%20%20println!(%22v%3A%20%7B%7D%2C%20v2%3A%20%7B%7D%22%2C%20v%2C%20v2.get())%3B%0A%20%20%20%20%0A%20%20%20%20%2F%2F%20RefCell%0A%20%20%20%20let%20v3%20%3D%20RefCell%3A%3Anew(5)%3B%0A%20%20%20%20%7B%0A%20%20%20%20%20%20%20%20let%20mut%20v4%20%3D%20v3.borrow_mut()%3B%0A%20%20%20%20%20%20%20%20*v4%20%3D%207%3B%0A%20%20%20%20%20%20%20%20println!(%22v4%3A%20%7B%7D%22%2C%20*v4)%3B%0A%20%20%20%20%7D%0A%20%20%20%20let%20v5%20%3D%20v3.borrow()%3B%0A%20%20%20%20println!(%22v3%3A%20%7B%7D%2C%20v5%3A%20%7B%7D%22%2C%20*v3.borrow()%2C%20*v5)%3B%0A%7D&version=stable&backtrace=0
[29]: https://play.rust-lang.org/?code=%23%5Ballow(unused_variables)%5D%0A%23%5Ballow(dead_code)%5D%0A%0Ause%20std%3A%3Arc%3A%3ARc%3B%0Ause%20std%3A%3Acell%3A%3ARefCell%3B%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20v%20%3D%20Rc%3A%3Anew(RefCell%3A%3Anew(vec!(1%2C%202%2C%203)))%3B%0A%20%20%20%20let%20v1%20%3D%20v.clone()%3B%0A%20%20%20%20v1.borrow_mut().push(4)%3B%0A%20%20%20%20println!(%22v%3A%20%7B%3A%3F%7D%22%2C%20v.borrow())%3B%0A%7D&version=stable&backtrace=0
[30]: https://play.rust-lang.org/?code=%23%5Ballow(unused_variables)%5D%0A%23%5Ballow(dead_code)%5D%0A%0Ause%20std%3A%3Async%3A%3A%7BArc%2C%20Mutex%7D%3B%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20v%20%3D%20Arc%3A%3Anew(Mutex%3A%3Anew(vec!(1%2C2%2C3)))%3B%0A%20%20%20%20let%20v1%20%3D%20v.clone()%3B%0A%20%20%20%20v1.lock().unwrap().push(4)%3B%0A%20%20%20%20println!(%22v%5B3%5D%3A%20%7B%7D%22%2C%20v.lock().unwrap()%5B3%5D)%3B%20%2F%2F%20-%3E%204%0A%7D&version=stable&backtrace=0
