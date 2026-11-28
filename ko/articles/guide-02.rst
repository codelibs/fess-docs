====================================
Docker로 Fess를 실행하고 검색해 보기
====================================

들어가며
========

Fess를 검토하기 시작할 때 가장 먼저 알고 싶은 것은 "내 환경에서 실행하면 어떤 검색을 할 수 있는가"입니다.
이 글에서는 Docker로 Fess 15.9를 기동하고, 웹 페이지 20개 정도를 크롤링한 뒤, 검색 구문을 시험해 보는 데까지 차례대로 진행합니다.

소재로는 Fess 공식 사이트에 있는 한국어 "검색 가이드"(AND 검색이나 와일드카드 검색 등을 설명하는 페이지 모음)를 사용합니다.
대상을 한 곳으로 좁히므로 크롤링은 몇 분 안에 끝나고, 검색 결과의 내용도 직접 읽어 확인할 수 있습니다.

이 글의 절차를 그대로 실행하면 다음을 할 수 있게 됩니다.

- Fess와 OpenSearch를 Docker Compose로 기동하고, 중지·재개하기
- 관리자의 첫 로그인과, 요구되는 비밀번호 변경을 마치기
- 웹 크롤링 설정을 만들고, 크롤링을 실행하고, 완료를 확인하기
- AND·OR·제외·구문·필드 지정 검색을 시험하기

운영 환경용 설정(모니터링, 백업, SSO, 규모 확장)은 다루지 않습니다.
마지막의 "다음에 읽을 글"에서 목적에 맞는 글로 넘어가십시오.

이 글에서 만드는 환경
=====================

docker-fess 저장소의 Compose 파일을 사용하면 다음 2개의 컨테이너가 기동합니다.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 서비스
     - 역할
     - 데이터 저장 위치
   * - ``fess01``
     - Fess 본체(이미지 ``ghcr.io/codelibs/fess:15.9.0``). 포트 8080에서 검색 화면과 관리 화면을 제공합니다
     - 볼륨 없음(컨테이너 내부)
   * - ``search01``
     - OpenSearch(이미지 ``ghcr.io/codelibs/fess-opensearch``). 포트 9200도 공개됩니다
     - 볼륨 ``search01_data``\ 와 ``search01_dictionary``

인덱스, 크롤링 설정, 사용자, 작업 로그 등은 모두 OpenSearch에 저장되므로 ``search01_data`` 볼륨에 남습니다.
반면 관리 화면의 [시스템] > [일반]에서 변경한 설정은 ``fess01`` 컨테이너 내부의 ``system.properties``\ 에 저장됩니다.
이 차이는 뒤의 "중지와 재개"에서 중요해집니다.

.. warning::

   이 구성의 OpenSearch는 보안 플러그인이 비활성화된 상태로 호스트의 포트 9200에 공개됩니다.
   자신의 PC에서 시험해 보기 위한 구성으로 사용하고, 공유 서버에서 실행하는 경우에는 :doc:`guide-10`\ 과 :doc:`guide-15`\ 를 먼저 확인하십시오.

준비
====

- Docker와 Docker Compose(``docker compose`` 명령)를 사용할 수 있을 것
- Docker가 사용할 수 있는 메모리가 4GB 이상일 것(OpenSearch의 힙만으로 1GB를 확보합니다)
- 인터넷에 연결할 수 있을 것(이미지 가져오기와 크롤링에 사용합니다)

Linux 또는 WSL2에서는 OpenSearch 기동에 필요한 ``vm.max_map_count``\ 를 올립니다.

::

    $ sudo sysctl -w vm.max_map_count=262144

이 값은 OS를 재시작하면 원래대로 돌아갑니다.
계속 사용하는 경우에는 ``/etc/sysctl.conf``\ 에도 적어 둡니다.

::

    $ echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf

Fess 기동하기
=============

15.9.0용 Compose 파일 가져오기
------------------------------

docker-fess 기본 브랜치의 Compose 파일은 새 버전 릴리스에 맞춰 갱신됩니다.
버전을 15.9.0으로 고정하기 위해 ``v15.9.0`` 태그의 파일을 가져옵니다.

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

``compose.yaml``\ 에는 ``fess01``\ 만 정의되어 있고, ``fess01``\ 이 의존하는 ``search01``\ 은 ``compose-opensearch3.yaml``\ 에 있습니다.
따라서 이후의 ``docker compose`` 명령에는 매번 2개의 파일을 ``-f``\ 로 지정합니다.
한쪽만으로 실행하면 기동도 중지도 올바르게 되지 않습니다.

기동하고 준비될 때까지 기다리기
-------------------------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

처음에는 이미지를 가져와야 하므로 몇 분 걸립니다.
상태는 다음 명령으로 확인합니다.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

``search01``\ 이 healthy가 된 뒤에 ``fess01``\ 이 기동합니다.
``fess01``\ 의 STATUS가 ``(healthy)``\ 가 되면 준비 완료입니다.
``fess01``\ 의 헬스 체크는 ``/api/v2/health``\ 를 호출하며, 기동 직후 120초는 유예 기간으로 취급됩니다.

좀처럼 healthy가 되지 않을 때는 로그를 확인합니다.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

포트 8080을 다른 애플리케이션이 사용하고 있다면 ``compose.yaml``\ 의 ``ports``\ 를 ``"9080:8080"``\ 처럼 변경합니다.
그 밖의 기동 문제는 `설치 문제 해결 <https://fess.codelibs.org/ko/stable/install/troubleshooting.html>`__\ 을 참조하십시오.

브라우저에서 ``http://localhost:8080/``\ 을 열면 Fess의 검색 화면이 표시됩니다.
아직 아무것도 크롤링하지 않았으므로 이 시점에서는 검색해도 결과가 나오지 않습니다.

관리 화면에 로그인하기
======================

``http://localhost:8080/admin/``\ 을 열고 사용자 이름 ``admin``, 비밀번호 ``admin``\ 으로 로그인합니다.

초기 비밀번호 ``admin``\ 은 계속 사용할 수 없도록 설정되어 있으므로, 로그인하면 "비밀번호를 갱신해야 합니다"라는 화면으로 넘어갑니다.

1. "새 비밀번호"와 "새 비밀번호 확인"에 같은 비밀번호를 입력합니다(8자 이상)
2. [갱신]을 클릭합니다

갱신이 끝나면 관리 화면의 대시보드가 열립니다.
이후에는 새 비밀번호로 로그인합니다.
이 비밀번호는 OpenSearch에 저장되므로 컨테이너를 다시 만들어도 남습니다(볼륨까지 삭제한 경우에는 ``admin``\ 으로 돌아갑니다).

크롤링 설정 만들기
==================

대상 정하기
-----------

이번에는 Fess 공식 사이트의 한국어 "검색 가이드"를 크롤링합니다.
``https://fess.codelibs.org/ko/stable/user/`` 아래에 있는 20페이지 정도이며, ``stable``\ 은 현재 안정판(15.9)의 문서를 가리킵니다.

웹 크롤링 설정 등록하기
-----------------------

1. 관리 화면의 왼쪽 메뉴에서 [크롤러] > [웹]을 엽니다
2. [새로 만들기]를 클릭합니다
3. 다음 항목을 입력합니다. 다른 항목은 초깃값 그대로 둡니다

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - 항목
        - 값
      * - 이름
        - ``Fess 검색 가이드``
      * - URL
        - ``https://fess.codelibs.org/ko/stable/user/index.html``
      * - 크롤링할 URL
        - ``https://fess.codelibs.org/ko/stable/user/.*``
      * - 최대 접근 횟수
        - ``50``

4. [작성]을 클릭합니다

각 항목의 의미는 다음과 같습니다.

- "이름"은 필수입니다. 비어 있으면 작성할 수 없습니다
- "URL"은 크롤링의 시작점입니다
- "크롤링할 URL"은 정규 표현식이며, 이와 일치하지 않는 URL로의 링크는 따라가지 않습니다. 비워 두면 페이지 안의 링크를 다른 버전이나 다른 언어, 외부 사이트까지 따라가 버립니다
- "최대 접근 횟수"는 정규 표현식을 잘못 썼을 때를 대비한 상한입니다

초깃값 그대로 둔 항목 중 "스레드 수"는 ``1``, "간격"은 ``10000``\ 밀리초입니다.
페이지마다 10초씩 기다리므로 상대 사이트에 주는 부하를 줄일 수 있습니다.
"권한"에는 ``{role}guest``\ 가 들어 있으므로 로그인하지 않은 사용자도 검색 결과를 볼 수 있습니다.
부서별로 다르게 보여 주는 방법은 :doc:`guide-05`\ 에서 다룹니다.

.. note::

   ``/ko/15.9/``\ 와 같이 버전 번호가 붙은 URL을 대상으로 하면 페이지가 하나도 등록되지 않습니다.
   이 페이지들에는 ``/ko/stable/``\ 을 가리키는 ``<link rel="canonical">``\ 이 들어 있습니다.
   Fess의 크롤러는 그 페이지를 등록하지 않고, 대신 canonical URL을 따라갑니다.
   그 URL이 "크롤링할 URL"의 정규 표현식에서 벗어나므로 아무것도 등록되지 않습니다.
   자사 사이트를 대상으로 하는 경우에도 canonical URL이 정규 표현식에 포함되는지 확인하십시오.

.. tip::

   [시스템] > [마법사]에서도 "이름", "크롤링 경로", "최대 접근 횟수", "깊이"를 입력하기만 하면 크롤링 설정을 만들고, 그대로 [크롤링 시작]까지 진행할 수 있습니다.
   다만 마법사로 만든 설정에는 "크롤링할 URL"이 들어가지 않으므로 링크를 따라가는 범위를 좁힐 수 없습니다.
   이번처럼 대상을 좁히고 싶은 경우에는 위의 [크롤러] > [웹]에서 작성하십시오.

크롤링을 실행하고 완료 확인하기
===============================

크롤링 시작하기
---------------

설정을 저장하기만 해서는 크롤링이 시작되지 않습니다.

1. [시스템] > [스케줄러]를 엽니다
2. 목록의 "Default Crawler"를 클릭합니다
3. [지금 시작]을 클릭합니다

"Default Crawler"는 활성화된 웹·파일 시스템·데이터 스토어 크롤링 설정을 한꺼번에 실행하는 작업입니다.
이 작업에는 초기 상태로 cron 식 ``0 0 * * *``\ 가 설정되어 있어 하루에 한 번 자동으로도 실행됩니다.
컨테이너를 계속 실행해 두면 다음 날 이후에도 같은 설정으로 다시 크롤링됩니다.

이번 설정에서는 20페이지 정도를 10초 간격으로 가져오므로, 끝날 때까지 몇 분 정도 걸립니다.

끝났는지 확인하기
-----------------

다음 순서로 확인합니다.

1. [시스템 정보] > [작업 로그]를 엽니다. "Default Crawler" 행의 "상태"가 "실행 중"에서 "OK"로 바뀌면 작업이 끝난 것입니다. "실패"인 경우에는 그 행을 클릭해 상세를 열고 "결과"를 확인합니다
2. [시스템 정보] > [크롤링 정보]를 열고 목록의 맨 위(최신) 세션을 클릭합니다. "인덱스 크기 (웹/파일)"이 이번 크롤링으로 등록된 문서 수입니다. 이번에는 20 전후가 됩니다
3. 건수가 예상보다 적은 경우에는 [시스템 정보] > [장애 URL]을 엽니다. 연결 오류 등으로 가져오지 못한 URL과 그 이유가 기록되어 있습니다

작업이 "OK"여도 등록 건수가 0인 경우가 있습니다.
"크롤링할 URL"의 정규 표현식과 일치하지 않은 URL은 오류가 아니라 대상 외로 취급되므로 장애 URL에도 기록되지 않습니다.
건수가 0이고 장애 URL도 비어 있다면 URL과 정규 표현식의 작성 방법(``https``\ 와 ``http``\ 의 차이, 끝의 ``.*`` 유무 등)을 다시 확인하십시오.

검색해 보기
===========

``http://localhost:8080/``\ 을 열고 검색합니다.
검색 화면은 Fess에 포함된 테마 ``bootstrap``\ 입니다.

먼저 ``와일드카드``\ 를 입력하고 검색해 보십시오.
"와일드카드 검색" 페이지나 "특수 문자" 페이지가 결과에 표시됩니다.
결과의 제목을 클릭하면 원래 페이지(fess.codelibs.org)가 열립니다.

이어서 다음 검색어를 차례로 입력해 봅니다.
모두 방금 크롤링한 페이지로 결과를 확인할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 입력할 검색어
     - 의미
   * - ``필드 URL``
     - 공백으로 구분하면 AND 검색이 되어, 두 단어를 모두 포함하는 페이지만 나옵니다
   * - ``와일드카드 OR 유사``
     - 어느 한쪽을 포함하는 페이지가 나옵니다. ``OR``\ 는 반각 대문자로 쓰고, 앞뒤에 공백이 필요합니다
   * - ``검색 -라벨``
     - "라벨"을 포함하는 페이지를 결과에서 제외합니다. ``-``\ 는 제외할 단어 바로 앞에 붙입니다
   * - ``"범위 지정 검색"``
     - 따옴표로 묶은 어구를 그 순서 그대로 포함하는 페이지를 찾습니다(구문 검색)
   * - ``title:정렬``
     - 제목에 "정렬"을 포함하는 페이지만 찾습니다(필드 지정 검색)

``or``\ 나 ``and``\ 처럼 소문자로 쓰면 연산자가 되지 않고 일반 검색어로 취급됩니다.

여기서 사용한 구문과 와일드카드·유사 검색·범위 지정 등 나머지 구문은 방금 크롤링한 `검색 가이드 <https://fess.codelibs.org/ko/stable/user/index.html>`__\ 에 설명되어 있습니다.
궁금한 구문을 자신의 Fess에서 검색하고 그 페이지를 열어 읽는 식으로 활용할 수도 있습니다.

중지와 재개
===========

중지하는 방법에 따라 남는 것이 달라집니다.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 조작
     - 남는 것
     - 잃는 것
   * - ``stop`` → ``start``
     - 전부
     - 없음
   * - ``down`` → ``up -d``
     - OpenSearch에 저장된 것(인덱스, 크롤링 설정, 사용자와 비밀번호, 작업 로그 등)
     - ``fess01`` 컨테이너 내부에 저장된 것([시스템] > [일반]에서 변경한 설정 등)
   * - ``down -v``
     - 없음
     - 전부(관리자 비밀번호도 ``admin``\ 으로 돌아갑니다)

평소에 중지할 때는 ``stop``, 재개할 때는 ``start``\ 를 사용합니다.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

``down``\ 은 컨테이너를 삭제합니다.
OpenSearch의 데이터는 볼륨에 남지만, [일반]의 설정은 ``fess01`` 컨테이너 내부의 ``system.properties``\ 에 기록되어 있으므로 컨테이너와 함께 사라집니다.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

시험 사용을 마치고 데이터까지 포함해 정리할 때는 ``-v``\ 를 붙입니다.
볼륨도 삭제되며 되돌릴 수 없습니다.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

[일반]에서 변경한 설정 중 일부는 ``compose.yaml``\ 의 ``FESS_JAVA_OPTS``\ 로 지정해 두면 컨테이너를 다시 만들어도 남습니다(SSO 연결 설정처럼 이 방법으로는 지정할 수 없는 항목도 있습니다).
절차는 `Docker 설치 (상세) <https://fess.codelibs.org/ko/stable/install/install-docker.html>`__\ 를 참조하십시오.

다음에 읽을 글
==============

목적에 맞춰 다음 글로 넘어가십시오.

- Fess의 구성과 글 전체를 읽어 나가는 방법을 알고 싶다: :doc:`guide-01`
- 기존 사내 사이트나 포털에 검색창을 두고 싶다: :doc:`guide-03`
- 사내 웹 사이트와 파일 서버를 한꺼번에 검색하고 싶다: :doc:`guide-04`
- 부서나 직위에 따라 보이는 검색 결과를 바꾸고 싶다: :doc:`guide-05`
- Slack, Confluence, 데이터베이스 등의 데이터도 검색하고 싶다: 먼저 :doc:`datastore-basics`, 이어서 :doc:`guide-06`·:doc:`guide-07`·:doc:`guide-12`
- 생성형 AI가 사내 문서를 바탕으로 답하게 하고 싶다: :doc:`guide-19`
- 키워드가 일치하지 않아도 의미가 가까운 문서를 찾고 싶다: :doc:`guide-18`
- 모니터링과 백업을 갖추고 운영 환경에서 사용하고 싶다: :doc:`guide-10`
- SSO나 접근 보호를 설정하고 싶다: :doc:`guide-15`
- 문서 수나 사용자 증가에 맞춰 확장하고 싶다: :doc:`guide-14`

참고 자료
=========

- `Docker 설치 (상세) <https://fess.codelibs.org/ko/stable/install/install-docker.html>`__
- `docker-fess(GitHub) <https://github.com/codelibs/docker-fess>`__
- `웹 크롤링 설정 <https://fess.codelibs.org/ko/stable/admin/webconfig-guide.html>`__
- `작업 로그 <https://fess.codelibs.org/ko/stable/admin/joblog-guide.html>`__
- `검색 가이드 <https://fess.codelibs.org/ko/stable/user/index.html>`__
