==========================
Ollama 설정
==========================

개요
====

Ollama는 로컬 환경에서 대규모 언어 모델(LLM)을 실행하기 위한 오픈소스 플랫폼입니다.
|Fess| 의 Ollama 연계 기능은 플러그인 ``fess-llm-ollama`` 로 제공되며, 프라이빗 환경에서의 사용에 적합합니다.

Ollama를 사용하면 데이터를 외부로 전송하지 않고 AI 검색 모드 기능을 이용할 수 있습니다.

주요 특징
---------

- **로컬 실행**: 데이터가 외부로 전송되지 않아 프라이버시 확보
- **다양한 모델**: Llama, Mistral, Gemma, CodeLlama 등 다수의 모델 지원
- **비용 효율**: API 비용 없음(하드웨어 비용만 발생)
- **커스터마이즈**: 직접 파인튜닝한 모델도 사용 가능

지원 모델
----------

Ollama에서 이용 가능한 주요 모델:

- ``llama3.3:70b`` - Meta사의 Llama 3.3(70B 파라미터)
- ``gemma4:e4b`` - Google사의 Gemma 4(E4B 파라미터, 기본값)
- ``mistral:7b`` - Mistral AI사의 Mistral(7B 파라미터)
- ``codellama:13b`` - Meta사의 Code Llama(13B 파라미터)
- ``phi3:3.8b`` - Microsoft사의 Phi-3(3.8B 파라미터)

.. note::
   이용 가능한 모델의 최신 목록은 `Ollama Library <https://ollama.com/library>`__ 에서 확인할 수 있습니다.

전제조건
========

Ollama를 사용하기 전에 다음을 확인하세요.

1. **Ollama 설치**: `https://ollama.com/ <https://ollama.com/>`__ 에서 다운로드하여 설치
2. **모델 다운로드**: 사용할 모델을 Ollama에 다운로드
3. **Ollama 서버 시작**: Ollama가 실행 중인지 확인

Ollama 설치
--------------------

Linux/macOS
~~~~~~~~~~~

::

    curl -fsSL https://ollama.com/install.sh | sh

Windows
~~~~~~~

공식 사이트에서 설치 프로그램을 다운로드하여 실행합니다.

Docker
~~~~~~

::

    docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

모델 다운로드
--------------------

::

    # 기본 모델(Gemma 4 E4B) 다운로드
    ollama pull gemma4:e4b

    # Llama 3.3 다운로드
    ollama pull llama3.3:70b

    # 모델 동작 확인
    ollama run gemma4:e4b "Hello, how are you?"

플러그인 설치
========================

Ollama 연계 기능은 플러그인으로 제공됩니다.
Ollama를 이용하려면 ``fess-llm-ollama`` 플러그인 설치가 필요합니다.

1. `fess-llm-ollama-15.8.0.jar` 를 다운로드합니다.
2. |Fess| 설치 디렉터리 내의 ``app/WEB-INF/plugin/`` 디렉터리에 배치합니다.

::

    cp fess-llm-ollama-15.8.0.jar /path/to/fess/app/WEB-INF/plugin/

3. |Fess| 를 재시작합니다.

.. note::
   플러그인 버전은 |Fess| 버전과 맞춰주세요.

기본 설정
=========

LLM 관련 설정은 여러 설정 파일로 나뉩니다.

최소 구성
---------

``system.properties`` (관리 화면 > 시스템 > 전반 에서도 설정 가능):

::

    # LLM 프로바이더를 Ollama로 설정
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI 검색 모드 기능 활성화
    rag.chat.enabled=true

    # Ollama URL(로컬 환경인 경우)
    rag.llm.ollama.api.url=http://localhost:11434

    # 사용할 모델
    rag.llm.ollama.model=gemma4:e4b

.. note::
   LLM 프로바이더 설정은 관리 화면(관리 화면 > 시스템 > 전반)에서 ``rag.llm.name`` 을 설정할 수도 있습니다.

권장 구성(프로덕션 환경)
------------------------

``system.properties`` (관리 화면 > 시스템 > 전반 에서도 설정 가능):

::

    # LLM 프로바이더 설정
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI 검색 모드 기능 활성화
    rag.chat.enabled=true

    # Ollama URL
    rag.llm.ollama.api.url=http://localhost:11434

    # 모델 설정(대규모 모델 사용)
    rag.llm.ollama.model=llama3.3:70b

    # 타임아웃 설정(대규모 모델용으로 증가)
    rag.llm.ollama.timeout=120000

    # 동시 요청 수 제어
    rag.llm.ollama.max.concurrent.requests=5

설정 항목
=========

Ollama 클라이언트에서 사용 가능한 모든 설정 항목입니다. ``rag.llm.name`` 을 제외한 모든 항목은 ``fess_config.properties`` 에 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.llm.ollama.api.url``
     - Ollama 서버의 기본 URL
     - ``http://localhost:11434``
   * - ``rag.llm.ollama.model``
     - 사용할 모델명(Ollama에 다운로드된 모델)
     - ``gemma4:e4b``
   * - ``rag.llm.ollama.timeout``
     - 요청 타임아웃 시간(밀리초)
     - ``60000``
   * - ``rag.llm.ollama.availability.check.interval``
     - 가용성 체크 간격(초). ``0`` 이하를 지정하면 정기적인 가용성 체크를 비활성화합니다
     - ``60``
   * - ``rag.llm.ollama.max.concurrent.requests``
     - 최대 동시 요청 수
     - ``5``
   * - ``rag.llm.ollama.chat.evaluation.max.relevant.docs``
     - 평가 최대 관련 문서 수
     - ``3``
   * - ``rag.llm.ollama.concurrency.wait.timeout``
     - 동시 실행 제어의 퍼밋 취득 대기 타임아웃(밀리초)
     - ``30000``
   * - ``rag.llm.ollama.connect.timeout``
     - TCP 연결 타임아웃(밀리초). ``rag.llm.ollama.timeout`` 과는 별도로 지정 가능
     - ``5000``
   * - ``rag.llm.ollama.retry.max``
     - HTTP 재시도의 최대 시도 횟수( ``429`` 및 ``5xx`` 계열 오류 시)
     - ``3``
   * - ``rag.llm.ollama.retry.base.delay.ms``
     - 지수 백오프의 기준 지연 시간(밀리초)
     - ``2000``

상세 설정
---------

히스토리 및 컨텍스트 크기에 관한 상세 설정 항목입니다.

.. list-table::
   :header-rows: 1
   :widths: 45 35 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.llm.ollama.chat.evaluation.description.max.chars``
     - 평가 시 설명의 최대 문자 수
     - ``500``
   * - ``rag.llm.ollama.history.max.chars``
     - 대화 히스토리의 최대 문자 수
     - ``4000``
   * - ``rag.llm.ollama.intent.history.max.messages``
     - 의도 판정 시 히스토리 최대 메시지 수
     - ``6``
   * - ``rag.llm.ollama.intent.history.max.chars``
     - 의도 판정 시 히스토리 최대 문자 수
     - ``3000``
   * - ``rag.llm.ollama.history.assistant.max.chars``
     - 어시스턴트 응답의 히스토리 최대 문자 수
     - ``500``
   * - ``rag.llm.ollama.history.assistant.summary.max.chars``
     - 어시스턴트 요약의 히스토리 최대 문자 수
     - ``500``

동시 실행 제어
--------------

``rag.llm.ollama.max.concurrent.requests`` 를 사용하여 Ollama로의 동시 요청 수를 제어할 수 있습니다.
기본값은 5입니다. Ollama 서버의 리소스에 따라 조정하세요.
동시 요청 수가 너무 많으면 Ollama 서버에 부하가 걸려 응답 속도가 저하될 수 있습니다.

프롬프트 타입별 설정
======================

|Fess| 에서는 프롬프트 타입별로 LLM 파라미터를 커스터마이즈할 수 있습니다.
설정은 ``fess_config.properties`` 에 기술합니다.

프롬프트 타입별로 다음 파라미터를 설정할 수 있습니다:

- ``rag.llm.ollama.{promptType}.temperature`` - 생성 시의 temperature
- ``rag.llm.ollama.{promptType}.max.tokens`` - 최대 토큰 수(Ollama API의 ``num_predict`` 에 매핑됩니다)
- ``rag.llm.ollama.{promptType}.context.max.chars`` - 컨텍스트의 최대 문자 수
- ``rag.llm.ollama.{promptType}.thinking.budget`` - 사고 버짓(불리언 형식의 사고 제어. 자세한 내용은 「사고 모델 지원」 참조)
- ``rag.llm.ollama.{promptType}.thinking.level`` - 사고 레벨( ``high`` / ``medium`` / ``low`` 의 문자열 형식. 자세한 내용은 「사고 모델 지원」 참조)
- ``rag.llm.ollama.{promptType}.top.p`` - Top-P 샘플링 값
- ``rag.llm.ollama.{promptType}.top.k`` - Top-K 샘플링 값
- ``rag.llm.ollama.{promptType}.num.ctx`` - 컨텍스트 윈도우 크기

각 파라미터는 다음 순서로 해결됩니다: ``rag.llm.ollama.{promptType}.<param>`` (프롬프트 타입별 설정) → ``rag.llm.ollama.default.<param>`` (전체 프롬프트 타입 공통 폴백) → 프롬프트 타입별 하드코딩된 기본값. 요청에 명시적으로 지정된 값은 항상 우선됩니다.

이용 가능한 프롬프트 타입:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 프롬프트 타입
     - 설명
   * - ``intent``
     - 사용자의 의도를 판정하는 프롬프트
   * - ``evaluation``
     - 검색 결과의 평가 프롬프트
   * - ``unclear``
     - 불명확한 쿼리에 대한 응답 프롬프트
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

각 프롬프트 타입에는 설정이 생략된 경우에 적용되는 하드코딩된 기본값이 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 30

   * - 프롬프트 타입
     - temperature
     - max.tokens
     - thinking.budget
     - context.max.chars
   * - ``intent``
     - ``0.1``
     - ``256``
     - ``0``
     - ``6000``
   * - ``evaluation``
     - ``0.1``
     - ``512``
     - ``0``
     - ``6000``
   * - ``unclear``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``noresults``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``docnotfound``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``answer``
     - ``0.5``
     - ``8192``
     - (설정 안 됨)
     - ``10000``
   * - ``summary``
     - ``0.3``
     - ``8192``
     - (설정 안 됨)
     - ``10000``
   * - ``faq``
     - ``0.7``
     - ``4096``
     - (설정 안 됨)
     - ``6000``
   * - ``direct``
     - ``0.7``
     - ``4096``
     - (설정 안 됨)
     - ``6000``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``
     - ``0``
     - ``6000``

설정 예::

    # 응답 생성 시의 temperature 설정
    rag.llm.ollama.answer.temperature=0.7

    # 요약 생성 시의 최대 토큰 수 설정
    rag.llm.ollama.summary.max.tokens=2048

    # 의도 판정 시의 컨텍스트 최대 문자 수 설정
    rag.llm.ollama.intent.context.max.chars=4000

Ollama 모델 옵션
======================

Ollama의 모델 파라미터를 ``fess_config.properties`` 에서 설정할 수 있습니다.
``rag.llm.ollama.default.<param>`` 형식으로 지정하면 전체 프롬프트 타입 공통의 폴백 값으로 사용됩니다.
``default`` 에 의한 폴백은 ``top.p`` / ``top.k`` / ``num.ctx`` 뿐만 아니라 ``temperature`` / ``max.tokens`` / ``thinking.budget`` / ``thinking.level`` 에도 적용됩니다.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``rag.llm.ollama.default.top.p``
     - Top-P 샘플링 값(0.0~1.0). 프롬프트 타입별로 ``rag.llm.ollama.{promptType}.top.p`` 로 덮어쓸 수 있음
     - (설정 안 됨)
   * - ``rag.llm.ollama.default.top.k``
     - Top-K 샘플링 값. 프롬프트 타입별로 ``rag.llm.ollama.{promptType}.top.k`` 로 덮어쓸 수 있음
     - (설정 안 됨)
   * - ``rag.llm.ollama.default.num.ctx``
     - 컨텍스트 윈도우 크기. 프롬프트 타입별로 ``rag.llm.ollama.{promptType}.num.ctx`` 로 덮어쓸 수 있음
     - (설정 안 됨)
   * - ``rag.llm.ollama.default.temperature``
     - 생성 시의 temperature 폴백 값. 프롬프트 타입별로 ``rag.llm.ollama.{promptType}.temperature`` 로 덮어쓸 수 있음
     - (설정 안 됨)
   * - ``rag.llm.ollama.default.max.tokens``
     - 최대 토큰 수 폴백 값. 프롬프트 타입별로 ``rag.llm.ollama.{promptType}.max.tokens`` 로 덮어쓸 수 있음
     - (설정 안 됨)
   * - ``rag.llm.ollama.default.thinking.budget``
     - 사고 버짓 폴백 값. 프롬프트 타입별로 ``rag.llm.ollama.{promptType}.thinking.budget`` 로 덮어쓸 수 있음
     - (설정 안 됨)
   * - ``rag.llm.ollama.default.thinking.level``
     - 사고 레벨( ``high`` / ``medium`` / ``low`` ) 폴백 값. 프롬프트 타입별로 ``rag.llm.ollama.{promptType}.thinking.level`` 로 덮어쓸 수 있음
     - (설정 안 됨)
   * - ``rag.llm.ollama.options.*``
     - Ollama API에 직접 전달되는 글로벌 옵션. 접미사가 옵션명으로 사용됨(예: ``rag.llm.ollama.options.repeat_penalty=1.1``). 값은 자동으로 Integer, Double, Boolean, String으로 변환됨
     - (설정 안 됨)

설정 예::

    # 기본 Top-P 샘플링(전체 프롬프트 타입 공통)
    rag.llm.ollama.default.top.p=0.9

    # 기본 Top-K 샘플링
    rag.llm.ollama.default.top.k=40

    # 기본 컨텍스트 윈도우 크기
    rag.llm.ollama.default.num.ctx=4096

    # 응답 생성 시에만 Top-P 변경
    rag.llm.ollama.answer.top.p=0.95

    # 글로벌 옵션(Ollama API에 직접 전달됨)
    rag.llm.ollama.options.repeat_penalty=1.1

사고 모델 지원
==============

gemma4나 qwen3 등의 사고 모델(thinking model)을 사용하는 경우, |Fess| 는 사고 버짓(thinking budget) 설정을 지원합니다.

사고 버짓은 프롬프트 타입별로 ``fess_config.properties`` 에서 설정합니다:

::

    # 응답 생성 시의 사고 버짓 설정
    rag.llm.ollama.answer.thinking.budget=1024

    # 요약 생성 시의 사고 버짓 설정
    rag.llm.ollama.summary.thinking.budget=1024

사고 버짓을 설정하면 모델이 응답을 생성하기 전에 "생각하는" 단계에 할당할 토큰 수를 제어할 수 있습니다.

.. note::
   Ollama에서는 사고 버짓이 불리언 플래그로 변환됩니다(값이 0보다 큰 경우 ``think: true``, 0인 경우 ``think: false``). 토큰 수에 의한 세밀한 제어는 Ollama API의 제약으로 인해 이용할 수 없습니다.

사고 레벨(thinking level)
----------------------------

gpt-oss 등 일부 모델은 불리언 형식의 ``think`` 플래그를 무시하고, ``high`` / ``medium`` / ``low`` 의 문자열 형식에 의한 사고 레벨 지정을 필요로 합니다.
이러한 모델에서는 ``rag.llm.ollama.{promptType}.thinking.level`` 을 사용합니다.

::

    # 응답 생성 시의 사고 레벨 설정
    rag.llm.ollama.answer.thinking.level=high

    # 요약 생성 시의 사고 레벨 설정
    rag.llm.ollama.summary.thinking.level=medium

``thinking.level`` 에 설정할 수 있는 값은 ``high`` / ``medium`` / ``low`` 중 하나입니다(대소문자 구분 없음). 잘못된 값을 지정한 경우 무시되고 경고 로그가 출력됩니다.

.. note::
   ``thinking.level`` (문자열 형식)과 ``thinking.budget`` (불리언 형식) 모두 설정된 경우, ``thinking.level`` 이 우선됩니다. GPT-OSS 계열 모델에서는 ``thinking.level`` 을, 그 외의 사고 모델에서는 ``thinking.budget`` 을 사용하세요.

네트워크 구성
================

Docker 구성
--------------

|Fess| 공식 `docker-fess <https://github.com/codelibs/docker-fess>`__ 에는 Ollama용 오버레이 ``compose-ollama.yaml`` 이 포함되어 있습니다. 최소 절차는 다음과 같습니다.

::

    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    docker exec -it ollama01 ollama pull gemma4:e4b

``compose-ollama.yaml`` 은 NVIDIA GPU를 사용하는 구성입니다(NVIDIA Container Toolkit 필요). 내용은 다음과 같습니다.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-ollama:15.8.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.ollama.api.url=http://ollama01:11434"
        depends_on:
          - ollama01

      ollama01:
        image: ollama/ollama:latest
        container_name: ollama01
        ports:
          - "11434:11434"
        volumes:
          - ollama-data:/root/.ollama
        networks:
          - search_net
        restart: unless-stopped
        deploy:
          resources:
            reservations:
              devices:
                - driver: nvidia
                  count: 1
                  capabilities: [gpu]

    volumes:
      ollama-data:
        driver: local

요점:

- ``FESS_PLUGINS=fess-llm-ollama:15.8.0`` 으로 시작 스크립트가 플러그인 JAR을 자동으로 가져와 ``app/WEB-INF/plugin/`` 에 배치합니다(버전은 사용 중인 |Fess| 에 맞게 조정하세요)
- ``-Dfess.config.rag.chat.enabled=true`` 로 AI 검색 모드를 활성화
- ``-Dfess.config.rag.llm.ollama.api.url=...`` 로 Ollama 서버의 URL을 지정(Docker Compose 네트워크 내에서는 ``ollama01`` 등의 서비스 이름으로 해결)
- LLM 프로바이더( ``rag.llm.name`` )의 기본값은 ``ollama`` 이므로, Ollama만 사용하는 경우 명시적인 지정은 불필요합니다. 다른 프로바이더에서 전환하는 경우 등에는 ``FESS_JAVA_OPTS`` 에 ``-Dfess.system.rag.llm.name=ollama`` 를 추가하거나, 시작 후 관리 화면 「시스템 > 전반」의 RAG 섹션에서 설정하세요
- ``deploy.resources.reservations.devices`` 블록은 GPU를 사용하기 위한 설정입니다. GPU를 사용하지 않는 경우(CPU만으로 실행하는 경우)는 이 블록을 삭제하세요

.. note::
   ``RAG_CHAT_ENABLED`` 나 ``RAG_LLM_NAME`` 등의 대문자 스네이크 케이스 환경 변수는 |Fess| 에서 직접 인식되지 않습니다. 설정 값은 반드시 ``FESS_JAVA_OPTS`` 내에서 ``-Dfess.config.<key>`` ( ``fess_config.properties`` 계열) 또는 ``-Dfess.system.<key>`` ( ``system.properties`` 계열)로 전달하세요.

원격 Ollama 서버
----------------------

Ollama를 Fess와 다른 서버에서 실행하는 경우:

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama는 기본적으로 인증 기능이 없으므로 외부에서 접근 가능하게 하는 경우
   네트워크 레벨에서의 보안 대책(방화벽, VPN 등)을 검토하세요.

HTTP 프록시 경유 사용
======================

Ollama 클라이언트는 |Fess| 전체의 HTTP 프록시 설정을 공유합니다. Ollama 서버로의 연결에 프록시를 경유해야 하는 경우(원격 Ollama 서버 이용 시 등), ``fess_config.properties`` 에서 다음 프로퍼티를 지정하세요.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``http.proxy.host``
     - 프록시 호스트 이름(빈 문자열이면 프록시를 사용하지 않음)
     - ``""``
   * - ``http.proxy.port``
     - 프록시 포트 번호
     - ``8080``
   * - ``http.proxy.username``
     - 프록시 인증의 사용자 이름(임의. 지정하면 Basic 인증이 활성화됨)
     - ``""``
   * - ``http.proxy.password``
     - 프록시 인증의 비밀번호
     - ``""``

.. note::
   Ollama는 일반적으로 로컬 또는 내부 네트워크에서 동작하므로, 프록시 설정이 필요한 경우는 제한적인 케이스(사내 프록시를 통해서만 도달할 수 있는 원격 Ollama 서버를 이용하는 경우 등)에 한정됩니다.
   이 설정은 크롤러 등 |Fess| 전체의 HTTP 액세스에도 영향을 미칩니다.

모델 선택 가이드
==================

사용 목적에 맞는 모델 선택 지침입니다.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - 모델
     - 크기
     - 필요 VRAM
     - 용도
   * - ``phi3:3.8b``
     - 소
     - 4GB 이상
     - 경량 환경, 단순한 질문 응답
   * - ``gemma4:e4b``
     - 소~중
     - 8GB 이상
     - 균형 잡힌 범용 용도, 사고 모드 지원(기본값)
   * - ``mistral:7b``
     - 중
     - 8GB 이상
     - 고품질 응답이 필요한 경우
   * - ``llama3.3:70b``
     - 대
     - 48GB 이상
     - 최고 품질의 응답, 복잡한 추론

GPU 지원
--------

Ollama는 GPU 가속을 지원합니다. NVIDIA GPU를 사용하면
추론 속도가 크게 향상됩니다.

::

    # GPU 지원 확인
    ollama run gemma4:e4b --verbose

문제 해결
======================

연결 오류
----------

**증상**: 채팅 기능에서 오류 발생, LLM을 사용할 수 없다고 표시됨

**확인 사항**:

1. Ollama가 실행 중인지 확인::

    curl http://localhost:11434/api/tags

2. 모델이 다운로드되었는지 확인::

    ollama list

3. 방화벽 설정 확인

4. ``fess-llm-ollama`` 플러그인이 ``app/WEB-INF/plugin/`` 에 배치되어 있는지 확인

모델을 찾을 수 없음
--------------------

**증상**: "Configured model not found"라는 로그가 출력됨

**해결 방법**:

1. 모델명이 정확한지 확인(``:latest`` 태그를 포함하는 경우 있음)::

    # 모델 목록 확인
    ollama list

2. 필요한 모델 다운로드::

    ollama pull gemma4:e4b

타임아웃
------------

**증상**: 요청이 타임아웃됨

**해결 방법**:

1. 타임아웃 시간 연장::

    rag.llm.ollama.timeout=120000

2. 더 작은 모델 사용 또는 GPU 환경 검토

디버그 설정
------------

문제를 조사할 때는 |Fess| 의 로그 레벨을 조정하여 Ollama 관련 상세 로그를 출력할 수 있습니다.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.ollama" level="DEBUG"/>

참고 정보
=========

- `Ollama 공식 사이트 <https://ollama.com/>`__
- `Ollama 모델 라이브러리 <https://ollama.com/library>`__
- `Ollama GitHub <https://github.com/ollama/ollama>`__
- :doc:`llm-overview` - LLM 통합 개요
- :doc:`rag-chat` - AI 검색 모드 기능 상세
