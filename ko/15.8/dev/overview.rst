==================================
개발자 문서 개요
==================================

개요
====

이 섹션에서는 |Fess| 의 확장 개발에 대해 설명합니다.
플러그인 개발, 커스텀 커넥터 작성, 테마 커스터마이즈 등
|Fess| 를 확장하기 위한 정보를 제공합니다.

대상 독자
========

- |Fess| 의 커스텀 기능을 개발하고 싶은 개발자
- 플러그인을 작성하고 싶은 개발자
- |Fess| 의 소스 코드를 이해하고 싶은 개발자

필요 지식
--------

- Java 21의 기본적인 지식
- Maven(빌드 시스템)의 기본
- 웹 애플리케이션 개발 경험

개발 환경
========

권장 환경
--------

- **JDK**: OpenJDK 21 이상
- **IDE**: IntelliJ IDEA / Eclipse / VS Code
- **빌드 도구**: Maven 3.9 이상
- **Git**: 버전 관리

설정
------------

1. 소스 코드 취득:

::

    git clone https://github.com/codelibs/fess.git
    cd fess

2. 빌드:

::

    mvn package -DskipTests

3. 개발 서버 시작:

::

    ./bin/fess

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
     - DBFlute에 의한 OpenSearch 연계
   * - 크롤러
     - fess-crawler 라이브러리에 의한 콘텐츠 수집
   * - 검색 엔진
     - OpenSearch에 의한 전문 검색

주요 프레임워크
------------------

- **LastaFlute**: 웹 프레임워크 (액션, 폼, 밸리데이션)
- **DBFlute**: 데이터 액세스 프레임워크 (OpenSearch 연계)
- **Lasta Di**: 의존성 주입 컨테이너

디렉토리 구조
================

::

    fess/
    ├── src/main/java/org/codelibs/fess/
    │   ├── app/
    │   │   ├── web/         # 컨트롤러(Action)
    │   │   ├── service/     # 서비스
    │   │   └── pager/       # 페이지네이션
    │   ├── api/             # REST API
    │   ├── helper/          # 헬퍼 클래스
    │   ├── crawler/         # 크롤러 관련
    │   ├── opensearch/      # OpenSearch 연계(DBFlute 생성)
    │   ├── llm/             # LLM 통합
    │   └── ds/              # 데이터스토어 커넥터
    ├── src/main/resources/
    │   ├── fess_config.properties  # 설정
    │   └── fess_*.xml              # DI 설정
    └── src/main/webapp/
        └── WEB-INF/view/    # JSP 템플릿

확장 포인트
============

|Fess| 는 다음의 확장 포인트를 제공합니다:

플러그인
----------

플러그인을 사용하여 기능을 추가할 수 있습니다.

- **데이터스토어 플러그인**: 새로운 데이터 소스에서 크롤링
- **스크립트 엔진 플러그인**: 새로운 스크립트 언어 지원
- **웹앱 플러그인**: 웹 인터페이스 확장
- **Ingest 플러그인**: 인덱싱 시 데이터 가공

상세: :doc:`plugin-architecture`

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

- 유닛 테스트 작성 (``*Test.java``)
- 통합 테스트는 ``*Tests.java``

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
