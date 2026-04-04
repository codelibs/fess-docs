==========================
LLM 통합 개요
==========================

개요
====

|Fess| 15.6에서는 대규모 언어 모델(LLM)을 활용한 AI 검색 모드(RAG: Retrieval-Augmented Generation) 기능을 지원합니다.
이 기능을 통해 사용자는 검색 결과를 기반으로 한 AI 어시스턴트와의 대화 형식으로 정보를 얻을 수 있습니다.

|Fess| 15.6에서는 LLM 연계 기능이 ``fess-llm-*`` 플러그인으로 제공됩니다. 사용할 LLM 프로바이더에 해당하는 플러그인을 도입하세요.

지원 프로바이더
================

|Fess|는 다음 LLM 프로바이더를 지원합니다.

.. list-table::
   :header-rows: 1
   :widths: 20 20 30 30

   * - 프로바이더
     - 설정값
     - 플러그인
     - 설명
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - 로컬 환경에서 동작하는 오픈소스 LLM 서버. Llama, Mistral, Gemma 등의 모델 실행 가능. 기본 설정.
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - OpenAI사의 클라우드 API. GPT-4 등의 모델 이용 가능.
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - Google사의 클라우드 API. Gemini 모델 이용 가능.

플러그인 도입
==============

|Fess| 15.6에서는 LLM 기능이 플러그인으로 분리되어 있습니다. 사용할 프로바이더에 해당하는 ``fess-llm-{provider}`` 플러그인의 JAR 파일을 플러그인 디렉터리에 배치해야 합니다.

예로, OpenAI 프로바이더를 사용하는 경우 ``fess-llm-openai-15.6.0.jar`` 를 다운로드하여 다음 디렉터리에 배치합니다.

::

    app/WEB-INF/plugin/

배치 후 |Fess| 를 재시작하면 플러그인이 로드됩니다.

아키텍처
==============

AI 검색 모드 기능은 다음 흐름으로 동작합니다.

1. **사용자 입력**: 사용자가 채팅 인터페이스에서 질문 입력
2. **의도 분석**: LLM이 사용자 질문을 분석하고 검색 키워드 추출
3. **검색 실행**: |Fess|의 검색 엔진으로 관련 문서 검색
4. **쿼리 재생성**: 검색 결과가 없는 경우 LLM이 쿼리를 재생성하여 재검색
5. **결과 평가**: LLM이 검색 결과의 관련성을 평가하고 최적의 문서 선택
6. **응답 생성**: 선택된 문서를 기반으로 LLM이 응답 생성(Markdown 렌더링 지원)
7. **출처 인용**: 응답에는 참조 문서로의 링크가 포함됨

기본 설정
========

LLM 기능의 설정은 다음 두 곳에서 수행합니다.

관리 화면의 전반 설정 / system.properties
------------------------------------------

관리 화면의 전반 설정 또는 ``system.properties`` 에서 설정합니다. LLM 프로바이더 선택에 사용합니다.

::

    # LLM 프로바이더 지정(ollama, openai, gemini)
    rag.llm.name=ollama

fess_config.properties
----------------------

``app/WEB-INF/conf/fess_config.properties`` 에서 설정합니다. 시작 시 로드되는 설정으로, AI 검색 모드 활성화, 세션·이력 관련 설정 및 프로바이더 고유의 설정(접속 URL, API 키, 생성 파라미터 등)을 수행합니다.

::

    # AI 검색 모드 기능 활성화
    rag.chat.enabled=true

    # 프로바이더 고유 설정 예(OpenAI의 경우)
    rag.llm.openai.api.key=sk-...
    rag.llm.openai.answer.temperature=0.7

각 프로바이더의 상세 설정은 다음 문서를 참조하세요.

- :doc:`llm-ollama` - Ollama 설정
- :doc:`llm-openai` - OpenAI 설정
- :doc:`llm-gemini` - Google Gemini 설정

공통 설정
========

모든 LLM 프로바이더에서 공통으로 사용되는 설정 항목입니다. 이 항목들은 ``fess_config.properties`` 에서 설정합니다.

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
   * - ``rag.chat.content.fields``
     - 문서에서 가져올 필드
     - ``title,url,content,...``

.. note::

   컨텍스트의 최대 문자 수( ``context.max.chars`` )는 프로바이더 및 프롬프트 타입별 설정으로 변경되었습니다. ``fess_config.properties`` 에서 ``rag.llm.{provider}.{promptType}.context.max.chars`` 로 설정하세요.

시스템 프롬프트
------------------

|Fess| 15.6에서는 시스템 프롬프트가 프로퍼티 파일이 아닌 각 플러그인의 DI XML 파일에서 관리됩니다.

각 ``fess-llm-*`` 플러그인에 포함된 ``fess_llm++.xml`` 파일에서 시스템 프롬프트가 정의됩니다. 프롬프트를 커스터마이즈하려면 플러그인 디렉터리 내의 DI XML 파일을 편집하세요.

가용성 체크
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.llm.{provider}.availability.check.interval``
     - LLM 가용성을 체크하는 간격(초). 0으로 비활성화
     - ``60``

이 설정은 ``fess_config.properties`` 에서 수행합니다. |Fess| 는 정기적으로 LLM 프로바이더의 연결 상태를 확인합니다.

세션 관리
==============

채팅 세션 관련 설정입니다. 이 항목들은 ``fess_config.properties`` 에서 설정합니다.

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
     - ``30``

동시 실행 제어
==============

LLM으로의 요청 동시 실행 수를 제어하는 설정입니다. ``fess_config.properties`` 에서 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.llm.{provider}.max.concurrent.requests``
     - 프로바이더로의 최대 동시 요청 수
     - ``5``

예를 들어, OpenAI 프로바이더의 동시 실행 수를 설정하는 경우 다음과 같습니다.

::

    rag.llm.openai.max.concurrent.requests=10

평가 설정
========

검색 결과 평가 관련 설정입니다. ``fess_config.properties`` 에서 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.llm.{provider}.chat.evaluation.max.relevant.docs``
     - 평가 단계에서 선택할 관련 문서의 최대 수
     - ``3``

프롬프트 타입별 설정
======================

|Fess| 15.6에서는 생성 파라미터를 프롬프트 타입별로 설정할 수 있습니다. 이를 통해 용도에 따른 세밀한 조정이 가능합니다. 설정은 ``fess_config.properties`` 에서 수행합니다.

프롬프트 타입 목록
--------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - 프롬프트 타입
     - 설정값
     - 설명
   * - 의도 분석
     - ``intent``
     - 사용자의 질문을 분석하고 검색 키워드를 추출
   * - 평가
     - ``evaluation``
     - 검색 결과의 관련성을 평가
   * - 불명확한 질문
     - ``unclear``
     - 질문이 불명확한 경우의 응답을 생성
   * - 검색 결과 없음
     - ``noresults``
     - 검색 결과가 없을 경우의 응답을 생성
   * - 문서 부재
     - ``docnotfound``
     - 해당 문서가 존재하지 않을 경우의 응답을 생성
   * - 응답 생성
     - ``answer``
     - 검색 결과를 기반으로 응답을 생성
   * - 요약
     - ``summary``
     - 문서의 요약을 생성
   * - FAQ
     - ``faq``
     - FAQ 형식의 응답을 생성
   * - 직접 응답
     - ``direct``
     - 검색을 거치지 않고 직접 응답을 생성
   * - 쿼리 재생성
     - ``queryregeneration``
     - 검색 결과가 없는 경우 쿼리를 재생성

설정 패턴
------------

프롬프트 타입별 설정은 다음 패턴으로 지정합니다.

::

    rag.llm.{provider}.{promptType}.temperature
    rag.llm.{provider}.{promptType}.max.tokens
    rag.llm.{provider}.{promptType}.context.max.chars

설정 예(OpenAI 프로바이더의 경우):

::

    # 응답 생성의 temperature를 낮게 설정
    rag.llm.openai.answer.temperature=0.5
    # 응답 생성의 최대 토큰 수
    rag.llm.openai.answer.max.tokens=4096
    # 의도 분석은 짧은 응답으로 충분하므로 낮게 설정
    rag.llm.openai.intent.max.tokens=256
    # 요약의 컨텍스트 최대 문자 수
    rag.llm.openai.summary.context.max.chars=8000

다음 단계
============

- :doc:`llm-ollama` - Ollama 상세 설정
- :doc:`llm-openai` - OpenAI 상세 설정
- :doc:`llm-gemini` - Google Gemini 상세 설정
- :doc:`rag-chat` - AI 검색 모드 기능 상세 설정
- :doc:`rank-fusion` - Rank Fusion 설정(하이브리드 검색 결과 통합)
