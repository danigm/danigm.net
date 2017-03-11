Date: 2017-03-11
Title: Rust: Pattern Matching
Tags: wadobo, rust, programming
Category: blog
Slug: rust-match
Gravatar: 8da96af78e0089d6d970bf3760b0e724

En Rust se utiliza mucho la *búsqueda de patrones*, más conocida como
**pattern matching**. Es una estructura lógica en el código que permite
hacer varias cosas diferentes de una forma muy sencilla. Se puede usar por
ejemplo para hacer algo similar al **switch** de lenguajes como **C/C++**,
pero también se puede usar para asignaciones complejas, descomposición de
estructuras comprobación de errores, etc.

Con el **pattern matching** lo que se hace, básicamente, es definir
condiciones o asignaciones en función de un patrón. Se podría decir que es
algo similar a las expresiones regulares, pero más simple, y aplicado a la
escritura de código.

En este artículo definiré el uso principal en Rust, que es el uso dentro de
los **match**, y también otros usos, como la asignación o la asignación
condicional.

## [Match][1]

*Match* es una expresión condicional en *Rust*. Se aplica sobre una
variable y se definen una serie de patrones, y sólo se ejecuta el código
correspondiente al patrón que concuerde con la variable.

El uso principal que se le puede dar a *match* es el de condición múltiple,
tenemos una estructura *if/else if/else if*, que podemos simplificar con
una sola expresión.

```rust
let x = 5;
match x {
    1 => println!("uno"),
    2 => println!("dos"),
    3 => println!("tres"),
    4 => println!("cuatro"),
    5 => println!("cinco"),
    _ => println!("> 5"),
}
```
[ejecutar][20]

Con este match, tenemos la condición múltiple, comprobamos un entero y
según el que sea se imprime ese número en texto.

Como se puede ver en el ejemplo, se usa el operador *=>* para diferenciar
el patrón y lo que se ejecuta si se cumple. Lo que se ejecuta no tiene por
qué ser una sola línea, se pueden ejecutar varias sentencias englobándolo
en unas llaves.

```rust
let x = 5;
match x {
    1 => println!("uno"),
    2 => println!("dos"),
    3 => println!("tres"),
    4 => println!("cuatro"),
    5 => {
        println!("cinco");
        println!("el valor es {}", x);
    }
    _ => println!("> 5"),
}
```

El match también es muy usado para asignaciones, devuelve lo que se
devuelva dentro de las condiciones, por lo tanto se puede usar en una
asignación let.

```rust
let x = 5;
let number = match x {
    1 => "uno",
    2 => "dos",
    3 => "tres",
    4 => "cuatro",
    5 => {
        println!("detro del match");
        "cinco"
    }
    _ => "> 5",
};
println!("{:?}", number);
```
[ejecutar][21]

Además de patrones simples de enteros o cadenas, en el match se pueden usar
*Enums*, estructuras y otras composiciones que lo hacen bastante más
potente, veamoslo con más detalle en el apartado de *Patrones*.

Hay que tener en cuenta que los patrones han de ser completos, es decir,
han de cubrir todas las posibilidades de la variable sobre la que se hace
*match*. Otra cosa importante es que se ejecutan de arriba hacia abajo, por
lo que la definición ha de ser de más concreto a más genérico siempre, ya
que si no, el compilador se quejará porque existen patrones que nunca se
alcanzarán.

## [Patrones][2]

Como hemos visto con el *match*, los patrones se pueden definir con
literales directamente, y el caso de *_*, que se explica más adelante.

Además de la comprobación con literales, los patrones pueden *definir*
nuevas variables, que se pueden usar dentro del *match*.

```rust
let x = 5;
match x {
    n => println!("El valor de x es {}", n)
}
```

En este caso, al no poner un literal en la parte izquierda de la expresión,
en el patrón, se hace el matching y se asigna el valor de *x* a *n*. Hay
que tener cuidado con esto, porque es lo mismo que una asignación con
*let*, en el caso de que el tipo implemente *Copy* se hará una copia, en
otro caso se hará un *move*. Para modificar estos comportamientos se pueden
usar *ref* y *ref mut*, pero eso lo veremos más adelante.

### Múltiples patrones

Se pueden definir múltiples patrones que ejecuten la misma secuencia, esto
podría verse como algo similar a lo que se hace en los *switch* cuando se
deja un case vacío, que sabes que se ejecutará lo mismo para este y para el
siguiente.

```rust
let x = 5;
match x {
    1 | 2 => println!("uno o dos"),
    _ => println!("otro número"),
}
```

Se utiliza el operador **|** para definir patrones múltiples. Se intenta
hacer matching con la primera parte del **|** y si no, se intenta con la
segunda, si alguno de los dos patrones concuerdan con el valor, se ejecuta
la sentencia.

### Descomposición

El pattern matching es muy útil cuando estamos usando estructuras más o
menos complejas o enums, ya que permite descomponer el valor de forma fácil
y acceder a componentes de estas estructuras de forma directa.

```rust
struct Complex {
    real: i32,
    img: i32,
};

let x = Complex{real: 5, img: 3};
match x {
    Complex{real: _, img: 0} => println!("parte imaginaria es 0"),
    Complex{real: r, img: i} => println!("{},{}i", r, i),
}
```
[ejecutar][22]

En este ejemplo se define una estructura compleja, con dos valores enteros,
y en el match se puede ver cómo se descompone, pudiendo acceder de forma
rápida y sencilla a los valores correspondientes. En el primer patrón se
ignora la parte real y se obliga a que la parte imaginaria sea 0, y en el
segundo patrón entraría cualquier otra cosa, y tenemos acceso a *r* e *i*
con los valores en concreto del valor de *x*.

La descomposición se puede usar para gestión de errores con los enums
*Option* y *Result*, teniendo expresiones del tipo:

```rust
match x.get(0) {
    Some(v) => println!("valor {}", v),
    None => println!("no existe"),
}
match somecall() {
    ok(v) => println!("resultado {}", v),
    err(_) => println!("ha ocurrido un error"),
}
```

### Ignorando variables o componentes

En los ejemplos anteriores ya hemos ignorado algunas variables, que en un
caso concreto no nos interesan dentro del match, para ello se usa el
operador **_**.

En otras ocasiones, dentro de una descomposición, por ejemplo, queremos
ignorar todos los elementos de este, o una parte y para eso existe el
operador **..**.

```rust
struct Complex {
    real: i32,
    img: i32,
};

let x = Complex{real: 5, img: 3};
match x {
    Complex{real: _, img: 0} => println!("parte imaginaria es 0"),
    Complex{..} => println!("Cualquier complejo"),
}
```

El operador **..** se puede usar como en el ejemplo, para ignorar todo, o
para ignorar sólo parte, si tuviéramos una estructura más compleja, con 5
variables, por ejemplo, y sólo nos interesa una:

```rust
struct SuperComplex {
    real: i32,
    img: i32,
    real1: i32,
    img1: i32,
    real2: i32,
    img2: i32,
};

let x = SuperComplex{real: 5, img: 3, real1: 6, img1: 4, real2: 2, img2: 8};
match x {
    SuperComplex{img1: 0, ..} => println!("parte imaginaria 1 es 0"),
    SuperComplex{..} => println!("Cualquier complejo"),
}
```

### Referencias (ref, ref mut)

Cuando se definen nuevos nombres en el match, se crean nuevas variables, de
forma similar a cuando se hace un let, y por lo tanto, entra en juego la
gestión de memoria. Por defecto se hace un *move*, pero habrá ocasiones en
las que no queramos eso, sino que queramos una referencia, para evitar que
la variable se destruya tras el match. Para eso se pueden usar las palabras
clave **ref** y **ref mut**.

```rust
struct Complex {
    real: i32,
    img: i32,
};

let x = Complex{real: 5, img: 3};
match x {
    Complex{real: _, img: 0} => println!("parte imaginaria es 0"),
    ref a => println!("Cualquier complejo {}, {}i", a.real, a.img),
}

println!("parte real: {}", x.real);
```

En este ejemplo definimos el patrón *ref a*, por lo tanto, *a* es del tipo
*&Complex* y al ser una referencia, se puede usar *x* después del match sin
problemas. Si eliminamos el *ref*, el compilador nos daría un error, ya que
en el match se movería el valor de *x* a *a* y por tanto ya no se podría
usar *x* después del match.

### Rangos (Ranges)

Con el uso de literales enteros y caracteres existe una definición que
permite definir de forma simple un rango de valores, para ello se usa el
operador **...**.

```rust
let x = 5;
match x {
    1 ... 10 => println!("entre uno y diez"),
    _ => println!("mayor que diez"),
}

let x = 'A';
match x {
    'a' ... 'z' => println!("minúscula"),
    'A' ... 'Z' => println!("mayúscula"),
    _ => println!("otra cosa"),
}
```

### Enlaces (Bindings)

Se pueden asignar variables a patrones, no sólo como hemos visto en la
descomposición, sino de manera global, ya sea a patrones literales, o al
global de una descomposición, y para ello se usa el operador **@**:

```rust
let n = 5;
match n {
    i @ 1 ... 9 => println!("{} es menor de 10", i),
    _ => println!("mayor de 10"),
}

struct Complex {
    real: i32,
    img: i32,
};

let x = Complex{real: 5, img: 3};
match x {
    Complex{real: _, img: 0} => println!("parte imaginaria es 0"),
    ref a @ Complex{..} => println!("Cualquier complejo {}, {}i", a.real, a.img),
}

println!("parte real: {}", x.real);
```

Hay que tener en cuenta que si se usan múltiples condiciones con **|**, el
binding se aplica a una parte, no al conjunto:

```rust
let x = 5;
match x {
    i @ 1 | i @ 2 => println!("{}: uno o dos", i),
    _ => println!("otro número"),
}
```

### Condicionales (Guards)

En los patrones también se pueden definir condicionantes, de tal forma que
sólo se ejecute la sentencia correspondiente si se aplica el match y además
si se cumple cierta condición.

```rust
let x = 5;

match x {
    i if i < 5 => println!("{}: es menor que 5", i),
    _ => println!("otro número"),
}
```

Los condicionales se definen con **if** y detrás la condición que se quiera
comprobar, además se pueden usar las variables que defina el patrón para la
condición, por lo que nos proporcionan una gran potencia a la hora de
definir patrones.

En las condiciones múltiples con **|** el **if** se aplica sobre las dos
partes de la condición, por lo tanto no se pueden definir varios **if** en
un mismo patrón.

## Otros usos de los patrones

Además de para el **match**, los patrones se usan en Rust en diferentes
partes.

### [If let][3]

En muchas ocasiones, nos encontramos con variables que son del tipo
*Option* o *Result* y queremos hacer algo, sólo si tienen un valor, por
ejemplo:

```rust
if x.is_some() {
    println!("{}", x.unwrap());
}
```

Para simplificar este caso existe el **if let** que unifica la asignación y
el condicional en una sola línea, teniendo algo que sólo se ejecuta si el
patrón se aplica correctamente:

```rust
if let Some(v) = x {
    println!("{}", v);
}
```

### [Asignación][4]

Los patrones también se pueden usar directamente en las asignaciones con
*let*. Esto es realmente útil cuando lo combinamos con una descomposición
de una lista o una estructura:

```rust
let (a, b) = (1, 2);

struct Complex {
    real: i32,
    img: i32,
};

let x = Complex{real: 5, img: 3};

let Complex{real: r, ..} = x;
println!("parte real: {}", r);
```

Como se puede ver, el pattern matching es algo muy utilizado en Rust y
bastante potente, con lo que se puede escribir código simple que haga cosas
increíbles.

[1]: https://doc.rust-lang.org/book/match.html
[2]: https://doc.rust-lang.org/book/patterns.html
[3]: https://doc.rust-lang.org/book/if-let.html
[4]: https://doc.rust-lang.org/book/variable-bindings.html#patterns

[20]: https://play.rust-lang.org/?code=fn%20main()%20%7B%0A%20%20%20%20let%20x%20%3D%205%3B%0A%20%20%20%20match%20x%20%7B%0A%20%20%20%20%20%20%20%201%20%3D%3E%20println!(%22uno%22)%2C%0A%20%20%20%20%20%20%20%202%20%3D%3E%20println!(%22dos%22)%2C%0A%20%20%20%20%20%20%20%203%20%3D%3E%20println!(%22tres%22)%2C%0A%20%20%20%20%20%20%20%204%20%3D%3E%20println!(%22cuatro%22)%2C%0A%20%20%20%20%20%20%20%205%20%3D%3E%20println!(%22cinco%22)%2C%0A%20%20%20%20%20%20%20%20_%20%3D%3E%20println!(%22%3E%205%22)%2C%0A%20%20%20%20%7D%0A%7D&version=stable&backtrace=0
[21]: https://play.rust-lang.org/?code=fn%20main()%20%7B%0A%20%20%20%20let%20x%20%3D%205%3B%0A%20%20%20%20let%20number%20%3D%20match%20x%20%7B%0A%20%20%20%20%20%20%20%201%20%3D%3E%20%22uno%22%2C%0A%20%20%20%20%20%20%20%202%20%3D%3E%20%22dos%22%2C%0A%20%20%20%20%20%20%203%20%3D%3E%20%22tres%22%2C%0A%20%20%20%20%20%20%204%20%3D%3E%20%22cuatro%22%2C%0A%20%20%20%20%20%20%205%20%3D%3E%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20println!(%22detro%20del%20match%22)%3B%0A%20%20%20%20%20%20%20%20%20%20%20%22cinco%22%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20_%20%3D%3E%20%22%3E%205%22%2C%0A%20%20%20%20%7D%3B%0A%20%20%20%20println!(%22%7B%3A%3F%7D%22%2C%20number)%3B%0A%7D&version=stable&backtrace=0
[22]: https://play.rust-lang.org/?code=fn%20main()%20%7B%0A%20%20%20%20struct%20Complex%20%7B%0A%20%20%20%20%20%20%20%20real%3A%20i32%2C%0A%20%20%20%20%20%20%20%20img%3A%20i32%2C%0A%20%20%20%20%7D%3B%0A%0A%20%20%20%20let%20x%20%3D%20Complex%7Breal%3A%205%2C%20img%3A%203%7D%3B%0A%20%20%20%20match%20x%20%7B%0A%20%20%20%20%20%20%20%20Complex%7Breal%3A%20_%2C%20img%3A%200%7D%20%3D%3E%20println!(%22parte%20imaginaria%20es%200%22)%2C%0A%20%20%20%20%20%20%20%20Complex%7Breal%3A%20r%2C%20img%3A%20i%7D%20%3D%3E%20println!(%22%7B%7D%2C%7B%7Di%22%2C%20r%2C%20i)%2C%0A%20%20%20%20%7D%0A%7D%0A&version=stable&backtrace=0
