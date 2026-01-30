==================================
Guide de developpement de themes
==================================

Vue d'ensemble
==============

Le systeme de themes de |Fess| permet de personnaliser le design de l'ecran de recherche.
Les themes peuvent etre distribues sous forme de plugins et vous pouvez basculer entre plusieurs themes.

Structure d'un theme
====================

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

Creation d'un theme de base
===========================

Personnalisation CSS
--------------------

``css/style.css``:

.. code-block:: css

    /* Personnalisation de l'en-tete */
    .navbar {
        background-color: #1a237e;
    }

    /* Style de la zone de recherche */
    .search-box {
        border-radius: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* Style des resultats de recherche */
    .search-result-item {
        border-left: 3px solid #1a237e;
        padding-left: 15px;
    }

Changement du logo
------------------

1. Placer le logo personnalise dans ``images/logo.png``
2. Referencer le logo dans le CSS:

.. code-block:: css

    .logo img {
        content: url("../images/logo.png");
        max-height: 40px;
    }

Personnalisation des templates
------------------------------

Les templates sont au format JSP.

``templates/search.html`` (extrait):

.. code-block:: html

    <div class="search-header">
        <h1>Portail de recherche personnalise</h1>
        <p>Rechercher dans les documents internes</p>
    </div>

Enregistrement du theme
=======================

pom.xml
-------

.. code-block:: xml

    <groupId>org.codelibs.fess</groupId>
    <artifactId>fess-theme-example</artifactId>
    <version>15.5.0</version>
    <packaging>jar</packaging>

Fichier de configuration
------------------------

``src/main/resources/theme.properties``:

::

    theme.name=example
    theme.display.name=Example Theme
    theme.version=1.0.0

Installation
============

::

    ./bin/fess-plugin install fess-theme-example

Selection du theme depuis l'interface d'administration:

1. "Systeme" -> "Design"
2. Selectionner le theme
3. Sauvegarder et appliquer

Exemples de themes existants
============================

- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__
- `fess-theme-minimal <https://github.com/codelibs/fess-theme-minimal>`__

Informations complementaires
============================

- :doc:`plugin-architecture` - Architecture des plugins
- :doc:`../admin/design-guide` - Guide de configuration du design
