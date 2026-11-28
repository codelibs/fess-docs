=======================================
문서와 사용자 증가에 맞춰 Fess 확장하기
=======================================

시작하며
========

문서와 사용자가 늘어나면 "크롤링이 아침까지 끝나지 않는다", "검색이 느려졌다", "Fess가 OutOfMemoryError로 멈췄다" 같은 문제가 생깁니다.
이때 곧바로 서버를 늘린다고 해결된다는 보장은 없습니다.
Fess는 여러 JVM 프로세스로 동작하며, 부족해지는 것은 그중 하나인 경우가 많기 때문입니다.

이 글에서는 Fess 15.9를 대상으로, 다음 순서로 확장하는 절차를 설명합니다.

1. 어느 프로세스의 무엇이 부족한지 확인한다
2. 서버 1대인 채로 메모리와 크롤링 병렬도를 조정한다
3. OpenSearch를 별도 서버로 분리한다
4. OpenSearch를 3대 클러스터로 만든다
5. Fess를 여러 대로 늘린다

모니터링 체계 구축(헬스 체크, 로그, 알림)과 백업은 :doc:`guide-10`\ 에서 다룹니다.

Fess를 구성하는 프로세스
========================

Fess를 1대로 운영하더라도 메모리 설정은 다음과 같이 나뉘어 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 20 30 25 25

   * - 프로세스
     - 역할
     - 힙 기본값
     - 설정하는 곳
   * - Fess 본체
     - 검색 화면, 관리 화면, API, 스케줄러
     - ZIP 버전은 최소 256m·최대 2g, RPM/DEB 버전과 Docker 이미지는 512m
     - 환경 변수 ``FESS_HEAP_SIZE``
   * - 크롤러
     - 크롤링 작업마다 시작되는 별도 JVM
     - 최대 512m
     - ``fess_config.properties``\ 의 ``jvm.crawler.options``
   * - 서제스트 생성, 썸네일 생성
     - 작업마다 시작되는 별도 JVM
     - 최대 256m
     - ``jvm.suggest.options``, ``jvm.thumbnail.options``
   * - OpenSearch
     - 인덱스 저장과 검색 실행
     - docker-fess의 ``compose-opensearch3.yaml``\ 에서는 1g
     - ``OPENSEARCH_JAVA_OPTS`` 또는 ``config/jvm.options``

시맨틱 검색에서 사용하는 청크 처리에도 별도 JVM(``jvm.chunk.options``, 최대 1g)이 있지만, 이는 :doc:`guide-18`\ 에서 다룹니다.

``fess-crawler.log``\ 에 OutOfMemoryError가 나온다면 부족한 것은 크롤러의 JVM입니다.
이 경우 ``FESS_HEAP_SIZE``\ 를 늘려도 효과가 없습니다.

부족한 것을 확인하기
====================

증상별로 다음 위치를 확인합니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 증상
     - 확인할 곳
   * - 검색이 느리다
     - [시스템 정보] > [검색 로그]의 [성능] 탭에서 응답 시간의 p95·p99와 응답이 느린 검색어를 봅니다. 특정 검색어만 느린지, 전체가 느린지를 구분합니다.
   * - 크롤링이 끝나지 않는다
     - [시스템 정보] > [작업 로그]에서 크롤링 작업의 시작 시간과 종료 시간의 추이를 봅니다. ``fess-crawler.log``\ 에 ``Cpu Load XX% is greater than 50%``\ 가 계속 나온다면 뒤에서 설명하는 부하 제어 때문에 대기하고 있는 것입니다.
   * - 크롤러가 멈춘다
     - ``fess-crawler.log``\ 에서 ``OutOfMemoryError``\ 를 찾습니다.
   * - Fess 본체가 멈춘다·관리 화면이 무겁다
     - ``fess.log``\ 의 ``OutOfMemoryError``\ 와 ``/api/admin/stats``\ 의 ``response.stats.jvm.memory.heap.percent``\ 를 봅니다.
   * - OpenSearch가 무겁다
     - ``/api/admin/stats``\ 의 ``response.stats.engine.status``\ 와 OpenSearch의 ``_cat/nodes``\ 에서 힙 사용률을 봅니다. ``circuit_breaker_exception``\ 은 힙 부족의 징후입니다.

``/api/admin/stats``\ 가 반환하는 것은 요청을 받은 Fess 본체의 JVM과 OS, 그리고 OpenSearch 클러스터의 상태입니다.
크롤러의 JVM과 OpenSearch 각 노드의 힙은 포함되지 않습니다.
호출하려면 ``admin-api`` 권한을 가진 액세스 토큰이 필요합니다.
만드는 방법은 `Admin API 개요 <https://fess.codelibs.org/ko/stable/api/admin/api-admin-overview.html>`__, 응답 항목은 `Stats API <https://fess.codelibs.org/ko/stable/api/admin/api-admin-stats.html>`__\ 를 참조하십시오.

OpenSearch 각 노드의 힙은 OpenSearch에 직접 조회합니다.

::

    $ curl -s 'http://localhost:9200/_cat/nodes?v&h=name,heap.max,heap.percent,ram.percent,cpu'

인덱스의 문서 수와 크기는 다음 명령으로 확인할 수 있습니다.
``fess.search``\ 는 검색에 사용하는 인덱스의 별칭입니다.

::

    $ curl -s 'http://localhost:9200/_cat/indices/fess.search?v&h=index,docs.count,pri.store.size,store.size'

1대인 채로 조정하기
===================

Fess 본체의 힙 변경
-------------------

Docker의 경우 ``compose.yaml``\ 의 ``fess01``\ 의 ``environment``\ 에 ``FESS_HEAP_SIZE``\ 를 추가합니다.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_DICTIONARY_PATH=${FESS_DICTIONARY_PATH:-/usr/share/opensearch/config/dictionary/}"
          - "FESS_HEAP_SIZE=2g"

``compose.yaml``\ 의 ``fess01``\ 의 ``environment``\ 나 ``volumes``\ 를 바꾸고 ``docker compose ... up -d``\ 를 실행하면 ``fess01`` 컨테이너가 다시 만들어집니다.
[시스템] > [일반]에서 바꾼 설정은 컨테이너 안의 ``system.properties``\ 에 있으므로, 다시 만들면 사라집니다.
이 글의 다른 절차에서 ``compose.yaml``\ 을 바꾸는 경우도 마찬가지입니다.
먼저 :doc:`guide-10`\ 의 절차로 백업을 받아 두십시오.

RPM 버전은 ``/etc/sysconfig/fess``, DEB 버전은 ``/etc/default/fess``\ 의 ``FESS_HEAP_SIZE=512m``\ 를 수정하고 Fess를 재시작합니다.
ZIP 버전은 Fess를 시작하는 환경에서 ``FESS_HEAP_SIZE``\ 를 export합니다.

반영되었는지는 실행 중인 프로세스의 인수로 확인합니다.
Docker의 경우는 다음과 같습니다.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml exec -T fess01 sh -c 'cat /proc/[0-9]*/cmdline 2>/dev/null' | tr '\0' '\n' | grep -e '^-Xmx' -e 'FessBoot' -e 'exec.Crawler'
    -Xmx2g
    org.codelibs.fess.FessBoot

``-Xmx`` 다음 줄이 해당 프로세스의 종류입니다.
``FessBoot``\ 는 Fess 본체, ``exec.Crawler``\ 는 크롤러입니다.
RPM/DEB 버전과 ZIP 버전에서는 ``sh -c`` 안의 명령부터 뒤를 Fess 서버에서 직접 실행합니다.

크롤러의 힙 변경
----------------

``jvm.crawler.options``\ 는 JVM 옵션을 ``\n``\ 으로 구분해 나열한 하나의 값입니다.
값 전체가 대체되므로 ``-Xmx1g``\ 만 적으면 G1GC 등 기본 옵션이 모두 사라집니다.
기본값을 남긴 채 ``-Xmx512m`` 줄만 수정합니다.

::

    -Xms128m\n\
    -Xmx1g\n\

설정 파일의 위치는 RPM/DEB 버전이 ``/etc/fess/fess_config.properties``, ZIP 버전이 ``app/WEB-INF/classes/fess_config.properties``\ 입니다.
Docker에서는 이미지의 ``fess_config.properties``\ 를 로컬로 가져와 편집한 뒤, 컨테이너의 ``/opt/fess/fess_config.properties``\ 에 마운트합니다.
``/opt/fess``\ 는 ``/etc/fess``\ 보다 우선해서 읽힙니다.
이 값은 여러 줄에 걸쳐 있으므로 ``FESS_JAVA_OPTS``\ 의 ``-Dfess.config.``\ 로 지정하는 데는 적합하지 않습니다.
절차는 `Docker 설치 (상세) <https://fess.codelibs.org/ko/stable/install/install-docker.html>`__\ 의 "설정 파일 반영 방법"을 참조하십시오.

Fess를 재시작한 후 [시스템 정보] > [설정 정보]의 "앱 속성"에서 ``jvm.crawler.options``\ 에 ``-Xmx1g``\ 가 포함되어 있는지 확인합니다.
변경은 다음에 시작되는 크롤러부터 적용됩니다.
크롤링 실행 중에 앞 절의 명령을 실행하면 ``org.codelibs.fess.exec.Crawler`` 앞 줄에 ``-Xmx1g``\ 가 표시됩니다.

크롤러의 JVM은 크롤링 작업 하나당 하나씩 시작됩니다.
"Default Crawler" 작업은 모든 크롤링 설정을 하나의 크롤러로 처리합니다.
크롤링 설정 상세 화면의 [새 작업 작성]으로 설정마다 작업을 만들면 각각이 별도의 크롤러로 시작되고, 각각이 ``-Xmx``\ 만큼 메모리를 사용합니다.
동시에 동작하는 크롤러 수에 상한을 두려면 ``fess_config.properties``\ 의 ``job.max.crawler.processes``\ (기본값 ``0``\ 은 무제한)를 사용합니다.
상한을 넘어 시작된 크롤링 작업은 차례를 기다리지 않고 오류로 종료됩니다.

서제스트 생성과 썸네일 생성의 JVM도 같은 방법으로 ``jvm.suggest.options``\ 와 ``jvm.thumbnail.options``\ 의 ``-Xmx256m`` 줄을 수정합니다.

OpenSearch의 힙 변경
--------------------

docker-fess에서는 ``compose-opensearch3.yaml``\ 의 ``search01``\ 에 다음 줄이 있습니다.

::

    - "OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g"

이 두 값을 같은 값으로 수정합니다.
ZIP이나 RPM으로 설치한 OpenSearch는 ``config/jvm.options``\ 의 ``-Xms``\ 와 ``-Xmx``\ 를 수정하고 재시작합니다.

상한의 기준은 물리 메모리의 절반 이하, 그리고 32GB 미만입니다.
나머지 메모리는 OS의 파일 캐시로서 검색 속도에 기여하므로 힙에 너무 많이 할당하지 않도록 합니다.
32GB 이상으로 하면 JVM의 Compressed OOPs가 비활성화되어 오히려 효율이 떨어집니다.
그 이상이 필요한 규모에서는 노드를 늘립니다.

인덱스 크기와 힙의 대응 기준은 `메모리 설정 <https://fess.codelibs.org/ko/stable/config/setup-memory.html>`__\ 에 있습니다.
기준에서 시작해, 앞에서 언급한 ``_cat/nodes``\ 의 힙 사용률과 검색 응답 시간을 보면서 조정합니다.

Fess와 OpenSearch를 같은 서버에서 운영하는 경우에는 Fess 본체, 크롤러, OpenSearch의 힙 합계가 물리 메모리 안에 들어가도록 합니다.

크롤링 병렬도 변경
------------------

크롤링 속도는 다음 3가지 설정으로 정해집니다.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - 설정
     - 기본값
     - 위치
   * - 스레드 수
     - 웹 1, 파일 시스템 5
     - 각 크롤링 설정([크롤러] > [웹], [파일 시스템])
   * - 간격
     - 웹 10000밀리초, 파일 시스템 1000밀리초
     - 위와 같음. 스레드마다 URL을 가져올 때마다 기다리는 시간입니다
   * - 동시 크롤러 설정
     - 5
     - [시스템] > [일반]. 하나의 크롤러에서 동시에 처리하는 크롤링 설정의 수입니다

스레드 수를 늘리면 해당 크롤링 설정의 수집은 빨라지지만, 크롤러의 메모리 사용량과 크롤링 대상 서버의 부하도 늘어납니다.
외부 사이트나 업무에서 사용 중인 서버를 크롤링하는 경우에는 간격을 너무 짧게 하지 않도록 합니다.

1대 구성에서 놓치기 쉬운 것이 ``fess_config.properties``\ 의 ``adaptive.load.control``\ (기본값 ``50``)입니다.
Fess가 동작하는 서버의 CPU 사용률이 이 값 이상인 동안에는 크롤링과 인덱스 등록 스레드가 대기합니다.
같은 서버에서 OpenSearch가 인덱스 쓰기나 검색에 CPU를 사용하고 있으면 크롤링이 거의 진행되지 않을 수 있습니다.
이때 ``fess-crawler.log``\ 에는 ``Cpu Load XX% is greater than 50%``\ 가 출력됩니다.
값을 올릴 수도 있지만, CPU가 만성적으로 부족하다면 다음 절처럼 OpenSearch를 별도 서버로 분리하는 것이 근본적인 대책입니다.
자세한 내용은 `부하 제어 설정 <https://fess.codelibs.org/ko/stable/config/load-control.html>`__\ 을 참조하십시오.

OpenSearch를 별도 서버로 분리하기
=================================

OpenSearch를 별도 서버로 옮기면 크롤링과 검색이 CPU, 메모리, 디스크 I/O를 서로 빼앗지 않게 됩니다.

OpenSearch 쪽에 필요한 것
-------------------------

Fess가 사용하는 OpenSearch에는 다음 2가지가 필요합니다.

- Fess용 플러그인 4개(``opensearch-analysis-fess``, ``opensearch-analysis-extension``, ``opensearch-minhash``, ``opensearch-configsync``). 버전은 OpenSearch와 일치시킵니다(Fess 15.9는 OpenSearch 3.9.0)
- ``opensearch.yml``\ 의 ``configsync.config_path``. OpenSearch 설정 디렉터리 아래에 있는 사전 파일용 디렉터리를 절대 경로로 지정합니다

설치 명령은 `Linux 설치 (상세 절차) <https://fess.codelibs.org/ko/stable/install/install-linux.html>`__\ 에 있습니다.
docker-fess의 ``ghcr.io/codelibs/fess-opensearch`` 이미지에는 이것들이 처음부터 들어 있습니다.

OpenSearch를 별도 서버에 두면 포트 9200이 네트워크에 공개됩니다.
보안 플러그인을 비활성화한 채로 운영 환경에서 사용하지 마십시오.
설정은 :doc:`guide-15`\ 와 `보안 설정 <https://fess.codelibs.org/ko/stable/install/security.html>`__\ 을 참조하십시오.

Fess 쪽에서 설정할 것
---------------------

Fess에는 접속 대상과 사전 위치를 2개의 환경 변수로 지정합니다.

- ``SEARCH_ENGINE_HTTP_URL`` : OpenSearch의 URL
- ``FESS_DICTIONARY_PATH`` : OpenSearch 쪽 ``configsync.config_path``\ 와 같은 경로

``FESS_DICTIONARY_PATH``\ 는 OpenSearch 서버상의 경로입니다.
Fess는 사전 파일을 ``configsync`` 플러그인을 통해 쓰므로, Fess 서버에서 그 디렉터리를 마운트할 필요는 없습니다.
설정하지 않으면 Fess는 인덱스를 만들 수 없어 시작되지 않습니다.

설정하는 곳은 RPM 버전이 ``/etc/sysconfig/fess``, DEB 버전이 ``/etc/default/fess``, ZIP 버전이 ``bin/fess.in.sh``\ 입니다.
Docker에서는 ``compose-opensearch3.yaml``\ 을 사용하지 않고, ``compose.yaml``\ 의 ``fess01``\ 의 ``environment``\ 에서 지정합니다.
v15.9.0의 ``compose.yaml``\ 의 ``fess01``\ 에는 ``search01``\ 을 기다리는 ``depends_on``\ 이 있어, ``search01``\ 을 정의하지 않는 구성에서는 ``service "fess01" depends on undefined service "search01"``\ 라는 오류로 시작할 수 없습니다.
``depends_on``\ 부터 ``condition: service_healthy``\ 까지의 3줄을 삭제합니다.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://opensearch1.example.com:9200"
          - "FESS_DICTIONARY_PATH=/etc/opensearch/dictionary/"

이 경우 이후의 ``docker compose`` 명령은 ``-f compose.yaml``\ 만으로 실행합니다.

ZIP 버전에서는 Fess를 시작하기 전에 ``bin/fess-setup check``\ 로 접속, 플러그인 4개, ``configsync``\ 의 응답을 확인할 수 있습니다.

::

    $ bin/fess-setup check --url http://opensearch1.example.com:9200

접속 대상을 바꿔도 기존 인덱스는 새 OpenSearch로 옮겨지지 않습니다.
기존 문서를 이어받으려면 스냅샷으로 이전합니다(`인덱스 관리 <https://fess.codelibs.org/ko/stable/config/admin-index-backup.html>`__\ 의 "데이터 이전").
다시 크롤링하면 되는 경우에는 빈 OpenSearch에 접속해 재크롤링하는 편이 간단합니다.

OpenSearch를 3대 클러스터로 만들기
==================================

OpenSearch를 1대로 운영하는 동안에는 그 서버가 멈추면 검색도 멈춥니다.
이중화가 필요해지면 OpenSearch를 클러스터로 만듭니다.

노드 구성
---------

클러스터 관리를 맡는 노드(cluster manager)를 선출하려면 과반수의 합의가 필요합니다.
cluster manager가 될 수 있는 노드가 1대나 2대라면 1대만 멈춰도 선출할 수 없게 됩니다.
그래서 cluster manager가 될 수 있는 노드를 3대 준비합니다.
3대 모두에 데이터도 담당시키는 구성이 가장 작은 구성입니다.

각 노드의 ``opensearch.yml`` 가운데 클러스터 구성에 관련된 설정의 예입니다(``node.name``\ 은 노드마다 바꿉니다).
``network.host`` 등의 네트워크 설정과 보안 설정은 환경에 맞게 추가합니다.

.. code-block:: yaml

    cluster.name: fess-search
    node.name: search01
    node.roles: [ cluster_manager, data, ingest ]
    discovery.seed_hosts: [ "search01", "search02", "search03" ]
    cluster.initial_cluster_manager_nodes: [ "search01", "search02", "search03" ]
    configsync.config_path: /etc/opensearch/dictionary/

Fess용 플러그인 4개는 3대 모두에 같은 버전으로 설치합니다.
``configsync.config_path``\ 도 3대에서 같은 경로로 합니다.
Fess는 인덱스 설정에 ``FESS_DICTIONARY_PATH`` 값을 하나만 쓰고, 어느 노드든 그 경로의 사전을 읽기 때문입니다.

docker-fess의 ``compose/snapshot/compose-cluster.yaml``\ 에 Docker로 여러 노드를 구성하는 예가 있습니다.
이 예는 개발 버전의 Fess 이미지와 조합하는 것을 전제로 한 파일이므로, OpenSearch 환경 변수를 작성하는 방법의 참고로 활용하십시오.

Fess에서의 접속
---------------

``SEARCH_ENGINE_HTTP_URL``\ 에는 노드의 URL을 쉼표로 구분해 나열합니다.
일부 노드가 멈춰 있어도 Fess는 나머지 노드에 접속합니다.

::

    SEARCH_ENGINE_HTTP_URL=http://search01:9200,http://search02:9200,http://search03:9200

샤드와 복제본
-------------

Fess는 문서용 인덱스를 ``fess_config.properties``\ 의 ``index.number_of_shards``\ (기본값 ``5``, 프라이머리 샤드 수)와 ``index.auto_expand_replicas``\ (기본값 ``0-1``, 데이터 노드 수에 맞춰 복제본을 0~1 범위에서 자동으로 증감)로 생성합니다.
기본값이 ``0-1``\ 이므로 데이터 노드가 2대 이상이 되면 Fess 설정을 바꾸지 않아도 각 샤드에 복제본이 1개 만들어집니다.
클러스터 상태가 ``green``\ 이 되면 모든 복제본이 배치된 것입니다.

샤드 수는 인덱스를 생성한 시점에 정해지며, 나중에 ``index.number_of_shards``\ 를 바꿔도 기존 인덱스에는 반영되지 않습니다.
바꾸려면 [시스템 정보] > [유지보수]의 "재인덱싱"을 사용합니다.
"샤드 수"와 "최대 복제본 수"를 지정하고 "에일리어스 갱신"을 활성화해 시작하면, 새 인덱스를 만들어 문서를 복사하고 ``fess.search``\ 와 ``fess.update`` 별칭을 새 인덱스로 바꿔 붙입니다.

재인덱싱에는 다음과 같은 주의점이 있습니다.

- 문서는 시작한 시점에 ``fess.update``\ 가 가리키는 인덱스에서 복사됩니다. 크롤링이 동작하지 않는 시간대에 실행하십시오
- 오래된 인덱스는 자동으로 삭제되지 않습니다. 디스크에는 신구 인덱스가 모두 들어갈 용량이 필요합니다

화면 항목은 `유지보수 <https://fess.codelibs.org/ko/stable/admin/maintenance-guide.html>`__\ 를 참조하십시오.

클러스터 확인
-------------

::

    $ curl -s 'http://search01:9200/_cat/nodes?v&h=name,node.role,cluster_manager,heap.percent'
    $ curl -s 'http://search01:9200/_cluster/health?pretty'

3대가 표시되고 ``status``\ 가 ``green``\ 이면 완성입니다.
Fess의 ``/api/admin/stats``\ 에서도 ``response.stats.engine.number_of_nodes``\ 와 ``response.stats.engine.status``\ 로 같은 내용을 확인할 수 있습니다.

Fess를 여러 대로 늘리기
=======================

검색 사용자가 늘어 Fess 본체의 CPU가 부족해진 경우나 Fess 자체를 이중화하고 싶은 경우에는 같은 OpenSearch에 여러 Fess를 연결합니다.
참고로 docker-fess의 ``compose/multi-instance/``\ 는 Fess마다 별도 인덱스를 사용하는, 독립된 검색 서비스를 나란히 두는 구성으로, 여기서 설명하는 구성과는 다릅니다(조직별로 나누는 경우는 :doc:`guide-13`).

크롤링 설정, 사용자, 작업, 작업 로그는 OpenSearch에 저장되므로 어느 Fess에서 보아도 같습니다.
반면 다음 항목은 Fess 서버마다 있으므로 모든 서버에서 맞춰야 합니다.

- [시스템] > [일반]의 설정(각 서버의 ``system.properties``). 설정 화면에서 바꾸면 그 서버의 값만 바뀝니다
- ``fess_config.properties``\ 와 ``FESS_HEAP_SIZE`` 등의 환경 변수
- 설치한 플러그인
- ``fess_config.properties``\ 의 ``app.cipher.key``. 크롤링 설정이나 데이터 스토어 설정의 파라미터 가운데 이름이 ``password``, ``key``, ``token``, ``secret`` 등으로 끝나는 값은 이 키로 암호화되어 OpenSearch에 저장됩니다. 서버마다 키가 다르면 다른 서버에서 저장한 값을 복호화할 수 없습니다

크롤링을 담당할 서버 정하기
---------------------------

기본 작업은 모두 "대상"이 ``all``\ 입니다.
``all``\ 은 어느 Fess에서나 일치하므로, 그대로 두면 "Default Crawler"가 모든 서버에서 같은 시각에 동작합니다.

크롤링을 1대에 맡기려면 다음 2가지를 모두 수행합니다.

1. 크롤링을 담당할 서버에서만 ``fess_config.properties``\ 에 ``scheduler.target.name=crawler``\ 처럼 식별 이름을 적고 재시작합니다. Docker에서는 ``FESS_JAVA_OPTS``\ 에 ``-Dfess.config.scheduler.target.name=crawler``\ 를 지정할 수 있습니다. 다른 서버는 비워 둡니다
2. [시스템] > [스케줄러]에서 "Default Crawler"를 열고 "대상"을 ``all``\ 에서 ``crawler``\ 로 바꿔 저장합니다. [새 작업 작성]으로 만든 크롤링 작업도 같은 방식으로 바꿉니다

"대상"에는 쉼표로 구분해 여러 식별 이름을 적을 수 있습니다.
절차 1만 수행하면 작업은 지금까지처럼 모든 서버에서 동작합니다.
절차 2만 수행하면 식별 이름이 일치하는 서버가 없으므로 크롤링은 어느 서버에서도 동작하지 않게 됩니다.
절차 1이 반영되었는지는 크롤링을 담당하는 서버의 [시스템 정보] > [설정 정보]의 "앱 속성"에서 ``scheduler.target.name`` 값을 보고 확인합니다.

크롤링 이외의 작업(로그 집계나 오래된 문서 삭제 등)은 "대상"을 ``all``\ 로 그대로 둡니다.

고정한 후에는 [지금 시작]도 크롤링을 담당하는 서버의 관리 화면에서 누릅니다.
다른 서버에서 누르면 화면에는 시작했다고 표시되지만 그 서버에서는 실행되지 않고, ``fess.log``\ 에 ``Ignoring job``\ 이 기록될 뿐입니다.
로드 밸런서 아래에 있는 경우에는 크롤링을 담당하는 서버에 직접 접근할 수 있는 경로를 마련해 둡니다.

로드 밸런서 설정
----------------

Fess 15.9의 로그인 세션은 각 Fess의 메모리에 저장됩니다.
로그인해서 사용하는 검색 화면이나 관리 화면을 로드 밸런서로 분산하는 경우에는 같은 사용자를 계속 같은 서버로 보내는 스티키 세션을 활성화합니다.
세션을 OpenSearch에 저장해 서버 간에 공유하는 기능은 15.10 이후에 사용할 수 있습니다.

로드 밸런서의 헬스 체크에는 ``/api/v2/health``\ 를 사용할 수 있습니다.
OpenSearch 클러스터가 ``RED``\ 인 경우와 OpenSearch에 접속할 수 없는 경우에는 503을 반환합니다.

유지보수 작업의 배타 제어
-------------------------

[시스템 정보] > [유지보수]의 "재인덱싱", "문서 인덱스 다시 로드", "크롤링용 인덱스 삭제", "설정 인덱스 재구축"은 여러 대의 Fess에서 동시에 실행되지 않도록 배타 제어됩니다.
다른 서버에서 실행 중인 경우에는 "<호스트명>에서 작업이 이미 실행 중입니다."라고 표시됩니다.
이 배타 제어는 유지보수 작업만 대상으로 하며, 작업이나 [일반] 설정을 서버 간에 조정하는 것은 아닙니다.

규모 기준에 대하여
==================

문서 수나 사용자 수만으로 필요한 구성이 정해지지는 않습니다.
문서 1건당 본문 길이, 첨부 파일의 비율, 검색어의 경향, 로그인해서 사용하는지 여부에 따라 필요한 메모리와 CPU가 크게 달라지기 때문입니다.

다음과 같이 측정한 값으로 판단하십시오.

- 인덱스의 ``store.size``\ 로부터 `메모리 설정 <https://fess.codelibs.org/ko/stable/config/setup-memory.html>`__\ 의 기준표를 보고 OpenSearch의 힙을 정한다
- 검색 로그의 p95가 나빠지고 ``_cat/nodes``\ 의 힙 사용률이나 CPU가 높은 상태로 유지되면 OpenSearch의 힙이나 노드를 늘린다
- 작업 로그의 크롤링 시간이 길어지고 ``Cpu Load`` 로그가 나온다면 OpenSearch를 별도 서버로 분리한다
- OpenSearch에 여유가 있는데 Fess 본체의 CPU가 높다면 Fess를 여러 대로 늘린다

다음에 읽을 글
==============

- 모니터링, 로그, 백업을 갖춰 운영 환경에서 사용하고 싶다: :doc:`guide-10`
- OpenSearch의 공개 범위와 로그인을 포함해 접근을 보호하고 싶다: :doc:`guide-15`
- 여러 대의 설정을 맞추는 작업을 코드로 관리하고 싶다: :doc:`guide-16`
- 하나의 Fess를 조직별로 나누어 사용하고 싶다: :doc:`guide-13`
- 전개 단계별로 확인할 사항을 정리하고 싶다: :doc:`guide-23`

참고 자료
=========

- `메모리 설정 <https://fess.codelibs.org/ko/stable/config/setup-memory.html>`__
- `포트 및 네트워크 설정 <https://fess.codelibs.org/ko/stable/config/setup-port-network.html>`__
- `부하 제어 설정 <https://fess.codelibs.org/ko/stable/config/load-control.html>`__
- `Linux 설치 (상세 절차) <https://fess.codelibs.org/ko/stable/install/install-linux.html>`__
- `Docker 설치 (상세) <https://fess.codelibs.org/ko/stable/install/install-docker.html>`__
- `fess-setup 명령 <https://fess.codelibs.org/ko/stable/install/fess-setup.html>`__
- `유지보수 <https://fess.codelibs.org/ko/stable/admin/maintenance-guide.html>`__
- `스케줄러 <https://fess.codelibs.org/ko/stable/admin/scheduler-guide.html>`__
- `검색 로그 <https://fess.codelibs.org/ko/stable/admin/searchlog-guide.html>`__
- `Stats API <https://fess.codelibs.org/ko/stable/api/admin/api-admin-stats.html>`__
- `인덱스 관리 <https://fess.codelibs.org/ko/stable/config/admin-index-backup.html>`__
