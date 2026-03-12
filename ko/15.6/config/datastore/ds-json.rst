==================================
JSON 커넥터
==================================

개요
====

JSON 커넥터는 JSON 파일 또는 JSON API에서 데이터를 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-json`` 플러그인이 필요합니다.

전제조건
========

1. 플러그인 설치가 필요합니다
2. JSON 파일 또는 API에 대한 액세스 권한이 필요합니다
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

    file_path=/path/to/data.json
    encoding=UTF-8
    json_path=$

HTTP 파일:

::

    file_path=https://api.example.com/products.json
    encoding=UTF-8
    json_path=$.data

REST API(인증 있음):

::

    file_path=https://api.example.com/v1/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    auth_type=bearer
    auth_token=your_api_token_here

복수 파일:

::

    file_path=/path/to/data1.json,https://api.example.com/data2.json
    encoding=UTF-8
    json_path=$

파라미터 목록
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``file_path``
     - 예
     - JSON 파일 경로 또는 API URL(복수 지정 가능: 쉼표 구분)
   * - ``encoding``
     - 아니오
     - 문자 인코딩(기본값: UTF-8)
   * - ``json_path``
     - 아니오
     - JSONPath를 통한 데이터 추출 경로(기본값: ``$``)
   * - ``http_method``
     - 아니오
     - HTTP 메서드(GET, POST 등, 기본값: GET)
   * - ``auth_type``
     - 아니오
     - 인증 타입(bearer, basic)
   * - ``auth_token``
     - 아니오
     - 인증 토큰(bearer 인증인 경우)
   * - ``auth_username``
     - 아니오
     - 인증 사용자명(basic 인증인 경우)
   * - ``auth_password``
     - 아니오
     - 인증 비밀번호(basic 인증인 경우)
   * - ``http_headers``
     - 아니오
     - 커스텀 HTTP 헤더(JSON 형식)

스크립트 설정
--------------

단순 JSON 오브젝트:

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

단순 배열
----------

::

    [
      {
        "id": 1,
        "name": "Product A",
        "description": "Description A",
        "price": 1000
      },
      {
        "id": 2,
        "name": "Product B",
        "description": "Description B",
        "price": 2000
      }
    ]

파라미터:

::

    json_path=$

중첩된 구조
--------------

::

    {
      "data": {
        "products": [
          {
            "id": 1,
            "name": "Product A",
            "details": {
              "description": "Description A",
              "price": 1000,
              "category": {
                "id": 10,
                "name": "Electronics"
              }
            }
          }
        ]
      }
    }

파라미터:

::

    json_path=$.data.products

스크립트:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.details.description
    price=data.details.price
    category=data.details.category.name

복잡한 배열
----------

::

    {
      "articles": [
        {
          "id": 1,
          "title": "Article 1",
          "content": "Content 1",
          "tags": ["tag1", "tag2", "tag3"],
          "author": {
            "name": "John Doe",
            "email": "john@example.com"
          }
        }
      ]
    }

파라미터:

::

    json_path=$.articles

스크립트:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    author=data.author.name
    tags=data.tags.join(", ")

JSONPath 사용
===============

JSONPath란
------------

JSONPath는 JSON 내 요소를 지정하기 위한 쿼리 언어입니다.
XML의 XPath에 해당합니다.

기본 구문
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 구문
     - 설명
   * - ``$``
     - 루트 요소
   * - ``$.field``
     - 최상위 필드
   * - ``$.parent.child``
     - 중첩된 필드
   * - ``$.array[0]``
     - 배열의 첫 번째 요소
   * - ``$.array[*]``
     - 배열의 모든 요소
   * - ``$..field``
     - 재귀적 검색

JSONPath 예
-------------

전체 요소 대상(루트):

::

    json_path=$

특정 배열 대상:

::

    json_path=$.data.items

중첩된 배열:

::

    json_path=$.response.results.products

재귀적 검색:

::

    json_path=$..products

사용 예
======

제품 카탈로그 API
---------------

API 응답:

::

    {
      "status": "success",
      "data": {
        "products": [
          {
            "product_id": "P001",
            "name": "노트북",
            "description": "고성능 노트북",
            "price": 120000,
            "category": "컴퓨터",
            "in_stock": true
          }
        ]
      }
    }

파라미터:

::

    file_path=https://api.example.com/products
    encoding=UTF-8
    json_path=$.data.products

스크립트:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " 가격: " + data.price + "원"
    digest=data.category
    price=data.price

블로그 기사 API
-------------

API 응답:

::

    {
      "posts": [
        {
          "id": 1,
          "title": "기사 제목",
          "body": "기사 본문...",
          "author": {
            "name": "홍길동",
            "email": "hong@example.com"
          },
          "tags": ["기술", "프로그래밍"],
          "published_at": "2024-01-15T10:00:00Z"
        }
      ]
    }

파라미터:

::

    file_path=https://blog.example.com/api/posts
    encoding=UTF-8
    json_path=$.posts

스크립트:

::

    url="https://blog.example.com/post/" + data.id
    title=data.title
    content=data.body
    author=data.author.name
    tags=data.tags.join(", ")
    created=data.published_at

Bearer 인증 API
---------------

파라미터:

::

    file_path=https://api.example.com/v1/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    auth_type=bearer
    auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

스크립트:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.description

Basic 인증 API
--------------

파라미터:

::

    file_path=https://api.example.com/data
    encoding=UTF-8
    json_path=$.data
    http_method=GET
    auth_type=basic
    auth_username=apiuser
    auth_password=password123

스크립트:

::

    url="https://example.com/data/" + data.id
    title=data.name
    content=data.content

커스텀 헤더 사용
----------------------

파라미터:

::

    file_path=https://api.example.com/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    http_headers={"X-API-Key":"your-api-key","Accept":"application/json"}

스크립트:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

복수 JSON 파일 통합
---------------------

파라미터:

::

    file_path=/var/data/data1.json,/var/data/data2.json,https://api.example.com/data3.json
    encoding=UTF-8
    json_path=$.items

스크립트:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

POST 요청
--------------

파라미터:

::

    file_path=https://api.example.com/search
    encoding=UTF-8
    json_path=$.results
    http_method=POST
    http_headers={"Content-Type":"application/json"}
    post_body={"query":"search term","limit":100}

스크립트:

::

    url="https://example.com/result/" + data.id
    title=data.title
    content=data.content

문제 해결
======================

파일을 찾을 수 없음
----------------------

**증상**: ``FileNotFoundException`` 또는 ``404 Not Found``

**확인 사항**:

1. 파일 경로 또는 URL이 올바른지 확인
2. 파일이 존재하는지 확인
3. URL인 경우 API가 가동 중인지 확인
4. 네트워크 연결 확인

JSON 파싱 오류
--------------

**증상**: ``JsonParseException`` 또는 ``Unexpected character``

**확인 사항**:

1. JSON 파일이 올바른 형식인지 확인:

   ::

       # JSON 검증
       cat data.json | jq .

2. 문자 인코딩이 올바른지 확인
3. 부정한 문자나 줄바꿈이 없는지 확인
4. 주석이 포함되어 있지 않은지 확인(JSON 표준에서는 주석 불가)

JSONPath 오류
--------------

**증상**: 데이터를 가져올 수 없거나 빈 결과

**확인 사항**:

1. JSONPath 구문이 올바른지 확인
2. 대상 요소가 존재하는지 확인
3. JSONPath를 테스트 도구로 검증:

   ::

       # jq를 사용한 확인
       cat data.json | jq '$.data.products'

4. 경로가 올바른 계층을 가리키는지 확인

인증 오류
----------

**증상**: ``401 Unauthorized`` 또는 ``403 Forbidden``

**확인 사항**:

1. 인증 타입이 올바른지 확인(bearer, basic)
2. 인증 토큰 또는 사용자명/비밀번호가 올바른지 확인
3. 토큰 유효기간 확인
4. API 권한 설정 확인

데이터를 가져올 수 없음
--------------------

**증상**: 크롤링은 성공하지만 건수가 0

**확인 사항**:

1. JSONPath가 올바른 요소를 가리키는지 확인
2. JSON 구조 확인
3. 스크립트 설정이 올바른지 확인
4. 필드명이 올바른지 확인(대소문자 포함)
5. 로그에서 오류 메시지 확인

배열 처리
----------

JSON이 배열인 경우:

::

    [
      {"id": 1, "name": "Item 1"},
      {"id": 2, "name": "Item 2"}
    ]

파라미터:

::

    json_path=$

JSON이 오브젝트이고 배열을 포함하는 경우:

::

    {
      "items": [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"}
      ]
    }

파라미터:

::

    json_path=$.items

대형 JSON 파일
------------------

**증상**: 메모리 부족 또는 타임아웃

**해결 방법**:

1. JSON 파일을 여러 개로 분할
2. JSONPath로 필요한 부분만 추출
3. API인 경우 페이지네이션 사용
4. |Fess|의 힙 크기 증가

API 속도 제한
-------------

**증상**: ``429 Too Many Requests``

**해결 방법**:

1. 크롤링 간격을 늘림
2. API 속도 제한 확인
3. 여러 API 키를 사용하여 부하 분산

스크립트 고급 사용 예
========================

조건부 처리
------------

::

    if (data.status == "published" && data.price > 1000) {
        url="https://example.com/product/" + data.id
        title=data.name
        content=data.description
        price=data.price
    }

배열 결합
----------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    tags=data.tags ? data.tags.join(", ") : ""
    categories=data.categories.map(function(c) { return c.name; }).join(", ")

기본값 설정
------------------

::

    url="https://example.com/item/" + data.id
    title=data.title || "무제"
    content=data.description || data.summary || "설명 없음"
    price=data.price || 0

날짜 형식
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
    price=parseFloat(data.price)
    stock=parseInt(data.stock_quantity)

참고 정보
========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-csv` - CSV 커넥터
- :doc:`ds-database` - 데이터베이스 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSONPath <https://goessner.net/articles/JsonPath/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
