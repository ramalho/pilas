Grupos
======

Ahora que podemos manejar a los actores de manera individual. Vamos
a ver organizarlos en grupos.

Organizar a los actores en grupo es muy útil, porque es
algo que hacemos todo el tiempo en el desarrollo de videojuegos. Por
ejemplo, en un juego de naves espaciales, podríamos hacer un
grupo de naves enemigas, o un grupo de estrellas, o un grupo
de disparos.

Creando grupos con la función fabricar
--------------------------------------

Para crear varios actores de una misma clase
podríamos ejecutar algo como lo que sigue:

.. code-block:: python

    bombas = pilas.atajos.fabricar(pilas.actor.Bomba, 30)


donde el primer argumento es la clase de la que buscamos crear
actores, y el segundo argumento es la cantidad de actores
que queremos.

Esto es lo que veríamos en la ventana de pilas:

.. image:: images/grupos_bombas.png


A partir de ahora, la referencia ``bombas`` nos servirá para
controlar a todas las bombas al mismo tiempo.

Veamos como alterar el atributo de posición horizontal:

.. code-block:: python

    bombas.x = 0

Y en la ventana obtendremos:

.. image:: images/grupos_bombas_x.png


Incluso, les podríamos enseñar a las bombas a reaccionar
como si fueran pelotas, es decir, que reboten e interactúen
con la aceleración gravitatoria:

.. code-block:: python

    bombas.aprender(pilas.habilidades.RebotaComoPelota)


.. image:: images/grupos_bombas_como_pelota.png


.. note::

    Un consejo, la gravedad del escenario se puede modificar
    usando una sentencia como la que sigue:

    .. code-block:: python

        pilas.atajos.definir_gravedad(200, 0)