==========================
Chat API
==========================

개요
====

Chat API는 |Fess|의 AI 모드 기능에 프로그램에서 접근하기 위한 RESTful API입니다.
검색 결과를 기반으로 한 AI 지원 응답을 가져올 수 있습니다.

이 API는 두 가지 엔드포인트를 제공합니다:

- **비스트리밍 API**: 완전한 응답을 한 번에 가져오기
- **스트리밍 API**: Server-Sent Events(SSE) 형식으로 실시간으로 응답 가져오기

전제조건
========

Chat API를 사용하려면 다음 설정이 필요합니다:

1. AI 모드 기능이 활성화되어 있을 것(``rag.chat.enabled=true``)
2. LLM 프로바이더가 설정되어 있을 것

자세한 설정 방법은 :doc:`../config/rag-chat`를 참조하세요.

비스트리밍 API
===================

엔드포인트
--------------

::

    POST /api/v1/chat

요청 파라미터
----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``message``
     - String
     - 예
     - 사용자의 메시지(질문)
   * - ``sessionId``
     - String
     - 아니오
     - 세션 ID. 대화를 계속하는 경우 지정
   * - ``clear``
     - String
     - 아니오
     - ``"true"``를 지정하면 세션 클리어

응답
----------

**성공 시(HTTP 200)**

.. code-block:: json

    {
      "status": "ok",
      "sessionId": "abc123def456",
      "content": "Fess는 전문 검색 서버입니다. 주요 특징으로는...",
      "sources": [
        {
          "title": "Fess 개요",
          "url": "https://fess.codelibs.org/ja/overview.html"
        },
        {
          "title": "기능 목록",
          "url": "https://fess.codelibs.org/ja/features.html"
        }
      ]
    }

**오류 시**

.. code-block:: json

    {
      "status": "error",
      "message": "Message is required"
    }

HTTP 상태 코드
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 코드
     - 설명
   * - 200
     - 요청 성공
   * - 400
     - 요청 파라미터가 잘못됨(message가 비어 있음 등)
   * - 404
     - 엔드포인트를 찾을 수 없음
   * - 405
     - 허용되지 않는 HTTP 메서드(POST만 허용)
   * - 500
     - 서버 내부 오류

사용 예
------

cURL
~~~~

.. code-block:: bash

    # 새 채팅 시작
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=Fess란 무엇입니까?"

    # 대화 계속
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=설치 방법을 알려주세요" \
         -d "sessionId=abc123def456"

    # 세션 클리어
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "sessionId=abc123def456" \
         -d "clear=true"

JavaScript
~~~~~~~~~~

.. code-block:: javascript

    async function chat(message, sessionId = null) {
      const params = new URLSearchParams();
      params.append('message', message);
      if (sessionId) {
        params.append('sessionId', sessionId);
      }

      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        body: params
      });

      return await response.json();
    }

    // 사용 예
    const result = await chat('Fess의 기능을 알려주세요');
    console.log(result.content);
    console.log('Session ID:', result.sessionId);

Python
~~~~~~

.. code-block:: python

    import requests

    def chat(message, session_id=None):
        data = {'message': message}
        if session_id:
            data['sessionId'] = session_id

        response = requests.post(
            'http://localhost:8080/api/v1/chat',
            data=data
        )
        return response.json()

    # 사용 예
    result = chat('Fess의 설치 방법은?')
    print(result['content'])
    print(f"Session ID: {result['sessionId']}")

스트리밍 API
=================

엔드포인트
--------------

::

    POST /api/v1/chat/stream
    GET /api/v1/chat/stream

요청 파라미터
----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``message``
     - String
     - 예
     - 사용자의 메시지(질문)
   * - ``sessionId``
     - String
     - 아니오
     - 세션 ID. 대화를 계속하는 경우 지정

응답 형식
--------------

스트리밍 API는 ``text/event-stream`` 형식(Server-Sent Events)으로 응답을 반환합니다.

각 이벤트는 다음 형식입니다:

::

    event: <이벤트명>
    data: <JSON 데이터>

SSE 이벤트
-----------

**session**

세션 정보를 알립니다. 스트림 시작 시 전송됩니다.

.. code-block:: json

    {
      "sessionId": "abc123def456"
    }

**phase**

처리 단계의 시작/완료를 알립니다.

.. code-block:: json

    {
      "phase": "intent_analysis",
      "status": "start",
      "message": "Analyzing user intent..."
    }

.. code-block:: json

    {
      "phase": "search",
      "status": "start",
      "message": "Searching documents...",
      "keywords": "Fess 설치"
    }

.. code-block:: json

    {
      "phase": "search",
      "status": "complete"
    }

단계 종류:

- ``intent_analysis`` - 의도 분석
- ``search`` - 검색 실행
- ``evaluation`` - 결과 평가
- ``generation`` - 응답 생성

**chunk**

생성된 텍스트 조각을 알립니다.

.. code-block:: json

    {
      "content": "Fess는"
    }

**sources**

참조 문서 정보를 알립니다.

.. code-block:: json

    {
      "sources": [
        {
          "title": "설치 가이드",
          "url": "https://fess.codelibs.org/ja/install.html"
        }
      ]
    }

**done**

처리 완료를 알립니다.

.. code-block:: json

    {
      "sessionId": "abc123def456",
      "htmlContent": "<p>Fess는 전문 검색 서버입니다...</p>"
    }

**error**

오류를 알립니다.

.. code-block:: json

    {
      "phase": "generation",
      "message": "LLM request failed"
    }

사용 예
------

cURL
~~~~

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v1/chat/stream" \
         -d "message=Fess의 특징을 알려주세요" \
         -H "Accept: text/event-stream" \
         --no-buffer

JavaScript(EventSource)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

    function streamChat(message, sessionId = null) {
      const params = new URLSearchParams();
      params.append('message', message);
      if (sessionId) {
        params.append('sessionId', sessionId);
      }

      // POST 요청에는 fetch 사용
      return fetch('/api/v1/chat/stream', {
        method: 'POST',
        body: params
      }).then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        function read() {
          return reader.read().then(({ done, value }) => {
            if (done) return;

            const text = decoder.decode(value);
            const lines = text.split('\n');

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const data = JSON.parse(line.slice(6));
                handleEvent(data);
              }
            }

            return read();
          });
        }

        return read();
      });
    }

    function handleEvent(data) {
      if (data.content) {
        // 청크 표시
        document.getElementById('output').textContent += data.content;
      } else if (data.phase) {
        // 단계 정보 표시
        console.log(`Phase: ${data.phase} - ${data.status}`);
      } else if (data.sources) {
        // 소스 정보 표시
        console.log('Sources:', data.sources);
      }
    }

Python
~~~~~~

.. code-block:: python

    import requests

    def stream_chat(message, session_id=None):
        data = {'message': message}
        if session_id:
            data['sessionId'] = session_id

        response = requests.post(
            'http://localhost:8080/api/v1/chat/stream',
            data=data,
            stream=True,
            headers={'Accept': 'text/event-stream'}
        )

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    import json
                    data = json.loads(line[6:])
                    yield data

    # 사용 예
    for event in stream_chat('Fess의 기능에 대해 알려주세요'):
        if 'content' in event:
            print(event['content'], end='', flush=True)
        elif 'phase' in event:
            print(f"\n[Phase: {event['phase']} - {event['status']}]")

오류 처리
==================

API 사용 시 적절한 오류 처리를 구현하세요.

.. code-block:: javascript

    async function chatWithErrorHandling(message, sessionId = null) {
      try {
        const params = new URLSearchParams();
        params.append('message', message);
        if (sessionId) {
          params.append('sessionId', sessionId);
        }

        const response = await fetch('/api/v1/chat', {
          method: 'POST',
          body: params
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || 'API request failed');
        }

        const result = await response.json();

        if (result.status === 'error') {
          throw new Error(result.message);
        }

        return result;

      } catch (error) {
        console.error('Chat API error:', error);
        throw error;
      }
    }

속도 제한
==========

Chat API에는 속도 제한이 적용됩니다.

기본 설정:

- 1분당 10개 요청

속도 제한을 초과하면 HTTP 429 오류가 반환됩니다.

속도 제한 설정은 :doc:`../config/rag-chat`를 참조하세요.

보안
============

Chat API 사용 시 보안 관련 주의사항:

1. **인증**: 현재 버전에서는 API에 인증이 필요하지 않지만, 프로덕션 환경에서는 적절한 접근 제어를 검토하세요
2. **속도 제한**: DoS 공격을 방지하기 위해 속도 제한을 활성화하세요
3. **입력 검증**: 클라이언트 측에서도 입력 검증을 수행하세요
4. **CORS**: 필요에 따라 CORS 설정을 확인하세요

참고 정보
========

- :doc:`../config/rag-chat` - AI 모드 기능 설정
- :doc:`../config/llm-overview` - LLM 통합 개요
- :doc:`../user/chat-search` - 최종 사용자용 채팅 검색 가이드
- :doc:`api-overview` - API 개요
