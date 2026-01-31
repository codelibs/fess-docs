==================================
Plugin WebApp
==================================

Vue d'ensemble
==============

Les plugins WebApp permettent d'etendre l'interface web de Fess.
Vous pouvez ajouter de nouvelles pages, personnaliser l'interface d'administration, etc.

Structure de base
=================

::

    fess-webapp-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/app/web/example/
        │   └── ExampleAction.java
        └── webapp/WEB-INF/view/example/
            └── index.jsp

Implementation de l'Action
==========================

.. code-block:: java

    package org.codelibs.fess.app.web.example;

    import org.codelibs.fess.app.web.base.FessSearchAction;
    import org.lastaflute.web.Execute;
    import org.lastaflute.web.response.HtmlResponse;

    public class ExampleAction extends FessSearchAction {

        @Execute
        public HtmlResponse index() {
            return asHtml(path_Example_IndexJsp);
        }
    }

Template JSP
============

``src/main/webapp/WEB-INF/view/example/index.jsp``:

.. code-block:: jsp

    <%@ page contentType="text/html; charset=UTF-8" %>
    <!DOCTYPE html>
    <html>
    <head>
        <title>Example Page</title>
    </head>
    <body>
        <h1>Page personnalisee</h1>
        <p>Ceci est une page personnalisee ajoutee par un plugin.</p>
    </body>
    </html>

Extension API
=============

.. code-block:: java

    public class ApiExampleAction extends FessApiAction {

        @Execute
        public JsonResponse<ApiResult> get$data() {
            return asJson(new ApiResult.ApiResponse()
                .result(Map.of("message", "Hello from plugin"))
                .status(Status.OK));
        }
    }

Informations complementaires
============================

- :doc:`plugin-architecture` - Architecture des plugins
- :doc:`overview` - Vue d'ensemble developpeur
