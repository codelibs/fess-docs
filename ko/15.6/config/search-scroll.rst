==================
검색 결과 일괄 취득
==================

개요
====

|Fess| 의 일반 검색에서는 페이징 기능으로 일정 수의 검색 결과만 표시됩니다.
모든 검색 결과를 일괄로 취득하려면 스크롤 검색(Scroll Search) 기능을 이용합니다.

이 기능은 데이터의 일괄 내보내기나 백업, 대량 데이터 분석 등
모든 검색 결과를 처리해야 하는 경우 유용합니다.

활용 사례
============

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
========

스크롤 검색 활성화
----------------------

기본적으로 보안과 성능 관점에서 스크롤 검색은 비활성화되어 있습니다.
활성화하려면 ``app/WEB-INF/classes/fess_config.properties`` 또는 ``/etc/fess/fess_config.properties`` 에서
다음 설정을 변경합니다.

::

    api.search.scroll=true

.. note::
   설정 변경 후 |Fess| 를 재시작해야 합니다.

응답 필드 설정
--------------------------

검색 결과 응답에 포함할 필드를 사용자 정의할 수 있습니다.
기본적으로 많은 필드가 반환되지만 추가 필드를 지정할 수 있습니다.

::

    query.additional.scroll.response.fields=content

.. note::
   ``content`` 필드는 기본 응답에 포함되지 않습니다. 필요한 경우 위 설정으로 추가하십시오.

사용 방법
========

기본 사용 방법
----------------

스크롤 검색에 접근하려면 다음 URL로 실행합니다.

::

    http://localhost:8080/api/v1/documents/all?q=검색키워드

검색 결과는 NDJSON(Newline Delimited JSON) 형식으로 반환됩니다.
1행마다 1개의 문서가 JSON 형식으로 출력됩니다.

**예:**

::

    curl "http://localhost:8080/api/v1/documents/all?q=Fess"

요청 파라미터
--------------------

스크롤 검색에서는 다음 파라미터를 사용할 수 있습니다.

.. note::
   스크롤 검색은 GET 메서드만 지원합니다.

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
   ``num`` 의 최대값은 ``paging.search.page.max.size`` 설정에 의해 결정됩니다.

검색 쿼리 지정
----------------

일반 검색과 동일하게 검색 쿼리를 지정할 수 있습니다.

**예: 키워드 검색**

::

    curl "http://localhost:8080/api/v1/documents/all?q=검색엔진"

**예: 필드 지정 검색**

::

    curl "http://localhost:8080/api/v1/documents/all?q=title:Fess"

**예: 전체 취득(검색 조건 없음)**

::

    curl "http://localhost:8080/api/v1/documents/all?q=*:*"

취득 건수 지정
--------------

1회 스크롤로 취득할 건수를 변경할 수 있습니다.

::

    curl "http://localhost:8080/api/v1/documents/all?q=Fess&num=100"

.. note::
   ``num`` 파라미터를 너무 크게 하면 메모리 사용량이 증가합니다.
   최대값은 ``paging.search.page.max.size`` 설정(기본값: 100)에 의해 결정됩니다.

레이블에 의한 필터링
--------------------------

특정 레이블에 속하는 문서만 취득할 수 있습니다.

::

    curl "http://localhost:8080/api/v1/documents/all?q=*:*&fields.label=public"

인증에 대하여
--------------

.. warning::
   스크롤 검색에서는 |Fess| 의 역할 기반 접근 제어(RBAC)가 적용되지 않습니다.
   검색 조건에 일치하는 모든 문서가 사용자의 권한에 관계없이 반환됩니다.
   접근 제한이 필요한 경우 리버스 프록시 등에서 IP 주소 제한이나 인증을 설정하십시오.

응답 형식
==============

NDJSON 형식
----------

스크롤 검색의 응답은 NDJSON(Newline Delimited JSON) 형식으로 반환됩니다.
각 행이 1개의 문서를 나타냅니다.

**예:**

::

    {"url":"http://example.com/page1","title":"Page 1","content":"..."}
    {"url":"http://example.com/page2","title":"Page 2","content":"..."}
    {"url":"http://example.com/page3","title":"Page 3","content":"..."}

응답 필드
--------------------

기본적으로 포함되는 필드:

- ``url_link``: 표시용 URL
- ``content_description``: 콘텐츠 설명
- ``site_path``: 사이트 경로
- ``content_title``: 콘텐츠 제목
- ``content_length``: 콘텐츠 길이
- ``host``: 호스트명
- ``last_modified``: 최종 수정 날짜 및 시간
- ``timestamp``: 타임스탬프
- ``cache``: 캐시 데이터
- ``doc_id``: 문서 ID
- ``url``: 문서의 URL
- ``created``: 생성 날짜 및 시간
- ``site``: 사이트
- ``boost``: 부스트 값
- ``title``: 제목
- ``click_count``: 클릭 수
- ``mimetype``: MIME 타입
- ``favorite_count``: 즐겨찾기 수
- ``_id``: 내부 ID
- ``filetype``: 파일 유형
- ``filename``: 파일명
- ``score``: 검색 점수

.. note::
   ``content`` 필드는 기본 응답에 포함되지 않습니다.
   ``query.additional.scroll.response.fields=content`` 설정으로 추가할 수 있습니다.

데이터 처리 예
============

Python으로 처리하는 예
----------------

.. code-block:: python

    import requests
    import json

    # 스크롤 검색 실행
    url = "http://localhost:8080/api/v1/documents/all"
    params = {
        "q": "Fess",
        "num": 100
    }

    response = requests.get(url, params=params, stream=True)

    # NDJSON 형식의 응답을 1행씩 처리
    for line in response.iter_lines():
        if line:
            doc = json.loads(line)
            print(f"Title: {doc.get('title')}")
            print(f"URL: {doc.get('url')}")
            print("---")

파일에 저장
----------------

검색 결과를 파일에 저장하는 예:

.. code-block:: bash

    curl "http://localhost:8080/api/v1/documents/all?q=*:*" > all_documents.ndjson

CSV로 변환
-----------

jq 명령을 사용하여 CSV로 변환하는 예:

.. code-block:: bash

    curl "http://localhost:8080/api/v1/documents/all?q=Fess" | \
        jq -r '[.url, .title, .score] | @csv' > results.csv

데이터 분석
----------

취득한 데이터를 분석하는 예:

.. code-block:: python

    import json
    import pandas as pd
    from collections import Counter

    # NDJSON 파일 읽기
    documents = []
    with open('all_documents.ndjson', 'r') as f:
        for line in f:
            documents.append(json.loads(line))

    # DataFrame으로 변환
    df = pd.DataFrame(documents)

    # 기본 통계
    print(f"Total documents: {len(df)}")
    print(f"Average score: {df['score'].mean()}")

    # URL의 도메인 분석
    df['domain'] = df['url'].apply(lambda x: x.split('/')[2])
    print(df['domain'].value_counts())

성능 및 모범 사례
==================================

효율적인 사용 방법
----------------

1. **적절한 num 파라미터 설정**

   - 너무 작으면 통신 오버헤드가 증가
   - 너무 크면 메모리 사용량이 증가
   - 기본 최대값: 100

2. **검색 조건 최적화**

   - 필요한 문서만 취득하도록 검색 조건 지정
   - 전체 취득은 정말 필요한 경우에만 실행

3. **오프피크 시간 이용**

   - 대량 데이터 취득은 시스템 부하가 낮은 시간대에 실행

4. **배치 처리에서 이용**

   - 정기적인 데이터 동기화 등은 배치 작업으로 실행

메모리 사용량 최적화
--------------------

대량의 데이터를 처리하는 경우 스트리밍 처리를 사용하여 메모리 사용량을 억제합니다.

.. code-block:: python

    import requests
    import json

    url = "http://localhost:8080/api/v1/documents/all"
    params = {"q": "*:*", "num": 100}

    # 스트리밍으로 처리
    with requests.get(url, params=params, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                doc = json.loads(line)
                # 문서 처리
                process_document(doc)

보안 고려 사항
====================

접근 제한
------------

스크롤 검색은 대량의 데이터를 반환하므로 적절한 접근 제한을 설정하십시오.

1. **IP 주소 제한**

   특정 IP 주소에서만 접근 허용

2. **API 인증**

   API 토큰이나 Basic 인증 사용

3. **역할 기반 제한**

   특정 역할을 가진 사용자만 접근 허용

속도 제한
----------

과도한 접근을 방지하기 위해 리버스 프록시에서 속도 제한을 설정하는 것을 권장합니다.

문제 해결
======================

스크롤 검색을 이용할 수 없음
----------------------------

1. ``api.search.scroll`` 이 ``true`` 로 설정되어 있는지 확인하십시오.
2. |Fess| 를 재시작했는지 확인하십시오.
3. 오류 로그를 확인하십시오.

타임아웃 오류가 발생함
----------------------------

1. ``num`` 파라미터를 작게 하여 처리를 분산하십시오.
2. 검색 조건을 좁혀 취득하는 데이터 양을 줄이십시오.

메모리 부족 오류
----------------

1. ``num`` 파라미터를 작게 하십시오.
2. |Fess| 의 힙 메모리 크기를 늘리십시오.
3. OpenSearch의 힙 메모리 크기를 확인하십시오.

응답이 비어 있음
--------------------

1. 검색 쿼리가 올바른지 확인하십시오.
2. 지정한 레이블이나 필터 조건이 올바른지 확인하십시오.
3. 역할 기반 검색의 권한 설정을 확인하십시오.

참고 정보
========

- :doc:`search-basic` - 검색 기능 자세히 보기
- :doc:`search-advanced` - 검색 관련 설정
- `OpenSearch Scroll API <https://opensearch.org/docs/latest/api-reference/scroll/>`_
