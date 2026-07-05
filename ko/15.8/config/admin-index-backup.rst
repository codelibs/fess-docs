==================
인덱스 관리
==================

개요
====

|Fess| 에서 다루는 데이터는 OpenSearch의 인덱스로 관리됩니다.
검색 인덱스의 백업과 복원은 시스템의 안정적인 운영에 필수적입니다.
본 섹션에서는 OpenSearch의 스냅샷 기능을 사용한 인덱스의 백업, 복원, 및 이전 절차에 대해 설명합니다.

.. note::
   |Fess| 에는 본 섹션에서 설명하는 OpenSearch 스냅샷을 통한 인덱스 백업과는 별도로, 관리 화면에서 설정 정보(크롤링 설정, 사용자 정보, 시스템 설정 등)를 내보내기/가져오기하는 기능도 있습니다. 설정 정보만 백업하거나 이전하고 싶은 경우는 :doc:`../admin/backup-guide` 를 참조하십시오. OpenSearch 스냅샷은 검색 문서를 포함한 인덱스 전체를 물리적으로 백업하는 용도에 적합합니다.

인덱스 구성
==================

|Fess| 에서는 다음 인덱스가 사용됩니다.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 인덱스 이름
     - 설명
   * - ``fess.{타임스탬프}``
     - 검색 대상 문서의 인덱스. 인덱스 재구축 시 ``fess.{yyyyMMddHHmmssSSS}`` 형식(밀리초 정밀도 타임스탬프)으로 생성되며, ``fess.search`` (검색용) 및 ``fess.update`` (업데이트용) 별칭으로 참조됩니다.
   * - ``fess_config.*``
     - 시스템 설정 정보( ``fess_config.web_config`` , ``fess_config.scheduled_job`` , ``fess_config.data_config`` 등 여러 하위 인덱스로 구성)
   * - ``fess_user.*``
     - 사용자 정보( ``fess_user.user`` , ``fess_user.role`` , ``fess_user.group`` )
   * - ``fess_log.*``
     - 검색 로그 및 클릭 로그 등( ``fess_log.search_log`` , ``fess_log.click_log`` , ``fess_log.favorite_log`` , ``fess_log.user_info`` , ``fess_log.notification_queue`` )
   * - ``fess_crawler.*``
     - 크롤링 처리 중 사용되는 임시 인덱스( ``fess_crawler.queue`` , ``fess_crawler.data`` , ``fess_crawler.filter`` ). 크롤링 완료 후에는 불필요하므로 통상적으로 백업 대상에 포함할 필요가 없습니다.

인덱스 백업 및 복원
====================================

OpenSearch의 스냅샷 기능을 사용하여 인덱스의 백업과 복원을 실행할 수 있습니다.

스냅샷 리포지토리 설정
--------------------------------

먼저 백업 데이터를 저장할 리포지토리를 설정합니다.

**파일 시스템 리포지토리의 경우:**

1. OpenSearch의 설정 파일 (``opensearch.yml``)에 리포지토리 경로를 추가합니다.

::

    path.repo: ["/var/opensearch/backup"]

2. OpenSearch를 재시작합니다.

3. 리포지토리를 등록합니다.

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup" -H 'Content-Type: application/json' -d'
    {
      "type": "fs",
      "settings": {
        "location": "/var/opensearch/backup",
        "compress": true
      }
    }'

.. note::
   |Fess| 의 zip/tar.gz 버전의 기본 설정에서는 OpenSearch가 9201 포트로 시작됩니다( ``fess_config.properties`` 의 ``search_engine.http.url`` ). RPM/DEB 패키지 버전에서는 기본적으로 9200 포트에 연결하도록 설정되어 있습니다(환경 설정 파일 ``/etc/sysconfig/fess`` (RPM) 또는 ``/etc/default/fess`` (DEB)의 ``SEARCH_ENGINE_HTTP_URL`` ). 사용하는 환경에 맞게 포트 번호를 변경하십시오.

**AWS S3 리포지토리의 경우:**

S3를 백업 대상으로 하는 경우 ``repository-s3`` 플러그인을 설치하여 설정합니다.

::

    curl -X PUT "localhost:9201/_snapshot/fess_s3_backup" -H 'Content-Type: application/json' -d'
    {
      "type": "s3",
      "settings": {
        "bucket": "my-fess-backup-bucket",
        "region": "ap-northeast-1",
        "base_path": "fess-snapshots"
      }
    }'

스냅샷 생성(백업)
------------------------------------

모든 인덱스 백업
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

모든 인덱스를 백업합니다.

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_1?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

특정 인덱스 백업
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

특정 인덱스만 백업합니다. 다음은 |Fess| 관련 인덱스( ``fess`` 로 시작하는 인덱스)만을 대상으로 하는 예입니다.

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_fess_only?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

정기 자동 백업
~~~~~~~~~~~~~~~~~~~~~~~~

cron 등을 사용하여 정기적으로 백업을 실행할 수 있습니다.

::

    #!/bin/bash
    DATE=$(date +%Y%m%d_%H%M%S)
    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_${DATE}?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

스냅샷 확인
----------------------

생성된 스냅샷 목록을 확인합니다.

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/_all?pretty"

특정 스냅샷의 상세 정보를 확인합니다.

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/snapshot_1?pretty"

스냅샷에서 복원
------------------------------

모든 인덱스 복원
~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

특정 인덱스 복원
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

검색 대상 문서의 인덱스는 ``fess.{yyyyMMddHHmmssSSS}`` 형식의 이름이 됩니다. ``_cat/indices`` 등으로 실제 인덱스 이름을 확인한 후 복원하십시오.

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101000000000",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

인덱스 이름을 변경하여 복원
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

복원 시 인덱스 이름을 변경할 수도 있습니다.

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101000000000",
      "rename_pattern": "fess\\.(.+)",
      "rename_replacement": "restored_fess.$1",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

.. note::
   검색 대상 문서의 인덱스( ``fess.{타임스탬프}`` )를 복원한 경우, ``fess.search`` 및 ``fess.update`` 별칭이 복원한 인덱스를 가리키고 있는지 반드시 확인하십시오. 스냅샷에는 별칭 정보도 포함되어 있으므로, 모든 인덱스를 그대로의 이름으로 복원한 경우에는 통상적으로 별칭도 복원됩니다. 단, ``rename_pattern`` 으로 인덱스 이름을 변경하여 복원한 경우나 다른 클러스터로 이전한 경우에는 별칭이 올바르게 설정되지 않을 수 있습니다. 그 경우에는 다음과 같이 별칭을 수동으로 재설정하십시오(인덱스 이름은 실제 것으로 교체하십시오).

   ::

       curl -X POST "localhost:9201/_aliases" -H 'Content-Type: application/json' -d'
       {
         "actions": [
           { "add": { "index": "restored_fess.20250101000000000", "alias": "fess.search" } },
           { "add": { "index": "restored_fess.20250101000000000", "alias": "fess.update" } }
         ]
       }'

스냅샷 삭제
----------------------

오래된 스냅샷을 삭제하여 스토리지 용량을 절약할 수 있습니다.

::

    curl -X DELETE "localhost:9201/_snapshot/fess_backup/snapshot_1"

설정 파일 백업
==========================

OpenSearch의 인덱스와는 별도로 다음 설정 파일도 백업하십시오. 설정 파일의 배치 위치는 설치 방법에 따라 다릅니다.

백업 대상 파일
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 파일/디렉터리
     - 설치 방법
     - 설명
   * - ``app/WEB-INF/conf/system.properties``
     - zip/tar.gz
     - 시스템 설정(일반 설정)
   * - ``/etc/fess/system.properties``
     - RPM/DEB
     - 시스템 설정(일반 설정)
   * - ``app/WEB-INF/classes/fess_config.properties``
     - zip/tar.gz
     - |Fess| 의 상세 설정
   * - ``/etc/fess/fess_config.properties``
     - RPM/DEB
     - |Fess| 의 상세 설정
   * - ``app/WEB-INF/classes/log4j2.xml``
     - zip/tar.gz
     - 로그 설정
   * - ``/usr/share/fess/app/WEB-INF/classes/log4j2.xml``
     - RPM/DEB
     - 로그 설정
   * - ``app/WEB-INF/classes/fess_indices/``
     - zip/tar.gz
     - 인덱스 정의 파일
   * - ``/usr/share/fess/app/WEB-INF/classes/fess_indices/``
     - RPM/DEB
     - 인덱스 정의 파일
   * - ``app/WEB-INF/thumbnails/``
     - zip/tar.gz
     - 썸네일 이미지(필요시)
   * - ``/var/lib/fess/thumbnails/``
     - RPM/DEB
     - 썸네일 이미지(필요시)

.. note::
   RPM/DEB 패키지 버전에서는 ``/etc/fess/`` 디렉터리에 ``fess_config.properties`` 외에도 ``fess_env_crawler.properties`` 등의 ``fess_env_*.properties`` 나 ``tika.xml`` 과 같은 설정 파일도 저장되어 있습니다. ``/etc/fess/`` 디렉터리 전체를 백업하는 것을 권장합니다. ``system.properties`` 는 관리 화면의 「시스템 > 일반」에서 설정을 저장할 때 ``/etc/fess/system.properties`` 로 생성·업데이트됩니다.

설정 파일 백업 예시
----------------------------

다음은 RPM/DEB 패키지 버전에서의 설정 파일 백업 예시입니다.

::

    #!/bin/bash
    BACKUP_DIR="/backup/fess/$(date +%Y%m%d_%H%M%S)"
    mkdir -p ${BACKUP_DIR}

    # 설정 파일 복사(system.properties 및 fess_config.properties 등 포함)
    cp -r /etc/fess/ ${BACKUP_DIR}/

    # 인덱스 정의 파일 및 로그 설정
    cp -r /usr/share/fess/app/WEB-INF/classes/fess_indices/ ${BACKUP_DIR}/
    cp /usr/share/fess/app/WEB-INF/classes/log4j2.xml ${BACKUP_DIR}/

    # 옵션: 썸네일 이미지
    # cp -r /var/lib/fess/thumbnails/ ${BACKUP_DIR}/

    echo "Backup completed: ${BACKUP_DIR}"

데이터 이전
==========

다른 환경으로의 이전 절차
------------------

1. **이전 소스에서 백업 생성**

   - OpenSearch의 스냅샷을 생성합니다.
   - 설정 파일을 백업합니다.

2. **이전 대상 준비**

   - |Fess| 를 새로운 환경에 설치합니다.
   - OpenSearch를 시작합니다.

3. **설정 파일 복원**

   - 백업한 설정 파일을 새로운 환경에 복사합니다.
   - 필요에 따라 경로나 호스트명 등을 수정합니다.

4. **인덱스 복원**

   - 스냅샷 리포지토리를 설정합니다.
   - 스냅샷에서 인덱스를 복원합니다.
   - 복원 후, ``fess.search`` 및 ``fess.update`` 별칭이 복원한 인덱스를 가리키고 있는지 확인합니다.

5. **동작 확인**

   - |Fess| 를 시작합니다.
   - 관리 화면에 접근하여 설정을 확인합니다.
   - 검색 기능이 정상 작동하는지 확인합니다.

버전 업그레이드 시 주의 사항
----------------------------

서로 다른 버전의 |Fess| 간에 데이터를 이전하는 경우 다음 사항에 주의하십시오.

- OpenSearch의 메이저 버전이 다른 경우 호환성 문제가 발생할 수 있습니다.
- 인덱스 구조가 변경된 경우 재인덱싱이 필요할 수 있습니다.
- 인덱스 구조 변경을 걸쳐 설정 정보를 이전하고 싶은 경우에는 OpenSearch 스냅샷이 아닌 관리 화면의 백업 기능( :doc:`../admin/backup-guide` )을 통한 논리적인 내보내기/가져오기의 활용을 검토하십시오.
- 자세한 내용은 각 버전의 업그레이드 가이드를 참조하십시오.

문제 해결
======================

스냅샷 생성 실패
--------------------------------

1. 리포지토리 경로에 대한 권한을 확인하십시오.
2. 디스크 용량이 충분한지 확인하십시오.
3. OpenSearch의 로그 파일에서 오류 메시지를 확인하십시오.

복원 실패
------------------

1. 동일한 이름의 인덱스가 이미 존재하지 않는지 확인하십시오. OpenSearch에서는 열려 있는 상태의 동일 이름 인덱스로는 복원할 수 없습니다. 복원 전에 대상 인덱스를 닫기( ``_close`` ) 또는 삭제하거나, ``rename_pattern`` 으로 다른 이름으로 복원하십시오.
2. OpenSearch의 버전이 호환되는지 확인하십시오.
3. 스냅샷이 손상되지 않았는지 확인하십시오.

복원 후 검색할 수 없음
------------------------

1. 인덱스가 정상적으로 복원되었는지 확인하십시오: ``curl -X GET "localhost:9201/_cat/indices?v"``
2. ``fess.search`` 및 ``fess.update`` 별칭이 복원한 인덱스를 가리키고 있는지 확인하십시오: ``curl -X GET "localhost:9201/_cat/aliases?v"`` . 별칭이 설정되어 있지 않은 경우에는 ``_aliases`` API로 재설정하십시오.
3. |Fess| 의 로그 파일에서 오류가 없는지 확인하십시오.
4. 설정 파일이 올바르게 복원되었는지 확인하십시오.

관련 항목
============

- :doc:`../admin/backup-guide` - 관리 화면에서의 설정 정보 백업/복원
- :doc:`admin-index-export` - 인덱스 내보내기 기능
- :doc:`admin-logging` - 로그 설정

참고 정보
========

자세한 정보는 OpenSearch의 공식 문서를 참조하십시오.

- `스냅샷 기능 <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_
- `리포지토리 설정 <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/>`_
- `S3 리포지토리 <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/plugins/#s3-repository>`_
