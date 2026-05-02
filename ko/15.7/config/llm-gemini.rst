==========================
Google Gemini 설정
==========================

개요
====

Google Gemini는 Google사가 제공하는 최첨단 대규모 언어 모델(LLM)입니다.
|Fess|에서는 Google AI API(Generative Language API)를 사용하여 Gemini 모델을 통한 AI 검색 모드 기능을 구현할 수 있습니다.

Gemini를 사용하면 Google의 최신 AI 기술을 활용한 고품질 응답 생성이 가능합니다.

주요 특징
--------

- **멀티모달 지원**: 텍스트뿐만 아니라 이미지도 처리 가능
- **긴 컨텍스트**: 대량의 문서를 한 번에 처리할 수 있는 긴 컨텍스트 윈도우
- **비용 효율**: Flash 모델은 빠르고 저렴
- **Google 통합**: Google Cloud 서비스와의 연계 용이

지원 모델
----------

Gemini에서 이용 가능한 주요 모델:

- ``gemini-3-flash-preview`` - 최신 고속 모델(권장)
- ``gemini-3.1-pro-preview`` - 최신 고추론 모델
- ``gemini-2.5-flash`` - 안정 버전의 고속 모델
- ``gemini-2.5-pro`` - 안정 버전의 고추론 모델

.. note::
   이용 가능한 모델의 최신 정보는 `Google AI for Developers <https://ai.google.dev/models/gemini>`__에서 확인할 수 있습니다.

전제조건
========

Gemini를 사용하기 전에 다음을 준비하세요.

1. **Google 계정**: Google 계정 필요
2. **Google AI Studio 액세스**: `https://aistudio.google.com/ <https://aistudio.google.com/>`__에 액세스
3. **API 키**: Google AI Studio에서 API 키 생성

API 키 발급
-------------

1. `Google AI Studio <https://aistudio.google.com/>`__에 액세스
2. "Get API key" 클릭
3. "Create API key" 선택
4. 프로젝트 선택 또는 새로 생성
5. 생성된 API 키를 안전하게 저장

.. warning::
   API 키는 기밀 정보입니다. 다음 사항에 주의하세요:

   - 버전 관리 시스템에 커밋하지 않기
   - 로그에 출력하지 않기
   - 환경 변수나 안전한 설정 파일에서 관리

플러그인 설치
========================

|Fess| 15.7에서는 Gemini 연계 기능이 ``fess-llm-gemini`` 플러그인으로 제공됩니다.
Gemini를 사용하려면 플러그인 설치가 필요합니다.

1. `fess-llm-gemini-15.7.0.jar` 를 다운로드합니다
2. |Fess| 의 ``app/WEB-INF/plugin/`` 디렉터리에 배치합니다
3. |Fess| 를 재시작합니다

::

    # 플러그인 배치 예
    cp fess-llm-gemini-15.7.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   플러그인 버전은 |Fess| 버전과 맞춰주세요.

기본 설정
========

|Fess| 15.7에서는 AI 검색 모드 기능 활성화 및 Gemini 고유 설정은 ``fess_config.properties`` 에서 수행하고, LLM 프로바이더 선택은 관리 화면 또는 ``system.properties`` 에서 수행합니다.

fess_config.properties 설정
----------------------------

``app/WEB-INF/conf/fess_config.properties`` 에 AI 검색 모드 기능 활성화 설정을 추가합니다.

::

    # AI 검색 모드 기능 활성화
    rag.chat.enabled=true

LLM 프로바이더 설정
---------------------

LLM 프로바이더는 관리 화면(관리 화면 > 시스템 > 전반)에서 설정하거나 ``system.properties`` 에 설정합니다.

최소 구성
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``app/WEB-INF/conf/fess_config.properties``:

::

    # Gemini API 키
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # 사용할 모델
    rag.llm.gemini.model=gemini-3-flash-preview

``system.properties``(관리 화면 > 시스템 > 전반 에서도 설정 가능):

::

    # LLM 프로바이더를 Gemini로 설정
    rag.llm.name=gemini

권장 구성(프로덕션 환경)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``app/WEB-INF/conf/fess_config.properties``:

::

    # Gemini API 키
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # 모델 설정(고속 모델 사용)
    rag.llm.gemini.model=gemini-3-flash-preview

    # API 엔드포인트(일반적으로 변경 불필요)
    rag.llm.gemini.api.url=https://generativelanguage.googleapis.com/v1beta

    # 타임아웃 설정
    rag.llm.gemini.timeout=60000

``system.properties``(관리 화면 > 시스템 > 전반 에서도 설정 가능):

::

    # LLM 프로바이더를 Gemini로 설정
    rag.llm.name=gemini

설정 항목
========

Gemini 클라이언트에서 사용 가능한 모든 설정 항목입니다. 모두 ``fess_config.properties`` 에 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.llm.gemini.api.key``
     - Google AI API 키(Gemini API를 사용하려면 설정이 필요합니다)
     - ``""``
   * - ``rag.llm.gemini.model``
     - 사용할 모델명
     - ``gemini-3-flash-preview``
   * - ``rag.llm.gemini.api.url``
     - API의 기본 URL
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - 요청 타임아웃 시간(밀리초)
     - ``60000``
   * - ``rag.llm.gemini.availability.check.interval``
     - 가용성 체크 간격(초)
     - ``60``
   * - ``rag.llm.gemini.max.concurrent.requests``
     - 최대 동시 요청 수
     - ``5``
   * - ``rag.llm.gemini.chat.evaluation.max.relevant.docs``
     - 평가 시 최대 관련 문서 수
     - ``3``
   * - ``rag.llm.gemini.chat.evaluation.description.max.chars``
     - 평가 시 문서 설명 최대 문자 수
     - ``500``
   * - ``rag.llm.gemini.concurrency.wait.timeout``
     - 동시 요청 대기 타임아웃(밀리초)
     - ``30000``
   * - ``rag.llm.gemini.history.max.chars``
     - 채팅 이력의 최대 문자 수
     - ``10000``
   * - ``rag.llm.gemini.intent.history.max.messages``
     - 의도 판정 시 이력 최대 메시지 수
     - ``10``
   * - ``rag.llm.gemini.intent.history.max.chars``
     - 의도 판정 시 이력 최대 문자 수
     - ``5000``
   * - ``rag.llm.gemini.history.assistant.max.chars``
     - 어시스턴트 이력의 최대 문자 수
     - ``1000``
   * - ``rag.llm.gemini.history.assistant.summary.max.chars``
     - 어시스턴트 요약 이력의 최대 문자 수
     - ``1000``

프롬프트 타입별 설정
======================

|Fess|에서는 프롬프트 종류별로 LLM 파라미터를 세밀하게 설정할 수 있습니다.
프롬프트 타입별 설정은 ``fess_config.properties`` 에 기술합니다.

설정 형식
----------------

::

    rag.llm.gemini.{promptType}.temperature
    rag.llm.gemini.{promptType}.max.tokens
    rag.llm.gemini.{promptType}.thinking.budget
    rag.llm.gemini.{promptType}.context.max.chars

이용 가능한 프롬프트 타입
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 프롬프트 타입
     - 설명
   * - ``intent``
     - 사용자의 의도를 판정하는 프롬프트
   * - ``evaluation``
     - 문서의 관련성을 평가하는 프롬프트
   * - ``unclear``
     - 질문이 불명확한 경우의 프롬프트
   * - ``noresults``
     - 검색 결과가 없을 경우의 프롬프트
   * - ``docnotfound``
     - 문서를 찾을 수 없을 경우의 프롬프트
   * - ``answer``
     - 응답 생성 프롬프트
   * - ``summary``
     - 요약 생성 프롬프트
   * - ``faq``
     - FAQ 생성 프롬프트
   * - ``direct``
     - 직접 응답 프롬프트
   * - ``queryregeneration``
     - 쿼리 재생성 프롬프트

프롬프트 타입별 기본값
------------------------------

각 프롬프트 타입의 기본값은 다음과 같습니다. 설정되지 않은 경우 이 값이 사용됩니다.

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20

   * - 프롬프트 타입
     - temperature
     - max.tokens
     - thinking.budget
   * - ``intent``
     - ``0.1``
     - ``256``
     - ``0``
   * - ``evaluation``
     - ``0.1``
     - ``256``
     - ``0``
   * - ``unclear``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``noresults``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``docnotfound``
     - ``0.7``
     - ``256``
     - ``0``
   * - ``direct``
     - ``0.7``
     - ``2048``
     - ``1024``
   * - ``faq``
     - ``0.7``
     - ``2048``
     - ``1024``
   * - ``answer``
     - ``0.5``
     - ``4096``
     - ``2048``
   * - ``summary``
     - ``0.3``
     - ``4096``
     - ``2048``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``
     - ``0``

설정 예
------

::

    # 응답 생성의 temperature 설정
    rag.llm.gemini.answer.temperature=0.7

    # 요약 생성의 최대 토큰 수
    rag.llm.gemini.summary.max.tokens=2048

    # 응답 생성의 컨텍스트 최대 문자 수
    rag.llm.gemini.answer.context.max.chars=16000

    # 요약 생성의 컨텍스트 최대 문자 수
    rag.llm.gemini.summary.context.max.chars=16000

    # FAQ 생성의 컨텍스트 최대 문자 수
    rag.llm.gemini.faq.context.max.chars=10000

.. note::
   ``context.max.chars`` 의 기본값은 프롬프트 타입에 따라 다릅니다.
   ``answer`` 와 ``summary`` 는 16000, ``faq`` 는 10000, 기타 프롬프트 타입은 10000입니다.

사고 모델 지원
==============

Gemini에서는 사고 모델(Thinking Model)을 지원합니다.
사고 모델을 사용하면 모델이 응답을 생성하기 전에 내부적인 추론 프로세스를 실행하여 더 정확한 응답을 생성할 수 있습니다.

프롬프트 타입별로 ``fess_config.properties`` 에서 사고 버짓을 설정할 수 있습니다.

::

    # 응답 생성 시 사고 버짓 설정
    rag.llm.gemini.answer.thinking.budget=1024

    # 요약 생성 시 사고 버짓 설정
    rag.llm.gemini.summary.thinking.budget=1024

.. note::
   사고 버짓을 설정하면 응답 시간이 길어질 수 있습니다.
   용도에 따라 적절한 값을 설정하세요.

JVM 옵션 설정
=============

보안상의 이유로 API 키는 체크인된 파일이 아니라 런타임 환경(JVM 옵션)을 통해
설정하는 것을 권장합니다.

Docker 환경
-----------

공식 `docker-fess <https://github.com/codelibs/docker-fess>`__ 리포지토리에는
Gemini용 오버레이 ``compose-gemini.yaml`` 이 포함되어 있습니다. 최소 절차:

::

    export GEMINI_API_KEY="AIzaSy..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

``compose-gemini.yaml`` 의 내용 (동등 구성을 직접 작성할 때의 참고):

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-gemini:15.7.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=${GEMINI_API_KEY:-} -Dfess.config.rag.llm.gemini.model=${GEMINI_MODEL:-gemini-2.5-flash} -Dfess.system.rag.llm.name=gemini"

요점:

- ``FESS_PLUGINS=fess-llm-gemini:15.7.0`` 으로 컨테이너의 ``run.sh`` 가 플러그인 JAR을 자동 다운로드하여 ``app/WEB-INF/plugin/`` 에 배치합니다
- ``-Dfess.config.rag.chat.enabled=true`` 로 AI 검색 모드를 활성화
- ``-Dfess.config.rag.llm.gemini.api.key=...`` 로 API 키, ``-Dfess.config.rag.llm.gemini.model=...`` 로 모델 지정
- ``-Dfess.system.rag.llm.name=gemini`` 는 OpenSearch에 값이 아직 기록되지 않은 첫 시작 시에만 기본값으로 적용됩니다. 시작 후에는 관리 화면 "시스템 > 전체 설정" 의 RAG 섹션에서도 변경할 수 있습니다

프록시 경유로 인터넷에 접속하는 경우 ``FESS_JAVA_OPTS`` 에
``-Dhttps.proxyHost=... -Dhttps.proxyPort=...`` 를 추가하세요.

systemd 환경
------------

``/etc/sysconfig/fess`` (또는 ``/etc/default/fess`` )의 ``FESS_JAVA_OPTS`` 에 추가합니다:

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=AIzaSy... -Dfess.system.rag.llm.name=gemini"

Vertex AI 사용
===================

Google Cloud Platform을 사용하는 경우 Vertex AI를 통해 Gemini를 사용할 수도 있습니다.
Vertex AI를 사용하는 경우 API 엔드포인트와 인증 방법이 다릅니다.

.. note::
   현재 |Fess|는 Google AI API(generativelanguage.googleapis.com)를 사용합니다.
   Vertex AI를 통한 사용이 필요한 경우 커스텀 구현이 필요할 수 있습니다.

모델 선택 가이드
==================

사용 목적에 맞는 모델 선택 지침입니다.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - 모델
     - 속도
     - 품질
     - 용도
   * - ``gemini-3-flash-preview``
     - 고속
     - 최고
     - 일반적인 용도(권장)
   * - ``gemini-3.1-pro-preview``
     - 중속
     - 최고
     - 복잡한 추론
   * - ``gemini-2.5-flash``
     - 고속
     - 높음
     - 안정 버전, 비용 중시
   * - ``gemini-2.5-pro``
     - 중속
     - 높음
     - 안정 버전, 긴 컨텍스트

컨텍스트 윈도우
----------------------

Gemini 모델은 매우 긴 컨텍스트 윈도우를 지원합니다:

- **Gemini 3 Flash / 2.5 Flash**: 최대 100만 토큰
- **Gemini 3.1 Pro / 2.5 Pro**: 최대 100만 토큰(3.1 Pro) / 200만 토큰(2.5 Pro)

이 특징을 활용하여 더 많은 검색 결과를 컨텍스트에 포함할 수 있습니다.

::

    # 더 많은 문서를 컨텍스트에 포함(fess_config.properties에 설정)
    rag.llm.gemini.answer.context.max.chars=20000

비용 기준
------------

Google AI API는 사용량에 따라 요금이 부과됩니다(무료 할당량 있음).

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 모델
     - 입력(100만 문자)
     - 출력(100만 문자)
   * - Gemini 3 Flash Preview
     - $0.50
     - $3.00
   * - Gemini 3.1 Pro Preview
     - $2.00
     - $12.00
   * - Gemini 2.5 Flash
     - $0.075
     - $0.30
   * - Gemini 2.5 Pro
     - $1.25
     - $5.00

.. note::
   최신 가격 및 무료 할당량 정보는 `Google AI Pricing <https://ai.google.dev/pricing>`__에서 확인하세요.

동시 요청 제어
==================

|Fess|에서는 Gemini로의 동시 요청 수를 제어할 수 있습니다.
``fess_config.properties`` 에서 다음 프로퍼티를 설정하세요.

::

    # 최대 동시 요청 수(기본값: 5)
    rag.llm.gemini.max.concurrent.requests=5

이 설정을 통해 Google AI API로의 과도한 요청을 방지하고 레이트 제한 오류를 회피할 수 있습니다.

무료 할당량 제한(참고)
--------------------

Google AI API에는 무료 할당량이 있지만 다음 제한이 있습니다:

- 요청/분: 15 RPM
- 토큰/분: 100만 TPM
- 요청/일: 1,500 RPD

무료 할당량을 사용하는 경우 ``rag.llm.gemini.max.concurrent.requests`` 를 낮게 설정하는 것을 권장합니다.

문제 해결
======================

인증 오류
----------

**증상**: API 키 관련 오류 발생

**확인 사항**:

1. API 키가 올바르게 설정되었는지 확인
2. API 키가 Google AI Studio에서 유효한지 확인
3. API 키에 필요한 권한이 있는지 확인
4. API가 프로젝트에서 활성화되어 있는지 확인

레이트 제한 오류
----------------

**증상**: "429 Resource has been exhausted" 오류 발생

**해결 방법**:

1. ``fess_config.properties`` 에서 동시 요청 수를 줄이기::

    rag.llm.gemini.max.concurrent.requests=3

2. 몇 분 후 재시도
3. 필요 시 쿼터 증가 요청

리전 제한
--------------

**증상**: 서비스를 사용할 수 없다는 오류

**확인 사항**:

Google AI API는 일부 지역에서만 사용 가능합니다. 지원되는 지역에 대해서는
Google 문서를 확인하세요.

타임아웃
------------

**증상**: 요청이 타임아웃됨

**해결 방법**:

1. 타임아웃 시간 연장::

    rag.llm.gemini.timeout=120000

2. Flash 모델(더 빠름) 사용 검토

디버그 설정
------------

문제를 조사할 때는 |Fess|의 로그 레벨을 조정하여 Gemini 관련 상세 로그를 출력할 수 있습니다.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.gemini" level="DEBUG"/>

보안 관련 주의사항
========================

Google AI API를 사용할 때는 다음 보안 사항에 주의하세요.

1. **데이터 프라이버시**: 검색 결과의 내용이 Google 서버로 전송됩니다
2. **API 키 관리**: 키 유출은 부정 사용으로 이어집니다
3. **규정 준수**: 기밀 데이터를 포함하는 경우 조직의 정책 확인
4. **이용 약관**: Google 이용 약관 및 Acceptable Use Policy 준수

참고 정보
========

- `Google AI for Developers <https://ai.google.dev/>`__
- `Google AI Studio <https://aistudio.google.com/>`__
- `Gemini API Documentation <https://ai.google.dev/docs>`__
- `Google AI Pricing <https://ai.google.dev/pricing>`__
- :doc:`llm-overview` - LLM 통합 개요
- :doc:`rag-chat` - AI 검색 모드 기능 상세
