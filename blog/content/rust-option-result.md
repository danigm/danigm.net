Date: 2017-03-4
Title: Rust: Tipos nulos (Option) y gestión de errores (Result)
Tags: wadobo, rust, programming
Category: blog
Slug: rust-option-result
Gravatar: 8da96af78e0089d6d970bf3760b0e724

## [Option][1], Tipos nulos

En rust no existe el tipo especial *null*, como en C/C++, y al ser
fuertemente tipado, no se puede asignar algo de diferente tipo a una
variable, por lo tanto no es posible tener variables declaradas de un tipo,
por ejemplo *File* y que valga *null* si no está inicializado o algo así,
ni tampoco se puede devolver *null* o algo así, como se haría en C++, en
una función que declara como valor de retorno un tipo, y por alguna razón
no tiene sentido para una entrada determinada.

Lo que se usa en rust para solucionar este tipo de problemas y poder
asignar valores nulos a variables o en devoluciones es el [*enum
Option*][3], que se define como:

```rust
pub enum Option<T> {
    None,
    Some(T),
}
```

*None* sería el tipo *nulo* en rust, y *Some(T)* sería cuando tenemos un
valor. Por lo tanto, si queremos declarar una variable que en principio
pueda ser nula, la declararemos como *Option*:

```rust
struct User<'a> {
    username: &'a str,
    email: Option<&'a str>,
}

fn send_email(u: &User) {
    match u.email {
        Some(email) => println!("correo para {}", email),
        None => println!("{} no tiene correo asignado", u.username)
    }
}

fn main() {
    let mut u = User{ username: "danigm", email: None };
    send_email(&u);

    u.email = Some("danigm@wadobo.com");
    send_email(&u);
}
```
[ejecutar][20]

En este ejemplo, declaramos una estructura con dos atributos, el nombre de
usuario que es de tipo *&str* y el email, que es de tipo *Option&lt;&str>*,
para poder tener usuarios que no tengan email asociado.

En la función *send_email* se utiliza el [*match*][4] para diferenciar si
el valor es *None* o si tiene una cadena asociada y se actúa en
consecuencia.

Además de poder diferenciar el tipo *Option* con *patter matching*, también
dispone de algunos métodos que se pueden llamar para ver si tiene un valor
o no:

```rust
if u.email.is_some() {
    println!("email definido: {}", u.email.unwrap());
}

if u.email.is_none() {
    println!("email no definido");
}

println!("email: {}", u.email.unwrap_or("no definido"));
```

En este ejemplo se usan los métodos *is_some* e *is_none*, que te devuelven
un *bool* si el tipo es lo que preguntamos, y también se usan el *unwrap*,
que lo que hace es devolver el valor dentro del *Some*, por lo que daría un
*panic* si el *Option* es *None*. Y por último también se usa el
*unwrap_or*, que es similar al *unwrap*, pero que no fallaría en caso de
ser *None*, sino que devolvería el valor definido.

En la [documentación de *Option*][3] vienen todos los métodos y es
recomendable echarle un vistazo porque hay muchos que son muy interesantes.

## [Result][2], Gestión de errores

En rust no existen excepciones, como en python y otros lenguajes, para
gestionar los errores, ni tampoco se hace como C, que realmente no tiene
gestión de errores alguna, sino que se usa el valor de retorno para indicar
errores, devolviendo números negativos, por ejemplo, o 0, o algo similar.

En rust la gestión de errores se hace usando el tipo de retorno, pero no
devolviendo un valor determinado, sino devolviendo un tipo *Result*, que te
*obliga* a comprobar si ha funcionado bien antes de poder usar el valor
devuelto, evitando así problemas de uso de variables no inicializadas y
demás.

El tipo *Result* es muy similar al *Option*, que hemos visto anteriormente,
la única diferencia es que el *Result* se define con dos tipos genéricos,
el de la respuesta y el del error, para poder especificar el tipo de error:

```rust
pub enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

Es un simple *enum*, por lo tanto un *Result* puede ser o un *Ok(T)* o un
*Err(E)*

```rust
struct User<'a> {
    username: &'a str,
    email: Option<&'a str>,
}

fn transform_email(u: &User) -> Result<String, String> {
    match u.email {
        Some(email) => {
            let s = email.split('@').nth(0).unwrap();
            Ok(String::from(s) + "@newdomain.com")
        },
        None => Err(String::from("email no definido"))
    }
}

fn main() {
    let mut u = User{ username: "danigm", email: None };

    let ret = transform_email(&u);
    match ret {
        Ok(email) => println!("Este es el nuevo email: {}", email),
        Err(error) => println!("Error: {}", error)
    }

    u.email = Some("danigm@wadobo.com");
    if let Ok(email) = transform_email(&u) {
        println!("Nuevo email: {}", email);
    }
}
```
[ejecutar][21]

En este ejemplo se define la función *transform_email*, que devuelve un
*Result* con el tipo *String* para el *Ok* y también para el *Err*. En este
caso he usado este tipo para los dos posibles valores, pero normalmente el
tipo de error implementa el [*trait Error*][6].

En la función lo único que hacemos es mirar si está definido, haciendo un
*match* al *email* y en caso de estar definido devolvemos *Ok(...)* con la
cadena transformada, y en el caso de error devolvemos *Err(...)* con un
mensaje de error.

Luego a la hora de usarlo, al ser el valor devuelto de tipo *Result* y no
de tipo *String*, nos obliga a comprobar si la llamada ha sido correcta
antes de poder usar el valor de retorno real. Por lo tanto hay que hacer un
*pattern matching* y actuar en consecuencia si es un error o si es un valor
correcto.

Al igual que el *Option*, el tipo *Result* tiene métodos similares
definidos, como el *is_ok*, *is_err*, *unwrap*, *unwrap_or*, etc.

## Propagación de errores

Esta forma de gestionar errores es muy simple, pero al obligarte a
comprobar el tipo de respuesta de cada llamada que devuelve un *Result*,
hace que se introduzca mucho código de comprobación de errores en todas las
funciones, y normalmente lo que queremos es que si va bien continuamos y si
va mal, devolvemos un error, osea, propagamos el error hacia arriba, como
se haría en python con un *raise*, como funcionan las excepciones.

Para eso existe la macro [*"try!"*][7] en *Rust* que simplifica el código, y
recientemente también han añadido el nuevo operador *?* que hace lo mismo
que la macro *try!*, pero a nivel de compilador, por lo que es recomendable
usar este último. Sin embargo voy a mostrar código con las dos
posibilidades, porque supongo que aún habrá mucho código rust por ahí que
usa la macro *try!*.

```rust
use std::slice::Iter;

struct User<'a> {
    username: &'a str,
    email: Option<&'a str>,
}

fn transform_email(u: &User) -> Result<String, String> {
    match u.email {
        Some(email) => {
            let s = email.split('@').nth(0).unwrap();
            Ok(String::from(s) + "@newdomain.com")
        },
        None => Err(String::from("email no definido"))
    }
}

fn transform_all_emails(users: Iter<&User>) -> Result<(), String> {
    for u in users {
        let new = transform_email(u)?;
        println!("{} new email: {}", u.username, new);
    }

    Ok(())
}

fn main() {
    let mut u = User{ username: "danigm", email: None };
    let u2 = User{ username: "user2", email: Some("user2@wadobo.com") };

    if let Err(e) = transform_all_emails(vec![&u, &u2].iter()) {
        println!("Error: {}", e);
    }

    u.email = Some("danigm@wadobo.com");
    if let Err(e) = transform_all_emails(vec![&u, &u2].iter()) {
        println!("Error: {}", e);
    }
}
```
[ejecutar][22]

En este ejemplo, además de lo anterior, he definido otra función que
transforma todos los emails de una lista de usuarios y devuelve un *Result*
con la lista vacía si todo ha ido bien, o con un mensaje de error si algo
ha fallado. Dentro de esta función no hay un *return Err* por ninguna
parte, sin embargo se hace en la línea:

```rust
    let new = transform_email(u)?;
```

El operador *?* lo que hace es básicamente un *match* de la respuesta, si
es *Ok(t)*, devuelve *t*, si es un *Err(e)*, hace un *return Err(e)*, por
lo que el error se propaga hacia arriba, y el código que hay detrás puede
suponer que el valor de *new* es un *String*.

Como he comentado antes, el operador *?* es relativamente nuevo, el mismo
código usando la macro *try!* sería:

```rust
    let new = try!(transform_email(u));
```

El operador *?* sólo se puede usar dentro de funciones de devuelvan un
*Result* y que tengan como tipo de error el mismo o compatible con las
funciones que lo usan, ya que se va a hacer un *return* directamente del
error devuelto y por tanto esos tipos tienen que coincidir.

### Propagación de errores con Option

El operador *?* sólo vale para el tipo *Result*, sin embargo, el tipo
*Option* es muy similar y es muy típico que en una función o método sólo se
pueda continuar si el *Option* tiene valor, es decir, si no es *None*, por
lo tanto, puede ser interesante poder propagar los errores de forma
sencilla sin tener que hacer el *match* y el *return*.

Para eso se puede utilizar el método *ok_or* del tipo *Option*, que lo que
hace es devolverte un *Result* con el valor si es *Some(t)* y en caso de
ser *None* te devolverá *Err(e)*, siendo *e* la variable que se pasa como
único argumento al método.

```rust
...

fn print_all_emails(users: Iter<&User>) -> Result<(), String> {
    for u in users {
        let em = u.email.ok_or(String::from(u.username) + " sin email")?;
        println!("{}", em);
    }

    Ok(())
}

...
    if let Err(e) = print_all_emails(vec![&u, &u2].iter()) {
        println!("Error: {}", e);
    }
...
```

[1]: https://doc.rust-lang.org/std/option/index.html
[2]: https://doc.rust-lang.org/std/result/index.html
[3]: https://doc.rust-lang.org/std/option/enum.Option.html
[4]: https://doc.rust-lang.org/book/match.html
[5]: https://doc.rust-lang.org/std/result/enum.Result.html
[6]: https://doc.rust-lang.org/std/error/trait.Error.html
[7]: https://doc.rust-lang.org/std/macro.try.html
[8]: https://doc.rust-lang.org/std/option/enum.Option.html#method.ok_or

[20]: https://play.rust-lang.org/?code=struct%20User%3C%27a%3E%20%7B%0A%20%20%20%20username%3A%20%26%27a%20str%2C%0A%20%20%20%20email%3A%20Option%3C%26%27a%20str%3E%2C%0A%7D%0A%0Afn%20send_email(u%3A%20%26User)%20%7B%0A%20%20%20%20match%20u.email%20%7B%0A%20%20%20%20%20%20%20%20Some(email)%20%3D%3E%20println!(%22correo%20para%20%7B%7D%22%2C%20email)%2C%0A%20%20%20%20%20%20%20%20None%20%3D%3E%20println!(%22%7B%7D%20no%20tiene%20correo%20asignado%22%2C%20u.username)%0A%20%20%20%20%7D%0A%7D%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20mut%20u%20%3D%20User%7B%20username%3A%20%22danigm%22%2C%20email%3A%20None%20%7D%3B%0A%20%20%20%20send_email(%26u)%3B%0A%0A%20%20%20%20u.email%20%3D%20Some(%22danigm%40wadobo.com%22)%3B%0A%20%20%20%20send_email(%26u)%3B%0A%7D&version=stable&backtrace=0
[21]: https://play.rust-lang.org/?code=%23%5Ballow(dead_code)%5D%0A%23%5Ballow(unused_variables)%5D%0A%0Astruct%20User%3C%27a%3E%20%7B%0A%20%20%20%20username%3A%20%26%27a%20str%2C%0A%20%20%20%20email%3A%20Option%3C%26%27a%20str%3E%2C%0A%7D%0A%0Afn%20transform_email(u%3A%20%26User)%20-%3E%20Result%3CString%2C%20String%3E%20%7B%0A%20%20%20%20match%20u.email%20%7B%0A%20%20%20%20%20%20%20%20Some(email)%20%3D%3E%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20let%20s%20%3D%20email.split(%27%40%27).nth(0).unwrap()%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20Ok(String%3A%3Afrom(s)%20%2B%20%22%40newdomain.com%22)%0A%20%20%20%20%20%20%20%20%7D%2C%0A%20%20%20%20%20%20%20%20None%20%3D%3E%20Err(String%3A%3Afrom(%22email%20no%20definido%22))%0A%20%20%20%20%7D%0A%7D%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20mut%20u%20%3D%20User%7B%20username%3A%20%22danigm%22%2C%20email%3A%20None%20%7D%3B%0A%0A%20%20%20%20let%20ret%20%3D%20transform_email(%26u)%3B%0A%20%20%20%20match%20ret%20%7B%0A%20%20%20%20%20%20%20%20Ok(email)%20%3D%3E%20println!(%22Este%20es%20el%20nuevo%20email%3A%20%7B%7D%22%2C%20email)%2C%0A%20%20%20%20%20%20%20%20Err(error)%20%3D%3E%20println!(%22Error%3A%20%7B%7D%22%2C%20error)%0A%20%20%20%20%7D%0A%0A%20%20%20%20u.email%20%3D%20Some(%22danigm%40wadobo.com%22)%3B%0A%20%20%20%20if%20let%20Ok(email)%20%3D%20transform_email(%26u)%20%7B%0A%20%20%20%20%20%20%20%20println!(%22Nuevo%20email%3A%20%7B%7D%22%2C%20email)%3B%0A%20%20%20%20%7D%0A%7D%0A&version=stable&backtrace=0
[22]: https://play.rust-lang.org/?code=use%20std%3A%3Aslice%3A%3AIter%3B%0A%0Astruct%20User%3C%27a%3E%20%7B%0A%20%20%20%20username%3A%20%26%27a%20str%2C%0A%20%20%20%20email%3A%20Option%3C%26%27a%20str%3E%2C%0A%7D%0A%0Afn%20transform_email(u%3A%20%26User)%20-%3E%20Result%3CString%2C%20String%3E%20%7B%0A%20%20%20%20match%20u.email%20%7B%0A%20%20%20%20%20%20%20%20Some(email)%20%3D%3E%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20let%20s%20%3D%20email.split(%27%40%27).nth(0).unwrap()%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20Ok(String%3A%3Afrom(s)%20%2B%20%22%40newdomain.com%22)%0A%20%20%20%20%20%20%20%20%7D%2C%0A%20%20%20%20%20%20%20%20None%20%3D%3E%20Err(String%3A%3Afrom(%22email%20no%20definido%22))%0A%20%20%20%20%7D%0A%7D%0A%0Afn%20transform_all_emails(users%3A%20Iter%3C%26User%3E)%20-%3E%20Result%3C()%2C%20String%3E%20%7B%0A%20%20%20%20for%20u%20in%20users%20%7B%0A%20%20%20%20%20%20%20%20let%20new%20%3D%20transform_email(u)%3F%3B%0A%20%20%20%20%20%20%20%20println!(%22%7B%7D%20new%20email%3A%20%7B%7D%22%2C%20u.username%2C%20new)%3B%0A%20%20%20%20%7D%0A%0A%20%20%20%20Ok(())%0A%7D%0A%0Afn%20main()%20%7B%0A%20%20%20%20let%20mut%20u%20%3D%20User%7B%20username%3A%20%22danigm%22%2C%20email%3A%20None%20%7D%3B%0A%20%20%20%20let%20u2%20%3D%20User%7B%20username%3A%20%22user2%22%2C%20email%3A%20Some(%22user2%40wadobo.com%22)%20%7D%3B%0A%0A%20%20%20%20if%20let%20Err(e)%20%3D%20transform_all_emails(vec!%5B%26u%2C%20%26u2%5D.iter())%20%7B%0A%20%20%20%20%20%20%20%20println!(%22Error%3A%20%7B%7D%22%2C%20e)%3B%0A%20%20%20%20%7D%0A%0A%20%20%20%20u.email%20%3D%20Some(%22danigm%40wadobo.com%22)%3B%0A%20%20%20%20if%20let%20Err(e)%20%3D%20transform_all_emails(vec!%5B%26u%2C%20%26u2%5D.iter())%20%7B%0A%20%20%20%20%20%20%20%20println!(%22Error%3A%20%7B%7D%22%2C%20e)%3B%0A%20%20%20%20%7D%0A%7D&version=stable&backtrace=0
