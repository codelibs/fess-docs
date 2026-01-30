==================================
Elasticsearch/OpenSearch 커넥터
==================================

개요
====

Elasticsearch/OpenSearch 커넥터는 Elasticsearch 또는 OpenSearch 클러스터에서 데이터를 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-elasticsearch`` 플러그인이 필요합니다.

지원 버전
==============

- Elasticsearch 7.x / 8.x
- OpenSearch 1.x / 2.x

전제조건
========

1. 플러그인 설치가 필요합니다
2. Elasticsearch/OpenSearch 클러스터에 대한 읽기 액세스가 필요합니다
3. 쿼리 실행 권한이 필요합니다

플러그인 설치
------------------------

방법 1: JAR 파일 직접 배치

::

    # Maven Central에서 다운로드
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-elasticsearch/X.X.X/fess-ds-elasticsearch-X.X.X.jar

    # 배치
    cp fess-ds-elasticsearch-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 또는
    cp fess-ds-elasticsearch-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

방법 2: 관리 화면에서 설치

1. "시스템" → "플러그인" 열기
2. JAR 파일 업로드
3. |Fess| 재시작

설정 방법
========

관리 화면에서 "크롤러" → "데이터 스토어" → "새로 만들기"에서 설정합니다.

기본 설정
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 항목
     - 설정 예
   * - 이름
     - External Elasticsearch
   * - 핸들러 이름
     - ElasticsearchDataStore
   * - 활성화
     - 켬

파라미터 설정
----------------

기본 연결:

::

    hosts=http://localhost:9200
    index=myindex
    scroll_size=100
    scroll_timeout=5m

인증 있는 연결:

::

    hosts=https://elasticsearch.example.com:9200
    index=myindex
    username=elastic
    password=changeme
    scroll_size=100
    scroll_timeout=5m

복수 호스트 설정:

::

    hosts=http://es-node1:9200,http://es-node2:9200,http://es-node3:9200
    index=myindex
    scroll_size=100
    scroll_timeout=5m

파라미터 목록
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``hosts``
     - 예
     - Elasticsearch/OpenSearch 호스트(쉼표 구분으로 복수 지정 가능)
   * - ``index``
     - 예
     - 대상 인덱스명
   * - ``username``
     - 아니오
     - 인증용 사용자명
   * - ``password``
     - 아니오
     - 인증용 비밀번호
   * - ``scroll_size``
     - 아니오
     - 스크롤 시 취득 건수(기본값: 100)
   * - ``scroll_timeout``
     - 아니오
     - 스크롤 타임아웃(기본값: 5m)
   * - ``query``
     - 아니오
     - 쿼리 JSON(기본값: match_all)
   * - ``fields``
     - 아니오
     - 취득할 필드(쉼표 구분)

스크립트 설정
--------------

기본 매핑:

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

중첩된 필드 액세스:

::

    url=data.metadata.url
    title=data.title
    content=data.body.content
    author=data.author.name
    created=data.created_at
    last_modified=data.updated_at

사용 가능한 필드
~~~~~~~~~~~~~~~~~~~~

- ``data.<field_name>`` - Elasticsearch 문서의 필드
- ``data._id`` - 문서 ID
- ``data._index`` - 인덱스명
- ``data._type`` - 문서 타입(Elasticsearch 7 미만)
- ``data._score`` - 검색 스코어

쿼리 설정
============

전체 문서 취득
--------------------

기본적으로 전체 문서가 취득됩니다.
``query`` 파라미터를 지정하지 않으면 ``match_all``이 사용됩니다.

특정 조건으로 필터링
--------------------------

::

    query={"query":{"term":{"status":"published"}}}

범위 지정:

::

    query={"query":{"range":{"timestamp":{"gte":"2024-01-01","lte":"2024-12-31"}}}}

복수 조건:

::

    query={"query":{"bool":{"must":[{"term":{"category":"news"}},{"range":{"views":{"gte":100}}}]}}}

정렬 지정:

::

    query={"query":{"match_all":{}},"sort":[{"timestamp":{"order":"desc"}}]}

특정 필드만 취득
========================

fields 파라미터로 취득 필드 제한
----------------------------------------

::

    hosts=http://localhost:9200
    index=myindex
    fields=title,content,url,timestamp
    scroll_size=100

모든 필드를 취득하려면 ``fields``를 지정하지 않거나 비워둡니다.

사용 예
======

기본 인덱스 크롤링
------------------------------

파라미터:

::

    hosts=http://localhost:9200
    index=articles
    scroll_size=100
    scroll_timeout=5m

스크립트:

::

    url=data.url
    title=data.title
    content=data.content
    created=data.created_at
    last_modified=data.updated_at

인증 포함 클러스터 크롤링
------------------------------

파라미터:

::

    hosts=https://es.example.com:9200
    index=products
    username=elastic
    password=changeme
    scroll_size=200
    scroll_timeout=10m

스크립트:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " " + data.specifications
    digest=data.category
    last_modified=data.updated_at

복수 인덱스 크롤링
------------------------------

파라미터:

::

    hosts=http://localhost:9200
    index=logs-2024-*
    query={"query":{"term":{"level":"error"}}}
    scroll_size=100

스크립트:

::

    url="https://logs.example.com/view/" + data._id
    title=data.message
    content=data.stack_trace
    digest=data.service + " - " + data.level
    last_modified=data.timestamp

OpenSearch 클러스터 크롤링
----------------------------

파라미터:

::

    hosts=https://opensearch.example.com:9200
    index=documents
    username=admin
    password=admin
    scroll_size=100
    scroll_timeout=5m

스크립트:

::

    url=data.url
    title=data.title
    content=data.body
    last_modified=data.modified_date

필드 제한 크롤링
----------------------------

파라미터:

::

    hosts=http://localhost:9200
    index=myindex
    fields=id,title,content,url,timestamp
    scroll_size=100

스크립트:

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

복수 호스트 부하 분산
----------------------

파라미터:

::

    hosts=http://es1.example.com:9200,http://es2.example.com:9200,http://es3.example.com:9200
    index=articles
    scroll_size=100
    scroll_timeout=5m

스크립트:

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

문제 해결
======================

연결 오류
----------

**증상**: ``Connection refused`` 또는 ``No route to host``

**확인 사항**:

1. 호스트 URL이 올바른지 확인(프로토콜, 호스트명, 포트)
2. Elasticsearch/OpenSearch가 실행 중인지 확인
3. 방화벽 설정 확인
4. HTTPS인 경우 인증서가 유효한지 확인

인증 오류
----------

**증상**: ``401 Unauthorized`` 또는 ``403 Forbidden``

**확인 사항**:

1. 사용자명과 비밀번호가 올바른지 확인
2. 사용자에게 적절한 권한이 있는지 확인:

   - 인덱스에 대한 읽기 권한
   - 스크롤 API 사용 권한

3. Elasticsearch Security(X-Pack)가 활성화된 경우 올바르게 설정되어 있는지 확인

인덱스를 찾을 수 없음
--------------------------

**증상**: ``index_not_found_exception``

**확인 사항**:

1. 인덱스명이 올바른지 확인(대소문자 포함)
2. 인덱스가 존재하는지 확인:

   ::

       GET /_cat/indices

3. 와일드카드 패턴이 올바른지 확인(예: ``logs-*``)

쿼리 오류
------------

**증상**: ``parsing_exception`` 또는 ``search_phase_execution_exception``

**확인 사항**:

1. 쿼리 JSON이 올바른지 확인
2. Elasticsearch/OpenSearch 버전에 맞는 쿼리인지 확인
3. 필드명이 올바른지 확인
4. 쿼리를 Elasticsearch/OpenSearch에서 직접 실행하여 테스트:

   ::

       POST /myindex/_search
       {
         "query": {...}
       }

스크롤 타임아웃
----------------------

**증상**: ``No search context found`` 또는 ``Scroll timeout``

**해결 방법**:

1. ``scroll_timeout``을 늘림:

   ::

       scroll_timeout=10m

2. ``scroll_size``를 줄임:

   ::

       scroll_size=50

3. 클러스터 리소스 확인

대량 데이터 크롤링
--------------------

**증상**: 크롤링이 느리거나 타임아웃됨

**해결 방법**:

1. ``scroll_size`` 조정(너무 크면 느려짐):

   ::

       scroll_size=100  # 기본값
       scroll_size=500  # 크게

2. ``fields``로 취득 필드 제한
3. ``query``로 필요한 문서만 필터링
4. 여러 데이터 스토어로 분할(인덱스 단위, 시간 범위 단위 등)

메모리 부족
----------

**증상**: OutOfMemoryError

**해결 방법**:

1. ``scroll_size``를 줄임
2. ``fields``로 취득 필드 제한
3. |Fess|의 힙 크기 증가
4. 큰 필드(바이너리 데이터 등) 제외

SSL/TLS 연결
===========

자체 서명 인증서의 경우
--------------------

.. warning::
   프로덕션 환경에서는 올바르게 서명된 인증서를 사용하세요.

자체 서명 인증서를 사용하는 경우 Java keystore에 인증서 추가:

::

    keytool -import -alias es-cert -file es-cert.crt -keystore $JAVA_HOME/lib/security/cacerts

클라이언트 인증서 인증
----------------------

클라이언트 인증서가 필요한 경우 추가 파라미터 설정이 필요합니다.
자세한 내용은 Elasticsearch 클라이언트 문서를 참조하세요.

고급 쿼리 예
==============

집계를 포함한 쿼리
----------------

.. note::
   집계 결과는 취득되지 않고 문서만 취득됩니다.

::

    query={"query":{"match_all":{}},"aggs":{"categories":{"terms":{"field":"category"}}}}

스크립트 필드
--------------------

::

    query={"query":{"match_all":{}},"script_fields":{"full_url":{"script":"doc['protocol'].value + '://' + doc['host'].value + doc['path'].value"}}}

스크립트:

::

    url=data.full_url
    title=data.title
    content=data.content

참고 정보
========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-database` - 데이터베이스 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `Elasticsearch Documentation <https://www.elastic.co/guide/>`_
- `OpenSearch Documentation <https://opensearch.org/docs/>`_
- `Elasticsearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_
