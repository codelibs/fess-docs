=================================
Ejecutar Fess con Docker y buscar
=================================

Introducción
============

Cuando se empieza a evaluar Fess, lo primero que se quiere saber es "¿qué búsquedas puedo hacer si lo ejecuto yo mismo?".
En este artículo iniciamos Fess 15.9 con Docker, rastreamos unas 20 páginas web y probamos la sintaxis de búsqueda, paso a paso.

Como ejemplo utilizamos la "Guía de búsqueda" en español del sitio oficial de Fess (un conjunto de páginas que explican la búsqueda AND, la búsqueda con comodines, etc.).
Como el objetivo se limita a un único lugar, el rastreo termina en pocos minutos y puede leer el contenido de los resultados para comprobarlos.

Si sigue los pasos de este artículo tal como están, podrá:

- Iniciar Fess y OpenSearch con Docker Compose, y detenerlos y reanudarlos
- Completar el primer inicio de sesión del administrador y el cambio de contraseña que se exige
- Crear una configuración de rastreo web, ejecutar el rastreo y comprobar que ha terminado
- Probar las búsquedas AND, OR, de exclusión, de frase y por campo

No se tratan los ajustes para entornos de producción (supervisión, copias de seguridad, SSO, escalado).
Desde "Artículos recomendados", al final, continúe con el artículo que se ajuste a su objetivo.

El entorno que se crea en este artículo
=======================================

Con los archivos Compose del repositorio docker-fess se inician los dos contenedores siguientes.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Servicio
     - Función
     - Dónde se guardan los datos
   * - ``fess01``
     - Fess (imagen ``ghcr.io/codelibs/fess:15.9.0``). Ofrece la página de búsqueda y la consola de administración en el puerto 8080
     - Sin volumen (dentro del contenedor)
   * - ``search01``
     - OpenSearch (imagen ``ghcr.io/codelibs/fess-opensearch``). También se publica el puerto 9200
     - Volúmenes ``search01_data`` y ``search01_dictionary``

El índice, las configuraciones de rastreo, los usuarios, los registros de trabajo, etc. se guardan todos en OpenSearch, por lo que se conservan en el volumen ``search01_data``.
En cambio, los ajustes modificados en [Sistema] > [General] de la consola de administración se guardan en ``system.properties`` dentro del contenedor ``fess01``.
Esta diferencia será importante más adelante, en "Detención y reanudación".

.. warning::

   En esta configuración, OpenSearch se ejecuta con el plugin de seguridad desactivado y se publica en el puerto 9200 del host.
   Úsela para hacer pruebas en su propio PC; si la ejecuta en un servidor compartido, consulte primero :doc:`guide-10` y :doc:`guide-15`.

Requisitos previos
==================

- Docker y Docker Compose (el comando ``docker compose``) están disponibles
- Docker dispone de al menos 4 GB de memoria (solo el heap de OpenSearch reserva 1 GB)
- Hay conexión a Internet (se usa para descargar las imágenes y para el rastreo)

En Linux o WSL2, aumente ``vm.max_map_count``, que OpenSearch necesita para iniciarse.

::

    $ sudo sysctl -w vm.max_map_count=262144

Este valor se restablece al reiniciar el sistema operativo.
Si va a seguir usando el entorno, escríbalo también en ``/etc/sysctl.conf``.

::

    $ echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf

Iniciar Fess
============

Obtener los archivos Compose para 15.9.0
----------------------------------------

Los archivos Compose de la rama predeterminada de docker-fess se actualizan con cada nueva versión.
Para fijar la versión en 15.9.0, obtenga los archivos de la etiqueta ``v15.9.0``.

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

``compose.yaml`` solo define ``fess01``; ``search01``, del que depende ``fess01``, está en ``compose-opensearch3.yaml``.
Por eso, en todos los comandos ``docker compose`` que siguen se indican siempre los dos archivos con ``-f``.
Si ejecuta un comando con solo uno de ellos, ni el inicio ni la detención funcionan correctamente.

Iniciar y esperar a que esté listo
----------------------------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

La primera vez tarda unos minutos, porque hay que descargar las imágenes.
Compruebe el estado con el siguiente comando.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

``fess01`` se inicia cuando ``search01`` pasa a healthy.
Fess está listo cuando el STATUS de ``fess01`` muestra ``(healthy)``.
La comprobación de estado de ``fess01`` llama a ``/api/v2/health``, y los primeros 120 segundos tras el inicio se tratan como periodo de gracia.

Si tarda mucho en pasar a healthy, revise los registros.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

Si otra aplicación usa el puerto 8080, cambie ``ports`` en ``compose.yaml``, por ejemplo a ``"9080:8080"``.
Para otros problemas de inicio, consulte la `solución de problemas de instalación <https://fess.codelibs.org/es/stable/install/troubleshooting.html>`__.

Al abrir ``http://localhost:8080/`` en el navegador, aparece la página de búsqueda de Fess.
Como todavía no se ha rastreado nada, en este momento las búsquedas no devuelven resultados.

Iniciar sesión en la consola de administración
==============================================

Abra ``http://localhost:8080/admin/`` e inicie sesión con el nombre de usuario ``admin`` y la contraseña ``admin``.

La contraseña inicial ``admin`` está configurada para que no se pueda seguir usando, así que al iniciar sesión pasará a una pantalla que indica "Debe actualizar su contraseña".

1. Escriba la misma contraseña en "Nueva contraseña" y "Confirmar nueva contraseña" (8 caracteres como mínimo)
2. Haga clic en [Actualizar]

Al terminar la actualización, se abre el tablero de la consola de administración.
A partir de ahora, inicie sesión con la nueva contraseña.
Esta contraseña se guarda en OpenSearch, por lo que se conserva aunque vuelva a crear los contenedores (si elimina también los volúmenes, vuelve a ser ``admin``).

Crear una configuración de rastreo
==================================

Decidir el objetivo
-------------------

En esta ocasión rastreamos la "Guía de búsqueda" en español del sitio oficial de Fess.
Son unas 20 páginas bajo ``https://fess.codelibs.org/es/stable/user/``; ``stable`` hace referencia a la documentación de la versión estable actual (15.9).

Registrar una configuración de rastreo web
------------------------------------------

1. En el menú izquierdo de la consola de administración, abra [Rastreador] > [Web]
2. Haga clic en [Crear nuevo]
3. Introduzca los siguientes campos. Deje el resto con sus valores predeterminados

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Campo
        - Valor
      * - Nombre
        - ``Guía de búsqueda de Fess``
      * - URLs
        - ``https://fess.codelibs.org/es/stable/user/index.html``
      * - URLs a incluir en el rastreo
        - ``https://fess.codelibs.org/es/stable/user/.*``
      * - Número máximo de accesos
        - ``50``

4. Haga clic en [Crear]

Cada campo significa lo siguiente.

- "Nombre" es obligatorio. Si está vacío, no se puede crear la configuración
- "URLs" es el punto de partida del rastreo
- "URLs a incluir en el rastreo" es una expresión regular; no se siguen los enlaces a URL que no coincidan con ella. Si lo deja vacío, el rastreador sigue los enlaces de las páginas hasta otras versiones, otros idiomas e incluso sitios externos
- "Número máximo de accesos" es un límite superior por si la expresión regular está mal escrita

De los campos que se dejan con su valor predeterminado, "Número de hilos" es ``1`` e "Intervalo" es ``10000`` milisegundos.
Como el rastreador espera 10 segundos por cada página, la carga sobre el sitio de destino se mantiene baja.
"Permisos" contiene ``{role}guest``, así que los usuarios que no han iniciado sesión también pueden ver los resultados de búsqueda.
Cómo mostrar resultados distintos según el departamento se trata en :doc:`guide-05`.

.. note::

   Si apunta a URL con número de versión, como ``/es/15.9/``, no se registra ni una sola página.
   Estas páginas contienen un ``<link rel="canonical">`` que apunta a ``/es/stable/``.
   El rastreador de Fess no registra una página así y, en su lugar, sigue la URL canónica.
   Esa URL queda fuera de la expresión regular de "URLs a incluir en el rastreo", por lo que no se registra nada.
   Si rastrea el sitio de su propia empresa, compruebe también que las URL canónicas quedan cubiertas por la expresión regular.

.. tip::

   Con [Sistema] > [Asistente] también puede crear una configuración de rastreo con solo introducir "Nombre", "Ruta de rastreo", "Número máximo de accesos" y "Profundidad", y pasar directamente a [Iniciar rastreo].
   Sin embargo, la configuración creada con el asistente no tiene "URLs a incluir en el rastreo", por lo que no puede limitar el alcance de los enlaces que se siguen.
   Si quiere limitar el objetivo como en este caso, cree la configuración desde [Rastreador] > [Web], como se ha descrito.

Ejecutar el rastreo y comprobar que ha terminado
================================================

Iniciar el rastreo
------------------

Guardar la configuración no inicia el rastreo.

1. Abra [Sistema] > [Programador]
2. Haga clic en "Default Crawler" en la lista
3. Haga clic en [Iniciar ahora]

"Default Crawler" es el trabajo que ejecuta juntas todas las configuraciones de rastreo web, de sistema de archivos y de almacén de datos habilitadas.
De forma predeterminada, este trabajo tiene la expresión cron ``0 0 * * *`` y también se ejecuta automáticamente una vez al día.
Si deja los contenedores en marcha, las mismas configuraciones se vuelven a rastrear los días siguientes.

Con esta configuración se obtienen unas 20 páginas a intervalos de 10 segundos, así que tardará unos minutos.

Comprobar que ha terminado
--------------------------

Compruébelo en el siguiente orden.

1. Abra [Información del sistema] > [Registro de trabajo]. Cuando el "Estado" de la fila "Default Crawler" cambia de "En ejecución" a "OK", el trabajo ha terminado. Si muestra "Fallo", haga clic en esa fila para abrir los detalles y revise el "Resultado"
2. Abra [Información del sistema] > [Información de rastreo] y haga clic en la sesión de más arriba (la más reciente) de la lista. "Tamaño del índice (Web/Archivo)" es el número de documentos registrados en este rastreo. En esta ocasión será de unos 20
3. Si el número es menor de lo esperado, abra [Información del sistema] > [URL de fallo]. Allí se registran las URL que no se pudieron obtener, por ejemplo por errores de conexión, junto con el motivo

Aunque el trabajo muestre "OK", el número de documentos registrados puede ser 0.
Las URL que no coinciden con la expresión regular de "URLs a incluir en el rastreo" se tratan como fuera del objetivo, no como errores, por lo que tampoco se registran en URL de fallo.
Si el número es 0 y URL de fallo también está vacío, revise cómo están escritas la URL y la expresión regular (``https`` o ``http``, si está el ``.*`` final, etc.).

Probar algunas búsquedas
========================

Abra ``http://localhost:8080/`` y busque.
La página de búsqueda usa ``bootstrap``, el tema incluido con Fess.

Primero, escriba ``comodines`` y busque.
En los resultados aparecen páginas como "Búsqueda con comodines" y "Caracteres especiales".
Al hacer clic en el título de un resultado, se abre la página original (fess.codelibs.org).

A continuación, introduzca uno tras otro los siguientes términos de búsqueda.
Puede comprobar los resultados de todos ellos con las páginas que acaba de rastrear.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Términos que se introducen
     - Significado
   * - ``campo URL``
     - Separar los términos con un espacio crea una búsqueda AND, y solo aparecen las páginas que contienen ambos
   * - ``comodines OR difusa``
     - Aparecen las páginas que contienen cualquiera de los dos. ``OR`` va en mayúsculas, con un espacio antes y después
   * - ``búsqueda -etiqueta``
     - Quita de los resultados las páginas que contienen "etiqueta". Ponga ``-`` justo delante del término que quiere excluir
   * - ``"búsqueda por rango"``
     - Busca páginas que contengan las palabras entre comillas exactamente en ese orden (búsqueda de frase)
   * - ``title:ordenamiento``
     - Busca solo las páginas cuyo título contiene "ordenamiento" (búsqueda por campo)

Si escribe ``or`` o ``and`` en minúsculas, no funcionan como operadores, sino que se tratan como términos de búsqueda normales.

La sintaxis usada aquí y el resto, como la búsqueda con comodines, la búsqueda difusa o la búsqueda por rango, se explican en la `Guía de búsqueda <https://fess.codelibs.org/es/stable/user/index.html>`__ que acaba de rastrear.
También puede buscar en su propio Fess una sintaxis que le interese y abrir y leer esa página.

Detención y reanudación
=======================

Lo que se conserva depende de cómo detenga los contenedores.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Operación
     - Qué se conserva
     - Qué se pierde
   * - ``stop`` → ``start``
     - Todo
     - Nada
   * - ``down`` → ``up -d``
     - Lo guardado en OpenSearch (índice, configuraciones de rastreo, usuarios y contraseñas, registros de trabajo, etc.)
     - Lo guardado dentro del contenedor ``fess01`` (ajustes modificados en [Sistema] > [General], etc.)
   * - ``down -v``
     - Nada
     - Todo (la contraseña del administrador también vuelve a ser ``admin``)

Para detener en el día a día, use ``stop``, y para reanudar, ``start``.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

``down`` elimina los contenedores.
Los datos de OpenSearch se conservan en los volúmenes, pero los ajustes de [General] están escritos en ``system.properties`` dentro del contenedor ``fess01``, por lo que desaparecen junto con el contenedor.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Cuando termine la prueba y quiera eliminarlo todo, incluidos los datos, añada ``-v``.
También se eliminan los volúmenes, y no se puede deshacer.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Algunos de los ajustes modificados en [General] se conservan aunque vuelva a crear los contenedores si los indica en ``FESS_JAVA_OPTS`` de ``compose.yaml`` (hay elementos, como los ajustes de conexión de SSO, que no se pueden indicar de esta manera).
Para el procedimiento, consulte `Instalación con Docker (Detalles) <https://fess.codelibs.org/es/stable/install/install-docker.html>`__.

Artículos recomendados
======================

Continúe con el artículo que se ajuste a su objetivo.

- Conocer la estructura de Fess y cómo recorrer los artículos: :doc:`guide-01`
- Colocar un cuadro de búsqueda en un sitio interno o portal existente: :doc:`guide-03`
- Buscar a la vez en los sitios web internos y en los servidores de archivos: :doc:`guide-04`
- Cambiar los resultados de búsqueda visibles según el departamento o el cargo: :doc:`guide-05`
- Buscar también datos de Slack, Confluence, bases de datos, etc.: primero :doc:`datastore-basics` y después :doc:`guide-06`, :doc:`guide-07` y :doc:`guide-12`
- Hacer que la IA generativa responda a partir de documentos internos: :doc:`guide-19`
- Encontrar documentos de significado similar aunque las palabras clave no coincidan: :doc:`guide-18`
- Preparar la supervisión y las copias de seguridad para la operación en producción: :doc:`guide-10`
- Configurar SSO y la protección de acceso: :doc:`guide-15`
- Escalar a medida que crecen los documentos y los usuarios: :doc:`guide-14`

Referencias
===========

- `Instalación con Docker (Detalles) <https://fess.codelibs.org/es/stable/install/install-docker.html>`__
- `docker-fess (GitHub) <https://github.com/codelibs/docker-fess>`__
- `Configuración del rastreo web <https://fess.codelibs.org/es/stable/admin/webconfig-guide.html>`__
- `Registro de trabajos <https://fess.codelibs.org/es/stable/admin/joblog-guide.html>`__
- `Guía de búsqueda <https://fess.codelibs.org/es/stable/user/index.html>`__
