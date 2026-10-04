===========
TagType API
===========

개요
====

TagType API는 |Fess| 의 사용자 태그(로그인한 사용자가 문서에 붙이는 사용자별 태그)를 관리하기 위한 API입니다( :doc:`../../admin/tagtype-guide` 참조). ``user.tag.enabled`` 값과 관계없이 모든 사용자의 태그를 관리할 수 있습니다.

인증 방법 및 응답의 공통 사양(``status`` 코드, ``version`` 필드, 오류 형식,
HTTP 상태 코드 등)에 대해서는 :doc:`api-admin-overview` 를 참조하십시오.
이 API에 접근하려면 관리 API 권한(``admin-api``)을 가진 액세스 토큰을
``Authorization: Bearer <액세스 토큰>`` 헤더로 지정해야 합니다.

이 API의 JSON 필드 이름은 스네이크 케이스( ``sort_order`` , ``virtual_host`` , ``seq_no`` , ``primary_term`` 등)입니다.

기본 URL
========

::

    /api/admin/tagtype

엔드포인트 목록
===============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 메서드
     - 경로
     - 설명
   * - GET
     - /settings
     - 태그 목록 조회
   * - GET
     - /setting/{id}
     - 태그 조회
   * - POST
     - /setting
     - 태그 생성
   * - PUT
     - /setting
     - 태그 업데이트
   * - DELETE
     - /setting/{id}
     - 태그 삭제

태그 목록 조회
==============

요청
----

::

    GET /api/admin/tagtype/settings

파라미터
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``size``
     - Integer
     - 아니요
     - 페이지당 건수. 기본값은 ``paging.page.size`` 설정값(기본 ``25`` )입니다.
   * - ``page``
     - Integer
     - 아니요
     - 페이지 번호(1부터 시작). 기본값은 ``1`` 입니다.
   * - ``name``
     - String
     - 아니요
     - 태그 이름으로 필터링(와일드카드 검색. 입력한 문자열을 포함하는 이름과 일치).
   * - ``owner``
     - String
     - 아니요
     - 소유자로 필터링(와일드카드 검색. 입력한 문자열을 포함하는 소유자와 일치).

태그는 표시 순서, 이름, 소유자 순으로 정렬됩니다.

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.9.0",
        "status": 0,
        "settings": [
          {
            "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
            "seq_no": 12,
            "primary_term": 1,
            "name": "to-review",
            "owner": "alice",
            "permissions": "{user}alice",
            "virtual_host": "",
            "sort_order": 0
          }
        ],
        "total": 5
      }
    }

.. note::

   목록에서는 길어질 수 있는 태그의 경로를 가져오지 않으므로, 각 요소에는 ``paths`` 가 없습니다. PUT 은 태그 전체를 교체하므로, 태그를 편집할 때는 ``paths`` 가 유지되도록 먼저 ``GET /setting/{id}`` 로 가져오십시오.

태그 조회
=========

요청
----

::

    GET /api/admin/tagtype/setting/{id}

응답
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
          "seq_no": 12,
          "primary_term": 1,
          "name": "to-review",
          "owner": "alice",
          "paths": "https://www.example.com/a.html\nhttps://www.example.com/b.html",
          "permissions": "{user}alice",
          "virtual_host": "",
          "sort_order": 0
        }
      }
    }

``seq_no`` 와 ``primary_term`` 은 읽어 온 태그의 버전을 나타냅니다. ``paths`` 와 ``permissions`` 는 한 줄에 하나의 값을 갖습니다.

태그 생성
=========

요청
----

::

    POST /api/admin/tagtype/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~

.. code-block:: json

    {
      "name": "specs",
      "owner": "bob",
      "paths": "https://www.example.com/spec.pdf",
      "permissions": "{user}bob\n{role}guest",
      "sort_order": 0
    }

필드 설명
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - 필드
     - 타입
     - 필수
     - 설명
   * - ``name``
     - String
     - 예
     - 태그 이름. NFKC 로 정규화되고, 연속된 공백은 하나로 합쳐지며, 앞뒤 공백은 제거됩니다. 정규화 후의 길이는 1 ~ ``user.tag.name.max.length`` (기본값: ``50`` )자이며, 제어 문자나 서식 문자는 사용할 수 없습니다.
   * - ``owner``
     - String
     - 예
     - 태그를 소유하는 사용자의 로그인 사용자 ID(최대 1000자).
   * - ``paths``
     - String
     - 아니요
     - 태그를 붙일 문서의 URL. 여러 개를 지정하려면 줄바꿈( ``\n`` )으로 구분합니다. 각각 문서의 ``url`` 필드와 완전히 일치해야 합니다. 최대 ``user.tag.max.paths`` (기본값: ``10000`` )개.
   * - ``permissions``
     - String
     - 아니요
     - 태그를 볼 수 있는 사용자·그룹·역할(예: ``{role}guest`` ). 여러 개를 지정하려면 줄바꿈( ``\n`` )으로 구분합니다. 비어 있으면 소유자만 볼 수 있습니다. ``{role}guest`` ( ``role.search.guest.permissions`` 의 값)를 포함하면 로그인한 모든 사용자와 공유됩니다.
   * - ``virtual_host``
     - String
     - 아니요
     - 가상 호스트(최대 1000자).
   * - ``sort_order``
     - Integer
     - 아니요
     - 표시 순서(0 이상의 정수). 생략하면 ``0`` 입니다.

태그 ID 는 이름과 소유자로 만들어지는 태그 값의 SHA-256 이며, 서버가 결정합니다. 소유자와 이름의 조합으로 태그가 식별되므로, 소유자가 같은 이름의 태그를 이미 가지고 있으면 유효성 검사 오류( ``status: 1`` , "A tag with the same name and owner already exists.")가 됩니다.

응답
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "41e429a7d0081e25390c3840268d736dca00250167bab94250389aee9e08e2ed",
        "created": true
      }
    }

생성에 성공하면 ``created`` 는 ``true`` 가 됩니다.

태그 업데이트
=============

요청
----

::

    PUT /api/admin/tagtype/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~

.. code-block:: json

    {
      "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
      "seq_no": 12,
      "primary_term": 1,
      "name": "reviewed",
      "owner": "alice",
      "paths": "https://www.example.com/a.html",
      "permissions": "{user}alice",
      "virtual_host": "",
      "sort_order": 0
    }

생성 시의 모든 필드에 더해 다음 필드가 필요합니다. 태그는 전체가 교체되므로, 유지하려는 ``paths`` 도 함께 보내십시오.

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - 필드
     - 타입
     - 필수
     - 설명
   * - ``id``
     - String
     - 예
     - 업데이트할 태그의 ID.
   * - ``seq_no``
     - Integer
     - 예
     - ``GET /setting/{id}`` 가 반환한 태그의 ``seq_no`` .
   * - ``primary_term``
     - Integer
     - 예
     - ``GET /setting/{id}`` 가 반환한 태그의 ``primary_term`` .

- 읽어 온 뒤 태그가 변경되어 ``seq_no`` 와 ``primary_term`` 이 일치하지 않으면 유효성 검사 오류( ``status: 1`` , "The tag was changed by someone else. Reload it and try again.")가 됩니다. 태그를 다시 가져온 뒤 재시도하십시오.
- ``name`` 이나 ``owner`` 를 변경하면 태그 ID 가 바뀌며, 응답의 ``id`` 는 새 ID 입니다. 소유자가 변경 후 이름의 태그를 이미 가지고 있으면 "A tag with the same name and owner already exists." 가 됩니다.
- 소유자를 변경하면 ``permissions`` 에 포함된 이전 소유자의 사용자 권한이 새 소유자의 것으로 바뀝니다.

응답
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "c1fd8e024cbadfc79468e66fa52350e46cc31837aabf75b7ee6d929edaa20396",
        "created": false
      }
    }

업데이트 시에는 ``created`` 가 ``false`` 가 됩니다.

태그 삭제
=========

요청
----

::

    DELETE /api/admin/tagtype/setting/{id}

응답
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

삭제 도중 태그가 변경된 경우 "The tag was changed by someone else. Reload it and try again." 가 됩니다.

문서에 대한 반영
================

이 API에 의한 태그의 생성·업데이트·삭제는 즉시 태그 정보에 저장됩니다. ``user.tag.enabled`` 가 ``true`` 인 동안에는 문서에 대한 변경(추가·삭제한 경로, 이름 변경, 삭제)이 큐에 들어가 1분마다 실행되는 「Log Aggregator」( ``log_aggregator`` ) 작업으로 반영됩니다. ``false`` 인 동안에는 큐에 들어가지 않으므로, 태그 기능을 활성화한 뒤 「Tag Updater」( ``tag_updater`` ) 작업을 실행하십시오. :doc:`../../admin/tagtype-guide` 를 참조하십시오.

사용 예시
=========

로그인한 모든 사용자와 태그 공유
--------------------------------

.. code-block:: bash

    # paths, seq_no, primary_term 을 포함해 태그를 가져오기
    curl "http://localhost:8080/api/admin/tagtype/setting/0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 권한에 {role}guest 를 추가해 다시 보내기
    curl -X PUT "http://localhost:8080/api/admin/tagtype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
           "seq_no": 12,
           "primary_term": 1,
           "name": "to-review",
           "owner": "alice",
           "paths": "https://www.example.com/a.html\nhttps://www.example.com/b.html",
           "permissions": "{user}alice\n{role}guest",
           "sort_order": 0
         }'

사용자의 태그 목록 조회
-----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/tagtype/settings" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"owner": "alice", "size": 50, "page": 1}'

참고 정보
=========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`../api-tag` - 태그 API
- :doc:`../../admin/tagtype-guide` - 태그 관리 가이드
