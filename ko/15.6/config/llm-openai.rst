==========================
OpenAI 설정
==========================

개요
====

OpenAI는 GPT-4를 비롯한 고성능 대규모 언어 모델(LLM)을 제공하는 클라우드 서비스입니다.
|Fess|에서는 OpenAI API를 사용하여 AI 검색 모드 기능을 구현할 수 있습니다.

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

- ``gpt-5`` - 최신 고성능 모델
- ``gpt-5-mini`` - GPT-5의 경량 버전(비용 효율적)
- ``gpt-4o`` - 고성능 멀티모달 모델
- ``gpt-4o-mini`` - GPT-4o의 경량 버전
- ``o3-mini`` - 추론 특화 경량 모델
- ``o4-mini`` - 차세대 추론 특화 경량 모델

.. note::
   이용 가능한 모델의 최신 정보는 `OpenAI Models <https://platform.openai.com/docs/models>`__에서 확인할 수 있습니다.

.. note::
   o1/o3/o4계열 또는 gpt-5계열 모델을 사용하는 경우, |Fess|는 OpenAI API의 ``max_completion_tokens`` 파라미터를 자동으로 사용합니다. 설정 변경은 필요 없습니다.

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

플러그인 설치
========================

|Fess| 15.6에서는 OpenAI 연계 기능이 플러그인으로 제공됩니다. 사용하려면 ``fess-llm-openai`` 플러그인 설치가 필요합니다.

1. `fess-llm-openai-15.6.0.jar` 를 다운로드합니다
2. |Fess| 설치 디렉터리에 있는 ``app/WEB-INF/plugin/`` 디렉터리에 JAR 파일을 배치합니다::

    cp fess-llm-openai-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

3. |Fess| 를 재시작합니다

.. note::
   플러그인 버전은 |Fess| 본체 버전과 맞춰주세요.

기본 설정
========

|Fess| 15.6에서는 설정 항목이 용도에 따라 다음 두 파일로 나뉩니다.

- ``app/WEB-INF/conf/fess_config.properties`` - |Fess| 본체 설정 및 LLM 프로바이더 고유 설정
- ``system.properties`` - 관리 화면(관리 화면 > 시스템 > 전반) 또는 파일에서 설정하는 LLM 프로바이더 선택

최소 구성
--------

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI 검색 모드 기능 활성화
    rag.chat.enabled=true

    # OpenAI API 키
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # 사용할 모델
    rag.llm.openai.model=gpt-5-mini

``system.properties``(관리 화면 > 시스템 > 전반 에서도 설정 가능):

::

    # LLM 프로바이더를 OpenAI로 설정
    rag.llm.name=openai

권장 구성(프로덕션 환경)
--------------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI 검색 모드 기능 활성화
    rag.chat.enabled=true

    # OpenAI API 키
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # 모델 설정(고성능 모델 사용)
    rag.llm.openai.model=gpt-4o

    # API 엔드포인트(일반적으로 변경 불필요)
    rag.llm.openai.api.url=https://api.openai.com/v1

    # 타임아웃 설정
    rag.llm.openai.timeout=120000

    # 동시 요청 수 제한
    rag.llm.openai.max.concurrent.requests=5

``system.properties``(관리 화면 > 시스템 > 전반 에서도 설정 가능):

::

    # LLM 프로바이더 설정
    rag.llm.name=openai

설정 항목
========

OpenAI 클라이언트에서 사용 가능한 모든 설정 항목입니다. ``rag.llm.name`` 만 ``system.properties`` 또는 관리 화면에서 설정하고, 그 외의 항목은 ``fess_config.properties`` 에서 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 35 35 15 15

   * - 프로퍼티
     - 설명
     - 기본값
     - 설정 위치
   * - ``rag.llm.name``
     - LLM 프로바이더 이름(``openai`` 지정)
     - ``ollama``
     - system.properties
   * - ``rag.llm.openai.api.key``
     - OpenAI API 키
     - (필수)
     - fess_config.properties
   * - ``rag.llm.openai.model``
     - 사용할 모델명
     - ``gpt-5-mini``
     - fess_config.properties
   * - ``rag.llm.openai.api.url``
     - API의 기본 URL
     - ``https://api.openai.com/v1``
     - fess_config.properties
   * - ``rag.llm.openai.timeout``
     - 요청 타임아웃 시간(밀리초)
     - ``120000``
     - fess_config.properties
   * - ``rag.llm.openai.availability.check.interval``
     - 가용성 체크 간격(초)
     - ``60``
     - fess_config.properties
   * - ``rag.llm.openai.max.concurrent.requests``
     - 최대 동시 요청 수
     - ``5``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.max.relevant.docs``
     - 평가 시 최대 관련 문서 수
     - ``3``
     - fess_config.properties
   * - ``rag.llm.openai.concurrency.wait.timeout``
     - 동시 요청 대기 타임아웃(ms)
     - ``30000``
     - fess_config.properties
   * - ``rag.llm.openai.reasoning.token.multiplier``
     - 추론 모델용 max_tokens 배율
     - ``4``
     - fess_config.properties
   * - ``rag.llm.openai.history.max.chars``
     - 대화 이력의 최대 문자 수
     - ``8000``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.messages``
     - 의도 판정 시 최대 이력 메시지 수
     - ``8``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.chars``
     - 의도 판정 시 최대 이력 문자 수
     - ``4000``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.max.chars``
     - 어시스턴트 메시지의 최대 문자 수
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.summary.max.chars``
     - 어시스턴트 요약의 최대 문자 수
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.description.max.chars``
     - 평가 시 문서 설명의 최대 문자 수
     - ``500``
     - fess_config.properties
   * - ``rag.chat.enabled``
     - AI 검색 모드 기능 활성화
     - ``false``
     - fess_config.properties

프롬프트 타입별 설정
======================

|Fess|에서는 프롬프트 종류별로 개별 파라미터를 설정할 수 있습니다. 설정은 ``fess_config.properties`` 에서 수행합니다.

설정 패턴
------------

프롬프트 타입별 설정은 다음 패턴으로 지정합니다:

- ``rag.llm.openai.{promptType}.temperature`` - 생성의 무작위성(0.0~2.0). 추론 모델(o1/o3/o4/gpt-5계열)에서는 무시됩니다
- ``rag.llm.openai.{promptType}.max.tokens`` - 최대 토큰 수
- ``rag.llm.openai.{promptType}.context.max.chars`` - 컨텍스트의 최대 문자 수(기본값: answer/summary는 ``16000``, 기타는 ``10000``)

프롬프트 타입
----------------

이용 가능한 프롬프트 타입:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 프롬프트 타입
     - 설명
   * - ``intent``
     - 사용자의 의도를 판정하는 프롬프트
   * - ``evaluation``
     - 검색 결과의 관련성을 평가하는 프롬프트
   * - ``unclear``
     - 불명확한 쿼리에 대한 응답 프롬프트
   * - ``noresults``
     - 검색 결과가 없을 경우의 응답 프롬프트
   * - ``docnotfound``
     - 문서를 찾을 수 없을 경우의 응답 프롬프트
   * - ``answer``
     - 응답을 생성하는 프롬프트
   * - ``summary``
     - 요약을 생성하는 프롬프트
   * - ``faq``
     - FAQ를 생성하는 프롬프트
   * - ``direct``
     - 직접 응답하는 프롬프트
   * - ``queryregeneration``
     - 검색 쿼리를 재생성하는 프롬프트

기본값
------

각 프롬프트 타입의 기본값입니다. 추론 모델(o1/o3/o4/gpt-5계열)에서는 temperature 설정이 무시됩니다.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - 프롬프트 타입
     - Temperature
     - Max Tokens
     - 비고
   * - ``intent``
     - 0.1
     - 256
     - 결정적 의도 판정
   * - ``evaluation``
     - 0.1
     - 256
     - 결정적 관련성 평가
   * - ``unclear``
     - 0.7
     - 512
     -
   * - ``noresults``
     - 0.7
     - 512
     -
   * - ``docnotfound``
     - 0.7
     - 256
     -
   * - ``direct``
     - 0.7
     - 1024
     -
   * - ``faq``
     - 0.7
     - 1024
     -
   * - ``answer``
     - 0.5
     - 2048
     - 메인 응답 생성
   * - ``summary``
     - 0.3
     - 2048
     - 요약 생성
   * - ``queryregeneration``
     - 0.3
     - 256
     - 쿼리 재생성

설정 예
------

::

    # answer 프롬프트의 temperature 설정
    rag.llm.openai.answer.temperature=0.7

    # answer 프롬프트의 최대 토큰 수
    rag.llm.openai.answer.max.tokens=2048

    # summary 프롬프트의 temperature 설정(요약은 낮게 설정)
    rag.llm.openai.summary.temperature=0.3

    # intent 프롬프트의 temperature 설정(의도 판정은 낮게 설정)
    rag.llm.openai.intent.temperature=0.1

추론 모델 지원
==============

o1/o3/o4계열 또는 gpt-5계열 추론 모델을 사용하는 경우, |Fess|는 자동으로 OpenAI API의 ``max_completion_tokens`` 파라미터를 ``max_tokens`` 대신 사용합니다. 추가 설정 변경은 필요 없습니다.

.. note::
   추론 모델(o1/o3/o4/gpt-5계열)에서는 ``temperature`` 설정이 무시되고 고정값(1)이 사용됩니다. 또한 추론 모델 사용 시 기본 ``max_tokens``가 ``reasoning.token.multiplier``(기본값: 4)배로 증가합니다.

추론 모델용 추가 파라미터
----------------------------

추론 모델을 사용하는 경우 다음 추가 파라미터를 ``fess_config.properties`` 에서 설정할 수 있습니다:

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.llm.openai.{promptType}.reasoning.effort``
     - o계열 모델의 추론 effort 설정(``low``, ``medium``, ``high``)
     - ``low``(intent/evaluation/docnotfound/unclear/noresults/queryregeneration), 미설정(기타)
   * - ``rag.llm.openai.{promptType}.top.p``
     - 토큰 선택의 확률 임계값(0.0~1.0)
     - (미설정)
   * - ``rag.llm.openai.{promptType}.frequency.penalty``
     - 빈도 페널티(-2.0~2.0)
     - (미설정)
   * - ``rag.llm.openai.{promptType}.presence.penalty``
     - 존재 페널티(-2.0~2.0)
     - (미설정)

``{promptType}``에는 ``intent``, ``evaluation``, ``answer``, ``summary`` 등의 프롬프트 타입이 들어갑니다.

설정 예
------

::

    # o3-mini로 추론 effort를 high로 설정
    rag.llm.openai.model=o3-mini
    rag.llm.openai.reasoning.effort=high

    # gpt-5로 top_p와 페널티 설정
    rag.llm.openai.model=gpt-5
    rag.llm.openai.top.p=0.9
    rag.llm.openai.frequency.penalty=0.5

JVM 옵션 설정
=============

보안상의 이유로 API 키는 체크인된 파일이 아니라 런타임 환경(JVM 옵션)을 통해
설정하는 것을 권장합니다.

|Fess| 는 ``RAG_CHAT_ENABLED`` 와 같은 단순 셸 환경 변수를 자동 매핑하지 **않습니다**.
모든 RAG / LLM 설정은 ``FESS_JAVA_OPTS`` 내에서 ``-Dfess.config.*`` (FessConfig 계열)
또는 ``-Dfess.system.*`` (SystemProperty 계열) JVM 옵션으로 전달해야 합니다.

Docker 환경
-----------

공식 `docker-fess <https://github.com/codelibs/docker-fess>`__ 리포지토리에는
OpenAI용 오버레이 ``compose-openai.yaml`` 이 포함되어 있습니다. 최소 절차:

::

    export OPENAI_API_KEY="sk-..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

``compose-openai.yaml`` 의 내용 (동등 구성을 직접 작성할 때의 참고):

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.6.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

요점:

- ``FESS_PLUGINS=fess-llm-openai:15.6.0`` 으로 컨테이너의 ``run.sh`` 가 플러그인 JAR을 자동 다운로드하여 ``app/WEB-INF/plugin/`` 에 배치합니다
- ``-Dfess.config.rag.chat.enabled=true`` 로 AI 검색 모드를 활성화
- ``-Dfess.config.rag.llm.openai.api.key=...`` 로 API 키, ``-Dfess.config.rag.llm.openai.model=...`` 로 모델 지정
- ``-Dfess.system.rag.llm.name=openai`` 는 OpenSearch에 값이 아직 기록되지 않은 첫 시작 시에만 기본값으로 적용됩니다. 시작 후에는 관리 화면 "시스템 > 전체 설정" 의 RAG 섹션에서도 변경할 수 있습니다

프록시 경유로 인터넷에 접속하는 경우 ``FESS_JAVA_OPTS`` 에
``-Dhttps.proxyHost=... -Dhttps.proxyPort=...`` 를 추가하세요.

systemd 환경
------------

``/etc/sysconfig/fess`` (또는 ``/etc/default/fess`` )의 ``FESS_JAVA_OPTS`` 에 추가합니다:

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=sk-... -Dfess.system.rag.llm.name=openai"

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
   * - ``gpt-5-mini``
     - 중간
     - 높음
     - 균형 잡힌 용도(권장)
   * - ``gpt-4o-mini``
     - 낮음~중간
     - 높음
     - 비용 중시 용도
   * - ``gpt-5``
     - 높음
     - 최고
     - 복잡한 추론, 고품질이 필요한 경우
   * - ``gpt-4o``
     - 중간~높음
     - 최고
     - 멀티모달 지원이 필요한 경우
   * - ``o3-mini`` / ``o4-mini``
     - 중간
     - 최고
     - 수학, 코딩 등의 추론 태스크

비용 기준
------------

OpenAI API는 사용량에 따라 요금이 부과됩니다.

.. note::
   최신 가격은 `OpenAI Pricing <https://openai.com/pricing>`__에서 확인하세요.

동시 요청 제어
==================

|Fess|에서는 OpenAI API로의 동시 요청 수를 ``fess_config.properties`` 의 ``rag.llm.openai.max.concurrent.requests`` 로 제어할 수 있습니다. 기본값은 ``5`` 입니다.

::

    # 최대 동시 요청 수 설정
    rag.llm.openai.max.concurrent.requests=5

이 설정을 통해 OpenAI API로의 과도한 요청을 방지하고 레이트 제한 오류를 회피할 수 있습니다.

OpenAI의 Tier별 제한
------------------

OpenAI 계정의 Tier에 따라 API 측 제한이 다릅니다:

- **Free**: 3 RPM(요청/분)
- **Tier 1**: 500 RPM
- **Tier 2**: 5,000 RPM
- **Tier 3+**: 더 높은 제한

OpenAI 계정의 Tier에 따라 ``rag.llm.openai.max.concurrent.requests`` 를 적절히 조정하세요.

문제 해결
======================

인증 오류
----------

**증상**: "401 Unauthorized" 오류 발생

**확인 사항**:

1. API 키가 올바르게 설정되었는지 확인
2. API 키가 유효한지 확인(OpenAI 대시보드에서 확인)
3. API 키에 필요한 권한이 있는지 확인

레이트 제한 오류
----------------

**증상**: "429 Too Many Requests" 오류 발생

**해결 방법**:

1. ``rag.llm.openai.max.concurrent.requests`` 의 값을 줄이기::

    rag.llm.openai.max.concurrent.requests=3

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

    rag.llm.openai.timeout=180000

2. 더 빠른 모델(gpt-5-mini 등) 검토

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
- :doc:`rag-chat` - AI 검색 모드 기능 상세
