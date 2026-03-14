==================================
JSON 커넥터
==================================

개요
====

JSON 커넥터는 JSON 파일 또는 JSON API에서 데이터를 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-json`` 플러그인이 필요합니다.

전제조건
========

1. 플러그인 설치가 필요합니다
2. JSON 파일 또는 API에 대한 액세스 권한이 필요합니다
3. JSON 구조를 이해하고 있어야 합니다

플러그인 설치
------------------------

방법 1: JAR 파일 직접 배치

::

    # Maven Central에서 다운로드
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # 배치
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 또는
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

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
     - Products JSON
   * - 핸들러 이름
     - JsonDataStore
   * - 활성화
     - 켬

파라미터 설정
----------------

로컬 파일:

::

    files=/path/to/data.json
    fileEncoding=UTF-8

HTTP 파일:

::

    files=https://api.example.com/products.json
    fileEncoding=UTF-8

REST API(인증 있음):

::

    files=https://api.example.com/v1/items
    fileEncoding=UTF-8

복수 파일:

::

    files=/path/to/data1.json,https://api.example.com/data2.json
    fileEncoding=UTF-8

파라미터 목록
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``files``
     - 예
     - JSON 파일 경로 또는 API URL(복수 지정 가능: 쉼표 구분)
   * - ``fileEncoding``
     - 아니오
     - 문자 인코딩(기본값: UTF-8)
