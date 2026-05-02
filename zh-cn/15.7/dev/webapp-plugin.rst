==================================
Web应用插件
==================================

概述
====

Web应用插件可以扩展Fess的Web界面。
可以添加新页面、自定义管理界面等。

基本结构
========

::

    fess-webapp-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/app/web/example/
        │   └── ExampleAction.java
        └── webapp/WEB-INF/view/example/
            └── index.jsp

Action实现
==========

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

JSP模板
=======

``src/main/webapp/WEB-INF/view/example/index.jsp``:

.. code-block:: jsp

    <%@ page contentType="text/html; charset=UTF-8" %>
    <!DOCTYPE html>
    <html>
    <head>
        <title>Example Page</title>
    </head>
    <body>
        <h1>Custom Page</h1>
        <p>This is a custom page added by plugin.</p>
    </body>
    </html>

API扩展
=======

.. code-block:: java

    public class ApiExampleAction extends FessApiAction {

        @Execute
        public JsonResponse<ApiResult> get$data() {
            return asJson(new ApiResult.ApiResponse()
                .result(Map.of("message", "Hello from plugin"))
                .status(Status.OK));
        }
    }

参考信息
========

- :doc:`plugin-architecture` - 插件架构
- :doc:`overview` - 开发者文档概述

