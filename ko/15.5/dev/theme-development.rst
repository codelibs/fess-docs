==================================
테마 개발 가이드
==================================

개요
====

|Fess|의 테마 시스템을 사용하여 검색 화면 디자인을 커스터마이즈할 수 있습니다.
테마는 플러그인으로 배포할 수 있으며, 여러 테마를 전환하여 사용할 수 있습니다.

테마 구조
==========

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

기본 테마 작성
==================

CSS 커스터마이즈
---------------

``css/style.css``:

.. code-block:: css

    /* 헤더 커스터마이즈 */
    .navbar {
        background-color: #1a237e;
    }

    /* 검색 박스 스타일 */
    .search-box {
        border-radius: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* 검색 결과 스타일 */
    .search-result-item {
        border-left: 3px solid #1a237e;
        padding-left: 15px;
    }

로고 변경
----------

1. 커스텀 로고를 ``images/logo.png``에 배치
2. CSS로 로고 참조:

.. code-block:: css

    .logo img {
        content: url("../images/logo.png");
        max-height: 40px;
    }

템플릿 커스터마이즈
--------------------------

템플릿은 JSP 형식입니다.

``templates/search.html`` (일부):

.. code-block:: html

    <div class="search-header">
        <h1>커스텀 검색 포털</h1>
        <p>사내 문서 검색</p>
    </div>

테마 등록
============

pom.xml
-------

.. code-block:: xml

    <groupId>org.codelibs.fess</groupId>
    <artifactId>fess-theme-example</artifactId>
    <version>15.5.0</version>
    <packaging>jar</packaging>

설정 파일
------------

``src/main/resources/theme.properties``:

::

    theme.name=example
    theme.display.name=Example Theme
    theme.version=1.0.0

설치
============

::

    ./bin/fess-plugin install fess-theme-example

관리 화면에서 테마 선택:

1. "시스템" -> "디자인"
2. 테마 선택
3. 저장하여 적용

기존 테마 예
==============

- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__
- `fess-theme-minimal <https://github.com/codelibs/fess-theme-minimal>`__

참고 정보
========

- :doc:`plugin-architecture` - 플러그인 아키텍처
- :doc:`../admin/design-guide` - 디자인 설정 가이드
