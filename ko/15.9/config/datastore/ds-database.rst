==================================================
데이터베이스 커넥터(데이터베이스 검색)
==================================================

개요
====

데이터베이스 커넥터는 JDBC 호환 관계형 데이터베이스(MySQL・PostgreSQL・Oracle・SQL Server 등)의 레코드를 |Fess| 의 인덱스에 등록하여 데이터베이스 검색(데이터베이스의 전문 검색)을 구현하는 기능입니다. SELECT 문으로 가져온 각 열을 검색 필드에 매핑하여 등록합니다.

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

방법1: 관리 화면에서 설치

1. "시스템" → "플러그인"을 엽니다
2. JAR 파일을 업로드
3. |Fess| 를 재시작

방법2: JAR 파일을 직접 배치

::

    # CodeLibs 리포지토리에서 다운로드
    wget https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # 배치（관리 화면에서 설치되는 디렉터리와 동일）
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # 또는
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

JDBC 드라이버 설치
------------------

JDBC 드라이버는 플러그인에 포함되어 있지 않습니다. 연결 대상 데이터베이스에 맞는 드라이버를 별도로 입수하여 배치하십시오.

데이터스토어 크롤링은 크롤러 프로세스에서 실행되므로, 드라이버는 **크롤러 프로세스의 클래스패스** 에 배치해야 합니다. 다음 디렉터리 중 하나가 해당됩니다:

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

::

    # 예: MySQL 드라이버
    cp mysql-connector-j-9.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # 또는
    cp mysql-connector-j-9.x.x.jar /usr/share/fess/app/WEB-INF/lib/

JDBC 드라이버를 배치한 후 |Fess| 를 재시작하여 로드합니다.

.. note::
   드라이버를 찾을 수 없는 경우, 크롤링은
   ``The JDBC driver ... is not on the crawler classpath.`` 메시지와 함께 실패합니다.

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
     - JDBC 페치 크기. ``MIN_VALUE`` 는 MySQL에서 결과 세트를 한 행씩 읽게 하기 위한 지정이며, 다른 드라이버는 음수 값을 받아들이지 않습니다（경고를 출력하고 드라이버 기본값으로 계속합니다）. 음수 값이나 숫자가 아닌 값은 경고를 출력하고 무시됩니다
   * - ``query_timeout``
     - 아니요
     - 쿼리 타임아웃（초）. ``0`` 은 무제한（JDBC 기본값）. 미지정 시 타임아웃을 설정하지 않습니다
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
   * - ``last_crawl_time``
     - 아니요
     - 차분 크롤링의 기준 시각. 크롤링 완료 시 자동으로 다시 기록됩니다（「차분 크롤링」 참조）
   * - ``last_crawl_time_format``
     - 아니요
     - ``last_crawl_time`` 의 형식. 기본값: ``yyyy-MM-dd HH:mm:ss``

.. note::
   쿼리가 멈춘 경우, 작업을 중지해도 크롤러 스레드는 해제되지 않습니다.
   중지 요청은 행과 행 사이에서만 확인되므로, 드라이버 내부에서 블록된 호출에는
   효과가 없습니다. 장시간 실행될 가능성이 있는 쿼리에는 ``query_timeout`` 을
   설정하십시오.

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
- ``crawlingConfig`` - 데이터스토어 설정
- ``crawlingContext`` - 크롤링 중의 컨텍스트. ``crawlingContext.doc`` 로 생성 중인 문서를 참조할 수 있습니다

.. note::
   열 이름은 ``SELECT`` 절의 컬럼 라벨（별칭）과 일치시켜야 합니다.
   집계 함수나 식을 사용하는 경우 ``AS`` 로 명시적으로 별칭을 붙여 주세요
   （예: ``COUNT(*) AS total``）.

.. note::
   컬럼 라벨의 대소문자는 데이터베이스마다 다릅니다. PostgreSQL은 따옴표로 감싸지 않은
   식별자를 소문자로, H2는 대문자로 변환하며, MySQL은 선언한 그대로 반환합니다.
   스크립트에서 참조한 이름을 해석할 수 없는 경우, 해당 필드는 오류 없이 설정되지 않은
   상태로 남습니다. 이식성이 중요한 경우에는 ``AS`` 로 명시적으로 별칭을 붙여 주세요.

.. warning::
   스크립트에서는 SQL 결과 열뿐만 아니라 **데이터스토어 파라미터 전체** 를 같은 이름의
   변수로 참조할 수 있습니다. ``driver`` ・ ``url`` ・ ``username`` ・ ``password`` ・
   ``sql`` 등도 변수로 보이기 때문에, 같은 이름의 열이 의도치 않게 가려지거나, 반대로
   열이 없을 때 파라미터 값이 들어갈 수 있습니다. 같은 이름의 열이 있는 경우에는 열의
   값이 우선합니다.

BLOB·바이너리 데이터 취득
==========================

바이너리 열（BLOB・ ``BYTEA`` ・바이트 배열・바이너리 스트림）은 콘텐츠 추출 처리
（파일 크롤링과 동일한 추출기）에 적용되어 텍스트로 취득됩니다.

한편 CLOB・NCLOB・문자 스트림은 **추출기를 거치지 않고** 문자열로 그대로 읽힙니다.
MIME 타입 지정（후술）은 이들에는 적용되지 않습니다.

배열형 열은 요소를 공백으로 연결한 문자열이 됩니다. NULL 값은 빈 문자열이 됩니다.

.. note::
   같은 BLOB 열이라도 JDBC 드라이버에 따라 ``java.sql.Blob`` 을 반환하는 것과 바이트
   배열을 반환하는 것이 있습니다（MySQL과 PostgreSQL은 바이트 배열）. 어느 쪽이든
   동일하게 추출됩니다.

.. note::
   CLOB・NCLOB은 크기 제한 없이 메모리에 읽어 들입니다. 매우 큰 텍스트 열을 다루는
   경우에는 SQL 측에서 ``SUBSTRING`` 등을 사용하여 잘라내는 것을 검토하십시오.
   추출기를 거치는 경로에는 크롤러의 최대 크기 설정이 적용됩니다.

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

``sql`` 에 ``${last_crawl_time}`` 이라고 쓰면 이전 크롤링을 시작한 시각으로 치환됩니다:

::

    sql=SELECT id, title, content, url, updated_at FROM articles WHERE updated_at > '${last_crawl_time}'

첫 회에는 ``1970-01-01 00:00:00`` 으로 치환되므로 전체가 대상이 됩니다.
결과 세트를 끝까지 다 읽으면, 이번 크롤링의 시작 시각이 ``last_crawl_time`` 으로
데이터스토어 설정에 다시 기록되어 다음 크롤링에서 사용됩니다.

시각의 형식은 ``last_crawl_time_format`` 으로 변경할 수 있습니다（기본값
``yyyy-MM-dd HH:mm:ss``）. 데이터베이스가 타임스탬프 리터럴로 받아들이는 형식을
지정하십시오.

기준 시각은 크롤링의 **시작 시각** 입니다. 크롤링 중에 업데이트된 행은 다음 크롤링에서
가져오게 됩니다. 또한 크롤링이 도중에 중지된 경우에는 다시 기록하지 않습니다.

.. warning::
   차분 크롤링에서는 삭제된 행을 감지할 수 없습니다.

   차분 크롤링을 활성화하면, |Fess| 가 「이전 크롤링에 포함되지 않은 문서」를 인덱스에서
   삭제하는 처리（ ``delete_old_docs`` ）도 자동으로 비활성화됩니다. 이를 비활성화하지
   않으면 변경되지 않은 문서가 매번 모두 삭제되기 때문입니다.

   그 결과, 데이터베이스에서 삭제된 행에 해당하는 문서는 유효 기간이 만료될 때까지
   인덱스에 남습니다. 정기적으로 전체 크롤링（ ``${last_crawl_time}`` 을 포함하지 않는
   설정）을 실행하십시오.

   ``delete_old_docs`` 를 데이터스토어 설정에 명시한 경우에는 그쪽이 우선합니다.

ID에 의한 범위 지정 등, 기존과 같이 ``sql`` 에 조건을 직접 쓰는 방법도 계속 사용할 수 있습니다:

::

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

.. warning::
   ``url=url`` 은 ``SELECT`` 결과에 ``url`` 이라는 라벨의 열이 있는 경우에만 의도대로
   동작합니다. 해당하는 열이 없으면 같은 이름의 데이터스토어 파라미터, 즉
   **JDBC 연결 URL** 이 문서의 URL로 설정됩니다. 열 이름이 다른 경우에는
   ``SELECT page_url AS url`` 과 같이 별칭을 붙이거나, ``url=page_url`` 과 같이
   스크립트 측에서 열 이름을 지정하십시오.

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

1. 자동 암호화 이용

   ``app.encrypt.property.pattern`` （기본값 ``.*password|.*key|.*token|.*secret`` ）에
   일치하는 파라미터 이름의 값은 관리 화면에서 저장하면 자동으로 암호화되어
   ``{cipher}`` 접두사가 붙은 상태로 저장됩니다. ``password`` 는 이 패턴에 일치하므로,
   관리 화면에서 설정했다면 평문으로 저장되지 않습니다.

2. 환경 변수 사용

   ``FESS_ENV_`` 로 시작하는 환경 변수는 데이터스토어 파라미터 안에서
   ``${환경 변수명}`` 으로 전개됩니다:

   ::

       password=${FESS_ENV_DB_PASSWORD}

   전개 대상이 되는 환경 변수 이름의 패턴은 ``crawler.data.env.param.key.pattern``
   （기본값 ``^FESS_ENV_.*`` ）으로 설정합니다.

3. 읽기 전용 사용자 사용

.. note::
   ``org.codelibs.fess.ds`` 의 로그 레벨을 DEBUG로 설정해도, 비밀번호 등
   ``app.encrypt.property.pattern`` 에 일치하는 파라미터의 값과 JDBC 연결 URL에
   포함된 인증 정보는 마스킹되어 출력됩니다.

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

크롤링이 실패했을 때는 먼저 로그의 메시지로 원인을 구분합니다.

JDBC 드라이버를 찾을 수 없음
-----------------------------

**증상**: ``The JDBC driver ... is not on the crawler classpath.``

**해결 방법**:

1. JDBC 드라이버가 ``app/WEB-INF/lib/`` 또는 ``app/WEB-INF/env/crawler/lib/`` 에 배치되어 있는지 확인
2. ``driver`` 에 지정한 클래스명이 올바른지 확인
3. |Fess| 재시작

연결 오류
---------

**증상**: ``Failed to connect to <URL>.``

**확인 사항**:

1. 데이터베이스가 시작되어 있는지
2. 호스트명, 포트 번호가 올바른지
3. 사용자명, 비밀번호가 올바른지
4. 방화벽 설정

쿼리 오류
---------

**증상**: ``Failed to execute the query.``

**확인 사항**:

1. SQL 쿼리를 직접 데이터베이스에서 실행하여 테스트
2. 열 이름이 올바른지 확인
3. 테이블 이름이 올바른지 확인

설정 누락
---------

**증상**: ``The driver parameter is required.`` ・ ``The url parameter is required.`` ・ ``The sql parameter is required.``

필수 파라미터가 설정되어 있지 않습니다. 파라미터 란을 확인하십시오.

일부 행만 실패함
----------------

행 단위의 실패는 크롤링을 중단시키지 않으며, "시스템" → "장애 URL"에 기록됩니다.
스크립트가 URL을 생성했다면 그 URL로, 생성 전에 실패한 경우에는
``datastore://<데이터스토어 설정 ID>/<행 번호>`` 로 기록됩니다.

검색 결과에 나오지 않음
-----------------------

1. 스크립트에서 ``url`` ・ ``title`` ・ ``content`` 가 설정되어 있는지 확인
2. 컬럼 라벨의 대소문자가 스크립트와 일치하는지 확인（「스크립트 설정」 참조）
3. 크롤링 작업의 로그에서 문서 수를 확인

참고 정보
=========

- :doc:`ds-overview` - 데이터스토어 커넥터 개요
- :doc:`ds-csv` - CSV 커넥터
- :doc:`ds-json` - JSON 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터스토어 설정 가이드
- :doc:`../crawler-basic` - 크롤러 기본 설정
- :doc:`../search-basic` - 검색 기능
