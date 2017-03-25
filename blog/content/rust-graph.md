Date: 2017-03-25
Title: Rust: Implementación de estructuras complejas (Grafo)
Tags: wadobo, rust, programming, graph
Category: blog
Slug: rust-graph
Gravatar: 8da96af78e0089d6d970bf3760b0e724

Con el cambio de paradigma que supone la gestión de memoria de Rust, una de
las cosas que pueden resultar más difíciles al principio es la definición
de estructuras de datos "complejas", con el concepto de propiedad de
memoria y referencias, definir cosas como una lista enlazada no es tan
"sencillo" como en C.

Por supuesto esto no es sencillo porque definir este tipo de estructuras de
forma segura es muy complejo, en C es muy fácil definir lo básico, con
punteros, pero también es muy fácil que una lista enlazada apunte a un nodo
eliminado, etc.

Voy a explicar diferentes aproximaciones para implementar una estructura
cíclica en Rust, en este caso, vamos a definir un grafo.

He creado un [repositorio en github][1] con el código para que se pueda
estudiar. En este artículo pondré partes del código para mostrar lo básico
de la implementación, pero sobretodo me centraré en explicar la teoría
detrás de cada solución.

## Problema

Queremos implementar una estructura de datos sencilla para manejar grafos
dirigidos.

Un grafo no es más que una lista de vértices conectados entre sí. Cada nodo
tiene un valor, y una lista de nodos a los que apunta.

Podemos pensar en una primera implementación donde definamos cada nodo, con
su valor y que tenga una lista de nodos hijos.

```rust
struct GraphNode<T> {
    value: T,
    childs: Vec<GraphNode<T>>,
}
```

Pero dada la gestión de memoria que se hace en Rust, esta estructura no nos
valdría de mucho, ya que tendríamos que tener una copia diferente de un
nodo para cada referencia, añadimos un nodo a otro, y luego intentamos
usarlo, no podremos, porque será el nodo padre el que tenga la propiedad de
sus hijos.

Con esta solución en realidad cada nodo es independiente, no se reutilizan,
por lo que deja de ser útil para nuestro caso.

Lo primero que se nos ocurre para solucionar este problema es usar
referencias:

```rust
struct GraphNode<T> {
    value: T,
    childs: Vec<&GraphNode<T>>,
}
```

Pero esto no compila, al usar referencias el compilador nos pide que
definamos el lifetime de estas referencias, y al ser una estructura
recursiva, se complica mucho el tema, los nodos se deben almacenar en
alguna parte y ser referenciados entre sí, además, dado que en rust no es
compatible tener referencias no mutables a la vez que una referencia
mutable, no podríamos modificar estos nodos hijos por la referencia.

## Usando punteros, unsafe

Una primera solución que se nos puede ocurrir es tirar directamente de
punteros tipo C. Rust nos da la posibilidad de acceder a la memoria como en
C, con punteros, de esta forma nos podemos saltar las limitaciones del
compilador de Rust, pero esto implica que también perdemos la gestión de
memoria, por lo que tendremos que controlar nosotros la memoria y perdemos
la seguridad que nos proporciona el compilador.

El uso de punteros en Rust nos obliga a usar el calificador **unsafe**,
para poder diferenciar de forma rápida el código seguro, donde la gestión
de memoria se comprueba en tiempo de compilación, del código inseguro, que
es código donde la memoria se gestiona de manera manual.

```rust
pub struct GraphNode<T> {
    pub value: T,
    pub childs: Vec<*mut GraphNode<T>>,
}
```

El tipo de dato [**Box**][2] nos permite convertir a puntero o desde
puntero de forma sencilla con los métodos **into_raw** y **from_raw**.

```rust
pub fn add_child(&mut self, node: &mut GraphNode<T>, value: T) -> *mut GraphNode<T> {
    let n = Box::new(GraphNode::new(value));
    let pointer = Box::into_raw(n);
    node.childs.push(pointer);
    pointer
}
```

Y podemos acceder al valor de un puntero utilizando el operador \* para
deferenciar el puntero.

```rust
unsafe {
    (*node).value
}
```

Con **into_raw** Rust deja la gestión de la memoria en nuestras manos, por
lo que para evitar memory leaks tenemos que destruir esa memoria en algún
momento, y para ello podemos usar el **from_raw** que hace la operación
inversa y devuelve a Rust la gestión de esa memoria.

## Usando referencias, Rc<RefCell<Node\>\>, Arc<Mutex<Node\>\>

El uso de punteros es algo de lo que queremos huir cuando usamos Rust, ya
que es código *menos seguro*. Por eso debemos dejar el uso de punteros sólo
para momentos en los que necesitemos eficiencia a nivel de memoria o
velocidad y sepamos exactamente lo que estamos haciendo.

En Rust hay una estructura que nos ofrece la posibilidad de implementar
algo *similar* a los punteros, el [contador de referencias][3]. El patrón
básico para permitir modificaciones de elementos interiores, es la
composición **Rc<RefCell<T\>\>**.

```rust
use std::cell::RefCell;
use std::rc::Rc;

type GraphNodeRef<T> = Rc<RefCell<GraphNode<T>>>;

pub struct GraphNode<T> {
    pub value: T,
    pub childs: Vec<GraphNodeRef<T>>,
}
```

De esta forma podemos hacer un uso exactamente igual al de los punteros,
pero con la seguridad de que no tendremos problemas de seguridad de
memoria.

```rust
pub fn add_child(&mut self, node: GraphNodeRef<T>, value: T) -> GraphNodeRef<T> {
    let n = GraphNode::new(value);
    let rnode = Rc::new(RefCell::new(n));
    node.borrow_mut().childs.push(rnode.clone());
    rnode
}
```

En lugar de usar \* para deferenciar los punteros, en este caso usamos
**borrow** y **borrow_mut** para obetener una referencia. Con el método
**clone**, el tipo **Rc** crea una referencia nueva, no duplica la
información en sí, y cuando se queda sin referencias es cuando se elimina
el contenido.

Esta solución nos permite hacer algo muy parecido a lo que hacemos con
punteros, pero sin preocuparnos de tener que eliminar la memoria o de que
hay overflow o lo que sea.

Sin embargo, esto no es la panacea, hay un problema si se generan ciclos,
ya que las referencias cíclicas no se eliminarán nunca, no es algo muy
grave, pero hay que tenerlo en cuenta, aunque ya hay alguien que ha
implementado un [recolector de basura][4] para estos casos.

De forma similar, en caso de querer que sea **thread safe**, se puede usar
**Arc<Mutex<T\>\>**.

## Usando una estructura básica e identificadores de nodos, Vec, HashMap

Otra posible aproximación puede ser usar una estructura básica de Rust,
como un Vec o un HashMap, para almacenar todos los elementos, y luego
definir las referencias de los nodos usando índices a esta estructura.

Por ejemplo podríamos definir un vector con todos los nodos de nuestro
grafo, y cada nodo define sus hijos como índices en ese vector, números
enteros.

```rust
pub struct Graph<T> {
    pub nodes: Vec<GraphNode<T>>,
    pub idx: u32,
}

pub struct GraphNode<T> {
    pub value: T,
    pub childs: Vec<u32>,
}
```

En el código de ejemplo he usado HashMap en lugar de Vec, porque si por
ejemplo queremos poder eliminar un nodo de forma fácil, en un Vec
tendríamos que recorrer todo el vector y cambiar los indices de todos los
nodos con cada cambio.

```rust
use std::collections::HashMap;

pub struct Graph<T> {
    pub nodes: HashMap<u32, GraphNode<T>>,
    pub idx: u32, // índice del siguiente nodo que se añada
}

pub struct GraphNode<T> {
    pub value: T,
    pub childs: Vec<u32>,
}
```

Con esta implementación, para nosotros los nodos serán enteros, y nos
podemos definir los métodos que hagan uso de estos índices.


```rust
pub fn add_child(&mut self, node: u32, value: T) -> u32 {
    let n = GraphNode::new(value);
    let idx = self.idx;

    self.nodes.insert(idx, n);
    self.idx += 1;

    self.nodes.get_mut(&node).unwrap().childs.push(idx);
    idx
}
```

De esta forma, todo el código será seguro y además no utilizamos
referencias, simplemente nos estamos implementando nuestros propios
*punteros*. Aquí tenemos el compilador que comprueba la seguridad de la
memoria, pero si no manejamos correctamente los índices enteros, podemos
tener algún que otro **panic**, aunque siempre es mejor un **panic** que un
**segmentation fault**, un **painc** es algo controlable y no da los mismos
problemas que podría dar un *overflow*.

## Conclusiones

Este ejemplo nos sirve para conocer diferentes formas de resolver un
problema, con las herramientas que nos da Rust, pero también nos muestra
que no sólo hay una solución correcta a un problema, se puede pensar de
manera diferente e implementar.

Para mi, en principio la manera más *natural* es la de **Rc<RefCell\>\>**,
viniendo de usar C y C++ y pensando en no usar punteros, pero después de
investigar, veo que la opción de usar el **HashMap** no me parece ninguna
locura, y se me ocurren otras formas de almacenar un grafo en memoria.

Por supuesto no soy un experto en este tipo de implementaciones y quizás
esté haciendo alguna locura, si ese es el caso, no dudes en comentar y
corregir cualquier gazapo.

[1]: https://github.com/danigm/rust-graph-example
[2]: https://doc.rust-lang.org/std/boxed/struct.Box.html
[3]: https://doc.rust-lang.org/std/rc/
[4]: https://github.com/cmr/rust-cc
