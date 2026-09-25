==================
Comando fess-setup
==================

``bin/fess-setup`` (``bin\fess-setup.bat`` en Windows) se incluye con el paquete ZIP de |Fess|.
Instala lo que |Fess| necesita pero no incluye: OpenSearch con los plugins que requiere |Fess|,
Node.js para el rastreador de Playwright, los plugins de |Fess| y los temas estáticos. También informa sobre el estado
de una instalación.

Ejecútelo desde el directorio de |Fess|. Sin argumentos, muestra la lista de comandos.

::

    $ cd /path/to/fess-15.9.0
    $ bin/fess-setup <command> [options]

Códigos de Salida
=================

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Código
     - Significado
   * - ``0``
     - El comando se completó correctamente.
   * - ``1``
     - El comando falló: por ejemplo, falló una descarga, la versión solicitada no existe,
       OpenSearch no publica ninguna versión para esta plataforma o ``check`` detectó un problema.
   * - ``2``
     - La línea de comandos es incorrecta: un comando desconocido o falta un argumento, como el
       nombre de un plugin.

Instalación de OpenSearch y Node.js
===================================

install opensearch
------------------

::

    $ bin/fess-setup install opensearch [--dest <dir>] [--version <version>] [--keep-bundled-plugins]

Descarga la versión de OpenSearch compatible con este |Fess| en ``opensearch/`` dentro del
directorio de |Fess|, instala los cuatro plugins que requiere |Fess| (``opensearch-analysis-fess``,
``opensearch-analysis-extension``, ``opensearch-minhash`` y ``opensearch-configsync``) y añade la
siguiente configuración a su ``config/opensearch.yml``:

- ``configsync.config_path``, con el directorio ``config/dictionary`` de ese OpenSearch como valor
- ``plugins.security.disabled: true``

Además, elimina los plugins incluidos ``opensearch-security-analytics`` y
``opensearch-performance-analyzer``, que |Fess| no utiliza; el OpenSearch de la imagen Docker
tampoco los incluye. Si la descarga no incluye alguno de ellos, se omite.

Una opción que ``opensearch.yml`` ya contiene no se vuelve a añadir, y
``plugins.security.disabled: true`` no se añade si el archivo contiene cualquier opción
``plugins.security.*``. Si el directorio de OpenSearch ya existe, se omite la descarga, de modo que
volver a ejecutar el comando sobre una instalación existente solo añade las opciones que faltan.

El comando muestra cada opción que ha añadido y, a continuación, indica si ``bin/fess.in.sh``
encuentra este OpenSearch por sí mismo. Lo encuentra cuando es el único OpenSearch con un
directorio ``config/dictionary`` dentro de ``opensearch/`` en el directorio de |Fess|: en ese caso
``bin/fess.in.sh`` (``bin\fess.in.bat`` en Windows) establece ``FESS_DICTIONARY_PATH`` en ese
directorio, y no hace falta configurar nada más para un OpenSearch en el mismo host. En caso
contrario, el comando muestra los valores de ``SEARCH_ENGINE_HTTP_URL`` y ``FESS_DICTIONARY_PATH``
que debe establecer, tal como se describe en :doc:`install-linux` o :doc:`install-windows`.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Opción
     - Descripción
   * - ``--dest <dir>``
     - El directorio en el que extraer OpenSearch, en lugar de ``opensearch/`` dentro del
       directorio de |Fess|. ``bin/fess.in.sh`` no busca OpenSearch fuera de ese directorio.
   * - ``--version <version>``
     - La versión de OpenSearch que se instala. Los plugins se instalan en la misma versión.
   * - ``--keep-bundled-plugins``
     - Conserva los plugins incluidos (``opensearch-security-analytics`` y ``opensearch-performance-analyzer``) en lugar de eliminarlos, y deja la descarga tal como se distribuye.

OpenSearch publica versiones oficiales solo para Linux y Windows. En otras plataformas, como macOS,
el comando termina con el código ``1`` antes de descargar nada y sugiere instalar OpenSearch con
Homebrew y añadir los plugins con ``install opensearch-plugins``, o bien utilizar Docker.

.. warning::

   Con ``plugins.security.disabled: true``, OpenSearch acepta peticiones sin autenticación.
   OpenSearch solo escucha en la dirección de loopback a menos que se establezca ``network.host``.
   Antes de que escuche en cualquier otra dirección, configure en su lugar el plugin de seguridad;
   consulte :doc:`security`.

install opensearch-plugins
--------------------------

::

    $ bin/fess-setup install opensearch-plugins --opensearch-home <dir> [--version <version>]

Instala los cuatro plugins que requiere |Fess| en un OpenSearch que ya tenga, en lugar de ejecutar
cuatro veces su ``bin/opensearch-plugin install``. ``--opensearch-home`` es el directorio de
instalación de OpenSearch y es obligatorio. ``--version`` establece la versión de los plugins, que
debe coincidir con la versión de OpenSearch.

Este comando no modifica ``opensearch.yml``. Añada usted mismo ``configsync.config_path`` y el
resto de la configuración, tal como se describe en :doc:`install-linux` o :doc:`install-windows`.

install nodejs
--------------

::

    $ bin/fess-setup install nodejs [--dest <dir>] [--version <version>]

Descarga Node.js, que necesita el rastreador de Playwright, en ``nodejs/`` dentro del directorio
de |Fess|. ``bin/fess.in.sh`` (``bin\fess.in.bat`` en Windows) lo encuentra allí y establece
``PLAYWRIGHT_NODEJS_PATH``. Con ``--dest`` fuera del directorio de |Fess|, el comando muestra en su
lugar la línea ``PLAYWRIGHT_NODEJS_PATH`` que debe añadir a ``bin/fess.in.sh``. ``--version``
selecciona otra versión de Node.js. Consulte :doc:`../config/crawler-advanced` para el rastreador de
Playwright.

Gestión de Plugins
==================

Estos comandos trabajan sobre el directorio de plugins ``app/WEB-INF/plugin`` de la instalación de
|Fess|. Reinicie |Fess| después de instalar, actualizar o eliminar plugins. Los plugins también se
pueden gestionar desde la página Sistema > Plugin de la pantalla de administración; consulte
:doc:`../admin/plugin-guide`.

``install plugin``, ``list plugins`` y ``upgrade plugins`` aceptan ``--repository <url>``. Con esta
opción, la lista de versiones, los jar y sus sumas de comprobación se obtienen de ese único
repositorio Maven, como un espejo interno, en lugar de los repositorios predeterminados de
versiones publicadas y de snapshots y de GitHub.

install plugin
--------------

::

    $ bin/fess-setup install plugin <name>[:<version>]... [--version <version>] [--repository <url>]

Instala uno o varios plugins de |Fess|, por ejemplo ``fess-script-groovy`` o ``fess-ds-git``. Un
nombre sin versión instala la versión más reciente compilada para este |Fess|.
``<name>:<version>`` fija la versión de ese plugin, y ``--version`` es la versión para todos los
nombres que no indican una propia. La versión instalada anteriormente de un plugin se elimina una
vez instalada la nueva.

Cada jar se obtiene de la release de GitHub del plugin, o del repositorio Maven cuando la release
no contiene ese archivo, y se verifica con la suma de comprobación SHA-1 que publica el repositorio
Maven. Una versión de desarrollo de |Fess| también instala las compilaciones snapshot de su propia
línea, y les da preferencia.

Consulte :doc:`../admin/plugin-guide` para ver ejemplos.

list plugins
------------

::

    $ bin/fess-setup list plugins [--repository <url>]

Lista los plugins publicados para este |Fess| y marca los instalados con
``(installed: <version>)``. Los plugins que están instalados pero no publicados en el repositorio,
como un jar compilado localmente, se listan por separado. Una versión de desarrollo de |Fess| lista
también el repositorio de snapshots.

list installed
--------------

::

    $ bin/fess-setup list installed

Lista los plugins instalados y sus versiones, sin consultar el repositorio.

upgrade plugins
---------------

::

    $ bin/fess-setup upgrade plugins [--repository <url>]

Vuelve a instalar cada plugin instalado en la versión adecuada para este |Fess|. Un plugin que ya
está en esa versión se deja como está. Los plugins de ``app/WEB-INF/plugin`` se compilan para una
versión concreta de |Fess|, así que ejecute este comando después de actualizar |Fess|.

remove plugin
-------------

::

    $ bin/fess-setup remove plugin <name>...

Elimina los jar instalados de los plugins indicados. Un nombre que no está instalado se notifica y
no cambia el código de salida.

Gestión de Temas
================

Estos comandos actúan sobre el directorio de temas ``app/themes`` de la instalación de |Fess|.
Reinicie |Fess| después de instalar o eliminar un tema, o pulse [Recargar] en la página
Sistema > Tema. Los temas también pueden subirse desde esa página; consulte
:doc:`../admin/theme-guide`.

La versión de un tema indica la línea de |Fess| a la que está destinado: ``15.9.0`` es un tema
para |Fess| 15.9. Por eso un nombre sin versión se resuelve al tema construido para este |Fess|,
igual que ocurre con un plugin.

install theme
-------------

::

    $ bin/fess-setup install theme <name>[:<version>]... [--version <version>] [--repository <url>]

Instala uno o varios temas estáticos, por ejemplo ``docuforge`` o ``voicebox``. Un nombre sin
versión instala la más reciente construida para este |Fess|. ``<name>:<version>`` fija la versión
de ese tema, y ``--version`` es la versión para todos los nombres que no lleven una propia.

El archivo se comprueba contra la suma SHA-1 que publica el repositorio Maven y se extrae en
``app/themes/<name>``. Un tema ya instalado con ese nombre se conserva como copia de seguridad
durante el mismo periodo que uno reemplazado desde la pantalla de administración (7 días por
omisión, ``theme.upload.attic.retention.days``).

La descarga, la extracción y la comprobación del manifiesto ocurren antes de tocar nada
instalado, de modo que un tema que ya esté ahí sobrevive a una instalación fallida. Se rechaza un
archivo cuyo ``theme.yml`` nombre un tema distinto.

list themes
-----------

::

    $ bin/fess-setup list themes [--repository <url>]

Lista los temas publicados para este |Fess| y marca los instalados con
``(installed: <version>)``. Los temas instalados que el repositorio no lista aparecen por
separado.

La lista se lee del índice de directorio del repositorio, que se genera periódicamente. Cuando no
puede leerse, el comando informa de la URL que intentó y sigue listando los temas instalados: un
tema puede instalarse nombrándolo, figure o no en el índice.

remove theme
------------

::

    $ bin/fess-setup remove theme <name>...

Elimina de ``app/themes`` los temas indicados y conserva cada uno como copia de seguridad durante
el periodo de retención. Un nombre que no esté instalado se informa y no cambia el código de
salida.

Si el tema eliminado era el predeterminado, |Fess| vuelve al tema ``bootstrap`` incluido hasta que
se elija otro.

Comprobación de una Instalación
===============================

list
----

::

    $ bin/fess-setup list

Muestra los componentes que descarga ``install``, ``opensearch`` y ``nodejs``, con la versión de
cada uno.

check
-----

::

    $ bin/fess-setup check [--url <engine url>] [--playwright]

Informa sobre la instalación, con una línea por comprobación, marcada como ``OK``, ``WARN`` o
``FAIL``:

- El motor de búsqueda: si es accesible, su versión (una advertencia si los nodos indican versiones
  distintas), si los cuatro plugins que requiere |Fess| están instalados en él y si ``configsync``
  responde.
- |Fess|: si el directorio de plugins existe y admite escritura, cada plugin instalado (un fallo
  para un plugin compilado para otra versión de |Fess| y para un plugin instalado en dos
  versiones) y si Node.js está instalado en ``nodejs/`` dentro del directorio de
  |Fess|.

La URL del motor es ``--url``; si no se indica, la variable de entorno ``SEARCH_ENGINE_HTTP_URL``;
y si tampoco existe, ``http://localhost:9200``. ``bin/fess-setup`` no lee ``bin/fess.in.sh``, así
que indique ``--url`` cuando OpenSearch esté en otro lugar. La ausencia de Node.js solo se
notifica, salvo que se indique ``--playwright``, que la convierte en un fallo.

El comando termina con el código ``0`` cuando ninguna comprobación ha fallado, aunque alguna haya
producido advertencias, y con el código ``1`` en caso contrario.
