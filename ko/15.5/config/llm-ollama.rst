==========================
Ollama 설정
==========================

개요
====

Ollama는 로컬 환경에서 대규모 언어 모델(LLM)을 실행하기 위한 오픈소스 플랫폼입니다.
|Fess|의 기본 LLM 프로바이더로 설정되어 있으며, 프라이빗 환경에서의 사용에 적합합니다.

Ollama를 사용하면 데이터를 외부로 전송하지 않고 AI 채팅 기능을 이용할 수 있습니다.

주요 특징
--------

- **로컬 실행**: 데이터가 외부로 전송되지 않아 프라이버시 확보
- **다양한 모델**: Llama, Mistral, Gemma, CodeLlama 등 다수의 모델 지원
- **비용 효율**: API 비용 없음(하드웨어 비용만 발생)
- **커스터마이즈**: 직접 파인튜닝한 모델도 사용 가능

지원 모델
----------

Ollama에서 이용 가능한 주요 모델:

- ``llama3.3:70b`` - Meta사의 Llama 3.3(70B 파라미터)
- ``gemma3:4b`` - Google사의 Gemma 3(4B 파라미터, 기본값)
- ``mistral:7b`` - Mistral AI사의 Mistral(7B 파라미터)
- ``codellama:13b`` - Meta사의 Code Llama(13B 파라미터)
- ``phi3:3.8b`` - Microsoft사의 Phi-3(3.8B 파라미터)

.. note::
   이용 가능한 모델의 최신 목록은 `Ollama Library <https://ollama.com/library>`__에서 확인할 수 있습니다.

전제조건
========

Ollama를 사용하기 전에 다음을 확인하세요.

1. **Ollama 설치**: `https://ollama.com/ <https://ollama.com/>`__에서 다운로드하여 설치
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

    # 기본 모델(Gemma 3 4B) 다운로드
    ollama pull gemma3:4b

    # Llama 3.3 다운로드
    ollama pull llama3.3:70b

    # 모델 동작 확인
    ollama run gemma3:4b "Hello, how are you?"

기본 설정
========

``app/WEB-INF/conf/fess_config.properties``에 다음 설정을 추가합니다.

최소 구성
--------

::

    # AI 모드 기능 활성화
    rag.chat.enabled=true

    # LLM 프로바이더를 Ollama로 설정
    rag.llm.type=ollama

    # Ollama URL(로컬 환경인 경우)
    rag.llm.ollama.api.url=http://localhost:11434

    # 사용할 모델
    rag.llm.ollama.model=gemma3:4b

권장 구성(프로덕션 환경)
--------------------

::

    # AI 모드 기능 활성화
    rag.chat.enabled=true

    # LLM 프로바이더 설정
    rag.llm.type=ollama

    # Ollama URL
    rag.llm.ollama.api.url=http://localhost:11434

    # 모델 설정(대규모 모델 사용)
    rag.llm.ollama.model=llama3.3:70b

    # 타임아웃 설정(대규모 모델용으로 증가)
    rag.llm.ollama.timeout=120000

설정 항목
========

Ollama 클라이언트에서 사용 가능한 모든 설정 항목입니다.

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
     - ``gemma3:4b``
   * - ``rag.llm.ollama.timeout``
     - 요청 타임아웃 시간(밀리초)
     - ``60000``

네트워크 구성
================

Docker 구성
--------------

|Fess|와 Ollama를 모두 Docker에서 실행하는 경우의 구성 예입니다.

``docker-compose.yml``:

::

    version: '3'
    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=ollama
          - RAG_LLM_OLLAMA_API_URL=http://ollama:11434
          - RAG_LLM_OLLAMA_MODEL=gemma3:4b
        depends_on:
          - ollama
        # ... 기타 설정

      ollama:
        image: ollama/ollama
        volumes:
          - ollama_data:/root/.ollama
        ports:
          - "11434:11434"

    volumes:
      ollama_data:

.. note::
   Docker Compose 환경에서는 호스트명으로 ``ollama``를 사용합니다(``localhost``가 아님).

원격 Ollama 서버
----------------------

Ollama를 Fess와 다른 서버에서 실행하는 경우:

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama는 기본적으로 인증 기능이 없으므로 외부에서 접근 가능하게 하는 경우
   네트워크 레벨에서의 보안 대책(방화벽, VPN 등)을 검토하세요.

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
   * - ``gemma3:4b``
     - 소~중
     - 6GB 이상
     - 균형 잡힌 범용 용도(기본값)
   * - ``mistral:7b``
     - 중
     - 8GB 이상
     - 고품질 응답이 필요한 경우
   * - ``llama3.3:70b``
     - 대
     - 48GB 이상
     - 최고 품질의 응답, 복잡한 추론

GPU 지원
-------

Ollama는 GPU 가속을 지원합니다. NVIDIA GPU를 사용하면
추론 속도가 크게 향상됩니다.

::

    # GPU 지원 확인
    ollama run gemma3:4b --verbose

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

모델을 찾을 수 없음
--------------------

**증상**: "Configured model not found in Ollama"라는 로그 출력

**해결 방법**:

1. 모델명이 정확한지 확인(``:latest`` 태그를 포함하는 경우 있음)::

    # 모델 목록 확인
    ollama list

2. 필요한 모델 다운로드::

    ollama pull gemma3:4b

타임아웃
------------

**증상**: 요청이 타임아웃됨

**해결 방법**:

1. 타임아웃 시간 연장::

    rag.llm.ollama.timeout=120000

2. 더 작은 모델 사용 또는 GPU 환경 검토

디버그 설정
------------

문제를 조사할 때는 |Fess|의 로그 레벨을 조정하여 Ollama 관련 상세 로그를 출력할 수 있습니다.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.ollama" level="DEBUG"/>

참고 정보
========

- `Ollama 공식 사이트 <https://ollama.com/>`__
- `Ollama 모델 라이브러리 <https://ollama.com/library>`__
- `Ollama GitHub <https://github.com/ollama/ollama>`__
- :doc:`llm-overview` - LLM 통합 개요
- :doc:`rag-chat` - AI 모드 기능 상세
