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


제안 기능
--------

배치한 검색 폼에 제안 기능을 설정할 수도 있습니다.
설정하는 경우 다음 코드를 </body> 앞에 추가하십시오.

::

    <script type="text/javascript" src="https://search.n2sm.co.jp/js/jquery-3.6.3.min.js"></script>
    <script type="text/javascript" src="https://search.n2sm.co.jp/js/suggestor.js"></script>
    <script>
    $(function() {
      $('#query').suggestor({
        ajaxinfo : {
          url : 'https://search.n2sm.co.jp/api/v1/suggest-words',
          fn :  ["_default", "content", "title"],
          num : 10
        },
        boxCssInfo: {
          border: "1px solid rgba(82, 168, 236, 0.5)",
          "-webkit-box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
          "-moz-box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
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

"z-index"로 지정하는 값은 다른 요소와 겹치지 않는 값을 지정하십시오.
