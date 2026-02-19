==========================
Google Gemini 설정
==========================

개요
====

Google Gemini는 Google사가 제공하는 최첨단 대규모 언어 모델(LLM)입니다.
|Fess|에서는 Google AI API(Generative Language API)를 사용하여 Gemini 모델을 통한 AI 모드 기능을 구현할 수 있습니다.

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

- ``gemini-2.5-flash`` - 빠르고 효율적인 모델(권장)
- ``gemini-2.5-pro`` - 더 높은 추론 능력을 가진 모델
- ``gemini-1.5-flash`` - 안정 버전의 Flash 모델
- ``gemini-1.5-pro`` - 안정 버전의 Pro 모델

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

기본 설정
========

``app/WEB-INF/conf/fess_config.properties``에 다음 설정을 추가합니다.

최소 구성
--------

::

    # AI 모드 기능 활성화
    rag.chat.enabled=true

    # LLM 프로바이더를 Gemini로 설정
    rag.llm.type=gemini

    # Gemini API 키
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # 사용할 모델
    rag.llm.gemini.model=gemini-2.5-flash

권장 구성(프로덕션 환경)
--------------------

::

    # AI 모드 기능 활성화
    rag.chat.enabled=true

    # LLM 프로바이더 설정
    rag.llm.type=gemini

    # Gemini API 키
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # 모델 설정(고속 모델 사용)
    rag.llm.gemini.model=gemini-2.5-flash

    # API 엔드포인트(일반적으로 변경 불필요)
    rag.llm.gemini.api.url=https://generativelanguage.googleapis.com/v1beta

    # 타임아웃 설정
    rag.llm.gemini.timeout=60000

설정 항목
========

Gemini 클라이언트에서 사용 가능한 모든 설정 항목입니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.llm.gemini.api.key``
     - Google AI API 키
     - (필수)
   * - ``rag.llm.gemini.model``
     - 사용할 모델명
     - ``gemini-2.5-flash``
   * - ``rag.llm.gemini.api.url``
     - API의 기본 URL
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - 요청 타임아웃 시간(밀리초)
     - ``60000``

환경 변수 설정
================

보안상의 이유로 API 키를 환경 변수로 설정하는 것을 권장합니다.

Docker 환경
----------

::

    docker run -e RAG_LLM_GEMINI_API_KEY=AIzaSy... codelibs/fess:15.5.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=gemini
          - RAG_LLM_GEMINI_API_KEY=${GEMINI_API_KEY}
          - RAG_LLM_GEMINI_MODEL=gemini-2.5-flash

systemd 환경
-----------

``/etc/systemd/system/fess.service.d/override.conf``:

::

    [Service]
    Environment="RAG_LLM_GEMINI_API_KEY=AIzaSy..."

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
   * - ``gemini-2.5-flash``
     - 고속
     - 높음
     - 일반적인 용도, 균형 중시(권장)
   * - ``gemini-2.5-pro``
     - 중속
     - 최고
     - 복잡한 추론, 고품질이 필요한 경우
   * - ``gemini-1.5-flash``
     - 고속
     - 양호
     - 비용 중시, 안정성 중시
   * - ``gemini-1.5-pro``
     - 중속
     - 높음
     - 긴 컨텍스트가 필요한 경우

컨텍스트 윈도우
----------------------

Gemini 모델은 매우 긴 컨텍스트 윈도우를 지원합니다:

- **Gemini 1.5/2.5 Flash**: 최대 100만 토큰
- **Gemini 1.5/2.5 Pro**: 최대 200만 토큰

이 특징을 활용하여 더 많은 검색 결과를 컨텍스트에 포함할 수 있습니다.

::

    # 더 많은 문서를 컨텍스트에 포함
    rag.chat.context.max.documents=10
    rag.chat.context.max.chars=20000

비용 기준
------------

Google AI API는 사용량에 따라 요금이 부과됩니다(무료 할당량 있음).

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 모델
     - 입력(100만 문자)
     - 출력(100만 문자)
   * - Gemini 1.5 Flash
     - $0.075
     - $0.30
   * - Gemini 1.5 Pro
     - $1.25
     - $5.00
   * - Gemini 2.5 Flash
     - 가격 변동 가능
     - 가격 변동 가능

.. note::
   최신 가격 및 무료 할당량 정보는 `Google AI Pricing <https://ai.google.dev/pricing>`__에서 확인하세요.

속도 제한
==========

Google AI API에는 속도 제한이 있습니다. |Fess|의 속도 제한 기능과 함께 적절히 설정하세요.

::

    # Fess의 속도 제한 설정
    rag.chat.rate.limit.enabled=true
    rag.chat.rate.limit.requests.per.minute=10

무료 할당량 제한
------------

Google AI API에는 무료 할당량이 있지만 다음 제한이 있습니다:

- 요청/분: 15 RPM
- 토큰/분: 100만 TPM
- 요청/일: 1,500 RPD

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

속도 제한 오류
----------------

**증상**: "429 Resource has been exhausted" 오류 발생

**해결 방법**:

1. |Fess|의 속도 제한을 더 엄격하게 설정::

    rag.chat.rate.limit.requests.per.minute=5

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
- :doc:`rag-chat` - AI 모드 기능 상세
