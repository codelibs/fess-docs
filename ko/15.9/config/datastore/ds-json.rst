==================================
JSON 커넥터
==================================

개요
====

JSON 커넥터는 로컬 JSONL 파일(JSON Lines 형식)에서 데이터를 가져와
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-json`` 플러그인이 필요합니다.

전제 조건
=========

1. 플러그인 설치가 필요합니다
2. JSON 파일에 대한 액세스 권한이 필요합니다
3. JSON 구조를 이해하고 있어야 합니다

플러그인 설치
-------------

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
=========

관리 화면에서 "크롤러" → "데이터 스토어" → "새로 만들기"에서 설정합니다.

기본 설정
---------

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
-------------

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
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 파라미터
     - 필수
     - 설명
   * - ``files``
     - 아니오
     - 처리할 JSON 파일 경로(복수 지정 가능: 쉼표 구분). ``.json`` 또는 ``.jsonl`` 확장자 파일만 처리됩니다.
   * - ``directories``
     - 아니오
     - JSON 파일을 포함하는 디렉터리 경로(복수 지정 가능: 쉼표 구분)
   * - ``fileEncoding``
     - 아니오
     - 문자 인코딩(기본값: UTF-8)

.. warning::
   ``files`` 또는 ``directories`` 중 하나를 반드시 지정해야 합니다.
   둘 다 미지정(공백)인 경우 ``DataStoreException`` 이 발생합니다.
   둘 다 지정한 경우 ``files`` 가 우선되며 ``directories`` 는 무시됩니다.

.. note::
   파라미터 이름은 카멜 케이스의 ``fileEncoding`` 입니다(스네이크 케이스의 ``file_encoding`` 이 아닙니다).

디렉터리 지정 시의 동작
~~~~~~~~~~~~~~~~~~~~~~~

``directories`` 를 지정한 경우, 각 디렉터리 바로 아래의 파일이 다음 규칙으로 처리됩니다.

- **하위 디렉터리는 탐색되지 않습니다** (재귀적 탐색은 수행하지 않습니다).
- 확장자가 ``.json`` 또는 ``.jsonl`` 인 파일만 대상입니다(대소문자 구분 없음).
- 파일은 수정 일시(최종 수정 시각) 오름차순으로 처리됩니다.

.. note::
   이 커넥터는 로컬 파일 시스템의 JSON 파일만 대상으로 하며, HTTP 액세스나 API 인증 기능은 지원하지 않습니다.

스크립트 설정
-------------

각 필드의 값은 JSON 오브젝트의 각 필드 값을 참조하여 조합합니다.
JSON 오브젝트 최상위 레벨의 필드는 스크립트 내에서 **접두사 없는 변수**
로 직접 참조할 수 있습니다( ``data.`` 와 같은 접두사는 붙지 않습니다).

단순한 JSON 오브젝트:

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=price
    category=category

중첩된 JSON 오브젝트(중첩된 오브젝트는 맵으로 참조합니다):

::

    url="https://example.com/product/" + id
    title=product.name
    content=product.description
    price=product.pricing.amount
    author=product.author.name

배열 요소 처리:

::

    url="https://example.com/article/" + id
    title=title
    content=body
    tags=tags.join(", ")
    categories=categories[0].name

사용 가능한 필드
~~~~~~~~~~~~~~~~

- ``<필드명>`` - JSON 오브젝트 최상위 레벨의 필드를 이름으로 직접 참조합니다
- ``<부모>.<자식>`` - 중첩된 오브젝트의 필드
- ``<배열>[<인덱스>]`` - 배열 요소
- ``<배열>.<메서드>`` - 배열 메서드( ``join``, ``collect``, ``size`` 등)

.. note::

   필드 이름에 공백이나 하이픈 등 Groovy 식별자로 유효하지 않은 문자가 포함된 경우,
   해당 필드를 변수명으로 직접 참조할 수 없습니다.

JSON 형식 상세
==============

JSON 파일 형식
--------------

JSON 커넥터는 JSONL(JSON Lines) 형식의 파일을 읽어들입니다.
한 줄에 하나의 JSON 오브젝트를 기술하는 형식입니다. 파일은 한 줄씩 읽어들이며,
각 줄이 독립된 JSON 오브젝트로 파싱됩니다.

.. note::
   확장자가 ``.json`` 인 파일도 처리 대상이 되지만, 내용은 JSONL 형식
   (한 줄에 하나의 오브젝트)이어야 합니다.
   배열 형식의 JSON 파일( ``[{...}, {...}]`` )이나, 여러 줄로 포맷된
   (pretty-print된) JSON은 직접 읽어들일 수 없습니다. JSONL 형식으로 변환해 주세요.

JSONL 형식 파일:

::

    {"id": 1, "name": "Product A", "description": "Description A"}
    {"id": 2, "name": "Product B", "description": "Description B"}

사용 예
=======

제품 카탈로그
-------------

파라미터:

::

    files=/var/data/products.json
    fileEncoding=UTF-8

스크립트:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description + " 가격: " + price + "원"
    digest=category
    price=price

복수 JSON 파일 통합
-------------------

파라미터:

::

    files=/var/data/data1.json,/var/data/data2.json
    fileEncoding=UTF-8

스크립트:

::

    url="https://example.com/item/" + id
    title=title
    content=content

문제 해결
=========

파일을 찾을 수 없음
-------------------

**증상**: 로그에 ``... is not found.`` 또는 ``Source file ... does not exist.`` 가 출력됩니다

**확인 사항**:

1. 파일 경로가 올바른지 확인
2. 파일이 존재하는지 확인
3. 파일 확장자가 ``.json`` 또는 ``.jsonl`` 인지 확인
4. 파일 읽기 권한이 있는지 확인

JSON 파싱 오류
--------------

**증상**: 로그에 ``Crawling Access Exception`` 과 ``JsonParseException`` 등이 출력됩니다

잘못된 줄이 포함된 경우, 해당 줄만 건너뛰고 실패 URL로 기록되며,
크롤링 자체는 다음 줄부터 계속됩니다.

**확인 사항**:

1. JSON 파일이 올바른 형식(한 줄에 하나의 오브젝트인 JSONL)인지 확인:

   ::

       # 각 줄이 유효한 JSON 오브젝트인지 검증
       cat data.json | jq -c .

2. 문자 인코딩이 올바른지 확인
3. 하나의 오브젝트가 여러 줄에 걸쳐 있지 않은지 확인
4. 주석이 포함되어 있지 않은지 확인(JSON 표준에서는 주석 불가)

데이터를 가져올 수 없음
-----------------------

**증상**: 크롤링은 성공하지만 건수가 0

**확인 사항**:

1. JSON 구조 확인
2. 스크립트 설정이 올바른지 확인(필드 참조가 ``data.`` 접두사 없이 되어 있는지)
3. 필드명이 올바른지 확인(대소문자 포함)
4. 로그에서 오류 메시지 확인

대용량 JSON 파일
----------------

**증상**: 메모리 부족 또는 타임아웃

파일은 한 줄씩 읽어들이기 때문에 파일 전체 크기가 직접 메모리 사용량에
영향을 주지는 않습니다. 단, 한 줄(오브젝트 하나)이 극단적으로 큰 경우나
인덱스 등록 부하가 높은 경우 문제가 발생할 수 있습니다.

**해결 방법**:

1. JSON 파일을 여러 개로 분할
2. |Fess| 힙 사이즈 늘리기

스크립트 고급 사용 예
=====================

조건부 처리
-----------

각 필드는 독립된 식으로 평가됩니다. 조건부 값에는 삼항 연산자를 사용합니다:

::

    url=status == "published" ? "https://example.com/product/" + id : null
    title=status == "published" ? name : null
    content=status == "published" ? description : null
    price=status == "published" ? price : null

배열 결합
---------

::

    url="https://example.com/article/" + id
    title=title
    content=content
    tags=tags ? tags.join(", ") : ""
    categories=categories.collect { it.name }.join(", ")

기본값 설정
-----------

::

    url="https://example.com/item/" + id
    title=title ?: "제목 없음"
    content=description ?: (summary ?: "설명 없음")
    price=price ?: 0

날짜 포맷
---------

::

    url="https://example.com/post/" + id
    title=title
    content=body
    created=created_at
    last_modified=updated_at

숫자 처리
---------

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=price as Float
    stock=stock_quantity as Integer

참고 정보
=========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-csv` - CSV 커넥터
- :doc:`ds-database` - 데이터베이스 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSON Lines <https://jsonlines.org/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
