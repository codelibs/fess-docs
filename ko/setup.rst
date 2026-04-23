================
설치 절차
================

설치 방법
================

Fess에서는 ZIP 아카이브, RPM/DEB 패키지, Docker 이미지 배포물을 제공합니다.
Docker를 이용하면 Windows나 Mac 등에서도 Fess를 간단히 설정할 수 있습니다.

.. note::

   이 페이지는 **Windows에서 Docker를 사용한 설치 절차**를 설명합니다. Linux나 macOS 사용자도 비슷한 절차로 설치할 수 있지만, Docker Desktop 설치 방법은 플랫폼에 따라 다릅니다.
   자세한 내용은 `Docker <https://docs.docker.com/get-docker/>`_ 문서를 참조하세요.

운용 환경을 구축하는 경우 반드시 :doc:`15.6/install/index` 를 참조하세요.
시스템 요구 사항은 :doc:`15.6/install/prerequisites` 를 확인하세요.

.. warning::

   **프로덕션 환경에서의 중요한 주의사항**

   프로덕션 환경이나 부하 검증 등에서는 내장 OpenSearch 가동은 권장하지 않습니다.
   반드시 외부 OpenSearch 서버를 구축하세요.

설정 개요
----------

다음 순서로 작업을 진행합니다:

1. Docker Desktop 설치
2. OS 설정 (vm.max_map_count 조정)
3. Fess 시작 파일 다운로드
4. Fess 시작 및 동작 확인

Docker Desktop 설치
============================

Docker Desktop이 설치되어 있지 않은 경우 다음 절차로 설치하세요.

다운로드
------------

`Docker Desktop <https://www.docker.com/products/docker-desktop/>`__ 에서 해당 OS의 설치 프로그램을 다운로드합니다.

설치 프로그램 실행
--------------------

다운로드한 설치 프로그램을 더블클릭하여 설치를 시작합니다.

"Install required Windows components for WSL 2" 또는
"Install required Enable Hyper-V Windows Features"가 선택되어 있는지 확인하고
OK 버튼을 클릭합니다.

|image0|

설치가 완료되면 "close" 버튼을 클릭하여 화면을 닫습니다.

|image1|

Docker Desktop 시작
---------------------

Windows 메뉴 내의 "Docker Desktop"을 클릭하여 시작합니다.

|image2|

Docker Desktop 시작 후 이용 약관이 표시되므로 "I accept the terms"에 체크하고 "Accept" 버튼을 클릭합니다.

튜토리얼 시작 안내가 나오지만 여기서는 "Skip tutorial"을 클릭하여 건너뜁니다.
"Skip tutorial"을 클릭하면 Dashboard가 표시됩니다.

|image3|

설정
====

OpenSearch가 Docker 컨테이너로 실행될 수 있도록 OS 측에서 "vm.max_map_count" 값을 조정합니다.
이용하는 환경에 따라 설정 방법이 다르므로 각 설정 방법은 "`Set vm.max_map_count to at least 262144 <https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#_set_vm_max_map_count_to_at_least_262144>`_ "를 참조하세요.

Fess 설정
==================

시작 파일 작성
------------------

적당한 폴더를 만들어 `compose.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml>`_ 과 `compose-opensearch3.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml>`_ 을 다운로드합니다.

.. note::

   ``compose-opensearch3.yaml`` 은 OpenSearch 3.x를 사용하기 위한 추가 설정 파일입니다.
   ``compose.yaml`` 과 조합하여 사용합니다.

curl 명령으로 다음과 같이 취득할 수도 있습니다:

.. code-block:: bash

    curl -o compose.yaml https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -o compose-opensearch3.yaml https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml

Fess 시작
----------

Fess를 docker compose 명령으로 시작합니다.

명령 프롬프트를 열고 compose.yaml 파일이 있는 폴더로 이동하여 다음 명령을 실행합니다:

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   시작에는 수 분이 걸릴 수 있습니다.
   다음 명령으로 로그를 확인할 수 있습니다:

   .. code-block:: bash

       docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

   ``Ctrl+C`` 로 로그 표시를 종료할 수 있습니다.


동작 확인
========

.. note::

   시작이 완료되면 브라우저에서 다음 URL에 접속하여 동작을 확인하세요:

   - **검색 화면:** http://localhost:8080/
   - **관리 UI:** http://localhost:8080/admin/

기본 관리자 계정의 사용자명/비밀번호는 admin/admin입니다.

.. warning::

   **보안에 관한 중요한 주의**

   기본 비밀번호는 반드시 변경하세요.
   특히 프로덕션 환경에서는 첫 로그인 후 즉시 비밀번호를 변경할 것을 강력히 권장합니다.

관리자 계정은 애플리케이션 서버에 의해 관리됩니다.
Fess의 관리 UI에서는 애플리케이션 서버에서 fess 역할로 인증된 사용자를 관리자로 판단합니다.

기타
======

Fess 정지
----------

Fess 정지는 Fess를 시작한 폴더에서 다음 명령을 실행합니다:

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml stop

컨테이너를 정지하고 삭제하는 경우:

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   ``down`` 명령으로 볼륨도 삭제하는 경우 ``-v`` 옵션을 추가합니다.
   이 경우 모든 데이터가 삭제되므로 주의하세요.

   .. code-block:: bash

       docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

관리자 비밀번호 변경
----------------------

관리 UI의 사용자 편집 화면에서 비밀번호를 변경할 수 있습니다.

1. http://localhost:8080/admin/ 에 접속하여 로그인합니다.
2. 우측 상단 메뉴에서 "사용자"를 선택합니다.
3. 관리자 사용자(admin)의 편집 화면을 열어 비밀번호를 변경합니다.

다음 단계
=========

Fess 설정이 완료되었으면 다음 문서를 참조하여 Fess를 활용하세요:

- :doc:`15.6/install/run` — Fess 시작·정지·설정 상세
- :doc:`15.6/admin/index` — 관리자 가이드 (크롤 설정, 사용자 관리 등)
- :doc:`15.6/user/index` — 사용자 가이드 (검색 사용법)

문제가 발생한 경우 :doc:`15.6/install/troubleshooting` 을 참조하세요.

.. |image0| image:: ../resources/images/en/install/dockerdesktop-1.png
.. |image1| image:: ../resources/images/en/install/dockerdesktop-2.png
.. |image2| image:: ../resources/images/en/install/dockerdesktop-3.png
.. |image3| image:: ../resources/images/en/install/dockerdesktop-4.png
