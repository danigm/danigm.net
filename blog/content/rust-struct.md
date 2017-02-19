Date: 2017-02-19
Title: Rust: Structs y Traits
Tags: wadobo, rust, programming
Category: blog
Slug: rust-traits
Gravatar: 8da96af78e0089d6d970bf3760b0e724

Rust ofrece por defecto los tipos de datos básicos que ofrece cualquier
lenguaje de programación, pero al igual que en otros lenguajes, se pueden
definir tipos propios más complejos con *struct*.

Rust no es un lenguaje orientado a objetos, y en su documentación no se
encuentra nada sobre clases, objetos, instancias, etc. Sin embargo, hay
conceptos similares cuando nos adentramos en la definición de nuevos tipos
con *struct* y también con los *traits*, donde sí tenemos cosas como la
herencia.

## [Structs][1], "Estructuras" y tipos de datos complejos

Los tipos de datos propios en Rust se definen con la palabra clave
*struct*. Para quien venga de C/C++ todo este código le será familiar.

```rust
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point{x: 0, y: 0};
    println!("Punto: ({}, {})", p.x, p.y);
}
```
[ejecutar][20]

También existen estructuras de tipo tupla, *Tuple Structs*, que no son más
que estructuras donde los atributos van sin nombre, por índice.

```rust
struct Point(i32, i32);

fn main() {
    let p = Point(0, 0);
    println!("Punto: ({}, {})", p.0, p.1);
}
```
[ejecutar][21]

Los atributos de las estructuras son privados por defecto, esto quiere
decir que no son accesibles cuando se usan desde un módulo diferente al de
su definición, en el módulo de su definición, todos los atributos son
accesibles. Para hacer un atributo accesible a todo el mundo tan sólo hay
que añadir la palabra clave *pub* delante, en la definición.

```rust
struct Point {
    pub x: i32,
    pub y: i32,
}
```

### Métodos

Además de los atributos normales de las estructuras, también se pueden
definir métodos que *implementa* esta estructura. Esto es muy similar a los
métodos de la programación orientada a objetos, y en realidad serán
llamados de forma similar, con el "*.*".

Para implementar métodos para una estructura se utiliza la palabra clave
*impl*.

```rust
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn new() -> Point {
        Point{x: 0, y: 0}
    }

    fn distance(&self, p: &Point) -> f32 {
        let d1 = (self.x - p.x).pow(2);
        let d2 = (self.y - p.y).pow(2);

        f32::sqrt((d1 + d2) as f32)
    }
}

impl Point {
    fn moveup(&mut self) {
        self.y += 1;
    }
}

fn main() {
    let mut p1 = Point::new();
    p1.moveup();

    let p2 = Point{x: 24, y: -30};

    println!("distancia: {}", p2.distance(&p1));
}
```
[ejecutar][22]

En este ejemplo hay varias cosas interesantes. Lo primero es el método
*new*, que es un método estático, osea, no se llama desde una estructura
instanciada, sino con el nombre de la estructura y el operador *::*. En
este caso se usa como un constructor.

Luego se implementa el método para calcular la distancia, que recibe un
primer parámetro sin tipo, pero llamado *self*, este parámetro es la
estructura en sí, y como en python es explícito, hay que ponerlo en la
lista de argumentos. En este caso se define como una referencia, pero al
igual que todas las definiciones de variables en Rust dependerá del uso que
queramos darle, si vamos a modificar debería ser un *&mut self* o si queremos
que vaya por *copia/movimiento* un simple *self*.

La otra cosa interesante de este ejemplo es que hay dos declaraciones de
*impl* para la estructura *Point*, y en realidad puede haber cuantas se
quiera, incluso se pueden añadir métodos a estructuras desde módulos
diferentes, pero no desde *crates* diferentes.

Con esto casi podríamos decir que tenemos lo mismo que en otros lenguajes
orientados a objetos, pero no tenemos herencia, polimorfismo ni nada de
eso, para ello existen los *Traits*.

## [Traits][2], "Rasgos" de tipos

Los *traits* no son más que una lista de métodos con o sin implementación
que las estructuras o los tipos deben implementar para cumplir ese *trait*.

Se definen con la palabra clave *trait* y una lista de funciones que
definen la *interfaz* y luego se implementa con la construcción **impl** TRAIT **for** TYPE.

```rust
struct Point {
    x: i32,
    y: i32,
}

trait Distance {
    fn distance(&self, p: &Point) -> f32;
}

impl Distance for Point {
    fn distance(&self, p: &Point) -> f32 {
        let d1 = (self.x - p.x).pow(2);
        let d2 = (self.y - p.y).pow(2);

        f32::sqrt((d1 + d2) as f32)
    }
}

fn main() {
    let p1 = Point{x: 0, y: 0};
    let p2 = Point{x: 24, y: -30};

    println!("distancia: {}", p2.distance(&p1));
}
```
[ejecutar][23]

Los *traits* se pueden usar en las definiciones de las funciones o de las
estructuras, en lugar de los tipos, para implementar funciones o tipos
*genéricos*, con la sintaxis de tipo genérico **<T: TRAIT\>**.

También se pueden definir implementaciones por defecto en los métodos de
los *traits*, por lo que no es obligatorio ofrecer una implementación para
esos métodos, si se ofrece una implementación estaremos sobreescribiendo
ese método, si no se utilizará la implementación por defecto.

Por ejemplo, podemos definir un *trait* para tipos que tengan posición en
un plano 2D, **HasPosition**, y podemos definir la distancia del *trait*
**Distance** como un método que recibe un tipo que tiene posición como
segundo argumento.

```rust
struct Point {
    x: i32,
    y: i32,
}

struct Circle {
    x: i32,
    y: i32,
    r: i32,
}

trait HasPosition {
    fn getx(&self) -> i32;
    fn gety(&self) -> i32;

    fn pos(&self) -> Point {
        Point { x: self.getx(), y: self.gety() }
    }
}

impl HasPosition for Circle {
    fn getx(&self) -> i32 { self.x }
    fn gety(&self) -> i32 { self.y }
}

impl HasPosition for Point {
    fn getx(&self) -> i32 { self.x }
    fn gety(&self) -> i32 { self.y }
}

trait Distance {
    fn distance<T: HasPosition>(&self, p: &T) -> f32;
}

impl Distance for Point {
    fn distance<T: HasPosition>(&self, p: &T) -> f32 {
        let d1 = (self.x - p.pos().x).pow(2);
        let d2 = (self.y - p.pos().y).pow(2);

        f32::sqrt((d1 + d2) as f32)
    }
}

fn main() {
    let p1 = Point{x: 0, y: 0};
    let p2 = Circle{x: 24, y: -30, r: 1};

    println!("distancia: {}", p1.distance(&p2));
}
```
[ejecutar][24]

En este ejemplo se definen dos estructuras, **Point** y **Circle** y dos
*traits*, **HasPosition** y **Distance**, así podemos comparar distancias
no sólo entre puntos, sino que también entre puntos y círculos, ya que
estas dos estructuras implementan el *trait* **HasPosition**.

Los métodos *getx* y *gety* se tienen que implementar obligatoriamente, ya
que no se ofrece una implementación por defecto, sin embargo, el método
*pos* no se está sobreescribiendo en ninguna de las dos estructuras, y por
lo tanto se usa la implementación por defecto del *trait*.

### Combinación de *Traits*

En ocasiones queremos que un tipo implemente varios *traits* y esto se
puede definir utilizando el símbolo "**+**":

```rust
fn f<T, K>(x: &T, y: &K) -> K
    where T: HasPosition,
          K: HasPosition + Distance + Clone {
    // Implementación de la función
}
```

En esta definición se puede ver cómo el tipo *K* tiene que implementar tres
*traits* mientras que el tipo *T* sólo ha de implementar uno. Aquí también
introduzco el uso de *where* para que la cabecera de la función quede más
clara.

### Herencia

Como he comentado antes, *Rust* no es un lenguaje orientado a objetos como
tal, los *structs* y los *traits* no son clases, aunque el código pueda ser
similar.

Aún así, con los *traits* se puede hacer algo similar a la herencia,
utilizando el operador "**:**". Con esta definición se obliga a que si se
implementa un *trait* también se tengan que implementar el resto de
*traits*.

```rust
trait Distance: HasPosition {
    fn distance<T: HasPosition>(&self, p: &T) -> f32 {
        let p1 = self.pos();
        let p2 = p.pos();
        let d1 = (p1.x - p2.x).pow(2);
        let d2 = (p1.y - p2.y).pow(2);

        f32::sqrt((d1 + d2) as f32)
    }
}

impl Distance for Point {}
impl Distance for Circle {}
```

En este ejemplo se define el *trait* **Distance**, que depende del *trait*
**HasPosition**.

En la *herencia* también se puede utilizar la combinación de *traits* con
el operador "**+**".

Pero en realidad, no se puede considerar esto como herencia, ya que no hay
posibilidad de llamar al método *padre*, por lo que no es posible encadenar
llamadas de métodos por defecto cuando una estructura implementa un
*trait*. Si se sobreescribe un método de un *trait* se tiene que escribir
todo el código, no es posible utilizar la implementación por defecto para
sobreescribir el método.

## Conclusiones

Con las estructuras y los *traits* se puede escribir código reutilizable,
definiendo funciones que reciban tipos *genéricos* que implementen una
serie de interfaces (*traits*) de tal forma que el mismo código sirva para
diferentes tipos.

En *Rust* todo el código de la librería estándar está fuertemente basado en
*traits* y por lo tanto hay una serie de *traits* que es necesario conocer,
porque sirven para implementar funcionamiento básico, como por ejemplo,
[Iterator](https://doc.rust-lang.org/std/iter/trait.Iterator.html),
[Copy](https://doc.rust-lang.org/std/marker/trait.Copy.html),
[Clone](https://doc.rust-lang.org/std/clone/trait.Clone.html),
[Debug](https://doc.rust-lang.org/std/fmt/trait.Debug.html).


[1]: https://doc.rust-lang.org/book/structs.html
[2]: https://doc.rust-lang.org/book/traits.html

[20]: https://play.rust-lang.org/?code=%23%5Ballow(unused_variables)%5D%0A%23%5Ballow(dead_code)%5D%0A%0Astruct%20Point%20%7B%0A%20%20%20%20x%3A%20i32%2C%0A%20%20%20%20y%3A%20i32%2C%0A%7D%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20p%20%3D%20Point%7Bx%3A%200%2C%20y%3A%200%7D%3B%0A%20%20%20%20println!(%22Punto%3A%20(%7B%7D%2C%20%7B%7D)%22%2C%20p.x%2C%20p.y)%3B%0A%7D&version=stable&backtrace=0
[21]: https://play.rust-lang.org/?code=%23%5Ballow(unused_variables)%5D%0A%23%5Ballow(dead_code)%5D%0A%0Astruct%20Point(i32%2C%20i32)%3B%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20p%20%3D%20Point(0%2C%200)%3B%0A%20%20%20%20println!(%22Punto%3A%20(%7B%7D%2C%20%7B%7D)%22%2C%20p.0%2C%20p.1)%3B%0A%7D%0A&version=stable&backtrace=0
[22]: https://play.rust-lang.org/?code=%23%5Ballow(unused_variables)%5D%0A%23%5Ballow(dead_code)%5D%0A%0Astruct%20Point%20%7B%0A%20%20%20%20x%3A%20i32%2C%0A%20%20%20%20y%3A%20i32%2C%0A%7D%0A%0Aimpl%20Point%20%7B%0A%20%20%20%20fn%20new()%20-%3E%20Point%20%7B%0A%20%20%20%20%20%20%20%20Point%7Bx%3A%200%2C%20y%3A%200%7D%0A%20%20%20%20%7D%0A%0A%20%20%20%20fn%20distance(%26self%2C%20p%3A%20%26Point)%20-%3E%20f32%20%7B%0A%20%20%20%20%20%20%20%20let%20d1%20%3D%20(self.x%20-%20p.x).pow(2)%3B%0A%20%20%20%20%20%20%20%20let%20d2%20%3D%20(self.y%20-%20p.y).pow(2)%3B%0A%0A%20%20%20%20%20%20%20%20f32%3A%3Asqrt((d1%20%2B%20d2)%20as%20f32)%0A%20%20%20%20%7D%0A%7D%0A%0Aimpl%20Point%20%7B%0A%20%20%20%20fn%20moveup(%26mut%20self)%20%7B%0A%20%20%20%20%20%20%20%20self.y%20%2B%3D%201%3B%0A%20%20%20%20%7D%0A%7D%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20mut%20p1%20%3D%20Point%3A%3Anew()%3B%0A%20%20%20%20p1.moveup()%3B%0A%0A%20%20%20%20let%20p2%20%3D%20Point%7Bx%3A%2024%2C%20y%3A%20-30%7D%3B%0A%0A%20%20%20%20println!(%22distancia%3A%20%7B%7D%22%2C%20p2.distance(%26p1))%3B%0A%7D&version=stable&backtrace=0
[23]: https://play.rust-lang.org/?code=%23%5Ballow(unused_variables)%5D%0A%23%5Ballow(dead_code)%5D%0A%0Astruct%20Point%20%7B%0A%20%20%20%20x%3A%20i32%2C%0A%20%20%20%20y%3A%20i32%2C%0A%7D%0A%0Atrait%20Distance%20%7B%0A%20%20%20%20fn%20distance(%26self%2C%20p%3A%20%26Point)%20-%3E%20f32%3B%0A%7D%0A%0Aimpl%20Distance%20for%20Point%20%7B%0A%20%20%20%20fn%20distance(%26self%2C%20p%3A%20%26Point)%20-%3E%20f32%20%7B%0A%20%20%20%20%20%20%20%20let%20d1%20%3D%20(self.x%20-%20p.x).pow(2)%3B%0A%20%20%20%20%20%20%20%20let%20d2%20%3D%20(self.y%20-%20p.y).pow(2)%3B%0A%0A%20%20%20%20%20%20%20%20f32%3A%3Asqrt((d1%20%2B%20d2)%20as%20f32)%0A%20%20%20%20%7D%0A%7D%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20p1%20%3D%20Point%7Bx%3A%200%2C%20y%3A%200%7D%3B%0A%20%20%20%20let%20p2%20%3D%20Point%7Bx%3A%2024%2C%20y%3A%20-30%7D%3B%0A%0A%20%20%20%20println!(%22distancia%3A%20%7B%7D%22%2C%20p2.distance(%26p1))%3B%0A%7D&version=stable&backtrace=0
[24]: https://play.rust-lang.org/?code=%23%5Ballow(unused_variables)%5D%0A%23%5Ballow(dead_code)%5D%0A%0Astruct%20Point%20%7B%0A%20%20%20%20x%3A%20i32%2C%0A%20%20%20%20y%3A%20i32%2C%0A%7D%0A%0Astruct%20Circle%20%7B%0A%20%20%20%20x%3A%20i32%2C%0A%20%20%20%20y%3A%20i32%2C%0A%20%20%20%20r%3A%20i32%2C%0A%7D%0A%0Atrait%20HasPosition%20%7B%0A%20%20%20%20fn%20getx(%26self)%20-%3E%20i32%3B%0A%20%20%20%20fn%20gety(%26self)%20-%3E%20i32%3B%0A%0A%20%20%20%20fn%20pos(%26self)%20-%3E%20Point%20%7B%0A%20%20%20%20%20%20%20%20Point%20%7B%20x%3A%20self.getx()%2C%20y%3A%20self.gety()%20%7D%0A%20%20%20%20%7D%0A%7D%0A%0Aimpl%20HasPosition%20for%20Circle%20%7B%0A%20%20%20%20fn%20getx(%26self)%20-%3E%20i32%20%7B%20self.x%20%7D%0A%20%20%20%20fn%20gety(%26self)%20-%3E%20i32%20%7B%20self.y%20%7D%0A%7D%0A%0Aimpl%20HasPosition%20for%20Point%20%7B%0A%20%20%20%20fn%20getx(%26self)%20-%3E%20i32%20%7B%20self.x%20%7D%0A%20%20%20%20fn%20gety(%26self)%20-%3E%20i32%20%7B%20self.y%20%7D%0A%7D%0A%0Atrait%20Distance%20%7B%0A%20%20%20%20fn%20distance%3CT%3A%20HasPosition%3E(%26self%2C%20p%3A%20%26T)%20-%3E%20f32%3B%0A%7D%0A%0Aimpl%20Distance%20for%20Point%20%7B%0A%20%20%20%20fn%20distance%3CT%3A%20HasPosition%3E(%26self%2C%20p%3A%20%26T)%20-%3E%20f32%20%7B%0A%20%20%20%20%20%20%20%20let%20d1%20%3D%20(self.x%20-%20p.pos().x).pow(2)%3B%0A%20%20%20%20%20%20%20%20let%20d2%20%3D%20(self.y%20-%20p.pos().y).pow(2)%3B%0A%0A%20%20%20%20%20%20%20%20f32%3A%3Asqrt((d1%20%2B%20d2)%20as%20f32)%0A%20%20%20%20%7D%0A%7D%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20p1%20%3D%20Point%7Bx%3A%200%2C%20y%3A%200%7D%3B%0A%20%20%20%20let%20p2%20%3D%20Circle%7Bx%3A%2024%2C%20y%3A%20-30%2C%20r%3A%201%7D%3B%0A%0A%20%20%20%20println!(%22distancia%3A%20%7B%7D%22%2C%20p1.distance(%26p2))%3B%0A%7D&version=stable&backtrace=0
