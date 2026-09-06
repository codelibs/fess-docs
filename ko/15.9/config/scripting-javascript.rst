==================================
JavaScript 스크립트 가이드
==================================

개요
====

JavaScript는 |Fess| 15.9 이후의 기본 스크립트 언어입니다.
|Fess|\ 가 DI XML 식 판정에도 사용하고 있는, CodeLibs의 Nashorn 포크인 Sai 위에서
동작하며, 스크립트는 ECMAScript 6로 실행됩니다. 식별자는 ``javascript``\ 이며,
``js`` 및 ``sai``\ 라는 별칭으로도 지정할 수 있습니다.

.. _javascript-statement-null:

스크립트 평가 방식
==================

|Fess|\ 의 스크립트 엔진은 스크립트 문자열을 먼저 하나의 「식」으로
컴파일하려고 시도하고, 그것이 구문 오류가 될 경우에만 「문（스테이트먼트）」
블록으로 다시 컴파일합니다.

이 때문에 값을 반환하기만 하는 단순한 식:

::

    content.length()

과, 최상위 레벨에 ``return`` 문을 포함하는 스크립트:

::

    return container.getComponent("crawlJob").execute();

는 모두 문제없이 동작합니다. 후자는 일반적인 JavaScript로는 최상위 레벨의
``return``\ 이 구문 오류가 되지만, 식으로서의 컴파일에 실패하기 때문에 문
블록으로 다시 해석되어 유효한 스크립트로 실행됩니다.

데이터 스토어 스크립트처럼 한 줄이 하나의 식으로 취급되는 경우에는 여러 문으로
구성된 스크립트를 사용할 수 없습니다. 반면 스케줄 작업처럼 스크립트 전체가
평가되는 경우에는 여러 줄의 문이나 ``let`` / ``const``\ 의 변수 선언, 제어
구문을 자유롭게 사용할 수 있습니다.

.. warning::

   문 블록으로 컴파일된 스크립트가 값을 반환하는 것은 명시적인 ``return`` 을 포함하는 경우
   뿐입니다. 스크립트 문자열을 식으로 해석할 수 없는 경우 그 문자열은 함수로 감싸져 문
   블록으로 실행되는데, ``return`` 이 없는 블록의 평가 결과는 ``null`` 이 됩니다.
   끝에 세미콜론을 하나 붙이는 것만으로 이 경계를 넘습니다.

   .. list-table::
      :header-rows: 1
      :widths: 40 15 45

      * - 스크립트
        - 결과
        - 이유
      * - ``content.length()``
        - ``11``
        - 식으로 해석되며, 식의 값이 그대로 결과가 됩니다
      * - ``content.length();``
        - ``null``
        - 문 블록으로만 해석되며, ``return`` 이 없습니다
      * - ``var x = 1; x + 2``
        - ``null``
        - 문 블록으로만 해석되며, ``return`` 이 없습니다

   Groovy에서는 마지막으로 평가된 문의 값이 스크립트의 반환값이 되기 때문에 위 세 가지 모두
   값을 반환했습니다. JavaScript에는 이러한 규칙이 없습니다.

   이는 이행 과정에서 오류도 로그도 남지 않고, 필드가 조용히 비는 것 외에는 아무런 증상도
   나타나지 않는 유일한 차이입니다. 스크립트가 ``null`` 을 반환한 데이터 스토어 매핑은 해당
   필드를 단순히 설정하지 않습니다. 데이터 스토어의 ``필드명=식`` 각 행은 끝에 세미콜론을
   붙이지 않은 식으로 작성하고, 스케줄 작업 스크립트에는 반드시 명시적인 ``return`` 을
   작성하십시오.

기본 구문
=========

아래에서 끝에 세미콜론이 붙어 있지 않은 행은 **식** 이며, 데이터 스토어의 ``필드명=식``
행을 포함해 어디에서든 사용할 수 있습니다. ``let`` / ``const`` 선언, ``if`` 블록, 반복문은
**문** 이며, 스케줄 작업처럼 스크립트 전체가 평가되는 경우에만 사용할 수 있습니다. 그 경우에도
값을 반환하려면 명시적인 ``return`` 이 필요합니다. 위의 "스크립트 평가 방식" 을 참조하세요.

변수 선언
---------

::

    // let（재대입 가능한 변수）
    let name = "Fess";
    let count = 100;

    // const（재대입 불가능한 상수）
    const title = "Document Title";
    const pageNum = 1;

문자열 조작
-----------

::

    // 템플릿 리터럴（ES6）
    const id = 123;
    const url = `https://example.com/doc/${id}`;

    // 여러 줄 문자열（템플릿 리터럴）
    const content = `
    This is a
    multi-line string
    `;

    // 치환（정규 표현식 사용. ECMAScript 6에는 String#replaceAll이 없습니다）
    title.replace(/old/g, "new")
    title.replace(/\s+/g, " ")  // 연속된 공백을 하나로 합침

    // 분할/결합
    const tags = "tag1,tag2,tag3".split(",");
    const joined = tags.join(", ");

    // 대문자/소문자 변환
    title.toUpperCase()
    title.toLowerCase()

컬렉션 조작
-----------

::

    // 배열
    const list = [1, 2, 3, 4, 5];
    const doubled = list.map(item => item * 2);
    const filtered = list.filter(item => item > 3);
    const total = list.reduce((sum, item) => sum + item, 0);

    // 객체
    const map = { name: "Fess", version: "15.9" };
    map.name
    map["version"]

조건 분기
---------

::

    // if-else
    if (data.status === "active") {
        return "활성화";
    } else {
        return "비활성화";
    }

    // 삼항 연산자
    data.count > 0 ? "있음" : "없음"

    // 기본값（논리 OR 연산자. JavaScript에는 Elvis 연산자가 없습니다）
    data.title || "무제"

    // 옵셔널 체이닝（?.）은 ES2020 구문으로 ES6에서는 사용할 수 없습니다.
    // 대신 명시적으로 null을 확인하세요.
    (data.content != null) ? data.content.length() : 0

반복 처리
---------

::

    // for...of（ES6）
    for (const item of items) {
        // 각 요소에 대한 처리
    }

    // forEach（화살표 함수）
    items.forEach(item => {
        // 각 요소에 대한 처리
    });

    // 범위를 다룰 때는 배열을 생성하거나 for문을 사용합니다
    // （JavaScript에는 Groovy의 범위 표현식이 없습니다）
    for (let i = 1; i <= 10; i++) {
        // ...
    }

데이터 스토어 스크립트
======================

데이터 스토어 설정에서의 스크립트 예입니다.

.. note::
   데이터 스토어 스크립트에서는 ``필드명=식`` 의 각 행이 각각 독립된 하나의 식으로 평가됩니다.
   따라서 ``let`` / ``const``\ 에 의한 변수 선언문이나, 여러 필드를 한꺼번에 설정하는 복수 행의 제어 구문( ``if`` 블록 등)은 사용할 수 없습니다.
   Java 클래스를 이용하는 경우에는 완전 정규화 클래스명(FQCN)을 사용하여 하나의 식으로 기술하고, 조건 분기는 필드별로 삼항 연산자로 기술합니다(예: ``url=data.published ? data.url : null`` ).
   또한 여기서 사용하는 변수명 ``data`` 는 설명을 위한 예시이며, 실제 변수명은 사용하는 데이터 스토어 커넥터에 따라 다릅니다. 자세한 내용은 :doc:`../admin/dataconfig-guide` 를 참조하세요.
   식은 끝에 세미콜론을 붙이지 않고 작성하십시오. 문 블록으로만 해석할 수 있는 행의 평가 결과는 ``null`` 이 되어 해당 필드가 설정되지 않습니다. :ref:`javascript-statement-null` 을 참조하세요.

기본 매핑
---------

::

    url=data.url
    title=data.title
    content=data.content
    lastModified=data.updated_at

URL 생성
--------

::

    // ID 기반 URL 생성
    url="https://example.com/article/" + data.id

    // 여러 필드 조합
    url="https://example.com/" + data.category + "/" + data.slug + ".html"

    // 조건부 URL
    url=data.external_url || "https://example.com/default/" + data.id

콘텐츠 가공
-----------

::

    // HTML 태그 제거
    content=data.html_content.replace(/<[^>]+>/g, "")

    // 여러 필드 결합
    content=data.title + "\n" + data.description + "\n" + data.body

    // 길이 제한
    content=data.content.length() > 10000 ? data.content.substring(0, 10000) : data.content

날짜 처리
---------

::

    // 날짜 파싱（FQCN을 사용한 단일 식. Java 상호운용은 Groovy와 동일한 표기법을 사용）
    lastModified=new java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss").parse(data.date_string)

    // 에포크 초에서 변환（long 타입의 L 접미사는 필요 없음）
    lastModified=new Date(data.timestamp * 1000)

사용 가능한 객체
=================

스크립트 실행 컨텍스트에 따라 사용 가능한 객체가 다릅니다.

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - 컨텍스트
     - 객체
     - 설명
   * - 모든 컨텍스트
     - ``container``
     - DI 컨테이너. ``container.getComponent("...")`` 를 통해 컴포넌트에 접근할 때 사용
   * - 스케줄 작업
     - ``executor``
     - 작업 실행 제어 ( ``JobExecutor`` ). 작업 정지 지원에 필요
   * - 데이터 스토어
     - (커넥터별)
     - 각 데이터 스토어가 제공하는 데이터 레코드 변수. 변수명은 커넥터에 따라 다름
   * - 패스 매핑
     - ``url`` , ``matcher``
     - 변환 대상 URL 문자열과 정규표현식 매치 결과( ``Matcher`` ). 치환 문자열에 등록된 엔진명이 접두사로 붙은 경우( ``javascript:`` , 별칭 ``js:`` , ``sai:`` )에 이용 가능
   * - 문서 부스트
     - (문서 필드)
     - 대상 문서의 각 필드를 변수로 이용 가능(조건식·부스트값 식에서 사용)

스케줄 작업 스크립트
====================

스케줄 작업에서 사용하는 JavaScript 스크립트 예입니다.
스케줄 작업에서는 ``container`` 와 ``executor`` 를 사용할 수 있습니다.
``executor`` 를 작업의 ``execute()`` 메서드에 전달하면 작업 정지 제어가 활성화됩니다.

.. note::
   스케줄 작업 스크립트는 스크립트 전체가 하나의 완전한 스크립트로 평가됩니다.
   스크립트 엔진은 먼저 이를 식으로 컴파일하려고 시도하며, 실패한 경우에만 문（스테이트먼트） 블록으로 다시 해석하므로, 여러 줄의 문이나 ``let`` / ``const`` 선언, 제어 구문, 최상위 레벨의 ``return`` 문을 사용할 수 있습니다（자세한 내용은 위의 「스크립트 평가 방식」을 참조）.
   이후의 "Java 클래스 사용", "Fess 컴포넌트 접근", "오류 처리", "디버그와 로그 출력" 예시도 이 완전한 스크립트 컨텍스트를 전제로 합니다.

크롤 작업 실행
--------------

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

조건부 크롤링
-------------

::

    const cal = java.util.Calendar.getInstance();
    const hour = cal.get(java.util.Calendar.HOUR_OF_DAY);

    // 업무 시간 외에만 크롤링
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);
    }
    return "Skipped during business hours";

여러 작업을 순서대로 실행
--------------------------

::

    const results = [];

    // 서제스트 업데이트
    results.push(container.getComponent("suggestJob").logLevel("info").sessionId("SUGGEST").execute(executor));

    // 크롤 실행
    results.push(container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor));

    return results.join("\n");

Java 클래스 사용
================

JavaScript 스크립트 내에서는 Sai（Nashorn）의 Java 상호운용 메커니즘을 통해
Java 표준 라이브러리나 |Fess| 클래스를 직접 사용할 수 있습니다. JavaScript에는
``import`` 문이 없으므로, 클래스는 항상 완전 정규화 이름（FQCN）으로 기술합니다.

::

    new java.io.File("/var/log/fess/fess.log")
    java.lang.System.getProperty("user.home")
    new org.codelibs.fess.job.IndexExportJob()

날짜/시간
---------

::

    const now = java.time.LocalDateTime.now();
    const formatted = now.format(java.time.format.DateTimeFormatter.ISO_LOCAL_DATE_TIME);

파일 조작
---------

::

    const content = new java.lang.String(
        java.nio.file.Files.readAllBytes(java.nio.file.Paths.get("/path/to/file.txt")));

HTTP 통신
---------

::

    const client = java.net.http.HttpClient.newHttpClient();
    const request = java.net.http.HttpRequest.newBuilder()
        .uri(java.net.URI.create("https://api.example.com/data"))
        .build();
    const response = client.send(request, java.net.http.HttpResponse.BodyHandlers.ofString());
    const body = response.body();

.. warning::
   외부 리소스 접근은 성능에 영향을 미치므로
   필요 최소한으로 줄이세요.

Fess 컴포넌트 접근
==================

``container``\ 를 사용하여 Fess 컴포넌트에 접근할 수 있습니다.

시스템 헬퍼
-----------

::

    const systemHelper = container.getComponent("systemHelper");
    const currentTime = systemHelper.getCurrentTimeAsLong();

설정값 가져오기
----------------

::

    const fessConfig = container.getComponent("fessConfig");
    const indexName = fessConfig.getIndexDocumentUpdateIndex();

검색 실행
---------

::

    const searchHelper = container.getComponent("searchHelper");
    // 검색 파라미터를 설정하고 검색 실행

오류 처리
=========

JavaScript에는 ``import`` 문이 없으므로 Groovy와 같은 배치 제약이 없습니다.
``try-catch``\ 로 예외를 포착하여 작업의 오류를 제어할 수 있습니다.

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("script");

    try {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);
    } catch (e) {
        logger.error("Failed to execute crawl job: {}", e.getMessage(), e);
        return "Error: " + e.getMessage();
    }

디버그와 로그 출력
==================

로그 출력
---------

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("script");

    logger.debug("Debug message: {}", value);
    logger.info("Processing: {}", title);
    logger.warn("Warning: {}", message);
    logger.error("Error: {}", e.getMessage(), e);

디버그용 출력
-------------

변수의 내용을 빠르게 확인하고 싶을 때는 ``JSON.stringify``\ 로 문자열화하여
로그에 출력하면 편리합니다.

::

    logger.debug("data = {}", JSON.stringify({ id: data.id, title: data.title }));

Groovy에서 마이그레이션
========================

기존 Groovy 스크립트를 JavaScript로 이식할 때는 다음 차이점에 주의하세요.

산술 연산의 정밀도
-------------------

JavaScript의 숫자 연산은 항상 배정밀도 부동소수점으로 처리됩니다. 예를 들어
다음 식은 Groovy에서는 정수 ``34``\ 를 반환하지만, JavaScript에서는
부동소수점수 ``34.0``\ 을 반환합니다.

::

    10 * boost1 + boost2

반면 Java 상호운용으로 호출하는 메서드의 반환값은 Java 쪽 타입이 그대로
유지되므로, ``content.length()``\ 는 계속해서 정수를 반환합니다.

Groovy 전용 구문 재작성
------------------------

다음의 Groovy 전용 구문은 JavaScript에서는 재작성이 필요합니다.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Groovy
     - JavaScript
     - 설명
   * - ``1000L``
     - ``1000``
     - long 타입 리터럴의 ``L`` 접미사는 필요 없음（숫자 리터럴을 그대로 기술）
   * - ``["a", "b"] as String[]``
     - ``["a", "b"]``
     - JavaScript 배열은 ``String[]``\ 를 인수로 받는 메서드에 전달하면 자동으로
       Java 배열로 변환되므로 캐스트가 필요 없음

Java 상호운용
--------------

Java 상호운용 표기법 자체는 Nashorn과 동일하며, Groovy와 거의 다르지 않습니다.
``new java.io.File(...)``, ``java.lang.System.getProperty(...)``,
``new org.codelibs.fess.job.IndexExportJob()``\ 과 같은 완전 정규화 생성자
호출은 그대로 해석됩니다.

ES6 구문
--------

|Fess|\ 의 JavaScript 엔진은 ECMAScript 6로 동작하므로, ``let`` / ``const``,
화살표 함수, 템플릿 리터럴, 구조 분해 할당, ``for...of``, ``class`` 등의 ES6
구문을 사용할 수 있습니다. 다만 옵셔널 체이닝（ ``?.`` ）과 null 병합 연산자
（ ``??`` ）는 ES2020 이후의 구문이므로 사용할 수 없습니다.

모범 사례
=========

1. **단순하게 유지**: 복잡한 로직은 피하고 읽기 쉬운 코드 작성
2. **기본값**: Elvis 연산자 대신 논리 OR 연산자（ ``||`` ）를 활용
3. **예외 처리**: 적절한 try-catch로 예상치 못한 오류 대응
4. **로그 출력**: 디버깅하기 쉽도록 로그 출력
5. **성능**: 외부 리소스 접근 최소화
6. **숫자 연산**: 정수가 필요한 곳에서는 Java 상호운용 메서드 호출 결과를 그대로 사용하거나, 필요에 따라 명시적으로 변환

참고 정보
=========

- `MDN JavaScript 레퍼런스 <https://developer.mozilla.org/ko/docs/Web/JavaScript>`__
- :doc:`scripting-overview` - 스크립팅 개요
- :doc:`scripting-groovy` - Groovy 스크립트 가이드（플러그인）
- :doc:`../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- :doc:`../admin/scheduler-guide` - 스케줄러 설정 가이드
