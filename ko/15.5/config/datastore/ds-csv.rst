==================================
CSV 커넥터
==================================

개요
====

CSV 커넥터는 CSV 파일에서 데이터를 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-csv`` 플러그인이 필요합니다.

전제조건
========

1. 플러그인 설치가 필요합니다
2. CSV 파일에 대한 액세스 권한이 필요합니다
3. CSV 파일의 문자 인코딩을 파악하고 있어야 합니다

플러그인 설치
------------------------

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
========

관리 화면에서 "크롤러" → "데이터 스토어" → "새로 만들기"에서 설정합니다.

기본 설정
--------

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
----------------

로컬 파일:

::

    file_path=/path/to/data.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

HTTP 파일:

::

    file_path=https://example.com/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

복수 파일:

::

    file_path=/path/to/data1.csv,/path/to/data2.csv,https://example.com/data3.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

파라미터 목록
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``file_path``
     - 예
     - CSV 파일 경로(로컬, HTTP, 복수 지정 가능: 쉼표 구분)
   * - ``encoding``
     - 아니오
     - 문자 인코딩(기본값: UTF-8)
   * - ``has_header``
     - 아니오
     - 헤더 행 유무(기본값: true)
   * - ``separator``
     - 아니오
     - 구분 문자(기본값: 쉼표 ``,``)
   * - ``quote``
     - 아니오
     - 인용 부호(기본값: 큰따옴표 ``"``)

스크립트 설정
--------------

헤더가 있는 경우:

::

    url="https://example.com/product/" + data.product_id
    title=data.product_name
    content=data.description
    digest=data.category
    price=data.price

헤더가 없는 경우(열 인덱스 지정):

::

    url="https://example.com/product/" + data.col0
    title=data.col1
    content=data.col2
    price=data.col3

사용 가능한 필드
~~~~~~~~~~~~~~~~~~~~

- ``data.<열명>`` - 헤더 행의 열명(has_header=true인 경우)
- ``data.col<N>`` - 열 인덱스(has_header=false인 경우, 0부터 시작)

CSV 형식 상세
=============

표준 CSV(RFC 4180 준수)
-----------------------

::

    product_id,product_name,description,price,category
    1,Laptop,High-performance laptop,150000,Electronics
    2,Mouse,Wireless mouse,3000,Electronics
    3,"Book, Programming","Learn to code",2800,Books

구분자 변경
------------------

탭 구분(TSV):

::

    # 파라미터
    separator=\t

세미콜론 구분:

::

    # 파라미터
    separator=;

커스텀 인용 부호
--------------

작은따옴표:

::

    # 파라미터
    quote='

인코딩
----------------

일본어 파일(Shift_JIS):

::

    encoding=Shift_JIS

일본어 파일(EUC-JP):

::

    encoding=EUC-JP

사용 예
======

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

    file_path=/var/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

스크립트:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " 카테고리: " + data.category + " 가격: " + data.price + "원"
    digest=data.category
    price=data.price

재고 정보 필터링:

::

    if (data.in_stock == "true") {
        url="https://shop.example.com/product/" + data.product_id
        title=data.name
        content=data.description
        price=data.price
    }

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

    file_path=/var/data/employees.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

스크립트:

::

    url="https://intranet.example.com/employee/" + data.emp_id
    title=data.name + " (" + data.department + ")"
    content="부서: " + data.department + "\n직책: " + data.position + "\n이메일: " + data.email + "\n전화: " + data.phone
    digest=data.department

헤더 없는 CSV
-----------------

CSV 파일(data.csv):

::

    1,상품A,상품A에 대한 설명입니다,1000
    2,상품B,상품B에 대한 설명입니다,2000
    3,상품C,상품C에 대한 설명입니다,3000

파라미터:

::

    file_path=/var/data/data.csv
    encoding=UTF-8
    has_header=false
    separator=,
    quote="

스크립트:

::

    url="https://example.com/item/" + data.col0
    title=data.col1
    content=data.col2
    price=data.col3

복수 CSV 파일 통합
---------------------

파라미터:

::

    file_path=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

스크립트:

::

    url="https://example.com/report/" + data.id
    title=data.title
    content=data.content
    timestamp=data.date

HTTP에서 CSV 가져오기
-----------------

파라미터:

::

    file_path=https://example.com/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

스크립트:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description

탭 구분(TSV) 파일
-------------------------

TSV 파일(data.tsv):

::

    id	title	content	category
    1	기사1	기사1의 내용입니다	뉴스
    2	기사2	기사2의 내용입니다	블로그

파라미터:

::

    file_path=/var/data/data.tsv
    encoding=UTF-8
    has_header=true
    separator=\t
    quote="

스크립트:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    digest=data.category

문제 해결
======================

파일을 찾을 수 없음
----------------------

**증상**: ``FileNotFoundException`` 또는 ``No such file``

**확인 사항**:

1. 파일 경로가 올바른지 확인(절대 경로 권장)
2. 파일이 존재하는지 확인
3. 파일의 읽기 권한이 있는지 확인
4. |Fess| 실행 사용자가 액세스 가능한지 확인

문자 깨짐 발생
------------------

**증상**: 한글이 올바르게 표시되지 않음

**해결 방법**:

올바른 문자 인코딩 지정:

::

    # UTF-8
    encoding=UTF-8

    # EUC-KR
    encoding=EUC-KR

    # Windows 표준(CP949)
    encoding=CP949

파일 인코딩 확인:

::

    file -i data.csv

열이 올바르게 인식되지 않음
----------------------

**증상**: 열 구분이 올바르게 인식되지 않음

**확인 사항**:

1. 구분 문자가 올바른지 확인:

   ::

       # 쉼표
       separator=,

       # 탭
       separator=\t

       # 세미콜론
       separator=;

2. 인용 부호 설정 확인
3. CSV 파일 형식 확인(RFC 4180 준수인지)

헤더 행 처리
----------------

**증상**: 첫 번째 행이 데이터로 인식됨

**해결 방법**:

헤더 행이 있는 경우:

::

    has_header=true

헤더 행이 없는 경우:

::

    has_header=false

데이터를 가져올 수 없음
--------------------

**증상**: 크롤링은 성공하지만 건수가 0

**확인 사항**:

1. CSV 파일이 비어 있지 않은지 확인
2. 스크립트 설정이 올바른지 확인
3. 열명이 올바른지 확인(has_header=true인 경우)
4. 로그에서 오류 메시지 확인

대형 CSV 파일
-----------------

**증상**: 메모리 부족 또는 타임아웃

**해결 방법**:

1. CSV 파일을 여러 개로 분할
2. 필요한 열만 스크립트에서 사용
3. |Fess|의 힙 크기 증가
4. 불필요한 행 필터링

줄바꿈을 포함하는 필드
--------------------

RFC 4180 형식에서는 인용 부호로 감싸면 줄바꿈을 포함하는 필드를 처리할 수 있습니다:

::

    id,title,description
    1,"Product A","This is
    a multi-line
    description"
    2,"Product B","Single line"

파라미터:

::

    file_path=/var/data/data.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

스크립트 고급 사용 예
========================

데이터 가공
------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=parseInt(data.price)
    category=data.category.toLowerCase()

조건부 인덱싱
--------------------

::

    # 가격이 10000 이상인 상품만
    if (parseInt(data.price) >= 10000) {
        url="https://example.com/product/" + data.id
        title=data.name
        content=data.description
        price=data.price
    }

복수 열 결합
------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description + "\n\n사양:\n" + data.specs + "\n\n주의사항:\n" + data.notes
    category=data.category

날짜 형식
------------------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    created=data.created_date
    # 날짜 형식 변환이 필요한 경우 추가 처리

참고 정보
========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-json` - JSON 커넥터
- :doc:`ds-database` - 데이터베이스 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `RFC 4180 - CSV 형식 <https://datatracker.ietf.org/doc/html/rfc4180>`_
