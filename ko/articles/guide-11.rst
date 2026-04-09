===========================================================================
제11회 검색 API로 기존 시스템 확장 -- CRM 및 사내 시스템과의 연동 패턴 모음
===========================================================================

들어가며
========

Fess는 독립적인 검색 시스템으로 사용할 수 있을 뿐만 아니라, 기존 업무 시스템에 검색 기능을 제공하는 "검색 마이크로서비스"로도 활용할 수 있습니다.

이 글에서는 Fess의 API를 사용하여 기존 시스템과 연동하는 구체적인 패턴을 소개합니다.
CRM에 고객 정보 검색 기능을 통합하거나, FAQ 검색 위젯을 구축하거나, 문서 포털을 구성하는 등 실용적인 연동 시나리오를 다룹니다.

대상 독자
=========

- 기존 업무 시스템에 검색 기능을 추가하고 싶은 분
- Fess의 API를 사용한 시스템 연동에 관심이 있는 분
- 웹 애플리케이션 개발에 대한 기본 지식이 있는 분

Fess API의 전체 구조
=====================

Fess가 제공하는 주요 API를 정리합니다.

.. list-table:: Fess API 목록
   :header-rows: 1
   :widths: 25 45 30

   * - API
     - 용도
     - 엔드포인트
   * - 검색 API
     - 문서의 전문 검색
     - ``/api/v1/documents``
   * - 라벨 API
     - 사용 가능한 라벨 조회
     - ``/api/v1/labels``
   * - 서제스트 API
     - 자동 완성 후보 조회
     - ``/api/v1/suggest-words``
   * - 인기 검색어 API
     - 인기 검색 키워드 조회
     - ``/api/v1/popular-words``
   * - 헬스 API
     - 시스템 가동 상태 확인
     - ``/api/v1/health``
   * - 관리 API
     - 설정 조작 (CRUD)
     - ``/api/admin/*``

액세스 토큰
-----------

API를 사용할 때는 액세스 토큰을 통한 인증이 권장됩니다.

1. 관리 화면의 [시스템] > [액세스 토큰]에서 액세스 토큰을 생성
2. API 요청의 헤더에 토큰을 포함

::

    Authorization: Bearer {액세스 토큰}

토큰에는 역할을 할당할 수 있으며, API를 통한 검색에도 역할 기반의 검색 결과 제어가 적용됩니다.

패턴 1: CRM에 검색 기능 통합
==============================

시나리오
--------

영업팀이 사용하는 CRM 시스템에 고객 관련 문서의 검색 기능을 추가합니다.
CRM의 고객 화면에서 해당 고객과 관련된 제안서, 회의록, 계약서 등을 횡단 검색할 수 있도록 합니다.

구현 접근 방식
--------------

CRM의 고객 화면에 검색 위젯을 삽입합니다.
고객 이름을 검색 쿼리로 Fess API에 전송하고, 결과를 CRM 화면 내에 표시합니다.

.. code-block:: javascript

    // CRM 화면 내의 검색 위젯
    async function searchCustomerDocs(customerName) {
      const params = new URLSearchParams({
        q: customerName,
        num: '5',
        'fields.label': 'sales-docs'
      });
      const url = `https://fess.example.com/api/v1/documents?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      return await response.json();
    }

포인트
------

- ``fields.label`` 로 영업 관련 문서로 범위를 한정
- ``num`` 으로 표시 건수를 제한 (CRM 화면 내 공간에 맞춤)
- 고객 이름뿐만 아니라 프로젝트 이름이나 프로젝트 번호로도 검색할 수 있으면 편리

패턴 2: FAQ 검색 위젯
=======================

시나리오
--------

사내 문의 대응 시스템에 FAQ 검색 위젯을 추가합니다.
직원이 문의를 접수하기 전에 관련 FAQ를 검색하여 자체 해결을 유도합니다.

구현 접근 방식
--------------

서제스트 API와 검색 API를 결합하여 입력 중에 실시간으로 후보를 표시합니다.

.. code-block:: javascript

    // 입력 중 서제스트
    async function getSuggestions(query) {
      const params = new URLSearchParams({ q: query, num: '5' });
      const url = `https://fess.example.com/api/v1/suggest-words?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      const data = await response.json();
      return data.data;
    }

서제스트 API는 사용자가 키워드를 입력하는 중에 후보를 표시하기 위해 사용합니다.
사용자가 키워드를 확정하고 검색을 실행하면 검색 API로 상세한 검색 결과를 가져옵니다.

포인트
------

- 서제스트 API는 실시간성이 중요하므로 응답 속도를 확인
- FAQ 카테고리를 라벨로 관리하고, 카테고리별 필터링도 제공
- 인기 검색어 API로 "자주 검색되는 키워드"를 표시하여 사용자의 검색을 지원

패턴 3: 문서 포털
===================

시나리오
--------

사내 문서 관리 포털을 구축합니다.
카테고리별 브라우징과 전문 검색을 결합한 인터페이스를 제공합니다.

구현 접근 방식
--------------

라벨 API로 카테고리 목록을 가져오고, 검색 API로 카테고리 내의 문서를 가져옵니다.

.. code-block:: javascript

    // 라벨 목록 조회
    async function getLabels() {
      const url = 'https://fess.example.com/api/v1/labels';
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      const data = await response.json();
      return data.data;
    }

    // 라벨로 필터링한 검색
    async function searchByLabel(query, label) {
      const params = new URLSearchParams({
        q: query || '*',
        'fields.label': label,
        num: '20',
        sort: 'last_modified.desc'
      });
      const url = `https://fess.example.com/api/v1/documents?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      return await response.json();
    }

포인트
------

- 라벨 API로 카테고리 목록을 동적으로 조회 (라벨의 추가/삭제가 API 측에 즉시 반영)
- ``sort=last_modified.desc`` 로 최신 문서를 상위에 표시
- ``q=*`` 로 키워드 없이 브라우징 (전체 조회)도 가능

패턴 4: 콘텐츠 인덱싱 API
===========================

시나리오
--------

외부 시스템이 생성하는 데이터 (로그, 리포트, 챗봇의 응답 기록 등)를 Fess의 인덱스에 등록하여 검색 대상으로 만들고자 합니다.

구현 접근 방식
--------------

Fess의 관리 API를 사용하여 외부에서 문서를 인덱스에 등록할 수 있습니다.

관리 API의 문서 엔드포인트를 사용하여 제목, URL, 본문 등의 정보를 POST 요청으로 전송합니다.

포인트
------

- 크롤링으로는 가져올 수 없는 데이터 소스의 통합에 유효
- 배치 처리로 여러 문서를 일괄 등록하는 것도 가능
- 액세스 토큰의 권한을 적절히 설정하고, 쓰기 권한을 제한

API 연동 모범 사례
====================

오류 처리
----------

API 연동에서는 네트워크 장애나 Fess 서버의 유지보수에 대비한 오류 처리가 중요합니다.

- 타임아웃 설정: 검색 API 호출에 적절한 타임아웃을 설정
- 재시도 로직: 일시적인 오류에 대한 재시도 (최대 3회 정도)
- 폴백: Fess가 응답하지 않을 경우의 대체 표시 ("검색 서비스를 현재 이용할 수 없습니다" 등)

성능 고려 사항
--------------

- 응답 캐시: 동일한 쿼리의 결과를 단시간 캐시
- 검색 결과 건수 제한: 필요한 건수만 조회 (``num`` 파라미터)
- 필드 지정: 필요한 필드만 조회하여 응답 크기를 축소

보안
----

- HTTPS 통신 사용
- 액세스 토큰의 로테이션
- 토큰의 권한을 최소한으로 설정 (읽기 전용 등)
- CORS의 적절한 설정

정리
====

이 글에서는 Fess의 API를 사용한 기존 시스템과의 연동 패턴을 소개했습니다.

- **CRM 연동**: 고객 화면에서의 관련 문서 검색
- **FAQ 위젯**: 서제스트 + 검색의 실시간 후보 표시
- **문서 포털**: 라벨 API를 활용한 카테고리 브라우징
- **콘텐츠 인덱싱**: 외부 데이터의 API를 통한 등록

Fess의 API는 REST 기반으로 심플하기 때문에 다양한 시스템과의 연동이 용이합니다.
기존 시스템에 검색 기능을 "사후에" 추가할 수 있다는 것이 Fess의 큰 강점 중 하나입니다.

다음 회에서는 SaaS나 데이터베이스의 데이터를 검색 가능하게 만드는 시나리오를 다룹니다.

참고 자료
=========

- `Fess 검색 API <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__

- `Fess 관리 API <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__
