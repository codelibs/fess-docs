=====================================
기존 사이트에 검색창과 검색 화면 넣기
=====================================

시작하며
========

사내 포털이나 제품 사이트에 검색을 붙이고 싶을 때, 이용자에게 Fess의 URL을 기억하게 하는 것은 현실적이지 않습니다.
늘 열어 두는 페이지의 헤더에 검색창이 있고, 결과 화면도 그 사이트의 일부로 보이는 것이 요구됩니다.

이 글에서는 Fess 15.9를 사용하여, 브라우저 쪽만으로 완결되는 다음 3가지 방법을 차례로 시도합니다.

- 기존 페이지에 HTML 검색 폼을 두고, Fess의 검색 화면에 결과를 표시한다
- Fess Site Search(FSS)를 사용하여, 기존 사이트의 페이지 안에 검색 결과를 표시한다
- Fess 검색 화면(테마)의 모양을 기존 사이트에 맞게 바꾼다

아울러 검색 결과의 링크 대상을 이용자가 접근할 수 있는 URL로 바꾸는 "경로 매핑"도 설정합니다.

업무 시스템의 서버에서 검색 API를 호출하여 자체 화면을 만드는 방법은 :doc:`guide-11`\ 에서 다룹니다.

전제 조건
=========

- :doc:`guide-02`\ 의 절차대로 Docker Compose의 Fess 15.9가 ``http://localhost:8080/``\ 에서 동작하고 있고, 무언가 하나를 크롤링해 두었을 것
- 기존 사이트 대신 사용할 로컬 HTML 파일

기존 사이트는 Fess와 다른 오리진(스킴·호스트·포트의 조합)에 있는 것이 일반적입니다.
이 글에서도 같은 조건으로 만들기 위해, HTML 파일을 둔 디렉터리에서 다음 명령을 실행하고 ``http://localhost:8000/``\ 에서 엽니다.

::

    $ python3 -m http.server 8000

방법 선택
=========

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * - 방법
     - 검색 결과를 표시하는 곳
     - Fess 쪽에 필요한 것
   * - 검색 폼
     - Fess 검색 화면(``/search``)으로 이동하여 표시
     - 없음
   * - Fess Site Search
     - 기존 사이트의 페이지 안
     - 플러그인 ``fess-webapp-v1-api``
   * - 테마 변경
     - Fess 검색 화면(모양을 바꿈)
     - 테마 ZIP(또는 [일반]의 설정)

검색 폼과 테마 변경은 함께 사용할 수 있습니다.
기존 사이트에서 이동한 곳의 화면도 같은 모양으로 하고 싶다면 둘 다 설정합니다.

검색 폼을 두고 Fess 검색 화면으로 보내기
========================================

폼 두기
-------

기존 페이지에서 검색창을 두고 싶은 위치에 다음 폼을 작성합니다.

.. code-block:: html

    <form method="get" action="http://localhost:8080/search">
      <input type="text" name="q" maxlength="1000" autocomplete="off">
      <button type="submit">검색</button>
    </form>

검색어는 ``q`` 파라미터로 Fess의 ``/search``\ 에 전송되고, Fess 검색 화면에 결과가 표시됩니다.
``maxlength``\ 는 Fess 쪽 검색어 길이의 상한인 ``query.max.length``\ (초기값 ``1000``)에 맞춘 것입니다.
운영 환경에서는 ``action``\ 의 URL을 이용자가 접근하는 Fess의 URL로 바꾸십시오.

특정 라벨의 문서만 검색하게 하려면, 라벨 값을 ``fields.label``\ 로 함께 보냅니다.

.. code-block:: html

    <form method="get" action="http://localhost:8080/search">
      <input type="text" name="q" maxlength="1000" autocomplete="off">
      <input type="hidden" name="fields.label" value="intranet">
      <button type="submit">검색</button>
    </form>

``intranet``\ 은 [크롤러] > [라벨]에서 만든 라벨의 값입니다.
존재하지 않는 값을 보내면 결과는 0건이 됩니다.
라벨을 만드는 방법은 :doc:`guide-04`\ 를 참조하십시오.

확인하기
--------

1. ``http://localhost:8000/``\ 에서 HTML 파일을 열고, 크롤링한 문서에 포함된 단어로 검색합니다
2. 브라우저가 ``http://localhost:8080/search?q=...``\ 로 이동하고 Fess 검색 화면에 결과가 표시되면 완료입니다

결과가 0건이라면 같은 단어를 ``http://localhost:8080/``\ 의 검색창에서 검색하여 비교합니다.
여기서도 0건이라면 폼이 아니라 크롤링이나 퍼미션의 문제입니다.

서제스트에 대하여
-----------------

`검색 폼 배치 <https://fess.codelibs.org/ko/stable/config/search-form-integration.html>`__ 페이지에는 폼에 서제스트를 붙이는 예가 있습니다.
다만 이 예가 읽어 들이는 ``/js/suggestor.js``\ 와 ``/js/jquery-3.7.1.min.js``\ 는 15.9의 Fess에 포함되어 있지 않으므로, 15.9에서는 이 예 그대로는 동작하지 않습니다.
폼 부분(``q``\ 를 ``/search``\ 로 보내는 부분)은 그대로 사용할 수 있습니다.

기존 사이트의 검색창에 서제스트를 표시하고 싶다면 다음 중 하나를 사용합니다.

- 다음 절의 Fess Site Search에서 서제스트를 활성화한다
- 자체 스크립트에서 ``/api/v2/suggest-words``\ 를 호출한다(API 사용법은 :doc:`guide-11` 참조)

Fess 검색 화면으로 이동한 후에는 Fess에 포함된 테마가 서제스트를 표시합니다.

Fess Site Search로 페이지 안에 결과 표시하기
============================================

Fess Site Search(FSS)는 기존 사이트의 페이지에 검색 폼과 검색 결과를 표시하는 JavaScript입니다.
이용자는 기존 사이트에서 이동하지 않고 검색할 수 있습니다.

FSS의 JavaScript는 Fess에서 제공되지 않습니다.
FSS JS Generator(https://fss-generator.codelibs.org/)에서 생성한 파일을 다운로드하여 기존 사이트의 서버에 둡니다.

v1 API 플러그인 설치하기
------------------------

FSS는 Fess의 ``/api/v1``\ 을 호출합니다.
15.9의 Fess 본체가 제공하는 것은 ``/api/v2``\ 뿐이며, ``/api/v1``\ 은 플러그인 ``fess-webapp-v1-api``\ 가 제공합니다.
이 플러그인은 Docker 이미지에 포함되어 있지 않습니다.

Docker Compose에서는 ``compose.yaml``\ 의 ``fess01``\ 의 ``environment``\ 에 다음 줄을 추가합니다.

.. code-block:: yaml

    - "FESS_PLUGINS=fess-webapp-v1-api:15.9.0"

이미 다른 플러그인을 지정하고 있다면 같은 값 안에 공백으로 구분하여 나열합니다.
저장했으면 2개의 Compose 파일을 지정하여 ``up -d``\ 를 실행합니다.
``fess01``\ 이 다시 만들어지고, 기동 시에 플러그인이 설치됩니다.
컨테이너가 다시 만들어지므로 [시스템] > [일반]에서 바꾼 설정은 ``down``\ 했을 때와 마찬가지로 원래대로 돌아갑니다(:doc:`guide-02`\ 의 중지와 재개에 관한 절 참조).

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

관리 화면의 [시스템] > [플러그인] > [설치]에서도 설치할 수 있습니다(설치 후 Fess를 재시작해야 합니다).
다만 Docker에서는 플러그인이 컨테이너 안에 놓이므로, ``down``\ 으로 컨테이너를 다시 만들면 사라집니다.
``FESS_PLUGINS``\ 로 지정해 두면 다시 만들 때마다 다시 설치됩니다.

``fess01``\ 이 healthy가 되면 API가 응답하는지 확인합니다.

::

    $ curl 'http://localhost:8080/api/v1/documents?q=fess'

``"record_count"``\ 를 포함한 JSON이 반환되면 준비가 끝난 것입니다.
404가 반환되면 플러그인이 설치되어 있지 않은 것입니다.
이때 ``fess.log``\ 에는 ``No plugin serves the legacy API``\ 로 시작하는 WARN이 한 번만 출력됩니다.
플러그인이 설치되어 있는데도 JSON이 반환되지 않는다면, [시스템] > [일반]의 "JSON 응답"이 꺼져 있지 않은지 확인합니다.
"JSON 응답"을 끄면 ``/api/v1``\ 뿐 아니라 ``/api/v2``\ 도 응답하지 않게 되어, Fess 자체의 검색 화면도 사용할 수 없게 됩니다.

JavaScript 생성하여 두기
------------------------

1. https://fss-generator.codelibs.org/\ 를 열고, 제너레이터에서 배색이나 글꼴을 지정한 후 [Generate]를 클릭합니다
2. [Download JS]로 JavaScript 파일을 다운로드합니다
3. 파일 이름을 ``fess-ss.js``\ 로 바꾸고, HTML 파일과 같은 디렉터리에 둡니다

검색 결과를 표시하는 페이지(예: ``result.html``)에 다음 코드를 작성합니다.

.. code-block:: html

    <script src="fess-ss.js"></script>

    <div class="fess-site-search">
      <fess-search-form
        language="ko"
        :enable-suggest="true"
        suggest-url="http://localhost:8080"
      ></fess-search-form>
      <fess-search-result
        fess-url="http://localhost:8080"
        language="ko"
      ></fess-search-result>
    </div>

``fess-url``\ 은 검색에 사용하는 Fess의 URL, ``suggest-url``\ 은 서제스트에 사용하는 Fess의 URL입니다.
운영 환경에서는 이용자의 브라우저에서 접근할 수 있는 Fess의 URL로 합니다.

다른 페이지의 헤더에는 검색 폼만 둡니다.

.. code-block:: html

    <script src="fess-ss.js"></script>

    <div class="fess-site-search">
      <fess-search-form result-page="result.html"></fess-search-form>
    </div>

폼은 검색어를 ``fss.query`` 파라미터에 넣어 ``result.html``\ 로 이동하고, ``result.html``\ 의 FSS가 검색을 실행합니다.
FSS를 읽어 들이지 않는 페이지에서 보내는 경우에도, ``result.html?fss.query=검색어`` 형태로 이동하는 폼을 작성하면 같은 방식으로 동작합니다.

그 밖의 속성(한 페이지의 건수 ``:page-size``, 라벨로 좁히기 ``:enable-label``, 링크를 새 탭에서 열기 ``link-target="_blank"`` 등)은 FSS JS Generator의 매뉴얼을 참조하십시오.

확인하기
--------

1. ``http://localhost:8000/result.html``\ 을 열고 검색 폼에서 검색합니다
2. 페이지 안에 검색 결과가 표시되면 완료입니다
3. 표시되지 않는 경우에는 브라우저 개발자 도구의 네트워크 탭에서 ``/api/v1/documents``\ 로의 요청을 확인합니다. 404라면 플러그인을, CORS 오류라면 다음 항목을 확인합니다

주의할 점
---------

브라우저에서 보면, ``localhost:8000``\ 의 페이지에서 ``localhost:8080``\ 의 API를 호출하는 것은 크로스 오리진 통신입니다.
Fess는 초기 설정에서 ``api.cors.allow.origin=*``\ 로 되어 있어, 어떤 오리진에서의 호출도 받아들입니다.
호출 측을 기존 사이트로 제한하고 싶은 경우의 설정은 :doc:`guide-11`\ 에서 다룹니다.

FSS가 다른 오리진에서 호출하는 검색은, 이용자가 Fess에 로그인해 있더라도 로그인하지 않은 이용자(게스트)의 검색으로 취급됩니다.
FSS는 Cookie를 붙이지 않고 API를 호출하며, 초기 설정인 ``api.cors.allow.origin=*``\ 에서는 자격 증명을 붙인 크로스 오리진 통신도 허용되지 않기 때문입니다.
따라서 결과에 나오는 것은 퍼미션에 ``{role}guest``\ 를 가진 문서뿐입니다.
부서별로 보여 줄 문서를 바꾸려면, 이용자가 Fess 검색 화면에서 로그인하도록 합니다(:doc:`guide-05` 참조).

Fess 검색 화면의 모양 바꾸기
============================

15.9의 검색 화면은 HTML·CSS·JavaScript를 묶은 "테마"로 표시됩니다.
이전 버전에 있던 [페이지 디자인]이나 JSP 편집은 없습니다.
아무것도 설정하지 않았다면 포함된 테마 ``bootstrap``\ 이 사용됩니다.

ZIP을 만들지 않고 바꿀 수 있는 것
---------------------------------

[시스템] > [일반]의 "알림 표시"에 있는 "검색 상단 페이지"에 작성한 내용은 포함된 테마의 검색 상단과 검색 결과 화면에 표시됩니다.
HTML도 작성할 수 있지만, ``<script>``\ 나 ``<style>`` 등은 제거됩니다.
사내용 안내를 한 줄 표시하고 싶을 뿐이라면 테마를 만들 필요가 없습니다.

공개된 테마 사용하기
--------------------

Fess 프로젝트는 문서 검색용인 ``docsearch`` 등의 테마를 공개하고 있습니다.

1. [시스템] > [테마]를 엽니다
2. "테마 설치"의 "이름"에서 테마를 고르고 [선택]을 클릭합니다
3. "버전"에서 15.9용 버전(``15.9.x``)을 고르고 [설치]를 클릭합니다
4. 목록 위의 "기본 테마"에서 설치한 테마를 고르고 [설정]을 클릭합니다

``http://localhost:8080/``\ 을 다시 열면 새 테마로 표시됩니다.
"(기본값 없음)"을 고르고 [설정]을 클릭하면 포함된 ``bootstrap``\ 으로 돌아갑니다.

포함된 테마를 복제하여 로고와 배색 바꾸기
-----------------------------------------

포함된 테마는 직접 편집할 수 없고, ``bootstrap``\ 이라는 이름의 테마를 업로드로 교체할 수도 없습니다.
다른 이름으로 복제하여 변경합니다.
여기서는 ``mytheme``\ 으로 합니다.

1. 컨테이너에서 포함된 테마를 꺼냅니다

   ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml cp fess01:/usr/share/fess/app/themes/bootstrap ./mytheme

2. ``mytheme/theme.yml``\ 의 ``name``\ 을 ``mytheme``\ 으로, ``displayName``\ 을 ``My Theme`` 등으로 바꿉니다
3. 다음 파일을 변경합니다

   - 배색·레이아웃: ``assets/styles.css``
   - 로고: ``assets/logo-head.png``\ (헤더)와 ``assets/logo.png``\ (검색 상단)
   - 푸터의 조직명: ``i18n/messages.ko.json``\ 의 ``footer.copyright_org``\ (영어 화면은 ``messages.en.json``)

4. ``theme.yml``\ 이 ZIP의 루트에 오도록 묶습니다

   ::

       $ cd mytheme && zip -r ../mytheme.zip . && cd ..

5. [시스템] > [테마]의 [업로드]에서 ``mytheme.zip``\ 을 업로드합니다
6. "기본 테마"에서 ``mytheme``\ 을 고르고 [설정]을 클릭합니다

``index.html``\ 은 변경하지 않습니다.
포함된 ``index.html``\ 은 테마 안의 파일을 ``{{themePath}}/assets/...`` 형태로 참조합니다.
Fess가 제공 시에 ``{{themePath}}``\ 를 ``themes/mytheme``\ 으로 바꾸므로, 이름만 바꾸면 복제한 테마의 파일이 읽혀 들어갑니다.

확인하기
--------

``http://localhost:8080/``\ 을 다시 열고 로고와 배색이 바뀌었는지 확인합니다.
바뀌지 않았다면 개발자 도구의 네트워크 탭에서 스타일시트가 ``/themes/mytheme/assets/styles.css``\ 에서 읽혀 들어오는지 봅니다.
``/themes/bootstrap/``\ 에서 읽혀 들어온다면 기본 테마 설정이 반영되지 않은 것입니다.

테마에서 주의할 점
------------------

- 검색 화면에는 스크립트·스타일·이미지의 취득처를 Fess 자신으로 제한하는 ``Content-Security-Policy`` 헤더가 붙습니다. 외부 CDN의 글꼴이나 스크립트는 읽혀 들어오지 않으므로 테마 ZIP에 넣으십시오
- 검색 화면은 다른 페이지의 ``iframe``\ 에는 표시되지 않습니다(``theme.index.frame.ancestors``\ 의 초기값이 ``'none'``\ 이기 때문입니다). 포털 안에 검색 결과를 표시하고 싶다면 FSS를 사용합니다
- Docker의 ``fess01``\ 에는 볼륨이 없습니다. 업로드한 테마는 컨테이너 안에 놓이고 기본 테마 설정은 ``system.properties``\ 에 저장되므로, ``down``\ 으로 컨테이너를 다시 만들면 둘 다 사라집니다. 평소에는 ``stop``/``start``\ 를 사용하고, 다시 만든 후에는 업로드와 설정을 다시 합니다
- 포함된 테마는 해당 버전 Fess의 ``/api/v2``\ 에 맞추어 만들어져 있습니다. Fess를 업그레이드했다면 새로 포함된 테마에서 다시 복제하여 변경 사항을 다시 적용하십시오

테마의 구조나 ``theme.yml``\ 의 항목은 `테마 개발 가이드 <https://fess.codelibs.org/ko/stable/dev/theme-development.html>`__\ 를 참조하십시오.

검색 결과의 링크 대상을 이용자용 URL로 하기
===========================================

크롤링에는 사내용 호스트 이름을 사용하고, 이용자에게는 포털의 URL로 열게 하고 싶은 경우가 있습니다.
예를 들어 ``http://intranet-web01:8080/docs/``\ 를 크롤링하고, 검색 결과에서는 ``https://portal.example.com/docs/``\ 를 열게 하는 경우입니다.
이때는 경로 매핑으로 표시할 때만 URL을 바꿉니다.

1. [크롤러] > [경로 매핑]을 열고 [새로 만들기]를 클릭합니다
2. 다음과 같이 입력하고 [작성]을 클릭합니다

   .. list-table::
      :header-rows: 1
      :widths: 25 75

      * - 항목
        - 값
      * - 정규 표현식
        - ``^http://intranet-web01:8080/docs/``
      * - 치환
        - ``https://portal.example.com/docs/``
      * - 처리 종류
        - 표시
      * - 표시 순서
        - ``0``

"표시"는 검색 결과에 표시하는 URL과 링크 대상만 바꿉니다.
인덱스에 저장된 URL은 바뀌지 않으므로 재크롤링이 필요 없고, 저장한 시점부터 검색 결과에 반영됩니다.
"크롤링"이나 "크롤링/표시"를 고르면 바꾼 URL이 인덱스에 저장됩니다.
표시만 바꾸고 싶은데 이것들을 고르면 이후 크롤링의 URL까지 바뀌므로 주의하십시오.

확인하려면 대상 문서가 나오는 단어로 검색하여, 결과의 URL과 링크 대상이 ``https://portal.example.com/docs/...``\ 로 되어 있는지 봅니다.
API로 결과를 받는 경우, 바꾼 URL이 들어가는 곳은 ``url``\ 이 아니라 ``url_link``\ 입니다(:doc:`guide-11` 참조).

파일 서버의 경로를 Web 서버의 URL로 바꾸는 예는 `경로 매핑 <https://fess.codelibs.org/ko/stable/admin/pathmap-guide.html>`__\ 을 참조하십시오.

다음에 읽을 글
==============

- 업무 시스템의 서버에서 검색 API를 호출하고 싶다: :doc:`guide-11`
- 포털에 표시할 문서를 부서별로 바꾸고 싶다: :doc:`guide-05`
- 웹 사이트와 파일 서버를 한꺼번에 검색하고 라벨로 나누고 싶다: :doc:`guide-04`
- 조직별로 다른 테마나 검색 대상을 보여 주고 싶다: :doc:`guide-13`
- 검색 화면에 로그인을 필수로 하고 싶다: :doc:`guide-15`

참고 자료
=========

- `검색 폼 배치 <https://fess.codelibs.org/ko/stable/config/search-form-integration.html>`__
- `테마 <https://fess.codelibs.org/ko/stable/admin/theme-guide.html>`__
- `테마 개발 가이드 <https://fess.codelibs.org/ko/stable/dev/theme-development.html>`__
- `경로 매핑 <https://fess.codelibs.org/ko/stable/admin/pathmap-guide.html>`__
- `플러그인 <https://fess.codelibs.org/ko/stable/admin/plugin-guide.html>`__
- `FSS JS Generator <https://fss-generator.codelibs.org/>`__
- `fess-site-search(GitHub) <https://github.com/codelibs/fess-site-search>`__
- `fess-webapp-v1-api(GitHub) <https://github.com/codelibs/fess-webapp-v1-api>`__
