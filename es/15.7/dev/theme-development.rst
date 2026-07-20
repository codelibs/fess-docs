==================================
Guía de Desarrollo de Temas
==================================

Visión General
==============

Usando el sistema de temas de |Fess|, puede personalizar el diseño de la pantalla de búsqueda.
Los temas se pueden distribuir como plugins y puede alternar entre múltiples temas.

Estructura del Tema
===================

::

    fess-theme-example/
    ├── pom.xml
    └── src/main/resources/
        └── theme/example/
            ├── css/
            │   ├── style.css
            │   └── custom.css
            ├── js/
            │   └── custom.js
            ├── images/
            │   └── logo.png
            └── templates/
                └── search.html

Creación Básica de Temas
========================

Personalización de CSS
----------------------

``css/style.css``:

.. code-block:: css

    /* Personalizacion del encabezado */
    .navbar {
        background-color: #1a237e;
    }

    /* Estilo del cuadro de busqueda */
    .search-box {
        border-radius: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* Estilo de los resultados de busqueda */
    .search-result-item {
        border-left: 3px solid #1a237e;
        padding-left: 15px;
    }

Cambio de Logo
--------------

1. Coloque el logo personalizado en ``images/logo.png``
2. Haga referencia al logo en el CSS:

.. code-block:: css

    .logo img {
        content: url("../images/logo.png");
        max-height: 40px;
    }

Personalización de Plantillas
-----------------------------

Las plantillas están en formato JSP.

``templates/search.html`` (parcial):

.. code-block:: html

    <div class="search-header">
        <h1>Portal de Busqueda Personalizado</h1>
        <p>Buscar documentos internos</p>
    </div>

Registro del Tema
=================

pom.xml
-------

.. code-block:: xml

    <groupId>org.codelibs.fess</groupId>
    <artifactId>fess-theme-example</artifactId>
    <version>15.7.0</version>
    <packaging>jar</packaging>

Archivo de Configuración
------------------------

``src/main/resources/theme.properties``:

::

    theme.name=example
    theme.display.name=Example Theme
    theme.version=1.0.0

Instalación
===========

::

    ./bin/fess-plugin install fess-theme-example

Seleccione el tema desde la pantalla de administración:

1. "Sistema" -> "Diseño"
2. Seleccione el tema
3. Guarde y aplique

Ejemplos de Temas Existentes
============================

- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__
- `fess-theme-minimal <https://github.com/codelibs/fess-theme-minimal>`__

Información de Referencia
=========================

- :doc:`plugin-architecture` - Arquitectura de plugins
- :doc:`../admin/design-guide` - Guía de configuración de diseño
