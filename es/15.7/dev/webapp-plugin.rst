==================================
Plugin de Aplicación Web
==================================

Visión General
==============

Con los plugins de aplicación web puede extender la interfaz web de Fess.
Es posible agregar nuevas páginas, personalizar la pantalla de administración, etc.

Estructura Básica
=================

::

    fess-webapp-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/app/web/example/
        │   └── ExampleAction.java
        └── webapp/WEB-INF/view/example/
            └── index.jsp

Implementación de Action
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

Extensión de API
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

Información de Referencia
=========================

- :doc:`plugin-architecture` - Arquitectura de plugins
- :doc:`overview` - Visión general de documentación para desarrolladores
