===========================================
데이터베이스·CSV·Salesforce 데이터 검색하기
===========================================

들어가며
========

제품 마스터는 사내 데이터베이스에, 거래처 목록은 기간 시스템이 매일 밤 내보내는 CSV에, 영업 기회와 문의 기록은 Salesforce에 들어 있습니다.
이런 업무 데이터는 각 시스템의 화면에서만 찾을 수 있는 경우가 많습니다.
Fess의 데이터 저장소 플러그인을 사용하면 이 데이터를 레코드 단위로 가져와서, 파일 서버나 사내 사이트의 문서와 같은 검색 화면에서 찾을 수 있게 됩니다.

이 글에서는 세 가지 정보원을 각각 가져오는 설정과, 정보원별 필터링, 실행 스케줄, 결과 확인 방법을 설명합니다.
플러그인 설치, 핸들러 이름·파라미터·스크립트 작성법, 작업 만들기와 같은 데이터 저장소 공통 절차는 :doc:`datastore-basics`\ 에 정리되어 있습니다.
먼저 그 글을 읽은 다음 진행하십시오.
글에 나오는 설정값은 Fess 15.9와 각 플러그인의 15.9.0 버전에 맞추었습니다.

이 글에서 만드는 구성
=====================

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - 정보원
     - 플러그인
     - 핸들러 이름
     - 미리 준비할 것
   * - 데이터베이스(제품 마스터)
     - ``fess-ds-db``
     - ``DatabaseDataStore``
     - JDBC 드라이버 jar 파일과, SELECT만 할 수 있는 DB 사용자
   * - CSV(거래처 목록)
     - ``fess-ds-csv``
     - ``CsvDataStore``
     - CSV를 내보낼 디렉터리(크롤러가 읽을 수 있는 위치)
   * - Salesforce(거래처·영업 기회·케이스)
     - ``fess-ds-salesforce``
     - ``SalesforceDataStore``
     - Connected App과, JWT 서명용 키 쌍

Docker로 운영하는 경우에는 ``compose.yaml``\ 의 ``fess01``\ 의 ``environment``\ 에 세 플러그인을 공백으로 구분하여 지정합니다.

.. code-block:: yaml

    environment:
      - "FESS_PLUGINS=fess-ds-db:15.9.0 fess-ds-csv:15.9.0 fess-ds-salesforce:15.9.0"

관리 화면이나 ``fess-setup``\ 으로 설치한 경우에는 Fess를 다시 시작해야 합니다.

먼저 정할 것: 검색 결과를 누구에게 보여 줄 것인가
=================================================

세 플러그인 모두 원래 시스템의 열람 권한(ACL)을 Fess로 가져오지 않습니다.
가져온 문서의 롤은 데이터 저장소 설정의 "권한" 칸에 입력한 값만으로 정해집니다.
이 칸에는 처음부터 ``{role}guest``\ 가 들어 있어서, 그대로 두면 로그인하지 않은 사용자도 검색할 수 있습니다.

가격이나 고객 정보가 포함된 데이터라면 이 칸을 보여 줄 그룹으로 바꿉니다(예: ``{group}sales``).
하나의 설정에서 등록되는 문서에는 모두 같은 권한이 붙습니다.
보여 줄 대상이 다른 데이터는 별도의 데이터 저장소 설정으로 나누십시오.
그룹 설계는 :doc:`guide-05`\ 를 참조하십시오.

데이터베이스: 제품 마스터 가져오기
==================================

JDBC 드라이버 배치하기
----------------------

``fess-ds-db``\ 에는 JDBC 드라이버가 포함되어 있지 않습니다.
접속할 데이터베이스에 맞는 드라이버 jar 파일(PostgreSQL이면 ``postgresql-<버전>.jar``, MySQL이면 ``mysql-connector-j-<버전>.jar``)을 구해서 크롤러의 클래스 경로에 둡니다.
데이터 저장소 크롤링은 Fess 본체와는 별도의 크롤러 프로세스에서 실행되며, 그 클래스 경로에는 다음 두 디렉터리의 jar가 포함됩니다.

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

ZIP 패키지에서는 Fess의 압축을 푼 디렉터리 아래에, RPM / DEB에서는 ``/usr/share/fess/`` 아래에 있습니다.
파일을 둔 다음 Fess를 다시 시작합니다.

Docker 이미지에서도 Fess는 ``/usr/share/fess/``\ 에 있습니다.
컨테이너 안에 복사한 jar는 컨테이너를 다시 만들면 사라지므로, ``compose.yaml``\ 의 ``fess01``\ 에 jar 파일 하나만 마운트합니다.

.. code-block:: yaml

    volumes:
      - ./postgresql-42.7.4.jar:/usr/share/fess/app/WEB-INF/env/crawler/lib/postgresql.jar:ro

디렉터리째 마운트하면 이미지가 그 디렉터리에 둔 jar가 보이지 않게 되어 크롤러가 시작되지 않습니다.
반드시 파일 단위로 마운트하십시오.
변경한 후에는 ``docker compose -f compose.yaml -f compose-opensearch3.yaml up -d``\ 로 컨테이너를 다시 만듭니다.

파라미터와 SQL
--------------

여기서는 PostgreSQL의 ``products`` 테이블을 예로 듭니다.
검색 결과의 링크 대상으로는 제품 마스터의 조회 화면(예: ``https://erp.example.com/products/<제품ID>``)을 사용합니다.
[크롤러] > [데이터 저장소] > [새로 만들기]에서 핸들러 이름으로 ``DatabaseDataStore``\ 를 선택하고, 파라미터를 다음과 같이 입력합니다.

.. code-block:: properties

    script_type=javascript
    driver=org.postgresql.Driver
    url=jdbc:postgresql://db.example.com:5432/erp
    username=fess_reader
    password=your-password
    query_timeout=600
    sql=SELECT p.product_id, concat('https://erp.example.com/products/', p.product_id) AS page_url, p.product_name AS title, concat_ws(' ', p.product_name, p.model_number, c.category_name, p.description) AS body, p.updated_at FROM products p JOIN categories c ON c.category_id = p.category_id WHERE p.discontinued = false

스크립트는 다음과 같습니다.

.. code-block:: properties

    url=page_url
    title=title
    content=body
    last_modified=updated_at
    label="products"

``sql``\ 은 한 줄로 작성합니다.
SQL은 그대로 데이터베이스에 전송되며, 결과의 한 행이 한 건의 문서가 됩니다.
링크 대상 URL과 본문을 SQL 안에서 조립해 두면 스크립트에는 열 이름만 쓰면 됩니다.
``concat_ws``\ 는 NULL인 열을 건너뛰고 연결하므로, 설명이 비어 있는 제품이라도 본문이 NULL이 되지 않습니다.
MySQL에서도 ``CONCAT_WS``\ 는 같은 동작을 하지만, ``CONCAT``\ 은 인수에 NULL이 있으면 결과 전체가 NULL이 됩니다.

Docker로 운영하는 경우 ``url``\ 의 ``localhost``\ 는 데이터베이스 서버가 아니라 Fess 컨테이너 자신을 가리킵니다.
데이터베이스의 호스트 이름이나 IP 주소를 입력하십시오.

열 이름과 스크립트의 대응
-------------------------

스크립트의 우변에는 SELECT 결과의 열 레이블(``AS``\ 로 붙인 별칭)을 그대로 씁니다.
다음 세 가지에 주의하십시오.

- 열 레이블의 대소문자는 데이터베이스에 따라 달라집니다. 따옴표로 감싸지 않은 별칭을 PostgreSQL은 소문자로, Oracle과 H2는 대문자로 바꾸고, MySQL은 쓴 그대로 돌려줍니다. 스크립트에는 데이터베이스가 돌려주는 대소문자 그대로 씁니다. 일치하지 않으면 해당 필드에 값이 들어가지 않습니다
- 스크립트에서는 파라미터 칸의 값도 같은 이름의 변수로 보입니다. 결과에 ``url`` 열이 없는 상태에서 ``url=url``\ 이라고 쓰면 JDBC 접속 URL이 문서의 URL이 됩니다. 링크 대상 열에는 ``page_url``\ 처럼 파라미터와 겹치지 않는 이름을 붙이십시오
- 멈춘 쿼리는 작업을 중지해도 멈추지 않습니다. ``query_timeout``\ (초)을 반드시 설정합니다

``fess-ds-db``\ 에는 증분 크롤링 옵션이 없습니다.
실행할 때마다 ``sql`` 전체를 실행하여 모든 행을 다시 등록합니다.
행 수가 많은 테이블에서는 데이터베이스 부하가 낮은 시간대에 작업을 실행하십시오(뒤의 "정보원별로 작업 만들기" 참조).

CSV: 기간 시스템이 내보내는 거래처 목록 가져오기
================================================

CSV 커넥터의 기본 사용법은 :doc:`datastore-basics`\ 의 CSV 파일 예제 절에서 설명합니다.
여기서는 기간 시스템이 정기적으로 내보내는 CSV를 가져올 때 필요한 점만 보충합니다.

예로, 일본의 기간 시스템이 매일 밤 2:00에 다음과 같은 ``customers_20261128.csv``\ 를 내보낸다고 합시다.
문자 코드는 MS932(Windows용 Shift_JIS)이고, 1행은 일본어 제목 행(거래처 코드, 거래처명, 소재지, 담당 부서, 거래 상태)입니다.

.. code-block:: text

    取引先コード,取引先名,所在地,担当部署,取引状況
    C0001,株式会社サンプル商事,東京都千代田区,第一営業部,取引中
    C0002,サンプル工業株式会社,大阪府大阪市,第二営業部,取引終了

파일을 두는 위치
----------------

CSV는 Fess 크롤러가 실행되는 서버에서 읽을 수 있는 경로에 내보냅니다.
Docker에서는 내보내기 대상 디렉터리를 ``fess01``\ 에 읽기 전용으로 마운트합니다.

.. code-block:: yaml

    volumes:
      - ./export/customers:/data/customers:ro

파라미터와 스크립트
-------------------

.. code-block:: properties

    script_type=javascript
    directories=/data/customers
    file_encoding=MS932
    has_header_line=true

.. code-block:: javascript

    url=cell5 == "取引中" ? "https://crm.example.com/customers/" + cell1 : null
    title=cell2
    content=cell2 + " " + cell3 + " " + cell4
    label="customers"

- ``directories``\ 를 지정하면 그 디렉터리 안의 확장자 ``.csv`` / ``.tsv`` 파일을 모두, 수정 시각이 오래된 순서로 읽습니다. 날짜가 붙은 파일 이름으로 매일 내보내는 경우에도 파라미터를 고치지 않아도 됩니다. 오래된 파일을 남겨 두면 그 파일의 행도 매번 읽힙니다
- 일본어판 Excel이나 일본어 Windows용 시스템이 내보내는 CSV는 대부분 MS932입니다. ``Shift_JIS``\ 를 지정하면 ``①``\ 이나 ``㈱`` 같은 문자가 대체 문자로 바뀌므로 ``MS932``\ 를 지정합니다
- 이 예처럼 제목이 일본어 등 비ASCII 문자여도 ``has_header_line=true``\ 로 1행을 건너뛸 수 있습니다. 스크립트에서는 열 번호(``cell1``, ``cell2`` …)로 참조하는 것이 확실합니다. 제목에 공백이나 기호가 포함된 열은 제목 이름으로 참조할 수 없습니다
- 탭으로 구분된 파일에는 ``separator_character=\t``\ 를 추가합니다
- ``url``\ 이 ``null``\ 이 된 행은 등록되지 않습니다. 이 예에서는 상태가 取引終了(거래 종료)인 거래처를 제외하고 取引中(거래 중)인 거래처만 등록합니다. 제외한 행 수는 ``fess-crawler.log``\ 에 ``Skipped 1 row(s) in ... because the script did not set the url field.``\ 라는 WARN으로 출력됩니다

내보내는 도중의 파일을 읽으면 그때까지 쓰인 행만 등록됩니다.
작업은 CSV 내보내기가 끝나는 시각보다 뒤에 실행하십시오.

Salesforce: 거래처·영업 기회·케이스 가져오기
============================================

Salesforce 측 준비
------------------

``fess-ds-salesforce``\ 는 ``auth_type=oauth_token``\ (JWT 베어러 플로)과 ``auth_type=oauth_password``\ (사용자 이름과 비밀번호)의 두 가지 인증 방식을 지원합니다.
여기서는 비밀번호를 저장하지 않아도 되는 ``oauth_token``\ 을 사용합니다.
``oauth_password``\ 에서 쓰는 사용자 이름·비밀번호 방식의 OAuth 플로는 Salesforce 조직의 설정에 따라 비활성화되어 있을 수 있습니다.

1. 키 쌍과 인증서를 만듭니다

   .. code-block:: bash

       openssl genrsa -out private_key.pem 2048
       openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

2. Salesforce Setup에서 Connected App을 만들고 OAuth 설정을 활성화한 다음, "디지털 서명 사용"에 ``certificate.crt``\ 를 업로드합니다. OAuth 범위는 레퍼런스에 적힌 대로 선택합니다
3. Connected App의 정책에서 "허용된 사용자"를 "관리자가 승인한 사용자만 사전 승인"으로 설정하고, 크롤링에 사용할 사용자의 프로필이나 권한 세트를 할당합니다
4. Connected App의 Consumer Key를 적어 둡니다

Salesforce 측의 화면과 명칭은 바뀔 수 있으므로, 자세한 내용은 Salesforce 도움말의 JWT 베어러 플로 설명도 확인하십시오.

Fess가 가져올 수 있는 것은 크롤링에 사용하는 사용자가 읽을 수 있는 레코드와 필드뿐입니다.
읽을 수 없는 필드를 뒤에서 설명하는 ``contents``\ 에 지정하면 해당 오브젝트를 가져오는 데 실패합니다.

파라미터와 스크립트
-------------------

``private_key``\ 에는 ``private_key.pem``\ 의 내용을, 줄바꿈을 ``\n``\ 으로 바꾸어 한 줄로 씁니다.
플러그인이 읽을 수 있는 것은 PKCS#8 형식(``-----BEGIN PRIVATE KEY-----``\ 로 시작하는 형식)뿐입니다.
오래된 OpenSSL로 만든 ``-----BEGIN RSA PRIVATE KEY-----``\ 로 시작하는 키는 ``openssl pkcs8 -topk8 -nocrypt -in private_key.pem -out private_key_pkcs8.pem``\ 으로 변환한 다음 사용합니다.

.. code-block:: properties

    script_type=javascript
    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=fess-crawler@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n
    include_pattern=.*/(001|006|500)[A-Za-z0-9]+
    OPPORTUNITY.contents=Name,StageName,NextStep,Description

.. code-block:: javascript

    url=object.url
    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    last_modified=object.last_modified
    label="salesforce"

Sandbox를 대상으로 할 때는 ``base_url=https://test.salesforce.com``\ 으로 합니다.

우변의 항목은 모두 ``object.``\ 로 시작합니다.
``url=url``\ 처럼 접두사 없이 쓰면 식의 평가가 실패하여, 레코드는 등록되지 않고 장애 URL에 기록됩니다.
``object.url``\ 은 ``<인스턴스 URL>/<레코드 ID>`` 형식이며, 클릭하면 Salesforce의 레코드 화면이 열립니다.

가져올 범위 좁히기
------------------

``fess-ds-salesforce``\ 는 Account, Contact, Lead, Opportunity, Case, Task, User 등 23종의 표준 오브젝트를 항상 모두 읽습니다.
오브젝트를 골라서 읽는 설정은 없습니다.
범위를 좁히려면 다음 세 가지를 조합합니다.

- ``include_pattern`` / ``exclude_pattern``: ``object.url`` 전체와 일치하는 정규 표현식으로, 등록할 레코드를 고릅니다. Salesforce 레코드 ID의 앞 세 글자는 오브젝트마다 정해져 있습니다(Account ``001``, Opportunity ``006``, Case ``500`` 등). 위의 예는 이 세 종류만 등록합니다. 가져오기 자체는 모든 오브젝트에 대해 이루어지고, 등록 전에 버려질 뿐입니다
- ``<오브젝트 이름>.title`` / ``<오브젝트 이름>.contents``: 제목과 본문에 사용할 필드를 필드의 API 이름으로 지정합니다. 표준 오브젝트의 이름은 ``ACCOUNT``, ``OPPORTUNITY``, ``CASE``\ 처럼 대문자 스네이크 케이스입니다. 지정하지 않으면 플러그인의 기본 필드가 사용됩니다
- ``custom``: 커스텀 오브젝트의 API 이름을 쉼표로 구분하여 지정하면 표준 오브젝트에 더해 읽습니다

커스텀 오브젝트에는 기본 필드가 없으므로 ``.title``\ 과 ``.contents``\ 를 반드시 지정합니다.
제목 필드는 본문 필드에도 포함하십시오.
플러그인은 ``.contents`` 등에 쓴 필드만 가져오므로, ``.title``\ 에만 쓴 필드는 가져오지 않아 제목이 비게 됩니다.

.. code-block:: properties

    custom=Project__c
    Project__c.title=Name
    Project__c.contents=Name,Customer_Name__c,Summary__c

라벨로 정보원별로 필터링하기
============================

지금까지의 예에서는 스크립트의 ``label``\ 로 ``products``, ``customers``, ``salesforce``\ 를 붙였습니다.
검색 화면의 라벨 선택지에 표시하려면 [크롤러] > [라벨]에서 같은 "값"을 가진 라벨을 만듭니다("대상 경로"는 비워 두어도 됩니다).
라벨 값에는 영숫자와 ``_``\ 만 사용할 수 있습니다.

Salesforce 데이터를 오브젝트별로 나누고 싶다면, 스크립트의 ``label`` 대신 "대상 경로"에서 레코드 ID의 앞 세 글자를 보는 라벨을 만듭니다.
예를 들어 값이 ``sf_case``, 대상 경로가 ``https://example\.my\.salesforce\.com/500.*``\ 인 라벨은 케이스에만 붙습니다.
URL과 일치하는 라벨이 있으면 스크립트로 붙인 라벨은 사라집니다.
하나의 데이터 저장소 설정에서는 두 방법 중 하나만 사용하십시오(자세한 내용은 :doc:`datastore-basics`\ 의 라벨 절).

정보원별로 작업 만들기
======================

초기 상태의 "Default Crawler"는 매일 0:00에 모든 설정을 한꺼번에 크롤링합니다.
정보원마다 적당한 시각이 다르므로, 데이터 저장소 설정마다 작업을 만듭니다.
각 설정의 상세 화면에서 [새 작업 작성]을 클릭하고 "스케줄"에 cron 형식으로 시각을 입력합니다(절차는 :doc:`datastore-basics`\ 의 스케줄 절).

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - 정보원
     - 스케줄 예
     - 고려할 점
   * - 데이터베이스
     - ``0 3 * * *``
     - 매번 모든 행을 읽으므로 데이터베이스 부하가 낮은 시간대로 한다
   * - CSV
     - ``30 2 * * *``
     - 내보내기가 끝나는 시각보다 뒤로 한다
   * - Salesforce
     - ``0 7,12,18 * * *``
     - 한 번 실행할 때마다 표준 오브젝트와 커스텀 오브젝트 수만큼 Bulk API 작업을 만든다. 조직의 API 제한 잔량을 보고 횟수를 정한다

Default Crawler도 계속 이 설정들을 크롤링합니다.
중복 실행을 원하지 않으면 데이터 저장소 설정의 "상태"를 "무효"로 합니다(설정 ID를 지정한 작업은 무효인 설정도 크롤링합니다).

원본 데이터에서 사라진 행의 처리
================================

데이터베이스의 행을 삭제하거나 CSV에서 행이 없어져도, 해당 문서는 다음 크롤링에서 삭제되지 않습니다.
데이터 저장소로 등록한 문서에는 유효 기간이 붙으며, 기한은 등록할 때마다 연장됩니다.
더 이상 등록되지 않는 문서는 마지막으로 등록된 뒤 [시스템] > [일반]의 "이전 문서 삭제" 일수(기본값 3일)가 지나면 자동으로 삭제됩니다.

이 구조에는 주의가 필요한 면도 있습니다.
데이터베이스에 접속할 수 없는 날이 계속되어 이 일수를 넘기면, 그 설정의 문서가 모두 검색 결과에서 사라집니다.
가져오기 실패는 다음 절의 방법으로 일찍 발견하십시오.

동작 확인하기
=============

작업 로그, [시스템 정보] > [크롤링 정보], 장애 URL, ``fess-crawler.log``\ 를 보는 방법은 :doc:`datastore-basics`\ 의 결과 확인 절에서 설명합니다.
데이터 저장소 크롤링은 가져오기에 실패해도 작업이 "OK"가 되는 경우가 있으므로, 건수와 로그로 판단하십시오.

1. [시스템 정보] > [검색]에서 ``label:products``, ``label:customers``, ``label:salesforce``\ 로 검색하여 건수를 원본 데이터와 비교합니다(데이터베이스라면 ``sql``\ 과 같은 조건의 ``SELECT count(*)``)
2. ``fess-crawler.log``\ 의 WARN과 ERROR를 확인합니다. 이 글의 구성에서 나오기 쉬운 메시지는 다음과 같습니다

   - ``The JDBC driver ... is not on the crawler classpath.``: 드라이버의 위치나 ``driver``\ 의 클래스 이름이 잘못되었다
   - ``Failed to connect to ...``: 데이터베이스의 호스트 이름·포트·사용자 이름·비밀번호를 확인한다
   - ``is not a directory.``\ 나 ``No CSV file.``: ``directories`` 경로에 크롤러가 읽을 수 있는 CSV가 없다
   - ``Batch:... Failed caused by ...``: Salesforce의 일부 오브젝트를 가져오지 못했다. ``.contents``\ 의 필드 이름이나, 크롤링에 사용하는 사용자의 필드 권한을 확인한다
   - ``Failed to process a data crawling: <설정 이름>``: 설정 전체가 실패했다. Salesforce에서는 인증 실패가 여기에 해당한다. 이어지는 스택 트레이스에서 원인을 확인한다

3. "권한" 칸을 바꾼 설정에서는 대상 그룹의 사용자로 로그인하여 검색 결과에 나오는지, 로그아웃한 상태에서는 나오지 않는지 확인합니다

정리
====

- 세 플러그인 모두 원래 시스템의 권한을 가져오지 않으므로, "권한" 칸의 ``{role}guest``\ 를 보여 줄 그룹으로 바꿉니다
- 데이터베이스는 JDBC 드라이버를 크롤러의 클래스 경로에 두고, 링크 대상 URL과 본문을 SQL로 조립합니다. 매번 모든 행을 읽습니다
- 기간 시스템의 CSV는 ``directories``\ 와 ``file_encoding=MS932``\ 로 읽고 ``cellN``\ 으로 참조합니다. ``url``\ 을 ``null``\ 로 한 행은 등록되지 않습니다
- Salesforce의 스크립트는 ``object.*``\ 로 씁니다. 표준 오브젝트는 고를 수 없으므로 ``include_pattern``\ 과 ``<오브젝트 이름>.contents``\ 로 좁힙니다
- 정보원별로 작업을 만들고, 원본 데이터에서 사라진 행은 "이전 문서 삭제" 일수가 지난 뒤 사라진다는 것을 전제로 운영합니다

다음에 읽을 글
==============

- 데이터 저장소의 공통 구조(스크립트, 권한, 라벨, 결과 확인 방법): :doc:`datastore-basics`
- Git, Confluence, Jira, Slack을 가져오고 싶다: :doc:`guide-06`
- Google Drive, SharePoint, Box를 가져오고 싶다: :doc:`guide-07`
- 부서별로 보이는 검색 결과를 바꾸고 싶다: :doc:`guide-05`
- 가져오기 실패를 모니터링하고 싶다: :doc:`guide-10`

참고 자료
=========

- `데이터베이스 커넥터 <https://fess.codelibs.org/ko/stable/config/datastore/ds-database.html>`__
- `CSV 커넥터 <https://fess.codelibs.org/ko/stable/config/datastore/ds-csv.html>`__
- `Salesforce 커넥터 <https://fess.codelibs.org/ko/stable/config/datastore/ds-salesforce.html>`__
- `데이터 저장소 설정 <https://fess.codelibs.org/ko/stable/admin/dataconfig-guide.html>`__
- `스케줄러 <https://fess.codelibs.org/ko/stable/admin/scheduler-guide.html>`__
- `라벨 <https://fess.codelibs.org/ko/stable/admin/labeltype-guide.html>`__
- `일반 <https://fess.codelibs.org/ko/stable/admin/general-guide.html>`__
