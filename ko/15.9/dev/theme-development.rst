==================================
테마 개발 가이드
==================================

개요
====

|Fess| 15.9 에서는 검색 화면이 항상 정적 테마로 표시됩니다. 정적 테마는
``/api/v2/*`` API 를 이용하는 독립된 SPA(싱글 페이지 애플리케이션)입니다.
테마는 ZIP 파일로 배포하고, 관리 화면에서 업로드하여 활성화합니다. 테마를
선택하지 않은 경우에는 |Fess| 에 번들된 정적 테마 ``bootstrap`` 이 사용됩니다.

검색 화면의 외관을 변경하려면 다른 테마를 설치하거나
(:doc:`../admin/theme-guide` 참조) 직접 만듭니다. 가장 빠른 방법은 번들된
테마를 복사하여 그 복사본을 변경하는 것입니다. `번들 테마 커스터마이징`_ 을
참조하십시오.

.. note::

   정적 테마는 |Fess| 15.7 이후 버전에서 사용할 수 있으며, 15.9 에서 기본
   검색 화면이 되었습니다. 검색 화면의 JSP 를 교체하는 JAR 테마 플러그인으로는
   15.9 에서 더 이상 검색 화면을 변경할 수 없습니다.
   `JAR 테마 플러그인(레거시)`_ 을 참조하십시오.

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
    version: "15.9.0"
    minFessVersion: "15.9"
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
     - 시맨틱 버저닝 형식(예: ``15.9.0``, ``15.9.1-beta.1``). 관례로
       ``major.minor`` 는 테마가 대상으로 하는 |Fess| 계열에 맞춥니다. 그러면
       버전만으로 어느 |Fess| 용 테마인지 알 수 있습니다.
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
     - 테마가 지원하는 |Fess| 의 최소 버전. ``version`` 의 ``major.minor`` 와
       같은 값으로 둡니다. ``maxFessVersion`` 은 없습니다. `공개`_ 를 참조하십시오.
   * - ``supportedLocales``
     - 선택
     - 지원 로케일 목록(예: ``[en, ja, de]``).
   * - ``entry``
     - 선택
     - SPA 엔트리 HTML. 기본값은 ``index.html``.
   * - ``spaFallback``
     - 선택
     - 더 이상 사용되지 않음. 호환성을 위해 허용되지만 읽히지 않습니다.
       15.9 부터는 검색 화면의 각 경로에서 항상 엔트리 HTML 이 반환됩니다.

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
- ``/``, ``/search``, ``/advance``, ``/help``, ``/error``, ``/profile``,
  ``/cache``, ``/chat`` 의 각 경로에서 엔트리 HTML(기본값은
  ``index.html``)이 반환되며, 이후의 라우팅은 SPA 가 담당합니다.
  15.9 부터는 ``spaFallback`` 의 값과 관계없이 이렇게 동작하며, 이 필드는
  더 이상 읽히지 않습니다.
- 오류도 테마가 표시합니다. 요청이 실패하면 브라우저는 요청한 URL 에서
  실제 HTTP 상태와 함께 테마의 엔트리 HTML 을 받습니다.
- 관리 화면(``/admin/*``), ``/api/*``, 로그인 화면 등은 정적 테마의 대상 외이며,
  |Fess| 본체가 처리합니다.
- 엔트리 HTML 은 스크립트, 스타일, 이미지, 접속을 |Fess| 자신으로부터만
  허용하는 ``Content-Security-Policy`` 헤더와 함께 반환됩니다(인라인 스타일은
  허용되지만 인라인 스크립트는 허용되지 않습니다). 따라서 외부 CDN 의 폰트나
  스크립트는 로드되지 않으므로 테마에 포함하십시오.
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

공개
----

|Fess| 프로젝트가 개발하는 테마는 https://maven.codelibs.org/release/org/codelibs/fess/themes/ 아래에 공개됩니다. 배치는 ``<name>/<version>/<name>-<version>.zip`` 이고 그 옆에 ``.sha1`` 이, 테마마다 공개된 버전을 나열한 ``maven-metadata.xml`` 이 놓입니다. ``bin/fess-setup install theme <name>`` 은 이 메타데이터를 읽어 실행 중인 |Fess| 용으로 만들어진 버전을 고릅니다.

테마의 버전은 대상으로 하는 |Fess| 계열에 맞추고, 아카이브가 담는 내용을 바꿀 때마다 버전을 올리십시오. 공개된 버전이 덮어써지는 일은 없으므로 버전을 그대로 둔 변경은 배포되지 않습니다.

매니페스트에 상한 필드가 없는 것도 같은 이유입니다. 공개된 아카이브는 변경되지 않으므로 새로운 |Fess| 에서 동작하지 않게 된 테마에 나중에 상한을 추가할 수 없습니다. 그 계열용으로 공개하지 않음으로써 알게 된 시점에 같은 것을 나타낼 수 있습니다.

.. note::

   공개된 버전을 조사할 때는 디렉터리 목록이 아니라 ``maven-metadata.xml`` 을 사용하십시오. 디렉터리 색인은 주기적으로 생성되므로 새로 공개한 테마는 목록에 나타나기 전에 메타데이터에서 읽을 수 있습니다.

설치와 활성화
--------------------

1. 관리 화면에서 [시스템 > 테마](``/admin/theme/``)를 엽니다.
2. 작성한 ZIP 파일을 업로드합니다. 공개된 테마는 명령줄에서
   ``bin/fess-setup install theme <name>`` 으로 설치할 수도 있습니다.
   :doc:`../install/fess-setup` 를 참조하십시오.
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

.. _theme-customize-bundled:

번들 테마 커스터마이징
----------------------

번들 테마 ``bootstrap`` 은 |Fess| 설치 디렉터리의 ``app/themes/bootstrap/`` 에
있습니다(RPM/DEB 패키지의 경우 ``/usr/share/fess/app/themes/bootstrap/``).
그 자리에서 편집하지 마십시오. 업그레이드 시 교체되며, ``bootstrap`` 이라는
이름은 번들 테마용으로 예약되어 있어 삭제할 수도, 업로드로 교체할 수도
없습니다. 대신 다른 이름으로 복사하십시오.

1. 디렉터리를 복사합니다. 예를 들어 ``mytheme`` 으로 복사합니다::

       $ cp -r app/themes/bootstrap /tmp/mytheme

2. ``theme.yml`` 에서 ``name`` 을 ``mytheme`` 으로 변경하고 ``displayName`` 도
   변경합니다. ``name`` 은 디렉터리 이름과 일치해야 합니다.

3. ``index.html`` 에서 모든 ``themes/bootstrap/`` 을 ``themes/mytheme/`` 으로
   바꿉니다. 번들된 ``index.html`` 은 자신의 디렉터리를 네 곳에서 지정합니다.
   스타일시트(``assets/styles.css``), 두 개의 로고(``assets/logo-head.png`` 와
   ``assets/logo.png``), 스크립트(``assets/app.js``)입니다. 이를 그대로 두면
   복사본은 계속 ``bootstrap`` 의 파일을 로드하므로, CSS·로고·메시지에 대한
   변경이 하나도 반영되지 않습니다. 그 외의 파일은 ``assets/app.js`` 를 기준으로
   한 상대 경로로 로드되므로, 변경해야 하는 것은 이 네 곳뿐입니다.

   ::

       $ sed -i 's#themes/bootstrap/#themes/mytheme/#g' /tmp/mytheme/index.html

4. 원하는 대로 변경합니다.

   - 배색과 레이아웃: ``assets/styles.css``.
   - 로고: ``assets/logo-head.png`` (헤더)와 ``assets/logo.png``
     (검색 첫 페이지).
   - 푸터(``footer.copyright_org``) 등의 텍스트: 언어별로 하나씩 있는
     ``i18n/messages.<locale>.json`` 파일.
   - 페이지 구조: ``index.html``.

5. ``theme.yml`` 이 루트에 오도록 디렉터리를 ZIP 으로 묶어, 관리 화면의
   「시스템」 > 「테마」에서 업로드합니다::

       $ cd /tmp/mytheme && zip -r ../mytheme.zip .

   또는 디렉터리를 ``app/themes/`` 에 배치하고, 같은 페이지에서
   「다시 로드」를 클릭합니다.

6. 같은 페이지에서 ``mytheme`` 을 기본 테마로 선택합니다.

.. note::

   번들 테마는 해당 |Fess| 버전의 ``/api/v2/*`` API 에 맞춰져 있으므로,
   |Fess| 를 업그레이드할 때마다 번들 테마에서 새로 복사본을 만들어 변경 사항을
   다시 적용하십시오.

JAR 테마 플러그인(레거시)
================================

.. warning::

   |Fess| 15.9 부터 검색 화면은 항상 정적 테마로 제공되므로, JAR 테마 플러그인으로는
   더 이상 검색 화면을 변경할 수 없습니다. JAR 테마가 제공하는 JSP 중 여전히
   사용되는 것은 로그인 화면(``/login/``)의 JSP 뿐입니다. 디자인은 정적 테마로
   옮기십시오. `번들 테마 커스터마이징`_ 을 참조하십시오.

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
        <version>15.9.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.9.0</version>
            <relativePath />
        </parent>
    </project>

CSS·이미지 커스터마이징
-----------------------

JSP 는 Bootstrap 기반입니다. CSS 를 덮어써서 배색이나 레이아웃을 변경하거나,
``images/logo.png`` 를 교체하여 로고를 변경할 수 있습니다. 15.9 부터 이는
로그인 화면에만 영향을 줍니다. 검색 화면은 정적 테마입니다
(`번들 테마 커스터마이징`_ 참조).

빌드와 설치
--------------------

::

    mvn clean package

``target/`` 디렉터리에 JAR 파일(예: ``fess-theme-example-15.9.0.jar``)이
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
=========

- :doc:`plugin-architecture` - 플러그인 아키텍처
- :doc:`../admin/plugin-guide` - 플러그인 설치
