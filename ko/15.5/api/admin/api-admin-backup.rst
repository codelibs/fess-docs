==========================
Backup API
==========================

개요
====

Backup API는 |Fess| 의 설정 데이터를 백업 및 복원하기 위한 API입니다.
크롤링 설정, 사용자, 역할, 사전 등의 설정을 내보내기/가져오기할 수 있습니다.

기본 URL
=========

::

    /api/admin/backup

엔드포인트 목록
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 메서드
     - 경로
     - 설명
   * - GET
     - /export
     - 설정 데이터 내보내기
   * - POST
     - /import
     - 설정 데이터 가져오기

설정 데이터 내보내기
======================

요청
----------

::

    GET /api/admin/backup/export

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``types``
     - String
     - 아니오
     - 내보내기 대상 (쉼표로 구분, 기본값: all)

내보내기 대상 타입
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 타입
     - 설명
   * - ``webconfig``
     - Web 크롤링 설정
   * - ``fileconfig``
     - 파일 크롤링 설정
   * - ``dataconfig``
     - 데이터스토어 설정
   * - ``scheduler``
     - 스케줄 설정
   * - ``user``
     - 사용자 설정
   * - ``role``
     - 역할 설정
   * - ``group``
     - 그룹 설정
   * - ``labeltype``
     - 라벨 타입 설정
   * - ``keymatch``
     - 키 매치 설정
   * - ``dict``
     - 사전 데이터
   * - ``all``
     - 모든 설정 (기본값)

응답
----------

바이너리 데이터 (ZIP 형식)

Content-Type: ``application/zip``
Content-Disposition: ``attachment; filename="fess-backup-20250129-100000.zip"``

ZIP 파일 내용
~~~~~~~~~~~~~~~

::

    fess-backup-20250129-100000.zip
    ├── webconfig.json
    ├── fileconfig.json
    ├── dataconfig.json
    ├── scheduler.json
    ├── user.json
    ├── role.json
    ├── group.json
    ├── labeltype.json
    ├── keymatch.json
    ├── dict/
    │   ├── synonym.txt
    │   ├── mapping.txt
    │   └── protwords.txt
    └── metadata.json

설정 데이터 가져오기
====================

요청
----------

::

    POST /api/admin/backup/import
    Content-Type: multipart/form-data

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: bash

    --boundary
    Content-Disposition: form-data; name="file"; filename="fess-backup.zip"
    Content-Type: application/zip

    [바이너리 데이터]
    --boundary
    Content-Disposition: form-data; name="overwrite"

    true
    --boundary--

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``file``
     - 예
     - 백업 ZIP 파일
   * - ``overwrite``
     - 아니오
     - 기존 설정 덮어쓰기 (기본값: false)
   * - ``types``
     - 아니오
     - 가져오기 대상 (쉼표로 구분, 기본값: all)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Backup imported successfully",
        "imported": {
          "webconfig": 5,
          "fileconfig": 3,
          "dataconfig": 2,
          "scheduler": 4,
          "user": 10,
          "role": 5,
          "group": 3,
          "labeltype": 8,
          "keymatch": 12,
          "dict": 3
        }
      }
    }

사용 예
======

전체 설정 내보내기
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/export" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess-backup.zip

특정 설정 내보내기
----------------------

.. code-block:: bash

    # Web 크롤링 설정과 사용자 설정만 내보내기
    curl -X GET "http://localhost:8080/api/admin/backup/export?types=webconfig,user" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess-backup-partial.zip

설정 가져오기
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "overwrite=false"

기존 설정을 덮어쓰고 가져오기
------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "overwrite=true"

특정 설정만 가져오기
----------------------

.. code-block:: bash

    # 사용자와 역할만 가져오기
    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "types=user,role" \
         -F "overwrite=false"

백업 자동화
--------------------

.. code-block:: bash

    #!/bin/bash
    # 매일 오전 2시에 백업을 가져오는 스크립트 예시

    DATE=$(date +%Y%m%d)
    BACKUP_DIR="/backup/fess"

    curl -X GET "http://localhost:8080/api/admin/backup/export" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o "${BACKUP_DIR}/fess-backup-${DATE}.zip"

    # 30일 이상 된 백업 삭제
    find "${BACKUP_DIR}" -name "fess-backup-*.zip" -mtime +30 -delete

주의 사항
========

- 백업에는 비밀번호 정보도 포함되므로 안전하게 보관하세요
- 가져오기 시 ``overwrite=true`` 를 지정하면 기존 설정이 덮어쓰여집니다
- 대규모 설정의 경우 내보내기/가져오기에 시간이 걸릴 수 있습니다
- 버전이 다른 Fess 간의 가져오기는 호환성 문제가 발생할 수 있습니다

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`../../admin/backup-guide` - 백업 관리 가이드
- :doc:`../../admin/maintenance-guide` - 유지보수 가이드
