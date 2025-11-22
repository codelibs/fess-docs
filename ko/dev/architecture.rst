============================
아키텍처 및 코드 구조
============================

이 페이지에서는 |Fess| 의 아키텍처, 코드 구조,
주요 컴포넌트에 대해 설명합니다.
|Fess| 의 내부 구조를 이해함으로써 효율적으로 개발을 진행할 수 있습니다.

.. contents:: 목차
   :local:
   :depth: 2

전체 아키텍처
================

|Fess| 는 다음 주요 컴포넌트로 구성됩니다:

.. code-block:: text

    ┌─────────────────────────────────────────────────┐
    │          사용자 인터페이스                         │
    │  ┌──────────────┐      ┌──────────────┐        │
    │  │  검색 화면     │      │   관리 화면    │        │
    │  │  (JSP/HTML)   │      │   (JSP/HTML)  │        │
    │  └──────────────┘      └──────────────┘        │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │              웹 애플리케이션 계층                   │
    │  ┌──────────────────────────────────────────┐  │
    │  │           LastaFlute                       │  │
    │  │  ┌────────┐  ┌─────────┐  ┌──────────┐  │  │
    │  │  │ Action │  │  Form   │  │  Service │  │  │
    │  │  └────────┘  └─────────┘  └──────────┘  │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │              비즈니스 로직 계층                      │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
    │  │ Crawler  │  │  Job     │  │  Helper  │    │
    │  └──────────┘  └──────────┘  └──────────┘    │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │              데이터 액세스 계층                      │
    │  ┌──────────────────────────────────────────┐  │
    │  │          DBFlute / OpenSearch             │  │
    │  │  ┌────────┐  ┌─────────┐  ┌──────────┐  │  │
    │  │  │Behavior│  │ Entity  │  │  Query   │  │  │
    │  │  └────────┘  └─────────┘  └──────────┘  │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │               데이터 스토어                         │
    │              OpenSearch 3.3.0                   │
    └─────────────────────────────────────────────────┘

계층 설명
------------

사용자 인터페이스 계층
~~~~~~~~~~~~~~~~~~~~~~~~

사용자가 직접 조작하는 화면입니다.
JSP와 HTML, JavaScript로 구현되어 있습니다.

- 검색 화면: 최종 사용자용 검색 인터페이스
- 관리 화면: 시스템 관리자용 설정·관리 인터페이스

웹 애플리케이션 계층
~~~~~~~~~~~~~~~~~~~~

LastaFlute 프레임워크를 사용한 웹 애플리케이션 계층입니다.

- **Action**: HTTP 요청을 처리하고 비즈니스 로직 호출
- **Form**: 요청 파라미터 수신 및 검증
- **Service**: 비즈니스 로직 구현

비즈니스 로직 계층
~~~~~~~~~~~~~~~~

|Fess| 의 주요 기능을 구현하는 계층입니다.

- **Crawler**: 웹사이트나 파일 시스템에서 데이터 수집
- **Job**: 스케줄 실행되는 작업
- **Helper**: 애플리케이션 전체에서 사용되는 헬퍼 클래스

데이터 액세스 계층
~~~~~~~~~~~~~~

DBFlute를 사용한 OpenSearch 액세스 계층입니다.

- **Behavior**: 데이터 조작 인터페이스
- **Entity**: 데이터 실체
- **Query**: 검색 쿼리 구축

데이터 스토어 계층
~~~~~~~~~~~~

검색 엔진으로 OpenSearch 3.3.0을 사용합니다.

프로젝트 구조
==============

디렉터리 구조
--------------

.. code-block:: text

    fess/
    ├── src/
    │   ├── main/
    │   │   ├── java/org/codelibs/fess/
    │   │   │   ├── app/              # 웹 애플리케이션
    │   │   │   │   ├── web/          # 검색 화면
    │   │   │   │   │   ├── admin/    # 관리 화면
    │   │   │   │   │   │   ├── ...Action.java
    │   │   │   │   │   │   └── ...Form.java
    │   │   │   │   │   └── ...Action.java
    │   │   │   │   └── service/      # 서비스 계층
    │   │   │   ├── crawler/          # 크롤러
    │   │   │   │   ├── client/       # 크롤러 클라이언트
    │   │   │   │   ├── extractor/    # 콘텐츠 추출
    │   │   │   │   ├── filter/       # 필터
    │   │   │   │   └── transformer/  # 데이터 변환
    │   │   │   ├── es/               # OpenSearch 관련
    │   │   │   │   ├── client/       # OpenSearch 클라이언트
    │   │   │   │   ├── query/        # 쿼리 빌더
    │   │   │   │   └── config/       # 설정 관리
    │   │   │   ├── helper/           # 헬퍼 클래스
    │   │   │   │   ├── ...Helper.java
    │   │   │   ├── job/              # 작업
    │   │   │   │   ├── ...Job.java
    │   │   │   ├── util/             # 유틸리티
    │   │   │   ├── entity/           # 엔티티(자동 생성)
    │   │   │   ├── mylasta/          # LastaFlute 설정
    │   │   │   │   ├── action/       # Action 기본 클래스
    │   │   │   │   ├── direction/    # 애플리케이션 설정
    │   │   │   │   └── mail/         # 메일 설정
    │   │   │   ├── Constants.java    # 상수 정의
    │   │   │   └── FessBoot.java     # 시작 클래스
    │   │   ├── resources/
    │   │   │   ├── fess_config.properties  # 설정 파일
    │   │   │   ├── fess_config.xml         # 추가 설정
    │   │   │   ├── fess_message_ja.properties  # 메시지(일본어)
    │   │   │   ├── fess_message_en.properties  # 메시지(영어)
    │   │   │   ├── log4j2.xml              # 로그 설정
    │   │   │   └── ...
    │   │   └── webapp/
    │   │       ├── WEB-INF/
    │   │       │   ├── view/          # JSP 파일
    │   │       │   │   ├── admin/     # 관리 화면 JSP
    │   │       │   │   └── ...
    │   │       │   └── web.xml
    │   │       ├── css/               # CSS 파일
    │   │       ├── js/                # JavaScript 파일
    │   │       └── images/            # 이미지 파일
    │   └── test/
    │       └── java/org/codelibs/fess/
    │           ├── ...Test.java       # 테스트 클래스
    │           └── it/                # 통합 테스트
    ├── pom.xml                        # Maven 설정
    ├── dbflute_fess/                  # DBFlute 설정
    │   ├── dfprop/                    # DBFlute 속성
    │   └── freegen/                   # FreeGen 설정
    └── README.md

주요 패키지 상세
==================

app 패키지
------------

웹 애플리케이션 계층의 코드입니다.

app.web 패키지
~~~~~~~~~~~~~~~~

검색 화면과 최종 사용자용 기능을 구현합니다.

**주요 클래스:**

- ``SearchAction.java``: 검색 처리
- ``LoginAction.java``: 로그인 처리

**예:**

.. code-block:: java

    @Execute
    public HtmlResponse index(SearchForm form) {
        // 검색 처리 구현
        return asHtml(path_IndexJsp);
    }

app.web.admin 패키지
~~~~~~~~~~~~~~~~~~~~~~~

관리 화면의 기능을 구현합니다.

**주요 클래스:**

- ``BwCrawlingConfigAction.java``: 웹 크롤 설정
- ``BwSchedulerAction.java``: 스케줄러 관리
- ``BwUserAction.java``: 사용자 관리

**명명 규칙:**

- ``Bw`` 접두사: Admin용 Action
- ``Action`` 접미사: Action 클래스
- ``Form`` 접미사: Form 클래스

app.service 패키지
~~~~~~~~~~~~~~~~~~~~

비즈니스 로직을 구현하는 서비스 계층입니다.

**주요 클래스:**

- ``SearchService.java``: 검색 서비스
- ``UserService.java``: 사용자 관리 서비스
- ``ScheduledJobService.java``: 작업 관리 서비스

**예:**

.. code-block:: java

    public class SearchService {
        public SearchResponse search(SearchRequestParams params) {
            // 검색 로직 구현
        }
    }

crawler 패키지
----------------

데이터 수집 기능을 구현합니다.

crawler.client 패키지
~~~~~~~~~~~~~~~~~~~~~~~

각종 데이터 소스에 대한 액세스를 구현합니다.

**주요 클래스:**

- ``FessClient.java``: 크롤러 클라이언트의 기본 클래스
- ``WebClient.java``: 웹사이트 크롤링
- ``FileSystemClient.java``: 파일 시스템 크롤링
- ``DataStoreClient.java``: 데이터베이스 등 크롤링

crawler.extractor 패키지
~~~~~~~~~~~~~~~~~~~~~~~~~~

문서에서 텍스트를 추출합니다.

**주요 클래스:**

- ``ExtractorFactory.java``: 추출기 팩토리
- ``TikaExtractor.java``: Apache Tika를 사용한 추출

crawler.transformer 패키지
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

크롤링한 데이터를 검색용 형식으로 변환합니다.

**주요 클래스:**

- ``Transformer.java``: 변환 처리 인터페이스
- ``BasicTransformer.java``: 기본 변환 처리

es 패키지
-----------

OpenSearch와의 연동을 구현합니다.

es.client 패키지
~~~~~~~~~~~~~~~~~~

OpenSearch 클라이언트 구현입니다.

**주요 클래스:**

- ``FessEsClient.java``: OpenSearch 클라이언트
- ``SearchEngineClient.java``: 검색 엔진 클라이언트 인터페이스

es.query 패키지
~~~~~~~~~~~~~~~~~

검색 쿼리 구축을 구현합니다.

**주요 클래스:**

- ``QueryHelper.java``: 쿼리 구축 헬퍼
- ``FunctionScoreQueryBuilder.java``: 스코어링 조정

helper 패키지
---------------

애플리케이션 전체에서 사용되는 헬퍼 클래스입니다.

**주요 클래스:**

- ``SystemHelper.java``: 시스템 전체 헬퍼
- ``CrawlingConfigHelper.java``: 크롤 설정 헬퍼
- ``SearchLogHelper.java``: 검색 로그 헬퍼
- ``UserInfoHelper.java``: 사용자 정보 헬퍼
- ``ViewHelper.java``: 뷰 관련 헬퍼

**예:**

.. code-block:: java

    public class SystemHelper {
        public void initializeSystem() {
            // 시스템 초기화 처리
        }
    }

job 패키지
------------

스케줄 실행되는 작업을 구현합니다.

**주요 클래스:**

- ``CrawlJob.java``: 크롤 작업
- ``SuggestJob.java``: 제안 작업
- ``ScriptExecutorJob.java``: 스크립트 실행 작업

**예:**

.. code-block:: java

    public class CrawlJob extends LaJob {
        @Override
        public void run() {
            // 크롤 처리 구현
        }
    }

entity 패키지
---------------

OpenSearch 문서에 대응하는 엔티티 클래스입니다.
이 패키지는 DBFlute로 자동 생성됩니다.

**주요 클래스:**

- ``SearchLog.java``: 검색 로그
- ``ClickLog.java``: 클릭 로그
- ``FavoriteLog.java``: 즐겨찾기 로그
- ``User.java``: 사용자 정보
- ``Role.java``: 역할 정보

.. note::

   entity 패키지의 코드는 자동 생성되므로
   직접 편집하지 마세요.
   스키마를 변경하여 재생성하는 것으로 업데이트합니다.

mylasta 패키지
----------------

LastaFlute의 설정과 커스터마이즈를 수행합니다.

mylasta.action 패키지
~~~~~~~~~~~~~~~~~~~~~~~

Action의 기본 클래스를 정의합니다.

- ``FessUserBean.java``: 사용자 정보
- ``FessHtmlPath.java``: HTML 경로 정의

mylasta.direction 패키지
~~~~~~~~~~~~~~~~~~~~~~~~~~

애플리케이션 전체 설정을 수행합니다.

- ``FessConfig.java``: 설정 읽기
- ``FessFwAssistantDirector.java``: 프레임워크 설정

디자인 패턴 및 구현 패턴
============================

|Fess| 에서는 다음과 같은 디자인 패턴이 사용됩니다.

MVC 패턴
----------

LastaFlute에 의한 MVC 패턴으로 구현되어 있습니다.

- **Model**: Service, Entity
- **View**: JSP
- **Controller**: Action

예:

.. code-block:: java

    // Controller (Action)
    public class SearchAction extends FessBaseAction {
        @Resource
        private SearchService searchService;  // Model (Service)

        @Execute
        public HtmlResponse index(SearchForm form) {
            SearchResponse response = searchService.search(form);
            return asHtml(path_IndexJsp).renderWith(data -> {
                data.register("response", response);  // View (JSP)로 데이터 전달
            });
        }
    }

DI 패턴
---------

LastaFlute의 DI 컨테이너를 사용합니다.

.. code-block:: java

    public class SearchService {
        @Resource
        private SearchEngineClient searchEngineClient;

        @Resource
        private UserInfoHelper userInfoHelper;
    }

Factory 패턴
--------------

각종 컴포넌트 생성에 사용됩니다.

.. code-block:: java

    public class ExtractorFactory {
        public Extractor createExtractor(String mimeType) {
            // MIME 타입에 따른 Extractor 생성
        }
    }

Strategy 패턴
---------------

크롤러와 트랜스포머에서 사용됩니다.

.. code-block:: java

    public interface Transformer {
        Map<String, Object> transform(Map<String, Object> data);
    }

    public class HtmlTransformer implements Transformer {
        // HTML용 변환 처리
    }

설정 관리
======

|Fess| 의 설정은 여러 파일로 관리됩니다.

fess_config.properties
--------------------

애플리케이션의 주요 설정을 정의합니다.

.. code-block:: properties

    # 포트 번호
    server.port=8080

    # OpenSearch 연결 설정
    opensearch.http.url=http://localhost:9201

    # 크롤 설정
    crawler.document.max.size=10000000

fess_config.xml
--------------

XML 형식의 추가 설정입니다.

.. code-block:: xml

    <component name="searchService" class="...SearchService">
        <property name="maxSearchResults">1000</property>
    </component>

fess_message_*.properties
------------------------

다국어 대응 메시지 파일입니다.

- ``fess_message_ja.properties``: 일본어
- ``fess_message_en.properties``: 영어

데이터 플로우
==========

검색 플로우
--------

.. code-block:: text

    1. 사용자가 검색 화면에서 검색
       ↓
    2. SearchAction이 검색 요청 수신
       ↓
    3. SearchService가 비즈니스 로직 실행
       ↓
    4. SearchEngineClient가 OpenSearch에 검색 쿼리 전송
       ↓
    5. OpenSearch가 검색 결과 반환
       ↓
    6. SearchService가 결과 정형화
       ↓
    7. SearchAction이 JSP에 결과 전달하여 표시

크롤링 플로우
------------

.. code-block:: text

    1. CrawlJob이 스케줄 실행됨
       ↓
    2. CrawlingConfigHelper가 크롤 설정 취득
       ↓
    3. FessClient가 대상 사이트에 접속
       ↓
    4. Extractor가 콘텐츠에서 텍스트 추출
       ↓
    5. Transformer가 데이터를 검색용 형식으로 변환
       ↓
    6. SearchEngineClient가 OpenSearch에 문서 등록

확장 포인트
==========

|Fess| 는 다음 포인트에서 확장할 수 있습니다.

커스텀 크롤러 추가
--------------------

``FessClient`` 를 상속하여 독자적인 데이터 소스에 대응할 수 있습니다.

커스텀 트랜스포머 추가
----------------------------

``Transformer`` 를 구현하여 독자적인 데이터 변환 처리를 추가할 수 있습니다.

커스텀 추출기 추가
--------------------------

``Extractor`` 를 구현하여 독자적인 콘텐츠 추출 처리를 추가할 수 있습니다.

커스텀 플러그인 추가
--------------------

``Plugin`` 인터페이스를 구현하여 독자적인 플러그인을 만들 수 있습니다.

참고 자료
======

프레임워크
------------

- `LastaFlute 레퍼런스 <https://github.com/lastaflute/lastaflute>`__
- `DBFlute 문서 <https://dbflute.seasar.org/>`__

기술 문서
--------------

- `OpenSearch API 레퍼런스 <https://opensearch.org/docs/latest/api-reference/>`__
- `Apache Tika <https://tika.apache.org/>`__

다음 단계
==========

아키텍처를 이해했다면 다음 문서를 참조하세요:

- :doc:`workflow` - 실제 개발 플로우
- :doc:`building` - 빌드 및 테스트
- :doc:`contributing` - 풀 리퀘스트 작성
