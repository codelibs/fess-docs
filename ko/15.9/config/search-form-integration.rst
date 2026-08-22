==============
검색 폼 배치
==============

검색 폼 배치 방법
=================

기존 사이트에 검색 폼을 배치하여 |Fess| 의 검색 결과로 유도할 수 있습니다.
여기서는 https://search.n2sm.co.jp/ 에 |Fess| 를 구축하고, 기존 사이트의 각 페이지에 검색 폼을 배치하는 예로 설명합니다.

검색 폼
---------

페이지 내에서 검색 폼을 배치하고 싶은 곳에 다음 코드를 배치하십시오.

::

    <form id="searchForm" method="get" action="https://search.n2sm.co.jp/search/">
    <input id="query" type="text" name="q" maxlength="1000" autocomplete="off">
    <input type="submit" name="search" value="검색">
    </form>

사이트 디자인에 맞춰 class 속성에 클래스 이름을 추가하는 등 CSS로 필요에 따라 조정하십시오.
https://search.n2sm.co.jp/ 의 URL은 구축한 |Fess| 서버의 URL로 변경하여 사용하십시오.

검색 키워드는 ``q`` 파라미터로 |Fess| 의 검색 페이지(``/search/``)로 전송됩니다.
``maxlength`` 에는 |Fess| 측의 키워드 길이 상한인 ``query.max.length`` (초기값은 ``1000``)에 맞춘 값을 지정하십시오.


제안 기능
--------

배치한 검색 폼에 제안 기능을 설정할 수도 있습니다.
설정하는 경우 다음 코드를 </body> 앞에 추가하십시오.

::

    <script type="text/javascript" src="https://search.n2sm.co.jp/js/jquery-3.7.1.min.js"></script>
    <script type="text/javascript" src="https://search.n2sm.co.jp/js/suggestor.js"></script>
    <script>
    $(function() {
      $('#query').suggestor({
        ajaxinfo : {
          url : 'https://search.n2sm.co.jp/api/v2/suggest-words',
          fn :  ["_default", "content", "title"],
          num : 10
        },
        boxCssInfo: {
          border: "1px solid rgba(82, 168, 236, 0.5)",
          "box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
          "background-color": "#fff",
          "z-index": "10000"
        },
        minterm: 2,
        adjustWidthVal : 11,
        searchForm : $('#searchForm')
      });
    });
    </script>

이미 사이트에서 jQuery를 사용하고 있는 경우 jQuery의 script 요소는 추가할 필요가 없습니다.

제안 기능은 |Fess| 의 제안 API(``/api/v2/suggest-words``)를 사용합니다.
``url`` 은 구축한 |Fess| 서버의 URL에 맞춰 변경하십시오.

``suggestor`` 에 지정할 수 있는 주요 옵션은 다음과 같습니다.

.. list-table:: suggestor 의 주요 옵션
   :header-rows: 1
   :widths: 25 75

   * - 옵션
     - 설명
   * - ``ajaxinfo.url``
     - 제안 API의 URL. |Fess| 서버의 ``/api/v2/suggest-words`` 를 지정합니다.
   * - ``ajaxinfo.fn``
     - 제안 대상으로 하는 필드 이름의 배열. 초기값인 ``["_default", "content", "title"]`` 을 그대로 사용할 수 있습니다.
   * - ``ajaxinfo.num``
     - 표시할 후보의 최대 개수.
   * - ``ajaxinfo.lang``
     - 제안 후보를 좁히는 언어(생략 가능).
   * - ``minterm``
     - 제안을 시작하는 최소 입력 문자 수.
   * - ``adjustWidthVal``
     - 제안 표시 영역의 폭을 입력란의 폭에 더하여 조정하는 값(픽셀).
   * - ``searchForm``
     - 후보를 선택했을 때 전송하는 검색 폼 요소.
   * - ``boxCssInfo``
     - 제안 표시 영역에 적용하는 CSS.
   * - ``listSelectedCssInfo``
     - 선택 중인 후보에 적용하는 CSS(생략 가능).
   * - ``listDeselectedCssInfo``
     - 비선택 후보에 적용하는 CSS(생략 가능).

"z-index"로 지정하는 값은 다른 요소와 겹치지 않는 값을 지정하십시오.

.. note::
    검색 폼을 |Fess| 서버와 다른 도메인의 페이지에 배치하는 경우, 제안 API에 대한 요청은 교차 출처(cross-origin) 통신이 됩니다.
    |Fess| 는 초기 설정에서 모든 출처를 허용(``api.cors.allow.origin=*``)하므로 그대로 사용할 수 있습니다.
    액세스를 제한하려면 ``fess_config.properties`` 의 ``api.cors.allow.origin`` 을 변경하십시오.

.. note::
    ``/api/v2/suggest-words`` 는 |Fess| 본체가 제공하는 API입니다.
    이전 버전에서 사용하던 ``/api/v1/suggest-words`` 는 |Fess| 본체에서는 더 이상 제공되지 않으며, 사용하려면 ``fess-webapp-v1-api`` 플러그인을 설치해야 합니다.
    새로 구축하는 경우 ``/api/v2/suggest-words`` 를 사용하십시오.
