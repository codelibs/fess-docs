==================================
JSON 커넥터
==================================

개요
====

JSON 커넥터는 로컬 JSON 파일이나 JSONL 파일에서 데이터를 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-json`` 플러그인이 필요합니다.

전제조건
========

1. 플러그인 설치가 필요합니다
2. JSON 파일에 대한 액세스 권한이 필요합니다
3. JSON 구조를 이해하고 있어야 합니다

플러그인 설치
------------------------

방법 1: JAR 파일 직접 배치

::

    # Maven Central에서 다운로드
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # 배치
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 또는
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

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
     - Products JSON
   * - 핸들러 이름
     - JsonDataStore
   * - 활성화
     - 켬

파라미터 설정
----------------

로컬 파일:

::

    files=/path/to/data.json
    fileEncoding=UTF-8

복수 파일:

::

    files=/path/to/data1.json,/path/to/data2.json
    fileEncoding=UTF-8

디렉터리 지정:

::

    directories=/path/to/json_dir/
    fileEncoding=UTF-8

파라미터 목록
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``files``
     - 아니오
     - JSON 파일 경로(복수 지정 가능: 쉼표 구분)
   * - ``directories``
     - 아니오
     - JSON 파일을 포함하는 디렉터리 경로
   * - ``fileEncoding``
     - 아니오
     - 문자 인코딩(기본값: UTF-8)

.. warning::
   ``files`` 또는 ``directories`` 중 하나를 반드시 지정해야 합니다.
   둘 다 미지정인 경우 ``DataStoreException`` 이 발생합니다.
   둘 다 지정한 경우 ``files`` 가 우선되며 ``directories`` 는 무시됩니다.

.. note::
   이 커넥터는 로컬 파일 시스템의 JSON 파일만 대상으로 하며, HTTP 액세스나 API 인증 기능은 지원하지 않습니다.

스크립트 설정
--------------

단순한 JSON 오브젝트:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=data.price
    category=data.category

중첩된 JSON 오브젝트:

::

    url="https://example.com/product/" + data.id
    title=data.product.name
    content=data.product.description
    price=data.product.pricing.amount
    author=data.product.author.name

배열 요소 처리:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.body
    tags=data.tags.join(", ")
    categories=data.categories[0].name

사용 가능한 필드
~~~~~~~~~~~~~~~~~~~~

- ``data.<필드명>`` - JSON 오브젝트의 필드
- ``data.<부모>.<자식>`` - 중첩된 오브젝트
- ``data.<배열>[<인덱스>]`` - 배열 요소
- ``data.<배열>.<메서드>`` - 배열 메서드(join, length 등)

JSON 형식 상세
==============

JSON 파일 형식
----------------

JSON 커넥터는 JSONL(JSON Lines) 형식의 파일을 읽어들입니다.
한 줄에 하나의 JSON 오브젝트를 기술하는 형식입니다.

.. note::
   배열 형식의 JSON 파일( ``[{...}, {...}]`` )은 직접 읽어들일 수 없습니다.
   JSONL 형식으로 변환해 주세요.

JSONL 형식 파일:

::

    {"id": 1, "name": "Product A", "description": "Description A"}
    {"id": 2, "name": "Product B", "description": "Description B"}

사용 예
======

제품 카탈로그
--------------

파라미터:

::

    files=/var/data/products.json
    fileEncoding=UTF-8

스크립트:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " 가격: " + data.price + "원"
    digest=data.category
    price=data.price

복수 JSON 파일 통합
---------------------

파라미터:

::

    files=/var/data/data1.json,/var/data/data2.json
    fileEncoding=UTF-8

스크립트:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

문제 해결
======================

파일을 찾을 수 없음
----------------------

**증상**: ``FileNotFoundException``

**확인 사항**:

1. 파일 경로가 올바른지 확인
2. 파일이 존재하는지 확인
3. 파일 읽기 권한이 있는지 확인

JSON 파싱 오류
--------------

**증상**: ``JsonParseException`` 또는 ``Unexpected character``

**확인 사항**:

1. JSON 파일이 올바른 형식인지 확인:

   ::

       # JSON 검증
       cat data.json | jq .

2. 문자 인코딩이 올바른지 확인
3. 잘못된 문자나 줄바꿈이 없는지 확인
4. 주석이 포함되어 있지 않은지 확인(JSON 표준에서는 주석 불가)

데이터를 가져올 수 없음
--------------------

**증상**: 크롤링은 성공하지만 건수가 0

**확인 사항**:

1. JSON 구조 확인
2. 스크립트 설정이 올바른지 확인
3. 필드명이 올바른지 확인(대소문자 포함)
4. 로그에서 오류 메시지 확인

대용량 JSON 파일
------------------

**증상**: 메모리 부족 또는 타임아웃

**해결 방법**:

1. JSON 파일을 여러 개로 분할
2. |Fess| 힙 사이즈를 늘리기

고급 스크립트 사용 예
========================

조건부 처리
------------

각 필드는 독립된 식으로 평가됩니다. 조건부 값에는 삼항 연산자를 사용합니다:

::

    url=data.status == "published" ? "https://example.com/product/" + data.id : null
    title=data.status == "published" ? data.name : null
    content=data.status == "published" ? data.description : null
    price=data.status == "published" ? data.price : null

배열 결합
----------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    tags=data.tags ? data.tags.join(", ") : ""
    categories=data.categories.collect { it.name }.join(", ")

기본값 설정
------------------

::

    url="https://example.com/item/" + data.id
    title=data.title ?: "제목 없음"
    content=data.description ?: (data.summary ?: "설명 없음")
    price=data.price ?: 0

날짜 포맷
------------------

::

    url="https://example.com/post/" + data.id
    title=data.title
    content=data.body
    created=data.created_at
    last_modified=data.updated_at

숫자 처리
----------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=data.price as Float
    stock=data.stock_quantity as Integer

참고 정보
========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-csv` - CSV 커넥터
- :doc:`ds-database` - 데이터베이스 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSONPath <https://goessner.net/articles/JsonPath/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
