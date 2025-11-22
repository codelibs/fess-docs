========================================================
Fess로 만드는 Elasticsearch 기반 검색 서버 〜 API 편
========================================================

들어가며
========

이번에는 Fess가 제공하는 API를 이용하여 클라이언트 사이드(브라우저 측)에서 검색과 그 결과 표시를 하는 방법을 소개합니다.
API를 이용하는 것으로 기존 웹 시스템에도 Fess를 검색 서버로 이용하여 HTML만의 변경으로 조합하는 것도 가능해집니다.

본 기사에서는 Fess 15.3.0을 이용하여 설명합니다.
Fess 구축 방법에 관해서는\ `도입편 <https://fess.codelibs.org/ja/articles/article-1.html>`__\ 을 참조하세요.

대상 독자
========

-  기존 웹 시스템에 검색 기능을 추가하고 싶은 분

필요한 환경
==========

이 기사의 내용에 관해서는 다음 환경에서 동작 확인을 하고 있습니다.

-  Google Chrome 120 이후

JSON API
========

Fess는 평소의 HTML에 의한 검색 표현 외에 API로서 JSON에 의한 검색 결과의 응답이 가능합니다.
API를 이용하는 것으로 Fess 서버를 구축해 두고, 기존 시스템에서 검색 결과만을 문의해 가는 것도 간단하게 실현할 수 있습니다.
검색 결과를 개발 언어에 의존하지 않는 형식으로 다룰 수 있으므로 Fess를 Java 이외의 시스템에도 통합하기 쉽다고 생각합니다.

Fess가 제공하는 API가 어떤 응답을 반환하는지에 관해서는 `JSON 응답 <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__ 을 참조하세요.

Fess는 내부 검색 엔진으로 OpenSearch를 이용하고 있습니다.
OpenSearch도 JSON에 의한 API를 제공하고 있지만 Fess의 API는 다른 것입니다.
OpenSearch의 API가 아니라 Fess의 API를 이용하는 메리트는, Fess의 API를 이용하는 것으로 검색 로그 관리나 열람 권한 제어 등 다양한 Fess 고유의 기능을 이용할 수 있는 것을 들 수 있습니다.
문서 크롤 구조를 제로부터 독자적으로 개발하고 싶은 경우에는 OpenSearch를 이용하는 것이 좋다고 생각하지만, 간단하게 검색 기능을 추가하고 싶다는 것이라면 Fess를 이용하여 많은 개발 비용을 절감할 수 있습니다.

JSON API를 이용한 검색 사이트 구축
==================================

이번에는 Fess의 API를 이용한 사이트를 구축하는 방법을 설명합니다.
Fess 서버와의 교류에는 JSON 응답을 이용합니다.
이번에 이용하는 Fess 서버는 Fess 프로젝트에서 데모용으로 공개하고 있는 Fess 서버를 이용하고 있습니다.
만약 독자적인 Fess 서버를 이용하고 싶은 경우에는 Fess 15.3.0 이후의 버전을 설치하세요.

JSON과 CORS
-----------

JSON으로 접속할 때에는 Same-Origin 정책에 주의할 필요가 있습니다.
이에 따라 브라우저에서 표시하는 HTML을 출력하는 서버와 Fess 서버가 동일한 도메인에 존재하는 경우에는 JSON을 이용할 수 있지만, 다른 경우에는 CORS(Cross-Origin Resource Sharing)를 이용할 필요가 있습니다.
이번에는 HTML이 놓여 있는 서버와 Fess 서버가 다른 도메인에 있는 경우로 이야기를 진행합니다.
Fess는 CORS에 대응하고 있으며, 설정값은 app/WEB-INF/classes/fess_config.properties에서 설정 가능합니다. 기본값으로는 다음이 설정되어 있습니다.

::

    api.cors.allow.origin=*
    api.cors.allow.methods=GET, POST, OPTIONS, DELETE, PUT
    api.cors.max.age=3600
    api.cors.allow.headers=Origin, Content-Type, Accept, Authorization, X-Requested-With
    api.cors.allow.credentials=true

이번에는 기본 설정을 이용하지만, 설정을 변경한 경우에는 Fess를 재시작하세요.


작성하는 파일
----------------

이번에는 HTML 상에서 JavaScript를 이용하여 검색 처리를 구현합니다.
JavaScript의 라이브러리로 jQuery를 이용하고 있습니다.
작성하는 파일은 다음과 같습니다.

-  검색 폼과 검색 결과를 표시하는 HTML 파일 "index.html"

- Fess 서버와 통신하는 JS 파일 "fess.js"

이번 구축 예에서는 다음 기능을 구현하고 있습니다.

-  검색 버튼으로 검색 리퀘스트 송신

-  검색 결과 일람

-  검색 결과 페이징 처리

HTML 파일 작성
------------------

먼저 검색 폼과 검색 결과를 표시하는 HTML을 작성합니다.
이번에는 이해하기 쉽도록 CSS로 디자인을 조정하지 않고 간단한 태그 구성으로 하였습니다.
이용하는 HTML 파일은 다음과 같습니다.

index.html의 내용
::

    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>검색 사이트</title>
    </head>
    <body>
    <div id="header">
      <form id="searchForm">
        <input id="searchQuery" type="text" name="query" size="30"/>
        <input id="searchButton" type="submit" value="검색"/>
        <input id="searchStart" type="hidden" name="start" value="0"/>
        <input id="searchNum" type="hidden" name="num" value="20"/>
      </form>
    </div>
    <div id="subheader"></div>
    <div id="result"></div>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script type="text/javascript" src="fess.js"></script>
    </body>
    </html>

body 태그 이하를 보면 먼저 id 속성이 header인 div 태그 부분에서 검색 입력란과 검색 버튼이 배치되어 있습니다.
또한, hidden 폼으로 표시 시작 위치(start)와 표시 건수(num)를 보유하고 있습니다.
검색 리퀘스트 송신 후에 JavaScript로 start와 num의 값은 갱신됩니다.
단, 표시 건수는 1페이지당 표시 건수이며, 이번 샘플 코드에서는 표시 건수를 변경하는 기능은 없으므로 num의 값은 변경되지 않습니다.

다음 subheader의 div 태그 부분에서 검색에 히트한 건수 등의 정보가 표시됩니다.
result의 div 태그에서는 검색 결과 및 페이징 링크가 표시됩니다.

마지막으로 jQuery의 JS 파일과 이번에 작성한 "fess.js"의 JavaScript를 읽어들입니다.
jQuery의 JS 파일을 "index.html"과 동일한 디렉터리에 저장해도 상관없지만, 이번에는 Google의 CDN 경유로 취득하도록 하고 있습니다.

JS 파일 작성
----------------

다음으로 Fess 서버와 통신하여 검색 결과를 표시하는 JS 파일 "fess.js"를 작성합니다.
다음 내용으로 "fess.js"를 작성하여 "index.html"과 동일한 디렉터리에 배치합니다.

fess.js의 내용
::

    $(function(){
        // (1) Fess의 URL
        var baseUrl = "http://SERVERNAME:8080/api/v1/documents?q=";
        // (2) 검색 버튼의 jQuery 오브젝트
        var $searchButton = $('#searchButton');

        // (3) 검색 처리 함수
        var doSearch = function(event){
          // (4) 표시 시작 위치, 표시 건수 취득
          var start = parseInt($('#searchStart').val()),
              num = parseInt($('#searchNum').val());
          // 표시 시작 위치 체크
          if(start < 0) {
            start = 0;
          }
          // 표시 건수 체크
          if(num < 1 || num > 100) {
            num = 20;
          }
          // (5) 표시 페이지 정보 취득
          switch(event.data.navi) {
            case -1:
              // 이전 페이지의 경우
              start -= num;
              break;
            case 1:
              // 다음 페이지의 경우
              start += num;
              break;
            default:
            case 0:
              start = 0;
              break;
          }
          // 검색 필드 값을 트림하여 저장
          var searchQuery = $.trim($('#searchQuery').val());
          // (6) 검색 폼이 빈 문자 체크
          if(searchQuery.length != 0) {
            var urlBuf = [];
            // (7) 검색 버튼을 무효로
            $searchButton.attr('disabled', true);
            // (8) URL 구축
            urlBuf.push(baseUrl, encodeURIComponent(searchQuery),
              '&start=', start, '&num=', num);
            // (9) 검색 리퀘스트 송신
            $.ajax({
              url: urlBuf.join(""),
              dataType: 'json',
            }).done(function(data) {
              // 검색 결과 처리
              var dataResponse = data.response;
              // (10) 상태 체크
              if(dataResponse.status != 0) {
                alert("검색 중에 문제가 발생했습니다. 관리자에게 문의하세요.");
                return;
              }

              var $subheader = $('#subheader'),
                  $result = $('#result'),
                  record_count = dataResponse.record_count,
                  offset = 0,
                  buf = [];
              if(record_count == 0) { // (11) 검색 결과가 없는 경우
                // 서브 헤더 영역에 출력
                $subheader[0].innerHTML = "";
                // 결과 영역에 출력
                buf.push("<b>", dataResponse.q, "</b>에 일치하는 정보를 찾을 수 없습니다.");
                $result[0].innerHTML = buf.join("");
              } else { // (12) 검색에 히트한 경우
                var page_number = dataResponse.page_number,
                    startRange = dataResponse.start_record_number,
                    endRange = dataResponse.end_record_number,
                    i = 0,
                    max;
                offset = startRange - 1;
                // (13) 서브 헤더에 출력
                buf.push("<b>", dataResponse.q, "</b>의 검색 결과 ",
                  record_count, "건 중 ", startRange, " - ",
                  endRange, "건 (", dataResponse.exec_time,
                    "초)");
                $subheader[0].innerHTML = buf.join("");

                // 검색 결과 영역 클리어
                $result.empty();

                // (14) 검색 결과 출력
                var $resultBody = $("<ol/>");
                var results = dataResponse.result;
                for(i = 0, max = results.length; i < max; i++) {
                  buf = [];
                  buf.push('<li><h3 class="title">', '<a href="',
                    results[i].url_link, '">', results[i].title,
                    '</a></h3><div class="body">', results[i].content_description,
                    '<br/><cite>', results[i].site, '</cite></div></li>');
                  $(buf.join("")).appendTo($resultBody);
                }
                $resultBody.appendTo($result);

                // (15) 페이지 번호 정보 출력
                buf = [];
                buf.push('<div id="pageInfo">', page_number, '페이지<br/>');
                if(dataResponse.prev_page) {
                  // 이전 페이지로의 링크
                  buf.push('<a id="prevPageLink" href="#">&lt;&lt;이전 페이지로</a> ');
                }
                if(dataResponse.next_page) {
                  // 다음 페이지로의 링크
                  buf.push('<a id="nextPageLink" href="#">다음 페이지로&gt;&gt;</a>');
                }
                buf.push('</div>');
                $(buf.join("")).appendTo($result);
              }
              // (16) 페이지 정보 갱신
              $('#searchStart').val(offset);
              $('#searchNum').val(num);
              // (17) 페이지 표시를 상부로 이동
              $(document).scrollTop(0);
            }).always(function() {
              // (18) 검색 버튼을 유효로
              $searchButton.attr('disabled', false);
            });
          }
          // (19) 서브밋하지 않으므로 false 반환
          return false;
        };

        // (20) 검색 입력란에서 Enter 키가 눌렸을 때의 처리
        $('#searchForm').submit({navi:0}, doSearch);
        // (21) 이전 페이지 링크가 눌렸을 때의 처리
        $('#result').on("click", "#prevPageLink", {navi:-1}, doSearch)
        // (22) 다음 페이지 링크가 눌렸을 때의 처리
          .on("click", "#nextPageLink", {navi:1}, doSearch);
      });

"fess.js"의 처리는 HTML 파일의 DOM이 구축된 후에 실행됩니다.
먼저 1에서 구축한 Fess 서버의 URL을 지정하고 있습니다.

2는 검색 버튼의 jQuery 오브젝트를 저장해 둡니다.
몇 번이나 검색 버튼의 jQuery 오브젝트를 이용하기 때문에 변수에 보유하여 재이용합니다.

3에서는 검색 처리 함수를 정의하고 있습니다. 이 함수의 내용은 다음 절에서 설명합니다.

20은 검색 폼이 서브밋되었을 때의 이벤트를 등록합니다.
검색 버튼이 클릭되었을 때나 검색 입력란에서 Enter 키가 클릭되었을 때에 20에서 등록된 처리가 실행됩니다.
이벤트가 발생했을 때에 검색 처리 함수 doSearch를 호출합니다.
navi의 값은 검색 처리 함수를 호출할 때 전달되며, 그 값은 페이징 처리를 하기 위해 이용됩니다.

21과 22에서 페이징 처리로 추가되는 링크가 클릭되었을 때의 이벤트를 등록합니다.
이러한 링크는 동적으로 추가되므로 delegate에 의해 이벤트를 등록할 필요가 있습니다.
이러한 이벤트에서도 20과 마찬가지로 검색 처리 함수를 호출합니다.

검색 처리 함수 doSearch
--------------------

3의 검색 처리 함수 doSearch에 대해 설명합니다.

4에서 표시 시작 위치와 표시 건수를 취득합니다.
이러한 값은 header 영역의 검색 폼에서 hidden 값으로 저장되어 있습니다.
표시 시작 위치는 0 이상, 표시 건수는 1부터 100까지의 값을 상정하고 있으므로, 그 외의 값이 취득되는 경우에는 기본값을 설정합니다.

5에서는 doSearch가 이벤트 등록되었을 때에 전달된 파라미터 navi의 값을 판정하여 표시 시작 위치를 수정합니다.
여기서는 -1이 이전 페이지로의 이동, 1이 다음 페이지의 이동, 그 외는 선두 페이지로의 이동으로 변경됩니다.

6은 검색 입력란의 값이 입력되어 있으면 검색을 실행하고, 비어 있으면 아무것도 하지 않고 처리를 종료하기 위한 판정을 합니다.

7에서 더블 서브밋 방지를 위해 Fess 서버에 문의하는 동안은 검색 버튼을 무효로 합니다.

8에서는 Ajax의 리퀘스트를 보내기 위한 URL을 조립합니다.
1의 URL에 검색어, 표시 시작 위치, 표시 건수를 결합합니다.

9에서 Ajax의 리퀘스트를 송신합니다.
리퀘스트가 정상적으로 반환되면 success의 함수가 실행됩니다.
success의 인수에는 Fess 서버로부터 반환된 검색 결과의 오브젝트가 전달됩니다.

먼저 10에서 레스폰스의 상태 내용을 확인하고 있습니다.
정상적으로 검색 리퀘스트가 처리된 경우에는 0이 설정되어 있습니다.
Fess의 JSON 응답 상세는\ `Fess 사이트 <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__\ 를 확인하세요.

검색 리퀘스트가 정상적으로 처리되어 검색 결과가 히트하지 않은 경우에는 11의 조건문 내에서 subheader 영역의 내용을 비우고, result 영역에서 검색 결과가 히트하지 않았다는 메시지를 표시합니다.

검색 결과가 히트한 경우, 12의 조건문 내에서는 검색 결과의 처리를 합니다.
13에서는 subheader 영역에 표시 건수나 실행 시간의 메시지를 설정합니다.
14는 검색 결과를 result 영역에 추가해 갑니다.
검색 결과는 data.response.result에 배열로 저장되어 있습니다.
results[i].〜로 접속하는 것으로 검색 결과 문서의 필드값을 취득할 수 있습니다.

15에서 현재 표시하고 있는 페이지 번호와, 이전 페이지와 다음 페이지로의 링크를 result 영역에 추가합니다.
16에서는 검색 폼의 hidden에 현재의 표시 시작 위치와 표시 건수를 저장합니다.
표시 시작 위치와 표시 건수는 다음번 검색 리퀘스트 시에 재차 이용됩니다.

다음으로 17에서 페이지 표시 위치를 변경합니다.
다음 페이지로의 링크가 클릭되었을 때에 페이지 자체는 갱신되지 않기 때문에 scrollTop에 의해 페이지 선두로 이동합니다.

18에서는 검색 처리가 완료 후에 검색 버튼을 유효로 합니다.
리퀘스트가 성공해도 실패해도 실행되도록 complete에서 불리도록 합니다.

19는 검색 처리 함수가 불린 후에 폼이나 링크가 송신되지 않도록 false를 반환하고 있습니다.
이에 따라 페이지 전환이 발생하는 것을 막습니다.

실행
----

"index.html"에 브라우저로 접속합니다.
다음과 같이 검색 폼이 표시됩니다.

검색 폼
|image1|

적당한 검색어를 입력하고 검색 버튼을 클릭하면 검색 결과가 표시됩니다.
기본 표시 건수는 20건이지만, 히트한 검색 건수가 많은 경우에는 검색 결과 일람 아래에 다음 페이지로의 링크가 표시됩니다.

검색 결과
|image2|

정리
======

Fess의 JSON API를 이용하여 jQuery 기반의 클라이언트 검색 사이트를 구축해 보았습니다.
JSON API를 이용하는 것으로 브라우저 기반의 애플리케이션에 한정되지 않고 별도의 애플리케이션에서 호출하여 Fess를 이용하는 시스템도 구축할 수 있습니다.

또한, 본 기사의 샘플 코드에서는 기존 API 엔드포인트 형식을 나타내고 있지만, Fess 15.3에서는 ``/api/v1/documents`` 엔드포인트 이용이 권장됩니다.
상세는 `API 사양 <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__ 을 참조하세요.

참고 자료
========

-  `Fess <https://fess.codelibs.org/ja/>`__

-  `jQuery <http://jquery.com/>`__

.. |image0| image:: ../../resources/images/en/article/4/sameorigin.png
.. |image1| image:: ../../resources/images/en/article/4/searchform.png
.. |image2| image:: ../../resources/images/en/article/4/searchresult.png
