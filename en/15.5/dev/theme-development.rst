==================================
Theme Development Guide
==================================

Overview
========

Using the |Fess| theme system, you can customize the design of the search screen.
Themes can be distributed as plugins, and you can switch between multiple themes.

Theme Structure
===============

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

Basic Theme Creation
====================

CSS Customization
-----------------

``css/style.css``:

.. code-block:: css

    /* Header customization */
    .navbar {
        background-color: #1a237e;
    }

    /* Search box style */
    .search-box {
        border-radius: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* Search result style */
    .search-result-item {
        border-left: 3px solid #1a237e;
        padding-left: 15px;
    }

Logo Change
-----------

1. Place custom logo at ``images/logo.png``
2. Reference logo in CSS:

.. code-block:: css

    .logo img {
        content: url("../images/logo.png");
        max-height: 40px;
    }

Template Customization
----------------------

Templates are in JSP format.

``templates/search.html`` (excerpt):

.. code-block:: html

    <div class="search-header">
        <h1>Custom Search Portal</h1>
        <p>Search internal documents</p>
    </div>

Theme Registration
==================

pom.xml
-------

.. code-block:: xml

    <groupId>org.codelibs.fess</groupId>
    <artifactId>fess-theme-example</artifactId>
    <version>15.5.0</version>
    <packaging>jar</packaging>

Configuration File
------------------

``src/main/resources/theme.properties``:

::

    theme.name=example
    theme.display.name=Example Theme
    theme.version=1.0.0

Installation
============

::

    ./bin/fess-plugin install fess-theme-example

Select theme from admin console:

1. Go to "System" -> "Design"
2. Select theme
3. Save and apply

Existing Theme Examples
=======================

- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__
- `fess-theme-minimal <https://github.com/codelibs/fess-theme-minimal>`__

Reference
=========

- :doc:`plugin-architecture` - Plugin Architecture
- :doc:`../admin/design-guide` - Design Settings Guide

