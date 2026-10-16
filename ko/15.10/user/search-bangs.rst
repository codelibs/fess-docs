=============================
뱅 검색(다른 사이트에서 검색)
=============================

뱅(bang)은 |Fess| 에서 검색하는 대신 다른 사이트로 검색을 보내는 기능입니다. DuckDuckGo의 뱅과 같은 방식으로, 검색어에 ``!`` 와 짧은 트리거 단어를 넣으면 |Fess| 가 나머지 검색어를 그 트리거 단어가 가리키는 사이트로 보냅니다.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 검색어
     - 전송 대상
   * - ``airplane !g``
     - Google에서 ``airplane`` 검색
   * - ``!w Ohm's law``
     - Wikipedia에서 ``Ohm's law`` 검색
   * - ``!g``
     - Google 홈페이지
   * - ``airplane !unknown``
     - |Fess| 에서의 일반 검색 (``!`` 는 NOT을 뜻합니다. :doc:`search-not` 참조)

뱅은 ``fess-webapp-bangs`` 플러그인이 제공하며, |Fess| 15.10 이상이 필요합니다. 관리 화면의 [시스템 > 플러그인] 또는 ``bin/fess-setup install plugin fess-webapp-bangs`` 로 설치하고(:doc:`../admin/plugin-guide` 참조) |Fess| 를 재시작합니다.

뱅으로 인식되는 조건
====================

- 뱅은 ``!`` 뒤에 트리거 단어가 붙은 것이며, 독립된 단어로 작성합니다. 트리거 단어는 대소문자를 구분하지 않습니다.
- 뱅은 검색어에서 제거되고, 나머지 검색어가 뱅의 URL로 전송됩니다.
- 정의된 뱅이 검색어에 여러 개 있으면 첫 번째 것만 유효합니다.
- 정의되지 않은 트리거 단어는 뱅이 아닙니다. ``!unknown`` 은 평소처럼 검색되며 단어 ``unknown`` 을 제외합니다.
- ``-g`` 와 ``NOT g`` 는 지금까지처럼 단어 ``g`` 를 제외합니다. 뱅이 되는 것은 ``!g`` 뿐입니다.

검색 화면과 ``/api/v2/search`` 는 리디렉션을 따릅니다. API는 ``redirect_url`` 을 반환하고(:doc:`../api/api-search` 참조), |Fess| 에 포함된 ``bootstrap`` 테마가 해당 URL로 이동합니다. 다른 테마에서는 같은 처리가 필요합니다.

채팅, MCP, v1 API와 클래식 JSON API, 관리 화면의 검색처럼 리디렉션할 수 없는 호출자는 다른 사이트로 검색을 보내지 않습니다. 뱅을 제거하고 나머지 검색어로 검색합니다.

뱅 정의
=======

뱅은 시스템 속성 ``bangs.definitions`` 로 정의합니다. ``app/WEB-INF/conf/system.properties`` 에 기술하거나 ``-Dfess.system.bangs.definitions=...`` 로 전달합니다. ``system.properties`` 의 변경은 |Fess| 를 재시작하지 않아도 반영됩니다.

값은 ``트리거 단어=URL`` 항목을 공백으로 구분한 목록입니다. URL 안의 ``{query}`` 는 URL 인코딩된 나머지 검색어로 바뀝니다.

::

    bangs.definitions=g=https://www.google.com/search?q={query} w=https://en.wikipedia.org/wiki/Special:Search?search={query}

- 트리거 단어에는 공백, ``(``, ``)``, ``!``, ``"``, ``=``, ``:`` 를 포함할 수 없습니다.
- 절대 URL인 ``http`` 또는 ``https`` 만 허용됩니다.
- 이 규칙에 맞지 않는 항목은 사용되지 않습니다. |Fess| 로그에 경고가 출력되며 다른 항목은 그대로 유효합니다.
- 같은 트리거 단어를 두 번 정의하면 첫 번째 정의가 사용됩니다.
- 값을 비우면 모든 뱅이 꺼집니다.

``bangs.definitions`` 를 설정하지 않으면 다음 5개의 뱅을 사용할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 트리거 단어
     - 사이트
   * - ``g``
     - Google
   * - ``b``
     - Bing
   * - ``ddg``
     - DuckDuckGo
   * - ``w``
     - Wikipedia (영어)
   * - ``gh``
     - GitHub

``bangs.definitions`` 를 설정하면 이 목록이 대체됩니다. 기본 뱅을 유지한 채 하나를 추가하려면 필요한 항목을 모두 작성하십시오.

관련 항목
=========

- :doc:`search-not` - NOT 검색
- :doc:`special-char` - 특수 문자와 이스케이프
- :doc:`../api/api-search` - 검색 API
