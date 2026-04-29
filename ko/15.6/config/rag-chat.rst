==========================
AI 검색 모드 기능 설정
==========================

개요
====

AI 검색 모드(RAG: Retrieval-Augmented Generation)는 |Fess|의 검색 결과를 LLM(대규모 언어 모델)으로 확장하여
대화 형식으로 정보를 제공하는 기능입니다. 사용자는 자연어로 질문하고 검색 결과를 기반으로 한
상세한 응답을 얻을 수 있습니다.

|Fess| 15.6에서는 LLM 기능이 ``fess-llm-*`` 플러그인으로 분리되었습니다.
코어 설정 및 LLM 프로바이더 고유의 설정은 ``fess_config.properties`` 에서 수행하고,
LLM 프로바이더 선택(``rag.llm.name``)은 ``system.properties`` 또는 관리 화면에서 수행합니다.

AI 검색 모드의 구조
==============

AI 검색 모드는 다음과 같은 다단계 플로우로 동작합니다.

1. **의도 분석 단계**: 사용자의 질문을 분석하고 검색에 최적화된 키워드 추출
2. **검색 단계**: 추출한 키워드로 |Fess| 검색 엔진을 사용하여 문서 검색
3. **쿼리 재생성 폴백**: 검색 결과가 없는 경우 LLM이 쿼리를 재생성하여 재검색
4. **평가 단계**: 검색 결과의 관련성을 평가하고 가장 적합한 문서 선택
5. **생성 단계**: 선택한 문서를 기반으로 LLM이 응답 생성
6. **출력 단계**: 응답과 출처 정보를 사용자에게 반환(Markdown 렌더링 지원)

이 플로우를 통해 단순한 키워드 검색보다 문맥을 이해한 고품질 응답이 가능해집니다.
쿼리 재생성을 통해 초기 검색 쿼리가 최적이 아닌 경우에도 응답 범위가 향상됩니다.

기본 설정
========

AI 검색 모드 기능의 설정은 코어 설정과 프로바이더 설정의 두 가지로 나뉩니다.

코어 설정 (fess_config.properties)
----------------------------------

AI 검색 모드 기능을 활성화하기 위한 기본 설정입니다.
``app/WEB-INF/conf/fess_config.properties`` 에 설정합니다.

::

    # AI 검색 모드 기능 활성화
    rag.chat.enabled=true

프로바이더 설정 (system.properties / 관리 화면)
-------------------------------------------------

LLM 프로바이더 선택은 관리 화면 또는 시스템 프로퍼티에서 수행합니다.

**관리 화면에서 설정하는 경우**:

관리 화면 > 시스템 > 전반 설정 화면에서 사용할 LLM 프로바이더를 선택합니다.

**system.properties 에서 설정하는 경우**:

::

    # LLM 프로바이더 선택(ollama, openai, gemini)
    rag.llm.name=ollama

LLM 프로바이더의 상세 설정은 다음을 참조하세요:

- :doc:`llm-ollama` - Ollama 설정
- :doc:`llm-openai` - OpenAI 설정
- :doc:`llm-gemini` - Google Gemini 설정

설정 경로 빠른 참조
================

|Fess| 15.6에서는 설정이 두 가지 계열로 분리되어 있습니다: FessConfig 계열
( ``fess_config.properties`` )과 SystemProperty 계열( ``system.properties``,
OpenSearch에 영속화). 두 계열의 설정 경로가 다르므로 혼동하지 마십시오.

.. list-table::
   :header-rows: 1
   :widths: 35 18 32 15

   * - 프로퍼티
     - 계열
     - Docker / JVM 옵션 전달 방법
     - 관리 화면
   * - ``rag.chat.enabled``
     - FessConfig
     - ``-Dfess.config.rag.chat.enabled=true``
     - 없음
   * - ``rag.llm.name``
     - SystemProperty
     - ``-Dfess.system.rag.llm.name=gemini`` (초기 기본값으로만 작용)
     - 있음 (전체 설정)
   * - ``rag.llm.gemini.api.key``
     - FessConfig
     - ``-Dfess.config.rag.llm.gemini.api.key=...``
     - 있음
   * - ``rag.llm.gemini.model``
     - FessConfig
     - ``-Dfess.config.rag.llm.gemini.model=...``
     - 있음
   * - ``rag.llm.openai.api.key``
     - FessConfig
     - ``-Dfess.config.rag.llm.openai.api.key=...``
     - 있음
   * - ``rag.llm.openai.model``
     - FessConfig
     - ``-Dfess.config.rag.llm.openai.model=...``
     - 있음
   * - ``rag.llm.ollama.api.url``
     - FessConfig
     - ``-Dfess.config.rag.llm.ollama.api.url=...``
     - 있음

.. important::

   ``RAG_CHAT_ENABLED=true`` 또는 ``RAG_LLM_GEMINI_API_KEY=...`` 와 같은 단순 환경 변수는
   |Fess| 에서 자동으로 매핑되지 **않습니다**. 모든 RAG / LLM 설정은 반드시
   ``FESS_JAVA_OPTS`` 내에서 ``-Dfess.config.*`` 또는 ``-Dfess.system.*`` JVM 옵션으로
   전달해야 합니다.

.. note::

   ``rag.llm.type`` 은 |Fess| 15.5 이전의 옛 프로퍼티 이름입니다.
   15.6 이후에는 ``rag.llm.name`` 으로 변경되었으며, ``rag.llm.type`` 에 작성된 값은
   읽혀지지 않습니다.

코어 설정 목록
============

``fess_config.properties`` 에서 설정 가능한 코어 설정 목록입니다.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.chat.enabled``
     - AI 검색 모드 기능 활성화
     - ``false``
   * - ``rag.chat.context.max.documents``
     - 컨텍스트에 포함할 최대 문서 수
     - ``5``
   * - ``rag.chat.session.timeout.minutes``
     - 세션 타임아웃 시간(분)
     - ``30``
   * - ``rag.chat.session.max.size``
     - 동시에 유지할 수 있는 세션의 최대 수
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - 대화 이력에 유지할 최대 메시지 수
     - ``30``
   * - ``rag.chat.content.fields``
     - 문서에서 가져올 필드
     - ``title,url,content,doc_id,content_title,content_description``
   * - ``rag.chat.message.max.length``
     - 사용자 메시지의 최대 문자 수
     - ``4000``
   * - ``rag.chat.highlight.fragment.size``
     - 하이라이트 표시의 프래그먼트 크기
     - ``500``
   * - ``rag.chat.highlight.number.of.fragments``
     - 하이라이트 표시의 프래그먼트 수
     - ``3``
   * - ``rag.chat.history.assistant.content``
     - 어시스턴트 이력에 포함할 콘텐츠 종류( ``full`` / ``smart_summary`` / ``source_titles`` / ``source_titles_and_urls`` / ``truncated`` / ``none`` )
     - ``smart_summary``

생성 파라미터
================

|Fess| 15.6에서는 생성 파라미터(최대 토큰 수, temperature 등)를 프로바이더별,
프롬프트 타입별로 설정합니다. 이 설정들은 코어 설정이 아닌 각 ``fess-llm-*``
플러그인의 설정으로 관리됩니다.

상세 내용은 각 프로바이더 문서를 참조하세요:

- :doc:`llm-ollama` - Ollama 생성 파라미터 설정
- :doc:`llm-openai` - OpenAI 생성 파라미터 설정
- :doc:`llm-gemini` - Google Gemini 생성 파라미터 설정

컨텍스트 설정
================

검색 결과에서 LLM에 전달하는 컨텍스트 설정입니다.

코어 설정
--------

다음 설정은 ``fess_config.properties`` 에서 수행합니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.chat.context.max.documents``
     - 컨텍스트에 포함할 최대 문서 수
     - ``5``
   * - ``rag.chat.content.fields``
     - 문서에서 가져올 필드
     - ``title,url,content,doc_id,content_title,content_description``

프로바이더 고유 설정
-----------------------

다음 설정은 프로바이더별로 ``fess_config.properties`` 에서 수행합니다.

- ``rag.llm.{provider}.{promptType}.context.max.chars`` - 컨텍스트의 최대 문자 수
- ``rag.llm.{provider}.chat.evaluation.max.relevant.docs`` - 평가 단계에서 선택할 최대 관련 문서 수

``{provider}`` 에는 ``ollama``, ``openai``, ``gemini`` 등의 프로바이더명이 들어갑니다.
``{promptType}`` 에는 ``chat``, ``intent_analysis``, ``evaluation`` 등의 프롬프트 타입이 들어갑니다.

상세 내용은 각 프로바이더 문서를 참조하세요.

콘텐츠 필드
--------------------

``rag.chat.content.fields`` 로 지정할 수 있는 필드:

- ``title`` - 문서의 제목
- ``url`` - 문서의 URL
- ``content`` - 문서의 본문
- ``doc_id`` - 문서 ID
- ``content_title`` - 콘텐츠의 제목
- ``content_description`` - 콘텐츠의 설명

시스템 프롬프트
==================

|Fess| 15.6에서는 시스템 프롬프트가 프로퍼티 파일이 아닌 각 ``fess-llm-*``
플러그인의 DI XML(``fess_llm++.xml``)에서 정의됩니다.

프롬프트 커스터마이즈
-------------------------

시스템 프롬프트를 커스터마이즈하려면 플러그인 JAR 내의 ``fess_llm++.xml`` 을
오버라이드합니다.

1. 사용 중인 플러그인의 JAR 파일에서 ``fess_llm++.xml`` 을 취득
2. 필요한 변경을 가함
3. ``app/WEB-INF/`` 아래의 적절한 위치에 배치하여 오버라이드

각 프롬프트 타입(의도 분석, 평가, 생성)별로 서로 다른 시스템 프롬프트가
정의되어 있어 용도에 따른 최적화가 이루어집니다.

상세 내용은 각 프로바이더 문서를 참조하세요:

- :doc:`llm-ollama` - Ollama 프롬프트 설정
- :doc:`llm-openai` - OpenAI 프롬프트 설정
- :doc:`llm-gemini` - Google Gemini 프롬프트 설정

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
     - ``30``

세션 동작
----------------

- 사용자가 새 채팅을 시작하면 새 세션이 생성됩니다
- 세션에는 대화 이력이 저장되어 문맥을 유지한 대화가 가능합니다
- 타임아웃 시간이 경과하면 세션이 자동으로 삭제됩니다
- 대화 이력이 최대 메시지 수를 초과하면 오래된 메시지부터 삭제됩니다

동시 실행 제어
==============

LLM으로의 요청 동시 실행 수는 프로바이더별로 ``fess_config.properties`` 에서 제어합니다.

::

    # 프로바이더별 최대 동시 요청 수
    rag.llm.ollama.max.concurrent.requests=5
    rag.llm.openai.max.concurrent.requests=10
    rag.llm.gemini.max.concurrent.requests=10

동시 실행 제어 고려 사항
-----------------------

- LLM 프로바이더 측의 레이트 제한도 고려하여 설정하세요
- 고부하 환경에서는 더 작은 값을 설정하는 것을 권장합니다
- 동시 실행 수의 상한에 도달한 경우 요청은 큐에 들어가 순차적으로 처리됩니다

대화 이력 모드
==============

``rag.chat.history.assistant.content`` 로 어시스턴트 응답의 대화 이력 저장 방식을 설정할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 모드
     - 설명
   * - ``smart_summary``
     - (기본값) 응답의 앞부분(60%)과 뒷부분(40%)을 보존하고 중간 부분을 생략 마커로 치환. 소스 타이틀도 추가
   * - ``full``
     - 응답 전체를 그대로 보존
   * - ``source_titles``
     - 소스 타이틀만 보존
   * - ``source_titles_and_urls``
     - 소스 타이틀과 URL을 보존
   * - ``truncated``
     - 응답을 최대 문자 수로 잘라서 보존
   * - ``none``
     - 이력을 보존하지 않음

.. note::

   ``smart_summary`` 모드에서는 긴 응답의 문맥을 효율적으로 보존하면서 토큰 사용량을 줄입니다.
   사용자와 어시스턴트의 메시지 쌍이 턴 단위로 그룹화되어 문자 수 바짓 내에서 최적으로 패킹됩니다.
   이력의 최대 문자 수와 요약의 최대 문자 수는 각 ``fess-llm-*`` 플러그인의 ``LlmClient`` 구현에서 제어됩니다.

쿼리 재생성
============

검색 결과가 없거나 관련 결과가 없는 경우, LLM이 자동으로 쿼리를 재생성하여 재검색합니다.

- 검색 결과 0건인 경우: 이유 ``no_results`` 로 쿼리 재생성 실행
- 관련 문서를 찾지 못한 경우: 이유 ``no_relevant_results`` 로 쿼리 재생성 실행
- 재생성에 실패한 경우 원래 쿼리로 폴백

이 기능은 기본적으로 활성화되어 있으며, 동기 및 스트리밍 RAG 플로우 모두에 통합되어 있습니다.
쿼리 재생성 프롬프트는 각 ``fess-llm-*`` 플러그인에서 정의됩니다.

Markdown 렌더링
================

AI 검색 모드의 응답은 Markdown 형식으로 렌더링됩니다.

- LLM의 응답이 Markdown으로 파싱되어 HTML로 변환됩니다
- 변환된 HTML은 안전한 태그와 속성만 허용하도록 새니타이징됩니다
- 제목, 리스트, 코드 블록, 테이블, 링크 등의 Markdown 구문을 지원
- 클라이언트 측에서는 ``marked.js`` 와 ``DOMPurify`` 를 사용하고, 서버 측에서는 OWASP 새니타이저를 사용

API 사용
=========

AI 검색 모드 기능은 REST API를 통해 이용할 수 있습니다.

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
   * - ``phase``
     - 처리 단계의 시작/완료(intent_analysis, search, evaluation, generation)
   * - ``chunk``
     - 생성된 텍스트 조각
   * - ``sources``
     - 참조 문서 정보
   * - ``done``
     - 처리 완료(sessionId, htmlContent). htmlContent에는 Markdown 렌더링된 HTML 문자열이 포함됨
   * - ``error``
     - 오류 정보. 타임아웃, 컨텍스트 길이 초과, 모델 미발견, 잘못된 응답, 연결 오류 등 유형별 메시지 제공

자세한 API 문서는 :doc:`../api/api-chat`를 참조하세요.

웹 인터페이스
===================

|Fess|의 웹 인터페이스에서는 검색 화면에서 AI 검색 모드 기능을 이용할 수 있습니다.

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

검색 화면에 AI 모드 버튼이 표시되지 않음
--------------------------------------

**증상**: 검색 결과 화면 헤더에 AI 모드 버튼이 표시되지 않고, ``/chat`` 에 접근하면
최상위 페이지로 리다이렉트됩니다.

**체크리스트**: 다음 항목을 위에서부터 순서대로 확인하세요.

1. ``rag.chat.enabled=true`` 가 설정되어 있는가

   - Docker: ``FESS_JAVA_OPTS`` 에 ``-Dfess.config.rag.chat.enabled=true`` 가 포함되어 있는가
   - 패키지 설치: ``app/WEB-INF/conf/fess_config.properties`` 에 기재되어 있는가

2. 해당 ``fess-llm-*`` 플러그인이 설치되어 있는가

   - Docker: ``FESS_PLUGINS=fess-llm-gemini:15.6.0`` (또는 ``fess-llm-openai`` / ``fess-llm-ollama`` )가 지정되어 있는가
   - 패키지 설치: JAR 파일이 ``app/WEB-INF/plugin/`` 에 배치되어 있는가
   - 시작 로그에 ``Installing fess-llm-XXX-15.6.0.jar`` 이 출력되고 있는가

3. ``rag.llm.name`` 의 값이 설치된 플러그인과 일치하는가

   - 기본값은 ``ollama`` 입니다. Gemini 플러그인만 설치한 경우에는 명시적으로 ``gemini`` (또는 ``openai`` )로 변경해야 합니다
   - 설정 방법 (a): 관리 화면 > 시스템 > 전체의 RAG 섹션에서 ``rag.llm.name`` 을 편집하고 저장
   - 설정 방법 (b): 시작 시 ``FESS_JAVA_OPTS`` 에 ``-Dfess.system.rag.llm.name=gemini`` 를 포함 (OpenSearch에 값이 아직 저장되지 않은 첫 시작 시에만 기본값으로 적용됨)

4. 시작 로그에 ``[LLM] LlmClient not found. componentName=ollamaLlmClient`` 와 같은 WARN이 계속 출력되는가

   - ``rag.llm.name`` 이 그대로 ``ollama`` 인 채 Ollama 플러그인이 설치되지 않은 경우의 전형적 증상입니다
   - ``rag.llm.name`` 을 실제로 사용하는 프로바이더 이름으로 변경하면 해결됩니다
   - 마찬가지로 ``componentName=geminiLlmClient`` 의 WARN이 출력되는 경우는 ``rag.llm.name=gemini`` 로 설정했는데 ``fess-llm-gemini`` 플러그인이 도입되지 않았음을 의미합니다

5. 프로바이더 고유 API 키가 올바르게 설정되어 있는가

   - ``rag.llm.gemini.api.key`` / ``rag.llm.openai.api.key`` 등이 비어 있으면 ``checkAvailabilityNow`` 가 ``false`` 를 반환하므로 AI 모드를 이용할 수 없습니다
   - ``log4j2.xml`` 에서 ``org.codelibs.fess.llm.gemini`` 를 ``DEBUG`` 로 설정하면 ``[LLM:GEMINI] Gemini is not available. apiKey is blank`` 와 같은 로그로 확인할 수 있습니다

6. LLM 프로바이더로의 네트워크 연결이 가능한가

   - 클라우드 API(Gemini / OpenAI)의 경우 컨테이너에서 외부로 도달할 수 있어야 합니다
   - 프록시 경유가 필요한 경우 ``FESS_JAVA_OPTS`` 에 ``-Dhttps.proxyHost=... -Dhttps.proxyPort=...`` 를 추가하세요

.. note::

   관리 화면 "전체 설정"에는 ``rag.chat.enabled`` 의 체크박스가 없습니다(사양).
   이 값은 FessConfig 계열 프로퍼티이므로 ``fess_config.properties`` 또는
   ``-Dfess.config.rag.chat.enabled=true`` 경유로만 설정할 수 있습니다.

AI 검색 모드가 활성화되지 않음
---------------------------

**확인 사항**:

1. ``rag.chat.enabled=true`` 가 설정되어 있는지
2. ``rag.llm.name`` 으로 LLM 프로바이더가 올바르게 설정되어 있는지
3. 해당 ``fess-llm-*`` 플러그인이 설치되어 있는지
4. LLM 프로바이더에 연결이 가능한지

응답 품질이 낮음
----------------

**개선 방법**:

1. 더 고성능의 LLM 모델 사용
2. ``rag.chat.context.max.documents`` 증가
3. DI XML에서 시스템 프롬프트 커스터마이즈
4. 프로바이더 고유의 temperature 설정 조정(각 ``fess-llm-*`` 플러그인 문서 참조)

응답이 느림
----------------

**개선 방법**:

1. 더 빠른 LLM 모델 사용(예: Gemini Flash)
2. 프로바이더 고유의 max.tokens 설정 감소(각 ``fess-llm-*`` 플러그인 문서 참조)
3. ``rag.chat.context.max.documents`` 감소

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

주요 로그 메시지에는 ``[RAG]`` 프리픽스가 부여되며,
단계별로 ``[RAG:INTENT]``, ``[RAG:EVAL]``, ``[RAG:ANSWER]`` 등의 서브 프리픽스가 사용됩니다.
INFO 레벨에서는 채팅 완료 로그(소요 시간, 소스 수)가 출력되고, DEBUG 레벨에서는 토큰 사용량,
동시 실행 제어, 이력 패킹의 상세 정보가 출력됩니다.

검색 로그와 액세스 타입
------------------------

AI 검색 모드를 통한 검색은 검색 로그의 액세스 타입으로 LLM 프로바이더명(예: ``ollama``, ``openai``, ``gemini``)이
기록됩니다. 이를 통해 일반 웹 검색이나 API 검색과 AI 검색 모드 경유 검색을 구분하여 분석할 수 있습니다.

참고 정보
========

- :doc:`llm-overview` - LLM 통합 개요
- :doc:`llm-ollama` - Ollama 설정
- :doc:`llm-openai` - OpenAI 설정
- :doc:`llm-gemini` - Google Gemini 설정
- :doc:`../api/api-chat` - Chat API 레퍼런스
- :doc:`../user/chat-search` - 최종 사용자용 채팅 검색 가이드
