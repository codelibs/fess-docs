========================
크롤러 고급 설정
========================

개요
====

본 가이드에서는 |Fess| 크롤러의 고급 설정에 대해 설명합니다.
기본적인 크롤러 설정에 대해서는 :doc:`crawler-basic` 을 참조하십시오.

.. warning::
   본 페이지의 설정은 시스템 전체에 영향을 미칠 수 있습니다.
   설정을 변경할 때는 충분히 테스트를 수행한 후 운영 환경에 적용하십시오.

전반 설정
========

설정 파일 위치
------------------

크롤러의 상세 설정은 다음 파일에서 수행합니다.

- **메인 설정**: ``/etc/fess/fess_config.properties`` (또는 ``app/WEB-INF/classes/fess_config.properties``)
- **콘텐츠 길이 설정**: ``app/WEB-INF/classes/crawler/contentlength.xml``
- **컴포넌트 설정**: ``app/WEB-INF/classes/crawler/container.xml``

기본 스크립트
--------------------

크롤러의 기본 스크립트 언어를 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.default.script``
     - 크롤러 스크립트 언어
     - ``groovy``

::

    crawler.default.script=groovy

HTTP 스레드 풀
------------------

HTTP 크롤러의 스레드 풀 설정입니다.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.http.thread_pool.size``
     - HTTP 스레드 풀 크기
     - ``0``

::

    # 0일 경우 자동 설정
    crawler.http.thread_pool.size=0

문서 처리 설정
====================

기본 설정
--------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.document.max.site.length``
     - 문서 사이트의 최대 행 수
     - ``100``
   * - ``crawler.document.site.encoding``
     - 문서 사이트의 인코딩
     - ``UTF-8``
   * - ``crawler.document.unknown.hostname``
     - 알 수 없는 호스트명의 대체 값
     - ``unknown``
   * - ``crawler.document.use.site.encoding.on.english``
     - 영어 문서에서 사이트 인코딩 사용
     - ``false``
   * - ``crawler.document.append.data``
     - 문서에 데이터 추가
     - ``true``
   * - ``crawler.document.append.filename``
     - 파일명을 문서에 추가
     - ``false``

설정 예
~~~~~~

::

    crawler.document.max.site.length=100
    crawler.document.site.encoding=UTF-8
    crawler.document.unknown.hostname=unknown
    crawler.document.use.site.encoding.on.english=false
    crawler.document.append.data=true
    crawler.document.append.filename=false

단어 처리 설정
------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.document.max.alphanum.term.size``
     - 영숫자 단어의 최대 길이
     - ``20``
   * - ``crawler.document.max.symbol.term.size``
     - 기호 단어의 최대 길이
     - ``10``
   * - ``crawler.document.duplicate.term.removed``
     - 중복 단어 제거
     - ``false``

설정 예
~~~~~~

::

    # 영숫자 최대 길이를 50자로 변경
    crawler.document.max.alphanum.term.size=50

    # 기호 최대 길이를 20자로 변경
    crawler.document.max.symbol.term.size=20

    # 중복 단어 제거
    crawler.document.duplicate.term.removed=true

.. note::
   ``max.alphanum.term.size`` 를 크게 하면 긴 ID, 토큰, URL 등을
   완전한 형태로 인덱싱할 수 있지만 인덱스 크기가 증가합니다.

문자 처리 설정
------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.document.space.chars``
     - 공백 문자 정의
     - ``\u0009\u000A...``
   * - ``crawler.document.fullstop.chars``
     - 마침표 문자 정의
     - ``\u002e\u06d4...``

설정 예
~~~~~~

::

    # 기본값(유니코드 문자 포함)
    crawler.document.space.chars=\u0009\u000A\u000B\u000C\u000D\u001C\u001D\u001E\u001F\u0020\u00A0\u1680\u180E\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u200B\u200C\u202F\u205F\u3000\uFEFF\uFFFD\u00B6

    crawler.document.fullstop.chars=\u002e\u06d4\u2e3c\u3002

프로토콜 설정
==============

지원 프로토콜
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.web.protocols``
     - 웹 크롤링 프로토콜
     - ``http,https``
   * - ``crawler.file.protocols``
     - 파일 크롤링 프로토콜
     - ``file,smb,smb1,ftp,storage``

설정 예
~~~~~~

::

    crawler.web.protocols=http,https
    crawler.file.protocols=file,smb,smb1,ftp,storage

환경 변수 파라미터
--------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.data.env.param.key.pattern``
     - 환경 변수 파라미터 키 패턴
     - ``^FESS_ENV_.*``

::

    # FESS_ENV_로 시작하는 환경 변수를 크롤 설정에서 사용 가능
    crawler.data.env.param.key.pattern=^FESS_ENV_.*

robots.txt 설정
===============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.ignore.robots.txt``
     - robots.txt 무시
     - ``false``
   * - ``crawler.ignore.robots.tags``
     - 무시할 robots 태그
     - (빈 값)
   * - ``crawler.ignore.content.exception``
     - 콘텐츠 예외 무시
     - ``true``

설정 예
~~~~~~

::

    # robots.txt 무시(권장하지 않음)
    crawler.ignore.robots.txt=false

    # 특정 robots 태그 무시
    crawler.ignore.robots.tags=

    # 콘텐츠 예외 무시
    crawler.ignore.content.exception=true

.. warning::
   ``crawler.ignore.robots.txt=true`` 로 설정하면 사이트의 이용 약관을
   위반할 수 있습니다. 외부 사이트를 크롤링할 때는 주의하십시오.

오류 처리 설정
==============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.failure.url.status.codes``
     - 실패로 간주할 HTTP 상태 코드
     - ``404``

설정 예
~~~~~~

::

    # 404에 더해 403도 오류로 처리
    crawler.failure.url.status.codes=404,403

시스템 모니터링 설정
================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.system.monitor.interval``
     - 시스템 모니터링 간격(초)
     - ``60``

::

    # 30초마다 시스템 모니터링
    crawler.system.monitor.interval=30

핫 스레드 설정
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.hotthread.ignore_idle_threads``
     - 유휴 스레드 무시
     - ``true``
   * - ``crawler.hotthread.interval``
     - 스냅샷 간격
     - ``500ms``
   * - ``crawler.hotthread.snapshots``
     - 스냅샷 수
     - ``10``
   * - ``crawler.hotthread.threads``
     - 모니터링 스레드 수
     - ``3``
   * - ``crawler.hotthread.timeout``
     - 타임아웃
     - ``30s``
   * - ``crawler.hotthread.type``
     - 모니터링 유형
     - ``cpu``

설정 예
~~~~~~

::

    crawler.hotthread.ignore_idle_threads=true
    crawler.hotthread.interval=500ms
    crawler.hotthread.snapshots=10
    crawler.hotthread.threads=3
    crawler.hotthread.timeout=30s
    crawler.hotthread.type=cpu

메타데이터 설정
==============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.metadata.content.excludes``
     - 제외할 메타데이터
     - ``resourceName,X-Parsed-By...``
   * - ``crawler.metadata.name.mapping``
     - 메타데이터 이름 매핑
     - ``title=title:string...``

설정 예
~~~~~~

::

    # 제외할 메타데이터
    crawler.metadata.content.excludes=resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*

    # 메타데이터 이름 매핑
    crawler.metadata.name.mapping=\
        title=title:string\n\
        Title=title:string\n\
        dc:title=title:string

HTML 크롤러 설정
===================

XPath 설정
----------

HTML 요소를 추출하기 위한 XPath 설정입니다.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.document.html.content.xpath``
     - 콘텐츠 XPath
     - ``//BODY``
   * - ``crawler.document.html.lang.xpath``
     - 언어 XPath
     - ``//HTML/@lang``
   * - ``crawler.document.html.digest.xpath``
     - 다이제스트 XPath
     - ``//META[@name='description']/@content``
   * - ``crawler.document.html.canonical.xpath``
     - 표준 URL XPath
     - ``//LINK[@rel='canonical'][1]/@href``

설정 예
~~~~~~

::

    # 기본 설정
    crawler.document.html.content.xpath=//BODY
    crawler.document.html.lang.xpath=//HTML/@lang
    crawler.document.html.digest.xpath=//META[@name='description']/@content
    crawler.document.html.canonical.xpath=//LINK[@rel='canonical'][1]/@href

사용자 정의 XPath 예
~~~~~~~~~~~~~~~~~~~

::

    # 특정 div 요소만 콘텐츠로 추출
    crawler.document.html.content.xpath=//DIV[@id='main-content']

    # meta keywords도 다이제스트에 포함
    crawler.document.html.digest.xpath=//META[@name='description']/@content|//META[@name='keywords']/@content

HTML 태그 처리
-------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.document.html.pruned.tags``
     - 제거할 HTML 태그
     - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
   * - ``crawler.document.html.max.digest.length``
     - 다이제스트 최대 길이
     - ``120``
   * - ``crawler.document.html.default.lang``
     - 기본 언어
     - (빈 값)

설정 예
~~~~~~

::

    # 제거할 태그 추가
    crawler.document.html.pruned.tags=noscript,script,style,header,footer,aside,nav,a[rel=nofollow],form

    # 다이제스트 길이를 200자로
    crawler.document.html.max.digest.length=200

    # 기본 언어를 한국어로
    crawler.document.html.default.lang=ko

URL 패턴 필터
---------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.document.html.default.include.index.patterns``
     - 인덱스에 포함할 URL 패턴
     - (빈 값)
   * - ``crawler.document.html.default.exclude.index.patterns``
     - 인덱스에서 제외할 URL 패턴
     - ``(?i).*(css|js|jpeg...)``
   * - ``crawler.document.html.default.include.search.patterns``
     - 검색 결과에 포함할 URL 패턴
     - (빈 값)
   * - ``crawler.document.html.default.exclude.search.patterns``
     - 검색 결과에서 제외할 URL 패턴
     - (빈 값)

설정 예
~~~~~~

::

    # 기본 제외 패턴
    crawler.document.html.default.exclude.index.patterns=(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)

    # 특정 경로만 인덱싱
    crawler.document.html.default.include.index.patterns=https://example\\.com/docs/.*

파일 크롤러 설정
======================

기본 설정
--------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.document.file.name.encoding``
     - 파일명 인코딩
     - (빈 값)
   * - ``crawler.document.file.no.title.label``
     - 제목 없는 파일의 레이블
     - ``No title.``
   * - ``crawler.document.file.ignore.empty.content``
     - 빈 콘텐츠 무시
     - ``false``
   * - ``crawler.document.file.max.title.length``
     - 제목 최대 길이
     - ``100``
   * - ``crawler.document.file.max.digest.length``
     - 다이제스트 최대 길이
     - ``200``

설정 예
~~~~~~

::

    # Windows-31J 파일명 처리
    crawler.document.file.name.encoding=Windows-31J

    # 제목 없는 파일의 레이블
    crawler.document.file.no.title.label=제목 없음

    # 빈 파일 무시
    crawler.document.file.ignore.empty.content=true

    # 제목과 다이제스트 길이
    crawler.document.file.max.title.length=200
    crawler.document.file.max.digest.length=500

콘텐츠 처리
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.document.file.append.meta.content``
     - 메타데이터를 콘텐츠에 추가
     - ``true``
   * - ``crawler.document.file.append.body.content``
     - 본문을 콘텐츠에 추가
     - ``true``
   * - ``crawler.document.file.default.lang``
     - 기본 언어
     - (빈 값)

설정 예
~~~~~~

::

    crawler.document.file.append.meta.content=true
    crawler.document.file.append.body.content=true
    crawler.document.file.default.lang=ko

파일 URL 패턴 필터
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.document.file.default.include.index.patterns``
     - 인덱스에 포함할 패턴
     - (빈 값)
   * - ``crawler.document.file.default.exclude.index.patterns``
     - 인덱스에서 제외할 패턴
     - (빈 값)
   * - ``crawler.document.file.default.include.search.patterns``
     - 검색 결과에 포함할 패턴
     - (빈 값)
   * - ``crawler.document.file.default.exclude.search.patterns``
     - 검색 결과에서 제외할 패턴
     - (빈 값)

설정 예
~~~~~~

::

    # 특정 확장자만 인덱싱
    crawler.document.file.default.include.index.patterns=.*\\.(pdf|docx|xlsx|pptx)$

    # temp 폴더 제외
    crawler.document.file.default.exclude.index.patterns=.*/temp/.*

캐시 설정
==============

문서 캐시
----------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``crawler.document.cache.enabled``
     - 문서 캐시 활성화
     - ``true``
   * - ``crawler.document.cache.max.size``
     - 캐시 최대 크기(바이트)
     - ``2621440`` (2.5MB)
   * - ``crawler.document.cache.supported.mimetypes``
     - 캐시 대상 MIME 타입
     - ``text/html``
   * - ``crawler.document.cache.html.mimetypes``
     - HTML로 처리할 MIME 타입
     - ``text/html``

설정 예
~~~~~~

::

    # 문서 캐시 활성화
    crawler.document.cache.enabled=true

    # 캐시 크기를 5MB로
    crawler.document.cache.max.size=5242880

    # 캐시 대상 MIME 타입
    crawler.document.cache.supported.mimetypes=text/html,application/xhtml+xml

    # HTML로 처리할 MIME 타입
    crawler.document.cache.html.mimetypes=text/html,application/xhtml+xml

.. note::
   캐시를 활성화하면 검색 결과에 캐시 링크가 표시되어
   사용자는 크롤 시점의 콘텐츠를 참조할 수 있습니다.

JVM 옵션
==============

크롤러 프로세스의 JVM 옵션을 설정할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 속성
     - 설명
     - 기본값
   * - ``jvm.crawler.options``
     - 크롤러 JVM 옵션
     - ``-Xms128m -Xmx512m...``

기본 설정
--------------

::

    jvm.crawler.options=-Xms128m -Xmx512m \
        -XX:MaxMetaspaceSize=128m \
        -XX:+UseG1GC \
        -XX:MaxGCPauseMillis=60000 \
        -XX:-HeapDumpOnOutOfMemoryError

주요 옵션 설명
----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 옵션
     - 설명
   * - ``-Xms128m``
     - 초기 힙 크기(128MB)
   * - ``-Xmx512m``
     - 최대 힙 크기(512MB)
   * - ``-XX:MaxMetaspaceSize=128m``
     - Metaspace 최대 크기(128MB)
   * - ``-XX:+UseG1GC``
     - G1 가비지 컬렉터 사용
   * - ``-XX:MaxGCPauseMillis=60000``
     - GC 중지 시간 목표값(60초)
   * - ``-XX:-HeapDumpOnOutOfMemoryError``
     - OutOfMemory 시 힙 덤프 비활성화

사용자 정의 설정 예
--------------

**큰 파일을 크롤링하는 경우:**

::

    jvm.crawler.options=-Xms256m -Xmx2g \
        -XX:MaxMetaspaceSize=256m \
        -XX:+UseG1GC \
        -XX:MaxGCPauseMillis=60000

**디버그 시:**

::

    jvm.crawler.options=-Xms128m -Xmx512m \
        -XX:MaxMetaspaceSize=128m \
        -XX:+UseG1GC \
        -XX:+HeapDumpOnOutOfMemoryError \
        -XX:HeapDumpPath=/tmp/crawler_dump.hprof

자세한 내용은 :doc:`setup-memory` 를 참조하십시오.

성능 튜닝
==========================

크롤 속도 최적화
--------------------

**1. 스레드 수 조정**

병렬 크롤 수를 늘려 크롤 속도를 향상시킬 수 있습니다.

::

    # 관리 화면의 크롤 설정에서 스레드 수 조정
    스레드 수: 10

단, 대상 서버의 부하에 주의하십시오.

**2. 타임아웃 조정**

응답이 느린 사이트의 경우 타임아웃을 조정합니다.

::

    # 크롤 설정의 "설정 파라미터"에 추가
    client.connectionTimeout=10000
    client.socketTimeout=30000

**3. 불필요한 콘텐츠 제외**

이미지, CSS, JavaScript 파일 등을 제외하여 크롤 속도를 향상시킵니다.

::

    # 제외 URL 패턴
    .*\.(jpg|jpeg|png|gif|css|js|ico)$

**4. 재시도 설정**

오류 시 재시도 횟수와 간격을 조정합니다.

::

    # 크롤 설정의 "설정 파라미터"에 추가
    client.maxRetry=3
    client.retryInterval=1000

메모리 사용량 최적화
--------------------

**1. 힙 크기 조정**

::

    jvm.crawler.options=-Xms256m -Xmx1g

**2. 캐시 크기 조정**

::

    crawler.document.cache.max.size=1048576  # 1MB

**3. 큰 파일 제외**

::

    # 크롤 설정의 "설정 파라미터"에 추가
    client.maxContentLength=10485760  # 10MB

자세한 내용은 :doc:`setup-memory` 를 참조하십시오.

인덱스 품질 향상
----------------------

**1. XPath 최적화**

불필요한 요소(네비게이션, 광고 등)를 제외합니다.

::

    crawler.document.html.content.xpath=//DIV[@id='main-content']
    crawler.document.html.pruned.tags=noscript,script,style,header,footer,aside,nav,form,iframe

**2. 다이제스트 최적화**

::

    crawler.document.html.max.digest.length=200

**3. 메타데이터 매핑**

::

    crawler.metadata.name.mapping=\
        title=title:string\n\
        description=digest:string\n\
        keywords=label:string

문제 해결
======================

메모리 부족
----------

**증상:**

- ``OutOfMemoryError`` 가 ``fess_crawler.log`` 에 기록됨
- 크롤이 중간에 중지됨

**대책:**

1. 크롤러의 힙 크기를 늘림

   ::

       jvm.crawler.options=-Xms256m -Xmx2g

2. 병렬 스레드 수를 줄임

3. 큰 파일을 제외함

자세한 내용은 :doc:`setup-memory` 를 참조하십시오.

크롤이 느림
--------------

**증상:**

- 크롤에 시간이 너무 오래 걸림
- 타임아웃이 빈번하게 발생함

**대책:**

1. 스레드 수를 늘림(대상 서버의 부하에 주의)

2. 타임아웃을 조정함

   ::

       client.connectionTimeout=5000
       client.socketTimeout=10000

3. 불필요한 URL을 제외함

특정 콘텐츠를 추출할 수 없음
------------------------------

**증상:**

- 페이지의 텍스트가 올바르게 추출되지 않음
- 중요한 정보가 검색 결과에 포함되지 않음

**대책:**

1. XPath를 확인 및 조정함

   ::

       crawler.document.html.content.xpath=//DIV[@class='content']

2. 제거 태그를 확인함

   ::

       crawler.document.html.pruned.tags=script,style

3. JavaScript로 동적으로 생성되는 콘텐츠의 경우 다른 방법(API 크롤링 등)을 검토

문자 깨짐 발생
------------------

**증상:**

- 검색 결과에서 문자가 깨짐
- 특정 언어가 올바르게 표시되지 않음

**대책:**

1. 인코딩 설정을 확인함

   ::

       crawler.document.site.encoding=UTF-8
       crawler.crawling.data.encoding=UTF-8

2. 파일명 인코딩을 설정함

   ::

       crawler.document.file.name.encoding=Windows-31J

3. 로그에서 인코딩 오류를 확인함

   ::

       grep -i "encoding" /var/log/fess/fess_crawler.log

모범 사례
==================

1. **테스트 환경에서 검증**

   운영 환경에 적용하기 전에 테스트 환경에서 충분히 검증하십시오.

2. **단계적 조정**

   설정을 한 번에 크게 변경하지 말고 단계적으로 조정하여 효과를 확인하십시오.

3. **로그 모니터링**

   설정 변경 후에는 로그를 모니터링하여 오류나 성능 문제가 없는지 확인하십시오.

   ::

       tail -f /var/log/fess/fess_crawler.log

4. **백업**

   설정 파일을 변경하기 전에 반드시 백업을 수행하십시오.

   ::

       cp /etc/fess/fess_config.properties /etc/fess/fess_config.properties.bak

5. **문서화**

   변경한 설정과 그 이유를 문서화하십시오.

참고 정보
========

- :doc:`crawler-basic` - 크롤러 기본 설정
- :doc:`crawler-thumbnail` - 썸네일 설정
- :doc:`setup-memory` - 메모리 설정
- :doc:`admin-logging` - 로그 설정
- :doc:`search-advanced` - 고급 검색 설정
