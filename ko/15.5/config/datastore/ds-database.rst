==================================
데이터베이스 커넥터
==================================

개요
====

데이터베이스 커넥터는 JDBC 호환 관계형 데이터베이스에서 데이터를 가져와
|Fess| 의 인덱스에 등록하는 기능을 제공합니다.

이 기능은 |Fess| 에 내장되어 있으며, 추가 플러그인이 필요하지 않습니다.

지원 데이터베이스
================

JDBC 호환 모든 데이터베이스를 지원합니다. 주요 예:

- MySQL / MariaDB
- PostgreSQL
- Oracle Database
- Microsoft SQL Server
- SQLite
- H2 Database

전제 조건
========

1. JDBC 드라이버가 필요합니다
2. 데이터베이스에 대한 읽기 액세스 권한이 필요합니다
3. 대량의 데이터를 가져올 경우, 적절한 쿼리 설계가 중요합니다

JDBC 드라이버 설치
----------------------------

JDBC 드라이버를 ``lib/`` 디렉토리에 배치합니다:

::

    # 예: MySQL 드라이버
    cp mysql-connector-java-8.0.33.jar /path/to/fess/lib/

|Fess| 를 재시작하여 드라이버를 로드합니다.

설정 방법
========

관리 화면에서 "크롤러" → "데이터스토어" → "신규 작성"으로 설정합니다.

기본 설정
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 항목
     - 설정 예
   * - 이름
     - Products Database
   * - 핸들러 이름
     - DatabaseDataStore
   * - 사용
     - 켜기

파라미터 설정
----------------

MySQL/MariaDB 예:

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=UTC
    username=fess_user
    password=your_password
    sql=SELECT id, title, content, url, updated_at FROM articles WHERE deleted = 0

PostgreSQL 예:

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/mydb
    username=fess_user
    password=your_password
    sql=SELECT id, title, content, url, updated_at FROM articles WHERE deleted = false

파라미터 목록
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``driver``
     - 예
     - JDBC 드라이버의 클래스명
   * - ``url``
     - 예
     - JDBC 연결 URL
   * - ``username``
     - 예
     - 데이터베이스 사용자명
   * - ``password``
     - 예
     - 데이터베이스 비밀번호
   * - ``sql``
     - 예
     - 데이터 취득용 SQL 쿼리
   * - ``fetch.size``
     - 아니요
     - 페치 크기 (기본값: 100)

스크립트 설정
--------------

SQL 열 이름을 인덱스 필드에 매핑합니다:

::

    url="https://example.com/articles/" + data.id
    title=data.title
    content=data.content
    lastModified=data.updated_at

사용 가능한 필드:

- ``data.<column_name>`` - SQL 쿼리 결과 열

SQL 쿼리 설계
===============

효율적인 쿼리
--------------

대량의 데이터를 다룰 경우, 쿼리 성능이 중요합니다:

::

    # 인덱스를 사용한 효율적인 쿼리
    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= :last_crawl_date
    ORDER BY id

차분 크롤링
------------

업데이트된 레코드만 가져오는 방법:

::

    # 업데이트 날짜로 필터링
    sql=SELECT * FROM articles WHERE updated_at >= '2024-01-01 00:00:00'

    # ID로 범위 지정
    sql=SELECT * FROM articles WHERE id > 10000

URL 생성
---------

문서의 URL은 스크립트로 생성합니다:

::

    # 고정 패턴
    url="https://example.com/article/" + data.id

    # 여러 필드 조합
    url="https://example.com/" + data.category + "/" + data.slug

    # 데이터베이스에 저장된 URL 사용
    url=data.url

다국어 문자 지원
====================

한국어 등 다국어 문자를 포함한 데이터를 다룰 경우:

MySQL
-----

::

    url=jdbc:mysql://localhost:3306/mydb?useUnicode=true&characterEncoding=UTF-8

PostgreSQL
----------

PostgreSQL은 보통 UTF-8이 기본입니다. 필요한 경우:

::

    url=jdbc:postgresql://localhost:5432/mydb?charSet=UTF-8

커넥션 풀링
==============

대량의 데이터를 처리할 경우, 커넥션 풀링을 고려하세요:

::

    # HikariCP 사용 시 설정
    datasource.class=com.zaxxer.hikari.HikariDataSource
    pool.size=5

보안
============

데이터베이스 인증 정보 보호
--------------------------

.. warning::
   비밀번호를 설정 파일에 직접 기술하는 것은 보안 위험이 있습니다.

권장 방법:

1. 환경 변수 사용
2. |Fess| 의 암호화 기능 사용
3. 읽기 전용 사용자 사용

최소 권한 원칙
--------------

데이터베이스 사용자에게는 필요 최소한의 권한만 부여합니다:

::

    -- MySQL 예
    CREATE USER 'fess_user'@'localhost' IDENTIFIED BY 'password';
    GRANT SELECT ON mydb.articles TO 'fess_user'@'localhost';

사용 예
======

제품 카탈로그 검색
------------------

파라미터:

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/shop
    username=fess_user
    password=password
    sql=SELECT p.id, p.name, p.description, p.price, c.name as category, p.updated_at FROM products p JOIN categories c ON p.category_id = c.id WHERE p.active = 1

스크립트:

::

    url="https://shop.example.com/product/" + data.id
    title=data.name
    content=data.description + " 카테고리: " + data.category + " 가격: " + data.price + "원"
    lastModified=data.updated_at

지식 베이스 문서
------------------

파라미터:

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/knowledge
    username=fess_user
    password=password
    sql=SELECT id, title, body, tags, author, created_at, updated_at FROM articles WHERE published = true ORDER BY id

스크립트:

::

    url="https://kb.example.com/article/" + data.id
    title=data.title
    content=data.body
    digest=data.tags
    author=data.author
    created=data.created_at
    lastModified=data.updated_at

문제 해결
======================

JDBC 드라이버를 찾을 수 없음
----------------------------

**증상**: ``ClassNotFoundException`` 또는 ``No suitable driver``

**해결 방법**:

1. JDBC 드라이버가 ``lib/`` 에 배치되어 있는지 확인
2. 드라이버의 클래스명이 올바른지 확인
3. |Fess| 재시작

연결 오류
----------

**증상**: ``Connection refused`` 또는 인증 오류

**확인 사항**:

1. 데이터베이스가 시작되어 있는지
2. 호스트명, 포트 번호가 올바른지
3. 사용자명, 비밀번호가 올바른지
4. 방화벽 설정

쿼리 오류
------------

**증상**: ``SQLException`` 또는 SQL 구문 오류

**확인 사항**:

1. SQL 쿼리를 직접 데이터베이스에서 실행하여 테스트
2. 열 이름이 올바른지 확인
3. 테이블 이름이 올바른지 확인

참고 정보
========

- :doc:`ds-overview` - 데이터스토어 커넥터 개요
- :doc:`ds-csv` - CSV 커넥터
- :doc:`ds-json` - JSON 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터스토어 설정 가이드
