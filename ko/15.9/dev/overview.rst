==================================
개발자 문서 개요
==================================

개요
====

이 섹션에서는 |Fess| 의 확장 개발에 대해 설명합니다.
플러그인 개발, 커스텀 커넥터 작성, 테마 커스터마이즈 등
|Fess| 를 확장하기 위한 정보를 제공합니다.

대상 독자
==========

- |Fess| 의 커스텀 기능을 개발하고 싶은 개발자
- 플러그인을 작성하고 싶은 개발자
- |Fess| 의 소스 코드를 이해하고 싶은 개발자

필요 지식
----------

- Java 21의 기본적인 지식
- Maven(빌드 시스템)의 기본
- 웹 애플리케이션 개발 경험
- OpenSearch에 대한 기본적인 지식(|Fess| 는 검색 엔진으로 OpenSearch를 사용합니다)

개발 환경
==========

권장 환경
----------

- **JDK**: OpenJDK 21 이상
- **IDE**: IntelliJ IDEA / Eclipse / VS Code
- **빌드 도구**: Maven(빌드에서 최소 버전이 강제되지는 않지만, Java 21에 대응하는 최신 3.x를 권장)
- **Git**: 버전 관리
- **OpenSearch**: 검색 엔진의 백엔드(IDE에서 실행하는 경우, 필요한 모듈과 플러그인은 빌드 시 다운로드됩니다)

설정
------------

|Fess| 는 Maven 프로젝트로 빌드합니다. 개발 시에는 IDE에서 실행하는 것이 가장 간단합니다.

1. 소스 코드 취득:

   ::

       git clone https://github.com/codelibs/fess.git

2. IDE로 임포트:

   취득한 디렉토리를 Maven 프로젝트로 IDE에 임포트합니다.

3. OpenSearch용 모듈·플러그인 다운로드:

   최초 한 번만 다음 명령으로 검색 엔진의 모듈과 플러그인을 ``plugins`` 디렉토리에 취득합니다.

   ::

       mvn antrun:run

4. 개발 서버 시작(IDE에서):

   IDE에서 ``org.codelibs.fess.FessBoot`` 를 실행 또는 디버그 실행하고,
   브라우저에서 http://localhost:8080/ 을 엽니다.
   관리 화면은 http://localhost:8080/admin/ (초기 계정: ``admin`` / ``admin``)입니다.

5. 패키지 빌드(배포물 생성):

   배포 패키지가 필요한 경우 ``package`` 골을 실행합니다.
   결과물은 ``target/releases`` 에 생성됩니다(유닛 테스트를 건너뛰려면 ``-DskipTests`` 를 지정).

   ::

       mvn package

   생성된 배포물을 압축 해제하면 ``bin/fess`` 실행 스크립트를 사용할 수 있습니다.

   ::

       unzip target/releases/fess-*.zip
       ./fess-*/bin/fess

.. note::

    ``bin/fess`` 실행 스크립트는 배포 패키지(zip/rpm/deb)에 포함되어 있는 것입니다.
    소스 트리에서 ``mvn package`` 를 실행하는 것만으로는 저장소 바로 아래에 ``bin/fess`` 가 생성되지 않습니다.
    소스에서 개발할 때는 위와 같이 IDE에서 ``FessBoot`` 를 실행하거나,
    압축을 해제한 배포물의 ``bin/fess`` 를 사용하세요.

아키텍처 개요
==================

|Fess| 는 다음의 주요 컴포넌트로 구성되어 있습니다:

컴포넌트 구성
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 컴포넌트
     - 설명
   * - Web층
     - LastaFlute 프레임워크에 의한 MVC 구현
   * - 서비스층
     - 비즈니스 로직
   * - 데이터 액세스층
     - DBFlute(ESFlute/FreeGen)에 의한 타입 세이프 OpenSearch 액세스
   * - 크롤러
     - fess-crawler 라이브러리에 의한 콘텐츠 수집
   * - 검색 엔진
     - OpenSearch에 의한 전문 검색

주요 프레임워크
------------------

- **LastaFlute**: 웹 프레임워크(액션, 폼, 밸리데이션)
- **DBFlute**: 데이터 액세스 프레임워크. OpenSearch용 타입 세이프 액세스 클래스(``Bhv`` / ``ConditionBean``)는
  DBFlute의 FreeGen 기능과 ESFlute 템플릿에 의해 생성됩니다
  (재생성은 ``mvn dbflute:freegen``)
- **Lasta Di**: 의존성 주입 컨테이너

디렉토리 구조
================

::

    fess/
    ├── src/main/java/org/codelibs/fess/
    │   ├── app/
    │   │   ├── web/         # 컨트롤러(Action)
    │   │   ├── service/     # 서비스
    │   │   ├── logic/       # 로직
    │   │   └── pager/       # 페이지네이션
    │   ├── api/             # REST API(api/v2 등)
    │   ├── helper/          # 헬퍼 클래스
    │   ├── crawler/         # 크롤러 관련
    │   ├── indexer/         # 인덱스 처리
    │   ├── opensearch/      # OpenSearch 액세스(ESFlute/FreeGen 생성)
    │   ├── llm/             # LLM 통합
    │   ├── ds/              # 데이터스토어 커넥터
    │   ├── ingest/          # Ingest(인덱싱 시 데이터 가공)
    │   ├── script/          # 스크립트 엔진
    │   ├── entity/          # 엔티티
    │   └── mylasta/         # LastaFlute 설정(DI·메시지·타입 세이프 설정)
    ├── src/main/resources/
    │   ├── fess_config.properties  # 설정
    │   └── fess_*.xml              # DI 설정(app.xml, fess_ds.xml 등)
    └── src/main/webapp/
        └── WEB-INF/view/    # JSP 템플릿

확장 포인트
============

|Fess| 는 다음의 확장 포인트를 제공합니다:

플러그인
----------

플러그인을 사용하여 기능을 추가할 수 있습니다.

- **데이터스토어 플러그인**: 새로운 데이터 소스로부터의 크롤링(``AbstractDataStore`` 를 상속)
- **스크립트 엔진 플러그인**: 새로운 스크립트 언어 지원(``ScriptEngine`` 을 구현)
- **웹앱 플러그인**: 웹 인터페이스 확장(Lasta Di의 컴포넌트 오버라이드와 리소스 병합)
- **Ingest 플러그인**: 인덱싱 시 데이터 가공(``Ingester`` 를 상속)

상세: :doc:`plugin-architecture`

.. note::

    |Fess| 본체는 ``war`` 로 패키징됩니다. 플러그인을 로컬에서 빌드할 때
    |Fess| 를 의존성으로 해결할 수 없는 경우에는, ``pom.xml`` 의 ``<packaging>`` 을 일시적으로 ``jar`` 로 변경하여
    ``mvn clean install -DskipTests`` 를 실행한 후, ``war`` 로 되돌리세요.

테마
------

검색 화면의 디자인을 커스터마이즈할 수 있습니다.

상세: :doc:`theme-development`

설정
----

``fess_config.properties`` 에서 다양한 동작을 커스터마이즈할 수 있습니다.

상세: :doc:`../config/intro`

플러그인 개발
==============

플러그인 개발의 상세에 대해서는 다음을 참조하세요:

- :doc:`plugin-architecture` - 플러그인 아키텍처
- :doc:`datastore-plugin` - 데이터스토어 플러그인 개발
- :doc:`script-engine-plugin` - 스크립트 엔진 플러그인
- :doc:`webapp-plugin` - 웹앱 플러그인
- :doc:`ingest-plugin` - Ingest 플러그인

테마 개발
==========

- :doc:`theme-development` - 테마 커스터마이즈

베스트 프랙티스
==================

코딩 규약
----------------

- |Fess| 의 기존 코드 스타일을 따름
- ``mvn formatter:format`` 으로 코드 포맷
- ``mvn license:format`` 으로 라이선스 헤더 추가

테스트
------

- 유닛 테스트(``*Test.java``): 기본 ``build`` 프로파일에서 ``mvn test`` 로 실행됩니다
- 통합 테스트(``*Tests.java``): ``mvn test -P integrationTests`` 로 실행됩니다.
  통합 테스트를 실행하려면 실행 중인 |Fess| 서버와 OpenSearch가 필요합니다

로깅
--------

- Log4j2 사용
- ``logger.debug()`` / ``logger.info()`` / ``logger.warn()`` / ``logger.error()``
- 민감한 정보는 로그에 출력하지 않음

리소스
========

- `GitHub Repository <https://github.com/codelibs/fess>`__
- `Issue Tracker <https://github.com/codelibs/fess/issues>`__
- `Discussions <https://github.com/codelibs/fess/discussions>`__
