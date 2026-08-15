====================
업그레이드 절차
====================

이 페이지에서는 |Fess| 를 이전 버전에서 최신 버전으로 업그레이드하는 절차에 대해 설명합니다.

.. warning::

   **업그레이드 전 중요한 주의사항**

   - 업그레이드 전에 반드시 백업을 취득하십시오
   - 테스트 환경에서 사전에 업그레이드를 검증할 것을 강력히 권장합니다
   - 업그레이드 중에는 서비스가 중지되므로 적절한 유지보수 시간을 설정하십시오
   - 버전에 따라 설정 파일 형식이 변경된 경우가 있습니다

대응 버전
============

이 업그레이드 절차는 다음 버전 간의 업그레이드에 대응합니다:

- Fess 14.x → Fess 15.8
- Fess 15.x → Fess 15.8

.. important::

   |Fess| 14.x는 OpenSearch 2.x 계열, |Fess| 15.8은 OpenSearch 3.8.0에 대응합니다.
   |Fess| 용 OpenSearch 플러그인은 OpenSearch 버전과 완전히 일치해야 하므로,
   14.x에서 업그레이드하는 경우 OpenSearch의 메이저 버전 업그레이드도 필수입니다.
   :ref:`upgrade-opensearch` 를 참조하십시오.

.. note::

   더 오래된 버전(13.x 이전)에서 업그레이드하는 경우 단계적 업그레이드가 필요할 수 있습니다.
   자세한 내용은 릴리스 노트를 확인하십시오.

업그레이드 전 준비
====================

버전 호환성 확인
--------------------

업그레이드 대상 버전과 현재 버전의 호환성을 확인하십시오.

- `릴리스 노트 <https://github.com/codelibs/fess/releases>`__
- :doc:`prerequisites` - |Fess| 15.8의 동작 환경(Java, OpenSearch 버전)

다운타임 계획
----------------

업그레이드 작업에는 시스템 중지가 필요합니다. 다음을 고려하여 다운타임을 계획하십시오:

- 백업 시간: 10분 ~ 수 시간(데이터 양에 따라)
- 업그레이드 시간: 10 ~ 30분
- 동작 확인 시간: 30분 ~ 1시간
- 예비 시간: 30분

**권장 유지보수 시간**: 총 2 ~ 4시간

단계 1: 데이터 백업
==============================

업그레이드 전에 모든 데이터를 백업하십시오.

설정 데이터 백업
----------------------

1. **관리 화면에서 백업**

   관리 화면에 로그인하여 「시스템 정보」→「백업」을 클릭합니다.

   백업 페이지에는 다음 설정 데이터가 항목별로 목록 표시됩니다.
   각 행을 클릭하여 다운로드합니다(단일 ZIP 파일이 아니라 항목별 개별 파일입니다.
   일괄 다운로드 기능은 없으므로 필요한 항목을 하나씩 다운로드합니다).

   - ``fess_basic_config.bulk`` - 설정 인덱스(크롤 설정, 스케줄러, 레이블,
     키 매치, 역할, 웹/파일 인증 등 19개 인덱스)
   - ``fess_config.bulk`` - 위 19개 인덱스에 더해 크롤 정보, 장애 URL, 작업 로그,
     썸네일 큐 등 실행 시 데이터를 포함하는 25개 인덱스
   - ``fess_user.bulk`` - 사용자, 역할, 그룹
   - ``system.properties`` - 전반 설정을 포함하는 시스템 설정
   - ``fess.json`` - 인덱스 설정(샤드 수, ``index.knn`` 등)
   - ``doc.json`` - 문서 매핑(필드 정의)

   .. note::

      ``fess_config.bulk`` 는 ``fess_basic_config.bulk`` 를 포함합니다. 업그레이드 전
      설정 백업으로는 ``fess_basic_config.bulk``, ``fess_user.bulk``,
      ``system.properties`` 3개면 충분합니다.

   .. note::

      검색 로그나 클릭 로그 등의 로그 데이터(``search_log.ndjson``, ``click_log.ndjson``,
      ``favorite_log.ndjson``, ``user_info.ndjson``)도 같은 페이지에서 다운로드할 수 있습니다.
      설정만 백업하는 경우에는 불필요합니다. 또한 이 ``*.ndjson`` 파일들은
      백업 페이지에서 업로드하여 복원할 수 없습니다
      (「롤백 절차」 참조).

2. **설정 파일 백업**

   TAR.GZ/ZIP 버전::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/
       $ cp /path/to/fess/bin/fess.in.sh /backup/

   RPM 버전::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/
       $ sudo cp /etc/sysconfig/fess /backup/

   DEB 버전::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/
       $ sudo cp /etc/default/fess /backup/

   .. note::

      ``/etc/sysconfig/fess`` (RPM 버전)와 ``/etc/default/fess`` (DEB 버전)는
      ``FESS_PORT``, ``FESS_HEAP_SIZE``, ``SEARCH_ENGINE_HTTP_URL``,
      ``FESS_DICTIONARY_PATH`` 등을 지정하는 환경 변수 파일입니다.
      TAR.GZ/ZIP 버전에서 이에 해당하는 설정은 ``bin/fess.in.sh`` 에 있습니다.

3. **커스터마이징한 설정 파일**

   커스터마이징한 설정 파일이 있는 경우 해당 파일도 백업합니다::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/

   .. note::

      ``app/WEB-INF/classes/log4j2.xml`` 은 |Fess| 본체(Web) 프로세스의 로그 설정입니다.
      크롤러 등의 자식 프로세스는 별도의 파일
      (``app/WEB-INF/env/crawler/resources/log4j2.xml`` 등 ``crawler``, ``suggest``,
      ``thumbnail``, ``chunk`` 총 4개)을 사용하므로, 이를 변경한 경우에는
      함께 백업하십시오.

인덱스 데이터 백업
------------------------------

OpenSearch의 인덱스 데이터를 백업합니다.

방법 1: 스냅샷 기능 사용(권장)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenSearch의 스냅샷 기능을 사용하여 인덱스를 백업합니다.

.. note::

   파일 시스템 리포지토리(``fs``)를 등록하려면 사전에 OpenSearch의 ``opensearch.yml`` 의
   ``path.repo`` 에 백업 대상 디렉터리를 지정하고 OpenSearch를 재시작해 두어야 합니다.

1. 리포지토리 설정::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup" -H 'Content-Type: application/json' -d'
       {
         "type": "fs",
         "settings": {
           "location": "/backup/opensearch/snapshots"
         }
       }'

2. 스냅샷 생성::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup/snapshot_1?wait_for_completion=true"

3. 스냅샷 확인::

       $ curl -X GET "http://localhost:9200/_snapshot/fess_backup/snapshot_1"

방법 2: 디렉터리별 백업
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenSearch를 중지한 후 데이터 디렉터리를 백업합니다.

::

    $ sudo systemctl stop opensearch
    $ sudo tar czf /backup/opensearch-data-$(date +%Y%m%d).tar.gz /var/lib/opensearch/data
    $ sudo systemctl start opensearch

Docker 버전 백업
---------------------

OpenSearch의 데이터는 Docker 볼륨에 저장됩니다. ``compose-opensearch3.yaml`` 에는
인덱스 데이터용 ``search01_data`` 와 사전 파일용 ``search01_dictionary`` 의
2개 볼륨이 정의되어 있습니다.

.. note::

   실제 볼륨 이름에는 Compose 프로젝트 이름(기본값은 Compose 파일을 배치한
   디렉터리 이름)이 접두사로 부여됩니다. 정확한 이름은 다음 명령으로 확인하십시오::

       $ docker volume ls

컨테이너를 중지한 후 볼륨을 백업합니다. ``docker run`` 의 ``-v`` 에는
접두사를 포함한 실제 볼륨 이름을 지정합니다::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ PROJECT=$(basename "$(pwd)")
    $ docker run --rm -v ${PROJECT}_search01_data:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-data-backup.tar.gz /data
    $ docker run --rm -v ${PROJECT}_search01_dictionary:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-dictionary-backup.tar.gz /data
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

.. warning::

   ``-v`` 에 접두사 없이 ``search01_data`` 를 지정하면 Docker는 기존 볼륨을 참조하지 않고
   같은 이름의 빈 볼륨을 새로 생성합니다. 명령은 오류 없이 실행되고 내용이 빈 아카이브가
   생성되므로, 마치 백업이 정상적으로 취득된 것처럼 보일 수 있습니다.

.. note::

   |Fess| 본체(``fess01``) 컨테이너에는 전용 볼륨이 없으므로 백업 대상은
   위 2개뿐입니다. 다만 관리 화면에서 변경한 전반 설정이나 관리 화면에서 설치한
   플러그인은 컨테이너 내부에만 저장되며, 컨테이너를 재생성하면 유실됩니다.
   이러한 항목은 Compose 파일의 ``FESS_JAVA_OPTS`` 나 ``FESS_PLUGINS`` 로 지정하여 영속화하십시오.

단계 2: 현재 버전 중지
================================

Fess와 OpenSearch를 중지합니다.

TAR.GZ/ZIP 버전에는 중지용 스크립트가 포함되어 있지 않습니다. ``bin/fess`` 를 ``-p`` 옵션과 함께
실행한 경우에는 PID 파일을 사용하여 중지합니다::

    $ kill $(cat /path/to/fess/fess.pid)
    $ kill <opensearch_pid>

``-p`` 를 지정하지 않고 실행한 경우에는 프로세스 ID를 확인하여 ``kill`` 합니다
(``-d`` 만으로는 PID 파일이 생성되지 않습니다).

RPM/DEB 버전 (systemd)::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker 버전::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

단계 3: 새 버전 설치
======================================

설치 방법에 따라 절차가 다릅니다.

TAR.GZ/ZIP 버전
---------------

1. 새 버전을 다운로드하여 압축을 해제합니다::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.8.0/fess-15.8.0.zip
       $ unzip fess-15.8.0.zip

   .. note::

      |Fess| 의 아카이브 버전은 ZIP 형식으로만 배포됩니다(``fess-15.8.0.tar.gz`` 는
      제공되지 않습니다).

2. 이전 버전의 설정을 복사합니다::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.8.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.8.0/app/WEB-INF/classes/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.8.0/bin/

3. 커스터마이징한 경우에는 다음도 복사합니다::

       # 로그 설정
       $ cp /path/to/old-fess/app/WEB-INF/classes/log4j2.xml /path/to/fess-15.8.0/app/WEB-INF/classes/
       # 설치된 플러그인
       $ cp -r /path/to/old-fess/app/WEB-INF/plugin/. /path/to/fess-15.8.0/app/WEB-INF/plugin/
       # 테마
       $ cp -r /path/to/old-fess/app/themes/. /path/to/fess-15.8.0/app/themes/

   .. warning::

      관리 화면 「디자인」에서 편집한 JSP(``app/WEB-INF/view/``)는 그대로 복사하지 마십시오.
      새 버전의 JSP와 구조가 달라진 경우 화면이 올바르게 표시되지 않을 수 있습니다.
      새 버전의 JSP에 변경 내용을 다시 적용하십시오.

4. 임베디드 OpenSearch(``SEARCH_ENGINE_HTTP_URL`` 을 설정하지 않고 ``bin/fess`` 를 실행하는 구성)를
   사용하는 경우에는 인덱스 데이터도 복사합니다::

       $ cp -r /path/to/old-fess/es/data/. /path/to/fess-15.8.0/es/data/

5. 설정 차이를 확인하고 필요에 따라 조정합니다

RPM/DEB 버전
------------

새 버전 패키지를 설치::

    # RPM
    $ sudo rpm -Uvh fess-15.8.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.8.0.deb

.. note::

   RPM 버전에서는 ``/etc/fess/*`` 의 설정 파일이 ``%config(noreplace)`` 로 등록되어 있으므로
   업그레이드 시에도 유지됩니다(새 기본 파일은 ``.rpmnew`` 로 함께 배치됩니다).
   새로운 설정 옵션이 추가된 경우에는 수동으로 조정이 필요합니다.

.. warning::

   DEB 버전에서는 ``/etc/fess/*`` 가 conffile로 등록되어 있지 않습니다(conffile은
   ``/etc/default/fess``, ``/etc/init.d/fess``, ``/usr/lib/systemd/system/fess.service``
   3개뿐입니다). 따라서 ``dpkg -i`` 를 실행하면 ``/etc/fess/fess_config.properties`` 등이
   새 버전의 파일로 덮어써집니다. 단계 1에서 백업한 설정을
   업그레이드 후에 다시 적용하십시오.
   또한 ``/etc/fess/system.properties`` 는 패키지에 포함되지 않는 실행 시 생성 파일이므로
   덮어써지지 않습니다.

Docker 버전
-----------

1. 새 버전의 Compose 파일 가져오기::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose-opensearch3.yaml

2. 새 이미지 가져오기::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

.. _upgrade-opensearch:

단계 4: OpenSearch 업그레이드
====================================

|Fess| 15.8은 OpenSearch 3.8.0에 대응합니다. 연결 대상 OpenSearch가 이보다 오래된 경우
다음 절차에 따라 업그레이드하십시오.

.. note::

   이 절차는 TAR.GZ/ZIP 버전 및 RPM/DEB 버전에서 OpenSearch를 수동으로 운용하는 경우의 절차입니다.
   Docker 버전에서는 단계 3에서 새 이미지를 가져오면 OpenSearch와 플러그인도
   함께 업데이트되므로 이 단계는 불필요합니다.

.. important::

   |Fess| 15.8은 청크 벡터 검색(시맨틱 검색) 사용 여부와 관계없이 검색 인덱스 설정에
   ``index.knn`` 을, 매핑에 ``content_chunk_vector`` (``knn_vector`` 타입)를 항상
   포함합니다. 따라서 연결 대상 OpenSearch에는 **k-NN 플러그인이 필수** 입니다.

   - 표준 배포판 OpenSearch 및 Docker 버전의 이미지에는 동봉되어 있습니다.
   - **minimal 배포판에는 포함되어 있지 않으므로 인덱스를 새로 생성하지 못해 |Fess| 가
     시작되지 않습니다.**
   - 인덱스 설정에는 ``knn.derived_source.enabled`` 도 항상 전송됩니다. 이를 인식하지 못하는
     오래된 OpenSearch에서는 k-NN 플러그인 유무와 관계없이 인덱스 생성에 실패합니다.

   자세한 내용은 :doc:`../config/search-semantic` 의 「전제 조건」을 참조하십시오.

.. warning::

   OpenSearch의 메이저 버전 업그레이드는 신중하게 수행하십시오.
   인덱스 호환성에 문제가 발생할 수 있습니다.
   |Fess| 14.x는 OpenSearch 2.x 계열이므로, 14.x에서의 업그레이드는 반드시 이 경우에 해당합니다.

1. 새 버전의 OpenSearch 설치

2. 플러그인 재설치::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.8.0

   .. note::

      이러한 플러그인의 버전은 사용하는 OpenSearch의 버전과 일치시켜야 합니다.
      |Fess| 15.8은 OpenSearch 3.8.0에 대응합니다. 버전이 일치하지 않으면
      플러그인 설치에 실패합니다.

3. OpenSearch 시작::

       $ sudo systemctl start opensearch.service

단계 5: 새 버전 시작
================================

TAR.GZ/ZIP 버전::

    $ cd /path/to/fess-15.8.0
    $ ./bin/fess -d -p /path/to/fess-15.8.0/fess.pid

.. note::

   ``-p`` 를 지정하면 PID 파일이 생성되며, 다음 중지 시
   ``kill $(cat /path/to/fess-15.8.0/fess.pid)`` 로 중지할 수 있습니다.

RPM/DEB 버전::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Docker 버전::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

단계 6: 동작 확인
==================

1. **로그 확인**

   오류가 없는지 확인합니다.

   TAR.GZ/ZIP 버전::

       $ tail -f /path/to/fess/logs/fess.log

   RPM/DEB 버전::

       $ sudo tail -f /var/log/fess/fess.log

   Docker 버전::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

   .. note::

      같은 로그 디렉터리에 크롤 처리의 ``fess-crawler.log``, 인증 및 관리 작업의
      ``audit.log``, 검색 요청의 ``searchlog.log`` 도 출력됩니다.

2. **웹 인터페이스 액세스**

   브라우저에서 http://localhost:8080/ 에 액세스합니다.

3. **관리 화면 로그인**

   http://localhost:8080/admin 에 액세스하여 관리자 계정으로 로그인합니다.

4. **버전 확인**

   관리 화면에서 「시스템 정보」→「설정 정보」를 클릭하여 「시스템 속성」에 표시되는
   ``fess.version`` 이 새 버전으로 되어 있는지 확인합니다.

5. **검색 동작 확인**

   검색 화면에서 검색을 실행하여 정상적으로 결과가 반환되는지 확인합니다.

단계 7: 인덱스 재작성(권장)
====================================

메이저 버전 업그레이드의 경우 인덱스를 재작성할 것을 권장합니다.

.. note::

   아래 단계는 크롤을 다시 실행하는 것으로, 인덱스 매핑(필드 정의)은 업데이트되지 않습니다.
   매핑을 업데이트하는 재인덱스가 필요한 경우 — 예를 들어 청크 벡터 검색(시맨틱 검색)을 새로
   활성화하려는 경우 등 — 는 관리 화면의 「시스템 정보」→「유지보수」에서 「재인덱싱」을 별도로
   실행하세요. 자세한 내용은 :ref:`semantic-search-migration`\ (:doc:`../config/search-semantic`)\ 을
   참조하세요.

1. 기존 크롤 일정 확인
2. 「시스템」→「스케줄러」에서 "Default Crawler" 실행
3. 크롤이 완료될 때까지 대기
4. 검색 결과 확인

.. warning::

   재인덱싱에서는 새로운 매핑으로 인덱스가 다시 생성되므로, k-NN 플러그인이
   없는 OpenSearch에서는 실패합니다. 단계 4의 주의사항을 확인하십시오.

15.8 전용 마이그레이션 작업
===========================

15.7 이전 버전에서 15.8로 업그레이드하는 경우, 사용 중인 기능에 따라 다음 작업이 필요합니다.

시맨틱 검색을 사용하고 있었던 경우
----------------------------------

15.7 이전에 시맨틱 검색을 제공하던 ``fess-webapp-semantic-search`` 플러그인은
15.8에서 코어로 통합되어 불필요해졌습니다(사용 중단). 플러그인 제거, ``-Dfess.semantic_search.*``
및 ``-Drank.fusion.searchers=default,semantic`` 의 제거, 기존 인제스트 파이프라인 분리가
필요합니다. 절차는 :ref:`semantic-search-migration` (:doc:`../config/search-semantic`)를
참조하십시오.

AI 검색 모드(RAG 채팅)를 사용하고 있었던 경우
---------------------------------------------

15.8부터 AI 검색 모드(RAG 채팅) 기능은 ``fess-llm-ollama``, ``fess-llm-openai``,
``fess-llm-gemini`` 등의 플러그인으로 분리되었습니다. 사용 중인 프로바이더에 대응하는
플러그인을 관리 화면 「시스템」→「플러그인」에서 설치하십시오.

SPNEGO(Windows 통합 인증)를 사용하고 있었던 경우
------------------------------------------------

15.8부터 클라이언트 주체의 Kerberos 영역이 서버의 영역과 다르면 SPNEGO 로그인이 거부됩니다.
AD 도메인 트리의 하위 도메인이나 신뢰 관계를 맺은 포리스트의 사용자가 로그인하는 구성에서는
관리 화면 「시스템」→「일반」 또는 ``app/WEB-INF/conf/system.properties`` 의
``spnego.allowed.realms`` 에 해당 영역을 쉼표로 구분하여 나열하십시오. 나열하지 않으면
15.7까지 로그인할 수 있었던 사용자가 ``Kerberos realm is not allowed`` 로 거부됩니다.
자세한 내용은 :doc:`../config/sso-spnego` 를 참조하십시오.

또한 15.8에서는 ``spnego.allow.unsecure.basic`` 과 ``spnego.allow.localhost`` 의 코드상 기본값이
``true`` 에서 ``false`` 로 변경되었습니다. 이 키들이 ``app/WEB-INF/conf/system.properties`` 에
없는 환경에서는 업그레이드와 함께 더 엄격한 동작이 적용됩니다. 특히
``spnego.allow.unsecure.basic=false`` 인 경우 SPNEGO 라이브러리는 ``HttpServletRequest#isSecure()``
가 ``true`` 를 반환하는 요청에만 Basic 인증을 제공하므로, 리버스 프록시에서 TLS를 종료하고 HTTP로
전달하는 구성에서는 지금까지 Basic 인증으로 대체하던 클라이언트가 로그인할 수 없게 됩니다.
이 경우 ``tomcat_config.properties`` 에서 ``tomcat.secure=true`` 를 설정하십시오.
자세한 내용은 :doc:`../config/sso-spnego` 를 참조하십시오.

.. warning::

   코드상의 기본값은 키가 없는 경우에만 적용되며, 관리 화면 「시스템」→「일반」은 저장할 때마다
   모든 ``spnego.*`` 키를 기록합니다. 따라서 15.7에서 이 화면으로 한 번이라도 갱신한 환경에는
   ``spnego.allow.unsecure.basic=true`` 와 ``spnego.allow.localhost=true`` 가 저장된 채로 남아
   있으며, 15.8로 업그레이드해도 설정은 강화되지 않습니다. 느슨한 동작이 조용히 유지되고, 15.8은
   SPNEGO 초기화 시 ``fess.log`` 에 경고를 기록할 뿐입니다. 관리 화면 「시스템」→「일반」 또는
   ``system.properties`` 에서 두 가지를 모두 명시적으로 비활성화하십시오. 특히
   ``spnego.allow.localhost=true`` 는 위험합니다. SPNEGO 라이브러리가 동일 호스트에서 온 요청을
   Kerberos 검증 없이 서버의 OS 사용자로 인증하므로, 동일 호스트에 리버스 프록시를 두는 구성에서는
   안전하지 않습니다.

SAML 인증(SSO)을 사용하고 있었던 경우
-------------------------------------

15.8부터 |Fess| 는 전송한 AuthnRequest의 ID와 SAML 응답을 대응시켜 검증하므로
IdP-Initiated(미요청·unsolicited) SSO는 동작하지 않습니다. IdP 포털(Okta 대시보드나
Microsoft Entra ID의 「내 앱」 등)에 배치한 타일에서 시작한 로그인은 대응시킬 AuthnRequest가
없어 거부됩니다. 15.7까지는 |Fess| 가 대응시키지 못한 응답을 IdP로 되돌려 보내고, IdP가 즉시
SP-Initiated 어서션을 반환했기 때문에 동작했습니다. IdP 측에 타일을 배치하는 경우에는 링크
대상을 |Fess| 의 ``/sso/`` 로 지정하여 SP-Initiated 로그인이 되도록 하십시오.

또한 IdP는 어서션을 크로스 사이트 POST로 반환하므로 ``tomcat_config.properties`` 의
``tomcat.sameSiteCookies`` 를 ``none`` 으로 설정해야 합니다. 포함된 기본값 ``lax`` 그대로는
세션 쿠키가 이 요청에 전송되지 않아 SAML 로그인을 완료할 수 없습니다. 이 파일은 ZIP 패키지에서는
``lib/classes/`` , DEB/RPM 패키지에서는 ``/etc/fess/`` 에 있으며, 변경 후에는 |Fess| 를
재시작해야 합니다. 브라우저는 ``Secure`` 속성이 함께 있는 쿠키에 대해서만 ``none`` 을
허용하므로 |Fess| 를 HTTPS로 제공해야 합니다. 15.7까지는 같은 설정 오류가 명확한 오류가 아니라
IdP로의 무한 리다이렉트 루프로 나타났으므로, 동작하는 것처럼 보였던 사이트에서도 설정을
확인하십시오. 15.8에서는 루프에 빠지지 않고 한 번에 실패합니다.
자세한 내용은 :doc:`../config/sso-saml` 을 참조하십시오.

Microsoft Entra ID(Azure AD)를 사용하고 있었던 경우
---------------------------------------------------

15.8부터 인가 엔드포인트에 요청하는 응답 모드의 기본값이 ``form_post`` 에서 ``query`` 로
변경되었습니다. 15.7까지는 콜백이 교차 사이트 POST로 반환되므로, |Fess| 의 기본값인
``tomcat.sameSiteCookies = lax`` 에서는 세션 쿠키가 전송되지 않아 ``none`` 으로 변경해야
했습니다. 이 회피책만을 위해 ``none`` 을 설정했다면 기본값으로 되돌릴 수 있습니다. 기존과 같이
``form_post`` 를 사용하려면 ``entraid.response.mode=form_post`` 를 지정하고
``tomcat.sameSiteCookies = none`` 을 유지하십시오. 브라우저는 ``Secure`` 속성이 함께 있는 쿠키에
대해서만 ``none`` 을 허용하므로, 이 경우에도 |Fess| 를 HTTPS로 제공해야 합니다.

또한 15.8부터 |Fess| 는 로그인이 완료된 후 백그라운드에서 사용자의 그룹·역할 소속을 해결하며,
로그인이 Microsoft Graph의 응답을 기다리다 멈추는 일은 없어졌습니다. 해결이 완료될 때까지, 또는
해결이 완전히 성공하지 못한 경우 사용자가 보유하는 것은 사용자 본인의 사용자 수준 권한과
``entraid.default.groups`` 및 ``entraid.default.roles`` 에 설정한 그룹·역할뿐입니다. 둘 다
설정하지 않은 경우（기본 제공 설정값）, 이 시간대의 검색은 한 건도 결과가 나오지 않습니다.
기본 제공 설정값 그대로 만든 크롤 설정으로 크롤링한 문서에는 ``{role}guest`` 가 부여되지만,
로그인한 사용자는 이 역할을 갖고 있지 않기 때문입니다. 해결이 진행되는 동안에는 검색 화면에
그 사실을 알리는 메시지가 표시되며, 완전히 성공하지 못한 경우에는 별도의 메시지가 표시됩니다
（직접 소속 조회와 중첩 그룹 탐색이 모두 성공하지 않는 한 해결은 실패로 처리됩니다）.
액세스 토큰이 갱신될 때마다 해결이 다시 실행되고, 그 후 성공하면 메시지는 사라지므로, 토큰 유효 기간을 넘겨 이어지는 세션에서는 실패가 최종적인
것이 되지는 않습니다. 바로 다시 시도하려면 일단 로그아웃한 후 다시 로그인하십시오.
자세한 내용은 :doc:`../config/sso-entraid` 를 참조하십시오.

백그라운드에서 해결하기 때문에 생기는 영향으로, 해결이 완료될 때까지는 해결된
역할을 아직 알 수 없습니다. 그래서 관리자는 관리 대시보드가 아니라 검색 화면으로 리다이렉트되며,
그 사이에 관리 화면을 열어도 검색 화면으로 되돌아옵니다. 이 시간대는 최대 약 1초의 스케줄링
지연에 더해 Microsoft Graph 호출 자체（직접 소속 조회 1회, 여기에 중첩 그룹을 따라가기 위해
직접 소속 그룹마다 1회씩 순차 실행. 캐시가 없는 경우）가 걸리므로, 사용자가 소속된 그룹 수에
따라 길어집니다. 이 시간대에 접근이 허용되는 일은 없고 거부될 뿐이며,
이 시간대를 넘기기 위한 설정은 필요하지 않습니다. 인가는 같은 세션의 요청마다
다시 평가되므로, 해결이 완료된 후에 다시 열면 다시 로그인하지 않아도 관리 화면에 정상적으로
접근할 수 있습니다.

.. warning::

   이 시간대를 줄이기 위해 |Fess| 의 관리자 역할을 ``entraid.default.roles`` 에 설정해서는
   안 됩니다. 이 속성은 단일 전역 설정으로, |Fess| 는 로그인 시 모든 Entra ID 사용자에게 이를
   적용하고 이후의 해결 때마다 다시 적용하므로, 테넌트의 모든 사용자에게 영구적인 |Fess|
   관리자 권한을 부여하게 됩니다.

플러그인 버전 갱신
------------------------

``app/WEB-INF/plugin/`` 에 설치된 플러그인은 |Fess| 버전에 대응하는
것으로 교체해야 합니다. Docker 버전에서 ``FESS_PLUGINS`` 를 지정하는 경우에는
``fess-ds-wikipedia:15.8.0`` 처럼 버전 부분을 갱신하십시오.

롤백 절차
==============

업그레이드에 실패한 경우 다음 절차로 롤백할 수 있습니다.

단계 1: 새 버전 중지
------------------------------

::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

단계 2: 이전 버전 복원
----------------------------

백업에서 설정 파일과 데이터를 복원합니다.

RPM/DEB 버전의 경우::

    $ sudo rpm -Uvh --oldpackage fess-<old-version>.rpm

또는::

    $ sudo dpkg -i fess-<old-version>.deb

단계 3: 데이터 복원
----------------------

스냅샷에서 복원::

    $ curl -X POST "http://localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true"

또는 백업에서 디렉터리 복원::

    $ sudo systemctl stop opensearch
    $ sudo rm -rf /var/lib/opensearch/data/*
    $ sudo tar xzf /backup/opensearch-data-backup.tar.gz -C /
    $ sudo systemctl start opensearch

Docker 버전에서는 이전 버전의 Compose 파일로 되돌린 후 볼륨의 내용을 복원합니다::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down
    $ PROJECT=$(basename "$(pwd)")
    $ docker run --rm -v ${PROJECT}_search01_data:/data -v $(pwd):/backup ubuntu \
        sh -c "rm -rf /data/* && tar xzf /backup/search01-data-backup.tar.gz -C /"
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   관리 화면에서 다운로드한 설정 데이터는 |Fess| 시작 후 「시스템 정보」→「백업」
   페이지의 업로드 기능으로 다시 임포트하여 복원할 수 있습니다. 업로드할 수 있는 것은
   ``*.bulk``, ``system`` 으로 시작하는 ``*.properties``, ``gsa`` 로 시작하는 ``*.xml``,
   ``fess`` 로 시작하는 ``*.json``, ``doc`` 으로 시작하는 ``*.json`` 뿐이며, 한 번의 조작에 파일 1개입니다.
   검색 로그 등의 ``*.ndjson`` 파일은 받아들여지지 않으며 오류가 됩니다.

.. warning::

   ``fess.json`` 과 ``doc.json`` 의 업로드는 |Fess| 에 동봉된 인덱스 정의
   파일 자체를 덮어씁니다. 업그레이드 후에 이전 버전의 ``fess.json`` 이나
   ``doc.json`` 을 업로드하면 새 버전의 인덱스 설정·매핑이 유실됩니다.
   롤백 목적 이외에는 업로드하지 마십시오.

.. note::

   업로드된 ``system.properties`` 는 메모리에만 로드되며 파일로는
   기록되지 않습니다. 따라서 ``system.properties`` 의 내용은 |Fess| 를 재시작하면 유실됩니다.
   확실히 복원하려면 백업한 파일을 정해진 위치(TAR.GZ/ZIP 버전은
   ``app/WEB-INF/conf/``, RPM/DEB 버전은 ``/etc/fess/``)에 직접 배치한 후 시작하십시오.

.. note::

   임포트는 비동기로 실행되며, 화면에는 시작되었다는 내용만 표시됩니다.
   실제로 성공했는지는 ``fess.log`` 를 확인하십시오.

단계 4: 서비스 시작 및 확인
----------------------------

::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

동작을 확인하고 정상적으로 복구되었는지 확인합니다.

자주 묻는 질문
==============

Q: 다운타임 없이 업그레이드할 수 있습니까?
--------------------------------------------

A: Fess의 업그레이드에는 서비스 중지가 필요합니다. 다운타임을 최소화하려면 다음을 고려하십시오:

- 사전에 테스트 환경에서 절차를 확인
- 백업을 사전에 취득
- 유지보수 시간을 충분히 확보

Q: OpenSearch도 업그레이드해야 합니까?
-------------------------------------------------

A: |Fess| 버전마다 대응하는 OpenSearch 버전이 정해져 있습니다.
|Fess| 15.8은 OpenSearch 3.8.0에 대응합니다.
``opensearch-analysis-fess`` 등의 |Fess| 용 OpenSearch 플러그인은 OpenSearch 버전과
완전히 일치해야 하므로, OpenSearch를 업그레이드하는 경우
대응하는 버전(3.8.0)의 플러그인으로 업데이트하십시오.

또한 |Fess| 15.8은 k-NN 플러그인을 필수로 하며, 인덱스 설정에 ``knn.derived_source.enabled``
를 항상 전송합니다. 오래된 OpenSearch를 그대로 사용하면 새 인덱스 생성에 실패하므로
사실상 OpenSearch의 업그레이드가 필요합니다. 자세한 내용은 단계 4를 참조하십시오.

Q: 인덱스를 재작성해야 합니까?
------------------------------------------

A: |Fess| 의 마이너 버전 업그레이드(15.x → 15.8)에서 청크 벡터 검색을 이용하지 않는 경우는
일반적으로 불필요합니다. 기존 인덱스를 그대로 이용할 수 있으며, ``content_chunker.enabled`` 등은
기본값이 비활성화이므로 동작은 변하지 않습니다.

다음의 경우에는 재작성·재인덱싱이 필요합니다.

- **새로 청크 벡터 검색(시맨틱 검색)을 활성화하는 경우**: 기존 인덱스에는
  새 매핑이 반영되지 않으므로 재인덱싱이 필수입니다. 자세한 내용은
  :ref:`semantic-search-migration` (:doc:`../config/search-semantic`)를 참조하십시오.
- **14.x에서 업그레이드하는 경우**: OpenSearch가 2.x에서 3.x로 메이저 버전 업그레이드
  되므로 인덱스 재작성을 권장합니다.

.. warning::

   인덱스를 새로 생성하는 작업(재인덱싱 포함)은 k-NN 플러그인이 없는
   OpenSearch에서는 실패합니다. 단계 4의 주의사항을 확인하십시오.

Q: 업그레이드 후 검색 결과가 표시되지 않습니다
----------------------------------------------

A: 다음을 확인하십시오:

1. OpenSearch가 시작되어 있는지 확인
2. 인덱스가 존재하는지 확인(``curl http://localhost:9200/_cat/indices``)
3. 크롤 재실행

다음 단계
==========

업그레이드가 완료되면:

- :doc:`run` - 시작 및 초기 설정 확인
- :doc:`security` - 보안 설정 검토
- :doc:`../config/search-semantic` - 청크 벡터 검색(시맨틱 검색) 설정 및 마이그레이션 절차
- 릴리스 노트에서 새 기능 확인
