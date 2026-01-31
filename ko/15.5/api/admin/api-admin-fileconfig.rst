==========================
FileConfig API
==========================

개요
====

FileConfig API는 |Fess| 의 파일 크롤링 설정을 관리하기 위한 API입니다.
파일 시스템이나 SMB/CIFS의 공유 폴더 등의 크롤링 설정을 조작할 수 있습니다.

기본 URL
=========

::

    /api/admin/fileconfig

엔드포인트 목록
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 메서드
     - 경로
     - 설명
   * - GET/PUT
     - /settings
     - 파일 크롤링 설정 목록 조회
   * - GET
     - /setting/{id}
     - 파일 크롤링 설정 조회
   * - POST
     - /setting
     - 파일 크롤링 설정 만들기
   * - PUT
     - /setting
     - 파일 크롤링 설정 업데이트
   * - DELETE
     - /setting/{id}
     - 파일 크롤링 설정 삭제

파일 크롤링 설정 목록 조회
============================

요청
----------

::

    GET /api/admin/fileconfig/settings
    PUT /api/admin/fileconfig/settings

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``size``
     - Integer
     - 아니오
     - 페이지당 건수 (기본값: 20)
   * - ``page``
     - Integer
     - 아니오
     - 페이지 번호 (0부터 시작)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "fileconfig_id_1",
            "name": "Shared Documents",
            "paths": "file://///server/share/documents",
            "includedPaths": ".*\\.pdf$",
            "excludedPaths": ".*/(temp|cache)/.*",
            "includedDocPaths": "",
            "excludedDocPaths": "",
            "configParameter": "",
            "depth": 10,
            "maxAccessCount": 1000,
            "numOfThread": 1,
            "intervalTime": 1000,
            "boost": 1.0,
            "available": true,
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

파일 크롤링 설정 조회
========================

요청
----------

::

    GET /api/admin/fileconfig/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "fileconfig_id_1",
          "name": "Shared Documents",
          "paths": "file://///server/share/documents",
          "includedPaths": ".*\\.pdf$",
          "excludedPaths": ".*/(temp|cache)/.*",
          "includedDocPaths": "",
          "excludedDocPaths": "",
          "configParameter": "",
          "depth": 10,
          "maxAccessCount": 1000,
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": true,
          "sortOrder": 0,
          "permissions": ["admin"],
          "virtualHosts": [],
          "labelTypeIds": []
        }
      }
    }

파일 크롤링 설정 만들기
========================

요청
----------

::

    POST /api/admin/fileconfig/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Local Files",
      "paths": "file:///data/documents",
      "includedPaths": ".*\\.(pdf|doc|docx|xls|xlsx)$",
      "excludedPaths": ".*/(temp|backup)/.*",
      "depth": 5,
      "maxAccessCount": 5000,
      "numOfThread": 2,
      "intervalTime": 500,
      "boost": 1.0,
      "available": true,
      "permissions": ["admin", "user"],
      "labelTypeIds": ["label_id_1"]
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``name``
     - 예
     - 설정 이름
   * - ``paths``
     - 예
     - 크롤링 시작 경로 (여러 개인 경우 줄바꿈으로 구분)
   * - ``includedPaths``
     - 아니오
     - 크롤링 대상 경로의 정규 표현식 패턴
   * - ``excludedPaths``
     - 아니오
     - 크롤링 제외 경로의 정규 표현식 패턴
   * - ``includedDocPaths``
     - 아니오
     - 인덱스 대상 경로의 정규 표현식 패턴
   * - ``excludedDocPaths``
     - 아니오
     - 인덱스 제외 경로의 정규 표현식 패턴
   * - ``configParameter``
     - 아니오
     - 추가 설정 파라미터
   * - ``depth``
     - 아니오
     - 크롤링 깊이 (기본값: -1=무제한)
   * - ``maxAccessCount``
     - 아니오
     - 최대 접근 수 (기본값: 100)
   * - ``numOfThread``
     - 아니오
     - 병렬 스레드 수 (기본값: 1)
   * - ``intervalTime``
     - 아니오
     - 접근 간격 (밀리초, 기본값: 0)
   * - ``boost``
     - 아니오
     - 검색 결과 부스트 값 (기본값: 1.0)
   * - ``available``
     - 아니오
     - 활성화/비활성화 (기본값: true)
   * - ``sortOrder``
     - 아니오
     - 표시 순서
   * - ``permissions``
     - 아니오
     - 접근 허용 역할
   * - ``virtualHosts``
     - 아니오
     - 가상 호스트
   * - ``labelTypeIds``
     - 아니오
     - 라벨 타입 ID

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_fileconfig_id",
        "created": true
      }
    }

파일 크롤링 설정 업데이트
========================

요청
----------

::

    PUT /api/admin/fileconfig/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_fileconfig_id",
      "name": "Updated Local Files",
      "paths": "file:///data/documents",
      "includedPaths": ".*\\.(pdf|doc|docx|xls|xlsx|ppt|pptx)$",
      "excludedPaths": ".*/(temp|backup|archive)/.*",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 3,
      "intervalTime": 300,
      "boost": 1.2,
      "available": true,
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_fileconfig_id",
        "created": false
      }
    }

파일 크롤링 설정 삭제
========================

요청
----------

::

    DELETE /api/admin/fileconfig/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_fileconfig_id",
        "created": false
      }
    }

경로 형식
==========

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 프로토콜
     - 경로 형식
   * - 로컬 파일
     - ``file:///path/to/directory``
   * - Windows 공유 (SMB)
     - ``file://///server/share/path``
   * - SMB 인증 포함
     - ``smb://username:password@server/share/path``
   * - NFS
     - ``file://///nfs-server/export/path``

사용 예
======

SMB 공유 크롤링 설정
---------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "SMB Share",
           "paths": "smb://user:pass@server/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|private)/.*",
           "depth": -1,
           "maxAccessCount": 50000,
           "numOfThread": 3,
           "intervalTime": 200,
           "available": true,
           "permissions": ["guest"]
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-webconfig` - Web 크롤링 설정 API
- :doc:`api-admin-dataconfig` - 데이터스토어 설정 API
- :doc:`../../admin/fileconfig-guide` - 파일 크롤링 설정 가이드
