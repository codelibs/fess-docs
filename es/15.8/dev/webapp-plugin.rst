==================================
Plugin de Aplicacion Web
==================================

Vision General
==============

Con los plugins de aplicacion web puede extender la interfaz web de Fess.
Es posible agregar nuevas paginas, personalizar la pantalla de administracion, etc.

Estructura Basica
=================

::

    fess-webapp-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/app/web/example/
        │   └── ExampleAction.java
        └── webapp/WEB-INF/view/example/
            └── index.jsp

Implementacion de Action
========================

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

Plantilla JSP
=============

``src/main/webapp/WEB-INF/view/example/index.jsp``:

.. code-block:: jsp

    <%@ page contentType="text/html; charset=UTF-8" %>
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pagina de Ejemplo</title>
    </head>
    <body>
        <h1>Pagina Personalizada</h1>
        <p>Esta es una pagina personalizada agregada por un plugin.</p>
    </body>
    </html>

Extension de API
================

.. code-block:: java

    public class ApiExampleAction extends FessApiAction {

        @Execute
        public JsonResponse<ApiResult> get$data() {
            return asJson(new ApiResult.ApiResponse()
                .result(Map.of("message", "Hello from plugin"))
                .status(Status.OK));
        }
    }

Informacion de Referencia
=========================

- :doc:`plugin-architecture` - Arquitectura de plugins
- :doc:`overview` - Vision general de documentacion para desarrolladores
