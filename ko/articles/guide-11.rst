=================================
검색 API로 업무 시스템과 연계하기
=================================

들어가며
========

CRM의 고객 화면에 관련 자료를 나열하고 싶다, 문의 접수 화면에서 비슷한 FAQ를 먼저 보여 주고 싶다, 자사 시스템이 만드는 보고서도 검색 대상으로 삼고 싶다.
이러한 요구는 업무 시스템의 서버에서 Fess의 검색 API(\ ``/api/v2``\ )를 호출하여 실현할 수 있습니다.

이 글에서는 Fess 15.9를 대상으로 다음 작업을 차례로 진행합니다.

- curl로 검색, 라벨, 추천, 인기 검색어 API를 호출하여 응답의 형태를 확인한다
- 액세스 토큰을 만들고, 토큰의 역할로 반환되는 문서를 제어한다
- 업무 시스템의 서버 측에서 검색 API를 호출하는 함수를 작성한다
- 크롤링할 수 없는 데이터를 ``PUT /api/admin/documents/bulk``\ 로 등록한다
- 오류와 속도 제한에 대비한다

기존 웹 사이트에 검색창이나 검색 화면을 넣는 방법(브라우저 측 삽입, 테마, Fess Site Search)은 :doc:`guide-03`\ 에서 다룹니다.
아직 Fess를 시작하고 크롤링하지 않았다면 먼저 :doc:`guide-02`\ 를 마치십시오.

이 글에서 만드는 구성
=====================

::

    [사용자의 브라우저] --> [업무 시스템의 서버] --(토큰 포함)--> [Fess /api/v2]
                               토큰은 여기에만 둔다

브라우저가 접근하는 것은 업무 시스템뿐이며, Fess를 호출하는 것은 업무 시스템의 서버입니다.
액세스 토큰은 서버의 환경 변수 등에 두고 브라우저에는 넘기지 않습니다.
이유는 "액세스 토큰 만들기"에서 설명합니다.

API의 전체 구성
===============

Fess 15.9 본체가 제공하는 검색 관련 API는 ``/api/v2`` 아래에 있습니다.
이 글에서 사용하는 API는 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 엔드포인트
     - 용도
   * - ``GET /api/v2/search``
     - 전문 검색. 결과는 ``response.data``\ 에 들어갑니다
   * - ``GET /api/v2/labels``
     - 호출자가 사용할 수 있는 라벨 목록
   * - ``GET /api/v2/suggest-words``
     - 입력 중인 단어에 대한 추천 후보
   * - ``GET /api/v2/popular-words``
     - 인기 검색어
   * - ``GET /api/v2/health``
     - 검색 엔진의 상태(모니터링에서의 사용법은 :doc:`guide-10`)
   * - ``PUT /api/admin/documents/bulk``
     - 문서 일괄 등록(관리 API)

``/api/v2``\ 의 응답은 모두 ``{"response": {...}}``\ 로 감싸져 있으며, ``response.status``\ 가 0이면 성공입니다.
JSON 키는 ``snake_case``\ 입니다.

.. note::

   15.9 본체는 ``/api/v1``\ 을 제공하지 않습니다.
   ``/api/v1``\ 을 호출하는 기존 클라이언트를 계속 동작시키려면 플러그인 ``fess-webapp-v1-api``\ 가 필요합니다(Docker 이미지에는 포함되어 있지 않습니다).
   새로 만드는 연계에는 ``/api/v2``\ 를 사용하십시오.

먼저 curl로 시험하기
====================

익명으로 검색할 수 있는 상태([시스템] > [일반]의 "로그인 필요"가 꺼짐, 기본 상태)라면 토큰 없이 호출할 수 있습니다.
한국어 등 ASCII가 아닌 문자나 공백이 들어간 검색어는 ``-G --data-urlencode``\ 로 URL 인코딩하여 보냅니다.
출력을 읽기 쉽게 하기 위해 ``jq``\ 를 사용합니다.

::

    $ curl -s -G "http://localhost:8080/api/v2/search" \
        --data-urlencode "q=검색 가이드" \
        --data-urlencode "num=3" \
      | jq '.response | {status, record_count, page_size, data: [.data[] | {doc_id, title, url_link, content_description}]}'

응답은 다음과 같은 형태입니다(``data``\ 는 첫 번째 1건만 표시했습니다. 값은 환경에 따라 달라집니다).

.. code-block:: json

    {
      "status": 0,
      "record_count": 12,
      "page_size": 3,
      "data": [
        {
          "doc_id": "5d4c0e0e5a7b4b5c9d2f6a1b3c8e7f90",
          "title": "검색 가이드",
          "url_link": "https://fess.codelibs.org/ko/stable/user/index.html",
          "content_description": "Fess <strong>검색</strong> <strong>가이드</strong>입니다. ..."
        }
      ]
    }

``response``\ 에는 그 밖에 ``page_count``, ``next_page``, ``exec_time``, ``query_id`` 등이 들어갑니다.
``data``\ 의 각 요소에 들어가는 것은 ``title``, ``url``, ``url_link``, ``content_description``, ``last_modified``, ``filetype``, ``score`` 등 API 응답용으로 허용된 필드뿐입니다.
본문 전체(\ ``content``\ )와 라벨(\ ``label``\ )은 기본적으로 반환되지 않습니다.
반환할 필드를 늘리려면 ``fess_config.properties``\ 의 ``query.additional.api.response.fields``\ 에 추가합니다.
``content_description``\ 은 검색어를 ``<strong>`` 태그로 감싼 발췌이므로, 화면에 표시할 때는 HTML로 다루거나 태그를 제거하십시오.

자주 사용하는 파라미터는 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 파라미터
     - 의미
   * - ``q``
     - 검색어. 검색 화면과 같은 구문(AND, OR, 제외, 필드 지정 등)을 사용할 수 있습니다
   * - ``num`` / ``start``
     - 1페이지당 건수(기본값 10, 상한을 넘으면 상한으로 조정됩니다)와 시작 위치(0부터 시작)
   * - ``sort``
     - 정렬 순서. 예: ``last_modified.desc``\ (갱신 일시가 최신인 순)
   * - ``fields.label``
     - 라벨 값으로 범위를 좁힙니다. 여러 번 지정할 수 있습니다

그 밖의 파라미터(패싯, 언어, 위치 정보 등)는 `검색 API <https://fess.codelibs.org/ko/stable/api/api-search.html>`__\ 를 참조하십시오.

라벨, 추천, 인기 검색어도 같은 요령으로 호출할 수 있습니다.

::

    $ curl -s "http://localhost:8080/api/v2/labels" | jq .response
    $ curl -s -G "http://localhost:8080/api/v2/suggest-words" --data-urlencode "q=fe" | jq .response
    $ curl -s "http://localhost:8080/api/v2/popular-words" | jq .response

각각 ``response.labels[]``\ (\ ``label``\ 과 ``value``\ ), ``response.suggest_words[]``\ (\ ``text``\ 와 ``types``\ ), ``response.popular_words``\ (문자열 배열)에 결과가 들어갑니다.
추천과 인기 검색어가 비어 있는 이유는 "라벨, 추천, 인기 검색어 사용하기"에서 설명합니다.

액세스 토큰 만들기
==================

업무 시스템에서 호출할 때는 액세스 토큰을 사용합니다.
토큰에는 "권한"을 부여하며, 그 권한으로 검색 결과가 좁혀집니다.

작성 절차
---------

1. 관리 화면의 [시스템] > [액세스 토큰]을 열고 [새로 만들기]를 클릭합니다.
2. "이름"에 용도를 알 수 있는 이름(예: ``crm-search``)을 입력합니다.
3. "권한"에 이 토큰으로 보여도 되는 문서의 역할을 한 줄에 하나씩 적습니다. 형식은 ``{role}역할명``, ``{group}그룹명``, ``{user}사용자명``\ 입니다.
4. "만료"를 ``2027-03-31T23:59:59`` 형식으로 입력합니다. 비워 두면 기한이 없습니다.
5. "파라미터 이름"은 비워 둡니다.
6. [작성]을 클릭합니다. 목록으로 돌아오면 이름을 클릭하고, 상세 화면의 "토큰"에 표시되는 값(영숫자 60자)을 메모해 둡니다.

"파라미터 이름"을 설정하면 호출 측이 그 요청 파라미터로 권한을 추가할 수 있게 됩니다.
호출 측을 완전히 관리할 수 있는 경우가 아니면 사용하지 마십시오.

토큰 보내는 방법
----------------

토큰은 ``Authorization`` 헤더로 보냅니다.
``Bearer``\ 를 붙이지 않은 ``Authorization: <토큰>``\ 도 받아들입니다.

::

    $ export FESS_SEARCH_TOKEN=<메모한 토큰>
    $ curl -s -G "http://localhost:8080/api/v2/search" \
        -H "Authorization: Bearer $FESS_SEARCH_TOKEN" \
        --data-urlencode "q=제안서" | jq '.response.record_count'

쿼리 파라미터로 토큰을 넘기는 방법은 ``api.access.token.request.parameter``\ 가 기본적으로 비어 있으므로 사용할 수 없습니다.
URL은 액세스 로그에 남으므로 헤더를 사용하십시오.

토큰의 역할로 결과가 정해진다
-----------------------------

토큰이 포함된 요청에서는 토큰의 권한만 역할로 사용됩니다.
토큰 없이 익명으로 호출할 때 붙는 게스트 역할(\ ``{role}guest``\ )은 토큰의 권한이 비어 있지 않는 한 붙지 않습니다.

한편, 크롤링 설정을 새로 만들면 권한 항목에 ``{role}guest``\ 가 들어 있으므로, 일반적인 공개 문서에는 ``{role}guest``\ 가 붙어 있습니다.
따라서 권한을 ``{group}sales``\ 만으로 한 토큰에서는 공개 문서가 검색 결과에서 사라집니다.
공개 문서와 영업부용 문서를 모두 반환하려면 토큰의 권한을 다음과 같이 2줄로 합니다.

::

    {role}guest
    {group}sales

설정했으면 같은 검색어로 토큰 없이 호출했을 때와 토큰을 붙였을 때의 ``record_count``\ 를 비교하여, 예상대로 늘거나 주는지 확인하십시오.
문서 측 권한의 설계는 :doc:`guide-05`\ 에서 다룹니다.

브라우저에 토큰을 넘기지 않는 이유
----------------------------------

- 브라우저의 JavaScript에 적은 토큰은 개발자 도구로 누구나 읽을 수 있습니다. 읽어 낸 사람은 토큰의 권한으로 보이는 문서를 모두, 업무 시스템을 거치지 않고 검색할 수 있습니다.
- 토큰은 사용자별로 주어지는 것이 아니라, 발급할 때 지정한 권한을 하나로 묶은 것입니다. 브라우저에 배포하면 사용자별 권한 차이가 없어집니다.
- "로그인 필요"를 켜 두어도, 유효한 토큰이 있으면 ``/search``, ``/documents/all``, ``/documents/export``, ``/suggest-words``, ``/labels``, ``/popular-words``\ 는 로그인 없이 응답합니다. 유출된 토큰은 로그인 대신 사용될 수 있습니다.

업무 시스템의 사용자에 따라 보여 줄 범위를 바꾸고 싶다면, 범위마다 토큰을 나누고 서버 측에서 사용자에 맞게 골라 씁니다.

서버 측에서 검색 API 호출하기
=============================

업무 시스템의 백엔드에 두는 Python 함수의 예입니다.
표준 라이브러리만 사용하며, 검색 결과를 화면에 필요한 항목만으로 줄여서 반환합니다.

.. code-block:: python

    import json
    import os
    import urllib.error
    import urllib.parse
    import urllib.request

    FESS_URL = os.environ.get("FESS_URL", "http://localhost:8080")
    FESS_SEARCH_TOKEN = os.environ["FESS_SEARCH_TOKEN"]


    class FessApiError(Exception):
        def __init__(self, http_status, code, retry_after=None):
            super().__init__(f"Fess API error: {http_status} {code}")
            self.http_status = http_status
            self.code = code
            self.retry_after = retry_after


    def search_documents(query, label=None, num=5):
        params = [("q", query), ("num", str(num))]
        if label:
            params.append(("fields.label", label))
        url = FESS_URL + "/api/v2/search?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + FESS_SEARCH_TOKEN})
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                body = json.load(res)
        except urllib.error.HTTPError as e:
            try:
                code = json.load(e)["response"]["error"]["code"]
            except (ValueError, KeyError, TypeError):
                code = "unknown"
            raise FessApiError(e.code, code, e.headers.get("Retry-After")) from e
        response = body["response"]
        return {
            "total": response["record_count"],
            "items": [
                {
                    "title": doc.get("title"),
                    "url": doc.get("url_link"),
                    "snippet": doc.get("content_description"),
                    "last_modified": doc.get("last_modified"),
                }
                for doc in response["data"]
            ],
        }

CRM의 고객 화면이라면 ``search_documents("주식회사 샘플", label="sales_docs")``\ 처럼 고객명과 라벨을 넘기고, 반환값을 그대로 화면에 그립니다.

- 타임아웃은 Fess 측의 검색 타임아웃(\ ``query.timeout``\ , 기본값 10000밀리초)보다 조금 길게 잡았습니다.
- ``FessApiError``\ 의 ``code``\ 와 ``retry_after``\ 를 보고 사용자에게 보여 줄 메시지와 재시도 여부를 정합니다("오류 대처" 참조).
- ``content_description``\ 은 ``<strong>`` 태그를 포함하므로, 템플릿에서 HTML로 출력하는 경우에는 허용하는 태그를 ``<strong>``\ 으로 제한하십시오.

외부 시스템의 데이터 등록하기
=============================

크롤링할 수 없는 데이터(업무 시스템이 생성하는 보고서, 티켓 요약 등)는 관리 API의 ``PUT /api/admin/documents/bulk``\ 로 인덱스에 직접 등록할 수 있습니다.

관리 API용 토큰을 따로 만들기
-----------------------------

관리 API에는 권한에 ``{role}admin-api``\ 를 가진 토큰이 필요합니다(\ ``api.admin.access.permissions=Radmin-api``\ ).
이 권한으로는 관리 API의 모든 엔드포인트가 허용됩니다.
문서 등록만으로 한정한 권한은 없습니다.
크롤링 설정, 사용자, 액세스 토큰 자체도 조작할 수 있으므로 관리자 비밀번호와 마찬가지로 다루어 보관하십시오.

또한 ``{role}admin-api``\ 만 가진 토큰으로 검색하면 역할이 ``admin-api``\ 뿐이므로 대부분의 문서가 반환되지 않습니다.
검색용과 등록용으로 토큰을 나누십시오.
[시스템] > [액세스 토큰]에서 권한을 ``{role}admin-api`` 한 줄만으로 한 토큰(예: 이름 ``crm-indexer``)을 하나 더 만들고 값을 메모해 둡니다.

::

    $ export FESS_ADMIN_TOKEN=<메모한 관리 API용 토큰>

등록하기
--------

``url``\ 과 ``title``\ 은 필수입니다.
``content``\ 는 본문, ``label``\ 은 라벨 값의 배열입니다.

::

    $ curl -s -X PUT "http://localhost:8080/api/admin/documents/bulk" \
        -H "Authorization: Bearer $FESS_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "documents": [
            {
              "url": "https://crm.example.com/reports/2026-11",
              "title": "2026년 11월 영업 월간 보고서",
              "content": "11월 신규 영업 기회는 전월보다 늘었습니다.",
              "label": ["sales_docs"]
            }
          ]
        }' | jq .response

성공하면 문서별 결과가 ``items``\ 에 반환됩니다.
새로 만든 경우는 ``CREATED``, 기존 문서를 갱신한 경우는 ``OK``\ 입니다.

.. code-block:: json

    {
      "version": "15.9",
      "status": 0,
      "items": [
        { "result": "CREATED", "id": "9c1e47b2...e04b" }
      ]
    }

``id``\ 는 ``url`` 등으로 계산한 해시 값(16진수 128자리)이며, 위의 예에서는 중간을 생략했습니다.
등록한 문서는 검색용 토큰으로 ``q=영업 월간 보고서``\ 를 검색하여 찾을 수 있으면 완료입니다.

등록 시 주의 사항
-----------------

- ``role``\ 을 생략하면 게스트 역할이 붙어 누구나 검색할 수 있는 문서가 됩니다. 보여 줄 범위를 제한하려면 ``role``\ 에 내부 형식의 값을 배열로 넣습니다. 내부 형식은 ``{role}x``\ 가 ``Rx``, ``{group}x``\ 가 ``2x``, ``{user}x``\ 가 ``1x``\ 입니다(예: ``"role": ["2sales"]``).
- 문서의 ID는 ``url``\ 과 ``role``\ (그리고 가상 호스트)로 만들어집니다. 같은 ``url``\ 로 다시 보내면 갱신되지만, ``role``\ 을 바꾸어 보내면 별개의 문서로 추가되어 이전 문서가 남습니다.
- 응답의 ``items[].id``\ 는 인덱스상의 ID이며, 문서의 ``doc_id``\ 와는 다른 값입니다. 1건씩 삭제하는 ``DELETE /api/admin/searchlist/doc/{id}``\ 에는 검색 결과의 ``doc_id``\ 를 넘깁니다. 조건으로 한꺼번에 지우려면 ``DELETE /api/admin/searchlist/query``\ 를 사용합니다(\ `SearchList API <https://fess.codelibs.org/ko/stable/api/admin/api-admin-searchlist.html>`__\ ).
- 일부 문서만 실패한 경우에는 ``status``\ 가 9가 되고, 실패한 요소에 ``message``\ 가 들어갑니다. ``url``\ 이나 ``title``\ 의 누락, 형이 맞지 않는 값 등 요청 자체가 잘못된 경우에는 ``status``\ 가 1이 되고 아무것도 등록되지 않습니다.

라벨, 추천, 인기 검색어 사용하기
================================

라벨로 카테고리 만들기
----------------------

``fields.label``\ 로 범위를 좁히는 라벨은 [크롤러] > [라벨]에서 만듭니다.
"값"에 사용할 수 있는 문자는 영숫자와 밑줄뿐입니다(\ ``sales-docs``\ 나 한국어 등 ASCII가 아닌 문자는 사용할 수 없습니다).
크롤링한 문서에는 라벨의 "대상 경로"에 URL이 일치할 때 라벨이 붙습니다(:doc:`guide-04`).
bulk로 등록하는 문서에는 앞 절처럼 ``label``\ 을 보냅니다.

``/api/v2/labels``\ 는 호출자의 역할로 사용할 수 있는 라벨만 반환합니다.
라벨에도 권한이 있으므로 토큰의 권한과 맞지 않는 라벨은 목록에 나오지 않습니다.
포털의 카테고리 목록은 이 응답의 ``label``\ (표시 이름)과 ``value``\ (\ ``fields.label``\ 에 넘기는 값)로 만듭니다.

추천
----

``/api/v2/suggest-words``\ 는 ``q``\ 의 전방 일치로 후보를 반환합니다.
건수는 ``num``\ (기본값 10)으로 정하고, 대상 필드는 ``fn``\ 을 반복하여 지정합니다.
후보의 출처는 크롤링한 문서의 단어([시스템] > [일반]의 "문서로 추천"), 검색어(같은 화면의 "검색어로 추천"), 관리자가 등록한 추천 단어입니다.
문서의 단어는 스케줄러의 "Suggest Indexer" 작업(기본적으로 하루 1회)이 실행될 때까지 후보에 나오지 않습니다.
후보도 호출자의 역할로 좁혀집니다.

인기 검색어
-----------

``/api/v2/popular-words``\ 는 검색 로그에서 모은 검색어 중 자주 검색된 단어를 반환합니다.
빈 배열이 반환되는 경우에는 다음 사항을 확인하십시오.

- [시스템] > [일반]의 "인기 검색어 응답"(\ ``web.api.popularword``\ , 기본값 켬)이 꺼져 있으면 ``invalid_request``\ (HTTP 400)가 됩니다.
- "검색어로 추천"이 켜져 있을 것. 검색어는 이 설정이 켜져 있을 때만 수집됩니다.
- 같은 단어가 10회 이상 검색되었을 것(\ ``suggest.popular.word.query.freq=10``\ ). 같은 세션에서 반복한 검색은 1분 이내라면 1회로 셉니다. 도입 직후에는 비어 있는 것이 보통입니다.
- 집계 대상은 게스트 역할만으로 수행된 검색입니다(\ ``suggest.search.log.permissions={user}guest,{role}guest``\ ). ``{group}sales`` 등을 가진 토큰이나 로그인한 사용자의 검색은 세지 않습니다.
- 인기 검색어도 호출자의 역할로 좁혀집니다. 집계되는 단어에는 게스트 역할만 붙으므로, 권한에 ``{role}guest``\ 를 포함하지 않는 토큰에서는 항상 비어 있습니다.
- 결과는 캐시되므로 검색이 늘어도 바로 바뀌지는 않습니다.

``seed``\ 를 바꾸면 후보 중에서 다른 조합이 반환됩니다.

오류 대처
=========

``/api/v2``\ 는 오류 시 HTTP 상태와 ``response.error.code``\ 를 반환합니다.

::

    {"response": {"status": 1, "error": {"code": "invalid_request", "message": "..."}}}

연계하는 쪽에서 처리 방법을 정해 두어야 할 것은 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - HTTP
     - ``error.code``
     - 원인과 대처
   * - 400
     - ``invalid_request``
     - ``num``\ 이 0 이하, 검색어의 구문 오류, ``q``\ 가 ``api.param.max.length``\ (기본값 1000자)를 넘은 경우 등. 재시도하지 말고 입력을 재검토합니다
   * - 401
     - ``auth_required``
     - 등록되지 않았거나 기한이 지난 토큰, 또는 "로그인 필요"가 켜져 있는데 토큰이 없음. 유효하지 않은 토큰을 붙이면 익명 취급으로 돌아가지 않고 401이 됩니다. 토큰을 다시 만듭니다
   * - 503
     - ``service_unavailable``
     - 검색 엔진이 처리하지 못해 검색을 거부했습니다. ``Retry-After: 5``\ 가 붙으므로 5초 기다린 뒤 재시도할 수 있습니다
   * - 500
     - ``internal_error``
     - Fess 내부 오류. [시스템 정보] > [로그 파일]의 ``fess.log``\ 를 확인합니다

속도 제한은 로그인, 비밀번호 변경, 채팅, 내보내기의 각 엔드포인트에 개별 상한이 있으며, 넘으면 429 ``rate_limited``\ 와 ``Retry-After``\ 가 반환됩니다.
서버 전체의 요청 수 제한(\ ``rate.limit.enabled``\ )은 기본적으로 비활성화되어 있습니다.
활성화한 경우 초과 시 429의 본문은 ``{"error":"rate_limit_exceeded", ...}``\ 이며, 위의 ``response`` 형태가 아닙니다.
업무 시스템의 서버에서 호출하는 경우, 모든 검색이 같은 IP 주소에서 도착한다는 점에 주의하십시오.
자세한 내용은 `속도 제한 설정 <https://fess.codelibs.org/ko/stable/config/rate-limiting.html>`__\ 을 참조하십시오.

관리 API(\ ``/api/admin/*``\ )에서는 오류의 형태가 다릅니다.
토큰이 없거나 ``{role}admin-api``\ 를 가지지 않은 경우에는 HTTP 401이며, ``response.status``\ 가 3, 이유는 ``response.message``\ 에 들어갑니다.

브라우저에서 직접 호출하는 경우(CORS)
=====================================

서버 간 호출에는 CORS가 관계없습니다.
브라우저의 JavaScript에서 다른 출처의 Fess를 직접 호출하는 경우에만 ``fess_config.properties``\ 의 ``api.cors.allow.origin``\ (기본값 ``*``), ``api.cors.allow.methods``, ``api.cors.allow.headers``\ (기본적으로 ``Authorization`` 포함), ``api.cors.allow.credentials``\ (기본값 ``true``), ``api.cors.max.age``\ (기본값 ``3600``\ 초)가 적용됩니다.

``api.cors.allow.origin``\ 이 ``*``\ 일 때는 Cookie 등 인증 정보가 포함된 요청이 허용되지 않습니다.
로그인한 사용자의 권한으로 브라우저에서 검색하게 하려면 ``https://portal.example.com``\ 처럼 출처를 나열합니다(쉼표 구분).
Docker에서는 ``FESS_JAVA_OPTS``\ 에 ``-Dfess.config.api.cors.allow.origin=https://portal.example.com``\ 을 지정하는 방법도 있습니다.
변경 후에는 Fess를 재시작하십시오.
브라우저 측에서 넣는 방법은 :doc:`guide-03`\ 을 참조하십시오.

다음에 읽을 글
==============

- 기존 사이트에 검색창이나 검색 화면을 넣고 싶다: :doc:`guide-03`
- 토큰이나 사용자별로 보이는 문서를 설계하고 싶다: :doc:`guide-05`
- 헬스 체크나 모니터링에 API를 사용하고 싶다: :doc:`guide-10`
- 관리 API와 fessctl로 설정을 코드로 관리하고 싶다: :doc:`guide-16`
- SSO나 액세스 토큰의 운영을 포함하여 검색 기반을 보호하고 싶다: :doc:`guide-15`

참고 자료
=========

- `API 개요 <https://fess.codelibs.org/ko/stable/api/api-overview.html>`__
- `검색 API <https://fess.codelibs.org/ko/stable/api/api-search.html>`__
- `레이블 API <https://fess.codelibs.org/ko/stable/api/api-label.html>`__
- `자동완성 API <https://fess.codelibs.org/ko/stable/api/api-suggest.html>`__
- `인기 검색어 API <https://fess.codelibs.org/ko/stable/api/api-popularword.html>`__
- `Documents API <https://fess.codelibs.org/ko/stable/api/admin/api-admin-documents.html>`__
- `Admin API 개요 <https://fess.codelibs.org/ko/stable/api/admin/api-admin-overview.html>`__
- `액세스 토큰 <https://fess.codelibs.org/ko/stable/admin/accesstoken-guide.html>`__
