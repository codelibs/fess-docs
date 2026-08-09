==============================
AI 검색(RAG) 및 LLM 통합 개요
==============================

개요
====

|Fess| 는 대규모 언어 모델(LLM)을 활용한 AI 검색 모드(RAG: Retrieval-Augmented Generation) 기능을 지원합니다.
이 기능을 통해 사용자는 검색 결과를 기반으로 한 AI 어시스턴트와의 대화 형식으로 정보를 얻을 수 있으며, 사내 검색 인덱스를 기반으로 자연어 질문에 출처를 인용하여 직접 답변받을 수 있습니다.

LLM 연계 기능은 ``fess-llm-*`` 플러그인으로 제공됩니다. 사용할 LLM 프로바이더에 해당하는 플러그인을 도입하세요.

AI 검색 모드는 전용 벡터 인덱스가 아닌 |Fess|\ 의 표준 검색 파이프라인(Rank Fusion)을 통해 문서를 취득하며,
기본값으로 키워드(BM25) 검색이 사용됩니다. 이 표준 파이프라인을 재사용하기 때문에 코어에 통합된 시맨틱
검색(콘텐츠 청킹 + 벡터 검색)을 활성화하면 해당 시맨틱 서처가 AI 검색 모드의 검색 단계를 포함한 모든
검색에서 Rank Fusion에 참여합니다. 시맨틱 서처를 참여시키기 위한 AI 검색 모드 전용 설정은 필요하지
않습니다. 다만 답변 생성에 전달할 청크 수는 ``content_chunker.chat.top_k`` 로 조정할 수 있습니다.
자세한 내용은 :doc:`rank-fusion` 및 :doc:`search-semantic` 을 참조하세요.

지원 프로바이더
================

|Fess| 는 다음 LLM 프로바이더를 지원합니다.

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
     - OpenAI사의 클라우드 API. GPT-5 등의 모델 이용 가능.
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - Google사의 클라우드 API. Gemini 모델 이용 가능.

프로바이더 비교
----------------

.. list-table::
   :header-rows: 1

   * - 프로바이더( ``rag.llm.name`` )
     - 기본 모델
     - 엔드포인트
     - 인증
     - 데이터 저장 위치
   * - Ollama( ``ollama`` )
     - ``gemma4:e4b``
     - ``http://localhost:11434``
     - 없음(로컬)
     - 로컬 / 자체 호스팅 — 질문과 문서가 호스트 내에 머무릅니다
   * - OpenAI( ``openai`` )
     - ``gpt-5-mini``
     - ``https://api.openai.com/v1``
     - ``Authorization: Bearer`` ( ``rag.llm.openai.api.key`` )
     - 클라우드 — 질문과 취득된 문서가 OpenAI로 전송됩니다
   * - Google Gemini( ``gemini`` )
     - ``gemini-3.1-flash-lite-preview``
     - ``https://generativelanguage.googleapis.com/v1beta``
     - ``x-goog-api-key`` ( ``rag.llm.gemini.api.key`` )
     - 클라우드 — 질문과 취득된 문서가 Google로 전송됩니다

.. note::

   ``rag.llm.name`` 의 기본값은 ``ollama`` 입니다. 이 값은 로드할 DI 컴포넌트 이름( ``{rag.llm.name}LlmClient`` )을 결정하는 데 사용됩니다.
   따라서 ``rag.llm.name`` 을 기본값으로 둔 채 ``fess-llm-ollama`` 이외의 플러그인만 도입한 경우, LLM 클라이언트가 하나도 활성화되지 않습니다.
   이때 로그에 ``[LLM] LlmClient not found. componentName=ollamaLlmClient`` 라는 경고가 출력되며, AI 검색 모드를 사용할 수 없습니다.
   도입한 플러그인에 맞춰 반드시 ``rag.llm.name`` 을 설정하세요. ``none`` 을 지정하면 LLM 연계를 명시적으로 비활성화할 수 있습니다.

플러그인 도입
==============

LLM 기능은 플러그인으로 제공됩니다. 사용할 프로바이더에 해당하는 ``fess-llm-{provider}`` 플러그인을 도입하세요.

관리 화면의 「시스템 > 플러그인」 페이지에서 설치할 수 있습니다. ``fess-llm-*`` 플러그인은 설치 가능한 플러그인 목록에 표시됩니다.

수동으로 도입하는 경우, 해당하는 JAR 파일(예: OpenAI 프로바이더의 경우 ``fess-llm-openai-15.8.0.jar`` )을 다음 디렉터리에 배치합니다.

::

    app/WEB-INF/plugin/

어느 방법으로 도입하든, 도입 후 |Fess|\ 를 재시작하면 플러그인이 로드됩니다.

아키텍처
==============

AI 검색 모드 기능은 다음 흐름으로 동작합니다.

1. **사용자 입력**: 사용자가 채팅 인터페이스에서 질문을 입력
2. **의도 분석（intent）**: LLM이 사용자 질문을 분석하고 검색 키워드를 추출
3. **검색 실행（search）**: |Fess| 의 검색 엔진으로 관련 문서를 검색
4. **결과 평가（evaluate）**: LLM이 검색 결과의 관련성을 평가하고 최적의 문서를 선택
5. **쿼리 재생성（필요에 따라）**: 검색 결과가 없거나, 평가에서 관련 문서가 발견되지 않은 경우 LLM이 쿼리를 재생성하여 재검색
6. **콘텐츠 취득（fetch）**: 선택된 문서의 본문을 취득
7. **응답 생성（answer）**: 취득한 문서를 기반으로 LLM이 응답을 생성（Markdown 렌더링 지원）
8. **출처 인용**: 응답에는 참조 문서로의 링크가 포함됨

.. note::

   내부 처리는 ``intent`` 、 ``search`` 、 ``evaluate`` 、 ``fetch`` 、 ``answer`` 의 5단계 페이즈로 구성되며, 각 페이즈의 진행 상황은 스트리밍（SSE）으로 클라이언트에 통보됩니다.
   쿼리 재생성은 독립된 페이즈가 아니라 ``search`` 페이즈의 폴백으로 통보되며, 이후 ``search`` 가 재실행됩니다.

.. note::

   위 흐름은 스트리밍 API에서 의도가 "검색"으로 판정된 경우의 흐름입니다. 의도 판정 결과에 따라 경로가 달라집니다.
   질문이 불명확하다고 판정된 경우에는 검색을 수행하지 않고 응답을 생성하며, URL 요약을 요청받은 경우에는 URL 검색을 수행하고 평가 페이즈는 실행하지 않습니다.
   또한 비스트리밍 방식인 ``POST /api/v2/chat`` 은 평가 페이즈를 실행하지 않으며, 페이즈 단위의 진행 상황 통보도 하지 않습니다.

기본 설정
=========

LLM 기능의 설정은 다음 두 곳에서 수행합니다.

관리 화면의 전반 설정 / system.properties
------------------------------------------

관리 화면의 전반 설정 또는 ``system.properties`` 에서 설정합니다. LLM 프로바이더 선택에 사용합니다.

::

    # LLM 프로바이더 지정（ollama, openai, gemini）
    rag.llm.name=ollama

fess_config.properties
----------------------

``app/WEB-INF/classes/fess_config.properties`` (패키지 버전에서는 ``/etc/fess/fess_config.properties`` )에서 설정합니다. AI 검색 모드 활성화, 세션·이력 관련 설정 외에 프로바이더 고유의 설정（접속 URL, API 키, 생성 파라미터 등）도 이 파일에 기술합니다.

::

    # AI 검색 모드 기능 활성화（기본값은 false）
    rag.chat.enabled=true

    # 프로바이더 고유 설정 예（OpenAI의 경우）
    rag.llm.openai.api.key=sk-...
    rag.llm.openai.answer.temperature=0.7

각 프로바이더의 상세 설정은 다음 문서를 참조하세요.

- :doc:`llm-ollama` - Ollama 설정
- :doc:`llm-openai` - OpenAI 설정
- :doc:`llm-gemini` - Google Gemini 설정

공통 설정
=========

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
     - ``title,url,content,doc_id,content_title,content_description``

.. note::

   컨텍스트의 최대 문자 수（ ``context.max.chars`` ）는 프로바이더 및 프롬프트 타입별 설정으로 변경되었습니다. ``fess_config.properties`` 에서 ``rag.llm.{provider}.{promptType}.context.max.chars`` 로 설정하세요.

시스템 프롬프트
------------------

시스템 프롬프트는 프로퍼티 파일이 아닌 각 플러그인의 DI XML 파일에서 관리됩니다.

각 ``fess-llm-*`` 플러그인의 JAR 파일 내에 포함된 ``fess_llm++.xml`` 파일에서 시스템 프롬프트가 정의됩니다.
프롬프트를 커스터마이즈하기 위해 JAR 파일을 압축 해제하여 다시 편집할 필요는 없습니다. LastaDi의 컴포넌트 재정의 메커니즘을 통해
``app/WEB-INF/classes/`` 에 ``fess_llm+{컴포넌트 이름}.xml`` 이라는 이름의 파일을 배치하면 플러그인 측의 컴포넌트 정의를 대체할 수 있습니다.

컴포넌트 이름은 프로바이더별로 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 프로바이더
     - 컴포넌트 이름
   * - Ollama
     - ``ollamaLlmClient``
   * - OpenAI
     - ``openaiLlmClient``
   * - Google Gemini
     - ``geminiLlmClient``

예로, OpenAI 프로바이더의 답변 생성 프롬프트를 변경하는 경우 ``app/WEB-INF/classes/fess_llm+openaiLlmClient.xml`` 을 작성합니다.

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="openaiLlmClient" class="org.codelibs.fess.llm.openai.OpenAiLlmClient">
            <postConstruct name="register"/>
            <postConstruct name="init"/>
            <preDestroy name="destroy"/>
            <property name="answerGenerationSystemPrompt">"고유한 답변 생성 프롬프트"</property>
            <!-- 변경하지 않는 프롬프트 프로퍼티도 모두 기술한다 -->
        </component>
    </components>

.. warning::

   재정의 파일은 컴포넌트 정의를 대체합니다. 따라서 원본 ``fess_llm++.xml`` 에 기술되어 있는 내용(클래스명, ``postConstruct`` ,
   ``preDestroy`` , 그리고 변경하지 않는 프롬프트 프로퍼티)을 모두 포함해야 합니다. 기술하지 않은 프로퍼티는 미설정 상태로 돌아갑니다.

.. warning::

   ``fess_llm++.xml`` 자체를 복사하여 ``app/WEB-INF/classes/`` 에 배치하지 마세요.
   파일명이 ``++`` 로 끝나는 DI XML은 클래스패스상의 모든 것이 "추가"로 로드되기 때문에 같은 이름의 컴포넌트가 이중으로 등록되어,
   ``TooManyRegistrationComponentException`` 이 발생하여 |Fess|\ 가 시작되지 않습니다.

가용성 체크
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.llm.{provider}.availability.check.interval``
     - LLM 가용성을 정기적으로 체크하는 간격(초)
     - ``60``

이 설정은 ``fess_config.properties`` 에서 수행합니다. |Fess| 는 정기적으로 LLM 프로바이더의 연결 상태를 확인합니다.

.. note::

   이 프로퍼티에 ``0`` 이하의 값이나 숫자가 아닌 값을 지정한 경우, 그 값은 무시되고 기본값( ``60`` )이 사용됩니다.
   이 프로퍼티로는 가용성 체크를 비활성화할 수 없습니다.
   또한 가용성 체크는 ``rag.chat.enabled`` 가 ``false`` 인 경우, 그리고 ``rag.llm.name`` 에서 선택되지 않은 프로바이더에서는 실행되지 않습니다.

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
     - 세션 타임아웃 시간（분）
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
   * - ``rag.llm.{provider}.concurrency.wait.timeout``
     - 동시 실행 수 상한에 도달했을 때 빈자리를 대기하는 최대 시간（밀리초）. 이 시간 내에 빈자리를 얻지 못한 경우 레이트 제한 오류가 발생합니다
     - ``30000``

예를 들어, OpenAI 프로바이더의 동시 실행 수를 설정하는 경우 다음과 같습니다.

::

    rag.llm.openai.max.concurrent.requests=10

평가 설정
=========

검색 결과 평가 관련 설정입니다. ``fess_config.properties`` 에서 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.llm.{provider}.chat.evaluation.max.relevant.docs``
     - 평가 페이즈에서 선택할 관련 문서의 최대 수
     - ``3``

프롬프트 타입별 설정
======================

생성 파라미터는 프롬프트 타입별로 설정할 수 있습니다. 이를 통해 용도에 따른 세밀한 조정이 가능합니다. 설정은 ``fess_config.properties`` 에서 수행합니다.

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
     - 사용자의 질문을 분석하고 검색 키워드를 추출한다
   * - 평가
     - ``evaluation``
     - 검색 결과의 관련성을 평가한다
   * - 불명확한 질문
     - ``unclear``
     - 질문이 불명확한 경우의 응답을 생성한다
   * - 검색 결과 없음
     - ``noresults``
     - 검색 결과가 없을 경우의 응답을 생성한다
   * - 문서 부재
     - ``docnotfound``
     - 해당 문서가 존재하지 않을 경우의 응답을 생성한다
   * - 응답 생성
     - ``answer``
     - 검색 결과를 기반으로 응답을 생성한다
   * - 요약
     - ``summary``
     - 문서의 요약을 생성한다
   * - FAQ
     - ``faq``
     - FAQ 형식의 응답을 생성한다
   * - 직접 응답
     - ``direct``
     - 검색을 거치지 않고 직접 응답을 생성한다(현재 버전에서는 호출되지 않습니다)
   * - 쿼리 재생성
     - ``queryregeneration``
     - 검색 결과가 없는 경우 쿼리를 재생성한다

설정 패턴
------------

프롬프트 타입별 설정은 다음 패턴으로 지정합니다.

::

    rag.llm.{provider}.{promptType}.temperature
    rag.llm.{provider}.{promptType}.max.tokens
    rag.llm.{provider}.{promptType}.context.max.chars

설정 예（OpenAI 프로바이더의 경우）:

::

    # 응답 생성의 temperature를 낮게 설정
    rag.llm.openai.answer.temperature=0.5
    # 응답 생성의 최대 토큰 수
    rag.llm.openai.answer.max.tokens=4096
    # 의도 분석은 짧은 응답으로 충분하므로 낮게 설정
    rag.llm.openai.intent.max.tokens=256
    # 요약의 컨텍스트 최대 문자 수
    rag.llm.openai.summary.context.max.chars=8000

.. note::

   ``temperature`` , ``max.tokens`` , ``context.max.chars`` 는 모든 프로바이더에서 공통으로 사용할 수 있습니다. 단, 이 값들의 기본값은 프로바이더 및 프롬프트 타입별로 다릅니다.

이 외에도 각 프로바이더는 고유의 파라미터를 지원합니다. 지원 현황은 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 40 20 20 20

   * - 파라미터
     - Ollama
     - OpenAI
     - Gemini
   * - ``thinking.budget``
     - 지원
     - 미지원
     - 지원
   * - ``thinking.level``
     - 지원
     - 미지원
     - 미지원
   * - ``top.p``
     - 지원
     - 지원
     - 미지원
   * - ``top.k`` , ``num.ctx``
     - 지원
     - 미지원
     - 미지원
   * - ``reasoning.effort``
     - 미지원
     - 지원
     - 미지원
   * - ``frequency.penalty`` , ``presence.penalty``
     - 미지원
     - 지원
     - 미지원

.. note::

   "미지원" 파라미터를 지정해도 오류가 발생하지 않으며 단순히 무시됩니다. 각 파라미터의 의미나 설정 가능한 값에 대한 자세한 내용은 각 프로바이더의 문서를 참조하세요.

.. note::

   Ollama 프로바이더에서만, 프롬프트 타입별 설정이 존재하지 않는 경우 ``rag.llm.ollama.default.{파라미터}`` 를 참조하는 폴백이 있습니다
   ( ``context.max.chars`` 는 제외). OpenAI 프로바이더와 Gemini 프로바이더에는 이 폴백이 없으며,
   프롬프트 타입별 설정이 없는 경우 플러그인에 내장된 기본값이 사용됩니다.

다음 단계
============

- :doc:`llm-ollama` - Ollama 상세 설정
- :doc:`llm-openai` - OpenAI 상세 설정
- :doc:`llm-gemini` - Google Gemini 상세 설정
- :doc:`rag-chat` - AI 검색 모드 기능 상세 설정
- :doc:`rank-fusion` - Rank Fusion 설정（하이브리드 검색 결과 통합）
- :doc:`../user/chat-search` - AI 검색 모드 사용법
- :doc:`../api/api-chat` - 채팅 API 레퍼런스
