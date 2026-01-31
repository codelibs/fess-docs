==========================
RAG 채팅 기능 설정
==========================

개요
====

RAG(Retrieval-Augmented Generation) 채팅은 |Fess|의 검색 결과를 LLM(대규모 언어 모델)으로 확장하여
대화 형식으로 정보를 제공하는 기능입니다. 사용자는 자연어로 질문하고 검색 결과를 기반으로 한
상세한 응답을 얻을 수 있습니다.

RAG 채팅의 구조
===================

RAG 채팅은 다음과 같은 다단계 플로우로 동작합니다.

1. **의도 분석 단계**: 사용자의 질문을 분석하고 검색에 최적화된 키워드 추출
2. **검색 단계**: 추출한 키워드로 |Fess| 검색 엔진을 사용하여 문서 검색
3. **평가 단계**: 검색 결과의 관련성을 평가하고 가장 적합한 문서 선택
4. **생성 단계**: 선택한 문서를 기반으로 LLM이 응답 생성
5. **출력 단계**: 응답과 출처 정보를 사용자에게 반환

이 플로우를 통해 단순한 키워드 검색보다 문맥을 이해한 고품질 응답이 가능해집니다.

기본 설정
========

RAG 채팅 기능을 활성화하기 위한 기본 설정입니다.

``app/WEB-INF/conf/system.properties``:

::

    # RAG 채팅 기능 활성화
    rag.chat.enabled=true

    # LLM 프로바이더 선택(ollama, openai, gemini)
    rag.llm.type=ollama

LLM 프로바이더의 상세 설정은 다음을 참조하세요:

- :doc:`llm-ollama` - Ollama 설정
- :doc:`llm-openai` - OpenAI 설정
- :doc:`llm-gemini` - Google Gemini 설정

생성 파라미터
================

LLM의 생성 동작을 제어하는 파라미터입니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.chat.max.tokens``
     - 생성할 최대 토큰 수
     - ``4096``
   * - ``rag.chat.temperature``
     - 생성의 무작위성(0.0~1.0)
     - ``0.7``

temperature 설정
---------------

- **0.0**: 결정적인 응답(동일한 입력에 대해 항상 동일한 응답)
- **0.3~0.5**: 일관성 있는 응답(사실에 기반한 질문에 적합)
- **0.7**: 균형 잡힌 응답(기본값)
- **1.0**: 창의적인 응답(브레인스토밍 등에 적합)

컨텍스트 설정
================

검색 결과에서 LLM에 전달하는 컨텍스트 설정입니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.chat.context.max.documents``
     - 컨텍스트에 포함할 최대 문서 수
     - ``5``
   * - ``rag.chat.context.max.chars``
     - 컨텍스트의 최대 문자 수
     - ``4000``
   * - ``rag.chat.content.fields``
     - 문서에서 가져올 필드
     - ``title,url,content,...``
   * - ``rag.chat.evaluation.max.relevant.docs``
     - 평가 단계에서 선택할 최대 관련 문서 수
     - ``3``

컨텐츠 필드
--------------------

``rag.chat.content.fields``로 지정할 수 있는 필드:

- ``title`` - 문서의 제목
- ``url`` - 문서의 URL
- ``content`` - 문서의 본문
- ``doc_id`` - 문서 ID
- ``content_title`` - 컨텐츠의 제목
- ``content_description`` - 컨텐츠의 설명

시스템 프롬프트
==================

시스템 프롬프트는 LLM의 기본적인 동작을 정의합니다.

기본 설정
--------------

::

    rag.chat.system.prompt=You are an AI assistant for Fess search engine. Answer questions based on the search results provided. Always cite your sources using [1], [2], etc.

커스터마이즈 예
--------------

한국어 응답을 우선하는 경우:

::

    rag.chat.system.prompt=당신은 Fess 검색 엔진의 AI 어시스턴트입니다. 제공된 검색 결과를 기반으로 질문에 답변하세요. 응답은 한국어로 하고, 출처를 [1], [2] 등의 형식으로 반드시 명시하세요.

전문 분야용 커스터마이즈:

::

    rag.chat.system.prompt=You are a technical documentation assistant. Provide detailed and accurate answers based on the search results. Include code examples when relevant. Always cite your sources using [1], [2], etc.

세션 관리
==============

채팅 세션 관리에 관한 설정입니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.chat.session.timeout.minutes``
     - 세션 타임아웃 시간(분)
     - ``30``
   * - ``rag.chat.session.max.size``
     - 동시에 유지할 수 있는 세션의 최대 수
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - 대화 이력에 유지할 최대 메시지 수
     - ``20``

세션 동작
----------------

- 사용자가 새 채팅을 시작하면 새 세션이 생성됩니다
- 세션에는 대화 이력이 저장되어 문맥을 유지한 대화가 가능합니다
- 타임아웃 시간이 경과하면 세션이 자동으로 삭제됩니다
- 대화 이력이 최대 메시지 수를 초과하면 오래된 메시지부터 삭제됩니다

속도 제한
==========

API 과부하를 방지하기 위한 속도 제한 설정입니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.chat.rate.limit.enabled``
     - 속도 제한 활성화
     - ``true``
   * - ``rag.chat.rate.limit.requests.per.minute``
     - 1분당 최대 요청 수
     - ``10``

속도 제한 고려 사항
--------------------

- LLM 프로바이더 측의 속도 제한도 고려하여 설정하세요
- 고부하 환경에서는 더 엄격한 제한을 설정하는 것이 좋습니다
- 속도 제한에 도달하면 사용자에게 오류 메시지가 표시됩니다

API 사용
=========

RAG 채팅 기능은 REST API를 통해 이용할 수 있습니다.

비스트리밍 API
-------------------

엔드포인트: ``POST /api/v1/chat``

파라미터:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 파라미터
     - 필수
     - 설명
   * - ``message``
     - 예
     - 사용자의 메시지
   * - ``sessionId``
     - 아니오
     - 세션 ID(대화를 계속하는 경우)
   * - ``clear``
     - 아니오
     - ``true``로 세션 클리어

요청 예:

::

    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=Fess의 설치 방법을 알려주세요"

응답 예:

::

    {
      "status": "ok",
      "sessionId": "abc123",
      "content": "Fess의 설치 방법은...",
      "sources": [
        {"title": "설치 가이드", "url": "https://..."}
      ]
    }

스트리밍 API
-----------------

엔드포인트: ``POST /api/v1/chat/stream``

Server-Sent Events(SSE) 형식으로 응답을 스트리밍합니다.

파라미터:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 파라미터
     - 필수
     - 설명
   * - ``message``
     - 예
     - 사용자의 메시지
   * - ``sessionId``
     - 아니오
     - 세션 ID(대화를 계속하는 경우)

요청 예:

::

    curl -X POST "http://localhost:8080/api/v1/chat/stream" \
         -d "message=Fess의 특징을 알려주세요" \
         -H "Accept: text/event-stream"

SSE 이벤트:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 이벤트
     - 설명
   * - ``session``
     - 세션 정보(sessionId)
   * - ``phase``
     - 처리 단계의 시작/완료(intent_analysis, search, evaluation, generation)
   * - ``chunk``
     - 생성된 텍스트 조각
   * - ``sources``
     - 참조 문서 정보
   * - ``done``
     - 처리 완료(sessionId, htmlContent)
   * - ``error``
     - 오류 정보

자세한 API 문서는 :doc:`../api/api-chat`를 참조하세요.

웹 인터페이스
===================

|Fess|의 웹 인터페이스에서는 검색 화면에서 RAG 채팅 기능을 이용할 수 있습니다.

채팅 시작
--------------

1. |Fess|의 검색 화면에 접속
2. 채팅 아이콘 클릭
3. 채팅 패널이 표시됨

채팅 사용
--------------

1. 텍스트 상자에 질문 입력
2. 전송 버튼 클릭 또는 Enter 키 누름
3. AI 어시스턴트의 응답이 표시됨
4. 응답에는 참조 문서로의 링크가 포함됨

대화 계속
----------

- 같은 채팅 세션 내에서 대화를 계속할 수 있습니다
- 이전 질문의 문맥을 고려한 응답을 얻을 수 있습니다
- "새 채팅"을 클릭하면 세션이 초기화됩니다

문제 해결
======================

RAG 채팅이 활성화되지 않음
---------------------------

**확인 사항**:

1. ``rag.chat.enabled=true``가 설정되어 있는지
2. LLM 프로바이더가 올바르게 설정되어 있는지
3. LLM 프로바이더에 연결이 가능한지

응답 품질이 낮음
----------------

**개선 방법**:

1. 더 고성능의 LLM 모델 사용
2. ``rag.chat.context.max.documents`` 증가
3. 시스템 프롬프트 커스터마이즈
4. ``rag.chat.temperature`` 조정

응답이 느림
----------------

**개선 방법**:

1. 더 빠른 LLM 모델 사용(예: Gemini Flash)
2. ``rag.chat.max.tokens`` 감소
3. ``rag.chat.context.max.chars`` 감소

세션이 유지되지 않음
------------------------

**확인 사항**:

1. 클라이언트 측에서 sessionId가 올바르게 전송되고 있는지
2. ``rag.chat.session.timeout.minutes`` 설정
3. 세션 스토리지의 용량

디버그 설정
------------

문제를 조사할 때는 로그 레벨을 조정하여 상세 로그를 출력할 수 있습니다.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm" level="DEBUG"/>
    <Logger name="org.codelibs.fess.api.chat" level="DEBUG"/>
    <Logger name="org.codelibs.fess.chat" level="DEBUG"/>

참고 정보
========

- :doc:`llm-overview` - LLM 통합 개요
- :doc:`llm-ollama` - Ollama 설정
- :doc:`llm-openai` - OpenAI 설정
- :doc:`llm-gemini` - Google Gemini 설정
- :doc:`../api/api-chat` - Chat API 레퍼런스
- :doc:`../user/chat-search` - 최종 사용자용 채팅 검색 가이드
