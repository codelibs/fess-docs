==================================
Guia de Desarrollo de Temas
==================================

Vision General
==============

Usando el sistema de temas de |Fess|, puede personalizar el diseno de la pantalla de busqueda.
Los temas se pueden distribuir como plugins y puede alternar entre multiples temas.

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

Creacion Basica de Temas
========================

Personalizacion de CSS
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

Personalizacion de Plantillas
-----------------------------

Las plantillas estan en formato JSP.

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
    <version>15.5.0</version>
    <packaging>jar</packaging>

Archivo de Configuracion
------------------------

``src/main/resources/theme.properties``:

::

    theme.name=example
    theme.display.name=Example Theme
    theme.version=1.0.0

Instalacion
===========

::

    ./bin/fess-plugin install fess-theme-example

Seleccione el tema desde la pantalla de administracion:

1. "Sistema" -> "Diseno"
2. Seleccione el tema
3. Guarde y aplique

Ejemplos de Temas Existentes
============================

- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__
- `fess-theme-minimal <https://github.com/codelibs/fess-theme-minimal>`__

Informacion de Referencia
=========================

- :doc:`plugin-architecture` - Arquitectura de plugins
- :doc:`../admin/design-guide` - Guia de configuracion de diseno
