==================================
데이터베이스 커넥터
==================================

개요
====

데이터베이스 커넥터는 JDBC 호환 관계형 데이터베이스에서 데이터를 가져와
|Fess| 의 인덱스에 등록하는 기능을 제공합니다.

이 기능에는 ``fess-ds-db`` 플러그인이 필요합니다.

지원 데이터베이스
=================

JDBC 호환 모든 데이터베이스를 지원합니다. 주요 예:

- MySQL / MariaDB
- PostgreSQL
- Oracle Database
- Microsoft SQL Server
- SQLite
- H2 Database

전제 조건
=========

1. ``fess-ds-db`` 플러그인 설치가 필요합니다
2. 연결 대상 데이터베이스에 맞는 JDBC 드라이버가 필요합니다
3. 데이터베이스에 대한 읽기 액세스 권한이 필요합니다
4. 대량의 데이터를 가져올 경우, 적절한 쿼리 설계가 중요합니다

플러그인 설치
-------------

방법1: JAR 파일을 직접 배치

::

    # Maven Central에서 다운로드
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # 배치
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 또는
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

방법2: 관리 화면에서 설치

1. "시스템" → "플러그인"을 엽니다
2. JAR 파일을 업로드
3. |Fess| 를 재시작

JDBC 드라이버 설치
------------------

연결 대상 데이터베이스에 맞는 JDBC 드라이버를 |Fess| 의 클래스패스（ ``app/WEB-INF/lib/`` 디렉터리）에 배치합니다:

::

    # 예: MySQL 드라이버
    cp mysql-connector-j-8.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # 또는
    cp mysql-connector-j-8.x.x.jar /usr/share/fess/app/WEB-INF/lib/

JDBC 드라이버를 배치한 후 |Fess| 를 재시작하여 로드합니다.

설정 방법
=========

관리 화면에서 "크롤러" → "데이터스토어" → "신규 작성"으로 설정합니다.

기본 설정
---------

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
-------------

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
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 파라미터
     - 필수
     - 설명
   * - ``driver``
     - 예
     - JDBC 드라이버의 클래스명（미지정 시 ``DataStoreException`` 발생）
   * - ``url``
     - 예
     - JDBC 연결 URL（연결에 필수）
   * - ``sql``
     - 예
     - 데이터 취득용 SQL 쿼리（미지정 시 ``DataStoreException`` 발생）
   * - ``username``
     - 아니요
     - 데이터베이스 사용자명
   * - ``password``
     - 아니요
     - 데이터베이스 비밀번호
   * - ``fetch_size``
     - 아니요
     - JDBC 페치 크기. MySQL의 스트리밍 결과 세트에는 ``MIN_VALUE`` 를 지정
   * - ``default_mimetype``
     - 아니요
     - BLOB·바이너리 열의 콘텐츠 추출 시 사용할 기본 MIME 타입
   * - ``column_label.mimetype``
     - 아니요
     - BLOB·바이너리 열 추출에 사용할 MIME 타입을 저장한 열 이름을 지정（예: ``column_label.mimetype=content_type``）
   * - ``column_label.filename``
     - 아니요
     - BLOB·바이너리 열 추출에 사용할 파일명을 저장한 열 이름을 지정（확장자에서 MIME 타입을 추정）
   * - ``info.*``
     - 아니요
     - 추가 JDBC 연결 프로퍼티（예: ``info.ssl=true``）. ``info.`` 를 제외한 키가 JDBC 드라이버에 전달됩니다
   * - ``readInterval``
     - 아니요
     - 각 행 처리 사이의 지연 시간（밀리초）. 기본값: 0
   * - ``script_type``
     - 아니요
     - 스크립트 엔진의 종류. 기본값: groovy

스크립트 설정
-------------

SQL 열 이름을 인덱스 필드에 매핑합니다:

::

    url="https://example.com/articles/" + id
    title=title
    content=content
    lastModified=updated_at

사용 가능한 필드:

- ``<column_name>`` - SQL 쿼리 결과의 열（컬럼 라벨명으로 직접 접근합니다. ``data.`` 와 같은 접두사는 붙지 않습니다）

.. note::
   열 이름은 ``SELECT`` 절의 컬럼 라벨（별칭）과 일치시켜야 합니다.
   집계 함수나 식을 사용하는 경우 ``AS`` 로 명시적으로 별칭을 붙여 주세요
   （예: ``COUNT(*) AS total``）.

BLOB·바이너리 데이터 취득
==========================

BLOB, CLOB, NCLOB, 바이트 배열, 바이너리 스트림 등의 열은 자동으로
콘텐츠 추출 처리（파일 크롤링과 동일한 추출기）에 적용되어 텍스트로
취득됩니다. 배열형 열은 공백으로 구분된 문자열로 변환됩니다. NULL 값은
빈 문자열이 됩니다.

BLOB나 바이너리 스트림에서 올바르게 텍스트를 추출하려면 데이터의 종류（MIME 타입）를
판별해야 합니다. 판별에는 다음 우선순위가 사용됩니다:

1. ``column_label.mimetype=<열 이름>`` - 지정한 열의 값을 MIME 타입으로 사용
2. ``column_label.filename=<열 이름>`` - 지정한 열의 값을 파일명으로 취급하여 확장자에서 MIME 타입을 추정
3. ``default_mimetype`` - 위에서 판별할 수 없는 경우에 사용할 기본 MIME 타입

예（ ``file_data`` 열의 BLOB를 ``content_type`` 열의 MIME 타입을 사용하여 추출）:

::

    sql=SELECT id, title, file_data, content_type FROM documents
    column_label.mimetype=content_type

SQL 쿼리 설계
=============

효율적인 쿼리
-------------

대량의 데이터를 다룰 경우, 쿼리 성능이 중요합니다.
SQL은 그대로 데이터베이스에 전송됩니다（파라미터 바인딩은 수행되지 않습니다）:

::

    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= '2024-01-01 00:00:00'
    ORDER BY id

차분 크롤링
-----------

업데이트된 레코드만 가져오는 방법:

::

    # 업데이트 날짜로 필터링
    sql=SELECT * FROM articles WHERE updated_at >= '2024-01-01 00:00:00'

    # ID로 범위 지정
    sql=SELECT * FROM articles WHERE id > 10000

URL 생성
--------

문서의 URL은 스크립트로 생성합니다:

::

    # 고정 패턴
    url="https://example.com/article/" + id

    # 여러 필드 조합
    url="https://example.com/" + category + "/" + slug

    # 데이터베이스에 저장된 URL 사용
    url=url

다국어 문자 지원
================

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

보안
====

데이터베이스 인증 정보 보호
---------------------------

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
=======

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

    url="https://shop.example.com/product/" + id
    title=name
    content=description + " 카테고리: " + category + " 가격: " + price + "원"
    lastModified=updated_at

지식 베이스 문서
----------------

파라미터:

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/knowledge
    username=fess_user
    password=password
    sql=SELECT id, title, body, tags, author, created_at, updated_at FROM articles WHERE published = true ORDER BY id

스크립트:

::

    url="https://kb.example.com/article/" + id
    title=title
    content=body
    digest=tags
    author=author
    created=created_at
    lastModified=updated_at

문제 해결
=========

JDBC 드라이버를 찾을 수 없음
-----------------------------

**증상**: ``ClassNotFoundException`` 또는 ``No suitable driver``

**해결 방법**:

1. JDBC 드라이버가 ``lib/`` 에 배치되어 있는지 확인
2. 드라이버의 클래스명이 올바른지 확인
3. |Fess| 재시작

연결 오류
---------

**증상**: ``Connection refused`` 또는 인증 오류

**확인 사항**:

1. 데이터베이스가 시작되어 있는지
2. 호스트명, 포트 번호가 올바른지
3. 사용자명, 비밀번호가 올바른지
4. 방화벽 설정

쿼리 오류
---------

**증상**: ``SQLException`` 또는 SQL 구문 오류

**확인 사항**:

1. SQL 쿼리를 직접 데이터베이스에서 실행하여 테스트
2. 열 이름이 올바른지 확인
3. 테이블 이름이 올바른지 확인

참고 정보
=========

- :doc:`ds-overview` - 데이터스토어 커넥터 개요
- :doc:`ds-csv` - CSV 커넥터
- :doc:`ds-json` - JSON 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터스토어 설정 가이드
