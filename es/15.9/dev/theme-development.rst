===========================
Guía de Desarrollo de Temas
===========================

Visión General
==============

En |Fess| 15.9, la pantalla de búsqueda es siempre un tema estático.
Un tema estático es una SPA (Single Page Application, aplicación de
página única) independiente que utiliza la API ``/api/v2/*``. El tema
se distribuye como un archivo ZIP, que se sube y se activa desde la
consola de administración. Cuando no hay ningún tema seleccionado,
|Fess| utiliza ``bootstrap``, el tema estático incluido con él.

Para cambiar el aspecto de la pantalla de búsqueda, instale otro tema
(consulte :doc:`../admin/theme-guide`) o cree el suyo propio: la forma
más rápida es copiar el tema incluido y modificar la copia, como se
describe en `Personalización del Tema Incluido`_.

.. note::

   Los temas estáticos están disponibles a partir de |Fess| 15.7 y se
   convirtieron en la pantalla de búsqueda predeterminada en 15.9. Los
   plugins de tema JAR, que sustituyen las JSP de la pantalla de
   búsqueda, ya no modifican la pantalla de búsqueda en 15.9; consulte
   `Plugin de Tema JAR (heredado)`_.

Tema Estático
=============

Un tema estático es un conjunto de recursos estáticos que incluye el
manifiesto ``theme.yml`` y el archivo ``index.html``. El propio tema se
implementa como una aplicación frontend que invoca la API
``/api/v2/*`` de |Fess|.

Estructura
----------

Un tema estático tiene la siguiente estructura de directorios.

::

    example/
    ├── theme.yml          # Manifiesto (obligatorio)
    ├── index.html         # HTML de entrada de la SPA
    ├── assets/            # Recursos estáticos como JavaScript y CSS
    │   └── styles.css
    ├── i18n/              # Mensajes multilingües (messages.<locale>.json)
    │   └── messages.en.json
    ├── help/              # Definiciones de ayuda (<locale>.json)
    │   └── en.json
    └── thumbnail.png      # Imagen de vista previa (opcional)

Manifiesto (theme.yml)
----------------------

``theme.yml`` es el manifiesto obligatorio que debe colocarse en la raíz
del ZIP. A continuación se muestra un ejemplo de configuración mínima.

.. code-block:: yaml

    apiVersion: fess.codelibs.org/v1
    kind: StaticTheme
    name: example
    displayName: "Example Theme"
    version: "15.9.0"
    minFessVersion: "15.9"
    entry: index.html
    spaFallback: true

Los campos que se pueden especificar son los siguientes.

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - Campo
     - Obligatorio
     - Descripción
   * - ``apiVersion``
     - Obligatorio
     - Valor fijo ``fess.codelibs.org/v1``.
   * - ``kind``
     - Obligatorio
     - Valor fijo ``StaticTheme``.
   * - ``name``
     - Obligatorio
     - Nombre del tema. Debe coincidir con
       ``^[a-z0-9][a-z0-9_-]{0,63}$``. Se utiliza como nombre del
       directorio del tema que se expande bajo ``themes/`` (al subir el
       archivo, este se determina automáticamente a partir de
       ``name``) y como URL de distribución (``/themes/<name>/``).
   * - ``displayName``
     - Obligatorio
     - Nombre que se muestra en la consola de administración.
   * - ``version``
     - Obligatorio
     - Formato de versionado semántico (ejemplo: ``15.9.0``,
       ``15.9.1-beta.1``). Por convención, ``major.minor`` es la línea de |Fess| a la
       que está destinado el tema, de modo que la versión por sí sola responde para
       qué |Fess| es un tema.
   * - ``author``
     - Opcional
     - Nombre del autor.
   * - ``description``
     - Opcional
     - Descripción del tema.
   * - ``license``
     - Opcional
     - Licencia.
   * - ``homepage``
     - Opcional
     - URL de la página de inicio.
   * - ``minFessVersion``
     - Opcional
     - Versión mínima de |Fess| compatible con el tema. Manténgala igual al
       ``major.minor`` de ``version``. No existe ``maxFessVersion``: consulte
       `Publicación`_.
   * - ``supportedLocales``
     - Opcional
     - Lista de configuraciones regionales admitidas (ejemplo:
       ``[en, ja, de]``).
   * - ``entry``
     - Opcional
     - HTML de entrada de la SPA. El valor predeterminado es
       ``index.html``.
   * - ``spaFallback``
     - Opcional
     - Obsoleto. Se acepta por compatibilidad, pero ya no se lee: desde
       15.9 el HTML de entrada se sirve siempre para las rutas de la
       pantalla de búsqueda.

.. note::

   Al subir el archivo desde un ZIP, el nombre del directorio de
   destino de la expansión se determina automáticamente a partir de
   ``name``. Si coloca el tema manualmente en el directorio
   ``themes/``, haga que el nombre del directorio coincida con
   ``name``. Los temas que no coincidan se ignorarán al volver a
   escanear.

.. note::

   La miniatura de vista previa se coloca en la raíz del tema con el
   nombre fijo ``thumbnail.png`` (se muestra en la lista de temas de la
   consola de administración). Esta imagen no se reconoce mediante un
   campo del manifiesto, sino por el nombre del archivo. Se recomienda
   que el tamaño no supere 512 KB y que las dimensiones no superen
   512×512 píxeles.

Distribución y API
------------------

- Los temas estáticos se distribuyen bajo ``/themes/<name>/`` (donde
  ``<name>`` es el ``name`` de ``theme.yml``).
- Se devuelve el HTML de entrada (por defecto ``index.html``) en cada
  una de las rutas ``/``, ``/search``, ``/advance``, ``/help``,
  ``/error``, ``/profile``, ``/cache`` y ``/chat``, y el enrutamiento
  posterior lo gestiona la SPA. Desde 15.9 esto ocurre sea cual sea el
  valor de ``spaFallback``; el campo ya no se lee.
- Los errores también los muestra el tema: cuando una solicitud falla,
  el navegador recibe el HTML de entrada del tema en la URL solicitada,
  con el código de estado HTTP real.
- La consola de administración (``/admin/*``), ``/api/*``, la pantalla
  de inicio de sesión, etc., quedan fuera del alcance de los temas
  estáticos y son gestionados por el propio |Fess|.
- El HTML de entrada se sirve con un encabezado
  ``Content-Security-Policy`` que solo permite scripts, estilos,
  imágenes y conexiones procedentes del propio |Fess| (se permiten los
  estilos en línea, pero no los scripts en línea). Por lo tanto, las
  fuentes o los scripts de una CDN externa no se cargan; inclúyalos en
  el tema.
- La SPA del tema obtiene datos como los resultados de búsqueda y el
  chat a través de la API ``/api/v2/*``.

Empaquetado
-----------

Si utiliza ``scripts/package.sh`` del repositorio `fess-themes
<https://github.com/codelibs/fess-themes>`__, puede empaquetar el tema
en un ZIP para su distribución.

::

    ./scripts/package.sh example

Se genera ``dist/example-<version>.zip`` (donde ``<version>`` es el
``version`` de ``theme.yml``).

.. note::

   ``theme.yml`` debe colocarse en la raíz del ZIP. Si se coloca en un
   subdirectorio, no se reconocerá al subirlo.

Publicación
-----------

Los temas que desarrolla el proyecto |Fess| se publican en
https://maven.codelibs.org/release/org/codelibs/fess/themes/ , en
``<name>/<version>/<name>-<version>.zip`` con un ``.sha1`` al lado y un
``maven-metadata.xml`` por tema que lista las versiones publicadas.
``bin/fess-setup install theme <name>`` lee esos metadatos para elegir la versión construida para
el |Fess| en ejecución.

Versione un tema según la línea de |Fess| a la que está destinado y suba la versión siempre que
cambie lo que entrega el archivo. Una versión publicada no se sobrescribe nunca, así que un cambio
que conserve su versión sencillamente no se distribuye.

Por lo mismo no hay en el manifiesto ningún campo de límite superior. Como un archivo publicado no
cambia nunca, no podría añadirse más tarde un límite para un tema que deja de funcionar en un
|Fess| más nuevo. No publicar ese tema para la línea nueva dice lo mismo, en el momento en que se
sabe.

.. note::

   Enumere las versiones publicadas a partir de ``maven-metadata.xml`` y no de un listado de
   directorio. El índice de directorio se genera periódicamente, de modo que un tema recién
   publicado puede leerse por sus metadatos antes de aparecer en ningún listado.

Instalación y Activación
------------------------

1. Abra «Sistema» → «Tema» (``/admin/theme/``) en la consola de
   administración.
2. Suba el archivo ZIP creado. Un tema publicado también puede instalarse desde la
   línea de comandos con ``bin/fess-setup install theme <name>``; consulte
   :doc:`../install/fess-setup`.
3. En la página de la lista, seleccione el tema deseado en el menú
   desplegable «Tema predeterminado» y pulse el botón «Establecer» para
   activarlo.

El mecanismo de activación es el siguiente.

- Al pulsar el botón «Establecer», el nombre del tema seleccionado se
  guarda en la propiedad del sistema ``theme.default`` y se convierte
  en el tema predeterminado de todo el sistema.
- Si el nombre del tema coincide con la clave de un host virtual, el
  tema solo se aplica al acceder a ese host virtual. Esto permite
  cambiar de tema según el host virtual.
- Si actualiza directamente el directorio ``themes/`` en el disco,
  puede volver a escanearlo con «Recargar».

.. note::

   La subida del ZIP tiene límites como el tamaño del archivo, el
   tamaño total tras la expansión y el número de entradas, que se
   pueden ajustar mediante las propiedades ``theme.*`` de
   ``fess_config.properties`` (por ejemplo, ``theme.upload.max.size``
   tiene un valor predeterminado de 50MB y ``theme.directory.path``
   tiene un valor predeterminado de ``themes``). Durante la expansión
   se realizan comprobaciones para prevenir ataques de tipo ZIP Slip y
   zip bomb.

.. _theme-customize-bundled:

Personalización del Tema Incluido
---------------------------------

El tema incluido ``bootstrap`` se encuentra en ``app/themes/bootstrap/``
de la instalación de |Fess| (``/usr/share/fess/app/themes/bootstrap/``
en los paquetes RPM/DEB). No lo edite directamente: una actualización
lo reemplaza, y el nombre ``bootstrap`` está reservado para él, por lo
que no se puede eliminar ni reemplazar mediante una subida. En su
lugar, cópielo con otro nombre.

1. Copie el directorio, por ejemplo a ``mytheme``::

       $ cp -r app/themes/bootstrap /tmp/mytheme

2. En ``theme.yml``, cambie ``name`` a ``mytheme`` y cambie
   ``displayName``. ``name`` debe coincidir con el nombre del
   directorio.

3. En ``index.html``, sustituya cada ``themes/bootstrap/`` por
   ``themes/mytheme/``. El ``index.html`` incluido menciona su propio
   directorio en cuatro lugares: la hoja de estilos
   (``assets/styles.css``), los dos logotipos (``assets/logo-head.png``
   y ``assets/logo.png``) y el script (``assets/app.js``). Si se dejan
   sin cambiar, la copia sigue cargando los archivos de ``bootstrap`` y
   no se ve ninguno de sus cambios en el CSS, los logotipos o los
   mensajes. Los demás archivos se cargan de forma relativa a
   ``assets/app.js``, así que estos cuatro son los únicos que hay que
   cambiar.

   ::

       $ sed -i 's#themes/bootstrap/#themes/mytheme/#g' /tmp/mytheme/index.html

4. Realice sus cambios:

   - Colores y diseño: ``assets/styles.css``.
   - Logotipos: ``assets/logo-head.png`` (encabezado) y
     ``assets/logo.png`` (página inicial de búsqueda).
   - Textos, como el pie de página (``footer.copyright_org``): los
     archivos ``i18n/messages.<locale>.json``, uno por idioma.
   - Estructura de la página: ``index.html``.

5. Empaquete el directorio como un ZIP con ``theme.yml`` en su raíz y
   súbalo en «Sistema» → «Tema» de la consola de administración::

       $ cd /tmp/mytheme && zip -r ../mytheme.zip .

   Como alternativa, coloque el directorio en ``app/themes/`` y pulse
   «Recargar» en la misma página.

6. Seleccione ``mytheme`` como tema predeterminado en esa página.

.. note::

   Después de cada actualización de |Fess|, sustituya la copia por una
   nueva copia del tema incluido y vuelva a aplicar sus cambios, ya que
   el tema incluido sigue la API ``/api/v2/*`` de su versión de |Fess|.

Plugin de Tema JAR (heredado)
=============================

.. warning::

   Desde |Fess| 15.9, la pantalla de búsqueda se sirve siempre con un
   tema estático, por lo que un plugin de tema JAR ya no la modifica.
   De las JSP que proporciona un tema JAR, solo se siguen utilizando
   las de la pantalla de inicio de sesión (``/login/``). Traslade el
   diseño a un tema estático; consulte
   `Personalización del Tema Incluido`_.

El plugin de tema JAR es un plugin que sobrescribe los directorios
``view`` / ``css`` / ``js`` / ``images`` del propio |Fess| para cada
nombre de tema. Para conocer la estructura general de los plugins y el
método de compilación, consulte también :doc:`plugin-architecture`.

Estructura
----------

::

    fess-theme-example/
    ├── pom.xml
    └── src/main/resources/
        ├── view/      # Archivos JSP (search.jsp, index.jsp, header.jsp, etc.)
        ├── css/       # Archivos CSS (style.css, etc.)
        ├── js/        # Archivos JavaScript
        └── images/    # Archivos de imagen (logo.png, etc.)

.. note::

   Las vistas (plantillas) están en formato JSP. Solo se reconocen los
   cuatro directorios de nivel superior de recursos: ``view`` / ``css``
   / ``js`` / ``images``. El nombre del artefacto debe comenzar con
   ``fess-theme-``.

pom.xml
-------

El plugin se construye como un jar con ``fess-parent`` como POM padre.
Puesto que el tema se compone únicamente de recursos, normalmente no es
necesario declarar dependencias adicionales.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <artifactId>fess-theme-example</artifactId>
        <version>15.9.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.9.0</version>
            <relativePath />
        </parent>
    </project>

Personalización de CSS e Imágenes
----------------------------------

Las JSP están basadas en Bootstrap. Puede sobrescribir el CSS para
cambiar los colores y el diseño, o sustituir ``images/logo.png`` para
cambiar el logotipo. Desde 15.9 esto solo afecta a la pantalla de
inicio de sesión; la pantalla de búsqueda es un tema estático
(consulte `Personalización del Tema Incluido`_).

Compilación e Instalación
--------------------------

::

    mvn clean package

En el directorio ``target/`` se genera un archivo JAR (por ejemplo,
``fess-theme-example-15.9.0.jar``). Puede instalarlo desde «Sistema» →
«Plugin» en la consola de administración. Para más detalles sobre el
procedimiento de instalación, consulte :doc:`../admin/plugin-guide`.

Al instalarlo, cada directorio dentro del JAR se expande, para cada
nombre de tema, en las siguientes ubicaciones (el nombre del tema es
la parte del nombre del artefacto que resulta de eliminar
``fess-theme-``; en el ejemplo anterior, ``example``).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Directorio dentro del JAR
     - Destino de expansión
   * - ``view/``
     - ``WEB-INF/view/<theme>/``
   * - ``css/``
     - ``css/<theme>/``
   * - ``js/``
     - ``js/<theme>/``
   * - ``images/``
     - ``images/<theme>/``

Activación
----------

Los temas JAR se activan mediante la función de host virtual. Si la
clave del host virtual coincide con el nombre del tema, este se aplica
al acceder a ese host.

1. En la configuración de host virtual de «Sistema» → «General»,
   asocie la cabecera ``Host`` de la solicitud con el nombre del tema
   (la clave del host virtual), como en
   ``Host:localhost:8080=example``.
2. Si es necesario, configure el mismo nombre (``example``) también en
   el host virtual de la configuración web del rastreo, entre otros.

Para más detalles sobre cómo configurar el host virtual, consulte
:doc:`../admin/general-guide`.

Ejemplos de Temas Existentes
============================

- `fess-themes <https://github.com/codelibs/fess-themes>`__ -
  Colección de temas estáticos (incluye varios temas estáticos como
  ``codesearch`` y ``docsearch``)
- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__
  - Tema JAR
- `fess-theme-classic <https://github.com/codelibs/fess-theme-classic>`__
  - Tema JAR

Información de Referencia
=========================

- :doc:`plugin-architecture` - Arquitectura de plugins
- :doc:`../admin/plugin-guide` - Instalación de plugins
