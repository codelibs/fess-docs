============================================================
제12회: SaaS 데이터를 검색 가능하게 만들기 -- Salesforce 및 데이터베이스 연동 시나리오
============================================================

들어가며
========

기업의 중요한 데이터는 파일 서버나 클라우드 스토리지뿐만 아니라 SaaS 애플리케이션과 데이터베이스에도 저장되어 있습니다.
Salesforce의 고객 정보, 사내 데이터베이스의 제품 마스터, CSV로 관리되는 리스트 데이터 -- 이러한 데이터는 일반적으로 각각의 시스템 내에서만 검색할 수 있습니다.

이 글에서는 SaaS와 데이터베이스의 데이터를 Fess 인덱스에 가져와서 다른 문서와 함께 횡단 검색할 수 있도록 하는 시나리오를 다룹니다.

대상 독자
=========

- SaaS와 데이터베이스 정보도 검색 대상에 포함하고 싶은 분
- 데이터 스토어 플러그인의 활용 방법을 알고 싶은 분
- 여러 데이터 소스를 횡단하는 검색 기반을 구축하고 싶은 분

시나리오
========

어떤 영업 조직에서 다음 시스템에 데이터가 분산되어 있습니다.

.. list-table:: 데이터 소스 현황
   :header-rows: 1
   :widths: 20 35 45

   * - 시스템
     - 저장 데이터
     - 현재 과제
   * - Salesforce
     - 고객 정보, 상담 기록, 활동 이력
     - Salesforce 내에서만 검색 가능
   * - 사내 DB
     - 제품 마스터, 가격표, 재고 정보
     - 전용 관리 화면에서만 접근 가능
   * - CSV 파일
     - 거래처 리스트, 이벤트 참가자 리스트
     - Excel로 열어 육안으로 찾는 수밖에 없음
   * - 파일 서버
     - 제안서, 견적서, 계약서
     - 이미 Fess로 크롤링 완료

목표는 이 모든 데이터를 Fess로 횡단 검색하여 영업 활동에 필요한 정보를 하나의 검색창에서 찾을 수 있도록 하는 것입니다.

Salesforce 데이터 연동
========================

Salesforce 데이터를 Fess에서 검색 가능하게 하려면 Salesforce 데이터 스토어 플러그인을 사용합니다.

플러그인 설치
--------------

1. 관리 화면의 [시스템] > [플러그인]을 선택
2. ``fess-ds-salesforce`` 를 설치

접속 설정
----------

Salesforce와의 연동에는 Connected App 설정이 필요합니다.

**Salesforce 측 준비**

1. Salesforce 설정 화면에서 Connected App을 생성
2. OAuth 설정을 활성화
3. 컨슈머 키와 시크릿을 취득

**Fess 측 설정**

1. [크롤러] > [데이터 스토어] > [새로 만들기]
2. 핸들러 이름: SalesforceDataStore를 선택
3. 파라미터와 스크립트 설정
4. 라벨: ``salesforce`` 를 설정

**파라미터 설정 예**

.. code-block:: properties

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=user@example.com
    password=your-password
    security_token=your-security-token
    client_id=your-consumer-key
    client_secret=your-consumer-secret

**스크립트 설정 예**

.. code-block:: properties

    url=url
    title=title
    content=content
    last_modified=last_modified

``auth_type`` 은 ``oauth_password`` (사용자 이름/비밀번호 인증) 또는 ``oauth_token`` (JWT Bearer 토큰 인증)을 지정합니다. JWT 인증의 경우 ``private_key`` 에 RSA 개인 키를 설정합니다.

대상 데이터 선정
------------------

Salesforce에는 많은 오브젝트가 있지만 모두를 검색 대상으로 할 필요는 없습니다.
영업 팀이 자주 검색하는 오브젝트에 집중합시다.

.. list-table:: 대상 오브젝트 예
   :header-rows: 1
   :widths: 25 35 40

   * - 오브젝트
     - 검색 대상 필드
     - 용도
   * - Account (거래처)
     - 이름, 업종, 주소, 설명
     - 거래처 기본 정보 검색
   * - Opportunity (상담)
     - 이름, 단계, 설명, 금액
     - 진행 중인 상담 검색
   * - Case (케이스)
     - 제목, 설명, 상태
     - 문의 이력 검색

데이터베이스 연동
==================

사내 데이터베이스의 데이터를 검색 가능하게 하려면 데이터베이스 데이터 스토어 플러그인을 사용합니다.

플러그인 설치
--------------

``fess-ds-db`` 플러그인을 설치합니다.
이 플러그인은 JDBC를 통해 다양한 데이터베이스(MySQL, PostgreSQL, Oracle, SQL Server 등)에 접속할 수 있습니다.

설정
-----

1. [크롤러] > [데이터 스토어] > [새로 만들기]
2. 핸들러 이름: DatabaseDataStore를 선택
3. 파라미터와 스크립트 설정
4. 라벨: ``database`` 를 설정

**파라미터 설정 예**

.. code-block:: properties

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://db-server:3306/mydb?useSSL=true
    username=fess_reader
    password=your-password
    sql=SELECT product_id, product_name, description, price, CONCAT('https://internal-app/products/', product_id) AS url FROM products WHERE status = 'active'

**스크립트 설정 예**

.. code-block:: properties

    url=url
    title=product_name
    content=description

``sql`` 에 지정한 SQL 쿼리의 결과가 크롤링됩니다. 스크립트에서는 SQL 컬럼 이름(또는 컬럼 라벨)을 사용하여 Fess 인덱스 필드에 매핑합니다.

SQL 쿼리 설계
---------------

``sql`` 파라미터에 지정하는 SQL 쿼리를 설계할 때의 포인트는 다음과 같습니다.

- 검색 결과의 링크 대상이 되는 ``url`` 컬럼을 포함할 것 (예: ``CONCAT('https://.../', id) AS url``)
- 검색 대상 본문이 되는 컬럼을 포함할 것
- ``WHERE`` 절로 불필요한 데이터를 제외할 것 (예: ``status = 'active'``)

스크립트에서는 SQL 컬럼 이름을 그대로 사용하여 Fess 인덱스 필드에 매핑합니다.

CSV 파일 연동
===============

CSV 파일의 데이터도 검색 대상으로 만들 수 있습니다.

설정
-----

``fess-ds-csv`` 플러그인 또는 CSV 데이터 스토어 기능을 사용합니다.

1. [크롤러] > [데이터 스토어] > [새로 만들기]
2. 핸들러 이름: CsvDataStore를 선택
3. 파라미터와 스크립트 설정
4. 라벨: ``csv-data`` 를 설정

**파라미터 설정 예**

.. code-block:: properties

    directories=/opt/fess/csv-data
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

**스크립트 설정 예** (헤더 행이 있는 경우 컬럼 이름을 사용)

.. code-block:: properties

    url="https://internal-app/contacts/" + id
    title=company_name
    content=company_name + " " + contact_name + " " + email

``has_header_line=true`` 인 경우, 헤더 행의 컬럼 이름을 스크립트에서 사용할 수 있습니다. 헤더 행이 없는 경우에는 ``cell1``, ``cell2``, ``cell3`` 과 같이 열 번호로 참조합니다. 스크립트에는 Groovy 식을 기술할 수 있으며 문자열 결합 등도 가능합니다.

CSV 파일이 정기적으로 갱신되는 경우, 파일 배치 위치를 고정하고 크롤링 스케줄을 설정하면 자동으로 최신 데이터가 인덱스에 반영됩니다.

데이터 소스 횡단 검색
======================

모든 데이터 소스의 설정이 완료되면 횡단 검색을 체험해 봅시다.

검색 예
--------

"ABC 주식회사"로 검색하면 다음과 같은 결과가 반환됩니다.

1. Salesforce 거래처 정보 (Account)
2. 파일 서버의 제안서 (PDF)
3. 데이터베이스의 제품 구매 이력
4. CSV의 전시회 참가자 리스트

이용자는 정보의 소재를 의식하지 않고 필요한 정보에 도달할 수 있습니다.

라벨에 의한 필터링
--------------------

검색 결과가 많은 경우 라벨로 좁힐 수 있습니다.

- ``salesforce``: Salesforce 데이터만
- ``database``: 데이터베이스 데이터만
- ``csv-data``: CSV 데이터만
- ``공유 파일``: 파일 서버 문서만

운용상의 고려 사항
===================

데이터의 신선도
-----------------

SaaS와 데이터베이스의 데이터는 빈번하게 갱신될 가능성이 있습니다.
크롤링 빈도를 적절하게 설정하여 검색 결과의 신선도를 유지합시다.

.. list-table:: 크롤링 빈도 가이드
   :header-rows: 1
   :widths: 25 25 50

   * - 데이터 소스
     - 권장 빈도
     - 이유
   * - Salesforce
     - 4~6시간마다
     - 상담 및 고객 정보는 업무 시간 중에 갱신됨
   * - 데이터베이스
     - 2~4시간마다
     - 재고 정보 등 변동이 큰 데이터
   * - CSV
     - 일 1회
     - 일반적으로 배치 처리로 갱신됨

데이터베이스 접속 보안
-----------------------

데이터베이스에 직접 접속하는 경우 보안에 충분히 주의하십시오.

- 읽기 전용 데이터베이스 사용자를 사용
- 접속 소스를 Fess 서버의 IP로 제한
- 불필요한 테이블에 대한 접근 권한을 부여하지 않음
- 비밀번호 관리에 주의

정리
=====

이 글에서는 Salesforce, 데이터베이스, CSV 파일의 데이터를 Fess에서 검색 가능하게 하는 시나리오를 다루었습니다.

- Salesforce 데이터 스토어 플러그인에 의한 CRM 데이터 연동
- 데이터베이스 데이터 스토어 플러그인에 의한 사내 DB 연동
- CSV 데이터 스토어에 의한 리스트 데이터 연동
- 필드 매핑과 SQL 쿼리 설계
- 횡단 검색에서의 라벨 활용

데이터 사일로를 해소하고 모든 정보 소스를 횡단 검색할 수 있는 환경이 실현됩니다.
실전 솔루션 편은 여기까지입니다. 다음 회부터는 아키텍처 및 스케일링 편으로서 멀티 테넌트 설계를 다룹니다.

참고 자료
=========

- `Fess 데이터 스토어 설정 <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess 플러그인 관리 <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
