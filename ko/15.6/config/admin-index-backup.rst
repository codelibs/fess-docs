==================
인덱스 관리
==================

개요
====

|Fess| 에서 다루는 데이터는 OpenSearch의 인덱스로 관리됩니다.
검색 인덱스의 백업과 복원은 시스템의 안정적인 운영에 필수적입니다.
본 섹션에서는 인덱스의 백업, 복원, 및 이전 절차에 대해 설명합니다.

인덱스 구성
==================

|Fess| 에서는 다음 인덱스가 사용됩니다.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 인덱스 이름
     - 설명
   * - ``fess.{날짜}``
     - 검색 대상 문서의 인덱스(일일 생성)
   * - ``fess_log``
     - 검색 로그 및 클릭 로그
   * - ``fess_user``
     - 사용자 정보
   * - ``fess_config``
     - 시스템 설정 정보
   * - ``configsync``
     - 설정 동기화 정보

인덱스 백업 및 복원
====================================

OpenSearch의 스냅샷 기능을 사용하여 인덱스의 백업과 복원을 실행할 수 있습니다.

스냅샷 리포지토리 설정
--------------------------------

먼저 백업 데이터를 저장할 리포지토리를 설정합니다.

**파일 시스템 리포지토리의 경우:**

1. OpenSearch의 설정 파일 (``config/opensearch.yml``)에 리포지토리 경로를 추가합니다.

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
   |Fess| 의 기본 설정에서는 OpenSearch가 9201 포트에서 시작됩니다.

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

특정 인덱스만 백업합니다.

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_fess_only?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.*,fess_config",
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

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

인덱스 이름을 변경하여 복원
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

복원 시 인덱스 이름을 변경할 수도 있습니다.

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101",
      "rename_pattern": "fess.(.+)",
      "rename_replacement": "restored_fess.$1",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

스냅샷 삭제
----------------------

오래된 스냅샷을 삭제하여 스토리지 용량을 절약할 수 있습니다.

::

    curl -X DELETE "localhost:9201/_snapshot/fess_backup/snapshot_1"

설정 파일 백업
==========================

OpenSearch의 인덱스와는 별도로 다음 설정 파일도 백업하십시오.

백업 대상 파일
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 파일/디렉터리
     - 설명
   * - ``app/WEB-INF/conf/system.properties``
     - 시스템 설정(zip 설치의 경우)
   * - ``/etc/fess/system.properties``
     - 시스템 설정(RPM/DEB 패키지의 경우)
   * - ``app/WEB-INF/classes/fess_config.properties``
     - Fess 상세 설정
   * - ``/etc/fess/fess_config.properties``
     - Fess 상세 설정(RPM/DEB 패키지)
   * - ``app/WEB-INF/classes/log4j2.xml``
     - 로그 설정
   * - ``/etc/fess/log4j2.xml``
     - 로그 설정(RPM/DEB 패키지)
   * - ``app/WEB-INF/classes/fess_indices/``
     - 인덱스 정의 파일
   * - ``thumbnail/``
     - 썸네일 이미지(필요시)

설정 파일 백업 예
----------------------------

::

    #!/bin/bash
    BACKUP_DIR="/backup/fess/$(date +%Y%m%d_%H%M%S)"
    mkdir -p ${BACKUP_DIR}

    # 설정 파일 복사
    cp -r /etc/fess/ ${BACKUP_DIR}/
    cp -r /var/lib/fess/app/WEB-INF/conf/ ${BACKUP_DIR}/
    cp -r /var/lib/fess/app/WEB-INF/classes/fess_indices/ ${BACKUP_DIR}/

    # 옵션: 썸네일 이미지
    # cp -r /var/lib/fess/thumbnail/ ${BACKUP_DIR}/

    echo "Backup completed: ${BACKUP_DIR}"

데이터 이전
==========

다른 환경으로의 이전 절차
------------------

1. **이전 소스에서 백업 생성**

   - OpenSearch의 스냅샷을 생성합니다.
   - 설정 파일을 백업합니다.

2. **이전 대상 준비**

   - |Fess| 를 새 환경에 설치합니다.
   - OpenSearch를 시작합니다.

3. **설정 파일 복원**

   - 백업한 설정 파일을 새 환경에 복사합니다.
   - 필요에 따라 경로나 호스트명 등을 수정합니다.

4. **인덱스 복원**

   - 스냅샷 리포지토리를 설정합니다.
   - 스냅샷에서 인덱스를 복원합니다.

5. **동작 확인**

   - |Fess| 를 시작합니다.
   - 관리 화면에 접근하여 설정을 확인합니다.
   - 검색 기능이 정상 작동하는지 확인합니다.

버전 업그레이드 시 주의 사항
----------------------------

서로 다른 버전의 |Fess| 간에 데이터를 이전하는 경우 다음 사항에 주의하십시오.

- OpenSearch의 메이저 버전이 다른 경우 호환성 문제가 발생할 수 있습니다.
- 인덱스 구조가 변경된 경우 재인덱싱이 필요할 수 있습니다.
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

1. 동일한 이름의 인덱스가 이미 존재하지 않는지 확인하십시오.
2. OpenSearch의 버전이 호환되는지 확인하십시오.
3. 스냅샷이 손상되지 않았는지 확인하십시오.

복원 후 검색할 수 없음
------------------------

1. 인덱스가 정상적으로 복원되었는지 확인하십시오: ``curl -X GET "localhost:9201/_cat/indices?v"``
2. |Fess| 의 로그 파일에서 오류가 없는지 확인하십시오.
3. 설정 파일이 올바르게 복원되었는지 확인하십시오.

참고 정보
========

자세한 정보는 OpenSearch의 공식 문서를 참조하십시오.

- `스냅샷 기능 <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_
- `리포지토리 설정 <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/>`_
- `S3 리포지토리 <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/plugins/#s3-repository>`_
