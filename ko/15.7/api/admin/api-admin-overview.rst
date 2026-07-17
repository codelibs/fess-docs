==========================
Admin API 개요
==========================

개요
========

|Fess| Admin API는 관리 기능에 프로그램에서 접근하기 위한 RESTful API입니다.
크롤링 설정, 사용자 관리, 스케줄러 제어 등 관리 화면에서 수행할 수 있는 대부분의 작업을 API를 통해 실행할 수 있습니다.

이 API를 사용하면 |Fess| 의 설정을 자동화하거나 외부 시스템과 연동할 수 있습니다.

기본 URL
============

Admin API의 기본 URL은 다음 형식입니다:

::

    http://<Server Name>/api/admin/

예를 들어 로컬 환경의 경우:

::

    http://localhost:8080/api/admin/

인증
========

Admin API에 접근하려면 액세스 토큰을 통한 인증이 필요합니다.

액세스 토큰 취득
--------------------------

1. 관리 화면에 로그인
2. "시스템" → "액세스 토큰"으로 이동
3. "새로 만들기" 클릭
4. 토큰 이름을 입력하고 "권한" 란에 토큰에 부여할 권한을 설정 (Admin API를 사용하는 경우 ``{role}admin-api`` 입력)
5. "만들기" 클릭하여 토큰 취득

토큰 사용
--------------------

요청 헤더에 액세스 토큰을 포함합니다:

::

    Authorization: Bearer <액세스 토큰>

``Bearer`` 를 생략하고 토큰만 지정할 수도 있습니다:

::

    Authorization: <액세스 토큰>

쿼리 파라미터로 지정할 수도 있지만 기본적으로 비활성화되어 있습니다. ``fess_config.properties`` 의
``api.access.token.request.parameter`` 에 파라미터 이름을 설정하면 그 이름으로
토큰을 전달할 수 있게 됩니다 (기본값은 비어 있으므로 헤더를 통한 지정만 유효합니다).
예를 들어 ``api.access.token.request.parameter=token`` 을 설정한 경우:

::

    ?token=<액세스 토큰>

cURL 예시
~~~~~~~~~~~~~~

.. code-block:: bash

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "http://localhost:8080/api/admin/scheduler/settings"

필요한 권한
--------------------

Admin API에 대한 접근은 기능별이 아니라 단일 권한 세트로 제어됩니다. Admin API의
어느 엔드포인트를 사용하든 액세스 토큰에 ``fess_config.properties`` 의
``api.admin.access.permissions`` 에 설정된 권한 중 하나가 부여되어 있어야 합니다.

기본값은 ``Radmin-api`` 이며, 이는 역할 ``admin-api`` 를 인코딩한 형식입니다
(앞쪽의 ``R`` 은 ``role.search.role.prefix`` 의 값). 액세스 토큰 생성 시
권한 란에 ``{role}admin-api`` 를 입력하면 내부적으로 ``Radmin-api`` 로 저장됩니다.

.. note::

   개별 리소스마다 다른 권한 (``admin-scheduler`` 나 ``admin-user`` 등)이나
   와일드카드 (``admin-*``)는 존재하지 않습니다. 설정된 권한을 가진 토큰은
   모든 Admin API 엔드포인트에 접근할 수 있습니다. 접근을 허용할 권한을
   변경하려면 ``api.admin.access.permissions`` 의 값을 변경하십시오.

공통 패턴
============

설정을 가진 리소스(webconfig, user, role 등)는 다음과 같은 공통 CRUD 패턴을 따릅니다.
다만 일부 리소스(systeminfo, stats, storage, plugin, log, backup, documents, suggest, dict 루트 등)는
이 공통 패턴과는 다른 독자적인 엔드포인트 구성을 가지므로 각 리소스 페이지를 참조하십시오.

목록 조회 (GET /settings)
-------------------------------

설정 목록을 조회합니다.

요청
~~~~~~~~~~~~

::

    GET /api/admin/<resource>/settings

파라미터 (페이지네이션):

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 파라미터
     - 타입
     - 설명
   * - ``size``
     - Integer
     - 페이지당 건수 (기본값: 25. ``fess_config.properties`` 의 ``paging.page.size`` 로 변경 가능)
   * - ``page``
     - Integer
     - 페이지 번호 (1부터 시작. 기본값: 1. 0 이하를 지정한 경우 1로 처리됩니다)

응답
~~~~~~~~~~~~

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
-----------------------------------------

ID를 지정하여 단일 설정을 조회합니다.

요청
~~~~~~~~~~~~

::

    GET /api/admin/<resource>/setting/{id}

응답
~~~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {...}
      }
    }

새로 만들기 (POST /setting)
---------------------------------

새 설정을 만듭니다.

요청
~~~~~~~~~~~~

::

    POST /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "name": "...",
      "...": "..."
    }

응답
~~~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "created_id",
        "created": true
      }
    }

업데이트 (PUT /setting)
-----------------------------

기존 설정을 업데이트합니다.

요청
~~~~~~~~~~~~

::

    PUT /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "id": "...",
      "name": "...",
      "...": "..."
    }

응답
~~~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "updated_id",
        "created": false
      }
    }

삭제 (DELETE /setting/{id})
---------------------------------

설정을 삭제합니다.

요청
~~~~~~~~~~~~

::

    DELETE /api/admin/<resource>/setting/{id}

응답
~~~~~~~~~~~~

삭제 응답의 형식은 리소스(액션)마다 다릅니다. 많은 리소스는
``status`` 만 반환합니다.

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

일부 리소스에서는 삭제 결과가 ``ApiUpdateResponse`` 로 반환되며, 삭제한 설정의
``id`` 와 ``created``\ (삭제 시에는 ``false``)가 부여됩니다.

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
============

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
--------------------

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
--------------------

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
--------------------------

Admin API는 대부분의 경우 HTTP 상태 ``200`` 을 반환하며, 처리 결과는 응답 본문의
``status`` 필드로 나타냅니다. 따라서 성공/실패 판정은 HTTP 상태 코드가 아니라
본문의 ``status`` 값으로 수행하십시오.

실제로 반환되는 HTTP 상태 코드는 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 코드
     - 설명
   * - 200
     - 일반 응답. 성공 시(``status: 0``)뿐만 아니라 대부분의 오류도 이 코드로
       반환됩니다. 예를 들어 액세스 토큰이 미지정·무효한 경우나 권한이 부족한 경우는
       ``status: 3``, 시스템 오류는 ``status: 2`` 로 모두 HTTP ``200`` 으로 반환됩니다.
   * - 400
     - 요청 파라미터의 검증 오류. 응답 본문의 ``status`` 는 ``1`` 이 됩니다.
       존재하지 않는 리소스를 조회하려고 한 경우에도 이 코드로 반환됩니다.
   * - 401
     - 로그인 인증에 관한 예외가 발생한 경우. 응답 본문의 ``status`` 는 ``3`` 이 됩니다.
       또한 액세스 토큰이 미지정·무효한 경우는 이 코드가 아니라 HTTP ``200`` 으로
       ``status: 3`` 이 반환됩니다.

.. note::

   Admin API에서는 ``403``, ``404``, ``500`` 과 같은 HTTP 상태 코드는 반환되지 않습니다.
   권한 부족이나 리소스의 부재도 HTTP ``200`` 또는 ``400`` 의 응답 본문에 포함된
   ``status`` 로 표시됩니다.

사용 가능한 API
====================

|Fess| 는 다음의 Admin API를 제공합니다.

크롤링 설정
--------------------

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
   (현재 시점에서는 개별 페이지가 정비되어 있지 않습니다): ``webauth``\ (Web 인증), ``fileauth``\ (파일 인증),
   ``reqheader``\ (요청 헤더), ``pathmap``\ (경로 매핑),
   ``duplicatehost``\ (중복 호스트), ``searchlist``\ (검색/문서 목록 조작).

인덱스 관리
--------------------

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
--------------------

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
------------------------

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
--------------------

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
--------------------

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
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 엔드포인트
     - 설명
   * - :doc:`api-admin-dict`
     - 사전 관리 (동의어, 불용어 등)

사용 예
============

Web 크롤링 설정 만들기
----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Example Site",
           "urls": "https://example.com/",
           "includedUrls": ".*example.com.*",
           "excludedUrls": "",
           "userAgent": "Mozilla/5.0 (compatible; Fess)",
           "numOfThread": 1,
           "intervalTime": 1000,
           "boost": 1.0,
           "maxAccessCount": 1000,
           "depth": 3,
           "sortOrder": 1,
           "available": "true"
         }'

.. note::

   Web 크롤링 설정 만들기에서는 ``name``, ``urls``, ``userAgent``, ``numOfThread``,
   ``intervalTime``, ``boost``, ``available``, ``sortOrder`` 가 필수입니다. 이들을
   생략하면 검증 오류(``status: 1``)가 됩니다. ``available`` 은 문자열로 지정하며,
   ``"true"`` 또는 ``"false"`` 를 설정합니다.

스케줄 작업 시작
------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

사용자 목록 조회
------------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/user/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

참고 정보
============

- :doc:`../api-overview` - API 개요
- :doc:`../../admin/accesstoken-guide` - 액세스 토큰 관리 가이드
