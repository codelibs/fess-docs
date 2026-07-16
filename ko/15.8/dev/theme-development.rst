==================================
테마 개발 가이드
==================================

개요
====

|Fess| 에서는 검색 화면의 디자인을 다음 2 가지 방법으로 커스터마이징할 수 있습니다.

정적 테마 (Static Theme)
    |Fess| 15.7 에서 도입된 방식입니다. 테마를 ZIP 파일로 배포하고,
    관리 화면에서 업로드하여 활성화합니다. 테마 본체는 ``/api/v2/*`` API 를
    이용하는 독립된 SPA(싱글 페이지 애플리케이션)이며, |Fess| 본체의
    JSP 에 의존하지 않습니다. 새로 테마를 만드는 경우에는 이 방법을 권장합니다.

JAR 테마 플러그인(레거시)
    ``view`` / ``css`` / ``js`` / ``images`` 를 덮어쓰는 기존 방식의 플러그인입니다.
    JAR 로 빌드하여 플러그인으로 설치합니다. 기존 JSP 기반의
    화면을 부분적으로 교체하고 싶은 경우에 사용합니다.

.. note::

   정적 테마는 |Fess| 15.7 이후 버전에서 사용할 수 있습니다. 15.6 이전 버전을
   대상으로 하는 경우에는 JAR 테마 플러그인을 사용하십시오. 검색 화면의
   JSP·CSS·이미지를 관리 화면에서 직접 편집하는 방법에 대해서는
   :doc:`../admin/design-guide` 를 참조하십시오.

정적 테마
==========

정적 테마는 ``theme.yml`` 매니페스트와 ``index.html`` 을 포함하는 정적 리소스의
집합입니다. 테마 본체는 |Fess| 의 ``/api/v2/*`` API 를 호출하는 프런트엔드
애플리케이션으로 구현합니다.

구조
----

정적 테마는 다음과 같은 디렉터리 구성을 가집니다.

::

    example/
    ├── theme.yml          # 매니페스트(필수)
    ├── index.html         # SPA 엔트리 HTML
    ├── assets/            # JavaScript·CSS 등 정적 리소스
    │   └── styles.css
    ├── i18n/              # 다국어 메시지(messages.<locale>.json)
    │   └── messages.en.json
    ├── help/              # 도움말 정의(<locale>.json)
    │   └── en.json
    └── thumbnail.png      # 미리보기 이미지(임의)

매니페스트 (theme.yml)
------------------------

``theme.yml`` 은 ZIP 의 루트에 배치하는 필수 매니페스트입니다. 다음은 최소 구성의
예입니다.

.. code-block:: yaml

    apiVersion: fess.codelibs.org/v1
    kind: StaticTheme
    name: example
    displayName: "Example Theme"
    version: "1.0.0"
    minFessVersion: "15.7"
    entry: index.html
    spaFallback: true

지정할 수 있는 필드는 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - 필드
     - 필수
     - 설명
   * - ``apiVersion``
     - 필수
     - 고정값 ``fess.codelibs.org/v1``.
   * - ``kind``
     - 필수
     - 고정값 ``StaticTheme``.
   * - ``name``
     - 필수
     - 테마 이름. ``^[a-z0-9][a-z0-9_-]{0,63}$`` 에 일치해야 합니다.
       ``themes/`` 아래에 전개되는 테마의 디렉터리 이름(업로드 시에는
       이 ``name`` 으로 자동으로 결정됩니다), 그리고 배포 URL
       (``/themes/<name>/``)에 사용됩니다.
   * - ``displayName``
     - 필수
     - 관리 화면에 표시되는 이름.
   * - ``version``
     - 필수
     - 시맨틱 버저닝 형식(예: ``1.0.0``, ``1.2.3-beta.1``).
   * - ``author``
     - 선택
     - 작성자 이름.
   * - ``description``
     - 선택
     - 테마 설명.
   * - ``license``
     - 선택
     - 라이선스.
   * - ``homepage``
     - 선택
     - 홈페이지 URL.
   * - ``minFessVersion``
     - 선택
     - 테마가 지원하는 |Fess| 의 최소 버전.
   * - ``supportedLocales``
     - 선택
     - 지원 로케일 목록(예: ``[en, ja, de]``).
   * - ``entry``
     - 선택
     - SPA 엔트리 HTML. 기본값은 ``index.html``.
   * - ``spaFallback``
     - 선택
     - SPA 폴백(fallback)의 활성화·비활성화 여부. 기본값은 ``true``.

.. note::

   ZIP 에서 업로드하는 경우, 전개될 디렉터리 이름은 ``name`` 으로 자동으로
   결정됩니다. ``themes/`` 디렉터리에 수동으로 테마를 배치하는 경우에는 디렉터리
   이름을 ``name`` 과 일치시켜 주십시오. 일치하지 않는 테마는 재스캔 시 무시됩니다.

.. note::

   미리보기용 썸네일은 테마의 루트에 ``thumbnail.png`` 라는 고정된 이름으로
   배치합니다(관리 화면의 테마 목록에 표시됩니다). 이 이미지는 매니페스트의
   필드가 아니라 파일 이름으로 인식됩니다. 크기는 512KB 이내·512×512
   픽셀 이내를 권장합니다.

배포와 API
----------

- 정적 테마는 ``/themes/<name>/`` 아래에서 배포됩니다(``<name>`` 은
  ``theme.yml`` 의 ``name``).
- ``spaFallback`` 이 활성화된 경우, ``/``, ``/search``, ``/help``, ``/error``,
  ``/profile``, ``/cache``, ``/chat`` 의 각 경로에서 엔트리 HTML(기본값은
  ``index.html``)이 반환되며, 이후의 라우팅은 SPA 가 담당합니다.
- 관리 화면(``/admin/*``), ``/api/*``, 로그인 화면 등은 정적 테마의 대상 외이며,
  |Fess| 본체가 처리합니다.
- 테마의 SPA 는 검색 결과나 채팅 등의 데이터를 ``/api/v2/*`` API 에서 가져옵니다.

패키징
--------------

`fess-themes <https://github.com/codelibs/fess-themes>`__ 리포지토리의
``scripts/package.sh`` 를 사용하면 테마를 배포용 ZIP 으로 묶을 수 있습니다.

::

    ./scripts/package.sh example

``dist/example-<version>.zip`` 이 생성됩니다(``<version>`` 은 ``theme.yml`` 의
``version``).

.. note::

   ``theme.yml`` 은 ZIP 의 루트에 배치해야 합니다. 하위 디렉터리에
   넣으면 업로드 시 인식되지 않습니다.

설치와 활성화
--------------------

1. 관리 화면에서 [시스템 > 테마](``/admin/theme/``)를 엽니다.
2. 작성한 ZIP 파일을 업로드합니다.
3. 목록 페이지의 「기본 테마」 드롭다운에서 대상 테마를 선택하고, 「설정」 버튼을
   눌러 활성화합니다.

활성화의 원리는 다음과 같습니다.

- 「설정」 버튼을 누르면 선택한 테마 이름이 시스템 프로퍼티 ``theme.default``
  에 저장되어 시스템 전체의 기본 테마가 됩니다.
- 테마 이름을 가상 호스트의 키와 일치시키면, 해당 가상 호스트에 접속했을 때만
  테마가 적용됩니다. 이를 통해 가상 호스트별로 테마를 전환할 수 있습니다.
- 디스크상의 ``themes/`` 디렉터리를 직접 갱신한 경우에는 「다시 로드」로
  재스캔할 수 있습니다.

.. note::

   ZIP 업로드에는 파일 크기·전개 후 총 크기·엔트리 수 등의 상한이 있으며,
   ``fess_config.properties`` 의 ``theme.*`` 프로퍼티로 조정할 수 있습니다
   (예: ``theme.upload.max.size`` 는 기본값 50MB, ``theme.directory.path`` 는
   기본값 ``themes``). 전개 시에는 ZIP Slip 이나 zip bomb 을 방지하기 위한
   검증이 이루어집니다.

JAR 테마 플러그인(레거시)
================================

JAR 테마 플러그인은 |Fess| 본체의 ``view`` / ``css`` / ``js`` / ``images``
디렉터리를 테마 이름별로 덮어쓰는 플러그인입니다. 플러그인의 일반적인 구조나
빌드 방법에 대해서는 :doc:`plugin-architecture` 도 참조하십시오.

구조
----

::

    fess-theme-example/
    ├── pom.xml
    └── src/main/resources/
        ├── view/      # JSP 파일(search.jsp, index.jsp, header.jsp 등)
        ├── css/       # CSS 파일(style.css 등)
        ├── js/        # JavaScript 파일
        └── images/    # 이미지 파일(logo.png 등)

.. note::

   뷰(템플릿)는 JSP 형식입니다. 리소스의 최상위 디렉터리는
   ``view`` / ``css`` / ``js`` / ``images`` 의 4 가지만 인식됩니다.
   아티팩트 이름은 ``fess-theme-`` 로 시작해야 합니다.

pom.xml
-------

플러그인은 ``fess-parent`` 를 부모 POM 으로 하는 jar 로 빌드합니다. 테마는
리소스만으로 구성되므로, 일반적으로 추가 의존 관계를 선언할 필요는 없습니다.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <artifactId>fess-theme-example</artifactId>
        <version>15.8.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.8.0</version>
            <relativePath />
        </parent>
    </project>

CSS·이미지 커스터마이징
-----------------------

검색 화면은 Bootstrap 기반의 JSP 로 구성되어 있습니다. CSS 를 덮어써서 배색이나
레이아웃을 변경하거나, ``images/logo.png`` 를 교체하여 로고를 변경할 수 있습니다.
대상이 되는 클래스 이름이나 마크업은 실제 JSP(``view/index.jsp`` /
``view/search.jsp`` 등)를 확인하십시오.

빌드와 설치
--------------------

::

    mvn clean package

``target/`` 디렉터리에 JAR 파일(예: ``fess-theme-example-15.8.0.jar``)이
생성됩니다. 관리 화면의 [시스템 > 플러그인]에서 설치할 수 있습니다.
설치 절차의 자세한 내용은 :doc:`../admin/plugin-guide` 를 참조하십시오.

설치하면 JAR 내의 각 디렉터리는 테마 이름별로 다음 위치에 전개됩니다
(테마 이름은 아티팩트 이름에서 ``fess-theme-`` 를 제외한 부분입니다. 위 예에서는
``example``).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - JAR 내 디렉터리
     - 전개 위치
   * - ``view/``
     - ``WEB-INF/view/<theme>/``
   * - ``css/``
     - ``css/<theme>/``
   * - ``js/``
     - ``js/<theme>/``
   * - ``images/``
     - ``images/<theme>/``

활성화
------

JAR 테마는 가상 호스트 기능을 사용하여 활성화합니다. 가상 호스트의 키를 테마
이름과 일치시키면, 해당 호스트로의 접속 시 테마가 적용됩니다.

1. [시스템 > 일반]의 가상 호스트 설정에서 ``Host:localhost:8080=example`` 과
   같이, 요청의 ``Host`` 헤더와 테마 이름(가상 호스트의 키)을 대응시킵니다.
2. 필요에 따라 크롤링의 웹 설정 등의 가상 호스트에도 같은 이름(``example``)을
   설정합니다.

가상 호스트 설정 방법의 자세한 내용은 :doc:`../admin/general-guide` 를 참조하십시오.

기존 테마 예시
==============

- `fess-themes <https://github.com/codelibs/fess-themes>`__ - 정적 테마 모음집
  (``codesearch``, ``docsearch`` 등 여러 정적 테마 수록)
- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__ - JAR 테마
- `fess-theme-classic <https://github.com/codelibs/fess-theme-classic>`__ - JAR 테마

참고 정보
========

- :doc:`plugin-architecture` - 플러그인 아키텍처
- :doc:`../admin/design-guide` - 페이지 디자인(JSP·CSS·이미지 직접 편집)
- :doc:`../admin/plugin-guide` - 플러그인 설치
