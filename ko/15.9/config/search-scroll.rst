====================
검색 결과 일괄 취득
====================

개요
====

|Fess| 의 일반 검색에서는 페이징 기능으로 일정 수의 검색 결과만 표시됩니다.
모든 검색 결과를 일괄로 취득하려면 스크롤 검색(Scroll Search) 기능을 이용합니다.

이 기능은 데이터의 일괄 내보내기나 백업, 대량 데이터 분석 등
모든 검색 결과를 처리해야 하는 경우에 유용합니다.

활용 사례
=========

스크롤 검색은 다음과 같은 용도에 적합합니다.

- 검색 결과 전체 내보내기
- 데이터 분석용 대량 데이터 취득
- 배치 처리에서의 데이터 취득
- 외부 시스템으로의 데이터 동기화
- 리포트 생성용 데이터 수집

.. warning::
   스크롤 검색은 대량의 데이터를 반환하므로 일반 검색에 비해
   서버 리소스를 많이 소비합니다. 필요한 경우에만 활성화하십시오.

설정 방법
=========

스크롤 검색 활성화
------------------

기본적으로 보안과 성능 관점에서 스크롤 검색은 비활성화되어 있습니다.
활성화하려면 ``app/WEB-INF/classes/fess_config.properties`` (RPM/DEB 패키지의 경우
``/etc/fess/fess_config.properties`` )에서 다음 설정을 변경합니다.

::

    api.search.scroll=true

.. note::
   설정 변경 후 |Fess| 를 재시작해야 합니다.

스크롤 컨텍스트 유효 기간
--------------------------

스크롤 검색의 스크롤 컨텍스트 유효 기간은 |Fess| 내부에서 ``1m`` (1분)으로 고정되어 있습니다.
이 값은 ``fess_config.properties`` 에서 변경할 수 없습니다.

.. note::
   ``index.scroll.search.timeout`` 라는 설정이 있지만, 이는 인덱스의 업데이트·삭제를
   수반하는 내부 처리(update by query / delete by query)에서 사용되는 것으로,
   본 기능(검색 스크롤)의 타임아웃에는 영향을 주지 않습니다.

응답 필드 설정
--------------

검색 결과 응답에 포함할 필드를 사용자 정의할 수 있습니다.
기본적으로 많은 필드가 반환되지만 추가 필드를 지정할 수도 있습니다.

::

    query.additional.scroll.response.fields=content

여러 필드를 지정하는 경우 쉼표로 구분하여 나열합니다.

.. note::
   ``content`` 필드는 기본 응답에 포함되지 않습니다.
   전문을 취득하려면 위 설정으로 추가하십시오.

사용 방법
=========

기본 사용 방법
--------------

스크롤 검색에 접근하려면 다음 URL로 실행합니다.

::

    http://localhost:8080/api/v2/documents/all?q=검색키워드

검색 결과는 NDJSON(Newline Delimited JSON) 형식으로 반환됩니다.
1행마다 1개의 문서가 JSON 형식으로 출력됩니다.

**예:**

::

    curl "http://localhost:8080/api/v2/documents/all?q=Fess"

요청 파라미터
-------------

스크롤 검색에서는 다음 파라미터를 사용할 수 있습니다.

.. note::
   스크롤 검색은 GET 메서드만 지원합니다. GET 이외의 메서드로 접근하면
   ``405 Method Not Allowed`` 가 반환됩니다.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 파라미터 이름
     - 설명
   * - ``q``
     - 검색 쿼리(필수)
   * - ``num``
     - 1회 스크롤로 취득할 건수(기본값: 10, 최대: 100)
   * - ``fields.label``
     - 레이블에 의한 필터링

.. note::
   ``num`` 의 최대값은 ``paging.search.page.max.size`` (기본값: 100)로 제어됩니다.
   최대값을 초과하는 값을 지정하면 자동으로 최대값으로 잘립니다.
   기본값은 ``paging.search.page.size`` (기본값: 10)가 사용됩니다.
   ``num`` 에 0 이하의 값을 지정하면 오류( ``INVALID_REQUEST`` )가 반환됩니다.

검색 쿼리 지정
--------------

일반 검색과 동일하게 검색 쿼리를 지정할 수 있습니다.

**예: 키워드 검색**

::

    curl "http://localhost:8080/api/v2/documents/all?q=검색엔진"

**예: 필드 지정 검색**

::

    curl "http://localhost:8080/api/v2/documents/all?q=title:Fess"

**예: 전체 취득(검색 조건 없음)**

::

    curl "http://localhost:8080/api/v2/documents/all?q=*:*"

취득 건수 지정
--------------

1회 스크롤로 취득할 건수를 변경할 수 있습니다.

::

    curl "http://localhost:8080/api/v2/documents/all?q=Fess&num=100"

.. note::
   ``num`` 파라미터를 너무 크게 하면 메모리 사용량이 증가합니다.
   기본 최대값은 100입니다. 더 큰 값이 필요한 경우에는
   ``paging.search.page.max.size`` 설정을 변경하십시오.

레이블에 의한 필터링
--------------------

특정 레이블에 속하는 문서만 취득할 수 있습니다.

::

    curl "http://localhost:8080/api/v2/documents/all?q=*:*&fields.label=public"

접근 제어에 대하여
------------------

.. note::
   스크롤 검색에서도 일반 검색과 동일하게 역할 기반 접근 제어(RBAC)가 적용됩니다.
   요청의 역할 정보를 기반으로 접근 가능한 문서만 반환되므로
   열람 권한이 없는 문서는 결과에 포함되지 않습니다.

.. warning::
   스크롤 검색 엔드포인트는 기본적으로 인증을 요구하지 않습니다(누구나 접근 가능합니다).
   단, 반환되는 문서는 위의 역할 기반 접근 제어에 의해 필터링됩니다.
   엔드포인트 자체에 대한 접근을 제한하려면 리버스 프록시 등에서 IP 주소 제한이나
   인증을 설정하십시오.

응답 형식
=========

NDJSON 형식
-----------

스크롤 검색의 응답은 NDJSON(Newline Delimited JSON) 형식으로 반환됩니다.
Content-Type 은 ``application/x-ndjson; charset=UTF-8`` 입니다.
각 행은 ``{"data": {...}}`` 형식으로 래핑된 1개의 문서를 나타냅니다.

**예:**

::

    {"data":{"url":"http://example.com/page1","title":"Page 1","digest":"..."}}
    {"data":{"url":"http://example.com/page2","title":"Page 2","digest":"..."}}
    {"data":{"url":"http://example.com/page3","title":"Page 3","digest":"..."}}

.. note::
   각 문서는 ``data`` 키 아래에 저장됩니다. 클라이언트 측에서는 각 행을 파싱한 후
   ``data`` 키의 값을 참조하십시오.

오류 발생 시의 동작
-------------------

스트림 전송 시작 후 서버 측에서 오류가 발생한 경우, 응답의 마지막 행에
다음과 같은 오류 종단 행이 출력됩니다.

::

    {"error":{"code":"internal_error","message":"stream error"}}

.. note::
   클라이언트 측에서는 마지막 행에 ``error`` 키가 포함되어 있는지 확인함으로써
   「스트림이 정상적으로 완료되었는지」아니면 「서버 측에서 중간에 오류가 발생했는지」를
   판별할 수 있습니다. 또한 오류 종단 행의 기록 자체가 실패한 경우에는 종단 행이 출력되지 않고
   스트림이 중간에 종료되므로 예기치 않은 연결 끊김도 오류로 처리하십시오.

응답 필드
---------

기본적으로 포함되는 필드:

- ``score``: 검색 점수
- ``_id``: 문서 ID(OpenSearch 의 문서 ID)
- ``doc_id``: 문서 ID( |Fess| 내부)
- ``boost``: 부스트 값
- ``content_length``: 콘텐츠 길이
- ``host``: 호스트명
- ``site``: 사이트
- ``last_modified``: 최종 수정 날짜 및 시간
- ``timestamp``: 타임스탬프
- ``mimetype``: MIME 타입
- ``filetype``: 파일 유형
- ``filename``: 파일명
- ``created``: 생성 날짜 및 시간
- ``title``: 제목
- ``digest``: 본문 발췌
- ``url``: 문서의 URL
- ``thumbnail``: 썸네일
- ``click_count``: 클릭 수
- ``favorite_count``: 즐겨찾기 수
- ``has_cache``: 캐시 유무
- ``content_title``: 표시용 제목
- ``content_description``: 표시용 본문 발췌
- ``url_link``: 표시용 링크 URL
- ``site_path``: 사이트 경로

.. note::
   실제로 출력되는 필드는 API 응답으로 허용된 필드에 한정됩니다.
   값이 존재하지 않는 필드는 출력되지 않습니다.

.. note::
   ``content`` (전문)은 기본적으로 포함되지 않습니다.
   ``query.additional.scroll.response.fields`` 로 추가할 수 있습니다.

데이터 처리 예
==============

Python으로 처리하는 예
----------------------

.. code-block:: python

    import requests
    import json

    # 스크롤 검색 실행
    url = "http://localhost:8080/api/v2/documents/all"
    params = {
        "q": "Fess",
        "num": 100
    }

    response = requests.get(url, params=params, stream=True)

    # NDJSON 형식의 응답을 1행씩 처리
    for line in response.iter_lines():
        if line:
            record = json.loads(line)
            if "error" in record:
                # 스트림 도중에 오류 발생
                print("stream error:", record["error"])
                break
            doc = record["data"]
            print(f"Title: {doc.get('title')}")
            print(f"URL: {doc.get('url')}")
            print("---")

파일에 저장
-----------

검색 결과를 파일에 저장하는 예:

.. code-block:: bash

    curl "http://localhost:8080/api/v2/documents/all?q=*:*" > all_documents.ndjson

CSV로 변환
----------

jq 명령을 사용하여 CSV로 변환하는 예:

.. code-block:: bash

    curl "http://localhost:8080/api/v2/documents/all?q=Fess" | \
        jq -r '.data | [.url, .title, .score] | @csv' > results.csv

데이터 분석
-----------

취득한 데이터를 분석하는 예:

.. code-block:: python

    import json
    import pandas as pd

    # NDJSON 파일 읽기(각 행의 data 키를 꺼냄)
    documents = []
    with open('all_documents.ndjson', 'r') as f:
        for line in f:
            record = json.loads(line)
            if "data" in record:
                documents.append(record["data"])

    # DataFrame으로 변환
    df = pd.DataFrame(documents)

    # 기본 통계
    print(f"Total documents: {len(df)}")
    print(f"Average score: {df['score'].mean()}")

    # URL의 도메인 분석
    df['domain'] = df['url'].apply(lambda x: x.split('/')[2])
    print(df['domain'].value_counts())

성능 및 모범 사례
=================

효율적인 사용 방법
------------------

1. **적절한 num 파라미터 설정**

   - 너무 작으면 통신 오버헤드가 증가
   - 너무 크면 메모리 사용량이 증가
   - 기본 최대값: 100

2. **검색 조건 최적화**

   - 필요한 문서만 취득하도록 검색 조건 지정
   - 전체 취득은 정말 필요한 경우에만 실행

3. **오프피크 시간 활용**

   - 대량 데이터 취득은 시스템 부하가 낮은 시간대에 실행

4. **배치 처리에서 활용**

   - 정기적인 데이터 동기화 등은 배치 작업으로 실행

메모리 사용량 최적화
--------------------

대량의 데이터를 처리하는 경우 스트리밍 처리를 사용하여 메모리 사용량을 억제합니다.

.. code-block:: python

    import requests
    import json

    url = "http://localhost:8080/api/v2/documents/all"
    params = {"q": "*:*", "num": 100}

    # 스트리밍으로 처리
    with requests.get(url, params=params, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                record = json.loads(line)
                if "error" in record:
                    break
                # 문서 처리
                process_document(record["data"])

보안 고려 사항
==============

접근 제한
---------

스크롤 검색은 대량의 데이터를 반환하므로 적절한 접근 제한을 설정하십시오.
엔드포인트 자체는 기본적으로 인증을 요구하지 않으므로 필요에 따라 다음과 같은
대책을 검토하십시오.

1. **IP 주소 제한**

   특정 IP 주소에서만 접근 허용

2. **API 인증**

   리버스 프록시 등에서 API 토큰이나 Basic 인증 사용

3. **역할 기반 접근 제어**

   반환되는 문서는 |Fess| 의 역할 기반 접근 제어에 의해 필터링됩니다

속도 제한
---------

과도한 접근을 방지하기 위해 리버스 프록시에서 속도 제한을 설정하는 것을 권장합니다.

문제 해결
=========

스크롤 검색을 이용할 수 없음
----------------------------

1. ``api.search.scroll`` 이 ``true`` 로 설정되어 있는지 확인하십시오.
2. |Fess| 를 재시작했는지 확인하십시오.
3. 오류 로그를 확인하십시오.

타임아웃 오류가 발생함
----------------------

1. ``num`` 파라미터를 작게 하여 처리를 분산하십시오.
2. 검색 조건을 좁혀 취득하는 데이터 양을 줄이십시오.

메모리 부족 오류
----------------

1. ``num`` 파라미터를 작게 하십시오.
2. |Fess| 의 힙 메모리 크기를 늘리십시오.
3. OpenSearch의 힙 메모리 크기를 확인하십시오.

응답이 비어 있음
----------------

1. 검색 쿼리가 올바른지 확인하십시오.
2. 지정한 레이블이나 필터 조건이 올바른지 확인하십시오.
3. 역할 기반 접근 제어로 인해 열람 권한이 없는 문서는 결과에 포함되지 않습니다. 요청의 역할 설정을 확인하십시오.

참고 정보
=========

- :doc:`search-basic` - 검색 기능 자세히 보기
- :doc:`search-advanced` - 검색 관련 설정
- `OpenSearch Scroll API <https://opensearch.org/docs/latest/api-reference/scroll/>`_
