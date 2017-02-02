Date: 2017-02-2
Title: Monkey Patching
Tags: wadobo, python, programming, monkey patching
Category: blog
Slug: monkey-patching
Gravatar: 8da96af78e0089d6d970bf3760b0e724

## Qué es el Monkey Patching

El [Monkey Patching][1] es una técnica de programación de los lenguajes
dinámicos que consiste en modificar el código en tiempo de ejecución.

Esto quiere decir que en lugar de modificar el código fuente de una clase,
por ejemplo, en tiempo de ejecución asignamos otra función a ese método y
todas las llamadas posteriores en lugar de ejecutar el código definido en
la clase ejecutarán el código "parcheado".

Esto está relacionado con el llamado [Duck typing][2], que viene a decir
que si nada como un pato y suena como un pato, esto es un pato. Y esto del
pato hace referencia a que los tipos no tienen que cumplir una interfaz
estricta, simplemente, si se comportan como tal, es el tipo esperado. Y con
el Monkey Patching podemos hacer que un perro haga cuak como un pato,
modificando el objeto perro en tiempo de ejecución.

<blockquote>
If it walks like a duck and talks like a duck, it’s a duck, right? So if
this duck is not giving you the noise that you want, you’ve got to just
punch that duck until it returns what you expect.
</blockquote>

*-- Patrick Ewing*

## Qué hay que tener en cuenta para el Monkey Patching

Para poder hacer Monkey Patching necesitamos, **tipado dinámico**, ya que si
un método espera un objeto tipo pato y le pasamos uno tipo perro, pero
"parcheado", el método no debe quejarse.

También tenemos que tener en cuenta la **vida útil** de los módulos y
objetos. Si parcheamos un módulo, es necesario conocer el alcance de esas
modificaciones, si sólo afectarán a mi módulo o si pueden afectar a otros
módulos que lo importen, o si parcheamos una instancia, es necesario
conocer hasta dónde llegarán esas modificaciones.

Y por supuesto también es necesario tener acceso a las partes del código
que se quieran modificar, si vamos a modificar un objeto con métodos
**privados**.

Por *suerte*, en Python no tenemos métodos privados realmente, se suele
usar el guión bajo (\_metodo), que según la herramienta lo oculta como
privado, pero en realidad en Python todo es accesible y por tanto podemos
parchear lo que queramos.

## Algunos ejemplos

### Veamos el ejemplo que viene en la wikipedia:

```python
>>> import math
>>> math.pi
3.141592653589793
>>> math.pi = 3
>>> math.pi
3
```

En este ejemplo se ve que se importa el módulo *math* y se modifica el valor
de *math.pi*. Fácil y sencillo. No tiene mucho sentido este cambio, pero si
lo hacemos en nuestro código, ya todo el código que venga después y use
*math.pi* recibirá como valor 3, y esto afecta incluso a librerías de
terceros.

### Algo más práctico con código Django:

```python
from django import shortcuts

old_render = shortcuts.render

def custom_render(*args, **kwargs):
    t1 = time.time()
    resp = old_render(*args, **kwargs)
    s = time.time() - t1
    print("Render time: %s seconds" % s)
    return resp

shortcuts.render = custom_render
```

En este ejemplo modificamos el comportamiento por defecto de la función
render de django. Reemplazamos esta función por otra que lo único que hace
es medir el tiempo que se tarda en la llamada a la función inicial y
sacarlo por pantalla.

### Otro ejemplo con Django:

```python
def password_logger(self, newp):
    send_to_hacker_email(self.username + ":" + newp)
    self.real_set_password(newp)

user = User.objects.get(username="admin")
user.real_set_password = user.set_password
user.set_password = password_logger
```

Aquí se muestra cómo se puede modificar una instancia. En este ejemplo se
modifica el método set\_password del usuario admin, para que cuando se
llame a este método se envíe la nueva contraseña por email a un presunto
hacker.

En el caso de los modelos de django no tiene mucho sentido modificar la
instancia, mejor sería modificar el modelo, la definición de la clase, pero
vale como ejemplo.

## Cuándo usar el Monkey Patching

El Monkey Patching es una herramienta muy poderosa, pero a la vez, es algo
tremendamente peligroso, ya que hace que una clase o un módulo no se
ejecuten como se espera, como dice su definición y por tanto puede dar más
de un dolor de cabeza.

<blockquote>
Un gran poder conlleva una gran responsabilidad
</blockquote>

*-- Ben Parker*

Por esto hay que saber cuándo usar el Monkey Patching y cuando no.

### Cuando SÍ:

 * **Depuración o ejecución paso a paso**: pdb, ipdb, mientras depuramos un
   código para que nos saque información por pantalla, etc.

 * **Testing**: Para reemplazar métodos, atributos o funciones en tiempo de
   ejecución en los tests, por ejemplo una función que genera números
   aleatorios la podemos transformar en algo predecible para testear otros
   métodos relacionados, o podemos reemplazar funciones que tarden mucho
   tiempo debido a sistemas externos, para que los tests se puedan ejecutar
   rápidamente.

 * **Fixs o arreglos de libs externas**: Para aplicar un parche o un
   arreglo de una biblioteca externa en una versión que aún no ha sido
   parcheada oficialmente.

### Cuando NO:

En la mayoría de las ocasiones, no es recomendable usar Monkey Patching.
Por lo tanto, si hay otra forma de hacer lo que queremos hacer, seguramente
sea mejor idea que el Monkey Patching.

Como he comentado antes, el Monkey Patching hace que el código que se
ejecuta sea diferente del descrito en la definición de la clase o módulo,
por tanto, hay que evitarlo y cuando se use hay que documentarlo muy bien,
porque si no, puede enmascarar problemas o hacer que futuras modificaciones
al código original no tengan efecto.

Resumiendo, el Monkey Patching está muy guay, pero úsalo bajo tu propia
responsabilidad.

[1]: https://en.wikipedia.org/wiki/Monkey_patch
[2]: https://es.wikipedia.org/wiki/Duck_typing
