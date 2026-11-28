=============================================
Buscar en sitios web y servidores de archivos
=============================================

Introducción
============

Los documentos internos suelen estar repartidos en varios lugares: el portal de la intranet, las carpetas compartidas de cada departamento, un directorio donde se archivan los documentos antiguos, etc.
Quien busca algo tiene que recordar primero dónde está y luego buscar por separado en cada lugar.

En este artículo usamos Fess 15.9 para rastrear los tres lugares siguientes, de modo que se puedan buscar desde un único cuadro de búsqueda.
En la página de búsqueda, haremos posible acotar los resultados mediante etiquetas, por ejemplo "solo el portal" o "solo la carpeta compartida".

- El portal de la intranet (un sitio web)
- Una carpeta compartida en un servidor de archivos Windows (SMB)
- Un directorio de archivo en el servidor (archivos locales)

Los pasos dan por hecho el entorno Docker iniciado en :doc:`guide-02` (``fess01`` y ``search01``).
El almacenamiento en la nube, como Google Drive, SharePoint y Box, se trata en :doc:`guide-07`.
Los aspectos que conviene revisar antes de implantar la búsqueda en servidores de archivos se resumen en :doc:`file-server-search`.

Lo que vamos a construir
========================

.. list-table::
   :header-rows: 1
   :widths: 18 40 14 28

   * - Destino
     - Ruta que se rastrea
     - Valor de la etiqueta
     - Ejecución del rastreo
   * - Portal de la intranet
     - ``https://portal.example.com/``
     - ``portal``
     - Todos los días a las 2:00
   * - Carpeta compartida
     - ``smb://fileserver.example.com/shared/``
     - ``shared``
     - Todos los días a las 3:00
   * - Archivo histórico
     - ``file:/data/archive/`` (``/srv/archive`` en el host)
     - ``archive``
     - Cada domingo a las 4:00

Los nombres de host y los directorios son ejemplos.
Sustitúyalos por los de su propio entorno.
Se da por hecho que dispone de una cuenta de servicio con acceso de lectura a la carpeta compartida (basta con solo lectura) y que el contenedor ``fess01`` puede conectarse al puerto SMB (445) del servidor de archivos.

Las etiquetas se asignan durante el rastreo, así que créelas antes que las configuraciones de rastreo.
Siga las secciones de este artículo en orden.

Hacer legible el directorio de archivo desde el contenedor
==========================================================

En el ``compose.yaml`` de docker-fess v15.9.0 no hay volúmenes definidos para ``fess01``.
Por eso, el directorio ``/srv/archive`` del host no es visible tal cual desde dentro del contenedor.
Añada ``volumes`` a ``fess01`` en ``compose.yaml`` y, además, añada una línea ``FESS_JAVA_OPTS`` en ``environment``.

.. code-block:: yaml

    services:
      fess01:
        image: ghcr.io/codelibs/fess:15.9.0
        container_name: fess01
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_DICTIONARY_PATH=${FESS_DICTIONARY_PATH:-/usr/share/opensearch/config/dictionary/}"
          - "FESS_JAVA_OPTS=-Duser.timezone=Asia/Tokyo -Dfess.system.day.for.cleanup=10"
        volumes:
          - /srv/archive:/data/archive:ro
        # ports y lo que sigue quedan como estaban

- ``/srv/archive:/data/archive:ro`` monta ``/srv/archive`` del host en ``/data/archive`` del contenedor en modo de solo lectura
- ``-Duser.timezone=Asia/Tokyo`` hace que las horas de ejecución de los trabajos que se configuran más adelante se interpreten en hora de Japón. Ni compose.yaml ni la imagen especifican una zona horaria, por lo que, sin esta opción, los trabajos se ejecutan a horas desplazadas respecto a la hora de Japón
- ``-Dfess.system.day.for.cleanup=10`` establece en 10 días el valor predeterminado del plazo de caducidad de los documentos (en días). El motivo se explica más adelante, en "Trabajos semanales y caducidad de los documentos"

Después del cambio, vuelva a crear los contenedores.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Como ``fess01`` se vuelve a crear, se pierden los ajustes que haya cambiado hasta ese momento en [Sistema] > [General] (consulte "Detención y reanudación" en :doc:`guide-02`).
Haga los cambios en [General] después de este paso.

Dentro del contenedor, Fess se ejecuta con el usuario ``fess`` (UID 1001).
Compruebe que este usuario puede ver la lista de archivos.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml exec -u fess fess01 ls /data/archive

Si obtiene ``Permission denied``, haga que todo lo que hay bajo ``/srv/archive`` en el host sea legible para el UID 1001 (por ejemplo, conceda permiso de lectura a otros usuarios y permiso de ejecución en los directorios).

Crear las etiquetas
===================

Una etiqueta se asigna cuando la URL de un documento coincide con una expresión regular.
Las pantallas de configuración de rastreo no tienen un campo para elegir etiqueta (está oculto de forma predeterminada), así que el alcance de cada etiqueta se indica en el campo "Rutas incluidas" de la propia etiqueta.

En [Rastreador] > [Etiqueta] > [Crear nuevo], cree las tres etiquetas siguientes.

.. list-table::
   :header-rows: 1
   :widths: 18 14 68

   * - Nombre
     - Valor
     - Rutas incluidas
   * - Portal
     - ``portal``
     - ``https://portal.example.com/.*``
   * - Carpeta compartida
     - ``shared``
     - ``smb://fileserver.example.com/shared/.*``
   * - Archivo histórico
     - ``archive``
     - ``file:/data/archive/.*``

- "Nombre" es el texto que se muestra en la página de búsqueda y admite caracteres no ASCII, como tildes, la ñ o el japonés
- "Valor" solo admite caracteres alfanuméricos y guiones bajos (los guiones y los caracteres no ASCII provocan un error de entrada)
- "Rutas incluidas" debe coincidir con la URL completa, así que no omita el ``.*`` final. Si lo deja vacío, la etiqueta no se asigna a ningún documento
- "Permisos" contiene ``{role}guest``. Así la etiqueta se muestra también a los usuarios que no han iniciado sesión; déjelo como está

Los documentos rastreados antes de crear las etiquetas no tienen etiqueta.
Si añade o cambia etiquetas más adelante, aplíquelas a los documentos existentes rastreando de nuevo o ejecutando "Label Updater" con [Iniciar ahora] en [Sistema] > [Programador].

Crear las configuraciones de rastreo
====================================

Portal de la intranet (rastreo web)
-----------------------------------

En [Rastreador] > [Web] > [Crear nuevo], introduzca los siguientes campos y haga clic en [Crear].

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Campo
     - Valor
   * - Nombre
     - ``Portal de la intranet``
   * - URLs
     - ``https://portal.example.com/``
   * - URLs a incluir en el rastreo
     - ``https://portal.example.com/.*``
   * - URLs a excluir del rastreo
     - Añadir ``https://portal.example.com/admin/.*`` debajo de las líneas que ya hay

"URLs a excluir del rastreo" trae de serie expresiones regulares que excluyen imágenes, CSS, etc.
No las borre; añada una línea.
"Número de hilos" vale ``1`` e "Intervalo" ``10000`` milisegundos de forma predeterminada, valores que mantienen baja la carga sobre el portal.

Carpeta compartida (SMB) y autenticación de archivos
----------------------------------------------------

Primero, cree la siguiente configuración en [Rastreador] > [Sistema de archivos] > [Crear nuevo].

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Campo
     - Valor
   * - Nombre
     - ``Carpeta compartida``
   * - Rutas
     - ``smb://fileserver.example.com/shared/``
   * - Rutas a incluir en el rastreo
     - ``smb://fileserver.example.com/shared/.*``
   * - Rutas a excluir del rastreo
     - ``.*\.tmp$``

En el rastreo de archivos, "Número de hilos" vale ``5`` e "Intervalo" ``1000`` milisegundos de forma predeterminada.

A continuación, vincule la cuenta de servicio a esta configuración.
La autenticación de archivos se crea seleccionando una configuración de rastreo de archivos.
Mientras no exista ninguna configuración de rastreo de archivos, la pantalla [Autenticación de archivos] no muestra [Crear nuevo].

En [Rastreador] > [Autenticación de archivos] > [Crear nuevo], introduzca los siguientes campos y haga clic en [Crear].

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Campo
     - Valor
   * - Nombre de host
     - ``fileserver.example.com`` (escrito igual que el nombre de host de la ruta)
   * - Puerto
     - Vacío
   * - Esquema
     - ``Samba``
   * - Nombre de usuario / Contraseña
     - Los de la cuenta de servicio
   * - Parámetros
     - Para una cuenta de dominio, indique el nombre de dominio, por ejemplo ``domain=EXAMPLE``
   * - Configuración de rastreo de archivos
     - ``Carpeta compartida``

"Nombre de host" debe coincidir literalmente con el nombre de host de la ruta.
Si escribió la ruta con una dirección IP, escriba también aquí la dirección IP.
Una autenticación con el "Puerto" vacío se usa para las rutas que no indican puerto, como ``smb://nombre-host/nombre-recurso/``.

.. note::

   De forma predeterminada, los archivos rastreados por SMB reciben roles derivados de los permisos de acceso (ACL) del archivo, que se añaden a los "Permisos" de la configuración de rastreo.
   Mientras el valor inicial ``{role}guest`` siga en "Permisos", cualquiera puede buscarlos, incluidos los usuarios que no han iniciado sesión.
   Para mostrar resultados distintos según los permisos de acceso, consulte :doc:`file-server-search` y :doc:`guide-05`.

Archivo histórico (archivos locales)
------------------------------------

En [Rastreador] > [Sistema de archivos] > [Crear nuevo], cree la siguiente configuración.
Indique la ruta tal como se ve dentro del contenedor.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Campo
     - Valor
   * - Nombre
     - ``Archivo histórico``
   * - Rutas
     - ``file:/data/archive/``
   * - Rutas a incluir en el rastreo
     - ``file:/data/archive/.*``
   * - Rutas a excluir del rastreo
     - ``.*\.(log|bak)$``

Los archivos locales se escriben con una sola barra tras ``file:``, como en ``file:/data/archive/``.
Las URL de los archivos que encuentra el rastreador tienen la forma ``file:/data/archive/2020/report.pdf``, y "Rutas a incluir en el rastreo" se compara con estas URL.
Si escribe ``file:///data/archive/.*``, no coincide con ningún archivo y no se indexa ni uno solo.

Crear un trabajo por configuración
==================================

El trabajo "Default Crawler" del programador ejecuta juntas todas las configuraciones de rastreo habilitadas, todos los días a las 0:00.
Para ejecutar cada destino a una hora distinta, cree un trabajo por cada configuración de rastreo.

1. En [Rastreador] > [Web], haga clic en "Portal de la intranet" y luego en [Crear nuevo trabajo] en la pantalla de detalles
2. Se abre la pantalla de creación del trabajo; "Nombre" contiene ``Web Crawler - Portal de la intranet`` y "Script", un contenido que rastrea solo esta configuración
3. "Programación" está vacía; introduzca una expresión cron y haga clic en [Crear]
4. Haga lo mismo con "Carpeta compartida" y "Archivo histórico" en [Rastreador] > [Sistema de archivos] (los nombres quedan como ``File Crawler - Carpeta compartida``)

.. list-table::
   :header-rows: 1
   :widths: 40 25 35

   * - Trabajo
     - Programación
     - Significado
   * - ``Web Crawler - Portal de la intranet``
     - ``0 2 * * *``
     - Todos los días a las 2:00
   * - ``File Crawler - Carpeta compartida``
     - ``0 3 * * *``
     - Todos los días a las 3:00
   * - ``File Crawler - Archivo histórico``
     - ``0 4 * * 0``
     - Cada domingo a las 4:00

Una expresión cron sigue el orden "minuto hora día mes día-de-la-semana", y el día de la semana ``0`` es el domingo.

Por último, evite que "Default Crawler" vuelva a rastrear las mismas configuraciones a las 0:00.
En [Sistema] > [Programador], haga clic en "Default Crawler", vacíe "Programación" con [Editar] y haga clic en [Actualizar].
Si deja marcado "Habilitado" en "Estado", podrá seguir ejecutándolo con [Iniciar ahora] cuando quiera rastrear todas las configuraciones a la vez (si lo deshabilita, [Iniciar ahora] deja de mostrarse).

Trabajos semanales y caducidad de los documentos
------------------------------------------------

Los documentos indexados por un rastreo reciben una fecha de caducidad y, cuando esta pasa, el trabajo "Doc Purger" (que se ejecuta cada minuto) los elimina del índice.
La fecha de caducidad es la hora de inicio del rastreo más el número de días de "Eliminar documentos anteriores" en [Sistema] > [General], cuyo valor inicial es ``3`` días.
Si el siguiente rastreo encuentra el mismo archivo, la fecha de caducidad se prolonga.

Con el valor inicial, los documentos del archivo histórico, que solo se rastrea los domingos, dejan de encontrarse el miércoles.
Por eso este número de días tiene que ser mayor que el intervalo de rastreo más largo (7 días).
En este artículo usamos ``10`` días, con margen para que los documentos no desaparezcan aunque un trabajo falle una vez.

- En el entorno Docker, el ``-Dfess.system.day.for.cleanup=10`` mencionado antes pasa a ser este valor inicial. Los valores de [General] se pierden al volver a crear ``fess01``, así que es más fiable escribirlo en compose.yaml
- En entornos que no son Docker, ponga "Eliminar documentos anteriores" a ``10`` en [General] y haga clic en [Actualizar]

Al aumentar este número de días, los archivos eliminados del servidor de archivos también permanecen en los resultados de búsqueda hasta ese número de días después del último rastreo que los encontró.

Ejecutar y comprobar los resultados
===================================

Ejecutar los trabajos
---------------------

Sin esperar al día siguiente, en [Sistema] > [Programador] haga clic en cada uno de los tres trabajos y, en cada uno, en [Iniciar ahora].

Comprobar que han terminado
---------------------------

1. En [Información del sistema] > [Registro de trabajo], espere a que el "Estado" de los tres trabajos pase de "En ejecución" a "OK". Si aparece "Fallo", haga clic en la fila y revise "Resultado"
2. En [Información del sistema] > [Información de rastreo], mire el "Tamaño del índice (Web/Archivo)" de cada sesión y compruebe que el número de documentos indexados se acerca a lo esperado
3. Si hay pocos, abra [Información del sistema] > [URL de fallo]. Ahí se registran las URL que no se pudieron obtener, junto con el tipo de error y el registro

Las causas más habituales son las siguientes.

- La carpeta compartida tiene 0 documentos y en URL de fallo figuran rutas del recurso compartido: revise el "Nombre de host" de la autenticación de archivos y cómo está escrita la ruta, la "Configuración de rastreo de archivos" seleccionada y la contraseña. Si el registro muestra errores de conexión, compruebe que el contenedor puede resolver el nombre del servidor de archivos y llegar al puerto 445
- El archivo histórico tiene 0 documentos y URL de fallo está vacío: compruebe que la ruta no está escrita con ``file:///`` y que "Rutas a incluir en el rastreo" tiene la misma forma que la ruta
- Se producen errores de lectura en el archivo histórico: compruebe con el comando ``exec -u fess`` mostrado antes que el contenedor puede leer los archivos

Filtrar por etiqueta
--------------------

En ``http://localhost:8080/``, busque una palabra que probablemente aparezca en los tres lugares.
Los resultados mezclan páginas del portal, documentos de Office de la carpeta compartida, PDF del archivo histórico, etc., ordenados por relevancia.

En la página de búsqueda de 15.9 (tema ``bootstrap``), el filtrado por etiqueta está en dos sitios.

- La lista "Etiqueta" que aparece junto a los resultados: muestra las etiquetas presentes en los resultados con su número, y al hacer clic en una se acotan los resultados a esa etiqueta
- El botón con forma de engranaje a la derecha del cuadro de búsqueda: abre "Opciones de búsqueda", donde se eligen una o más entradas de la lista "Etiquetas" y se hace clic en [Buscar]. Si elige varias, se incluyen los documentos que tengan cualquiera de ellas; si no elige ninguna, se busca en todo

Al filtrar, se añade a la URL un parámetro como ``fields.label=shared``.
Si "Etiqueta" no aparece junto a los resultados, o el filtrado devuelve 0 resultados, compruebe si rastreó antes de crear las etiquetas (ejecutar "Label Updater" lo soluciona).
Si la lista "Etiquetas" no aparece en "Opciones de búsqueda", compruebe que los "Permisos" de la etiqueta incluyen el rol de quien busca.

Enlaces de los resultados y mapeo de rutas
==========================================

Al hacer clic en un resultado de la carpeta compartida o del archivo histórico, Fess lee el archivo y lo devuelve al navegador.
Esto lo hace "Search File Proxy" de [General], que está habilitado de forma predeterminada.
Así se pueden abrir los archivos aunque el navegador no pueda abrir directamente las URL ``smb://`` o ``file:``.

Si los mismos archivos del archivo histórico también se publican en un servidor web interno (aquí ``https://archive.example.com/``) y quiere que se abran desde allí, convierta las URL con el mapeo de rutas.

En [Rastreador] > [Mapeo de rutas] > [Crear nuevo], introduzca los siguientes campos y haga clic en [Crear].

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Valor
   * - Expresión regular
     - ``^file:/data/archive/(.*)$``
   * - Reemplazo
     - ``https://archive.example.com/$1``
   * - Tipo de proceso
     - Visualización

En "Tipo de proceso" está seleccionado inicialmente "Rastreo", así que cámbielo siempre a "Visualización".

- Visualización: la URL del índice sigue siendo ``file:/data/archive/...``; solo cambia el destino al hacer clic en el enlace de un resultado. Surte efecto desde que se crea y no hace falta volver a rastrear
- Rastreo: reescribe la propia URL que se guarda en el índice. No surte efecto hasta volver a rastrear, y las "Rutas incluidas" de las etiquetas también deben ajustarse a las URL ``https://`` reescritas

Después de configurarlo, busque y haga clic en un resultado del archivo histórico para comprobar que se abre el servidor web ``https://archive.example.com/``.

Artículos recomendados
======================

- Mostrar resultados de búsqueda distintos según el departamento o el cargo: :doc:`guide-05`
- Revisar los requisitos de la búsqueda en servidores de archivos (formatos admitidos, herencia de permisos de acceso): :doc:`file-server-search`
- Buscar también archivos de Google Drive, SharePoint y Box: :doc:`guide-07`
- Mejorar la calidad de búsqueda a partir de los registros de búsqueda: :doc:`guide-08`
- Preparar la supervisión y las copias de seguridad para la operación en producción: :doc:`guide-10`

Referencias
===========

- `Rastreo de Sistema de Archivos (Búsqueda en Servidores de Archivos) <https://fess.codelibs.org/es/stable/admin/fileconfig-guide.html>`__
- `Autenticación de Archivos <https://fess.codelibs.org/es/stable/admin/fileauth-guide.html>`__
- `Etiquetas <https://fess.codelibs.org/es/stable/admin/labeltype-guide.html>`__
- `Programador de Tareas <https://fess.codelibs.org/es/stable/admin/scheduler-guide.html>`__
- `General <https://fess.codelibs.org/es/stable/admin/general-guide.html>`__
- `Mapeo de Rutas <https://fess.codelibs.org/es/stable/admin/pathmap-guide.html>`__
- `Instalación con Docker (Detalles) <https://fess.codelibs.org/es/stable/install/install-docker.html>`__
