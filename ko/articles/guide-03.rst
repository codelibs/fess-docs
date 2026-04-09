============================================================
제3회 사내 포털에 검색을 삽입하기 -- 기존 웹 사이트에 검색 기능 추가 시나리오
============================================================

들어가며
========

지난 회에서는 Docker Compose로 Fess를 기동하고 검색을 체험했습니다.
그러나 실제 업무에서는 "Fess의 검색 화면을 그대로 사용하는" 것뿐만 아니라, "기존 사내 사이트나 포털에 검색 기능을 추가하고 싶다"는 니즈가 많이 있습니다.

본 기사에서는 기존 웹 사이트에 Fess의 검색 기능을 통합하기 위한 3가지 접근 방식을 소개하고, 각각의 특징과 선택 기준을 해설합니다.

대상 독자
========

- 사내 포털이나 웹 사이트에 검색 기능을 추가하고 싶은 분
- 프론트엔드 개발의 기본 지식이 있는 분
- 제2회의 절차에 따라 Fess가 기동 완료된 상태일 것

필요한 환경
==========

- 제2회에서 구축한 Fess 환경(Docker Compose)
- 테스트용 웹 페이지(로컬 HTML 파일도 가능)

3가지 통합 접근 방식
====================

Fess의 검색 기능을 기존 사이트에 통합하는 방법은 크게 3가지가 있습니다.

.. list-table:: 통합 접근 방식의 비교
   :header-rows: 1
   :widths: 15 30 25 30

   * - 접근 방식
     - 개요
     - 개발 공수
     - 적합한 케이스
   * - FSS(Fess Site Search)
     - JavaScript 태그를 삽입하는 것만으로 완료
     - 최소(몇 줄의 코드)
     - 간편하게 검색을 추가하고 싶은 경우
   * - 검색 폼 연계
     - HTML 폼에서 Fess로 이동
     - 소(HTML 수정만)
     - Fess의 검색 화면을 그대로 사용하고 싶은 경우
   * - 검색 API 연계
     - JSON API로 커스텀 UI를 구축
     - 중~대(프론트엔드 개발)
     - 디자인이나 동작을 완전히 커스터마이즈하고 싶은 경우

각각의 방법을 구체적인 시나리오와 함께 해설해 나갑니다.

접근 방식 1: FSS(Fess Site Search)로 간편하게 추가
==================================================

시나리오
--------

사내 포털 사이트가 있으며, HTML의 편집 권한은 있지만 대규모 개수는 피하고 싶다.
최소한의 변경으로 포털에서 사내 문서를 검색할 수 있도록 하고 싶다.

FSS란
--------

Fess Site Search(FSS)는 JavaScript 태그를 웹 페이지에 삽입하는 것만으로 검색 기능을 추가할 수 있는 구조입니다.
검색창과 검색 결과 표시가 모두 JavaScript로 처리되므로, 기존 페이지 구조를 거의 변경할 필요가 없습니다.

구현 절차
--------

1. Fess 관리 화면에서 API의 접근을 허가합니다.
   [시스템] > [전반] 페이지에서 JSON 응답을 유효화해 둡니다.

2. 검색 기능을 추가하고 싶은 페이지에 아래 코드를 삽입합니다.

.. code-block:: html

    <script>
      (function() {
        var fess = document.createElement('script');
        fess.type = 'text/javascript';
        fess.async = true;
        fess.src = 'http://localhost:8080/js/fess-ss.min.js';
        fess.charset = 'utf-8';
        fess.setAttribute('id', 'fess-ss');
        fess.setAttribute('fess-url', 'http://localhost:8080/api/v1/documents');
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(fess, s);
      })();
    </script>

    <fess:search></fess:search>

``<fess:search>`` 태그를 배치한 위치에 검색창과 검색 결과가 표시됩니다.

커스터마이즈
------------

FSS의 외관은 CSS로 커스터마이즈할 수 있습니다.
Fess가 제공하는 기본 스타일을 덮어쓰는 것으로, 기존 사이트의 디자인에 맞출 수 있습니다.

.. code-block:: css

    .fessWrapper {
      font-family: 'Noto Sans JP', sans-serif;
      max-width: 800px;
      margin: 0 auto;
    }
    .fessWrapper .searchButton {
      background-color: #1a73e8;
    }

접근 방식 2: 검색 폼 연계로 심플하게 실현
================================================

시나리오
--------

사내 포털에는 이미 헤더에 내비게이션 바가 있다.
거기에 검색창을 추가하고, 검색 실행 시 Fess의 검색 결과 화면으로 이동시키고 싶다.
JavaScript는 사용하지 않고 HTML만으로 실현하고 싶다.

구현 절차
--------

기존 내비게이션 바에 아래와 같은 HTML 폼을 추가합니다.

.. code-block:: html

    <form action="http://localhost:8080/search" method="get">
      <input type="text" name="q" placeholder="사내 검색..." />
      <button type="submit">검색</button>
    </form>

이것만으로 검색 실행 시 Fess의 검색 결과 화면으로 이동합니다.
Fess 측의 검색 화면 디자인을 커스터마이즈함으로써 통일감 있는 경험을 제공할 수 있습니다.

Fess의 검색 화면 커스터마이즈
----------------------------

Fess의 검색 화면은 JSP 파일로 구성되어 있으며, 관리 화면에서도 편집 가능합니다.

1. 관리 화면의 [시스템] > [페이지 디자인]을 선택
2. 헤더, 푸터, CSS 등을 커스터마이즈

예를 들어, 로고를 사내 포털과 맞추거나 배색을 통일함으로써, 이용자에게 위화감 없는 검색 경험을 제공할 수 있습니다.

패스 매핑의 활용
--------------------

검색 결과에 표시되는 URL을 이용자가 접근하기 쉬운 URL로 변환할 수 있습니다.
예를 들어, 크롤 시의 URL이 ``http://internal-server:8888/docs/`` 이더라도, 검색 결과에는 ``https://portal.example.com/docs/`` 로 표시시킬 수 있습니다.

관리 화면의 [크롤러] > [패스 매핑]에서 설정할 수 있습니다.

접근 방식 3: 검색 API로 완전 커스텀
======================================

시나리오
--------

사내 업무 애플리케이션에 검색 기능을 통합하고 싶다.
디자인이나 검색 결과의 표시 방법을 완전히 제어하고 싶다.
프론트엔드 개발 리소스가 있다.

검색 API의 기본
----------------

Fess는 JSON 기반의 검색 API를 제공하고 있습니다.

::

    GET http://localhost:8080/api/v1/documents?q=검색키워드

응답은 아래와 같은 JSON 형식입니다.

.. code-block:: json

    {
      "record_count": 10,
      "page_count": 5,
      "data": [
        {
          "title": "ドキュメントタイトル",
          "url": "https://example.com/doc.html",
          "content_description": "...検索キーワードを含む本文の抜粋..."
        }
      ]
    }

JavaScript에서의 구현 예
----------------------

아래는 검색 API를 사용한 기본적인 구현 예입니다.

.. code-block:: javascript

    async function searchFess(query) {
      const url = new URL('http://localhost:8080/api/v1/documents');
      url.searchParams.set('q', query);
      const response = await fetch(url);
      const data = await response.json();

      const results = data.data;
      const container = document.getElementById('search-results');
      container.textContent = '';

      results.forEach(item => {
        const div = document.createElement('div');
        const heading = document.createElement('h3');
        const link = document.createElement('a');
        link.href = item.url;
        link.textContent = item.title;
        heading.appendChild(link);
        const desc = document.createElement('p');
        desc.textContent = item.content_description;
        div.appendChild(heading);
        div.appendChild(desc);
        container.appendChild(div);
      });
    }

API의 추가 파라미터
---------------------

검색 API는 다양한 파라미터로 검색 동작을 커스터마이즈할 수 있습니다.

.. list-table:: 주요 API 파라미터
   :header-rows: 1
   :widths: 20 50 30

   * - 파라미터
     - 설명
     - 예
   * - ``q``
     - 검색 키워드
     - ``q=Fess``
   * - ``num``
     - 1페이지당 표시 건수
     - ``num=20``
   * - ``start``
     - 검색 결과의 시작 위치
     - ``start=20``
   * - ``fields.label``
     - 라벨에 의한 필터링
     - ``fields.label=intranet``
   * - ``sort``
     - 정렬 순서
     - ``sort=last_modified.desc``

API를 활용함으로써 검색 결과의 필터링, 정렬, 페이지네이션 등 세밀한 제어가 가능합니다.

어떤 접근 방식을 선택할 것인가
========================

3가지 접근 방식은 상황에 따라 선택합니다.

**FSS를 선택하는 경우**

- 개발 리소스가 한정되어 있다
- 기존 페이지에 최소한의 변경으로 검색을 추가하고 싶다
- 검색 기능의 외관은 표준적인 것으로 충분하다

**검색 폼 연계를 선택하는 경우**

- Fess의 검색 화면 디자인으로 충분하다
- JavaScript를 사용하고 싶지 않다
- 헤더나 사이드바에 검색창을 추가하는 것만으로 충분하다

**검색 API를 선택하는 경우**

- 검색 결과의 표시를 완전히 커스터마이즈하고 싶다
- SPA(Single Page Application)에 통합하고 싶다
- 검색 결과에 독자적인 로직(필터링, 하이라이트 등)을 적용하고 싶다
- 프론트엔드 개발 리소스가 있다

조합도 가능
----------------

이러한 접근 방식은 상호 배타적이지 않습니다.
예를 들어, 톱 페이지에는 FSS로 간편하게 검색 기능을 추가하고, 전용 검색 페이지에서는 API를 사용한 커스텀 UI를 제공하는 조합도 효과적입니다.

정리
======

본 기사에서는 기존 웹 사이트에 Fess의 검색 기능을 통합하는 3가지 접근 방식을 소개했습니다.

- **FSS**: JavaScript 태그의 삽입만으로 검색 기능을 추가
- **검색 폼 연계**: HTML 폼에서 Fess의 검색 화면으로 이동
- **검색 API**: JSON API로 완전히 커스터마이즈된 검색 경험을 구축

어떤 접근 방식이든 Fess의 백엔드가 제공하는 검색 품질을 그대로 활용할 수 있습니다.
요건과 개발 리소스에 따라 최적의 방법을 선택해 주십시오.

다음 회에서는 파일 서버나 클라우드 스토리지 등 여러 데이터 소스를 일원적으로 검색하는 시나리오를 다룹니다.

참고 자료
========

- `Fess Site Search <https://github.com/codelibs/fess-site-search>`__

- `Fess 검색 API <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__
