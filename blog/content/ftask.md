Date: 2013-01-13
Title: FTask, gestión de tareas con Flask y mongodb
Tags: wadobo, ftask, flask, mongodb, trello
Category: blog
Slug: ftask
Gravatar: 8da96af78e0089d6d970bf3760b0e724

### Simplificando la gestión de tareas ([Trello][1])

La gestión de tareas y las listas de cosas por hacer es un problema
general de la vida al que casi todo el mundo se ha tenido que
enfrentar alguna vez.

Se han desarrollado multitud de soluciones, agendas, bloc de notas,
folios, post-its... Incluso se han desarrollado completas teorías como
[GTD][7] con las que se han hartado de vender libros desarrollando la
fabulosa metodología de apuntar las cosas en una lista e ir tachando
una a una.

Con respecto al mundo de las aplicaciones informáticas, también ha
habido multitud de aproximaciones con más o menos éxito. El mayor
problema que nos encontramos en la mayoría de las aplicaciones
informáticas de gestión de tareas es que aunque en un principio pueden
ser simples normalmente se van complicando más y más hasta que hacen
multitud de cosas y en realidad el apuntar algo para hacerlo luego se
convierte en una tarea tediosa, por lo que mucha gente acaba acudiendo
a los bonitos post-its pegados en la pantalla.

Recientemente he conocido la fabulosa aplicación web [Trello][1], que
no es más que otra solución a este problema mundialmente conocido. El
enfoque que dan desde Trello a la gestión de tareas es bien sencillo,
implementa un modelo de tablones-listas-tareas en una aplicación web
con una interfaz realmente sencilla.

La aplicación es bien sencilla, tienes tablones, donde puedes definir
listas y cada lista tiene una serie de tareas. Las tareas se pueden
mover entre listas, y de primeras te proponen tres listas: To Do,
Doing, Done. Es muy simple empezar apuntando cosas en la lista To Do,
cuando estás haciendo algo coges y arrastras la tarea a la lista Doing
y una vez terminas la mueves a Done. Algo simple, sencillo y muy
similar a tener un montón de post-its pero en tu pantalla.

Otra gran genialidad de Trello es la edición colaborativa, varias
personas pueden estar trabajando en un mismo tablón y los cambios se
ven en tiempo real.

Por lo tanto Trello es una gran herramienta para gestión de tareas. Es
algo simple, que hace completamente su función y que permite trabajar
en equipo de una manera más o menos simple.

### Haciendolo libre

[Trello][1] está muy bien, peeero, no es libre, no puedo descargarme
el código, modificarlo y usarlo en el servidor de [mi empresa][2] para
gestionar mis tareas.

Estando así las cosas y siendo un poco talibán del software libre, qué
mejor que implementar un [clon libre][8] de esta fabulosa herramienta,
y si además durante el proceso aprendemos algunas tecnologías nuevas,
pues mejor.

Así pues, desde [wadobo labs][2], nos hemos puesto a desarrollar él
clon con una licencia libre AGPLv3.

<p class="img">
    <a href="/static/pictures/trello.png">
        <img src="/static/pictures/trello.png" />
    </a>
    Trello.com en funcionamiento
</p>

<p class="img">
    <a href="/static/pictures/ftask.png">
        <img src="/static/pictures/ftask.png" />
    </a>
    Ftask en funcionamiento
</p>

### Un nombre...

Todo proyecto merece un nombre, y la selección del nombre es uno de
los momentos cruciales en el desarrollo. En este caso, en un alarde de
originalidad y creatividad el nombre elegido ha sido [FTask][8],
porque elegí [Flask][3] como framework de desarrollo y se parece mucho
Flask a Task, así que combiné las dos palabras et voilá.

Vale, no es un buen nombre. No se me ocurrió uno mejor, siempre
podemos cambiarlo más adelante.


### Arquitectura

<p class="img">
    <a href="/static/pictures/ftask-arch.png">
        <img src="/static/pictures/ftask-arch.png" />
    </a>
    Arquitectura del proyecto FTask
</p>

Para el desarrollo de este proyecto quería separar la interfaz de la
aplicación.

Normalmente las aplicaciones web tienen una interfaz HTML ligada. Pero
últimamente estoy observando que el modelo de simplificar la interfaz
facilita el desarrollo y las pruebas de la aplicación. Por lo tanto
decidí separar la aplicación en una aplicación básica con una interfaz
JSON y una interfaz HTML con todo el acceso al backend a través de
AJAX.

Esta arquitectura permite una separación más clara entre aplicación e
interfaz y por tanto es mucho más difícil mezclar cosas. Además
facilita el desarrollo de futuras aplicaciones no web ya sea
integración con escritorio o aplicaciones para dispositivos móviles.


### Flask y Mongo

Como ya he dicho antes, he elegido [Flask][3] como framework para el
desarrollo de esta aplicación. Dado que mi lenguaje favorito de
programación es python[10], estaba claro que el framework de
desarrollo tenía que ser en este lenguaje.

El framework con el que más he trabajado es [django][11], y es un gran
framework, pero tiene muchas cosas que no uso y para este proyecto
quería usar un micro-framework, algo más pequeño y modular. Ya he
trabajado antes con [web.py][12] e incluso con [cherrypy][13], pero
desde hacía ya algún tiempo venía oyendo hablar de [Flask][3] y tenía
ganas de hacer algo con este framework, así que el motivo principal
por el que elegí este framework fue porque no lo conocía.

Con respecto al almacenamiento tenía muchas ganas de hacer algo con
una base de datos no relacional, algo NoSQL. Ya había cacharreado algo
con [Mongo][9], pero no había hecho nada serio. Así que decidí
utilizar esta base de datos NoSQL.


### Tiempo real y Backbone

Como todos los datos de la interfaz se obtienen a través de peticiones
AJAX de la API JSON de la aplicación decidí que lo mejor para
controlar todos estos datos y mantener sincronizada la interfaz era
usar [backbone][4].

Con [backbone][4] es relativamente sencillo tener "edición
colaborativa en tiempo real" en la aplicación, ya que usando
medianamente bien la biblioteca js se separa la representación de los
datos y simplemente haciendo polling a la API cada poco tiempo se
actualiza automáticamente la interfaz.

Esta parte de [backbone][4] en [Ftask][8] es muy mejorable, porque
actualmente se hace polling y es bastante costoso en tráfico, esas
peticiones se pueden optimizar para que sean lo mínimo necesario e
incluso se podría utilizar websocket para evitar el polling. Por
suerte [backbone][4] permite cambiar de polling al uso de websocket de
manera más o menos sencilla, por lo que esa tarea la he ido delegando
para el momento en el que haya que optimizar.


### Versión usable y colaboraciones

Actualmente hay una versión [usable en el servidor de wadobo][6], pero
hay muchas cosas y mejoras que se pueden ir añadiendo, desde copias
literales de funcionalidad de [trello][1] a nueva funcionalidad que a
cualquiera se le pueda ocurrir.

El desarrollo de este proyecto es totalmente abierto y estando el
código en [github][8] es muy fácil hacer un fork y empezar a hacer
cositas por ahí, como siempre, toda colaboración será bienvenida.


[1]: http://trello.com/
[2]: http://wadobo.com/
[3]: http://flask.pocoo.org/
[4]: http://backbonejs.org/
[5]: http://twitter.github.com/bootstrap/
[6]: http://ftask.wadobo.com/
[7]: http://en.wikipedia.org/wiki/Getting_Things_Done
[8]: https://github.com/wadobo/Ftask
[9]: http://www.mongodb.com/
[10]: http://python.org
[11]: http://djangoproject.com
[12]: http://webpy.org
[13]: http://www.cherrypy.org/
