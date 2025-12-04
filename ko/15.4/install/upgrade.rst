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

- Fess 14.x → Fess 15.4
- Fess 15.x → Fess 15.4

.. note::

   더 오래된 버전(13.x 이전)에서 업그레이드하는 경우 단계적 업그레이드가 필요할 수 있습니다.
   자세한 내용은 릴리스 노트를 확인하십시오.

업그레이드 전 준비
====================

버전 호환성 확인
--------------------

업그레이드 대상 버전과 현재 버전의 호환성을 확인하십시오.

- `릴리스 노트 <https://github.com/codelibs/fess/releases>`__
- `업그레이드 가이드 <https://fess.codelibs.org/ko/>`__

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

   관리 화면에 로그인하여 "시스템"→"백업"을 클릭합니다.

   다음 파일을 다운로드:

   - ``fess_basic_config.bulk``
   - ``fess_user.bulk``

2. **설정 파일 백업**

   TAR.GZ/ZIP 버전::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/

   RPM/DEB 버전::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/

3. **커스터마이징한 설정 파일**

   커스터마이징한 설정 파일이 있는 경우 해당 파일도 백업합니다::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/

인덱스 데이터 백업
------------------------------

OpenSearch의 인덱스 데이터를 백업합니다.

방법 1: 스냅샷 기능 사용(권장)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenSearch의 스냅샷 기능을 사용하여 인덱스를 백업합니다.

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

Docker 볼륨을 백업합니다::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ docker run --rm -v fess-es-data:/data -v $(pwd):/backup ubuntu tar czf /backup/fess-es-data-backup.tar.gz /data
    $ docker run --rm -v fess-data:/data -v $(pwd):/backup ubuntu tar czf /backup/fess-data-backup.tar.gz /data
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

단계 2: 현재 버전 중지
================================

Fess와 OpenSearch를 중지합니다.

TAR.GZ/ZIP 버전::

    $ kill <fess_pid>
    $ kill <opensearch_pid>

RPM/DEB 버전 (systemd)::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker 버전::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

단계 3: 새 버전 설치
======================================

설치 방법에 따라 절차가 다릅니다.

TAR.GZ/ZIP 버전
-----------

1. 새 버전 다운로드 및 압축 해제::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.4.0/fess-15.4.0.tar.gz
       $ tar -xzf fess-15.4.0.tar.gz

2. 이전 버전 설정 복사::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.4.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.4.0/bin/

3. 설정 차이를 확인하고 필요에 따라 조정합니다

RPM/DEB 버전
--------

새 버전 패키지를 설치::

    # RPM
    $ sudo rpm -Uvh fess-15.4.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.4.0.deb

.. note::

   설정 파일(``/etc/fess/*``)은 자동으로 유지됩니다.
   단, 새로운 설정 옵션이 추가된 경우 수동으로 조정이 필요합니다.

Docker 버전
-------

1. 새 버전의 Compose 파일 가져오기::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.4.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.4.0/compose/compose-opensearch3.yaml

2. 새 이미지 가져오기::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

단계 4: OpenSearch 업그레이드(필요한 경우)
=================================================

OpenSearch도 업그레이드하는 경우 다음 절차를 따르십시오.

.. warning::

   OpenSearch의 메이저 버전 업그레이드는 신중하게 수행하십시오.
   인덱스 호환성에 문제가 발생할 수 있습니다.

1. 새 버전의 OpenSearch 설치

2. 플러그인 재설치::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.1

3. OpenSearch 시작::

       $ sudo systemctl start opensearch.service

단계 5: 새 버전 시작
================================

TAR.GZ/ZIP 버전::

    $ cd /path/to/fess-15.4.0
    $ ./bin/fess -d

RPM/DEB 버전::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Docker 버전::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

단계 6: 동작 확인
==================

1. **로그 확인**

   오류가 없는지 확인합니다::

       $ tail -f /path/to/fess/logs/fess.log

2. **웹 인터페이스 액세스**

   브라우저에서 http://localhost:8080/ 에 액세스합니다.

3. **관리 화면 로그인**

   http://localhost:8080/admin 에 액세스하여 관리자 계정으로 로그인합니다.

4. **시스템 정보 확인**

   관리 화면에서 "시스템"→"시스템 정보"를 클릭하여 버전이 업데이트되었는지 확인합니다.

5. **검색 동작 확인**

   검색 화면에서 검색을 실행하여 정상적으로 결과가 반환되는지 확인합니다.

단계 7: 인덱스 재작성(권장)
====================================

메이저 버전 업그레이드의 경우 인덱스를 재작성할 것을 권장합니다.

1. 기존 크롤 일정 확인
2. "시스템"→"스케줄러"에서 "Default Crawler" 실행
3. 크롤이 완료될 때까지 대기
4. 검색 결과 확인

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

단계 4: 서비스 시작 및 확인
----------------------------

::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

동작을 확인하고 정상적으로 복구되었는지 확인합니다.

자주 묻는 질문
==========

Q: 다운타임 없이 업그레이드할 수 있습니까?
--------------------------------------------

A: Fess의 업그레이드에는 서비스 중지가 필요합니다. 다운타임을 최소화하려면 다음을 고려하십시오:

- 사전에 테스트 환경에서 절차를 확인
- 백업을 사전에 취득
- 유지보수 시간을 충분히 확보

Q: OpenSearch도 업그레이드해야 합니까?
-------------------------------------------------

A: Fess 버전에 따라 특정 버전의 OpenSearch가 필요합니다.
릴리스 노트에서 권장되는 OpenSearch 버전을 확인하십시오.

Q: 인덱스를 재작성해야 합니까?
------------------------------------------

A: 마이너 버전 업그레이드의 경우 일반적으로 불필요하지만 메이저 버전 업그레이드의 경우 재작성을 권장합니다.

Q: 업그레이드 후 검색 결과가 표시되지 않습니다
------------------------------------------

A: 다음을 확인하십시오:

1. OpenSearch가 시작되어 있는지 확인
2. 인덱스가 존재하는지 확인(``curl http://localhost:9200/_cat/indices``)
3. 크롤 재실행

다음 단계
==========

업그레이드가 완료되면:

- :doc:`run` - 시작 및 초기 설정 확인
- :doc:`security` - 보안 설정 검토
- 릴리스 노트에서 새 기능 확인
