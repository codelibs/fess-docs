==========================================
Integrar la búsqueda en un sitio existente
==========================================

Introducción
============

Cuando se quiere añadir búsqueda a un portal de intranet o a un sitio de productos, no es realista pedir a los usuarios que recuerden la URL de Fess.
Lo que se espera es un cuadro de búsqueda en la cabecera de las páginas que abren siempre, y una página de resultados que parezca parte de ese sitio.

En este artículo, usamos Fess 15.9 para probar por orden los tres métodos siguientes, que se resuelven por completo en el lado del navegador.

- Colocar un formulario de búsqueda HTML en una página existente y mostrar los resultados en la página de búsqueda de Fess
- Usar Fess Site Search (FSS) para mostrar los resultados de búsqueda dentro de una página del sitio existente
- Cambiar el aspecto de la página de búsqueda de Fess (el tema) para que coincida con el sitio existente

Además, configuramos el "mapeo de rutas", que cambia el destino de los enlaces de los resultados de búsqueda por URL a las que los usuarios pueden acceder.

Cómo crear pantallas propias llamando a la API de búsqueda desde el servidor de un sistema empresarial se trata en :doc:`guide-11`.

Requisitos previos
==================

- Siguiendo los pasos de :doc:`guide-02`, Fess 15.9 se ejecuta con Docker Compose en ``http://localhost:8080/`` y ya se ha rastreado al menos un contenido
- Un archivo HTML local que haga las veces del sitio existente

Normalmente, un sitio existente está en un origen (la combinación de esquema, host y puerto) distinto del de Fess.
Para reproducir esa misma condición en este artículo, ejecute el siguiente comando en el directorio donde está el archivo HTML y ábralo en ``http://localhost:8000/``.

::

    $ python3 -m http.server 8000

Cómo elegir el método
=====================

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * - Método
     - Dónde se muestran los resultados de búsqueda
     - Qué se necesita en Fess
   * - Formulario de búsqueda
     - Se pasa a la página de búsqueda de Fess (``/search``) y se muestran allí
     - Nada
   * - Fess Site Search
     - Dentro de una página del sitio existente
     - El plugin ``fess-webapp-v1-api``
   * - Cambio de tema
     - La página de búsqueda de Fess (con otro aspecto)
     - Un ZIP de tema (o los ajustes de [General])

El formulario de búsqueda y el cambio de tema se pueden combinar.
Si quiere que la página a la que se llega desde el sitio existente tenga el mismo aspecto, configure ambos.

Enviar búsquedas desde un formulario a la página de búsqueda de Fess
====================================================================

Colocar el formulario
---------------------

Escriba el siguiente formulario en el lugar de la página existente donde quiera poner el cuadro de búsqueda.

.. code-block:: html

    <form method="get" action="http://localhost:8080/search">
      <input type="text" name="q" maxlength="1000" autocomplete="off">
      <button type="submit">Buscar</button>
    </form>

Los términos de búsqueda se envían a ``/search`` de Fess como parámetro ``q``, y los resultados se muestran en la página de búsqueda de Fess.
``maxlength`` coincide con el límite de longitud de los términos de búsqueda en Fess, ``query.max.length`` (valor predeterminado ``1000``).
En producción, cambie la URL de ``action`` por la URL de Fess a la que acceden los usuarios.

Si quiere que solo se busquen los documentos de una etiqueta concreta, envíe también el valor de la etiqueta como ``fields.label``.

.. code-block:: html

    <form method="get" action="http://localhost:8080/search">
      <input type="text" name="q" maxlength="1000" autocomplete="off">
      <input type="hidden" name="fields.label" value="intranet">
      <button type="submit">Buscar</button>
    </form>

``intranet`` es el valor de una etiqueta creada en [Rastreador] > [Etiqueta].
Si se envía un valor que no existe, se obtienen 0 resultados.
Para saber cómo crear etiquetas, consulte :doc:`guide-04`.

Comprobar
---------

1. Abra el archivo HTML desde ``http://localhost:8000/`` y busque una palabra que aparezca en un documento rastreado
2. Si el navegador pasa a ``http://localhost:8080/search?q=...`` y los resultados se muestran en la página de búsqueda de Fess, ha terminado

Si obtiene 0 resultados, busque la misma palabra en el cuadro de búsqueda de ``http://localhost:8080/`` y compare.
Si ahí también obtiene 0 resultados, el problema no está en el formulario, sino en el rastreo o en los permisos.

Sobre las sugerencias
---------------------

La página `Integración de Formulario de Búsqueda <https://fess.codelibs.org/es/stable/config/search-form-integration.html>`__ incluye un ejemplo que añade sugerencias al formulario.
Sin embargo, ``/js/suggestor.js`` y ``/js/jquery-3.7.1.min.js``, que carga ese ejemplo, no están incluidos en Fess 15.9, por lo que el ejemplo no funciona tal cual en 15.9.
La parte del formulario (enviar ``q`` a ``/search``) se puede usar tal cual.

Para mostrar sugerencias en el cuadro de búsqueda del sitio existente, use una de las siguientes opciones.

- Activar las sugerencias en Fess Site Search, que se describe en la siguiente sección
- Llamar a ``/api/v2/suggest-words`` desde su propio script (para el uso de la API, consulte :doc:`guide-11`)

Una vez en la página de búsqueda de Fess, el tema incluido en Fess muestra las sugerencias.

Mostrar los resultados dentro de la página con Fess Site Search
===============================================================

Fess Site Search (FSS) es un JavaScript que muestra un formulario de búsqueda y los resultados de búsqueda en una página del sitio existente.
Los usuarios pueden buscar sin salir del sitio existente.

Fess no distribuye el JavaScript de FSS.
Descargue el archivo generado con FSS JS Generator (https://fss-generator.codelibs.org/) y colóquelo en el servidor del sitio existente.

Instalar el plugin de la API v1
-------------------------------

FSS llama a ``/api/v1`` de Fess.
Fess 15.9 por sí mismo solo ofrece ``/api/v2``; ``/api/v1`` lo ofrece el plugin ``fess-webapp-v1-api``.
Este plugin no está incluido en la imagen de Docker.

Con Docker Compose, añada la siguiente línea en ``environment`` de ``fess01`` en ``compose.yaml``.

.. code-block:: yaml

    - "FESS_PLUGINS=fess-webapp-v1-api:15.9.0"

Si ya indica otros plugins, enumérelos en el mismo valor separados por espacios.
Después de guardar, ejecute ``up -d`` indicando los dos archivos de Compose.
``fess01`` se vuelve a crear y el plugin se instala al iniciarse.
Como el contenedor se vuelve a crear, los ajustes cambiados en [Sistema] > [General] se restablecen, igual que al hacer ``down`` (consulte la sección sobre la detención y la reanudación en :doc:`guide-02`).

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

También puede instalarlo desde [Sistema] > [Plugin] > [Instalar] en la consola de administración (después de la instalación hay que reiniciar Fess).
Sin embargo, en Docker el plugin se coloca dentro del contenedor, por lo que desaparece cuando el contenedor se vuelve a crear con ``down``.
Si lo indica en ``FESS_PLUGINS``, se vuelve a instalar cada vez que se crea el contenedor.

Cuando ``fess01`` esté healthy, compruebe que la API responde.

::

    $ curl 'http://localhost:8080/api/v1/documents?q=fess'

Si se devuelve un JSON que contiene ``"record_count"``, todo está listo.
Si se devuelve 404, el plugin no está instalado.
En ese caso, en ``fess.log`` aparece una sola vez un WARN que empieza por ``No plugin serves the legacy API``.
Si el plugin está instalado pero no se devuelve JSON, compruebe que "Respuesta JSON" no esté desactivada en [Sistema] > [General].
Si se desactiva "Respuesta JSON", dejan de responder no solo ``/api/v1``, sino también ``/api/v2``, y tampoco se puede usar la propia página de búsqueda de Fess.

Generar y colocar el JavaScript
-------------------------------

1. Abra https://fss-generator.codelibs.org/, indique en el generador los colores, las fuentes, etc. y haga clic en [Generate]
2. Descargue el archivo JavaScript con [Download JS]
3. Cambie el nombre del archivo a ``fess-ss.js`` y colóquelo en el mismo directorio que el archivo HTML

En la página que muestra los resultados de búsqueda (por ejemplo, ``result.html``), escriba el siguiente código.

.. code-block:: html

    <script src="fess-ss.js"></script>

    <div class="fess-site-search">
      <fess-search-form
        language="es"
        :enable-suggest="true"
        suggest-url="http://localhost:8080"
      ></fess-search-form>
      <fess-search-result
        fess-url="http://localhost:8080"
        language="es"
      ></fess-search-result>
    </div>

``fess-url`` es la URL de Fess que se usa para buscar y ``suggest-url``, la URL de Fess que se usa para las sugerencias.
En producción, indique una URL de Fess a la que se pueda acceder desde el navegador de los usuarios.

En la cabecera de las demás páginas, coloque solo el formulario de búsqueda.

.. code-block:: html

    <script src="fess-ss.js"></script>

    <div class="fess-site-search">
      <fess-search-form result-page="result.html"></fess-search-form>
    </div>

El formulario pone los términos de búsqueda en el parámetro ``fss.query`` y pasa a ``result.html``, y el FSS de ``result.html`` ejecuta la búsqueda.
Al enviar desde una página que no carga FSS, un formulario que pase a ``result.html?fss.query=términos`` funciona de la misma manera.

Para los demás atributos (número de resultados por página ``:page-size``, filtrado por etiqueta ``:enable-label``, abrir los enlaces en otra pestaña ``link-target="_blank"``, etc.), consulte el manual de FSS JS Generator.

Comprobar
---------

1. Abra ``http://localhost:8000/result.html`` y busque con el formulario de búsqueda
2. Si los resultados de búsqueda se muestran dentro de la página, ha terminado
3. Si no se muestran, revise la solicitud a ``/api/v1/documents`` en la pestaña Red de las herramientas de desarrollo del navegador. Si es 404, revise el plugin; si es un error de CORS, revise el siguiente apartado

Puntos a tener en cuenta
------------------------

Desde el punto de vista del navegador, llamar a la API de ``localhost:8080`` desde una página de ``localhost:8000`` es una comunicación entre orígenes (cross-origin).
De forma predeterminada, Fess usa ``api.cors.allow.origin=*`` y acepta llamadas desde cualquier origen.
Cómo limitar las llamadas al sitio existente se trata en :doc:`guide-11`.

Las búsquedas que FSS envía desde otro origen se tratan como búsquedas de un usuario que no ha iniciado sesión (invitado), aunque el usuario haya iniciado sesión en Fess.
Esto se debe a que FSS llama a la API sin cookies, y el valor predeterminado ``api.cors.allow.origin=*`` tampoco permite la comunicación entre orígenes con credenciales.
Por eso, en los resultados solo aparecen los documentos que tienen ``{role}guest`` en sus permisos.
Si quiere mostrar documentos distintos según el departamento, pida a los usuarios que inicien sesión en la página de búsqueda de Fess (consulte :doc:`guide-05`).

Cambiar el aspecto de la página de búsqueda de Fess
===================================================

En 15.9, la página de búsqueda se muestra mediante un "tema" que agrupa HTML, CSS y JavaScript.
La pantalla [Diseño de página] y la edición de JSP de versiones anteriores ya no existen.
Si no se configura nada, se usa el tema incluido ``bootstrap``.

Lo que se puede cambiar sin crear un ZIP
----------------------------------------

Lo que escriba en "Página superior de búsqueda", dentro de "Mostrar notificación" en [Sistema] > [General], se muestra en la página principal de búsqueda y en la página de resultados del tema incluido.
También puede escribir HTML, pero se eliminan elementos como ``<script>`` y ``<style>``.
Si solo quiere mostrar un aviso de una línea para los usuarios internos, no hace falta crear un tema.

Usar un tema publicado
----------------------

El proyecto Fess publica temas como ``docsearch``, pensado para la búsqueda de documentos.

1. Abra [Sistema] > [Tema]
2. En "Instalar tema", elija un tema en "Nombre" y haga clic en [Seleccionar]
3. En "Versión", elija la versión para 15.9 (``15.9.x``) y haga clic en [Instalar]
4. En "Tema predeterminado", encima de la lista, elija el tema instalado y haga clic en [Establecer]

Al volver a abrir ``http://localhost:8080/``, la página se muestra con el nuevo tema.
Si elige "(sin predeterminado)" y hace clic en [Establecer], se vuelve al tema incluido ``bootstrap``.

Duplicar el tema incluido y cambiar el logotipo y los colores
-------------------------------------------------------------

El tema incluido no se puede editar directamente, y tampoco se puede reemplazar subiendo un tema llamado ``bootstrap``.
Duplíquelo con otro nombre y modifique la copia.
Aquí usamos ``mytheme``.

1. Copie el tema incluido desde el contenedor

   ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml cp fess01:/usr/share/fess/app/themes/bootstrap ./mytheme

2. En ``mytheme/theme.yml``, cambie ``name`` a ``mytheme`` y ``displayName`` a, por ejemplo, ``My Theme``
3. Modifique los siguientes archivos

   - Colores y diseño: ``assets/styles.css``
   - Logotipo: ``assets/logo-head.png`` (cabecera) y ``assets/logo.png`` (página principal de búsqueda)
   - Nombre de la organización en el pie de página: ``footer.copyright_org`` de ``i18n/messages.es.json`` (para la interfaz en inglés, ``messages.en.json``)

4. Empaquete los archivos de modo que ``theme.yml`` quede en la raíz del ZIP

   ::

       $ cd mytheme && zip -r ../mytheme.zip . && cd ..

5. Suba ``mytheme.zip`` con [Subir] en [Sistema] > [Tema]
6. En "Tema predeterminado", elija ``mytheme`` y haga clic en [Establecer]

No modifique ``index.html``.
El ``index.html`` incluido hace referencia a los archivos del tema con la forma ``{{themePath}}/assets/...``.
Como Fess sustituye ``{{themePath}}`` por ``themes/mytheme`` al servir la página, basta con cambiar el nombre para que se carguen los archivos del tema duplicado.

Comprobar
---------

Vuelva a abrir ``http://localhost:8080/`` y compruebe que el logotipo y los colores han cambiado.
Si no han cambiado, compruebe en la pestaña Red de las herramientas de desarrollo si la hoja de estilos se carga desde ``/themes/mytheme/assets/styles.css``.
Si se carga desde ``/themes/bootstrap/``, el ajuste del tema predeterminado no se ha aplicado.

Precauciones con los temas
--------------------------

- La página de búsqueda lleva un encabezado ``Content-Security-Policy`` que limita el origen de los scripts, los estilos y las imágenes al propio Fess. Las fuentes y los scripts de CDN externos no se cargan, así que inclúyalos en el ZIP del tema
- La página de búsqueda no se muestra dentro de un ``iframe`` de otra página (porque el valor predeterminado de ``theme.index.frame.ancestors`` es ``'none'``). Para mostrar resultados de búsqueda dentro de un portal, use FSS
- ``fess01`` de Docker no tiene volúmenes. Los temas subidos se guardan dentro del contenedor y el ajuste del tema predeterminado se guarda en ``system.properties``, por lo que ambos desaparecen cuando el contenedor se vuelve a crear con ``down``. Normalmente use ``stop``/``start`` y, después de volver a crear el contenedor, repita la subida y el ajuste
- El tema incluido está hecho para la ``/api/v2`` de la misma versión de Fess. Después de actualizar Fess, vuelva a duplicar el nuevo tema incluido y aplique de nuevo sus cambios

Para la estructura de los temas y los elementos de ``theme.yml``, consulte la `Guía de Desarrollo de Temas <https://fess.codelibs.org/es/stable/dev/theme-development.html>`__.

Hacer que los enlaces de los resultados apunten a URL para los usuarios
=======================================================================

A veces se quiere rastrear con un nombre de host interno y que los usuarios abran los documentos con la URL del portal.
Por ejemplo, se rastrea ``http://intranet-web01:8080/docs/`` y se quiere que los resultados de búsqueda abran ``https://portal.example.com/docs/``.
En ese caso, se usa el mapeo de rutas para sustituir la URL solo al mostrarla.

1. Abra [Rastreador] > [Mapeo de rutas] y haga clic en [Crear nuevo]
2. Introduzca lo siguiente y haga clic en [Crear]

   .. list-table::
      :header-rows: 1
      :widths: 25 75

      * - Campo
        - Valor
      * - Expresión regular
        - ``^http://intranet-web01:8080/docs/``
      * - Reemplazo
        - ``https://portal.example.com/docs/``
      * - Tipo de proceso
        - Visualización
      * - Orden de clasificación
        - ``0``

"Visualización" solo sustituye la URL que se muestra en los resultados de búsqueda y el destino del enlace.
La URL guardada en el índice no cambia, así que no hace falta volver a rastrear, y el cambio se refleja en los resultados de búsqueda desde el momento en que se guarda.
Si elige "Rastreo" o "Rastreo/Visualización", la URL sustituida se guarda en el índice.
Tenga en cuenta que, si elige una de estas opciones cuando solo quiere cambiar la visualización, también cambiarán las URL de los rastreos posteriores.

Para comprobarlo, busque una palabra que haga aparecer el documento en cuestión y compruebe que la URL y el destino del enlace en los resultados son ``https://portal.example.com/docs/...``.
Si recibe los resultados mediante la API, la URL sustituida está en ``url_link``, no en ``url`` (consulte :doc:`guide-11`).

Para un ejemplo que convierte las rutas de un servidor de archivos en URL de un servidor web, consulte `Mapeo de Rutas <https://fess.codelibs.org/es/stable/admin/pathmap-guide.html>`__.

Artículos siguientes
====================

- Llamar a la API de búsqueda desde el servidor de un sistema empresarial: :doc:`guide-11`
- Cambiar los documentos que muestra el portal según el departamento: :doc:`guide-05`
- Buscar a la vez en sitios web y servidores de archivos y separarlos con etiquetas: :doc:`guide-04`
- Mostrar un tema o unos destinos de búsqueda distintos a cada organización: :doc:`guide-13`
- Exigir el inicio de sesión para la página de búsqueda: :doc:`guide-15`

Referencias
===========

- `Integración de Formulario de Búsqueda <https://fess.codelibs.org/es/stable/config/search-form-integration.html>`__
- `Tema <https://fess.codelibs.org/es/stable/admin/theme-guide.html>`__
- `Guía de Desarrollo de Temas <https://fess.codelibs.org/es/stable/dev/theme-development.html>`__
- `Mapeo de Rutas <https://fess.codelibs.org/es/stable/admin/pathmap-guide.html>`__
- `Complemento <https://fess.codelibs.org/es/stable/admin/plugin-guide.html>`__
- `FSS JS Generator <https://fss-generator.codelibs.org/>`__
- `fess-site-search (GitHub) <https://github.com/codelibs/fess-site-search>`__
- `fess-webapp-v1-api (GitHub) <https://github.com/codelibs/fess-webapp-v1-api>`__
