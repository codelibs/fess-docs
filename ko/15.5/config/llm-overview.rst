==========================
LLM 통합 개요
==========================

개요
====

|Fess| 15.5에서는 대규모 언어 모델(LLM)을 활용한 AI 모드(RAG: Retrieval-Augmented Generation) 기능을 지원합니다.
이 기능을 통해 사용자는 검색 결과를 기반으로 한 AI 어시스턴트와의 대화 형식으로 정보를 얻을 수 있습니다.

지원 프로바이더
================

|Fess|는 다음 LLM 프로바이더를 지원합니다.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - 프로바이더
     - 설정값
     - 설명
   * - Ollama
     - ``ollama``
     - 로컬 환경에서 동작하는 오픈소스 LLM 서버. Llama, Mistral, Gemma 등의 모델 실행 가능. 기본 설정.
   * - OpenAI
     - ``openai``
     - OpenAI사의 클라우드 API. GPT-4 등의 모델 이용 가능.
   * - Google Gemini
     - ``gemini``
     - Google사의 클라우드 API. Gemini 모델 이용 가능.

아키텍처
==============

AI 모드 기능은 다음 흐름으로 동작합니다.

1. **사용자 입력**: 사용자가 채팅 인터페이스에서 질문 입력
2. **의도 분석**: LLM이 사용자 질문을 분석하고 검색 키워드 추출
3. **검색 실행**: |Fess|의 검색 엔진으로 관련 문서 검색
4. **결과 평가**: LLM이 검색 결과의 관련성을 평가하고 최적의 문서 선택
5. **응답 생성**: 선택된 문서를 기반으로 LLM이 응답 생성
6. **출처 인용**: 응답에는 참조 문서로의 링크가 포함됨

기본 설정
========

LLM 기능을 활성화하려면 ``app/WEB-INF/conf/fess_config.properties``에 다음 설정을 추가합니다.

AI 모드 활성화
-------------------

::

    # AI 모드 기능 활성화
    rag.chat.enabled=true

LLM 프로바이더 선택
---------------------

::

    # LLM 프로바이더 지정(ollama, openai, gemini)
    rag.llm.type=ollama

각 프로바이더의 상세 설정은 다음 문서를 참조하세요.

- :doc:`llm-ollama` - Ollama 설정
- :doc:`llm-openai` - OpenAI 설정
- :doc:`llm-gemini` - Google Gemini 설정

공통 설정
========

모든 LLM 프로바이더에서 공통으로 사용되는 설정 항목입니다.

생성 파라미터
----------------

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
     - 생성의 무작위성(0.0~1.0). 낮을수록 결정적인 응답
     - ``0.7``

컨텍스트 설정
----------------

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

시스템 프롬프트
------------------

::

    rag.chat.system.prompt=You are an AI assistant for Fess search engine. Answer questions based on the search results provided. Always cite your sources using [1], [2], etc.

이 프롬프트는 LLM의 기본 동작을 정의합니다. 필요에 따라 커스터마이즈할 수 있습니다.

가용성 체크
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.llm.availability.check.interval``
     - LLM 가용성을 체크하는 간격(초). 0으로 비활성화
     - ``60``

이 설정으로 |Fess|는 정기적으로 LLM 프로바이더의 연결 상태를 확인합니다.

세션 관리
==============

채팅 세션 관련 설정입니다.

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
     - 세션 최대 수
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - 대화 이력에 유지할 최대 메시지 수
     - ``20``

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

평가 설정
========

검색 결과 평가 관련 설정입니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.chat.evaluation.max.relevant.docs``
     - 평가 단계에서 선택할 관련 문서의 최대 수
     - ``3``

다음 단계
============

- :doc:`llm-ollama` - Ollama 상세 설정
- :doc:`llm-openai` - OpenAI 상세 설정
- :doc:`llm-gemini` - Google Gemini 상세 설정
- :doc:`rag-chat` - AI 모드 기능 상세 설정
- :doc:`rank-fusion` - Rank Fusion 설정 (하이브리드 검색 결과 통합)
