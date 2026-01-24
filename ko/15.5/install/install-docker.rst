==============================
Docker 설치 (상세)
==============================

이 페이지에서는 Docker 및 Docker Compose를 사용한 |Fess| 의 설치 절차를 설명합니다.
Docker를 사용하면 간단하고 신속하게 |Fess| 환경을 구축할 수 있습니다.

전제 조건
========

- :doc:`prerequisites` 에 기재된 시스템 요구사항을 충족할 것
- Docker 20.10 이상이 설치되어 있을 것
- Docker Compose 2.0 이상이 설치되어 있을 것

Docker 설치 확인
=======================

다음 명령으로 Docker 및 Docker Compose 버전을 확인합니다.

::

    $ docker --version
    $ docker compose version

.. note::

   이전 버전의 Docker Compose를 사용하는 경우 ``docker-compose`` 명령을 사용합니다.
   본 문서에서는 새로운 ``docker compose`` 명령 형식을 사용하고 있습니다.

Docker 이미지 정보
=====================

|Fess| 의 Docker 이미지는 다음 구성요소로 구성됩니다:

- **Fess**: 전문 검색 시스템 본체
- **OpenSearch**: 검색 엔진

공식 Docker 이미지는 `Docker Hub <https://hub.docker.com/r/codelibs/fess>`__ 에서 공개되고 있습니다.

단계 1: Docker Compose 파일 가져오기
=======================================

Docker Compose를 사용한 시작에는 다음 파일이 필요합니다.

방법 1: 파일을 개별적으로 다운로드
----------------------------------

다음 파일을 다운로드합니다:

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.5.0/compose/compose.yaml
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.5.0/compose/compose-opensearch3.yaml

방법 2: Git으로 리포지토리 복제
--------------------------------

Git이 설치되어 있는 경우 리포지토리 전체를 복제할 수도 있습니다:

::

    $ git clone --depth 1 --branch v15.5.0 https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

단계 2: Docker Compose 파일 확인
=======================================

``compose.yaml`` 의 내용
----------------------

``compose.yaml`` 에는 Fess의 기본 설정이 포함되어 있습니다.

주요 설정 항목:

- **포트 번호**: Fess의 웹 인터페이스 포트(기본값: 8080)
- **환경 변수**: Java 힙 크기 등의 설정
- **볼륨**: 데이터 영속화 설정

``compose-opensearch3.yaml`` 의 내용
---------------------------------

``compose-opensearch3.yaml`` 에는 OpenSearch 설정이 포함되어 있습니다.

주요 설정 항목:

- **OpenSearch 버전**: 사용할 OpenSearch 버전
- **메모리 설정**: JVM 힙 크기
- **볼륨**: 인덱스 데이터 영속화 설정

설정 커스터마이징(옵션)
------------------------------

기본 설정을 변경하는 경우 ``compose.yaml`` 을 편집합니다.

예: 포트 번호 변경::

    services:
      fess:
        ports:
          - "9080:8080"  # 호스트의 9080번 포트에 매핑

예: 메모리 설정 변경::

    services:
      fess:
        environment:
          - "FESS_HEAP_SIZE=2g"  # Fess의 힙 크기를 2GB로 설정

단계 3: Docker 컨테이너 시작
================================

기본 시작
----------

다음 명령으로 Fess와 OpenSearch를 시작합니다:

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   - ``-f`` 옵션으로 여러 Compose 파일을 지정합니다
   - ``-d`` 옵션으로 백그라운드에서 실행합니다

시작 로그 확인::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

``Ctrl+C`` 로 로그 표시를 종료할 수 있습니다.

시작 확인
--------

컨테이너 상태를 확인합니다::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

다음과 같은 컨테이너가 시작되어 있는지 확인하십시오:

- ``fess``
- ``opensearch``

.. tip::

   시작에는 몇 분 정도 소요될 수 있습니다.
   로그에서 "Fess is ready" 또는 유사한 메시지가 표시될 때까지 기다립니다.

단계 4: 브라우저에서 액세스
==============================

시작이 완료되면 다음 URL에 액세스합니다:

- **검색 화면**: http://localhost:8080/
- **관리 화면**: http://localhost:8080/admin

기본 관리자 계정:

- 사용자 이름: ``admin``
- 비밀번호: ``admin``

.. warning::

   **보안 관련 중요 주의사항**

   운영 환경에서는 관리자 비밀번호를 반드시 변경하십시오.
   자세한 내용은 :doc:`security` 를 참조하십시오.

데이터 영속화
============

Docker 컨테이너를 삭제해도 데이터를 유지하기 위해 볼륨이 자동으로 생성됩니다.

볼륨 확인::

    $ docker volume ls

|Fess| 관련 볼륨:

- ``fess-es-data``: OpenSearch의 인덱스 데이터
- ``fess-data``: Fess의 설정 데이터

.. important::

   컨테이너를 삭제해도 볼륨은 삭제되지 않습니다.
   볼륨을 삭제하려면 명시적으로 ``docker volume rm`` 명령을 실행해야 합니다.

Docker 컨테이너 중지
===================

컨테이너 중지::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

컨테이너 중지 및 삭제::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   ``down`` 명령은 컨테이너를 삭제하지만 볼륨은 삭제하지 않습니다.
   볼륨도 삭제하는 경우 ``-v`` 옵션을 추가합니다::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

   **주의**: 이 명령을 실행하면 모든 데이터가 삭제됩니다.

고급 설정
========

환경 변수 커스터마이징
--------------------

``compose.yaml`` 에서 환경 변수를 추가·변경하여 상세한 설정이 가능합니다.

주요 환경 변수:

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - 환경 변수
     - 설명
   * - ``FESS_HEAP_SIZE``
     - Fess의 JVM 힙 크기(기본값: 1g)
   * - ``SEARCH_ENGINE_HTTP_URL``
     - OpenSearch의 HTTP 엔드포인트
   * - ``TZ``
     - 시간대(예: Asia/Seoul)

예::

    environment:
      - "FESS_HEAP_SIZE=4g"
      - "TZ=Asia/Seoul"

설정 파일 반영 방법
--------------------

|Fess| 의 상세한 설정은 ``fess_config.properties`` 파일에 기술합니다.
Docker 환경에서는 이 파일의 설정을 반영시키기 위해 다음 방법이 있습니다.

방법 1: 설정 파일 마운트
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``fess_config.properties`` 등의 설정 파일을 포함하는 디렉터리를 마운트하여
호스트 측에서 편집한 설정 파일을 컨테이너에 반영할 수 있습니다.

1. 호스트 측에 설정 디렉터리 생성::

       $ mkdir -p /path/to/fess-config

2. 설정 파일 템플릿 가져오기(최초 1회)::

       $ curl -o /path/to/fess-config/fess_config.properties https://raw.githubusercontent.com/codelibs/fess/refs/tags/fess-15.5.0/src/main/resources/fess_config.properties

3. ``/path/to/fess-config/fess_config.properties`` 를 편집하여 필요한 설정 기술::

       # 예
       crawler.document.cache.enabled=false
       adaptive.load.control=20
       query.facet.fields=label,host

4. ``compose.yaml`` 에 볼륨 마운트 추가::

       services:
         fess:
           volumes:
             - /path/to/fess-config:/opt/fess/app/WEB-INF/conf

5. 컨테이너 시작::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   ``fess_config.properties`` 에는 검색 설정, 크롤러 설정,
   메일 설정, 기타 시스템 설정을 기술합니다.
   ``docker compose down`` 으로 컨테이너를 삭제해도 호스트 측 파일은 유지됩니다.

방법 2: 시스템 속성에 의한 설정
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``fess_config.properties`` 의 설정 항목을 환경 변수를 통해 시스템 속성으로 덮어쓸 수 있습니다.

``fess_config.properties`` 에 기재되는 설정 항목(예: ``crawler.document.cache.enabled=false``)을
``-Dfess.config.설정항목명=값`` 형식으로 지정합니다.

``compose.yaml`` 의 환경 변수에 ``FESS_JAVA_OPTS`` 를 추가::

    services:
      fess:
        environment:
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.cache.enabled=false -Dfess.config.adaptive.load.control=20 -Dfess.config.query.facet.fields=label,host"

.. note::

   ``-Dfess.config.`` 뒤에 계속되는 부분이 ``fess_config.properties`` 의 설정 항목명에 대응합니다.

외부 OpenSearch 연결
------------------------

기존 OpenSearch 클러스터를 사용하는 경우 ``compose.yaml`` 을 편집하여 연결 대상을 변경합니다.

1. ``compose-opensearch3.yaml`` 을 사용하지 않음::

       $ docker compose -f compose.yaml up -d

2. ``SEARCH_ENGINE_HTTP_URL`` 설정::

       environment:
         - "SEARCH_ENGINE_HTTP_URL=http://your-opensearch-host:9200"

Docker 네트워크 설정
-----------------------

여러 서비스와 연계하는 경우 사용자 정의 네트워크를 사용할 수 있습니다.

예::

    networks:
      fess-network:
        driver: bridge

    services:
      fess:
        networks:
          - fess-network

Docker Compose로 운영 환경 운용
=========================

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
====================

컨테이너가 시작되지 않음
------------------

1. 로그 확인::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. 포트 번호 충돌 확인::

       $ sudo netstat -tuln | grep 8080
       $ sudo netstat -tuln | grep 9200

3. 디스크 용량 확인::

       $ df -h

메모리 부족 오류
--------------

OpenSearch가 메모리 부족으로 시작되지 않는 경우 ``vm.max_map_count`` 를 늘려야 합니다.

Linux의 경우::

    $ sudo sysctl -w vm.max_map_count=262144

영구적으로 설정하는 경우::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

데이터 초기화
------------

모든 데이터를 삭제하고 초기 상태로 되돌리기::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v
    $ docker volume prune

.. warning::

   이 명령을 실행하면 모든 데이터가 완전히 삭제됩니다.

다음 단계
==========

설치가 완료되면 다음 문서를 참조하십시오:

- :doc:`run` - |Fess| 시작 및 초기 설정
- :doc:`security` - 운영 환경의 보안 설정
- :doc:`troubleshooting` - 문제 해결

자주 묻는 질문
==========

Q: Docker 이미지의 크기는 어느 정도입니까?
--------------------------------------------

A: Fess 이미지는 약 1GB, OpenSearch 이미지는 약 800MB입니다.
최초 시작 시에는 다운로드에 시간이 소요될 수 있습니다.

Q: Kubernetes에서의 운용이 가능합니까?
----------------------------------

A: 가능합니다. Docker Compose 파일을 Kubernetes 매니페스트로 변환하거나
Helm 차트를 사용하여 Kubernetes 상에서 운용할 수 있습니다.
자세한 내용은 Fess 공식 문서를 참조하십시오.

Q: 컨테이너 업데이트는 어떻게 수행합니까?
----------------------------------------------

A: 다음 절차로 업데이트합니다:

1. 최신 Compose 파일 가져오기
2. 컨테이너 중지::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

3. 새 이미지 가져오기::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

4. 컨테이너 시작::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Q: 다중 노드 구성이 가능합니까?
--------------------------------

A: 가능합니다. ``compose-opensearch3.yaml`` 을 편집하여 여러 OpenSearch 노드를 정의하면
클러스터 구성으로 만들 수 있습니다. 다만 운영 환경에서는 Kubernetes 등의 오케스트레이션 도구 사용을 권장합니다.
