=======================
검색 로그 시각화 설정
=======================

검색 로그 시각화에 대하여
========================

|Fess| 에서는 사용자의 검색 로그 및 클릭 로그를 수집합니다.
수집한 검색 로그를 `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__ 를 사용하여 데이터 분석 및 시각화를 할 수 있습니다.

시각화 가능한 정보
----------------

기본 설정에서는 다음 정보를 시각화할 수 있습니다.

-  검색 결과 표시에 걸리는 평균 시간
-  초당 검색 횟수
-  접속 사용자의 User Agent 순위
-  검색 키워드 순위
-  검색 결과가 0건인 검색 키워드 순위
-  검색 결과 총 개수
-  시계열 검색 트렌드

Visualize 기능을 사용하여 새 그래프를 생성하고 Dashboard에 추가하여 독자적인 모니터링 대시보드를 구축할 수 있습니다.

OpenSearch Dashboards를 통한 데이터 시각화 설정
==============================================

OpenSearch Dashboards 설치
------------------------------------

OpenSearch Dashboards는 |Fess| 에서 사용하는 OpenSearch의 데이터를 시각화하는 도구입니다.
`OpenSearch 공식 문서 <https://opensearch.org/docs/latest/install-and-configure/install-dashboards/index/>`__ 에 따라 OpenSearch Dashboards를 설치합니다.

설정 파일 편집
------------------

OpenSearch Dashboards에 |Fess| 에서 사용하는 OpenSearch를 인식시키기 위해 설정 파일 ``config/opensearch_dashboards.yml`` 을 편집합니다.

::

    opensearch.hosts: ["http://localhost:9201"]

``localhost`` 는 환경에 맞게 적절한 호스트명이나 IP 주소로 변경하십시오.
|Fess| 의 기본 설정에서는 OpenSearch가 9201 포트에서 시작됩니다.

.. note::
   OpenSearch의 포트 번호가 다른 경우 적절한 포트 번호로 변경하십시오.

OpenSearch Dashboards 시작
-----------------------------

설정 파일을 편집한 후 OpenSearch Dashboards를 시작합니다.

::

    $ cd /path/to/opensearch-dashboards
    $ ./bin/opensearch-dashboards

시작 후 브라우저에서 ``http://localhost:5601`` 에 접속합니다.

인덱스 패턴 설정
--------------------------

1. OpenSearch Dashboards 홈 화면에서 "Management" 메뉴를 선택합니다.
2. "Index Patterns"를 선택합니다.
3. "Create index pattern" 버튼을 클릭합니다.
4. Index pattern name에 ``fess_log*`` 를 입력합니다.
5. "Next step" 버튼을 클릭합니다.
6. Time field에서 ``requestedAt`` 을 선택합니다.
7. "Create index pattern" 버튼을 클릭합니다.

이것으로 |Fess| 의 검색 로그를 시각화하기 위한 준비가 완료되었습니다.

시각화 및 대시보드 생성
----------------------------

기본 시각화 생성
~~~~~~~~~~~~~~~~~~~~

1. 왼쪽 메뉴에서 "Visualize"를 선택합니다.
2. "Create visualization" 버튼을 클릭합니다.
3. 시각화 유형(꺾은선 그래프, 원 그래프, 막대 그래프 등)을 선택합니다.
4. 생성한 인덱스 패턴 ``fess_log*`` 를 선택합니다.
5. 필요한 메트릭이나 버킷(집계 단위)을 설정합니다.
6. "Save" 버튼을 클릭하여 시각화를 저장합니다.

대시보드 생성
~~~~~~~~~~~~~~~~~~~~

1. 왼쪽 메뉴에서 "Dashboard"를 선택합니다.
2. "Create dashboard" 버튼을 클릭합니다.
3. "Add" 버튼을 클릭하여 생성한 시각화를 추가합니다.
4. 레이아웃을 조정하고 "Save" 버튼을 클릭하여 저장합니다.

시간대 설정
------------------

시간 표시가 올바르지 않은 경우 시간대를 설정합니다.

1. 왼쪽 메뉴에서 "Management"를 선택합니다.
2. "Advanced Settings"를 선택합니다.
3. ``dateFormat:tz`` 를 검색합니다.
4. 시간대를 적절한 값(예: ``Asia/Seoul`` 또는 ``UTC``)으로 설정합니다.
5. "Save" 버튼을 클릭합니다.

로그 데이터 확인
----------------

1. 왼쪽 메뉴에서 "Discover"를 선택합니다.
2. 인덱스 패턴 ``fess_log*`` 를 선택합니다.
3. 검색 로그 데이터가 표시됩니다.
4. 오른쪽 상단의 시간 범위 선택에서 표시할 기간을 지정할 수 있습니다.

주요 검색 로그 필드
----------------------

|Fess| 의 검색 로그에는 다음과 같은 정보가 포함됩니다.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 필드 이름
     - 설명
   * - ``queryId``
     - 검색 쿼리의 고유 식별자
   * - ``searchWord``
     - 검색 키워드
   * - ``requestedAt``
     - 검색이 실행된 날짜 및 시간
   * - ``responseTime``
     - 검색 결과의 응답 시간(밀리초)
   * - ``queryTime``
     - 쿼리 실행 시간(밀리초)
   * - ``hitCount``
     - 검색 결과 히트 건수
   * - ``userAgent``
     - 사용자의 브라우저 정보
   * - ``clientIp``
     - 클라이언트 IP 주소
   * - ``languages``
     - 사용 언어
   * - ``roles``
     - 사용자의 역할 정보
   * - ``user``
     - 사용자 이름(로그인 시)

이러한 필드를 활용하여 다양한 관점에서 검색 로그를 분석할 수 있습니다.

문제 해결
----------------------

데이터가 표시되지 않는 경우
~~~~~~~~~~~~~~~~~~~~~~~~

- OpenSearch가 올바르게 시작되어 있는지 확인하십시오.
- ``opensearch_dashboards.yml`` 의 ``opensearch.hosts`` 설정이 올바른지 확인하십시오.
- |Fess| 에서 검색이 실행되어 로그가 기록되어 있는지 확인하십시오.
- 인덱스 패턴의 시간 범위가 적절히 설정되어 있는지 확인하십시오.

연결 오류가 발생하는 경우
~~~~~~~~~~~~~~~~~~~~~~~~

- OpenSearch의 포트 번호가 올바른지 확인하십시오.
- 방화벽이나 보안 그룹 설정을 확인하십시오.
- OpenSearch의 로그 파일에서 오류가 없는지 확인하십시오.
