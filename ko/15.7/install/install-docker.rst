==============================
Docker 설치 (상세)
==============================

이 페이지에서는 Docker 및 Docker Compose를 사용한 |Fess| 의 설치 절차를 설명합니다.
Docker를 사용하면 간단하고 신속하게 |Fess| 환경을 구축할 수 있습니다.

전제 조건
============

- :doc:`prerequisites` 에 기재된 시스템 요구 사항을 충족할 것
- Docker 20.10 이상이 설치되어 있을 것
- Docker Compose 2.0 이상이 설치되어 있을 것

Docker 설치 확인
====================

다음 명령으로 Docker 및 Docker Compose의 버전을 확인합니다.

::

    $ docker --version
    $ docker compose version

.. note::

   이전 버전의 Docker Compose를 사용하는 경우 ``docker-compose`` 명령을 사용합니다.
   이 문서에서는 새로운 ``docker compose`` 명령 형식을 사용합니다.

Docker 이미지 정보
======================

|Fess| 를 Docker Compose로 시작하면 다음 2개의 컨테이너가 동작합니다.

- **Fess** (``fess01``): 전문 검색 시스템 본체
- **OpenSearch** (``search01``): 검색 엔진

공식 Docker 이미지는 `GitHub Container Registry <https://github.com/codelibs/docker-fess/pkgs/container/fess>`__ 에서 공개되고 있습니다.
Compose 파일 및 시작 절차는 `docker-fess <https://github.com/codelibs/docker-fess>`__ 리포지토리에서 관리됩니다.

단계 1: Docker Compose 파일 가져오기
========================================

Docker Compose를 사용한 시작에는 다음 파일이 필요합니다.

방법 1: 파일을 개별적으로 다운로드
------------------------------------

다음 파일을 다운로드합니다:

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.7.0/compose/compose.yaml
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.7.0/compose/compose-opensearch3.yaml

방법 2: Git으로 리포지토리 복제
----------------------------------

Git이 설치되어 있는 경우 리포지토리 전체를 클론할 수도 있습니다:

::

    $ git clone --depth 1 --branch v15.7.0 https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

단계 2: Docker Compose 파일 확인
====================================

``compose.yaml`` 의 내용
--------------------------

``compose.yaml`` 에는 Fess 본체(``fess01`` 서비스)의 설정이 포함되어 있습니다.

주요 설정 항목:

- **포트 번호**: Fess 웹 인터페이스의 포트 (기본값: 8080)
- **환경 변수**: OpenSearch 연결 대상 (``SEARCH_ENGINE_HTTP_URL``) 이나 사전 파일 경로 (``FESS_DICTIONARY_PATH``) 등
- **시작 순서**: OpenSearch (``search01``) 가 정상 상태가 된 후 시작하도록 ``depends_on`` 이 설정되어 있습니다

``compose-opensearch3.yaml`` 의 내용
---------------------------------------

``compose-opensearch3.yaml`` 에는 검색 엔진(``search01`` 서비스, OpenSearch)의 설정이 포함되어 있습니다.

주요 설정 항목:

- **OpenSearch 이미지**: 사용할 OpenSearch 이미지 (``ghcr.io/codelibs/fess-opensearch``)
- **메모리 설정**: JVM 힙 크기
- **볼륨**: 데이터 영속화용 볼륨 (``search01_data``: 인덱스 데이터, ``search01_dictionary``: 사전 파일)

설정 커스터마이징(옵션)
--------------------------

기본 설정을 변경하는 경우 ``compose.yaml`` 을 편집합니다.

예: 포트 번호를 변경하는 경우::

    services:
      fess01:
        ports:
          - "9080:8080"  # 호스트의 9080번 포트에 매핑

예: 메모리 설정을 변경하는 경우::

    services:
      fess01:
        environment:
          - "FESS_HEAP_SIZE=2g"  # Fess의 힙 크기를 2GB로 설정

단계 3: Docker 컨테이너 시작
================================

기본 시작
------------

다음 명령으로 Fess와 OpenSearch를 시작합니다:

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   - ``-f`` 옵션으로 여러 개의 Compose 파일을 지정합니다
   - ``-d`` 옵션으로 백그라운드에서 실행합니다

시작 로그 확인::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

``Ctrl+C`` 로 로그 표시를 종료할 수 있습니다.

시작 확인
------------

컨테이너 상태를 확인합니다::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

다음과 같은 컨테이너가 시작되어 있는지 확인하십시오:

- ``fess01``
- ``search01``

.. tip::

   시작에는 몇 분 정도 걸릴 수 있습니다. 먼저 OpenSearch (``search01``) 가 정상 상태가 된 후 Fess (``fess01``) 가 시작됩니다.
   ``docker compose ... ps`` 로 각 컨테이너의 상태를 확인하고, ``fess01`` 이 시작되면 브라우저에서 http://localhost:8080/ 에 접속할 수 있습니다.

단계 4: 브라우저에서 액세스
================================

시작이 완료되면 다음 URL에 접속합니다:

- **검색 화면**: http://localhost:8080/
- **관리 화면**: http://localhost:8080/admin

기본 관리자 계정:

- 사용자 이름: ``admin``
- 비밀번호: ``admin``

.. warning::

   **보안 관련 중요 주의사항**

   운영 환경에서는 관리자 비밀번호를 반드시 변경하십시오.
   자세한 내용은 :doc:`security` 를 참조하십시오.

AI 검색 모드(LLM 플러그인) 활성화
====================================

|Fess| 15.7부터 AI 검색 모드(RAG Chat) 기능은 ``fess-llm-*`` 플러그인으로 분리되었습니다.
공식 `docker-fess <https://github.com/codelibs/docker-fess>`__ 리포지토리에는 주요 LLM 프로바이더용 오버레이 파일이 동봉되어 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 오버레이
     - 용도
   * - ``compose-ollama.yaml``
     - Ollama (로컬 LLM, 추가 ``ollama01`` 서비스를 시작)
   * - ``compose-gemini.yaml``
     - Google Gemini (클라우드 API)
   * - ``compose-openai.yaml``
     - OpenAI (클라우드 API)

각 오버레이는 ``FESS_PLUGINS`` 로 해당 플러그인을 자동으로 가져오고, ``FESS_JAVA_OPTS`` 에
``-Dfess.config.rag.chat.enabled=true`` 를 설정하여 RAG Chat을 활성화합니다.
클라우드 API를 이용하는 Gemini와 OpenAI에서는 추가로 ``-Dfess.system.rag.llm.name`` 으로 사용할 프로바이더를 지정하고,
API 키 (``rag.llm.<provider>.api.key``) 와 모델 (``rag.llm.<provider>.model``) 을 설정합니다.
Ollama에서는 ``rag.llm.name`` 의 기본값 (``ollama``) 이 그대로 사용되므로 명시적인 지정은 없으며,
접속 대상 (``rag.llm.ollama.api.url``) 이 설정됩니다.

Gemini를 사용하는 예::

    $ export GEMINI_API_KEY="AIzaSy..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

OpenAI를 사용하는 예::

    $ export OPENAI_API_KEY="sk-..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

.. note::

   사용할 모델은 ``GEMINI_MODEL`` 및 ``OPENAI_MODEL`` 환경 변수로 변경할 수 있습니다
   (기본값은 각각 ``gemini-2.5-flash`` 와 ``gpt-5-mini`` 입니다).

Ollama를 사용하는 예::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    $ docker exec -it ollama01 ollama pull gpt-oss:20b

.. warning::

   ``compose-ollama.yaml`` 의 ``ollama01`` 서비스는 기본적으로 NVIDIA GPU를 사용하도록 정의되어 있습니다
   (`NVIDIA Container Toolkit <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html>`__ 가 필요합니다).
   GPU가 탑재되지 않은 환경에서 실행하는 경우에는 ``compose-ollama.yaml`` 의 ``deploy:`` 블록 (``reservations`` 아래의 GPU 지정)을 삭제하거나 주석 처리하십시오.

.. tip::

   시작 후 관리 화면 "시스템 > 전체" 의 설정 화면에서 사용할 LLM 프로바이더 (``rag.llm.name``) 나
   각 프로바이더 고유의 설정을 변경할 수 있습니다. 다만 이러한 변경 사항은 컨테이너 내부의 설정 파일에 저장되므로,
   컨테이너를 재생성(``docker compose down`` 후 ``up``)하면 사라집니다.
   설정을 영속화하려면 위 예시와 같이 Compose 파일의 ``FESS_JAVA_OPTS`` 로 지정하십시오.

데이터 영속화
================

|Fess| 의 데이터(인덱스, 크롤링한 문서, 사용자 정보, 설정 등)는 모두 OpenSearch에 저장됩니다.
이 데이터는 OpenSearch의 볼륨에 영속화되므로, 컨테이너를 삭제해도 데이터는 유지됩니다.
Fess 본체(``fess01``) 컨테이너 자체는 상태를 갖지 않으며, 전용 볼륨은 없습니다.

볼륨 확인::

    $ docker volume ls

``compose-opensearch3.yaml`` 에서 정의되는 주요 볼륨:

- ``search01_data``: OpenSearch의 인덱스 데이터(Fess의 모든 데이터를 포함)
- ``search01_dictionary``: 사전 파일

.. note::

   Docker Compose의 볼륨 이름에는 프로젝트 이름(기본값은 Compose 파일이 있는 디렉터리 이름)이 접두사로 붙습니다.
   예를 들어 ``compose`` 디렉터리에서 시작한 경우, 실제 볼륨 이름은 ``compose_search01_data`` 와 같이 됩니다.

.. important::

   컨테이너를 삭제해도 볼륨은 삭제되지 않습니다.
   볼륨을 삭제하려면 명시적으로 ``docker volume rm`` 명령을 실행해야 합니다.

Docker 컨테이너 중지
========================

컨테이너 중지::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

컨테이너 중지 및 삭제::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   ``down`` 명령은 컨테이너를 삭제하지만 볼륨은 삭제하지 않습니다.
   볼륨(``search01_data`` 등)도 삭제하려면 ``-v`` 옵션을 추가합니다::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

   **주의**: 이 명령을 실행하면 OpenSearch에 저장된 모든 데이터가 삭제됩니다.

고급 설정
============

환경 변수 커스터마이징
--------------------------

``compose.yaml`` 에서 환경 변수를 추가·변경함으로써 상세한 설정이 가능합니다.

주요 환경 변수:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 환경 변수
     - 설명
   * - ``FESS_HEAP_SIZE``
     - Fess의 JVM 힙 크기(Docker 이미지의 기본값: 512m)
   * - ``FESS_JAVA_OPTS``
     - 추가 JVM 옵션 지정(``-Dfess.config.*`` 에 의한 설정 오버라이드 등)
   * - ``FESS_PLUGINS``
     - 시작 시 자동으로 설치할 플러그인(공백으로 구분된 ``name:version`` 형식. 예: ``fess-ds-wikipedia:15.7.0``)
   * - ``SEARCH_ENGINE_HTTP_URL``
     - OpenSearch의 HTTP 엔드포인트(``compose.yaml`` 의 기본값: ``http://search01:9200``)
   * - ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD``
     - 인증이 활성화된 OpenSearch에 접속할 때의 자격 증명
   * - ``FESS_DICTIONARY_PATH``
     - 사전 파일의 경로(OpenSearch와 공유하는 디렉터리)
   * - ``FESS_PORT``
     - Fess가 컨테이너 내부에서 대기하는 포트(기본값: 8080)

예::

    services:
      fess01:
        environment:
          - "FESS_HEAP_SIZE=4g"

.. note::

   시간대를 변경하는 경우에는 ``FESS_JAVA_OPTS`` 에 ``-Duser.timezone=Asia/Tokyo`` 와 같이 지정합니다.

설정 파일 반영 방법
----------------------

|Fess| 의 상세한 설정은 ``fess_config.properties`` 파일에 기술합니다.
Docker 이미지에서는 ``fess_config.properties`` 가 컨테이너 내부의 ``/etc/fess`` 에 배치되어 있습니다.
Docker 환경에서 설정을 반영시키려면 다음 방법이 있습니다.

방법 1: 설정 파일 마운트
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``/etc/fess`` 에는 Fess 동작에 필요한 다른 설정 파일도 포함되어 있으므로, 이 디렉터리를 그대로 마운트로 교체하면 시작에 실패합니다.
대신 클래스패스 맨 앞에 추가되는 오버라이드용 디렉터리 ``/opt/fess`` 를 사용합니다(초기 상태는 비어 있습니다).

1. 호스트 측에 설정 파일을 준비하기 위한 디렉터리를 생성::

       $ mkdir -p /path/to/fess-config

2. 설정 파일 템플릿을 가져오기(최초 1회만)::

       $ curl -o /path/to/fess-config/fess_config.properties https://raw.githubusercontent.com/codelibs/fess/refs/tags/fess-15.7.0/src/main/resources/fess_config.properties

3. ``/path/to/fess-config/fess_config.properties`` 를 편집하여 필요한 설정을 기술::

       # 예
       crawler.document.cache.enabled=false
       adaptive.load.control=20
       query.facet.fields=label,host

4. ``compose.yaml`` 의 ``fess01`` 서비스에 볼륨 마운트를 추가::

       services:
         fess01:
           volumes:
             - /path/to/fess-config/fess_config.properties:/opt/fess/fess_config.properties

5. 컨테이너 시작::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   ``/opt/fess`` 는 클래스패스 맨 앞에 추가되므로, 여기에 배치한 ``fess_config.properties`` 가
   이미지에 동봉된 ``/etc/fess/fess_config.properties`` 보다 우선됩니다.
   프로퍼티 파일은 파일 단위로 읽어들이며, 항목별로 병합되지 않습니다.
   따라서 덮어쓰고 싶은 항목뿐만 아니라 **모든 설정 항목을 포함한 완전한 파일** 을 배치해야 합니다.
   일부 항목만 변경하고 싶은 경우에는 다음의 "방법 2"를 이용하십시오.

방법 2: 시스템 속성에 의한 설정
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``fess_config.properties`` 의 설정 항목을 환경 변수를 통해 시스템 속성으로 오버라이드할 수 있습니다.

``fess_config.properties`` 에 기재되는 설정 항목(예: ``crawler.document.cache.enabled=false``)을
``-Dfess.config.설정항목명=값`` 형식으로 지정합니다.

``compose.yaml`` 의 ``fess01`` 서비스의 환경 변수에 ``FESS_JAVA_OPTS`` 를 추가::

    services:
      fess01:
        environment:
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.cache.enabled=false -Dfess.config.adaptive.load.control=20 -Dfess.config.query.facet.fields=label,host"

.. note::

   ``-Dfess.config.`` 뒤에 이어지는 부분이 ``fess_config.properties`` 의 설정 항목명에 대응합니다.
   일부 항목만 오버라이드하는 경우에는 이 방법이 간단합니다.

외부 OpenSearch 연결
------------------------

기존 OpenSearch 클러스터를 사용하는 경우에는 ``compose-opensearch3.yaml`` 을 사용하지 않고 ``compose.yaml`` 만으로 시작하여 접속 대상을 변경합니다.

1. ``compose-opensearch3.yaml`` 을 지정하지 않고 시작::

       $ docker compose -f compose.yaml up -d

2. ``compose.yaml`` 의 ``fess01`` 서비스에서 접속 대상을 설정::

       environment:
         - "SEARCH_ENGINE_HTTP_URL=http://your-opensearch-host:9200"

.. note::

   인증이 활성화된 OpenSearch에 접속하는 경우에는 ``SEARCH_ENGINE_USERNAME`` 과 ``SEARCH_ENGINE_PASSWORD`` 도 지정합니다.

기타 오버레이 및 구성
------------------------

``docker-fess`` 리포지토리에는 위에서 설명한 것 외에도 용도별 Compose 파일 및 디렉터리가 포함되어 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 파일 / 디렉터리
     - 용도
   * - ``compose-dashboards3.yaml``
     - OpenSearch Dashboards를 추가(포트 5601, 데이터 시각화용)
   * - ``compose-minio.yaml``
     - MinIO(오브젝트 스토리지)를 추가하여 Fess의 스토리지 기능의 저장 위치로 이용
   * - ``vanilla/``
     - Fess용 플러그인을 포함하지 않는 순정 OpenSearch와 조합하는 구성(사전 관리 등 일부 기능은 이용 불가)
   * - ``snapshot/``
     - 개발판(snapshot) 이미지를 사용하는 구성(클러스터 구성 및 Elasticsearch 8과의 조합을 포함)
   * - ``multi-instance/``
     - 하나의 OpenSearch를 공유하는 여러 개의 Fess 인스턴스를 시작하는 구성

Docker 네트워크 설정
------------------------

여러 서비스와 연계하는 경우 사용자 정의 네트워크를 사용할 수 있습니다.

예::

    networks:
      fess-network:
        driver: bridge

    services:
      fess01:
        networks:
          - fess-network

Docker Compose로 운영 환경 운용
====================================

운영 환경에서 Docker Compose를 사용하는 경우의 권장 설정:

1. **리소스 제한 설정**::

       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 4G
           reservations:
             cpus: '1.0'
             memory: 2G

2. **재시작 정책 설정**::

       restart: unless-stopped

3. **로그 설정**::

       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"

4. **보안 설정 활성화**

   OpenSearch의 보안 플러그인을 활성화하고 적절한 인증을 설정합니다.
   자세한 내용은 :doc:`security` 를 참조하십시오.

문제 해결
============

컨테이너가 시작되지 않음
--------------------------

1. 로그 확인::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. 포트 번호 충돌 확인::

       $ sudo netstat -tuln | grep 8080
       $ sudo netstat -tuln | grep 9200

3. 디스크 용량 확인::

       $ df -h

메모리 부족 오류
--------------------

OpenSearch가 메모리 부족으로 시작되지 않는 경우, ``vm.max_map_count`` 를 늘려야 합니다.

Linux의 경우::

    $ sudo sysctl -w vm.max_map_count=262144

영구적으로 설정하는 경우::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

데이터 초기화
----------------

모든 데이터를 삭제하고 초기 상태로 되돌리기::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v
    $ docker volume prune

.. warning::

   이 명령을 실행하면 모든 데이터가 완전히 삭제됩니다.

다음 단계
============

설치가 완료되면 다음 문서를 참조하십시오:

- :doc:`run` - |Fess| 시작 및 초기 설정
- :doc:`security` - 운영 환경에서의 보안 설정
- :doc:`troubleshooting` - 문제 해결

자주 묻는 질문
==================

Q: 이미지 다운로드에는 어느 정도의 디스크 용량이 필요합니까?
----------------------------------------------------------------

A: Fess와 OpenSearch의 이미지는 처음 시작할 때 다운로드되며, 합쳐서 수 GB 정도의 디스크 용량이 필요합니다.
네트워크 환경에 따라 다운로드에 시간이 걸릴 수 있습니다.

Q: Kubernetes에서의 운용이 가능합니까?
--------------------------------------------

A: 가능합니다. Docker Compose 파일을 ``kompose`` 등의 도구로 Kubernetes 매니페스트로 변환하거나,
직접 매니페스트를 작성하여 운용할 수 있습니다(공식 Helm 차트는 제공되지 않습니다).

Q: 컨테이너 업데이트는 어떻게 수행합니까?
--------------------------------------------------

A: 다음 절차로 업데이트합니다:

1. 최신 Compose 파일 가져오기
2. 컨테이너 중지::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

3. 새 이미지 가져오기::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

4. 컨테이너 시작::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Q: 다중 노드 구성이 가능합니까?
--------------------------------------

A: 가능합니다. ``docker-fess`` 리포지토리의 ``snapshot/compose-cluster.yaml`` 을 참고하여 OpenSearch를 여러 노드로 구성하거나,
``multi-instance/`` 를 참고하여 하나의 OpenSearch를 공유하는 여러 개의 Fess 인스턴스를 구성할 수 있습니다.
다만 운영 환경에서는 Kubernetes 등의 오케스트레이션 도구 사용을 권장합니다.
