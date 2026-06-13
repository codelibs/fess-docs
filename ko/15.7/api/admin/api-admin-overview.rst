==========================
Admin API 개요
==========================

개요
====

|Fess| Admin API는 관리 기능에 프로그램에서 접근하기 위한 RESTful API입니다.
크롤링 설정, 사용자 관리, 스케줄러 제어 등 관리 화면에서 수행할 수 있는 대부분의 작업을 API를 통해 실행할 수 있습니다.

이 API를 사용하면 |Fess| 의 설정을 자동화하거나 외부 시스템과 연동할 수 있습니다.

기본 URL
=========

Admin API의 기본 URL은 다음 형식입니다:

::

    http://<Server Name>/api/admin/

예를 들어 로컬 환경의 경우:

::

    http://localhost:8080/api/admin/

인증
====

Admin API에 접근하려면 액세스 토큰을 통한 인증이 필요합니다.

액세스 토큰 취득
----------------------

1. 관리 화면에 로그인
2. "시스템" → "액세스 토큰"으로 이동
3. "새로 만들기" 클릭
4. 토큰 이름을 입력하고 필요한 권한 선택
5. "만들기" 클릭하여 토큰 취득

토큰 사용
--------------

요청 헤더에 액세스 토큰을 포함합니다:

::

    Authorization: Bearer <액세스 토큰>

또는 쿼리 파라미터로 지정:

::

    ?token=<액세스 토큰>

cURL 예시
~~~~~~

.. code-block:: bash

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "http://localhost:8080/api/admin/scheduler/settings"

필요한 권한
----------

Admin API를 사용하려면 토큰에 다음 권한이 필요합니다:

- ``admin-*`` - 모든 관리 기능에 대한 접근
- ``admin-scheduler`` - 스케줄러 관리만
- ``admin-user`` - 사용자 관리만
- 그 외 기능별 권한

공통 패턴
============

설정을 가진 리소스(webconfig, user, role 등)는 다음과 같은 공통 CRUD 패턴을 따릅니다.
다만 일부 리소스(systeminfo, stats, storage, plugin, log, backup, documents, suggest, dict 루트 등)는
이 공통 패턴과는 다른 독자적인 엔드포인트 구성을 가지므로 각 리소스 페이지를 참조하십시오.

목록 조회 (GET /settings)
-------------------------

설정 목록을 조회합니다.

요청
~~~~~~~~~~

::

    GET /api/admin/<resource>/settings

파라미터 (페이지네이션):

.. list-table::
   :header-rows: 1
   :widths: 20 15.75

   * - 파라미터
     - 타입
     - 설명
   * - ``size``
     - Integer
     - 페이지당 건수 (기본값: 20)
   * - ``page``
     - Integer
     - 페이지 번호 (0부터 시작)

응답
~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [...],
        "total": 100
      }
    }

.. note::

   모든 응답의 ``response`` 객체에는 제품 버전을 나타내는 ``version``
   (예: ``"15.7.0"``)이 항상 포함됩니다. 이후 예시에서는 간결함을 위해 생략하는 경우가 있습니다.

단일 설정 조회 (GET /setting/{id})
---------------------------------

ID를 지정하여 단일 설정을 조회합니다.

요청
~~~~~~~~~~

::

    GET /api/admin/<resource>/setting/{id}

응답
~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {...}
      }
    }

새로 만들기 (POST /setting)
-------------------------

새 설정을 만듭니다.

요청
~~~~~~~~~~

::

    POST /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "name": "...",
      "...": "..."
    }

응답
~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "created_id",
        "created": true
      }
    }

업데이트 (PUT /setting)
--------------------

기존 설정을 업데이트합니다.

요청
~~~~~~~~~~

::

    PUT /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "id": "...",
      "name": "...",
      "...": "..."
    }

응답
~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "updated_id",
        "created": false
      }
    }

삭제 (DELETE /setting/{id})
----------------------------

설정을 삭제합니다.

요청
~~~~~~~~~~

::

    DELETE /api/admin/<resource>/setting/{id}

응답
~~~~~~~~~~

삭제 응답의 형식은 리소스(액션)마다 다릅니다. 많은 리소스는
``status`` 만 반환합니다.

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

일부 리소스에서는 삭제 결과가 ``ApiUpdateResponse`` 로 반환되며, 삭제한 설정의
``id`` 와 ``created``(삭제 시에는 ``false``)가 부여됩니다.

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_id",
        "created": false
      }
    }

또한 ``ApiDeleteResponse`` 를 반환하는 리소스에서는 삭제 건수를 나타내는 ``count``
(기본값 ``1``)가 부여되는 경우가 있습니다. 실제 형식은 각 리소스 페이지를 참조하십시오.

응답 형식
==============

모든 응답은 ``response`` 객체로 래핑되며, 제품 버전을 나타내는
``version`` 과 처리 결과를 나타내는 ``status`` 를 항상 포함합니다.

``status`` 의 값은 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 값
     - 설명
   * - ``0``
     - OK (성공)
   * - ``1``
     - BAD_REQUEST (잘못된 요청)
   * - ``2``
     - SYSTEM_ERROR (시스템 오류)
   * - ``3``
     - UNAUTHORIZED (인증 오류)
   * - ``9``
     - FAILED (처리 실패)

성공 응답
--------------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "...": "..."
      }
    }

``status: 0`` 은 성공을 나타냅니다.

오류 응답
----------------

오류 시에는 ``status`` 에 0 이외의 값이 설정되며, ``message`` 에 오류 메시지가
포함됩니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "Failed to process the request."
      }
    }

HTTP 상태 코드
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 코드
     - 설명
   * - 200
     - 요청 성공
   * - 400
     - 요청 파라미터가 잘못됨
   * - 401
     - 인증 필요 (토큰 없음 또는 무효)
   * - 403
     - 접근 권한 없음
   * - 404
     - 리소스를 찾을 수 없음
   * - 500
     - 서버 내부 오류

사용 가능한 API
=============

|Fess| 는 다음의 Admin API를 제공합니다.

크롤링 설정
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 엔드포인트
     - 설명
   * - :doc:`api-admin-webconfig`
     - Web 크롤링 설정
   * - :doc:`api-admin-fileconfig`
     - 파일 크롤링 설정
   * - :doc:`api-admin-dataconfig`
     - 데이터스토어 설정

.. note::

   이 외에 인증 정보나 크롤링 제어에 관한 다음 리소스도 API로 제공됩니다
   (현재 시점에서는 개별 페이지가 정비되어 있지 않습니다): ``webauth``(Web 인증), ``fileauth``(파일 인증),
   ``reqheader``(요청 헤더), ``pathmap``(경로 매핑),
   ``duplicatehost``(중복 호스트), ``searchlist``(검색/문서 목록 조작).

인덱스 관리
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 엔드포인트
     - 설명
   * - :doc:`api-admin-documents`
     - 문서 일괄 조작
   * - :doc:`api-admin-crawlinginfo`
     - 크롤링 정보
   * - :doc:`api-admin-failureurl`
     - 실패 URL 관리
   * - :doc:`api-admin-backup`
     - 백업/복원

스케줄러
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 엔드포인트
     - 설명
   * - :doc:`api-admin-scheduler`
     - 작업 스케줄링
   * - :doc:`api-admin-joblog`
     - 작업 로그 조회

사용자/권한 관리
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 엔드포인트
     - 설명
   * - :doc:`api-admin-user`
     - 사용자 관리
   * - :doc:`api-admin-role`
     - 역할 관리
   * - :doc:`api-admin-group`
     - 그룹 관리
   * - :doc:`api-admin-accesstoken`
     - API 토큰 관리

검색 튜닝
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 엔드포인트
     - 설명
   * - :doc:`api-admin-labeltype`
     - 라벨 타입
   * - :doc:`api-admin-keymatch`
     - 키 매치
   * - :doc:`api-admin-boostdoc`
     - 문서 부스트
   * - :doc:`api-admin-elevateword`
     - 엘리베이트 워드
   * - :doc:`api-admin-badword`
     - NG 워드
   * - :doc:`api-admin-relatedcontent`
     - 관련 콘텐츠
   * - :doc:`api-admin-relatedquery`
     - 관련 쿼리
   * - :doc:`api-admin-suggest`
     - 서제스트 관리

시스템
--------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 엔드포인트
     - 설명
   * - :doc:`api-admin-general`
     - 일반 설정
   * - :doc:`api-admin-systeminfo`
     - 시스템 정보
   * - :doc:`api-admin-stats`
     - 시스템 통계
   * - :doc:`api-admin-log`
     - 로그 조회
   * - :doc:`api-admin-searchlist`
     - 문서 검색 및 관리
   * - :doc:`api-admin-storage`
     - 스토리지 관리
   * - :doc:`api-admin-plugin`
     - 플러그인 관리

사전
----

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 엔드포인트
     - 설명
   * - :doc:`api-admin-dict`
     - 사전 관리 (동의어, 불용어 등)

사용 예
======

Web 크롤링 설정 만들기
---------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Example Site",
           "urls": "https://example.com/",
           "includedUrls": ".*example.com.*",
           "excludedUrls": "",
           "maxAccessCount": 1000,
           "depth": 3,
           "available": true
         }'

스케줄 작업 시작
------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

사용자 목록 조회
------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/user/settings?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

참고 정보
========

- :doc:`../api-overview` - API 개요
- :doc:`../../admin/accesstoken-guide` - 액세스 토큰 관리 가이드
