==========
UI 설정 API
==========

개요
====

UI 설정 API 는 싱글 페이지 애플리케이션 (SPA) 이 필요로 하는 초기 설정 (테마, 기능 플래그, 페이지네이션 상한, CSRF 가 필요한 경우 새 CSRF 토큰) 을 반환합니다.
이 엔드포인트는 로그인 전에 익명으로 호출됩니다.

공통 응답 엔벨로프 및 오류 모델에 대해서는 :doc:`api-overview` 를 참조하십시오.

UI 설정 취득
============

요청
----

==================  ====================================================
HTTP 메서드          GET
엔드포인트           ``/api/v2/ui/config``
==================  ====================================================

SPA 가 필요로 하는 초기 설정을 반환합니다.

응답
----

성공 시 (HTTP 200, UiConfigResponse) 에는 다음과 같은 공통 엔벨로프 형식의 응답이 반환됩니다 (일부 발췌).

.. code-block:: json

    {
      "response": {
        "status": 0,
        "site_name": "Fess",
        "login_required": false,
        "locales": ["en", "ja"],
        "theme": {
          "name": "default",
          "display_name": "Default Theme",
          "version": "1.0.0",
          "supported_locales": ["en", "ja"]
        },
        "features": {
          "user_favorite": false,
          "popular_word": true,
          "suggest_search_log": true,
          "suggest_documents": true,
          "login_required": false,
          "eoled": false,
          "development_mode": false,
          "search_log_enabled": true,
          "thumbnail_enabled": true,
          "display_label_type": false,
          "clipboard_copy_icon": true,
          "eol_link": "",
          "installation_link": "https://fess.codelibs.org/15.8/install/",
          "login_link": true,
          "rag_chat_enabled": false
        },
        "page_size_default": 20,
        "page_size_max": 100,
        "sort_options": [
          {"value": "", "label_key": "labels.search_result_sort_score_desc"}
        ],
        "num_options": [10, 20, 30, 40, 50, 100],
        "lang_options": [
          {"value": "all", "label_key": "labels.searchoptions_all_langs"},
          {"value": "ja", "label_key": "labels.lang_ja"}
        ],
        "label_options": [],
        "notifications": {
          "search_top": "",
          "advance_search": "",
          "login": ""
        },
        "facet_views": [],
        "filetype_options": [
          {"value": "html", "label_key": "labels.facet_filetype_html"}
        ],
        "csrf_required": true,
        "csrf_token": "0c1f2e3d4a5b6c7d8e9f"
      }
    }

``response`` 의 각 요소에 대해서는 다음과 같습니다. 모든 필드는 필수입니다.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: 응답 정보
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 타입
     - 설명
   * - ``site_name``
     - string
     - 사이트 이름. 활성 테마가 매니페스트를 포함하는 경우 해당 표시 이름( ``display_name`` )이며, 그렇지 않으면 ``Fess`` 입니다.
   * - ``login_required``
     - boolean
     - 로그인이 필요한지 여부.
   * - ``locales``
     - string[]
     - 사용 가능한 로케일 배열.
   * - ``theme``
     - object
     - 활성 테마 디스크립터. 자세한 내용은 아래 표를 참조하십시오.
   * - ``features``
     - object
     - 기능 플래그. 자세한 내용은 아래 표를 참조하십시오.
   * - ``page_size_default``
     - integer
     - 기본 페이지 크기.
   * - ``page_size_max``
     - integer
     - 페이지 크기의 최대값.
   * - ``sort_options``
     - object[]
     - 검색 UI 용 정렬 옵션. 자세한 내용은 아래 표를 참조하십시오.
   * - ``num_options``
     - integer[]
     - 선택 가능한 페이지 크기 배열. ``page_size_max`` 를 초과하지 않는 값으로 좁혀집니다.
   * - ``lang_options``
     - object[]
     - 언어 필터 옵션. 자세한 내용은 아래 표를 참조하십시오.
   * - ``label_options``
     - object[]
     - 설정된 레이블 옵션. 자세한 내용은 아래 표를 참조하십시오.
   * - ``notifications``
     - object
     - 특정 뷰 상단에 표시할 HTML 알림 스니펫. 자세한 내용은 아래 표를 참조하십시오.
   * - ``facet_views``
     - object[]
     - 설정된 패싯 쿼리 뷰 그룹. 자세한 내용은 아래 표를 참조하십시오.
   * - ``filetype_options``
     - object[]
     - 고급 검색 폼용 파일 타입 패싯 옵션. 자세한 내용은 아래 표를 참조하십시오.
   * - ``csrf_required``
     - boolean
     - CSRF 토큰이 필요한지 여부.
   * - ``csrf_token``
     - string
     - ``csrf_required`` 가 ``false`` 인 경우 빈 문자열, 그 외에는 현재 세션에 연결된 새 토큰.

theme
~~~~~

``theme`` 는 항상 존재하지만, 요청에 커스텀 테마가 연결되지 않은 경우 빈 객체가 됩니다.
매니페스트 유래 키 ( ``display_name`` / ``version`` / ``supported_locales`` ) 는 활성 테마가 매니페스트를 포함하는 경우에만 존재합니다.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: theme
   :header-rows: 1
   :widths: 28 15 57

   * - 필드
     - 타입
     - 설명
   * - ``name``
     - string
     - 테마 이름.
   * - ``display_name``
     - string
     - 테마 표시 이름.
   * - ``version``
     - string
     - 테마 버전.
   * - ``supported_locales``
     - string[]
     - 테마가 지원하는 로케일 배열.

features
~~~~~~~~

모든 필드가 필수입니다.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: features
   :header-rows: 1
   :widths: 28 15 57

   * - 필드
     - 타입
     - 설명
   * - ``user_favorite``
     - boolean
     - 사용자 즐겨찾기 기능이 활성화되어 있는지 여부.
   * - ``popular_word``
     - boolean
     - 인기 검색어 기능이 활성화되어 있는지 여부.
   * - ``suggest_search_log``
     - boolean
     - 검색 로그에 의한 자동완성이 활성화되어 있는지 여부.
   * - ``suggest_documents``
     - boolean
     - 문서에 의한 자동완성이 활성화되어 있는지 여부.
   * - ``login_required``
     - boolean
     - 로그인이 필요한지 여부.
   * - ``eoled``
     - boolean
     - 이 |Fess| 빌드가 EOL 에 도달했는지 여부.
   * - ``development_mode``
     - boolean
     - 내장 (개발용) 검색 엔진을 사용 중일 때 ``true`` 가 됩니다.
   * - ``search_log_enabled``
     - boolean
     - 검색 로그가 활성화되어 있는지 여부.
   * - ``thumbnail_enabled``
     - boolean
     - 썸네일이 활성화되어 있는지 여부.
   * - ``display_label_type``
     - boolean
     - 레이블이 1개 이상 설정되어 있을 때 ``true`` 가 됩니다.
   * - ``clipboard_copy_icon``
     - boolean
     - 클립보드 복사 아이콘을 표시할지 여부.
   * - ``eol_link``
     - string
     - 해결된 EOL 정보 URL. EOL 이 아니거나 해결할 수 없을 때는 빈 문자열입니다.
   * - ``installation_link``
     - string
     - 해결된 설치 가이드 URL. 해결할 수 없을 때는 빈 문자열입니다.
   * - ``login_link``
     - boolean
     - 로그인 링크를 표시해야 하는지 여부.
   * - ``rag_chat_enabled``
     - boolean
     - RAG 채팅 기능이 사용 가능한지 여부.

sort_options
~~~~~~~~~~~~

검색 UI 용 정렬 옵션 배열입니다.
각 요소는 ``value`` 와 ``label_key`` 를 가집니다.
``click_count.*`` 항목은 검색 로그가 활성화된 경우에만, ``favorite_count.*`` 항목은 사용자 즐겨찾기가 활성화된 경우에만 존재합니다.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: sort_options 요소
   :header-rows: 1
   :widths: 28 15 57

   * - 필드
     - 타입
     - 설명
   * - ``value``
     - string
     - 정렬 값.
   * - ``label_key``
     - string
     - 레이블 키.

num_options
~~~~~~~~~~~

선택 가능한 페이지 크기의 정수 배열입니다. ``page_size_max`` 를 초과하지 않는 값으로 좁혀집니다.

lang_options
~~~~~~~~~~~~

언어 필터 옵션 배열입니다.
각 요소는 ``value`` 와 ``label_key`` 를 가집니다.
첫 번째 요소는 ``all`` 센티넬이며, 이후 지원 언어 코드별로 1항목씩 나열됩니다.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: lang_options 요소
   :header-rows: 1
   :widths: 28 15 57

   * - 필드
     - 타입
     - 설명
   * - ``value``
     - string
     - 언어 값.
   * - ``label_key``
     - string
     - 레이블 키.

label_options
~~~~~~~~~~~~~

설정된 레이블 옵션 배열입니다. 레이블이 미정의인 경우 빈 배열이 됩니다.
각 요소는 ``value`` 와 ``name`` 을 가집니다.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: label_options 요소
   :header-rows: 1
   :widths: 28 15 57

   * - 필드
     - 타입
     - 설명
   * - ``value``
     - string
     - 레이블 값.
   * - ``name``
     - string
     - 레이블 이름.

notifications
~~~~~~~~~~~~~

특정 뷰 상단에 표시할 HTML 알림 스니펫입니다. 빈 문자열은 해당 뷰에 알림이 없음을 의미합니다.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: notifications
   :header-rows: 1
   :widths: 28 15 57

   * - 필드
     - 타입
     - 설명
   * - ``search_top``
     - string
     - 검색 상단에 표시할 알림.
   * - ``advance_search``
     - string
     - 고급 검색에 표시할 알림.
   * - ``login``
     - string
     - 로그인에 표시할 알림.

facet_views
~~~~~~~~~~~

설정된 패싯 쿼리 뷰 그룹 배열입니다. 미정의인 경우 빈 배열이 됩니다.
각 요소는 ``group_name`` 과 ``queries`` 를 가집니다.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: facet_views 요소
   :header-rows: 1
   :widths: 28 15 57

   * - 필드
     - 타입
     - 설명
   * - ``group_name``
     - string
     - 그룹 이름.
   * - ``queries``
     - object[]
     - 해당 그룹의 패싯 쿼리 배열. 각 요소는 ``label_key`` (string) 와 ``value`` (string) 를 가집니다.

filetype_options
~~~~~~~~~~~~~~~~

고급 검색 폼용 파일 타입 패싯 옵션 배열입니다.
각 요소는 ``value`` 와 ``label_key`` 를 가집니다.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: filetype_options 요소
   :header-rows: 1
   :widths: 28 15 57

   * - 필드
     - 타입
     - 설명
   * - ``value``
     - string
     - 파일 타입 값.
   * - ``label_key``
     - string
     - 레이블 키.

오류 응답
---------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답
   :header-rows: 1
   :widths: 25 75

   * - 상태 코드
     - 설명
   * - 405 Method Not Allowed
     - 지원되지 않는 HTTP 메서드가 지정된 경우.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.
