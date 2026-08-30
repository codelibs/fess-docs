==================================
JSON 커넥터
==================================

개요
====

JSON 커넥터는 로컬 파일 시스템 상의 JSON 파일에서 데이터를 가져와
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-json`` 플러그인이 필요합니다.

다음 3가지 형식을 지원하며, 기본적으로 파일 내용으로부터 자동으로 판별됩니다.

- JSON Lines 형식(1행에 1개의 JSON 오브젝트)
- JSON 오브젝트의 배열(정형화된 것, 1행으로 정리된 것 모두 가능)
- 단일 JSON 오브젝트

레코드는 1건씩 읽어들이므로, 큰 배열이라도 파일 전체가 메모리에
유지되는 일은 없습니다.

.. note::

   이 커넥터는 로컬 파일 시스템 상의 JSON 파일만을 대상으로 합니다.
   HTTP 등을 통한 원격 취득에는 대응하지 않으며, ``urls`` 파라미터를 지정한 경우에는
   무시되는 것이 아니라 오류가 됩니다.

전제 조건
=========

1. 플러그인 설치가 필요합니다
2. JSON 파일에 대한 액세스 권한이 필요합니다
3. JSON 구조를 이해하고 있어야 합니다

플러그인 설치
-------------

방법 1: 관리 화면에서 설치

1. "시스템" → "플러그인" 열기
2. JAR 파일 업로드
3. |Fess| 재시작

방법 2: JAR 파일 직접 배치

::

    # CodeLibs 저장소에서 다운로드
    wget https://maven.codelibs.org/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # 배치
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # 또는
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

.. note::

   15.8.0 이후 버전의 JAR는 `CodeLibs 저장소 <https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-json/>`_
   에서 배포하고 있습니다. 15.7.0 이전 버전은
   `Maven Central <https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/>`_ 에 있습니다.

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

    files=/var/data/products.jsonl
    file_encoding=UTF-8

복수 파일:

::

    files=/var/data/data1.json,/var/data/data2.json
    file_encoding=UTF-8

디렉터리 지정:

::

    directories=/var/data/json_dir/
    file_encoding=UTF-8

파라미터 목록
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - 파라미터
     - 기본값
     - 설명
   * - ``files``
     -
     - 처리할 JSON 파일의 경로(복수 지정 가능: 쉼표 구분). 지정한 순서대로 처리됩니다.
   * - ``directories``
     -
     - JSON 파일이 포함된 디렉터리의 경로(복수 지정 가능: 쉼표 구분).
   * - ``recursive``
     - ``false``
     - ``directories`` 를 하위 디렉터리까지 탐색할지 여부.
   * - ``max_depth``
     - ``10``
     - ``recursive=true`` 일 때, 각 디렉터리의 몇 계층 아래까지 내려갈지. ``0`` 을 지정하면 ``recursive=false`` 와 동일하게 동작합니다.
   * - ``include_pattern``
     -
     - 파일의 절대 경로가 완전히 일치해야 하는 정규 표현식.
   * - ``exclude_pattern``
     -
     - 파일의 절대 경로가 일치해서는 안 되는 정규 표현식.
   * - ``file_suffixes``
     - ``.json,.jsonl``
     - 대상으로 할 파일의 접미사(복수 지정 가능: 쉼표 구분). 대소문자를 구분하지 않습니다.
   * - ``file_encoding``
     - ``UTF-8``
     - 파일의 문자 인코딩.
   * - ``format``
     - ``auto``
     - 문서의 형식. ``auto`` , ``jsonl`` , ``json`` 중 하나.
   * - ``root_path``
     -
     - 레코드를 읽어들일 위치를 지정하는 JSON Pointer(예: ``/data/items`` ).

.. note::

   파라미터 이름은 스네이크 케이스로 기재했지만, 캐멀 케이스 표기
   ( ``file_encoding`` 에 대한 ``fileEncoding`` 등)도 동일하게 사용할 수 있습니다.

.. note::

   ``files`` 와 ``directories`` 중 적어도 하나를 지정하십시오.
   양쪽 모두 비어 있으면 오류가 발생합니다.
   양자는 배타적이지 않으며, 양쪽을 모두 지정한 경우 양쪽 모두 처리됩니다.
   같은 파일이 양쪽에서 도달하는 경우에도 읽어들이는 것은 1회뿐입니다.

파일 탐색 순서
~~~~~~~~~~~~~~

- ``files`` 로 지정한 파일은 지정한 순서대로 처리됩니다.
- ``directories`` 아래에서 발견된 파일은 수정 일시가 오래된 순서로 처리됩니다.
- ``files`` 로 지정한 파일은 ``directories`` 아래의 파일보다 먼저 처리됩니다.

``file_suffixes`` 에 의한 필터링은 ``files`` 로 직접 지정한 파일에도 적용됩니다.
접미사가 일치하지 않는 파일은 로그에 이유가 출력된 후 건너뜁니다.

존재하지 않는 경로, ``files`` 에 지정된 디렉터리, ``directories`` 에 지정된 파일은,
모두 경고로 로그에 기록되며, 크롤링 자체는 계속 진행됩니다.

``format``
----------

``auto`` 는 문서의 앞부분을 읽어 그 문법으로부터 형식을 판별합니다. 3가지 형식 중 어느
것이든, 올바르게 작성된 파일이라면 이 방법으로 판별할 수 있습니다.

``format=jsonl`` 을 명시하는 것은, JSON Lines 형식의 파일이면서 앞부분 근처의 행이
손상되어 있을 가능성이 있는 경우입니다(배너 행, 진행 로그, 전송이 도중에 끊긴 레코드 등).
자동 판별은 그런 행을 건너뛰어 판단해야 하기 때문입니다.

이 설정은 잘못된 레코드의 영향 범위도 결정합니다.

- **JSON Lines 형식**: 각 행이 독립적으로 파싱되므로, 잘못된 행의 비용은 그 행뿐입니다.
  실패는 ``<파일의 절대 경로>@<행 번호>`` 라는 키로 실패 URL에 기록되며,
  다음 행부터 그대로 처리가 계속됩니다.
- **그 외 형식**: 토큰 스트림으로 읽어들이기 때문에, 하나의 실패가 후속 레코드까지
  끌어들이는 경우가 있습니다. 오브젝트 도중에 끊긴 문서는 복구할 수 없으며,
  일정 횟수 연속으로 실패하면 해당 파일은 경고를 출력하고 중단됩니다.

``root_path``
-------------

중첩된 배열을 가리키는 JSON Pointer를 지정하면, 그 요소가 레코드로 등록됩니다.

::

    root_path=/data/items

.. code-block:: json

    { "meta": { "count": 2 }, "data": { "items": [ { "id": "1" }, { "id": "2" } ] } }

- 배열을 가리킨 경우, 그 요소마다 1개의 레코드가 됩니다.
- 오브젝트를 가리킨 경우, 그 오브젝트가 1개의 레코드가 됩니다.
- 어디에도 일치하지 않는 경우, 오류가 되지 않고 레코드가 0건이 됩니다.
- JSON Pointer의 이스케이프( ``~1`` 이 ``/`` , ``~0`` 이 ``~`` )를 사용할 수 있습니다.

``root_path`` 는 ``format`` 보다 우선됩니다. JSON Pointer로 도달한 문서는 행 단위로
읽어들이지 않기 때문이며, ``format=jsonl`` 과 동시에 지정한 경우에는 그 취지의 경고가
로그에 출력됩니다.

.. warning::

   ``root_path`` 는 ``/`` 로 시작해야 합니다. ``data/items`` 처럼 앞의 ``/`` 를
   빠뜨리면, JSON Pointer로 해석할 수 없어 데이터 설정 전체가 오류가 됩니다.
   이때 실패 URL은 파라미터 이름이 아니라 데이터 설정으로 기록되므로,
   어느 파라미터가 원인인지는 로그의
   ``JSON Pointer expression must start with '/'`` 를 통해 판단하십시오.

.. note::

   ``root_path`` 를 지정하지 않고, 레코드가 여러 행에 걸쳐 정형화된 문서
   (메타 정보와 배열을 포함하는 이른바 래퍼 형식)를 읽어들이면, 행 단위 파싱이
   시도되기 때문에 의도한 레코드를 가져오지 못하고 실패가 기록됩니다.
   그러한 문서에서는 ``root_path`` 를 지정하십시오.

스크립트 설정
-------------

각 필드의 값은 JSON 오브젝트의 각 필드 값을 참조하여 구성합니다.
JSON 오브젝트 최상위 레벨의 필드는 스크립트 내에서 **접두사 없는 변수**
로 직접 참조할 수 있습니다( ``data.`` 와 같은 접두사는 붙지 않습니다).

단순한 JSON 오브젝트:

::

    url="https://shop.example.com/product/" + id
    title=name
    content=description
    digest=description
    host="shop.example.com"
    site="shop.example.com"

중첩된 오브젝트는 맵, 중첩된 배열은 리스트로 참조할 수 있습니다:

::

    url="https://example.com/product/" + id
    title=product.name
    content=product.description
    price=product.pricing.amount
    first_tag=tags[0]

사용 가능한 필드
~~~~~~~~~~~~~~~~

- ``<필드명>`` - JSON 오브젝트 최상위 레벨의 필드를 이름으로 직접 참조합니다
- ``<부모>.<자식>`` - 중첩된 오브젝트의 필드
- ``<배열>[<인덱스>]`` - 배열 요소

.. note::

   필드의 값이 ``null`` 인 경우, 그 필드는 문서에 등록되지 않습니다.

.. note::

   |Fess| 15.9 부터 내장 스크립트 엔진이 JavaScript로 변경되었습니다.
   Groovy는 ``fess-script-groovy`` 플러그인으로 제공됩니다.
   사용할 엔진은 데이터 스토어의 파라미터 ``script_type`` 으로 지정합니다
   ( ``script_type=javascript`` 등). 생략한 경우에는 ``groovy`` 가 사용됩니다.
   위 예시와 같은 단순한 참조나 문자열 연결은 두 엔진 모두 동일하게 동작하지만,
   그 외의 표기법은 엔진에 따라 다릅니다.

주의 사항
=========

``app.encrypt.property.pattern`` 에 일치하는 이름의 파라미터(기본값에서는 ``password`` ,
``key`` , ``token`` , ``secret`` 으로 끝나는 것)는 스크립트에서는 ``null`` 로
참조됩니다. 데이터 스토어의 파라미터에 기재한 자격 증명이 인덱스
필드로 복사되는 것을 방지하기 위해서입니다.

같은 이름의 필드가 레코드 쪽에 있는 경우, 다른 파라미터와 마찬가지로 레코드 쪽의 값이
우선됩니다.

.. note::

   일치 판정은 파라미터 이름에 대한 대소문자를 구분하는 완전 일치입니다.
   ``access_token`` 은 대상이 되지만, 캐멀 케이스인 ``accessToken`` 은
   대상이 되지 않습니다. 자격 증명을 파라미터에 기재하는 경우에는 스네이크 케이스로
   기재하십시오.

잘못된 파라미터와 오류
======================

``format`` , ``include_pattern`` , ``exclude_pattern`` , ``urls`` 에 사용할 수 없는 값을
지정한 경우에는 파일을 읽어들이기 전에 크롤링이 종료되며, 해당 파라미터 이름을 포함한
실패 URL(예: ``JsonDataStore:format`` )이 기록됩니다.

``max_depth`` 에 숫자가 아닌 값을 지정한 경우에는 로그에 기록된 후 기본값이 사용됩니다.

.. note::

   데이터 스토어의 크롤링은 대상을 1건도 가져오지 못한 경우에도 작업으로서는
   정상 종료합니다. 가져온 건수가 예상과 다른 경우에는 인덱스 건수, 실패 URL,
   그리고 ``fess-crawler.log`` 를 확인하십시오.

사용 예
=======

제품 카탈로그
-------------

파라미터:

::

    files=/var/data/products.jsonl
    file_encoding=UTF-8

스크립트:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description
    digest=category
    host="shop.example.com"
    site="shop.example.com"

API 응답을 저장한 파일
-----------------------

파라미터:

::

    files=/var/data/response.json
    root_path=/data/items

스크립트:

::

    url="https://example.com/item/" + id
    title=title
    content=body
    host="example.com"
    site="example.com"

디렉터리를 재귀적으로 처리하기
-------------------------------

파라미터:

::

    directories=/var/data/exports
    recursive=true
    max_depth=3
    include_pattern=.*\.jsonl
    file_encoding=UTF-8

문제 해결
=========

파일을 찾을 수 없음
--------------------

**증상**: 로그에 ``... does not exist.`` , ``... is not a file.`` ,
``... is skipped because its suffix is not one of ...`` 가 출력됨

**확인 사항**:

1. 파일 경로가 올바른지 확인
2. 파일이 존재하는지 확인
3. 파일의 접미사가 ``file_suffixes`` (기본값은 ``.json`` 또는 ``.jsonl`` )에
   일치하는지 확인
4. |Fess| 실행 사용자에게 읽기 권한이 있는지 확인

JSON 파싱 오류
---------------

**증상**: 로그에 ``Failed to parse ...`` 나 ``Failed to read ...`` 가 출력되거나,
실패 URL이 기록됨

**확인 사항**:

1. 파일이 올바른 JSON인지 검증

   ::

       # JSON Lines 형식의 경우, 각 행이 유효한 JSON 오브젝트인지 검증
       cat data.jsonl | jq -c .

       # 배열이나 단일 오브젝트의 경우
       jq . data.json

2. 문자 인코딩이 올바른지 확인
3. 파일이 도중에 잘리지 않았는지 확인
4. 주석이 포함되어 있지 않은지 확인(JSON 표준에서는 주석 불가)

데이터를 가져올 수 없음
------------------------

**증상**: 크롤링은 성공하지만 건수가 0

**확인 사항**:

1. ``root_path`` 를 지정하고 있는 경우, 그 JSON Pointer가 문서의 구조와
   일치하는지 확인(일치하지 않는 경우 오류가 되지 않고 0건이 됩니다)
2. ``include_pattern`` , ``exclude_pattern`` , ``file_suffixes`` 로 대상이
   모두 제외되지 않았는지 확인. 이 경우에는 로그에 ``No sources to process`` 가
   출력됩니다
3. 스크립트 설정이 올바른지 확인(필드 참조가 ``data.`` 접두사 없이 되어 있는지)
4. 필드 이름이 올바른지 확인(대소문자 포함)
5. ``url`` 이 구성되어 있는지 확인. ``url`` 이 비어 있는 경우 레코드마다 실패로
   처리됩니다

문자 깨짐 발생
---------------

**증상**: 등록된 문서의 문자가 깨져 있음

``file_encoding`` 에 실제로 존재하지만 잘못된 인코딩을 지정한 경우, 오류가 되지 않고
문자가 깨진 채로 등록됩니다. 파일의 실제 인코딩을 확인하십시오.
존재하지 않는 인코딩 이름을 지정한 경우에는 파일마다 실패 URL이 기록됩니다.

대형 JSON 파일
---------------

**증상**: 메모리 부족 또는 타임아웃

레코드는 1건씩 읽어들이므로, 파일 전체의 크기가 직접 메모리 사용량에
영향을 미치지는 않습니다. 다만, 하나의 레코드가 극단적으로 큰 경우나,
인덱스 등록 부하가 높은 경우에는 문제가 발생할 수 있습니다.

**해결 방법**:

1. JSON 파일을 여러 개로 분할
2. |Fess| 의 힙 크기 증가

참고 정보
=========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-csv` - CSV 커넥터
- :doc:`ds-database` - 데이터베이스 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSON Lines <https://jsonlines.org/>`_
- `JSON Pointer (RFC 6901) <https://datatracker.ietf.org/doc/html/rfc6901>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
