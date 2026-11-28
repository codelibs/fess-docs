==========================
플러그인으로 Fess 확장하기
==========================

들어가며
========

사내 고유 시스템에 맞는 ``fess-ds-*`` 플러그인이 없거나, 모든 문서를 등록하기 전에 가공하고 싶다면 플러그인을 직접 만듭니다.
이 글은 Java 개발자를 대상으로, Fess 15.9에서 동작하는 플러그인을 공식 템플릿으로 만들고, 설치하여 동작을 확인하기까지의 과정을 설명합니다.

이 글의 절차를 그대로 실행하면 다음을 할 수 있게 됩니다.

- 플러그인의 종류와 Fess가 이를 구별하는 방식을 이해한다
- ``fess-ds-example``\ 을 바탕으로 데이터 저장소 플러그인을 빌드하고, Fess에 넣어 문서를 등록한다
- ``fess-ingest-example``\ 을 바탕으로 등록 전 문서를 가공하는 Ingester를 만든다

전제로, Java 21 이상과 Maven 3을 사용할 수 있고 Fess 15.9가 실행 중이라고 가정합니다(:doc:`guide-02`).
데이터 저장소 설정 화면의 사용법은 :doc:`datastore-basics`\ 에서 설명하므로, 먼저 읽어 두면 절차를 따라가기 쉬워집니다.

플러그인의 종류
===============

플러그인은 jar 파일이며, Fess 설치 디렉터리의 ``app/WEB-INF/plugin/``\ 에 놓입니다.
Fess는 jar 파일 이름의 앞부분(접두사)으로 플러그인의 종류를 판별합니다(``PluginHelper.ArtifactType``).
15.9의 종류는 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 22 43 35

   * - 접두사
     - 역할
     - 참고할 리포지토리
   * - ``fess-ds``
     - 데이터 저장소. 외부 시스템에서 레코드를 가져와 등록한다
     - ``fess-ds-example``
   * - ``fess-ingest``
     - Ingester. 등록 전 문서를 가공한다
     - ``fess-ingest-example``
   * - ``fess-script``
     - 스크립트 엔진
     - ``fess-script-groovy``
   * - ``fess-webapp``
     - 웹 애플리케이션 확장(API나 엔드포인트 추가)
     - ``fess-webapp-mcp``
   * - ``fess-thumbnail``
     - 섬네일 생성
     - ``fess-thumbnail-playwright``
   * - ``fess-crawler``
     - 크롤러 클라이언트
     - ``fess-crawler-playwright``
   * - ``fess-llm``
     - AI 검색 모드에서 사용하는 LLM 제공자
     - ``fess-llm-openai``
   * - ``fess-storage``
     - 오브젝트 스토리지(S3 / GCS)
     - ``fess-storage-s3``
   * - ``fess-sso``
     - 싱글 사인온 인증 방식
     - ``fess-sso-oidc``

모든 리포지토리는 https://github.com/codelibs 에 공개되어 있습니다.

검색 화면의 디자인은 플러그인으로 바꾸지 않습니다.
JSP를 교체하는 ``fess-theme-*`` JAR 테마 플러그인은 15.9에서 삭제되었고, 검색 화면은 ``theme.yml``, ``index.html``, ``assets/``\ 로 구성된 ZIP 테마가 되었습니다.
테마는 [시스템] > [테마]에서 업로드합니다.
만드는 방법은 `테마 개발 가이드 <https://fess.codelibs.org/ko/stable/dev/theme-development.html>`__\ 를, 기존 사이트에 넣는 방법은 :doc:`guide-03`\ 을 참조하십시오.

데이터 저장소 플러그인 만들기
=============================

템플릿 가져오기
---------------

``fess-ds-example``\ 은 데이터 저장소 플러그인의 템플릿으로 공개된 리포지토리입니다.
기본 브랜치는 개발 중인 버전(15.10.0-SNAPSHOT)에 맞춰져 있으므로, 15.9용으로 빌드하려면 15.9.0에 맞춘 커밋을 사용합니다.

::

    $ git clone https://github.com/codelibs/fess-ds-example.git
    $ cd fess-ds-example
    $ git checkout 0252a8b08d7de4eeea7a88c52aa884094ef099be

이 커밋과 기본 브랜치의 차이는 ``pom.xml``\ 의 2줄(프로젝트와 부모 POM의 버전)뿐입니다.
기본 브랜치 그대로 다음 절의 2곳을 15.9용으로 고쳐도 같은 결과가 됩니다.

pom.xml
-------

``pom.xml``\ 의 핵심은 다음 부분입니다.

.. code-block:: xml

    <artifactId>fess-ds-example</artifactId>
    <packaging>jar</packaging>
    <version>15.9.0-SNAPSHOT</version>

    <parent>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-parent</artifactId>
        <version>15.9.0</version>
        <relativePath />
    </parent>

    <dependencies>
        <dependency>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess</artifactId>
            <version>${fess.version}</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.opensearch</groupId>
            <artifactId>opensearch</artifactId>
            <version>${opensearch.version}</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

``fess-parent``\ 의 버전은 플러그인을 설치할 Fess의 버전에 맞춥니다.
``fess-parent`` 15.9.0에서는 ``fess.version``\ 이 ``15.9.0``\ 이므로, Fess 15.9.0의 API로 컴파일됩니다.
Fess 본체와 OpenSearch의 클래스는 실행 시 Fess가 가지고 있으므로 ``provided``\ 로 합니다.
실제 ``pom.xml``\ 에는 이 밖의 의존 관계와 빌드 설정도 있으므로, 우선은 그대로 사용하십시오.
``fess`` jar는 Maven Central이 아니라 ``fess-parent``\ 가 선언한 CodeLibs 리포지토리(``https://maven.codelibs.org/release/``)에서 가져옵니다.
프록시나 미러를 사용하는 환경에서는 이 리포지토리에 접근할 수 있도록 해 둡니다.

자신의 플러그인으로 만들 때는 ``artifactId``\ 를 반드시 ``fess-ds-``\ 로 시작합니다.
뒤에서 설명하듯이, 관리 화면의 "핸들러 이름" 후보는 파일 이름이 ``fess-ds``\ 로 시작하는 jar에서만 수집됩니다.

데이터 저장소 클래스
--------------------

데이터 저장소는 ``org.codelibs.fess.ds.AbstractDataStore``\ 를 상속하고 ``getName()``\ 과 ``storeData(...)``\ 를 구현합니다.
다음은 ``ExampleDataStore``\ 에서 처리의 골격만 남긴 것입니다.
이것은 구조를 이해하기 위한 것이며, 빌드에는 리포지토리의 ``ExampleDataStore``\ 를 그대로 사용합니다(테스트가 골격에 없는 메서드를 사용하므로, 바꿔 넣으면 테스트 컴파일이 통과하지 않습니다).

.. code-block:: java

    package org.codelibs.fess.ds.example;

    import java.util.HashMap;
    import java.util.LinkedHashMap;
    import java.util.Map;

    import org.codelibs.fess.ds.AbstractDataStore;
    import org.codelibs.fess.ds.callback.IndexUpdateCallback;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.opensearch.config.exentity.DataConfig;

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        protected String getName() {
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback, final DataStoreParams paramMap,
                final Map<String, String> scriptMap, final Map<String, Object> defaultDataMap) {
            final String scriptType = getScriptType(paramMap);
            final int dataSize = Integer.parseInt(paramMap.getAsString("data.size", "10"));

            for (int i = 0; i < dataSize && alive; i++) {
                // 외부 시스템에서 가져온 레코드 1건(여기서는 고정값)
                final Map<String, Object> source = new HashMap<>();
                source.put("title", "Sample " + i);
                source.put("body", "Sample body text for record " + i);
                source.put("url", "http://fess.codelibs.org/?sample=" + i);

                // 스크립트는 "파라미터 + 레코드"에 대해 평가된다
                final Map<String, Object> resultMap = new LinkedHashMap<>(paramMap.asMap());
                resultMap.putAll(source);

                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);
                for (final Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    final Object value = convertValue(scriptType, entry.getValue(), resultMap);
                    if (value != null) {
                        dataMap.put(entry.getKey(), value);
                    }
                }
                callback.store(paramMap, dataMap);
            }
        }
    }

각 부분의 역할은 다음과 같습니다.

- ``getName()``\ 의 반환값이 이 데이터 저장소의 이름으로 ``DataStoreFactory``\ 에 등록됩니다. 클래스의 단순 이름을 반환하는 것이 관례입니다
- ``paramMap``\ 에는 데이터 저장소 설정의 "파라미터" 칸의 값이 들어 있습니다. ``getAsString(키, 기본값)``\ 으로 꺼냅니다
- ``scriptMap``\ 은 "스크립트" 칸의 ``필드명=식`` 각 줄입니다. ``convertValue()``\ 가 식을 평가하고, 그 결과를 인덱스의 필드에 넣습니다
- ``defaultDataMap``\ 에는 설정 ID, 권한(역할), 부스트 값, 가상 호스트 등 데이터 저장소 설정에서 정해지는 값이 들어 있습니다. 이것을 복사한 다음 각 필드를 추가합니다
- ``callback.store()``\ 로 1건씩 등록합니다. ``alive``\ 는 작업이 중지되면 ``false``\ 가 되므로, 루프 조건에 넣어 둡니다

즉, 어떤 레코드의 값을 어떤 필드에 넣을지는 플러그인에 쓰지 않고, 관리자가 "스크립트" 칸에서 정합니다.
플러그인의 역할은 레코드를 가져와 ``resultMap``\ 에 늘어놓는 것입니다.

실제 ``ExampleDataStore``\ 는 이 밖에 레코드 단위의 예외 처리([장애 URL]에 기록)와 크롤링 통계(``CrawlerStatsHelper``)를 구현하고 있습니다.
자신의 플러그인을 만들 때는 이 골격이 아니라 ``ExampleDataStore``\ 를 복사하고, ``// CUSTOMIZE:``\ 라고 적힌 곳(레코드를 가져오는 부분)을 고쳐 쓰십시오.

DI 설정 파일
------------

클래스를 만들기만 해서는 Fess에 읽혀 들어가지 않습니다.
``src/main/resources/fess_ds++.xml``\ 에 컴포넌트로 등록합니다.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

DI 컨테이너(Lasta Di)는 클래스패스상의 ``fess_ds++.xml``\ 을 Fess 본체의 ``fess_ds.xml``\ 에 포함합니다.
``<postConstruct name="register">``\ 에 의해 생성 후 ``AbstractDataStore.register()``\ 가 호출되어, ``getName()``\ 의 이름으로 등록됩니다.
클래스 이름이나 패키지를 바꾸면 ``class`` 속성도 맞춰서 바꿉니다.

빌드하기
--------

::

    $ mvn clean package

``target/``\ 에 jar 3개가 만들어집니다.
Fess에 넣는 것은 ``-sources``\ 나 ``-javadoc``\ 이 붙지 않은 ``fess-ds-example-15.9.0-SNAPSHOT.jar``\ 입니다.
안에 ``fess_ds++.xml``\ 과 ``ExampleDataStore.class``\ 가 들어 있는지는 ``unzip -l``\ 로 확인할 수 있습니다.

설치하기
========

관리 화면에서 설치하는 것이 간편합니다.

1. [시스템] > [플러그인]에서 [설치]를 클릭합니다
2. [원격] 탭의 드롭다운은 첫 항목인 ``-`` 그대로 둡니다. 다른 플러그인을 선택해 두면 그 플러그인이 설치됩니다
3. [로컬] 탭의 "Jar 파일"에서 빌드한 jar를 선택하고 [설치]를 클릭합니다
4. Fess를 재시작합니다

업로드한 jar는 ``app/WEB-INF/plugin/``\ 에 ``<이름>-<버전>.jar`` 형태로 저장됩니다.
파일 이름에서 이름과 버전을 읽어 들이므로, Maven이 붙인 파일 이름을 바꾸지 말고 업로드하십시오.
관리 화면을 사용하지 않고 jar를 이 디렉터리에 직접 복사한 뒤 재시작해도 같습니다(Docker 이미지에서는 ``/usr/share/fess/app/WEB-INF/plugin/``).

Docker의 경우 ``FESS_PLUGINS``\ 는 리포지토리에 공개된 플러그인을 가져오는 구조이므로, 직접 만든 jar에는 사용할 수 없습니다.
관리 화면에서 설치한 다음 ``docker compose -f compose.yaml -f compose-opensearch3.yaml restart fess01``\ 로 재시작합니다.
jar는 컨테이너 안에 놓이므로, ``down``\ 과 ``up``\ 으로 컨테이너를 다시 만들면 사라집니다.
그 경우에는 다시 설치하십시오.

동작 확인하기
=============

핸들러 이름 확인하기
--------------------

재시작 후 [크롤러] > [데이터 저장소] > [새로 만들기]를 열고, "핸들러 이름" 드롭다운에 ``ExampleDataStore``\ 가 있는지 확인합니다.
이 후보는 ``app/WEB-INF/plugin/``\ 에 있는, 파일 이름이 ``fess-ds``\ 로 시작하는 jar로부터 만들어집니다.
jar 안의 ``fess_ds++.xml``\ 을 읽어, ``class`` 속성에 적힌 클래스의 단순 이름을 후보로 삼습니다(60초 동안 캐시됩니다).
표시되지 않으면 jar 파일 이름, jar 안의 ``fess_ds++.xml``, 재시작했는지 여부를 확인하십시오.

데이터 저장소 설정 만들기
-------------------------

같은 화면에서 다음과 같이 입력하고 [작성]을 클릭합니다.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 항목
     - 값
   * - 이름
     - ``Example``
   * - 핸들러 이름
     - ``ExampleDataStore``
   * - 파라미터
     - 미리 입력되어 있는 ``script_type=javascript`` 다음 줄에 ``data.size=5``\ 를 추가
   * - 스크립트
     - ``title=title``, ``content=body``, ``url=url``\ 의 3줄

스크립트의 우변이 레코드의 키(``title``, ``body``, ``url``)와 일치하면, ``convertValue()``\ 는 스크립트 엔진을 사용하지 않고 그 값을 그대로 반환합니다.
``content=title + " " + body``\ 와 같은 식을 쓰면 ``script_type``\ 에서 지정한 엔진으로 평가됩니다.
``script_type``\ 을 지우면 ``groovy``\ 로 취급되어, ``fess-script-groovy``\ 가 설치되지 않은 환경에서는 식 평가에 실패하므로 지우지 말고 남겨 두십시오.

``url``\ 은 필수입니다.
``callback.store()``\ 는 ``url``\ 이 없는 문서를 받아들이지 않고 예외를 던집니다.

작업 실행하기
-------------

1. [크롤러] > [데이터 저장소] 목록에서 ``Example``\ 을 클릭하고 [새 작업 작성]을 클릭합니다
2. 스케줄러 작성 화면이 열리면 그대로 [작성]을 클릭합니다
3. [시스템] > [스케줄러]에서 작성한 작업을 열고 [지금 시작]을 클릭합니다

결과 확인하기
-------------

다음 4가지를 확인합니다.

1. [시스템 정보] > [작업 로그]에서 작업 상태가 "OK"로 되어 있다
2. [시스템 정보] > [크롤링 정보]에서 해당 세션의 "인덱스 크기 (데이터 저장소)"가 ``5``\ 로 되어 있다
3. [시스템 정보] > [장애 URL]에 기록이 없다
4. [시스템 정보] > [검색]에서 ``Sample``\ 을 검색하면 ``Sample 0``\ 부터 ``Sample 4``\ 까지 5건이 표시된다

작업 상태가 "OK"여도 데이터 저장소 처리가 성공했다고는 할 수 없습니다.
예를 들어 스크립트에서 ``url=url``\ 을 지우고 실행하면, ``callback.store()``\ 가 모든 레코드에서 예외를 던져 등록은 0건이 됩니다.
``ExampleDataStore``\ 는 레코드 단위로 예외를 잡으므로 [장애 URL]에 ``record:0``\ 부터 ``record:4``\ 까지 기록되고 ``fess-crawler.log``\ 에 WARN이 나오지만, 작업 로그는 "OK" 그대로입니다.
골격처럼 예외를 잡지 않는 코드에서는 설정 전체가 실패하고, [장애 URL]에 ``D<설정ID>:Example`` 형태로 1건만 기록됩니다.
확인 절차와 로그 위치는 :doc:`datastore-basics`\ 의 결과 확인에 관한 절에 정리되어 있습니다.

여기까지 확인했다면 ``createSourceRecord()`` 등 레코드를 가져오는 부분을 실제 API나 파일을 읽는 처리로 바꿔 나갑니다.
외부 시스템의 접속 대상이나 인증 정보는 코드에 쓰지 말고, "파라미터" 칸에서 ``paramMap``\ 으로 받도록 합니다.

템플릿의 ``src/test``\ 에는 UTFlute의 ``LastaDiTestCase``\ 를 사용한 테스트가 있습니다.
``IndexUpdateCallback``\ 을 구현한 테스트용 클래스로 ``store()``\ 에 전달된 ``dataMap``\ 을 모아, 건수와 필드 값을 확인합니다.
그래서 OpenSearch 없이 ``mvn test``\ 를 실행할 수 있습니다.
레코드를 가져오는 부분을 고쳐 쓰면 이 테스트도 함께 고치십시오.

Ingester로 등록 전 문서 가공하기
================================

Ingester는 데이터 저장소, 웹, 파일 시스템 중 어떤 크롤링에서든 문서를 인덱스로 보내기 직전에 호출됩니다.
모든 문서에 공통 필드를 추가하거나 값을 정규화하는 등의 처리에 사용합니다.
설정별로 활성화·비활성화를 전환하는 구조는 없으며, 설치하면 모든 크롤링에 적용됩니다.

``org.codelibs.fess.ingest.Ingester``\ 를 상속하고, 필요한 ``process`` 메서드만 오버라이드합니다.

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - 메서드
     - 호출되는 시점
   * - ``process(Map<String, Object> target, DataStoreParams params)``
     - 데이터 저장소 크롤링(``callback.store()`` 내부)
   * - ``process(Map<String, Object> target, AccessResult<String> accessResult)``
     - 웹·파일 크롤링의 인덱스 등록 시
   * - ``process(ResultData target, ResponseData responseData)``
     - 웹·파일 크롤링에서 가져온 응답을 처리할 때
   * - ``protected process(Map<String, Object> target)``
     - 위의 두 ``Map`` 버전이 기본으로 호출하는 메서드. 데이터 저장소와 웹·파일 양쪽에 적용하고 싶을 때는 이것만 오버라이드한다

다음은 ``fess-ingest-example``\ 의 ``ExampleIngester``\ 에서 데이터 저장소용 처리만 남긴 것입니다.

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import java.util.Map;

    import org.apache.logging.log4j.LogManager;
    import org.apache.logging.log4j.Logger;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.ingest.Ingester;

    public class ExampleIngester extends Ingester {
        private static final Logger logger = LogManager.getLogger(ExampleIngester.class);

        public ExampleIngester() {
            setPriority(50);
        }

        @Override
        public Map<String, Object> process(final Map<String, Object> target, final DataStoreParams params) {
            target.put("ingested_by", ExampleIngester.class.getSimpleName());
            logger.info("DATASTORE CRAWL: {}", target);
            return target;
        }
    }

등록은 ``src/main/resources/fess_ingest++.xml``\ 에서 합니다.
내용은 ``fess_ds++.xml``\ 과 같은 형태로, ``exampleIngester``\ 라는 이름의 컴포넌트에 ``<postConstruct name="register">``\ 를 붙입니다.
``Ingester.register()``\ 가 ``IngestFactory``\ 에 자기 자신을 추가합니다.

템플릿 가져오기, 빌드, 설치, 재시작은 데이터 저장소와 같은 절차입니다(15.9용 커밋은 ``8a1e45ddb63a118802287120effd3ce49fb60bfb``, jar는 ``fess-ingest-example-15.9.0-SNAPSHOT.jar``).
자신의 플러그인에서는 artifactId를 ``fess-ingest-``\ 로 시작합니다.

구현할 때는 다음 사항에 주의하십시오.

- ``target``\ 은 변경한 다음 반드시 반환합니다. 반환값은 다음 Ingester와 인덱서에 그대로 전달되며, ``null`` 검사는 없습니다. ``null``\ 을 반환해도 문서는 제외되지 않고, 등록 처리가 깨집니다
- 여러 Ingester는 ``priority``\ 가 작은 순서로 실행됩니다(기본값은 99). 앞의 Ingester가 변경한 ``target``\ 을 다음 Ingester가 받습니다
- ``process``\ 에서 예외가 발생하면 Fess는 WARN을 로그에 출력하고 다음 Ingester로 넘어갑니다. 문서 등록은 멈추지 않습니다. 예외 전에 ``target``\ 에 가한 변경은 그대로 남습니다

동작은 위의 "동작 확인하기"에서 만든 데이터 저장소 설정의 작업을 한 번 더 실행하여 확인합니다.
Ingester는 크롤러 프로세스에서 동작하므로, ``fess-crawler.log``\ 에 ``DATASTORE CRAWL:`` 줄이 문서마다 출력되어 있으면 호출되고 있는 것입니다.
리포지토리의 ``ExampleIngester``\ 는 웹·파일 크롤링의 문서도 ``WEB/FILE CRAWL:``\ 로 1건씩 로그에 출력합니다.
모든 크롤링에 적용되므로, 확인이 끝나면 [시스템] > [플러그인]에서 삭제하고 Fess를 재시작하십시오.

Fess를 업그레이드할 때
======================

플러그인은 설치할 Fess와 같은 마이너 버전의 ``fess-parent``\ 로 빌드합니다(Fess 15.9라면 15.9.x).
공개된 플러그인도 Fess의 마이너 버전마다 대응하는 버전이 릴리스되어 있습니다.

Fess를 15.10으로 올릴 때는 ``pom.xml``\ 의 ``fess-parent`` 버전을 맞춰 다시 빌드합니다.
[시스템] > [플러그인] 목록에서 이전 jar를 삭제하고, 새 jar를 설치한 뒤 재시작합니다.
``bin/fess-setup upgrade plugins``\ 는 새 버전을 플러그인 리포지토리에서 가져오는 구조이므로, 리포지토리에 없는 직접 만든 플러그인은 이 방법으로 업데이트할 수 없습니다.

다음에 읽을 글
==============

- 데이터 저장소 설정의 파라미터, 스크립트, 권한, 스케줄을 자세히 알고 싶다: :doc:`datastore-basics`
- 공개된 데이터 저장소 플러그인의 설정 예를 보고 싶다: :doc:`guide-06`, :doc:`guide-07`, :doc:`guide-12`
- 검색 화면의 겉모습을 바꾸고 싶다: :doc:`guide-03`
- LLM 플러그인을 사용하여 AI 검색 모드를 활성화하고 싶다: :doc:`guide-19`
- 웹 애플리케이션 플러그인(MCP 서버)을 사용하고 싶다: :doc:`guide-20`

참고 자료
=========

- `플러그인 아키텍처 <https://fess.codelibs.org/ko/stable/dev/plugin-architecture.html>`__
- `데이터스토어 플러그인 개발 <https://fess.codelibs.org/ko/stable/dev/datastore-plugin.html>`__
- `Ingest 플러그인 <https://fess.codelibs.org/ko/stable/dev/ingest-plugin.html>`__
- `테마 개발 가이드 <https://fess.codelibs.org/ko/stable/dev/theme-development.html>`__
- `플러그인(관리 화면) <https://fess.codelibs.org/ko/stable/admin/plugin-guide.html>`__
- `fess-ds-example(GitHub) <https://github.com/codelibs/fess-ds-example>`__
- `fess-ingest-example(GitHub) <https://github.com/codelibs/fess-ingest-example>`__
