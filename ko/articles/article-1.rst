===============================================
Fess로 만드는 엔터프라이즈 검색 환경 〜 도입편
===============================================

들어가며
========

관리하는 문서는 날이 갈수록 증가하고, 이러한 문서를 효율적으로 관리하여 지식 활용이 되는 것이 요구됩니다.
관리 대상 문서가 많아질수록, 그 중에서 특정 정보를 가진 것을 찾기 어려워집니다.
그 해결책으로서 방대한 정보에서 검색할 수 있는 전문 검색 서버를 도입하는 것 등을 들 수 있습니다.

Fess는 쉽게 도입할 수 있는 Java 기반의 오픈소스 전문 검색 서버입니다.
Fess의 검색 엔진 부분에는 Elasticsearch를 이용하고 있습니다.
Elasticsearch는 Lucene 기반의 확장 가능하고 유연한 설계의 고기능 검색 엔진입니다.
한편으로, Elasticsearch로 전문 검색 시스템을 구축하려고 할 경우, 크롤러 부분 등 다양한 기능을 직접 구현할 필요가 있습니다.
Fess에서는 크롤러 부분에 Fess Crawler를 이용하여 웹이나 파일 시스템 상의 다양한 종류의 문서를 수집하여 검색 대상으로 할 수 있습니다.

이에, 본 기사에서는 Fess를 이용한 검색 서버 구축에 대해 소개합니다.

대상 독자
========

-  엔터프라이즈 검색/검색 시스템을 구축해 보고 싶은 분

-  기존 시스템에 검색 기능을 추가해 보고 싶은 분

- 사내 검색을 실현하여 지식을 활용할 수 있는 환경을 만들고 싶은 분

-  Lucene이나 Elasticsearch 등의 검색 소프트웨어에 관심이 있는 분

필요한 환경
==========

이 기사의 내용에 관해서는 다음 환경에서 동작 확인을 하고 있습니다.

-  Ubuntu 22.04

-  OpenJDK 21

Fess란
=========

Fess는 웹이나 파일 시스템을 대상으로 하는 오픈소스 전문 검색 시스템입니다.
GitHub의 CodeLibs 프로젝트에서 `Fess 사이트 <https://fess.codelibs.org/ja/>`__\ 로부터 Apache 라이센스로 제공되고 있습니다.

Fess의 특징
-----------

Java 기반 검색 시스템
~~~~~~~~~~~~~~~~~~~~~~~~~

Fess는 다양한 오픈소스 제품을 이용하여 구축되어 있습니다.

배포물은 실행 가능한 애플리케이션으로 제공됩니다.
Fess에서는 검색 화면과 관리 화면을 제공합니다.
Fess는 웹 프레임워크로 LastaFlute를 채용하고 있습니다.
따라서 화면 등의 커스터마이즈가 필요한 경우 JSP를 수정하는 것으로 간단하게 커스터마이즈가 가능합니다.
또한, 설정 데이터나 크롤 데이터는 OpenSearch에 저장되어 있으며, 이러한 데이터에 대한 접근은 O/R 매퍼인 DBFlute를 이용하여 접근하고 있습니다.

Fess는 Java 기반 시스템으로 구축되어 있으므로 Java가 동작 가능한 모든 플랫폼에서도 실행 가능합니다.
각종 설정도 웹 브라우저에서 간단하게 설정하는 UI를 갖추고 있습니다.

OpenSearch를 검색 엔진으로 이용
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenSearch는 AWS로부터 제공되는 Lucene을 기반으로 한 오픈소스 검색·분석 엔진입니다.
특징으로는 실시간 검색, 검색 결과 강조 표시 및 집계 기능 등을 지원하는 것을 들 수 있습니다.
또한, 검색 대상으로 할 수 있는 문서 수는 OpenSearch 서버 구성에 따라 수억 문서에 이르며, 대규모 사이트로도 확장할 수 있는 검색 서버입니다.
이용 실적도 일본에서도 다수 있으며, 주목받고 있는 검색 엔진 중 하나라고 할 수 있습니다.

Fess에서는 검색 엔진 부분에 OpenSearch를 채용하고 있습니다.
Fess의 Docker 버전에서는 OpenSearch를 내장한 형태로 배포하고 있지만, Fess 서버와는 별도의 서버로 분리하여 이용하는 것도 가능합니다.
또한, Fess와 OpenSearch에서 각각 이중화 구성을 구성할 수 있으며, 높은 확장성을 활용할 수 있는 설계로 되어 있습니다.

Fess Crawler를 크롤 엔진으로 이용
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fess Crawler는 CodeLibs 프로젝트로부터 제공되는 크롤러 프레임워크입니다.
Fess Crawler는 웹 상에 있는 문서나 파일 시스템 상에 있는 문서를 순회하여 수집할 수 있습니다.
문서 수집도 멀티스레드로 동시에 여러 문서를 효율적으로 처리하는 것이 가능합니다.
또한, 다룰 수 있는 문서는 HTML은 물론, Word나 Excel 등의 MS Office 계열 파일, zip 등의 아카이브 파일, 이미지나 음성 파일 등 다수의 포맷에 대응하고 있습니다(이미지나 음성 파일의 경우 메타 정보를 취득합니다).

Fess에서는 Fess Crawler를 이용하여 웹 상 및 파일 시스템 상의 문서를 순회하여 텍스트 정보를 수집합니다.
대응하는 파일 포맷도 Fess Crawler가 다룰 수 있는 것을 검색 대상으로 할 수 있습니다.
Fess Crawler로 크롤 실행하기 위한 파라미터 등은 Fess의 관리 UI에서 설정하는 것이 가능합니다.

설치와 시작
==================

여기에서는 Fess를 시작시켜 검색을 수행하기까지의 순서를 설명합니다.
Ubuntu 22.04에서 실행하는 것을 상정하여 설명하지만, macOS나 Windows에서도 거의 동일한 순서로 설치와 시작을 할 수 있습니다.

다운로드 및 설치
--------------------------

Fess 다운로드
^^^^^^^^^^^^^^^^^^^

https://github.com/codelibs/fess/releases 에서 최신 패키지를 다운로드합니다.
이 기사 작성 시점(2025/11)에서의 최신 버전은 15.3.0입니다.
다운로드 완료 후, 임의의 디렉터리에 압축을 해제하세요.

Fess 다운로드
|image1|

OpenSearch 다운로드
^^^^^^^^^^^^^^^^^^^^^^^^^

OpenSearch의 `다운로드 페이지 <https://opensearch.org/downloads.html>`__\ 에서 다운로드합니다.
Fess 다운로드 페이지에서는 각 버전에 대응하는 OpenSearch 버전을 기재하고 있으므로, 버전을 확인하고 다운로드하세요.
Fess 15.3.0에 대응하는 버전은 3.3.0이므로 이 버전을 다운로드합니다.
다운로드 완료 후, 임의의 디렉터리에 압축을 해제하세요.

설정
----

시작하기 전에 Fess에서 OpenSearch 클러스터에 접속하기 위한 설정을 합니다.
ZIP/TAR.GZ 패키지의 설정 방법에 관해서는 설치 페이지의 `설치 방법 <https://fess.codelibs.org/ja/15.3/install/install.html>`__\ 을 참조하세요.
이용하는 패키지가 RPM/DEB 패키지인 경우도 동일한 설치 페이지를 참조하세요.

시작
----

시작은 간단합니다. 압축 해제한 디렉터리 opensearch-<version>, fess-<version> 안에서 다음 명령을 실행합니다.
OpenSearch → Fess 순서로 시작합니다.

OpenSearch 시작
::

    $ ./bin/opensearch

Fess 시작
::

    $ ./bin/fess

브라우저에서 http://localhost:8080/ 에 접속하여 다음과 같은 화면이 표시되면 시작된 것입니다.

검색 톱 화면
|image2|

정지
----

Fess 서버를 정지시키려면 Fess 프로세스를 정지(kill)합니다.
정지할 때는 Fess → OpenSearch 순서로 정지합니다.

디렉터리 구성
----------------

디렉터리 구성은 다음과 같습니다.

Fess 디렉터리 구성
::

    fess-15.3.0
    ├── LICENSE
    ├── README.md
    ├── app
    │   ├── META-INF
    │   ├── WEB-INF
    │   │   ├── cachedirs
    │   │   ├── classes
    │   │   ├── conf
    │   │   ├── env
    │   │   ├── fe.tld
    │   │   ├── lib
    │   │   ├── logs
    │   │   ├── orig
    │   │   ├── plugin
    │   │   ├── project.properties
    │   │   ├── site
    │   │   ├── thumbnails
    │   │   ├── view
    │   ├── css
    │   │   ├── admin
    │   │   ├── fonts
    │   │   └── style.css
    │   ├── favicon.ico
    │   ├── images
    │   └── js
    ├── bin
    ├── extension
    ├── lib
    ├── logs
    └── temp


Fess는 LastaFlute가 제공하는 TomcatBoot를 기반으로 구성되어 있습니다.
Fess의 애플리케이션 그룹 파일은 app 디렉터리 이하에 배치됩니다.
관리 화면에서도 편집은 가능하지만, 검색 화면의 JSP는 app/WEB-INF/view 이하에 저장됩니다.
또한, app 디렉터리 직하의 js, css, images가 검색 화면에서 이용되는 파일입니다.

OpenSearch 디렉터리 구성
::

    opensearch-3.3.0
    ├── LICENSE.txt
    ├── NOTICE.txt
    ├── README.md
    ├── bin
    ├── config
    │   ├── opensearch.yml
    │   ├── jvm.options
    │   ├── jvm.options.d
    │   ├── log4j2.properties
    │   └── ...
    ├── data
    ├── lib
    ├── logs
    ├── modules
    └── plugins

인덱스 데이터는 data 디렉터리에 저장됩니다.

인덱스 작성부터 검색까지
==============================

시작 직후 상태에서는 검색하기 위한 인덱스가 작성되어 있지 않기 때문에 검색해도 아무런 결과가 반환되지 않습니다.
따라서 먼저 인덱스를 작성할 필요가 있습니다. 여기서는 https://fess.codelibs.org/ja/ 이하를 대상으로 인덱스를 작성하여 검색을 수행하기까지를 예로 들어 설명합니다.

관리 페이지 로그인
----------------------

먼저 관리 페이지인 http://localhost:8080/admin 에 접속하여 로그인하세요.
기본값은 사용자명, 비밀번호 모두 admin입니다.

관리 페이지 로그인
|image3|

크롤 대상 등록
------------------

다음으로 크롤 대상을 등록합니다. 이번에는 웹 페이지를 대상으로 하므로 관리 페이지 왼쪽에서 [웹]을 선택하세요.
초기 상태에서는 아무것도 등록되어 있지 않기 때문에 [신규 작성]을 선택합니다.

[신규 작성] 선택
|image4|

웹 크롤 설정으로, 이번에는 https://fess.codelibs.org/ja/ 이하의 페이지 그룹을 10초 간격의 2 스레드로 크롤하여(10초에 2페이지 정도를 크롤), 100페이지 정도를 검색 대상으로 합니다.
설정 항목은 URL : \https://fess.codelibs.org/ja/ , 크롤 대상 URL : \https://fess.codelibs.org/ja/.* , 최대 접속 수 : 100 , 스레드 수 : 2 , 간격 : 10000 밀리초로 하고, 그 외는 기본값으로 합니다.

웹 크롤 설정
|image5|

[작성]을 클릭하는 것으로 크롤 대상을 등록할 수 있습니다.
등록 내용은 각 설정을 클릭하여 변경하는 것이 가능합니다.

웹 크롤 설정 등록 완료
|image6|

크롤 시작
------------------

다음으로 시스템 > 스케줄러 > Default Crawler를 선택하여 [지금 시작] 버튼을 클릭합니다.

스케줄러 선택
|image7|

크롤이 시작되어 인덱스가 작성되고 있는지 여부는 시스템 정보 > 크롤 정보에서 확인할 수 있습니다.
크롤이 완료된 경우, [크롤 정보]의 인덱스 크기(웹/파일)에 검색 대상으로 한 문서 수가 표시됩니다.

크롤 상황 확인
|image8|

크롤이 완료된 경우의 예
|image9|

검색 실행 예
----------

크롤 완료 후, 검색하면 아래 이미지와 같은 결과가 반환됩니다.

검색 예
|image10|

검색 화면 커스터마이즈
======================

여기에서는 이용자가 가장 많이 보는 검색 톱 화면과 검색 결과 일람 화면을 커스터마이즈하는 방법을 소개합니다.

이번에는 로고 파일명을 바꾸는 방법을 나타냅니다.
디자인 자체를 바꾸고 싶은 경우에 관해서는 간단한 JSP 파일로 기술되어 있으므로 HTML 지식이 있으면 변경할 수 있습니다.

먼저 검색 톱 화면은 "app/WEB-INF/view/index.jsp" 파일입니다.

검색 톱 화면의 JSP 파일 일부
::

    <la:form action="/search" method="get" styleId="searchForm">
      ${fe:facetForm()}${fe:geoForm()}
      ・
      ・
      ・
      <main class="container">
        <div class="row">
          <div class="col text-center searchFormBox">
            <h1 class="mainLogo">
              <img src="${fe:url('/images/logo.png')}"
                alt="<la:message key="labels.index_title" />" />
            </h1>
            <div class="notification">${notification}</div>
            <div>
              <la:info id="msg" message="true">
                <div class="alert alert-info">${msg}</div>
              </la:info>
              <la:errors header="errors.front_header"
                footer="errors.front_footer" prefix="errors.front_prefix"
                suffix="errors.front_suffix" />
            </div>

검색 톱 화면에 표시되는 이미지를 변경하는 경우 위의 "logo.png" 부분을 바꾸고 싶은 파일명으로 변경합니다.
파일은 "app/images"에 배치합니다.

<la:form>이나 <la:message> 등은 JSP 태그입니다.
예를 들어, <s:form>은 실제 HTML 표시 시 form 태그로 변환됩니다.
자세한 설명은 LastaFlute 사이트나 JSP에 관한 사이트를 참조하세요.

다음으로 검색 결과 일람 화면의 헤더 부분은 "app/WEB-INF/view/header.jsp" 파일입니다.

헤더 JSP 파일 일부
::

				<la:link styleClass="navbar-brand d-inline-flex" href="/">
					<img src="${fe:url('/images/logo-head.png')}"
						alt="<la:message key="labels.header_brand_name" />"
						class="align-items-center" />
				</la:link>

검색 결과 일람 화면 상부에 표시되는 이미지를 변경하는 경우 위의 "logo-head.png" 부분의 파일명을 변경합니다.
"logo.png"의 경우와 마찬가지로 "app/images"에 배치합니다.

또한, 이러한 설정은 시스템 > 페이지 디자인에서도 설정하는 것이 가능합니다.

JSP 파일에서 이용하는 CSS 파일을 변경하고 싶은 경우 "app/css"에 배치되어 있는 "style.css"를 편집하세요.

정리
======

전문 검색 시스템인 Fess에 대해 설치부터 검색까지와 간단한 커스터마이즈 방법에 대해 설명했습니다.
특별한 환경 구축도 필요 없이 Java 실행 환경이 있으면 검색 시스템을 간단하게 구축할 수 있다는 것을 소개할 수 있었다고 생각합니다.
기존 시스템에 사이트 검색 기능을 추가하고 싶은 경우에도 도입할 수 있으므로 꼭 시도해 보세요.

참고 자료
========

-  `Fess <https://fess.codelibs.org/ja/>`__

-  `OpenSearch <https://opensearch.org/>`__

-  `LastaFlute <https://lastaflute.dbflute.org/>`__
.. |image1| image:: ../../resources/images/en/article/1/fess-download.png
.. |image2| image:: ../../resources/images/en/article/1/top.png
.. |image3| image:: ../../resources/images/en/article/1/login.png
.. |image4| image:: ../../resources/images/en/article/1/web-crawl-conf-1.png
.. |image5| image:: ../../resources/images/en/article/1/web-crawl-conf-2.png
.. |image6| image:: ../../resources/images/en/article/1/web-crawl-conf-3.png
.. |image7| image:: ../../resources/images/en/article/1/scheduler.png
.. |image8| image:: ../../resources/images/en/article/1/session-info-1.png
.. |image9| image:: ../../resources/images/en/article/1/session-info-2.png
.. |image10| image:: ../../resources/images/en/article/1/search-result.png
