==================================
Groovy 스크립트 가이드
==================================

개요
====

Groovy는 |Fess|의 기본 스크립트 언어입니다.
Java 가상 머신(JVM) 위에서 동작하며, Java와의 높은 호환성을 유지하면서
더 간결한 구문으로 스크립트를 작성할 수 있습니다.

기본 구문
========

변수 선언
--------

::

    // 타입 추론(def)
    def name = "Fess"
    def count = 100

    // 명시적 타입 지정
    String title = "Document Title"
    int pageNum = 1

문자열 조작
----------

::

    // 문자열 보간(GString)
    def id = 123
    def url = "https://example.com/doc/${id}"

    // 여러 줄 문자열
    def content = """
    This is a
    multi-line string
    """

    // 치환
    title.replace("old", "new")
    title.replaceAll(/\s+/, " ")  // 정규표현식

    // 분할/결합
    def tags = "tag1,tag2,tag3".split(",")
    def joined = tags.join(", ")

    // 대문자/소문자 변환
    title.toUpperCase()
    title.toLowerCase()

컬렉션 조작
----------------

::

    // 리스트
    def list = [1, 2, 3, 4, 5]
    list.each { println it }
    def doubled = list.collect { it * 2 }
    def filtered = list.findAll { it > 3 }

    // 맵
    def map = [name: "Fess", version: "15.5"]
    println map.name
    println map["version"]

조건 분기
--------

::

    // if-else
    if (data.status == "active") {
        return "활성화"
    } else {
        return "비활성화"
    }

    // 삼항 연산자
    def result = data.count > 0 ? "있음" : "없음"

    // 엘비스 연산자(null 병합 연산자)
    def value = data.title ?: "무제"

    // 안전 탐색 연산자
    def length = data.content?.length() ?: 0

반복 처리
----------

::

    // for-each
    for (item in items) {
        println item
    }

    // 클로저
    items.each { item ->
        println item
    }

    // 범위
    (1..10).each { println it }

데이터 스토어 스크립트
======================

데이터 스토어 설정에서의 스크립트 예입니다.

기본 매핑
------------------

::

    url=data.url
    title=data.title
    content=data.content
    lastModified=data.updated_at

URL 생성
---------

::

    // ID 기반 URL 생성
    url="https://example.com/article/" + data.id

    // 여러 필드 조합
    url="https://example.com/" + data.category + "/" + data.slug + ".html"

    // 조건부 URL
    url=data.external_url ?: "https://example.com/default/" + data.id

콘텐츠 가공
----------------

::

    // HTML 태그 제거
    content=data.html_content.replaceAll(/<[^>]+>/, "")

    // 여러 필드 결합
    content=data.title + "\n" + data.description + "\n" + data.body

    // 길이 제한
    content=data.content.length() > 10000 ? data.content.substring(0, 10000) : data.content

날짜 처리
----------

::

    // 날짜 파싱
    import java.text.SimpleDateFormat
    def sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss")
    lastModified=sdf.parse(data.date_string)

    // 에포크 초에서 변환
    lastModified=new Date(data.timestamp * 1000L)

스케줄 작업 스크립트
============================

스케줄 작업에서 사용하는 Groovy 스크립트 예입니다.

크롤 작업 실행
--------------------

::

    return container.getComponent("crawlJob").execute();

조건부 크롤링
----------------

::

    import java.util.Calendar

    def cal = Calendar.getInstance()
    def hour = cal.get(Calendar.HOUR_OF_DAY)

    // 업무 시간 외에만 크롤링
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").execute()
    }
    return "Skipped during business hours"

여러 작업을 순서대로 실행
------------------------

::

    def results = []

    // 인덱스 최적화
    results << container.getComponent("optimizeJob").execute()

    // 크롤 실행
    results << container.getComponent("crawlJob").execute()

    return results.join("\n")

Java 클래스 사용
================

Groovy 스크립트 내에서는 Java 표준 라이브러리나 Fess 클래스를 사용할 수 있습니다.

날짜/시간
----------

::

    import java.time.LocalDateTime
    import java.time.format.DateTimeFormatter

    def now = LocalDateTime.now()
    def formatted = now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)

파일 조작
------------

::

    import java.nio.file.Files
    import java.nio.file.Paths

    def content = new String(Files.readAllBytes(Paths.get("/path/to/file.txt")))

HTTP 통신
--------

::

    import java.net.URL

    def url = new URL("https://api.example.com/data")
    def response = url.text

.. warning::
   외부 리소스 접근은 성능에 영향을 미치므로
   필요 최소한으로 줄이세요.

Fess 컴포넌트 접근
==============================

``container``를 사용하여 Fess 컴포넌트에 접근할 수 있습니다.

시스템 헬퍼
----------------

::

    def systemHelper = container.getComponent("systemHelper")
    def currentTime = systemHelper.getCurrentTimeAsLong()

설정값 가져오기
------------

::

    def fessConfig = container.getComponent("fessConfig")
    def indexName = fessConfig.getIndexDocumentUpdateIndex()

검색 실행
----------

::

    def searchHelper = container.getComponent("searchHelper")
    // 검색 파라미터를 설정하고 검색 실행

오류 처리
==================

::

    try {
        def result = processData(data)
        return result
    } catch (Exception e) {
        import org.apache.logging.log4j.LogManager
        def logger = LogManager.getLogger("script")
        logger.error("Error processing data: {}", e.message, e)
        return "Error: " + e.message
    }

디버그와 로그 출력
==================

로그 출력
--------

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("script")

    logger.debug("Debug message: {}", data.id)
    logger.info("Processing document: {}", data.title)
    logger.warn("Warning: {}", message)
    logger.error("Error: {}", e.message)

디버그용 출력
----------------

::

    // 콘솔 출력(개발 시에만)
    println "data.id = ${data.id}"
    println "data.title = ${data.title}"

모범 사례
==================

1. **단순하게 유지**: 복잡한 로직은 피하고 읽기 쉬운 코드 작성
2. **null 체크**: ``?.`` 연산자나 ``?:`` 연산자 활용
3. **예외 처리**: 적절한 try-catch로 예상치 못한 오류 대응
4. **로그 출력**: 디버깅하기 쉽도록 로그 출력
5. **성능**: 외부 리소스 접근 최소화

참고 정보
========

- `Groovy 공식 문서 <https://groovy-lang.org/documentation.html>`__
- :doc:`scripting-overview` - 스크립팅 개요
- :doc:`../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- :doc:`../admin/scheduler-guide` - 스케줄러 설정 가이드
