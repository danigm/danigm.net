Date: 2012-11-27
Title: Nuevo blog, el ciclo de la web y otras cosas
Tags: pelican, web
Category: blog
Slug: nuevo-blog
Gravatar: 8da96af78e0089d6d970bf3760b0e724

Hacía ya bastante tiempo que venía queriendo cambiar mi
[antiguo blog][1], tenía un [drupal][3]. La decisión de poner un drupal como
blog fue algo que tomé así a la ligera, lo mismo que puse un drupal
podría haber puesto un wordpress[4]. La cosa es que cuando monté mi blog
en mi servidor personal era cuando se pusieron de moda los CMS estos y
yo opté por drupal.


### Problemas con drupal

Drupal está muy bien, pero para un blog es algo así como matar moscas
a cañonazos. No es que yo tenga problemas de rendimiento o algo así en
mi blog, pero tener una base de datos, y todo el tema de php ahí
montado a día de hoy es una exageración para tener un simple blog.

Estos son los principales problemas con los que me he encontrado a la
hora de usar drupal como sistema de blog:

* Urls limpias: Como servidor web estoy usando lighttpd [3] y no es
fácil hacer que un drupal te muestre urls sin parámetros por get con
este servidor.

* Actualizaciones: Las actualizaciones de drupal no es que sean
complicadas de llevar a cabo, pero hay muchas cosas que hay que hacer
manualmente y que me molesta tener que hacer, no por falta de tiempo,
sino por pereza.

* Comentarios: Últimamente me estaba empezando a entrar un montón de
spam diario en el blog a través de los comentarios, y eso que tenía
activado el módulo de recaptcha. Llegó hasta tal punto que decidí
desactivar los comentarios anónimos en mi blog.

* Tema: Durante el tiempo que he tenido el blog en drupal he cambiado
un par de veces de tema. Sin embargo, como soy así un poco especialito,
no me gusta poner un tema así tal cual, sino que me gusta meterle mis
modificaciones y ponerlo un poquito más a mi gusto. Pues bien, cambiar
un tema de drupal no es muy buena idea si no lo vas a mantener, porque
las actualizaciones suelen romper los temas.


### El ciclo de la web

Desde hace ya algún tiempo me he dado cuenta de que la web está
volviendo hacia atrás. Estamos volviendo un poco al pasado. Tras la
explosión de los blogs, cuando todo el mundo tenía uno, se hizo muy
famoso wordpress, drupal y este tipo de CMS, que tienen un montón de
funcionalidad, son modulares, extensibles, tienen sus temas y esas
cosas. Sin embargo, la mayoría de los blogs/páginas tienen un
contenido más bien estático y lo único realmente dinámico son los
comentarios.

Antes de la llegada del php y el código en servidor, la mayoría de las
páginas webs eran simples documentos html, que se actualizaban cuando
cambiaba el contenido. No había base de datos ni nada de eso. La web
era más estática, pero requería menos mantenimiento y recursos.

Hoy en día se está volviendo un poco a eso, en algunas partes. Muchas
webs están tendiendo a este tipo de soluciones por temas de
rendimiento y seguridad, servir documentos html sin código que se
ejecute en servidor es muchísimo más rápido y seguro que utilizar una
web php/python/cgi o lo que sea. Pero también se está volviendo a este
tipo de despliegues web porque es mucho más sencillo y lo anterior, en
muchos casos no tenía sentido.

Aún así, la vuelta atrás no implica perder funcionalidad ni facilidad.
No tiene sentido volver a escribir las webs en html, teniendo que
copiar o repetir partes de código como cabeceras, menus, etc. Ni
tampoco tiene sentido perder funcionalidad tan importante como son los
comentarios y la interacción de los visitantes.

La aparición de aplicaciones web que dan servicios son uno de los
factores que han facilitado esta vuelta atrás, por ejemplo
[disqus][5], que te proporciona comentarios en tu web de forma fácil,
y así te olvidas tanto de almacenarlos como del spam (en gran medida).

Por esto han nacido multitud de sistemas de publicación/generación web
offline, que hacen la función de CMS, facilitando al usuario o gestor
de contenidos la tarea de la publicación y encargándose de generar el
código html que irá en el servidor.

El funcionamiento de estos generadores de sitios web estáticos es
relativamente sencillo. Se basan en una serie de plantillas que
rellenan con los ficheros de contenido que se van encontrando. Los
ficheros de contenido suelen ser ficheros con un formato tipo
[Markdown][6] o algo así, para facilitar su escritura. Y buscando por
Internet se pueden encontrar [muchos diferentes][7].

### Salto a Pelican

De entre todos los diferentes sistemas de generación de contenido
estático que existen me decanté por [pelican][8]. Esta elección es
meramente técnica. Pelican está escrito en python, que es un lenguaje
que domino, y utiliza el sistema de plantillas [jinja][9], que es lo
que se usa en [django][10] y por lo tanto estoy familiarizado con él.

### Ventajas de Pelican

La principal ventaja de utilizar Pelican es que a partir de ahora me
puedo olvidar de tener que administrar el CMS, ni actualizaciones ni
nada. El blog en el servidor será html plano, por lo que si no quiero
actualizar a la última versión de Pelican no me arriesgo a que haya
problemas de seguridad explotables o cosas así.

Además de esto, el uso de Pelican trae consigo una serie de ventajas
que no podemos pasar por alto:

* Gestión del blog y cambios utilizando git[11], esto hace que para mí
como desarrollador y usuario diario de git sea mucho más fácil
controlar los cambios que vaya haciendo en el blog, tanto de contenido
como de visualización. Además lo tengo alojado en [github][12], por lo
que tengo backup automágico.

* Escritura de entradas del blog con [vim][13]. Al escribir el
contenido desde mi máquina puedo utilizar mi editor de textos favorito
y además escribo los posts utilizando la sintaxis [Markdown][6] y
luego ya Pelican se encarga de transformar eso en html.

* Mayor control, al controlar la tecnología con la que está hecha la
herramienta de generación puedo modificar a mi gusto y tengo control
absoluto sobre mi blog.

* Comentarios externalizados, con lo que me olvido del tema del
spam... Al menos por ahora.

### Contras de este nuevo modelo

* Comentarios externalizados, de momento así será, pero no me gusta
que haya contenido por ahí desperdigado en servidores que no conozco y
que a saber qué hacen con los comentarios que la gente hace en mi
blog. Si fuera software libre me montaría mi propio servidor de
comentarios integrado, pero al fin y al cabo esto es más fácil y al
final la desidia es lo que tiene. Sin embargo esto me duele y tarde o
temprano lo cambiaré por otra cosa que sea software libre y que me
pueda instalar en mi propio servidor controlando así que ningún ente
externo esté haciendo cosas por ahí.

* No hay edición web. Esto sería un problema si quisiera poder
escribir en mi blog desde cualquier parte y con cualquier dispositivo.
Pero no es el caso, así que es un problema menor, y en un momento dado
sería solucionable metiendo una pequeña aplicación de gestión de
ficheros markdown.

### Conclusiones

Cambio mi blog por otra cosa. Esto es otra moda, como lo fue en su día
drupal y de igual manera me dejo influenciar por estas modas y cambio
mi blog a esta *nueva* tecnología. Esto me sirve para seguir
aprendiendo cosas nuevas y ya de paso le doy un poco de vidilla a
esto, que no se puede quedar parado.

Y así nos va :P

[1]: http://old.danigm.net
[2]: http://drupal.org
[3]: http://lighttpd.net
[4]: http://wordpress.org
[5]: http://disqus.com
[6]: http://en.wikipedia.org/wiki/Markdown
[7]: http://iwantmyname.com/blog/2011/02/list-static-website-generators.html
[8]: http://docs.getpelican.com/
[9]: http://jinja.pocoo.org/
[10]: http://djangoproject.com
[11]: http://git-scm.com/
[12]: https://github.com/danigm/danigm.net
[13]: http://www.vim.org/
