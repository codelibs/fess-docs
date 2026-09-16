====================
fess-setup 명령
====================

``bin/fess-setup`` (Windows 에서는 ``bin\fess-setup.bat`` )은 |Fess| 의 ZIP 패키지에 포함되어 있습니다. |Fess| 에 필요하지만 배포물에 포함되지 않은 것, 즉 |Fess| 가 필요로 하는 플러그인을 넣은 OpenSearch, Playwright 크롤러가 사용하는 Node.js, |Fess| 플러그인을 설치합니다. 설치 상태를 진단할 수도 있습니다.

|Fess| 디렉터리에서 실행합니다. 인수 없이 실행하면 명령 목록을 표시합니다.

::

    $ cd /path/to/fess-15.9.0
    $ bin/fess-setup <command> [options]

종료 코드
==========

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 코드
     - 의미
   * - ``0``
     - 명령이 성공했습니다.
   * - ``1``
     - 명령이 실패했습니다. 예를 들어 다운로드에 실패한 경우, 지정한 버전이 존재하지 않는 경우, 이 플랫폼용 OpenSearch 배포판이 없는 경우, ``check`` 가 문제를 발견한 경우입니다.
   * - ``2``
     - 명령줄이 잘못되었습니다. 알 수 없는 명령을 지정했거나 플러그인 이름 등의 인수가 부족한 경우입니다.

OpenSearch 와 Node.js 설치
============================

install opensearch
------------------

::

    $ bin/fess-setup install opensearch [--dest <dir>] [--version <version>]

이 |Fess| 가 지원하는 버전의 OpenSearch 를 |Fess| 디렉터리의 ``opensearch/`` 에 다운로드하고, |Fess| 가 필요로 하는 4개의 플러그인( ``opensearch-analysis-fess`` , ``opensearch-analysis-extension`` , ``opensearch-minhash`` , ``opensearch-configsync`` )을 설치한 다음, 해당 OpenSearch 의 ``config/opensearch.yml`` 에 다음 설정을 추가합니다.

- ``configsync.config_path`` (값은 해당 OpenSearch 의 ``config/dictionary`` 디렉터리)
- ``plugins.security.disabled: true``

``opensearch.yml`` 에 이미 있는 설정은 다시 추가하지 않으며, ``plugins.security.*`` 설정이 하나라도 있으면 ``plugins.security.disabled: true`` 를 추가하지 않습니다. OpenSearch 디렉터리가 이미 있으면 다운로드를 건너뛰므로, 기존 설치에 대해 다시 실행하면 부족한 설정만 추가됩니다.

명령은 추가한 설정을 표시한 다음, ``bin/fess.in.sh`` 가 이 OpenSearch 를 자동으로 찾을 수 있는지 표시합니다. |Fess| 디렉터리의 ``opensearch/`` 아래에서 ``config/dictionary`` 디렉터리를 가진 OpenSearch 가 이것 하나뿐이면 찾을 수 있습니다. 이때 ``bin/fess.in.sh`` (Windows 에서는 ``bin\fess.in.bat`` )가 ``FESS_DICTIONARY_PATH`` 를 그 디렉터리로 설정하므로, 같은 호스트에서 실행하는 OpenSearch 라면 그 밖의 설정은 필요하지 않습니다. 찾을 수 없으면 설정해야 할 ``SEARCH_ENGINE_HTTP_URL`` 과 ``FESS_DICTIONARY_PATH`` 값을 표시합니다. 설정 방법은 :doc:`install-linux` 또는 :doc:`install-windows` 를 참조하십시오.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 옵션
     - 설명
   * - ``--dest <dir>``
     - OpenSearch 를 압축 해제할 디렉터리를 |Fess| 디렉터리의 ``opensearch/`` 대신 지정합니다. ``bin/fess.in.sh`` 는 이 디렉터리 밖에 있는 OpenSearch 를 찾지 않습니다.
   * - ``--version <version>``
     - 설치할 OpenSearch 버전입니다. 플러그인도 같은 버전으로 설치됩니다.

OpenSearch 공식 배포판은 Linux 용과 Windows 용뿐입니다. macOS 등 그 밖의 플랫폼에서는 아무것도 다운로드하지 않고 종료 코드 ``1`` 로 종료하며, Homebrew 로 OpenSearch 를 설치하고 ``install opensearch-plugins`` 로 플러그인을 넣는 방법 또는 Docker 를 사용하는 방법을 안내합니다.

.. warning::

   ``plugins.security.disabled: true`` 를 설정한 OpenSearch 는 인증 없이 요청을 받아들입니다. OpenSearch 는 ``network.host`` 를 설정하지 않는 한 루프백 주소에서만 수신 대기합니다. 그 밖의 주소에서 수신 대기하기 전에 대신 보안 플러그인을 설정하십시오. 자세한 내용은 :doc:`security` 를 참조하십시오.

install opensearch-plugins
--------------------------

::

    $ bin/fess-setup install opensearch-plugins --opensearch-home <dir> [--version <version>]

이미 있는 OpenSearch 에 |Fess| 가 필요로 하는 4개의 플러그인을 설치합니다. 해당 OpenSearch 의 ``bin/opensearch-plugin install`` 을 4번 실행하는 대신 사용할 수 있습니다. ``--opensearch-home`` 에는 OpenSearch 설치 디렉터리를 지정합니다(필수). ``--version`` 은 플러그인 버전이며, OpenSearch 버전과 일치시켜야 합니다.

이 명령은 ``opensearch.yml`` 을 변경하지 않습니다. ``configsync.config_path`` 등의 설정은 :doc:`install-linux` 또는 :doc:`install-windows` 에 따라 직접 추가하십시오.

install nodejs
--------------

::

    $ bin/fess-setup install nodejs [--dest <dir>] [--version <version>]

Playwright 크롤러가 필요로 하는 Node.js 를 |Fess| 디렉터리의 ``nodejs/`` 에 다운로드합니다. ``bin/fess.in.sh`` (Windows 에서는 ``bin\fess.in.bat`` )가 이를 찾아 ``PLAYWRIGHT_NODEJS_PATH`` 를 설정합니다. ``--dest`` 로 |Fess| 디렉터리 밖에 압축 해제한 경우에는 대신 ``bin/fess.in.sh`` 에 추가할 ``PLAYWRIGHT_NODEJS_PATH`` 줄을 표시합니다. ``--version`` 으로 다른 버전의 Node.js 를 지정할 수 있습니다. Playwright 크롤러에 대해서는 :doc:`../config/crawler-advanced` 를 참조하십시오.

플러그인 관리
================

다음 명령은 |Fess| 설치의 플러그인 디렉터리 ``app/WEB-INF/plugin`` 을 대상으로 합니다. 플러그인을 설치, 업그레이드, 삭제한 후에는 |Fess| 를 재시작하십시오. 플러그인은 관리 화면의 「시스템 > 플러그인」 페이지에서도 관리할 수 있습니다. :doc:`../admin/plugin-guide` 를 참조하십시오.

``install plugin`` , ``list plugins`` , ``upgrade plugins`` 에는 ``--repository <url>`` 을 지정할 수 있습니다. 지정하면 버전 목록, jar, 체크섬을 모두 그 하나의 Maven 저장소(사내 미러 등)에서 가져오며, 기본 릴리스 저장소, 스냅숏 저장소, GitHub 은 사용하지 않습니다.

install plugin
--------------

::

    $ bin/fess-setup install plugin <name>[:<version>]... [--version <version>] [--repository <url>]

``fess-script-groovy`` 나 ``fess-ds-git`` 등 |Fess| 플러그인을 하나 이상 설치합니다. 버전을 붙이지 않은 이름에는 이 |Fess| 용으로 빌드된 최신 버전이 설치됩니다. ``<name>:<version>`` 으로 해당 플러그인의 버전을 고정할 수 있으며, ``--version`` 은 자체 버전이 없는 모든 이름에 사용됩니다. 새 버전의 설치가 완료된 후에 같은 플러그인의 이전 버전이 삭제됩니다.

jar 는 플러그인의 GitHub 릴리스에서 가져오며, 릴리스에 해당 파일이 없으면 Maven 저장소에서 가져옵니다. 어느 경우든 Maven 저장소가 공개하는 SHA-1 체크섬으로 검증합니다. |Fess| 의 개발 빌드에서는 같은 계열의 스냅숏 빌드도 설치 대상이 되며, 스냅숏이 우선됩니다.

사용 예는 :doc:`../admin/plugin-guide` 를 참조하십시오.

list plugins
------------

::

    $ bin/fess-setup list plugins [--repository <url>]

이 |Fess| 용으로 공개된 플러그인 목록을 표시하고, 설치된 플러그인에는 ``(installed: <version>)`` 을 붙입니다. 설치되어 있지만 저장소에 공개되지 않은 플러그인(로컬에서 빌드한 jar 등)은 따로 표시합니다. |Fess| 의 개발 빌드에서는 스냅숏 저장소도 참조합니다.

list installed
--------------

::

    $ bin/fess-setup list installed

설치된 플러그인과 그 버전을 저장소에 조회하지 않고 표시합니다.

upgrade plugins
---------------

::

    $ bin/fess-setup upgrade plugins [--repository <url>]

설치된 모든 플러그인을 이 |Fess| 에 맞는 버전으로 다시 설치합니다. 이미 그 버전인 플러그인은 그대로 둡니다. ``app/WEB-INF/plugin`` 의 플러그인은 특정 |Fess| 릴리스용으로 빌드되므로, |Fess| 를 업그레이드한 후에 이 명령을 실행하십시오.

remove plugin
-------------

::

    $ bin/fess-setup remove plugin <name>...

지정한 플러그인의 설치된 jar 를 삭제합니다. 설치되지 않은 이름은 그 사실을 표시할 뿐이며, 종료 코드에는 영향을 주지 않습니다.

설치 상태 확인
================

list
----

::

    $ bin/fess-setup list

``install`` 이 다운로드하는 구성 요소( ``opensearch`` 와 ``nodejs`` )를 각각의 버전과 함께 표시합니다.

check
-----

::

    $ bin/fess-setup check [--url <engine url>] [--playwright]

설치 상태를 진단하고, 확인 항목마다 ``OK`` , ``WARN`` , ``FAIL`` 중 하나를 붙여 한 줄씩 표시합니다.

- 검색 엔진: 접속할 수 있는지, 버전(노드 간에 버전이 다르면 경고), |Fess| 가 필요로 하는 4개의 플러그인이 설치되어 있는지, ``configsync`` 가 응답하는지
- |Fess| : 플러그인 디렉터리가 존재하고 쓰기 가능한지, 설치된 각 플러그인(다른 |Fess| 릴리스용이거나 두 버전이 설치되어 있으면 실패), |Fess| 디렉터리의 ``nodejs/`` 에 Node.js 가 설치되어 있는지

검색 엔진 URL 은 ``--url`` , 지정하지 않으면 환경 변수 ``SEARCH_ENGINE_HTTP_URL`` , 그것도 없으면 ``http://localhost:9200`` 입니다. ``bin/fess-setup`` 은 ``bin/fess.in.sh`` 를 읽지 않으므로, OpenSearch 가 다른 곳에 있으면 ``--url`` 을 지정하십시오. Node.js 가 없는 것은 보고만 되지만, ``--playwright`` 를 지정하면 실패로 처리됩니다.

실패한 항목이 없으면 경고가 있더라도 종료 코드 ``0`` 으로 종료하고, 실패한 항목이 있으면 종료 코드 ``1`` 로 종료합니다.
