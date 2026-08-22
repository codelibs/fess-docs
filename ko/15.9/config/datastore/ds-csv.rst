==================================
CSV 커넥터
==================================

개요
====

CSV 커넥터는 CSV 파일에서 데이터를 가져와
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-csv`` 플러그인이 필요합니다.

전제 조건
=========

1. 플러그인 설치가 필요합니다
2. CSV 파일에 대한 액세스 권한이 필요합니다
3. CSV 파일의 문자 인코딩을 파악하고 있어야 합니다

플러그인 설치
-------------

방법 1: JAR 파일 직접 배치

::

    # Maven Central에서 다운로드
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-csv/X.X.X/fess-ds-csv-X.X.X.jar

    # 배치
    cp fess-ds-csv-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 또는
    cp fess-ds-csv-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

방법 2: 관리 화면에서 설치

1. "시스템" → "플러그인" 열기
2. JAR 파일 업로드
3. |Fess| 재시작

설정 방법
=========

관리 화면에서 "크롤러" → "데이터 스토어" → "새로 만들기"에서 설정합니다.

기본 설정
---------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 항목
     - 설정 예
   * - 이름
     - Products CSV
   * - 핸들러 이름
     - CsvDataStore
   * - 활성화
     - 켬

파라미터 설정
-------------

로컬 파일:

::

    files=/path/to/data.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="
    quote_disabled=false

복수 파일:

::

    files=/path/to/data1.csv,/path/to/data2.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="
    quote_disabled=false

.. note::

   인용 부호(쿼트) 처리와 이스케이프 처리는 기본적으로 **비활성화** 되어 있습니다.
   인용 부호로 감싼 필드 내에 구분 문자나 줄바꿈을 포함하는 CSV(RFC 4180 준수)를 처리하는 경우,
   ``quote_disabled=false`` 를 명시적으로 지정하여 인용 부호 처리를 활성화하십시오.
   자세한 내용은 아래의 "인용 부호·이스케이프 처리 활성화"를 참고하십시오.

파라미터 목록
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``files``
     - 아니오
     - CSV 파일 경로(로컬 경로, 복수 지정 가능: 쉼표 구분). ``files`` 또는 ``directories`` 중 하나를 반드시 지정해야 합니다. 양쪽 모두 지정한 경우 ``files`` 가 우선됩니다. 지정하는 파일은 확장자가 ``.csv`` 또는 ``.tsv`` 이어야 하며, 그 외 확장자의 파일은 건너뜁니다.
   * - ``directories``
     - 아니오
     - CSV 파일이 포함된 디렉터리 경로(복수 지정 가능: 쉼표 구분). 디렉터리 내의 ``.csv`` 및 ``.tsv`` 파일만 대상이 됩니다. ``files`` 가 지정되지 않은 경우에 사용됩니다.
   * - ``file_encoding``
     - 아니오
     - 문자 인코딩(기본값: UTF-8)
   * - ``has_header_line``
     - 아니오
     - 헤더 행 유무(기본값: false)
   * - ``separator_character``
     - 아니오
     - 구분 문자(기본값: 쉼표 ``,``). ``\t`` 와 같은 이스케이프 시퀀스를 지정할 수 있습니다(탭 구분).
   * - ``quote_character``
     - 아니오
     - 인용 부호(기본값: 큰따옴표 ``"``). 단, 인용 부호 처리는 기본적으로 비활성화되어 있습니다( ``quote_disabled`` 참고).
   * - ``escape_character``
     - 아니오
     - 이스케이프 문자(기본값: 백슬래시 ``\``). 단, 이스케이프 처리는 기본적으로 비활성화되어 있습니다( ``escape_disabled`` 참고).

.. note::

   ``files`` 와 ``directories`` 모두 비어 있는 경우 오류( ``DataStoreException`` )가 발생합니다.
   반드시 어느 하나를 지정하십시오.

고급 파라미터
~~~~~~~~~~~~~

아래 파라미터는 CSV 파싱 동작을 세밀하게 제어합니다:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 파라미터
     - 설명
   * - ``quote_disabled``
     - 인용 부호(쿼트) 처리를 비활성화할지 여부(기본값: true). RFC 4180 준수의 인용 부호 포함 필드를 처리하는 경우 ``false`` 를 지정합니다.
   * - ``escape_disabled``
     - 이스케이프 처리를 비활성화할지 여부(기본값: true). ``escape_character`` 에 의한 이스케이프를 활성화하는 경우 ``false`` 를 지정합니다.
   * - ``skip_lines``
     - 건너뛸 선두 행 수(기본값: 0)
   * - ``ignore_line_patterns``
     - 무시할 행의 정규식 패턴(예: ``^#.*`` 으로 주석 행 무시)
   * - ``ignore_empty_lines``
     - 빈 행을 무시할지 여부(기본값: false)
   * - ``ignore_trailing_whitespaces``
     - 후행 공백을 무시할지 여부(기본값: false)
   * - ``ignore_leading_whitespaces``
     - 선행 공백을 무시할지 여부(기본값: false)
   * - ``null_string``
     - null 값으로 처리할 문자열
   * - ``break_string``
     - 필드 값 내의 줄바꿈을 대체할 문자열
   * - ``readInterval``
     - 레코드 1건을 처리할 때마다의 대기 시간(밀리초)(기본값: 0)

스크립트 설정
-------------

각 필드의 값은 CSV 각 열의 값을 참조하여 구성합니다. CSV의 열은 스크립트 내에서
**접두사 없는 변수** 로 직접 참조할 수 있습니다( ``data.`` 와 같은 접두사는 붙지 않습니다).

헤더가 있는 경우(열 이름으로 참조):

::

    url="https://example.com/product/" + product_id
    title=product_name
    content=description
    digest=category
    price=price

헤더가 없는 경우(열 인덱스로 참조):

::

    url="https://example.com/product/" + cell1
    title=cell2
    content=cell3
    price=cell4

사용 가능한 필드
~~~~~~~~~~~~~~~~

- ``<열명>`` - 헤더 행의 열 이름으로 직접 참조합니다( ``has_header_line=true`` 인 경우에만 유효. 열 이름이 공백이 아닌 경우에 사용 가능)
- ``cell<N>`` - 열 인덱스로 참조합니다( ``cell1``, ``cell2`` ...와 같이 1부터 시작. 헤더 유무에 관계없이 사용 가능)
- ``csvfile`` - 처리 중인 CSV 파일의 전체 경로
- ``csvfilename`` - 처리 중인 CSV 파일 이름

.. note::

   열 이름에 공백이나 하이픈 등 Groovy 식별자로 유효하지 않은 문자가 포함된 경우,
   열 이름으로 참조할 수 없습니다. 그 경우에는 ``cell<N>`` 을 사용하십시오.

CSV 형식 상세
=============

표준 CSV(RFC 4180 준수)
-----------------------

::

    product_id,product_name,description,price,category
    1,Laptop,High-performance laptop,150000,Electronics
    2,Mouse,Wireless mouse,3000,Electronics
    3,"Book, Programming","Learn to code",2800,Books

.. note::

   위의 ``"Book, Programming"`` 과 같이 인용 부호로 감싸 필드 내에 구분 문자를
   포함하려면 ``quote_disabled=false`` 를 지정하여 인용 부호 처리를 활성화해야 합니다.
   인용 부호 처리가 비활성화(기본값)된 경우, 인용 부호는 일반 문자로 취급되며
   필드는 구분 문자로 분할됩니다.

인용 부호·이스케이프 처리 활성화
---------------------------------

인용 부호 처리와 이스케이프 처리는 기본적으로 비활성화되어 있습니다. 아래와 같이 명시적으로 활성화합니다.

인용 부호 처리를 활성화:

::

    # 파라미터
    quote_disabled=false
    quote_character="

이스케이프 처리를 활성화:

::

    # 파라미터
    escape_disabled=false
    escape_character=\

구분자 변경
-----------

탭 구분(TSV):

::

    # 파라미터
    separator_character=\t

세미콜론 구분:

::

    # 파라미터
    separator_character=;

커스텀 인용 부호
----------------

작은따옴표(인용 부호 처리 활성화 필요):

::

    # 파라미터
    quote_disabled=false
    quote_character='

인코딩
------

한국어 파일(EUC-KR):

::

    file_encoding=EUC-KR

한국어 파일(CP949):

::

    file_encoding=CP949

사용 예
=======

제품 카탈로그 CSV
-----------------

CSV 파일(products.csv):

::

    product_id,name,description,price,category,in_stock
    1001,노트북,고성능 노트북,120000,컴퓨터,true
    1002,마우스,무선 마우스,2500,주변기기,true
    1003,키보드,기계식 키보드,8500,주변기기,false

파라미터:

::

    files=/var/data/products.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

스크립트:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description + " 카테고리: " + category + " 가격: " + price + "원"
    digest=category
    price=price

재고 정보 필터링:

::

    url=in_stock == "true" ? "https://shop.example.com/product/" + product_id : null
    title=in_stock == "true" ? name : null
    content=in_stock == "true" ? description : null
    price=in_stock == "true" ? price : null

직원 명부 CSV
-------------

CSV 파일(employees.csv):

::

    emp_id,name,department,email,phone,position
    E001,홍길동,영업부,hong@example.com,02-1234-5678,부장
    E002,김철수,개발부,kim@example.com,02-2345-6789,매니저
    E003,이영희,총무부,lee@example.com,02-3456-7890,담당자

파라미터:

::

    files=/var/data/employees.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

스크립트:

::

    url="https://intranet.example.com/employee/" + emp_id
    title=name + " (" + department + ")"
    content="부서: " + department + "\n직책: " + position + "\n이메일: " + email + "\n전화: " + phone
    digest=department

헤더 없는 CSV
-------------

CSV 파일(data.csv):

::

    1,상품A,상품A에 대한 설명입니다,1000
    2,상품B,상품B에 대한 설명입니다,2000
    3,상품C,상품C에 대한 설명입니다,3000

파라미터:

::

    files=/var/data/data.csv
    file_encoding=UTF-8
    has_header_line=false
    separator_character=,

스크립트:

::

    url="https://example.com/item/" + cell1
    title=cell2
    content=cell3
    price=cell4

복수 CSV 파일 통합
------------------

파라미터:

::

    files=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

스크립트:

::

    url="https://example.com/report/" + id
    title=title
    content=content
    timestamp=date

탭 구분(TSV) 파일
-----------------

TSV 파일(data.tsv):

::

    id	title	content	category
    1	기사1	기사1의 내용입니다	뉴스
    2	기사2	기사2의 내용입니다	블로그

파라미터:

::

    files=/var/data/data.tsv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=\t

스크립트:

::

    url="https://example.com/article/" + id
    title=title
    content=content
    digest=category

문제 해결
=========

파일을 찾을 수 없음
-------------------

**증상**: 크롤링이 실행되지만 파일이 처리되지 않음, 로그에 ``is not found`` 가 출력됨

**확인 사항**:

1. 파일 경로가 올바른지 확인(절대 경로 권장)
2. 파일이 존재하는지 확인
3. 파일 확장자가 ``.csv`` 또는 ``.tsv`` 인지 확인(그 외 확장자는 건너뜁니다)
4. 파일의 읽기 권한이 있는지 확인
5. |Fess| 실행 사용자가 액세스 가능한지 확인

문자 깨짐 발생
--------------

**증상**: 한글이 올바르게 표시되지 않음

**해결 방법**:

올바른 문자 인코딩 지정:

::

    # UTF-8
    file_encoding=UTF-8

    # EUC-KR
    file_encoding=EUC-KR

    # Windows 표준(CP949)
    file_encoding=CP949

파일 인코딩 확인:

::

    file -i data.csv
    # 또는
    nkf -g data.csv

열이 올바르게 인식되지 않음
----------------------------

**증상**: 열 구분이 올바르게 인식되지 않거나, 인용 부호로 감싼 필드가 분할됨

**확인 사항**:

1. 구분 문자가 올바른지 확인:

   ::

       # 쉼표
       separator_character=,

       # 탭
       separator_character=\t

       # 세미콜론
       separator_character=;

2. 인용 부호 포함 필드(필드 내에 구분 문자를 포함하는 경우)를 처리하는 경우 인용 부호 처리를 활성화:

   ::

       quote_disabled=false

3. CSV 파일 형식 확인(RFC 4180 준수인지)

헤더 행 처리
------------

**증상**: 첫 번째 행이 데이터로 인식됨

**해결 방법**:

헤더 행이 있는 경우:

::

    has_header_line=true

헤더 행이 없는 경우:

::

    has_header_line=false

데이터를 가져올 수 없음
------------------------

**증상**: 크롤링은 성공하지만 건수가 0

**확인 사항**:

1. CSV 파일이 비어 있지 않은지 확인
2. 스크립트 설정이 올바른지 확인(열 이름·``cell<N>`` 참조가 ``data.`` 접두사 없이 되어 있는지)
3. 열 이름이 올바른지 확인(has_header_line=true인 경우)
4. 로그에서 오류 메시지 확인

대형 CSV 파일
-------------

**증상**: 메모리 부족 또는 타임아웃

**해결 방법**:

1. CSV 파일을 여러 개로 분할
2. 필요한 열만 스크립트에서 사용
3. |Fess| 의 힙 크기 증가
4. 불필요한 행 필터링

줄바꿈을 포함하는 필드
----------------------

RFC 4180 형식에서는 인용 부호로 감싸면 줄바꿈을 포함하는 필드를 처리할 수 있습니다.
인용 부호 처리는 기본적으로 비활성화되어 있으므로 ``quote_disabled=false`` 지정이 필요합니다:

::

    id,title,description
    1,"Product A","This is
    a multi-line
    description"
    2,"Product B","Single line"

파라미터:

::

    files=/var/data/data.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_disabled=false
    quote_character="

CsvListDataStore
================

``fess-ds-csv`` 플러그인에는 ``CsvDataStore`` 외에 ``CsvListDataStore`` 핸들러도 포함되어 있습니다.

``CsvListDataStore`` 는 ``CsvDataStore`` 를 확장하여 다음의 추가 기능을 제공합니다:

- 멀티스레드 처리( ``numOfThreads`` 파라미터로 제어)
- 처리 완료된 CSV 파일의 자동 삭제
- 타임스탬프 기반 파일 필터링(쓰기 중인 파일 건너뜀)

``CsvDataStore`` 의 모든 파라미터 및 스크립트 설정을 그대로 사용할 수 있습니다.

기본 설정
---------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 항목
     - 설정 예
   * - 핸들러 이름
     - CsvListDataStore

추가 파라미터
-------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``timestamp_margin``
     - 아니오
     - 파일의 마지막 수정 시각으로부터 경과 시간(밀리초). 이 시간이 경과하지 않은 파일은 쓰기 중으로 간주하여 건너뜁니다(기본값: 10000)
   * - ``numOfThreads``
     - 아니오
     - 처리 스레드 수(기본값: 1)

.. note::

   ``CsvListDataStore`` 는 처리 완료 후 CSV 파일을 자동으로 삭제합니다. 처리 중에 오류가 발생한 경우, 파일은 ``.txt`` 로 이름이 변경됩니다(이름 변경에 실패한 경우에는 삭제됩니다).

스크립트 고급 사용 예
=====================

데이터 가공
-----------

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=Integer.parseInt(price)
    category=category.toLowerCase()

조건부 인덱싱
-------------

::

    // 가격이 10000 이상인 상품만 인덱싱
    url=Integer.parseInt(price) >= 10000 ? "https://example.com/product/" + id : null
    title=Integer.parseInt(price) >= 10000 ? name : null
    content=Integer.parseInt(price) >= 10000 ? description : null
    price=Integer.parseInt(price) >= 10000 ? price : null

복수 열 결합
------------

::

    url="https://example.com/product/" + id
    title=name
    content=description + "\n\n사양:\n" + specs + "\n\n주의사항:\n" + notes
    category=category

날짜 형식
---------

::

    url="https://example.com/article/" + id
    title=title
    content=content
    created=created_date
    // 날짜 형식 변환이 필요한 경우 추가 처리

참고 정보
=========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-json` - JSON 커넥터
- :doc:`ds-database` - 데이터베이스 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `RFC 4180 - CSV 형식 <https://datatracker.ietf.org/doc/html/rfc4180>`_
