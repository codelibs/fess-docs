==========================
Chat API
==========================

개요
====

Chat API 는 |Fess| 의 AI 검색 모드 (RAG 채팅) 기능에 프로그램에서 접근하기 위한 v2 API 입니다.
검색 결과를 기반으로 한 LLM 에 의한 답변 (보완) 을 취득할 수 있습니다.

이 API 는 다음 3개의 엔드포인트를 제공합니다.

.. tabularcolumns:: |p{6cm}|p{9cm}|
.. list-table::
   :header-rows: 1

   * - 엔드포인트
     - 설명
   * - ``POST /chat``
     - 일괄 (비스트리밍) RAG 채팅 보완.
   * - ``POST /chat/stream``
     - 스트리밍 RAG 채팅 보완 (Server-Sent Events).
   * - ``DELETE /chat/sessions/{session_id}``
     - 채팅 세션의 대화 기록 삭제.

베이스 URL 및 공통 응답 엔벨로프·오류 코드에 대해서는 :doc:`api-overview` 를 참조하십시오.

::

    http://<Server Name>/api/v2/

로컬 환경 예:

::

    http://localhost:8080/api/v2

전제 조건
=========

Chat API 를 사용하려면 다음 설정이 필요합니다.

1. AI 검색 모드 (RAG 채팅) 기능이 활성화되어 있을 것 ( ``rag.chat.enabled=true`` )
2. LLM 프로바이더가 설정되어 있을 것

기능이 비활성화 ( ``rag.chat.enabled=false`` ) 된 경우 요청은 ``invalid_request`` 오류가 됩니다.

자세한 설정 방법은 :doc:`../config/rag-chat` 및 :doc:`../config/llm-overview` 를 참조하십시오.

인증과 CSRF
===========

Chat API 의 모든 엔드포인트는 상태를 변경하는 요청 ( ``POST`` / ``DELETE`` ) 이므로 ``X-Fess-CSRF-Token`` 헤더가 필요합니다.
CSRF 토큰 취득 방법 및 인증·세션의 자세한 내용은 :doc:`api-overview` 를 참조하십시오.

속도 제한
=========

``POST /chat`` , ``POST /chat/stream`` 및 ``DELETE /chat/sessions/{session_id}`` 에는 사용자별 속도 제한이 적용됩니다.

- 기본값: 1분당 30 요청 (사용자별)
- 설정 키: ``api.v2.chat.rate.limit.per.user.per.minute``
- 값을 ``0`` 이하로 설정하면 속도 제한이 비활성화됩니다.

속도 제한을 초과한 경우 ``rate_limited`` 오류 (HTTP 429) 가 반환됩니다. ``Retry-After`` 헤더에는 고정값 ``60`` (초) 가 설정됩니다.
이 속도 제한은 ``POST /chat`` , ``POST /chat/stream`` , ``DELETE /chat/sessions/{session_id}`` 에서 공유됩니다.

.. note::

   속도 제한은 사용자를 식별할 수 있는 경우에만 적용됩니다. 세션이 확립되지 않아 사용자 ID를 확인할 수 없는 익명 호출에서는 속도 제한이 건너뜁니다.

POST /chat
==========

동기적인 채팅 보완을 수행합니다.
세션은 ``session_id`` 로 식별합니다. ``session_id`` 를 생략한 경우 서버가 세션을 생성하고 응답의 ``session_id`` 로 반환합니다.

``fields.label`` 이나 ``extra_queries`` 에 전달된 잘못된 값은 해결된 요청에서 자동으로 제거되며, 응답 엔벨로프에는 표면화되지 않습니다.

엔드포인트
----------

::

    POST /api/v2/chat

요청 본문
---------

``Content-Type: application/json`` 의 JSON 본문입니다.

요청 본문의 크기 제한은 32 KiB 입니다. 이를 초과하면 ``payload_too_large`` 오류 (HTTP 413) 가 됩니다.

.. tabularcolumns:: |p{3.5cm}|p{2.5cm}|p{1.5cm}|p{7cm}|
.. list-table:: ChatRequest
   :header-rows: 1

   * - 필드
     - 타입
     - 필수
     - 설명
   * - ``message``
     - string
     - 예
     - 사용자의 메시지 (질문). 최대 문자 수는 ``rag.chat.message.max.length`` (기본값 4000) 로 제한됩니다. 초과한 경우 ``invalid_request`` 오류 (HTTP 400) 가 됩니다.
   * - ``session_id``
     - string
     - 아니오
     - 세션 ID. 생략 시 서버가 생성하여 응답으로 반환합니다.
   * - ``fields``
     - object
     - 아니오
     - 취득 단계용 임의 필터 필드.
   * - ``fields.label``
     - string / string 배열
     - 아니오
     - 허용 목록화된 레이블로 취득을 제한합니다.
   * - ``extra_queries``
     - string / string 배열
     - 아니오
     - 허용 목록화된 패싯 쿼리 식.

요청 예:

.. code-block:: json

    {
      "message": "Fessとは何ですか？",
      "session_id": "abc123def456",
      "fields": {
        "label": "news"
      },
      "extra_queries": "label:faq"
    }

응답
----

**성공 시 (HTTP 200, ChatResponse)**

응답은 공통 엔벨로프 ``response`` 에 저장됩니다. ``session_id`` 는 항상 존재합니다.

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: response 요소
   :header-rows: 1

   * - 필드
     - 타입
     - 설명
   * - ``session_id``
     - string
     - 세션 ID.
   * - ``content``
     - string (nullable)
     - 생성된 메시지 텍스트. 항상 존재하지만, 모델이 내용을 생성하지 않은 경우 ``null`` 이 될 수 있습니다.
   * - ``sources``
     - array
     - 참조 문서 배열. 각 요소는 ChatSource.

**ChatSource**

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: ChatSource 요소
   :header-rows: 1

   * - 필드
     - 타입
     - 설명
   * - ``rank``
     - integer
     - 취득 세트 내의 1 시작 위치.
   * - ``title``
     - string (nullable)
     - 문서 제목.
   * - ``url``
     - string (nullable)
     - 문서 URL.
   * - ``doc_id``
     - string (nullable)
     - 문서 ID.
   * - ``snippet``
     - string (nullable)
     - 스니펫.
   * - ``url_link``
     - string (nullable)
     - 표시용 URL 링크.
   * - ``go_url``
     - string (nullable)
     - 리다이렉트용 URL.

응답 예:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123def456",
        "content": "Fessは全文検索サーバーです。主な特徴として...",
        "sources": [
          {
            "rank": 1,
            "title": "Fessの概要",
            "url": "https://fess.codelibs.org/ja/overview.html",
            "doc_id": "abcdef0123456789",
            "snippet": "Fessは...",
            "url_link": "https://fess.codelibs.org/ja/overview.html",
            "go_url": "/go/?docId=abcdef0123456789"
          }
        ]
      }
    }

HTTP 상태 코드
--------------

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - 코드
     - 설명
   * - 200
     - 요청 성공.
   * - 400
     - 요청이 잘못됨 ( ``message`` 누락, ``message`` 최대 길이 초과, ``rag.chat.enabled=false`` 등).
   * - 403
     - CSRF 토큰 누락·만료 등.
   * - 405
     - HTTP 메서드가 허용되지 않습니다.
   * - 413
     - 요청 본문이 크기 제한 (32 KiB) 을 초과했습니다.
   * - 415
     - ``Content-Type`` 이 ``application/json`` 이 아니거나, 누락되어 있거나, ``charset`` 이 UTF-8 이 아닙니다.
   * - 429
     - 속도 제한을 초과했습니다.
   * - 500
     - 서버 내부 오류.

cURL 예
-------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -d '{"message":"Fessとは何ですか？","session_id":"abc123def456"}'

POST /chat/stream
=================

스트리밍 형식으로 채팅 보완을 수행합니다.
요청 본문은 ``POST /chat`` 와 동일 (ChatRequest) 합니다.

성공 응답은 ``text/event-stream`` 형식 (Server-Sent Events) 의 이름 있는 이벤트입니다.
각 이벤트는 ``event: <이름>`` 과 ``data: <JSON>`` 으로 구성됩니다.

스트림 전 유효성 검사 실패는 여전히 JSON 엔벨로프를 반환합니다 ( ``POST /chat`` 와 동일한 오류 코드).
``fields.label`` 이나 ``extra_queries`` 에 전달된 잘못된 값은 자동으로 제거되며, 응답 엔벨로프나 SSE 이벤트에도 표면화되지 않습니다.

엔드포인트
----------

::

    POST /api/v2/chat/stream

SSE 이벤트
----------

.. tabularcolumns:: |p{2.5cm}|p{12.5cm}|
.. list-table::
   :header-rows: 1

   * - 이벤트
     - 설명 (페이로드)
   * - ``phase``
     - 파이프라인 페이즈 전환 ( ``{ phase, status, message?, keywords?, hit_count?, ... }`` ). ``message`` 와 ``keywords`` 는 onPhaseStart 에서 출력됩니다. 추가 임의 필드 (예: ``hit_count`` ) 는 onPhaseComplete 의 페이로드에서 흘러옵니다.
   * - ``chunk``
     - 생성 텍스트 단편 ( ``{ content }`` ).
   * - ``sources``
     - 취득된 소스 ( ``{ sources: [ChatSource] }`` ).
   * - ``retry``
     - 일시적 실패의 백오프 ( ``{ phase, operation, attempt, max_attempts, sleep_ms, cause? }`` ).
   * - ``waiting``
     - 장시간 페이즈의 진행 상황 ( ``{ phase, reason, elapsed_ms, timeout_ms }`` ).
   * - ``fallback``
     - 쿼리 재작성·전략 폴백 ( ``{ phase, reason, original_query?, new_query? }`` ).
   * - ``warning``
     - 복구 가능한 경고 ( ``{ phase, code, detail? }`` ).
   * - ``done``
     - 스트림 종료 ( ``{ session_id, html_content? }`` ).
   * - ``error``
     - 종단 스트림 중도 실패 ( ``{ phase?, message, error_code }`` ). ``message`` 필드는 ``error_code`` 와 동일한 문자열을 가집니다. 클라이언트는 ``error_code`` 를 기반으로 현지화해야 합니다.

SSE 스트림 예:

::

    event: phase
    data: {"phase":"search","status":"start","message":"Searching documents...","keywords":"Fess インストール"}

    event: chunk
    data: {"content":"Fessは"}

    event: sources
    data: {"sources":[{"rank":1,"title":"インストールガイド","url":"https://fess.codelibs.org/ja/install.html"}]}

    event: done
    data: {"session_id":"abc123def456"}

HTTP 상태 코드
--------------

스트림 전 유효성 검사에서 실패한 경우 다음 오류 코드가 JSON 엔벨로프로 반환됩니다.

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - 코드
     - 설명
   * - 200
     - SSE 스트림 시작 (성공).
   * - 400
     - 요청이 잘못됨 ( ``message`` 누락, ``rag.chat.enabled=false`` 등).
   * - 403
     - CSRF 토큰 누락·만료 등.
   * - 405
     - HTTP 메서드가 허용되지 않습니다.
   * - 413
     - 요청 본문이 크기 제한 (32 KiB) 을 초과했습니다.
   * - 415
     - ``Content-Type`` 이 ``application/json`` 이 아니거나, 누락되어 있거나, ``charset`` 이 UTF-8 이 아닙니다.
   * - 429
     - 속도 제한을 초과했습니다.
   * - 500
     - 서버 내부 오류.

cURL 예
-------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat/stream" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -H "Accept: text/event-stream" \
         --no-buffer \
         -d '{"message":"Fessの特徴を教えてください"}'

DELETE /chat/sessions/{session_id}
==================================

지정한 채팅 세션의 대화 기록을 삭제합니다.
세션은 경로의 ``session_id`` 로 식별합니다.

성공 시에는 ``cleared: true`` 가 반환됩니다. 일치하는 활성 세션이 없는 경우 ``not_found`` 오류 (HTTP 404) 가 됩니다.

엔드포인트
----------

::

    DELETE /api/v2/chat/sessions/{session_id}

경로 파라미터
-------------

.. tabularcolumns:: |p{3cm}|p{2cm}|p{10cm}|
.. list-table::
   :header-rows: 1

   * - 파라미터
     - 타입
     - 설명
   * - ``session_id``
     - string
     - 삭제 대상 세션 ID. minLength 1, maxLength 100, 패턴 ``^[A-Za-z0-9._-]+$`` .

응답
----

**성공 시 (HTTP 200, ChatClearResponse)**

응답은 공통 엔벨로프 ``response`` 에 저장됩니다. ``session_id`` 와 ``cleared`` 는 항상 존재합니다.

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: response 요소
   :header-rows: 1

   * - 필드
     - 타입
     - 설명
   * - ``session_id``
     - string
     - 세션 ID.
   * - ``cleared``
     - boolean
     - 항상 ``true`` (세션이 발견되어 삭제된 경우).

응답 예:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123def456",
        "cleared": true
      }
    }

HTTP 상태 코드
--------------

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - 코드
     - 설명
   * - 200
     - 세션을 삭제했습니다.
   * - 400
     - 요청이 잘못되었습니다 ( ``session_id`` 가 패턴 ``^[A-Za-z0-9._-]+$`` 또는 길이 제한 (1〜100문자) 에 일치하지 않거나, ``rag.chat.enabled=false`` 등).
   * - 403
     - CSRF 토큰 누락·만료 등.
   * - 404
     - 일치하는 활성 세션을 찾을 수 없습니다.
   * - 405
     - HTTP 메서드가 허용되지 않습니다.
   * - 429
     - 속도 제한을 초과했습니다.
   * - 500
     - 서버 내부 오류.

cURL 예
-------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/v2/chat/sessions/abc123def456" \
         -H "X-Fess-CSRF-Token: <token>"

보안
====

Chat API 를 사용할 때의 보안 상 주의사항:

1. **인증**: v2 API 는 세션 기반 인증을 채택하고 있습니다. 자세한 내용은 :doc:`api-overview` 를 참조하십시오.
2. **CSRF**: 상태 변경 요청에는 ``X-Fess-CSRF-Token`` 헤더가 필요합니다.
3. **속도 제한**: DoS 공격을 방지하기 위해 사용자별 속도 제한 (기본 30/분) 이 적용됩니다. 설정 키는 ``api.v2.chat.rate.limit.per.user.per.minute`` 입니다.

참고 정보
=========

- :doc:`../config/rag-chat` - AI 검색 모드 기능 설정
- :doc:`../config/llm-overview` - LLM 통합 개요
- :doc:`../user/chat-search` - 최종 사용자용 채팅 검색 가이드
- :doc:`api-overview` - API 개요
