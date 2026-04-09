===========================================================
Fess로 만드는 Elasticsearch 기반 검색 서버 ~ FSS 편
===========================================================

들어가며
========

구축한 Fess 서버를 이용하여 웹사이트에 검색 서비스를 통합하는 방법을 소개합니다.
Fess Site Search(FSS)가 제공하는 태그와 JavaScript 파일을 이용하면, 기존 웹사이트에 검색 박스와 검색 결과를 표시할 수 있습니다.


대상 독자
========

- 기존 웹사이트에 검색 기능을 추가하고 싶은 분

- Google Site Search나 Google 맞춤 검색 등에서 이전하고 싶은 분


Fess Site Search(FSS)란
===========================

FSS는 검색 서버 Fess를 기존 웹사이트에 도입하는 기능입니다. CodeLibs 프로젝트의 FSS 사이트에서 제공하고 있습니다. Google Site Search(GSS) 등의 사이트 내 검색과 마찬가지로, 검색 서비스를 이용하고 싶은 페이지에 JavaScript 태그를 삽입하는 것만으로 이용할 수 있으므로, GSS에서의 이전도 간단하게 수행할 수 있습니다.

FSS JS란
=============

FSS JS는 Fess의 검색 결과를 표시하는 JavaScript 파일입니다. 이 JavaScript 파일을 웹사이트에 배치하면 검색 결과를 표시할 수 있게 됩니다.
FSS JS는 "https://fss-generator.codelibs.org/"의 FSS JS Generator에서 생성하여 입수할 수 있습니다.
FSS JS는 Fess 11.3 이상의 버전에 대응하고 있으므로, Fess 구축 시 Fess 11.3 이상의 버전을 설치하세요. Fess 구축 방법에 대해서는\ `도입편 <https://fess.codelibs.org/ja/articles/article-1.html>`__\ 을 참조하세요.


FSS JS Generator에서는 검색 폼의 배색이나 글꼴을 지정할 수 있습니다.
"Generate" 버튼을 클릭하면 지정된 설정의 JavaScript 파일을 생성할 수 있습니다.

|image0|

프리뷰 표시에 문제가 없으면 "Download JS" 버튼을 클릭하여 JavaScript 파일을 다운로드하세요.

|image1|

사이트에 도입
================

이번에는 정적 HTML로 만들어진 "`www.n2sm.net`"에 사이트 내 검색을 도입하는 예를 살펴봅니다.

검색 결과는 해당 사이트 내의 search.html에 표시하도록 하고, Fess 서버는 "nss833024.n2search.net"에 별도로 구축합니다.

다운로드한 FSS JS의 JavaScript 파일은 /js/fess-ss.min.js로 사이트에 배치합니다.

위의 정보를 정리하면 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - 대상명
     - URL
   * - 검색 대상 사이트
     - https://www.n2sm.net/
   * - 검색 결과 페이지
     - https://www.n2sm.net/search.html
   * - FSS JS
     - https://www.n2sm.net/js/fess-ss.min.js
   * - Fess 서버
     - https://nss833024.n2search.net/

JavaScript 태그의 삽입은 search.html 내에서 검색 결과를 표시하고 싶은 위치에 다음 태그를 배치합니다.

..
  <script>
    (function() {
      var fess = document.createElement('script');
      fess.type = 'text/javascript';
      fess.async = true;
      // FSS JS의 URL을 src에 설정합니다
      fess.src = 'https://www.n2sm.net/js/fess-ss.min.js';
      fess.charset = 'utf-8';
      fess.setAttribute('id', 'fess-ss');
      // Fess의 검색 API URL을 fess-url에 설정합니다
      fess.setAttribute('fess-url', 'https://nss833024.n2search.net/json');
      var s = document.getElementsByTagName('script')[0];
      s.parentNode.insertBefore(fess, s);
    })();
  </script>
  <fess:search></fess:search>

search.html에 접속하면 검색 폼이 표시됩니다.

검색어를 입력하면 다음과 같이 검색 결과를 표시할 수 있습니다.

|image2|

다른 페이지에 검색 폼을 배치하여 검색 결과를 표시하려면, 다음과 같은 검색 폼을 각 페이지에 배치하고 "`https://www.n2sm.net/search.html?q=검색어`"로 이동하도록 설정하세요.

..
  <form action="https://www.n2sm.net/search.html" method="get">
    <input type="text" name="q">
    <input type="submit" value="검색">
  </form>


정리
======

JavaScript 태그를 배치하는 것만으로 Fess의 검색 결과를 사이트에 통합하는 방법을 소개했습니다.
FSS를 통해 GSS에서의 이전도 기존 JavaScript 태그를 교체하는 것만으로 실현할 수 있습니다.
FSS JS에는 다른 표시 방법이나 검색 로그를 Google Analytics와 연동하는 방법 등도 있습니다. 그 외의 설정 방법에 대해서는 `FSS [매뉴얼] <https://fss-generator.codelibs.org/ja/docs/manual>`__ 을 참조하세요.

참고 자료
========
- `Fess Site Search <https://fss-generator.codelibs.org/ja/>`__

.. |image0| image:: ../../resources/images/ja/article/5/FSS-JS-Generator1.png
.. |image1| image:: ../../resources/images/ja/article/5/FSS-JS-Generator2.png
.. |image2| image:: ../../resources/images/ja/article/5/N2Search-review.png
