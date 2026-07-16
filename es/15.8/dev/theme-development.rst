===========================
Guía de Desarrollo de Temas
===========================

Visión General
==============

En |Fess|, el diseño de la pantalla de búsqueda se puede personalizar
mediante los dos métodos siguientes.

Tema Estático (Static Theme)
    Es el mecanismo introducido en |Fess| 15.7. El tema se distribuye
    como un archivo ZIP, que se sube y se activa desde la consola de
    administración. El propio tema es una SPA (Single Page Application,
    aplicación de página única) independiente que utiliza la API
    ``/api/v2/*`` y no depende de las JSP del propio |Fess|. Se
    recomienda este método para crear temas nuevos.

Plugin de Tema JAR (heredado)
    Es el plugin de tipo tradicional que sobrescribe ``view`` / ``css``
    / ``js`` / ``images``. Se construye como JAR y se instala como
    plugin. Se utiliza cuando se desea sustituir parcialmente las
    pantallas basadas en JSP existentes.

.. note::

   Los temas estáticos están disponibles a partir de |Fess| 15.7. Si el
   objetivo son las versiones 15.6 o anteriores, utilice el plugin de
   tema JAR. Para el método de edición directa de las JSP, el CSS y las
   imágenes de la pantalla de búsqueda desde la consola de
   administración, consulte :doc:`../admin/design-guide`.

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
    version: "1.0.0"
    minFessVersion: "15.7"
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
     - Formato de versionado semántico (ejemplo: ``1.0.0``,
       ``1.2.3-beta.1``).
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
     - Versión mínima de |Fess| compatible con el tema.
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
     - Habilita o deshabilita el fallback de la SPA. El valor
       predeterminado es ``true``.

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
- Cuando ``spaFallback`` está habilitado, se devuelve el HTML de
  entrada (por defecto ``index.html``) en cada una de las rutas ``/``,
  ``/search``, ``/help``, ``/error``, ``/profile``, ``/cache`` y
  ``/chat``, y el enrutamiento posterior lo gestiona la SPA.
- La consola de administración (``/admin/*``), ``/api/*``, la pantalla
  de inicio de sesión, etc., quedan fuera del alcance de los temas
  estáticos y son gestionados por el propio |Fess|.
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

Instalación y Activación
------------------------

1. Abra «Sistema» → «Tema» (``/admin/theme/``) en la consola de
   administración.
2. Suba el archivo ZIP creado.
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

Plugin de Tema JAR (heredado)
=============================

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
        <version>15.8.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.8.0</version>
            <relativePath />
        </parent>
    </project>

Personalización de CSS e Imágenes
----------------------------------

La pantalla de búsqueda está compuesta por JSP basadas en Bootstrap.
Puede sobrescribir el CSS para cambiar los colores y el diseño, o
sustituir ``images/logo.png`` para cambiar el logotipo. Para conocer
los nombres de clase y el marcado correspondientes, consulte las JSP
reales (``view/index.jsp``, ``view/search.jsp``, etc.).

Compilación e Instalación
--------------------------

::

    mvn clean package

En el directorio ``target/`` se genera un archivo JAR (por ejemplo,
``fess-theme-example-15.8.0.jar``). Puede instalarlo desde «Sistema» →
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
- :doc:`../admin/design-guide` - Diseño de página (edición directa de
  JSP, CSS e imágenes)
- :doc:`../admin/plugin-guide` - Instalación de plugins
