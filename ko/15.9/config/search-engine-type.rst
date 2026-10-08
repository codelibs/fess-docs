==============
검색 엔진 종류
==============

개요
====

|Fess| 는 데이터를 OpenSearch 에 저장합니다. ``search_engine.type`` 은 접속 대상 OpenSearch 가 어떤 종류인지를 |Fess| 에 알려 주는 설정입니다. 이 설정에 따라 |Fess| 가 생성하는 인덱스 정의와 사용할 수 있는 기능이 결정됩니다.

기본값인 ``default`` 는 CodeLibs 의 플러그인 4개(``opensearch-analysis-fess``, ``opensearch-analysis-extension``, ``opensearch-minhash``, ``opensearch-configsync``)가 설치된 OpenSearch 를 전제로 합니다( :doc:`../install/install` 참조). 자체 플러그인을 설치할 수 없는 매니지드 서비스 등, 이러한 플러그인이 없는 순정 OpenSearch 에 접속하는 경우에는 ``vanilla`` 를 지정합니다.

종류
====

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 값
     - 설명
   * - ``default``
     - CodeLibs 의 플러그인이 설치된 OpenSearch. 기본값입니다.
   * - ``vanilla``
     - CodeLibs 의 플러그인이 없는 순정 OpenSearch. 15.9 에서 추가되었습니다. 인덱스 정의는 ``fess_indices/_vanilla/`` 에서 읽어 들입니다. |Fess| 15.8 이전 버전은 이 값을 인식하지 못하므로, 15.8 이전 버전에서는 ``cloud`` 를 지정하십시오.
   * - ``aws``
     - ``vanilla`` 와 같습니다. Amazon OpenSearch Service 에서 사용하기 위한 종류입니다( :ref:`search-engine-type-aws` 참조).
   * - ``cloud``
     - ``vanilla`` 의 사용 중단 예정(deprecated) 별칭입니다. 시작할 때 경고를 로그에 출력합니다. ``vanilla`` 로 변경하십시오.
   * - 그 밖의 값
     - ``default`` 와 같게 취급합니다. 단, ``fess_indices/_<종류>/`` 에 있는 정의 파일이 ``fess_indices/`` 에 있는 같은 이름의 파일보다 우선합니다.

|Fess| 는 플러그인의 유무를 자동으로 판별하지 않으므로 사용자가 종류를 지정해야 합니다. 처음 시작하기 전에 설정하십시오. 인덱스 정의는 인덱스를 생성할 때 적용되므로, 나중에 값을 변경해도 이미 만들어진 인덱스는 바뀌지 않습니다.

플러그인 없이는 사용할 수 없는 기능
===================================

``vanilla`` 와 ``aws`` (사용 중단 예정인 ``cloud`` 포함)에서는 다음 기능을 사용할 수 없습니다. 이러한 기능에 의존하는 관리 화면의 항목은 표시되지 않습니다.

* **사전 관리**: [시스템 > 사전] 이 표시되지 않습니다. 사전 관리 화면과 사전 관리용 API(``/api/admin/dict/``)도 사용할 수 없습니다. 유지보수의 「사전 초기화」와 「문서 인덱스 다시 로드」도 표시되지 않습니다. 애널라이저는 사전 파일이 아니라 인덱스 정의에 포함된 규칙을 사용합니다.
* **검색 결과의 중복 접기**: 「일반」의 「중복 결과 접기」는 표시되지 않으며 항상 비활성 상태가 됩니다.
* **중복 문서 검출**: 내용이 같은 문서를 찾기 위한 내용 서명이 계산되지 않습니다. 문서 리포트의 「중복 문서」 탭은 표시되지 않습니다(「휴면 문서」는 사용할 수 있습니다). 유사 문서를 찾는 검색 파라미터 ``sdh`` 는 무시됩니다.
* **애널라이저**: 일본어, 한국어, 중국어 간체는 CodeLibs 의 토크나이저가 아니라 OpenSearch 표준의 Kuromoji, Nori, SmartCN 애널라이저로 분할됩니다. 따라서 ``default`` 와는 분할 결과가 다릅니다. 베트남어(``*_vi`` 필드)와 중국어 번체(``*_zh-tw`` 필드)는 어떤 단어도 등록하지 않는 빈 애널라이저가 사용됩니다. 이러한 언어의 문서도 언어에 의존하지 않는 ``content`` 필드와 ``title`` 필드에는 등록됩니다.

필요한 OpenSearch 플러그인
==========================

``vanilla`` 와 ``aws`` 의 인덱스 정의는 OpenSearch 공식 플러그인이 제공하는 애널라이저와 벡터 필드 타입을 사용합니다. 접속 대상 OpenSearch 에 다음 플러그인이 필요합니다.

* ``analysis-kuromoji``
* ``analysis-nori``
* ``analysis-smartcn``
* ``opensearch-knn`` (k-NN)

CodeLibs 의 플러그인은 필요하지 않습니다. 직접 운영하는 OpenSearch 에는 ``bin/opensearch-plugin install analysis-nori`` 와 같이 ``opensearch-plugin install`` 로 설치합니다. Amazon OpenSearch Service 에 대해서는 :ref:`search-engine-type-aws` 를 참조하십시오.

종류가 ``vanilla`` 또는 ``aws`` 이면 |Fess| 는 시작할 때 설치된 플러그인 목록을 조회합니다(``GET /_cat/plugins``). 위의 플러그인 중 하나라도 없으면 누락된 플러그인을 알리는 경고를 로그에 한 번 출력하고 그대로 시작을 계속합니다. 서비스가 이 API 를 허용하지 않는 등의 이유로 요청이 실패하면 확인을 건너뜁니다.

종류 설정
=========

Docker
------

``compose.yaml`` 의 ``fess01`` 서비스에 환경 변수 ``SEARCH_ENGINE_TYPE`` 을 지정합니다.

::

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "SEARCH_ENGINE_TYPE=vanilla"

``vanilla`` 는 |Fess| 15.9 이상의 이미지에서 지정할 수 있습니다. 그보다 이전 이미지에서는 ``SEARCH_ENGINE_TYPE=cloud`` 를 지정하십시오. 그 밖의 Docker 설정은 :doc:`../install/install-docker` 를 참조하십시오.

Docker 이외
-----------

``bin/fess.in.sh`` 는 ``SEARCH_ENGINE_TYPE`` 을 읽지 않습니다. 다음 중 한 가지 방법으로 지정합니다.

* ``fess_config.properties`` 에 ``search_engine.type`` 을 기술합니다(ZIP 버전은 ``app/WEB-INF/classes/fess_config.properties``, RPM/DEB 버전은 ``/etc/fess/fess_config.properties``).
* ZIP 버전의 ``bin/fess.in.sh`` (Windows 는 ``bin\fess.in.bat``)에서 ``FESS_JAVA_OPTS`` 에 JVM 옵션을 추가합니다.

::

    # fess_config.properties
    search_engine.type=vanilla

    # bin/fess.in.sh
    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.config.search_engine.type=vanilla"

    REM bin\fess.in.bat
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.config.search_engine.type=vanilla

변경한 후에는 |Fess| 를 재시작합니다. 크롤러 등 작업 프로세스에는 |Fess| 가 설정을 전달하므로 따로 지정할 필요가 없습니다.

접속 설정
=========

OpenSearch 로의 접속은 다른 종류와 같은 방법으로 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 설정
     - 설명
   * - ``search_engine.http.url``
     - OpenSearch 의 HTTP 엔드포인트. 환경 변수 ``SEARCH_ENGINE_HTTP_URL`` 을 지정한 경우에는 그쪽이 우선합니다.
   * - ``search_engine.username`` / ``search_engine.password``
     - HTTP Basic 인증의 사용자 이름과 비밀번호. 둘 다 지정한 경우에만 사용됩니다. Docker 에서는 환경 변수 ``SEARCH_ENGINE_USERNAME`` 과 ``SEARCH_ENGINE_PASSWORD`` 로 지정합니다.
   * - ``search_engine.http.ssl.certificate_authorities``
     - HTTPS 엔드포인트의 서버 인증서를 검증하기 위한 CA 인증서 파일(X.509)의 경로. Java 가 기본적으로 신뢰하는 CA 가 발급한 인증서라면 필요하지 않습니다.

``fess_config.properties`` 의 항목은 ``FESS_JAVA_OPTS`` 에 ``-Dfess.config.<항목 이름>`` 으로 지정하여 덮어쓸 수도 있습니다( :doc:`../install/install-docker` 참조).

.. _search-engine-type-aws:

Amazon OpenSearch Service
=========================

Amazon OpenSearch Service 도메인을 사용하는 경우에는 ``search_engine.type`` 에 ``aws`` 를 지정합니다(``vanilla`` 도 동일하게 동작합니다).

전제 조건
---------

* 도메인의 OpenSearch 가 3.x 일 것. |Fess| 는 시작할 때 엔진을 확인하며, OpenSearch 3 이외의 엔진이면 시작하지 않습니다.
* 「필요한 OpenSearch 플러그인」에 나열한 플러그인을 도메인에서 사용할 수 있을 것. Amazon OpenSearch Service 에서 Nori 는 선택 패키지입니다. |Fess| 를 시작하기 전에 도메인에 연결(associate)하십시오.
* 엔드포인트가 HTTPS 일 것.
* 세분화된 액세스 제어(fine-grained access control)를 활성화하고, |Fess| 가 로그인할 내부 사용자를 만들 것(HTTP Basic 인증). AWS IAM 자격 증명에 의한 요청 서명(SigV4)은 아직 지원하지 않으므로, IAM 으로 서명한 요청만 받는 도메인은 사용할 수 없습니다.

설정 예
-------

::

    search_engine.type=aws
    search_engine.http.url=https://<domain-endpoint>:443
    search_engine.username=<internal-user-name>
    search_engine.password=<password>

시작할 때의 확인
----------------

* 종류가 ``aws`` 인 경우에도 「필요한 OpenSearch 플러그인」에서 설명한 플러그인 확인이 수행됩니다. Nori 의 연결을 잊었다면 ``fess.log`` 에 경고가 출력됩니다.
* 도메인이 HTTP 401 또는 403 으로 요청을 거부하면 |Fess| 는 경고를 로그에 출력합니다. 이로 인해 시작에 실패했을 때의 오류 메시지에는 사용자 이름, 비밀번호, 도메인의 액세스 정책을 확인하도록 안내하는 내용이 포함됩니다.

DNS 캐시 TTL
------------

매니지드 서비스의 엔드포인트는 시간이 지나면 다른 IP 주소로 해석될 수 있고, JVM 은 DNS 조회 결과를 캐시합니다. 캐시 시간을 짧게 해 두면 주소가 바뀌어도 |Fess| 가 따라갈 수 있습니다. ``-Dsun.net.inetaddr.ttl=5`` (초)를 다음 두 곳에 지정합니다.

1. |Fess| 본체: ``FESS_JAVA_OPTS`` 에 추가합니다.

   ::

       FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dsun.net.inetaddr.ttl=5"

2. 작업 프로세스: 크롤러, Suggest, 청크, 썸네일 프로세스는 |Fess| 가 별도의 JVM 으로 시작하므로 ``FESS_JAVA_OPTS`` 를 이어받지 않습니다. ``fess_config.properties`` 의 ``jvm.crawler.options``, ``jvm.suggest.options``, ``jvm.chunk.options``, ``jvm.thumbnail.options`` 끝에 같은 옵션을 추가합니다. 이 값들은 한 줄에 옵션 하나씩 기술하며, 각 줄의 끝은 ``\n\`` 입니다.

   ::

       jvm.crawler.options=\
       -Djava.awt.headless=true\n\
       ...
       -Dsun.net.inetaddr.ttl=5\n\

   기존 줄 뒤에 이 줄을 추가하고, 나머지 3개 항목에도 같은 방법으로 추가하십시오.

Docker 에서는 ``FESS_JAVA_OPTS`` 를 Compose 파일의 환경 변수로 지정합니다. ``jvm.*.options`` 를 변경하려면 수정한 ``fess_config.properties`` 를 마운트합니다( :doc:`../install/install-docker` 참조).
