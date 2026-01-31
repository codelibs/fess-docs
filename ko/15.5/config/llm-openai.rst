==========================
OpenAI 설정
==========================

개요
====

OpenAI는 GPT-4를 비롯한 고성능 대규모 언어 모델(LLM)을 제공하는 클라우드 서비스입니다.
|Fess|에서는 OpenAI API를 사용하여 AI 모드 기능을 구현할 수 있습니다.

OpenAI를 사용하면 최첨단 AI 모델을 통한 고품질 응답 생성이 가능합니다.

주요 특징
--------

- **고품질 응답**: 최첨단 GPT 모델을 통한 고정밀 응답 생성
- **확장성**: 클라우드 서비스이므로 쉽게 확장 가능
- **지속적인 개선**: 모델의 정기적인 업데이트로 성능 향상
- **풍부한 기능**: 텍스트 생성, 요약, 번역 등 다양한 작업 지원

지원 모델
----------

OpenAI에서 이용 가능한 주요 모델:

- ``gpt-4o`` - 최신 고성능 모델
- ``gpt-4o-mini`` - GPT-4o의 경량 버전(비용 효율적)
- ``gpt-4-turbo`` - GPT-4의 고속 버전
- ``gpt-3.5-turbo`` - 비용 대비 성능이 우수한 모델

.. note::
   이용 가능한 모델의 최신 정보는 `OpenAI Models <https://platform.openai.com/docs/models>`__에서 확인할 수 있습니다.

전제조건
========

OpenAI를 사용하기 전에 다음을 준비하세요.

1. **OpenAI 계정**: `https://platform.openai.com/ <https://platform.openai.com/>`__에서 계정 생성
2. **API 키**: OpenAI 대시보드에서 API 키 생성
3. **결제 설정**: API 사용에는 요금이 발생하므로 결제 정보 설정

API 키 발급
-------------

1. `OpenAI Platform <https://platform.openai.com/>`__에 로그인
2. "API keys" 섹션으로 이동
3. "Create new secret key" 클릭
4. 키 이름을 입력하고 생성
5. 표시된 키를 안전하게 저장(한 번만 표시됨)

.. warning::
   API 키는 기밀 정보입니다. 다음 사항에 주의하세요:

   - 버전 관리 시스템에 커밋하지 않기
   - 로그에 출력하지 않기
   - 환경 변수나 안전한 설정 파일에서 관리

기본 설정
========

``app/WEB-INF/conf/system.properties``에 다음 설정을 추가합니다.

최소 구성
--------

::

    # AI 모드 기능 활성화
    rag.chat.enabled=true

    # LLM 프로바이더를 OpenAI로 설정
    rag.llm.type=openai

    # OpenAI API 키
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # 사용할 모델
    rag.llm.openai.model=gpt-4o-mini

권장 구성(프로덕션 환경)
--------------------

::

    # AI 모드 기능 활성화
    rag.chat.enabled=true

    # LLM 프로바이더 설정
    rag.llm.type=openai

    # OpenAI API 키
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # 모델 설정(고성능 모델 사용)
    rag.llm.openai.model=gpt-4o

    # API 엔드포인트(일반적으로 변경 불필요)
    rag.llm.openai.api.url=https://api.openai.com/v1

    # 타임아웃 설정
    rag.llm.openai.timeout=60000

설정 항목
========

OpenAI 클라이언트에서 사용 가능한 모든 설정 항목입니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.llm.openai.api.key``
     - OpenAI API 키
     - (필수)
   * - ``rag.llm.openai.model``
     - 사용할 모델명
     - ``gpt-5-mini``
   * - ``rag.llm.openai.api.url``
     - API의 기본 URL
     - ``https://api.openai.com/v1``
   * - ``rag.llm.openai.timeout``
     - 요청 타임아웃 시간(밀리초)
     - ``60000``

환경 변수 설정
================

보안상의 이유로 API 키를 환경 변수로 설정하는 것을 권장합니다.

Docker 환경
----------

::

    docker run -e RAG_LLM_OPENAI_API_KEY=sk-xxx... codelibs/fess:15.5.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=openai
          - RAG_LLM_OPENAI_API_KEY=${OPENAI_API_KEY}
          - RAG_LLM_OPENAI_MODEL=gpt-4o-mini

systemd 환경
-----------

``/etc/systemd/system/fess.service.d/override.conf``:

::

    [Service]
    Environment="RAG_LLM_OPENAI_API_KEY=sk-xxx..."

Azure OpenAI 사용
==================

Microsoft Azure를 통해 OpenAI 모델을 사용하는 경우 API 엔드포인트를 변경합니다.

::

    # Azure OpenAI 엔드포인트
    rag.llm.openai.api.url=https://your-resource.openai.azure.com/openai/deployments/your-deployment

    # Azure API 키
    rag.llm.openai.api.key=your-azure-api-key

    # 배포 이름(모델명으로 지정)
    rag.llm.openai.model=your-deployment-name

.. note::
   Azure OpenAI를 사용하는 경우 API 요청 형식이 약간 다를 수 있습니다.
   자세한 내용은 Azure OpenAI 문서를 참조하세요.

모델 선택 가이드
==================

사용 목적에 맞는 모델 선택 지침입니다.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - 모델
     - 비용
     - 품질
     - 용도
   * - ``gpt-3.5-turbo``
     - 낮음
     - 양호
     - 일반적인 질문 응답, 비용 중시
   * - ``gpt-4o-mini``
     - 중간
     - 높음
     - 균형 잡힌 용도(권장)
   * - ``gpt-4o``
     - 높음
     - 최고
     - 복잡한 추론, 고품질이 필요한 경우
   * - ``gpt-4-turbo``
     - 높음
     - 최고
     - 빠른 응답이 필요한 경우

비용 기준
------------

OpenAI API는 사용량에 따라 요금이 부과됩니다. 다음은 2024년 기준 참고 가격입니다.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 모델
     - 입력(1K 토큰)
     - 출력(1K 토큰)
   * - gpt-3.5-turbo
     - $0.0005
     - $0.0015
   * - gpt-4o-mini
     - $0.00015
     - $0.0006
   * - gpt-4o
     - $0.005
     - $0.015

.. note::
   최신 가격은 `OpenAI Pricing <https://openai.com/pricing>`__에서 확인하세요.

속도 제한
==========

OpenAI API에는 속도 제한이 있습니다. |Fess|의 속도 제한 기능과 함께 적절히 설정하세요.

::

    # Fess의 속도 제한 설정
    rag.chat.rate.limit.enabled=true
    rag.chat.rate.limit.requests.per.minute=10

OpenAI의 Tier별 제한
------------------

OpenAI 계정의 Tier에 따라 제한이 다릅니다:

- **Free**: 3 RPM(요청/분)
- **Tier 1**: 500 RPM
- **Tier 2**: 5,000 RPM
- **Tier 3+**: 더 높은 제한

문제 해결
======================

인증 오류
----------

**증상**: "401 Unauthorized" 오류 발생

**확인 사항**:

1. API 키가 올바르게 설정되었는지 확인
2. API 키가 유효한지 확인(OpenAI 대시보드에서 확인)
3. API 키에 필요한 권한이 있는지 확인

속도 제한 오류
----------------

**증상**: "429 Too Many Requests" 오류 발생

**해결 방법**:

1. |Fess|의 속도 제한을 더 엄격하게 설정::

    rag.chat.rate.limit.requests.per.minute=5

2. OpenAI 계정의 Tier 업그레이드

쿼터 초과
------------

**증상**: "You exceeded your current quota" 오류

**해결 방법**:

1. OpenAI 대시보드에서 사용량 확인
2. 결제 설정을 확인하고 필요 시 한도 상향

타임아웃
------------

**증상**: 요청이 타임아웃됨

**해결 방법**:

1. 타임아웃 시간 연장::

    rag.llm.openai.timeout=120000

2. 더 빠른 모델(gpt-3.5-turbo 등) 검토

디버그 설정
------------

문제를 조사할 때는 |Fess|의 로그 레벨을 조정하여 OpenAI 관련 상세 로그를 출력할 수 있습니다.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.openai" level="DEBUG"/>

보안 관련 주의사항
========================

OpenAI API를 사용할 때는 다음 보안 사항에 주의하세요.

1. **데이터 프라이버시**: 검색 결과의 내용이 OpenAI 서버로 전송됩니다
2. **API 키 관리**: 키 유출은 부정 사용으로 이어집니다
3. **규정 준수**: 기밀 데이터를 포함하는 경우 조직의 정책 확인
4. **이용 약관**: OpenAI 이용 약관 준수

참고 정보
========

- `OpenAI Platform <https://platform.openai.com/>`__
- `OpenAI API Reference <https://platform.openai.com/docs/api-reference>`__
- `OpenAI Pricing <https://openai.com/pricing>`__
- :doc:`llm-overview` - LLM 통합 개요
- :doc:`rag-chat` - AI 모드 기능 상세
