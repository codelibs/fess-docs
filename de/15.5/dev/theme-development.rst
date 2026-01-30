==================================
Theme-Entwicklungsanleitung
==================================

Übersicht
=========

Mit dem Theme-System von |Fess| konnen Sie das Design der Suchoberflache anpassen.
Themes konnen als Plugins verteilt werden, und Sie konnen zwischen mehreren Themes wechseln.

Theme-Struktur
==============

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

Grundlegendes Theme erstellen
=============================

CSS-Anpassung
-------------

``css/style.css``:

.. code-block:: css

    /* Header-Anpassung */
    .navbar {
        background-color: #1a237e;
    }

    /* Suchfeld-Stil */
    .search-box {
        border-radius: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* Suchergebnis-Stil */
    .search-result-item {
        border-left: 3px solid #1a237e;
        padding-left: 15px;
    }

Logo andern
-----------

1. Benutzerdefiniertes Logo in ``images/logo.png`` platzieren
2. Logo in CSS referenzieren:

.. code-block:: css

    .logo img {
        content: url("../images/logo.png");
        max-height: 40px;
    }

Template-Anpassung
------------------

Templates sind im JSP-Format.

``templates/search.html`` (Auszug):

.. code-block:: html

    <div class="search-header">
        <h1>Benutzerdefiniertes Suchportal</h1>
        <p>Interne Dokumente durchsuchen</p>
    </div>

Theme-Registrierung
===================

pom.xml
-------

.. code-block:: xml

    <groupId>org.codelibs.fess</groupId>
    <artifactId>fess-theme-example</artifactId>
    <version>15.5.0</version>
    <packaging>jar</packaging>

Konfigurationsdatei
-------------------

``src/main/resources/theme.properties``:

::

    theme.name=example
    theme.display.name=Example Theme
    theme.version=1.0.0

Installation
============

::

    ./bin/fess-plugin install fess-theme-example

Theme in der Administrationsoberflache auswahlen:

1. "System" -> "Design"
2. Theme auswahlen
3. Speichern und anwenden

Beispiel-Themes
===============

- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__
- `fess-theme-minimal <https://github.com/codelibs/fess-theme-minimal>`__

Referenzinformationen
=====================

- :doc:`plugin-architecture` - Plugin-Architektur
- :doc:`../admin/design-guide` - Design-Einstellungsanleitung
