==================================
웹앱 플러그인
==================================

개요
====

웹앱 플러그인으로 Fess의 웹 인터페이스를 확장할 수 있습니다.
새 페이지 추가, 관리 화면 커스터마이즈 등이 가능합니다.

기본 구조
========

::

    fess-webapp-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/app/web/example/
        │   └── ExampleAction.java
        └── webapp/WEB-INF/view/example/
            └── index.jsp

Action 구현
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

JSP 템플릿
===============

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

API 확장
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

참고 정보
========

- :doc:`plugin-architecture` - 플러그인 아키텍처
- :doc:`overview` - 개발자 문서 개요
