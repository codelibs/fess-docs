===================================================
Fess 설정을 코드로 관리하고 같은 환경을 다시 만들기
===================================================

들어가며
========

관리 화면에서 쌓아 온 설정은 누가 언제 무엇을 바꿨는지 나중에 추적할 수 없습니다.
검증 환경에서 확인한 설정을 운영 환경으로 옮길 때도 같은 화면 조작을 손으로 반복하게 됩니다.

이 글에서는 Fess 15.9의 설정을 Git 리포지토리의 파일로 작성하고, 새로 시작한 Docker 환경에 스크립트로 적용한 뒤, 적용되었는지 확인하는 데까지 진행합니다.
사용하는 것은 docker-fess의 Compose 파일, Fess의 관리 API(Admin API), 그리고 그 CLI인 fessctl입니다.

백업 대상 범위와 복원 절차는 다루지 않습니다.
:doc:`guide-10`\ 을 참조하세요.

설정이 저장되는 위치별로 관리 방법 정하기
=========================================

Fess의 설정은 한곳에 모여 있지 않습니다.
저장되는 위치에 따라 코드로 만드는 방법이 달라집니다.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 설정
     - 저장 위치
     - 코드로 만드는 방법
   * - Fess 버전, 플러그인
     - Docker 이미지, 컨테이너
     - Compose 파일의 이미지 태그와 ``FESS_PLUGINS``
   * - ``fess_config.properties``\ 의 항목(``app.cipher.key`` 등)
     - 컨테이너 안의 파일
     - ``FESS_JAVA_OPTS``\ 의 ``-Dfess.config.<키>``
   * - [시스템] > [일반]의 항목
     - 컨테이너 안의 ``system.properties``
     - ``FESS_JAVA_OPTS``\ 의 ``-Dfess.system.<키>``
   * - 크롤 설정, 라벨, 스케줄러, 사용자 등
     - OpenSearch의 설정용 인덱스
     - 관리 API(fessctl)
   * - 사전(동의어 등)
     - OpenSearch 컨테이너의 ``FESS_DICTIONARY_PATH``
     - 관리 API의 사전 업로드(fessctl)
   * - 액세스 토큰, 암호화 키의 값
     - 토큰은 OpenSearch, 암호화 키는 시작 옵션
     - Git에 넣지 않고 ``.env``\ 나 CI의 시크릿에 둔다

docker-fess의 ``fess01`` 컨테이너에는 볼륨이 없으므로, ``system.properties``\ 는 ``docker compose down``\ 으로 컨테이너와 함께 사라집니다.
OpenSearch에 저장되는 크롤 설정 등은 볼륨에 남습니다.

리포지토리 구성
===============

이 글에서는 다음 파일을 Git으로 관리합니다.

::

    fess-infra/
    ├── compose.yaml               docker-fess v15.9.0의 파일
    ├── compose-opensearch3.yaml   docker-fess v15.9.0의 파일
    ├── compose-site.yaml          자신의 환경에 맞춘 차이
    ├── dict/
    │   └── synonym.txt            동의어 사전
    ├── apply.sh                   설정을 적용하는 스크립트
    ├── .gitignore
    └── .env                       Git에 넣지 않음(암호화 키와 토큰)

Docker 구성을 버전까지 고정하기
===============================

Compose 파일 가져오기
---------------------

docker-fess의 ``v15.9.0`` 태그의 파일을 가져옵니다.
``compose.yaml``\ 은 이미지 ``ghcr.io/codelibs/fess:15.9.0``\ 을, ``compose-opensearch3.yaml``\ 은 ``ghcr.io/codelibs/fess-opensearch:3.9.0``\ 을 가리키므로 버전이 고정됩니다.

::

    $ mkdir fess-infra && cd fess-infra
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

이 두 파일은 편집하지 않고, 자신의 환경에 맞춘 차이는 별도 파일에 작성합니다.
docker-fess 버전을 올릴 때 파일을 다시 가져오기만 하면 됩니다.

자신의 환경에 맞춘 차이 작성하기
--------------------------------

``compose-site.yaml``\ 을 만듭니다.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-ds-git:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.app.cipher.key=${FESS_CIPHER_KEY:?FESS_CIPHER_KEY is not set} -Dfess.system.purge.searchlog.day=180"

- ``FESS_PLUGINS``\ 에는 시작할 때 가져올 플러그인을 ``이름:버전`` 형식으로 공백으로 구분해 적습니다. 버전은 Fess와 같은 15.9.x로 합니다. 예의 ``fess-ds-git``\ 은 Git 리포지토리를 데이터 저장소로 크롤링할 때 쓰는 플러그인입니다. 가져오는 곳이 ``maven.codelibs.org``\ 로 고정되어 있으므로 여기에 적을 수 있는 것은 공개된 플러그인뿐이며, 컨테이너에서 인터넷에 접속할 수 있어야 합니다
- ``-Dfess.config.<키>``\ 는 ``fess_config.properties``\ 의 같은 이름 항목보다 우선합니다
- ``-Dfess.system.<키>``\ 는 [일반] 항목의 기본값이 됩니다. 예의 ``purge.searchlog.day``\ 는 [일반]의 "이전 검색 로그 삭제" 일수입니다

Compose는 ``environment``\ 를 변수 이름별로 병합하므로, ``compose.yaml``\ 에 있는 ``SEARCH_ENGINE_HTTP_URL`` 등은 그대로 남습니다.
다만 같은 변수를 여러 파일에 적으면 뒤에 오는 파일의 값으로 바뀝니다.
``compose-openai.yaml`` 같은 오버레이도 ``FESS_PLUGINS``\ 와 ``FESS_JAVA_OPTS``\ 를 설정하므로, 함께 사용할 때는 값을 하나의 파일로 합치세요.

.. note::

   ``-Dfess.system.<키>``\ 는 ``system.properties``\ 에 그 키가 없을 때만 사용됩니다.
   관리 화면의 [일반]에서 한 번이라도 저장하거나 ``fessctl general update``\ 를 실행하면 화면의 각 항목이 ``system.properties``\ 에 기록되고, 이후에는 그쪽이 우선합니다.
   이 상태에서 ``compose-site.yaml``\ 의 값을 바꿔도 ``down``\ 으로 컨테이너를 다시 만들 때까지 반영되지 않습니다.

암호화 키 정하기
----------------

``app.cipher.key``\ 는 웹 인증·파일 인증의 비밀번호와, 크롤 설정·데이터 저장소 설정의 파라미터에 저장한 비밀 값을 암호화하는 키입니다.
기본값 ``___change__me___`` 그대로 사용하지 말고, 처음 시작하기 전에 정합니다.

키 문자열은 그대로 AES 키로 사용되므로 16·24·32바이트 중 하나로 합니다.
``openssl rand -hex 16``\ 의 출력(16진수 32자)이라면 32바이트가 됩니다.

::

    $ printf 'FESS_CIPHER_KEY=%s\n' "$(openssl rand -hex 16)" > .env
    $ printf '.env\nbackup/\n' > .gitignore

인증 정보를 저장한 뒤에 키를 바꾸면 저장된 값을 복호화할 수 없어, 그 설정을 사용하는 크롤링이 실패합니다.
백업을 다른 환경에 복원할 때도 같은 키가 필요합니다(:doc:`guide-10`).
``.env``\ 와는 별도로 비밀번호 관리 도구 등에도 기록해 둡니다.

``FESS_JAVA_OPTS``\ 의 값은 ``docker inspect``\ 로 볼 수 있습니다.
이를 피하고 싶다면 ``fess_config.properties``\ 를 ``/opt/fess``\ 에 마운트하는 방법을 사용합니다(`Docker 설치 (상세) <https://fess.codelibs.org/ko/stable/install/install-docker.html>`__\ 의 "설정 파일 반영 방법").

시작하기
--------

Compose 명령에는 매번 세 파일을 지정합니다.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-site.yaml up -d

``fess01``\ 의 헬스 체크는 ``/api/v2/health``\ 를 호출하며, ``docker compose ... ps``\ 에서 ``fess01``\ 이 ``(healthy)``\ 가 되면 준비가 끝난 것입니다.

관리 API용 액세스 토큰 만들기
=============================

관리 API를 호출하려면 액세스 토큰이 필요하며, 토큰을 만드는 API도 토큰 없이는 호출할 수 없습니다.
그래서 새 환경마다 처음 한 번만 관리 화면에서 만듭니다.

1. ``http://localhost:8080/admin/``\ 에 ``admin`` / ``admin``\ 으로 로그인하고, 요구되는 새 비밀번호(8자 이상)를 설정합니다
2. [시스템] > [액세스 토큰]을 열고 [새로 만들기]를 클릭합니다
3. "이름"에 ``fess-infra``, "권한"에 ``{role}admin-api``\ 를 입력하고 [작성]을 클릭합니다
4. 목록에서 만든 토큰을 열고 "토큰"의 값을 복사합니다

복사한 값을 ``.env``\ 에 추가합니다.

::

    $ echo 'FESS_ACCESS_TOKEN=<복사한 값>' >> .env

``{role}admin-api``\ 를 가진 토큰은 관리 API의 모든 작업을 할 수 있습니다.
설정 변경, 사용자 생성, 백업 다운로드까지 포함되며, 용도를 좁힌 토큰은 만들 수 없습니다.
관리자 비밀번호와 똑같이 다루고, Git이나 브라우저에서 동작하는 JavaScript에는 넣지 마세요.

fessctl 준비하기
================

fessctl은 관리 API를 호출하는 명령줄 도구입니다.
Fess 15.9용 기본값을 가진 0.4.0을 버전을 고정해 설치합니다.
Python 3.13 이상이 필요합니다.

::

    $ pipx install fessctl==0.4.0

``uv tool install fessctl==0.4.0``\ 을 사용해도 됩니다.
이후 스크립트에서는 응답에서 값을 꺼내기 위해 ``jq``\ 와 ``curl``\ 도 사용합니다.

fessctl은 접속 대상을 ``FESS_ENDPOINT``\ (기본값 ``http://localhost:8080``)에서, 토큰을 ``FESS_ACCESS_TOKEN``\ 에서, 접속 대상 Fess의 버전을 ``FESS_VERSION``\ 에서 읽습니다.
``FESS_VERSION``\ 에는 ``15.9.0``\ 을 지정합니다.
버전에 따라 API 호출 방식이 달라지기 때문입니다.

접속을 확인합니다.

::

    $ set -a; . ./.env; set +a
    $ export FESS_VERSION=15.9.0
    $ fessctl ping
    $ fessctl webconfig list

``ping``\ 은 클러스터 상태가 GREEN 또는 YELLOW이면 종료 코드 0으로 끝납니다.
헬스 체크는 토큰 없이도 통과하므로, 토큰이 유효한지는 ``webconfig list``\ 로 확인합니다.
인증 오류가 나면 토큰 값과 권한을 다시 확인하세요.
모든 명령은 ``-o json``\ 을 붙이면 관리 API의 응답을 그대로 출력하므로 ``jq``\ 로 값을 꺼낼 수 있습니다.

사전의 초기 내용을 Git에 넣기
-----------------------------

사전 업로드는 파일 전체를 교체합니다.
기본 내용을 지우지 않도록, 먼저 현재 동의어 사전을 다운로드해 리포지토리에 넣고 그것을 편집합니다.

::

    $ mkdir -p dict
    $ SYNONYM_ID=$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')
    $ fessctl dict synonym download "$SYNONYM_ID" --file dict/synonym.txt

다운로드한 파일에는 기본 동의어 ``fess,フエス``\ 가 이미 들어 있습니다.
그 끝에 동의어를 한 줄 추가합니다.
쉼표로 구분한 단어는 어느 것으로 검색해도 다른 단어를 포함하는 문서가 검색됩니다(형식은 `동의어 사전 <https://fess.codelibs.org/ko/stable/admin/synonym-guide.html>`__\ 을 참조).

::

    fess,페스

일본어 단어를 등록할 때는 히라가나는 가타카나로, 작은 가타카나는 큰 가타카나로("フェス"는 "フエス"), 전각 영숫자는 반각 영숫자로 바꿔 등록합니다.

설정을 적용하는 스크립트
========================

``apply.sh``\ 에는 환경에 넣고 싶은 설정을 fessctl 명령으로 작성합니다.
새 환경에 대해 실행하는 것을 전제로 하지만, 같은 이름의 설정이 있으면 생성을 건너뛰므로 다시 실행해도 중복되지 않습니다.

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail
    cd "$(dirname "$0")"
    if [ -f .env ]; then set -a; . ./.env; set +a; fi
    export FESS_ENDPOINT="${FESS_ENDPOINT:-http://localhost:8080}"
    export FESS_VERSION=15.9.0

    until curl -fsS "$FESS_ENDPOINT/api/v2/health" > /dev/null; do sleep 10; done
    fessctl ping

    # 라벨: 대상 경로와 일치하는 문서에 크롤링할 때 붙는다
    if ! fessctl labeltype list -o json | jq -e '.response.settings[] | select(.value == "fess_docs")' > /dev/null; then
      fessctl labeltype create --name "Fess 문서" --value fess_docs --version-no 1 \
        --included-path 'https://fess\.codelibs\.org/ko/stable/.*' \
        --permission '{role}guest'
    fi

    # 웹 크롤 설정
    if ! fessctl webconfig list -o json | jq -e '.response.settings[] | select(.name == "Fess 검색 가이드")' > /dev/null; then
      fessctl webconfig create --name "Fess 검색 가이드" \
        --url https://fess.codelibs.org/ko/stable/user/index.html \
        --included-url 'https://fess\.codelibs\.org/ko/stable/user/.*' \
        --depth 2 --max-access-count 50 \
        --permission '{role}guest'
    fi

    # 동의어 사전: 파일 전체를 교체하고, 문서 인덱스를 다시 열어 읽어 들이게 한다
    SYNONYM_ID=$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')
    fessctl dict synonym upload "$SYNONYM_ID" dict/synonym.txt --yes
    curl -fsS -X POST "localhost:9200/_configsync/flush" > /dev/null
    curl -fsS -X POST "localhost:9200/fess.update/_close" > /dev/null
    curl -fsS -X POST "localhost:9200/fess.update/_open" > /dev/null

    # 크롤링을 시작하고 작업이 끝나기를 기다린다
    SCHEDULER_ID=$(fessctl scheduler list -o json | jq -er '.response.settings[] | select(.name == "Default Crawler") | .id')
    JOBLOG_ID=$(fessctl scheduler start "$SCHEDULER_ID" -o json | jq -er '.response.job_log_id')
    until fessctl joblog get "$JOBLOG_ID" -o json \
        | jq -e '.response.log.job_status == "ok" or .response.log.job_status == "fail"' > /dev/null; do
      sleep 30
    done
    fessctl joblog get "$JOBLOG_ID" -o json | jq -e '.response.log.job_status == "ok"'

스크립트의 요점은 다음과 같습니다.

- fessctl은 기본 텍스트 출력에서는 API가 오류를 반환하면 0이 아닌 종료 코드로 끝나므로 ``set -e``\ 로 도중에 멈춥니다. ``-o json``\ 에서는 많은 명령이 오류 응답을 출력하고 0으로 끝나므로, 꺼낸 값을 ``jq -e``\ 로 확인합니다. 값이 없으면 jq가 실패하고 거기서 멈춥니다
- ``labeltype create``\ 의 ``--version-no``\ 는 fessctl 0.4.0에서는 필수입니다. 새로 만들 때는 ``1``\ 을 지정합니다
- ``webconfig create``\ 에서 생략한 항목은 fessctl의 기본값이 됩니다. ``--depth``\ 는 ``1``, ``--max-access-count``\ 는 ``1000000``\ 이므로 의도한 값은 생략하지 말고 적습니다. ``--permission``\ 의 기본값은 ``{role}guest``\ 입니다
- 라벨 값에는 영숫자와 ``_``\ 만 쓸 수 있습니다. 라벨은 크롤링할 때 붙으므로 크롤 설정보다 먼저 만듭니다
- 사전 업로드는 ``--yes``\ 를 붙이지 않으면 확인을 요구하며 멈춥니다
- 동의어 사전은 검색할 때 적용되지만, OpenSearch가 애널라이저를 만드는 것은 인덱스를 열 때뿐입니다. 그래서 ``_configsync/flush``\ 로 사전을 파일에 기록한 다음 ``fess.update``\ 를 close / open 합니다. 이 동안에는 검색할 수 없으므로, 운영 중인 환경에서는 접속이 적은 시간에 실행합니다. 관리 화면의 [시스템 정보] > [유지보수]에 있는 "문서 인덱스 다시 로드"와 같은 작업입니다
- ``scheduler start`` 응답의 ``job_log_id``\ 가 그대로 [작업 로그]의 ID가 됩니다. 작업 상태가 ``ok`` 또는 ``fail``\ 이 될 때까지 기다리고, ``ok``\ 가 아니면 실패로 끝납니다. "Default Crawler"는 활성화된 크롤 설정을 모두 실행합니다

이미 있는 설정의 값을 바꿀 때 이 스크립트는 생성을 건너뛸 뿐이며 값을 덮어쓰지 않습니다.
``fessctl webconfig update <ID> --max-access-count 100``\ 처럼 ID를 지정해 업데이트하거나, 볼륨째 다시 만든 환경에 다시 실행합니다.

스크립트를 CI에서 실행할 때는 ``.env``\ 를 두지 않고, CI의 시크릿에서 ``FESS_ACCESS_TOKEN``\ 과 ``FESS_ENDPOINT``\ 를 환경 변수로 전달합니다.
이 경우 ``localhost:9200``\ 이 들어간 세 줄은 OpenSearch에 닿는 주소로 바꿔 주세요.

적용되었는지 확인하기
=====================

``apply.sh``\ 가 종료 코드 0으로 끝나면 다음 순서로 확인합니다.

1. 플러그인이 설치되어 있는지

   ::

       $ fessctl plugin installed

   ``fess-ds-git``\ 의 15.9.0이 목록에 있으면 설치된 것입니다.
   ``FESS_PLUGINS``\ 의 플러그인은 가져오기에 실패해도 Fess 시작이 멈추지 않고 ``docker compose ... logs fess01``\ 에 ``Failed to download``\ 가 나올 뿐이므로, 여기서 확인합니다.

2. [일반]의 값이 반영되었는지

   ::

       $ fessctl general get -o json | jq '.response.setting.purge_search_log_day'

   ``180``\ 이 반환되면 ``-Dfess.system.purge.searchlog.day``\ 가 적용된 것입니다.
   관리 API에서의 이름은 ``purge_search_log_day`` 같은 snake_case로, ``-Dfess.system.`` 뒤에 오는 키와는 다릅니다.

3. 사전이 교체되었는지

   ::

       $ fessctl dict synonym download "$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')" | grep '페스'

   추가한 줄이 표시되면 업로드된 것입니다.
   ``fessctl dict synonym list``\ 로도 확인할 수 있지만 기본적으로 100건씩 표시되므로, 끝에 추가한 줄은 첫 페이지에 나오지 않을 수 있습니다.

4. 라벨을 지정해 검색할 수 있는지

   ::

       $ curl -fsS --get --data-urlencode 'q=검색' --data-urlencode 'fields.label=fess_docs' \
           http://localhost:8080/api/v2/search | jq '.response.record_count'

   1 이상이 반환되면 크롤링, 라벨 부여, 검색까지 이어진 것입니다.
   0인 경우에는 관리 화면의 [시스템 정보] > [장애 URL]과 [작업 로그]의 결과를 확인합니다.

관리 API를 직접 호출하기
========================

fessctl이 호출하는 것은 ``/api/admin/``\ 의 관리 API입니다.
크롤 설정처럼 설정을 가진 리소스는 모두 다음 형태입니다(``<resource>``\ 는 ``webconfig``, ``fileconfig``, ``dataconfig``, ``labeltype``, ``keymatch`` 등).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 요청
     - 작업
   * - ``GET /api/admin/<resource>/settings``
     - 목록
   * - ``GET /api/admin/<resource>/setting/<ID>``
     - 1건 조회
   * - ``POST /api/admin/<resource>/setting``
     - 생성
   * - ``PUT /api/admin/<resource>/setting``
     - 업데이트
   * - ``DELETE /api/admin/<resource>/setting/<ID>``
     - 삭제

fessctl에도 같은 이름의 하위 명령(``create``, ``list``, ``get``, ``update``, ``delete``)이 있으며, ``fessctl fileconfig create --help``\ 처럼 항목을 확인할 수 있습니다.
사전 업로드는 ``POST /api/admin/dict/<종류>/upload/<사전ID>``\ 에 multipart로 보냅니다.
파일 항목 이름은 종류마다 다르며, 동의어는 ``synonymFile``\ 입니다.
JSON 항목 이름은 ``max_access_count`` 같은 snake_case입니다.
각 항목은 `Admin API 개요 <https://fess.codelibs.org/ko/stable/api/admin/api-admin-overview.html>`__\ 에서 따라갈 수 있는 리소스별 페이지를 참조하세요.

다음 명령은 웹 크롤 설정의 건수를 반환합니다.

::

    $ curl -fsS -H "Authorization: Bearer $FESS_ACCESS_TOKEN" \
        http://localhost:8080/api/admin/webconfig/settings | jq '.response.total'

``-f``\ 를 붙이지 않으면 404나 401 응답에도 curl이 성공으로 처리하여, 스크립트가 실패를 알아차리지 못합니다.

설정 사본 받아 두기
===================

Git에 적지 않은 설정(관리 화면에서 직접 바꾼 것 등)에 대비해 백업도 정기적으로 받아 둡니다.
대상 파일과 복원 절차는 :doc:`guide-10`\ 에서 설명합니다.
여기서는 ``apply.sh``\ 와 같은 준비로 동작하는 스크립트 예만 보여 줍니다.

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail
    cd "$(dirname "$0")"
    if [ -f .env ]; then set -a; . ./.env; set +a; fi
    export FESS_VERSION=15.9.0
    dest="backup/$(date +%Y%m%d)"
    umask 077
    mkdir -p "$dest"
    for id in fess_basic_config.bulk fess_config.bulk fess_user.bulk system.properties fess.json doc.json; do
      fessctl backup download "$id" --dest "$dest/$id" --force
    done

``fessctl backup download``\ 는 ID에 점이 들어 있을 때 필요한 URL 끝의 ``/``\ 를 붙여 ``/api/admin/backup/file/<ID>/``\ 를 호출합니다.
curl로 호출할 때는 끝의 ``/``\ 와 ``-f``\ 를 잊지 마세요.
끝의 ``/``\ 가 없으면 404가 됩니다.

관리 API로 할 수 있는 것은 다운로드까지이며, 복원은 관리 화면의 [시스템 정보] > [백업]에서만 할 수 있습니다.
백업으로 다른 환경을 다시 만드는 절차가 되지는 않으므로, 설정의 원본은 ``apply.sh`` 쪽에 둡니다.

Git에 넣으면 안 되는 것
=======================

- ``.env``\ (암호화 키와 액세스 토큰)
- 백업 파일. ``*.bulk``\ 에는 암호화되지 않은 값도 들어 있어 기밀 파일로 다뤄야 합니다. ``system.properties``\ 에도 [일반]에서 입력한 스토리지 비밀 키나 SSO 클라이언트 시크릿 등이 들어갑니다

``.gitignore``\ 에 ``.env``\ 와 ``backup/``\ 를 넣은 것은 이 때문입니다.
백업은 암호화된 스토리지처럼 접근을 제한한 곳에 보관합니다.

다음에 읽을 글
==============

- 백업 대상과 복원, 모니터링을 갖추고 싶다: :doc:`guide-10`
- Docker에서의 시작과 중지의 기본을 확인하고 싶다: :doc:`guide-02`
- 업무 시스템에서 검색 API를 호출하고 싶다: :doc:`guide-11`
- 액세스 토큰 취급이나 SSO를 포함해 관리 화면을 보호하고 싶다: :doc:`guide-15`
- 직접 플러그인을 만들고 싶다: :doc:`guide-17`

참고 자료
=========

- `Docker 설치 (상세) <https://fess.codelibs.org/ko/stable/install/install-docker.html>`__
- `Admin API 개요 <https://fess.codelibs.org/ko/stable/api/admin/api-admin-overview.html>`__
- `Dict API <https://fess.codelibs.org/ko/stable/api/admin/api-admin-dict.html>`__
- `Backup API <https://fess.codelibs.org/ko/stable/api/admin/api-admin-backup.html>`__
- `사전 (반영 시점) <https://fess.codelibs.org/ko/stable/admin/dict-guide.html>`__
- `액세스 토큰 <https://fess.codelibs.org/ko/stable/admin/accesstoken-guide.html>`__
- `fessctl (GitHub) <https://github.com/codelibs/fessctl>`__
- `docker-fess (GitHub) <https://github.com/codelibs/docker-fess>`__
