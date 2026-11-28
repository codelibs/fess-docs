==================================
Fess 운영: 모니터링·백업·장애 대응
==================================

들어가며
========

Fess를 사내에 공개한 뒤 운영 담당자가 곤란해지는 것은 다음과 같은 상황입니다.
검색이 안 된다는 사실을 사용자의 문의를 받고서야 처음 알게 되거나, 야간 크롤링이 실패하고 있었는데 며칠 동안 눈치채지 못하거나, 서버를 다시 구축했더니 설정이 돌아오지 않는 경우입니다.

이 글에서는 Fess 15.9에 갖춰진 기능을 사용해 이러한 상황에 대비하는 절차를 설명합니다.

- ``/api/v2/health``\ 와 ``/api/admin/stats``\ 로 Fess와 OpenSearch의 상태를 외부 모니터링 도구에서 확인한다
- 크롤링 종료, OpenSearch 상태 변화, 오류 로그를 메일·Slack·Google Chat으로 통지한다
- 어느 로그 파일에 무엇이 기록되고, 어디에 있는지 파악한다
- 설정 백업을 cron으로 받아 다른 서버에 복원한다
- 장애가 발생했을 때 Fess의 어느 화면과 어느 로그를 봐야 하는지 파악한다

설정을 코드로 관리하는 방법은 :doc:`guide-16`\ 에서, 문서 수나 사용자 증가에 맞춘 확장(힙 조정 포함)은 :doc:`guide-14`\ 에서 다룹니다.
예시 명령은 :doc:`guide-02`\ 의 Docker 구성(``fess01``\ 과 ``search01``)을 전제로 합니다.
ZIP 버전·RPM/DEB 버전에서의 차이는 그때그때 덧붙입니다.

모니터링하기
============

가용성 모니터링: /api/v2/health
-------------------------------

Fess는 인증 없이 호출할 수 있는 헬스 체크 API를 갖추고 있습니다.

::

    $ curl -fsS --max-time 10 http://localhost:8080/api/v2/health
    {"response":{"status":0,"engine":{"status":"GREEN","ping_status":0}}}

HTTP 상태 코드의 의미는 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 상태 코드
     - 상태
   * - 200
     - Fess가 응답하고 있으며, OpenSearch 클러스터가 ``GREEN`` 또는 ``YELLOW``
   * - 503
     - OpenSearch 클러스터가 ``RED``\ 이거나, Fess에서 OpenSearch에 연결할 수 없음(``error.details.engine.status``\ 는 ``UNAVAILABLE``)
   * - 응답 없음·타임아웃
     - Fess 프로세스가 멈춰 있거나, OpenSearch가 응답하지 않아 대기하고 있음

모니터링 도구에서는 이 상태 코드로 판정합니다.
``curl``\ 을 사용할 경우 ``-f``\ 를 붙이면 503일 때 종료 코드가 0이 아닌 값이 됩니다.
OpenSearch 프로세스가 멈추지 않은 채 응답하지 않게 되면, 이 API는 OpenSearch의 응답을 ``index.health.timeout``\ (기본값 ``10m``)까지 기다립니다.
모니터링 쪽에서는 위 예의 ``--max-time 10``\ 처럼 타임아웃을 설정하고, 타임아웃도 이상으로 취급하십시오.
참고로 이전 버전의 글에서 소개했던 ``/api/v1/health``\ 는 15.9의 표준 구성에서는 사용할 수 없습니다(``/api/v1``\ 은 ``fess-webapp-v1-api`` 플러그인을 설치한 경우에만 제공됩니다).

Docker의 ``fess01``\ 은 이 API를 두 가지 방식으로 사용합니다.

- ``compose.yaml``\ 의 ``healthcheck``\ 가 30초마다 호출하며, ``docker compose ps``\ 의 ``(healthy)`` 표시가 됩니다
- 컨테이너 안의 시작 스크립트도 60초마다 호출하며, 시작 후 200이 아닌 응답이 5회 연속되면 컨테이너를 종료합니다. ``restart: unless-stopped``\ 에 의해 컨테이너는 다시 시작됩니다

따라서 OpenSearch가 ``RED``\ 인 채로 몇 분이 지나면 ``fess01``\ 이 재시작을 반복합니다.
``fess01``\ 의 재시작이 계속될 때는 먼저 ``search01``\ 을 확인하십시오.

리소스 모니터링: /api/admin/stats
---------------------------------

힙 사용률이나 디스크 여유 공간은 관리 API ``GET /api/admin/stats``\ 로 가져옵니다.
[시스템 정보] > [설정 정보]에는 프로퍼티 목록만 있고 메모리 사용량은 표시되지 않습니다.

관리 API에는 액세스 토큰이 필요합니다.

1. [시스템] > [액세스 토큰]을 열고 [새로 만들기]를 클릭합니다
2. "이름"에 용도(예: ``monitoring``)를, "권한"에 ``{role}admin-api``\ 를 입력하고 [작성]을 클릭합니다
3. 목록에서 만든 토큰을 열고 "토큰" 값을 기록해 둡니다

.. warning::

   ``{role}admin-api`` 토큰으로는 설정 변경이나 삭제를 포함한 모든 관리 API를 사용할 수 있습니다.
   읽기 전용으로 제한하는 설정은 없습니다.
   모니터링 서버의 파일 등에 보관할 때는 관리자 비밀번호와 똑같이 취급하십시오.

토큰은 ``Authorization`` 헤더로 전달합니다.
다음 예에서는 힙 사용률(%)과 파일 시스템별 사용률을 추출합니다.

::

    $ curl -fsS -H "Authorization: Bearer <토큰>" http://localhost:8080/api/admin/stats \
        | jq '{heap: .response.stats.jvm.memory.heap.percent, fs: [.response.stats.fs[] | {path, percent}]}'

그 밖에도 GC 횟수와 누적 시간(``jvm.gc``), OS의 CPU 사용률과 로드 애버리지(``os``), OpenSearch의 클러스터 상태와 샤드 수(``engine``)가 반환됩니다.
항목 목록은 `Stats API <https://fess.codelibs.org/ko/stable/api/admin/api-admin-stats.html>`__\ 를 참조하십시오.

값을 읽을 때는 다음 두 가지에 주의하십시오.

- ``jvm``\ 은 Fess 본체(웹 애플리케이션)의 JVM 값입니다. 크롤링은 별도의 JVM 프로세스에서 동작하므로 크롤러의 메모리 부족은 여기에 나타나지 않습니다. ``fess-crawler.log``\ 에서 확인합니다(후술)
- ``fs``\ 는 Fess가 동작하는 호스트(Docker에서는 컨테이너)의 파일 시스템입니다. OpenSearch 데이터 영역의 여유 공간은 OpenSearch에 직접 조회합니다

::

    $ curl -s "http://localhost:9200/_cat/allocation?v"

힙 크기를 변경하는 방법은 :doc:`guide-14`\ 에서 설명합니다.

알림 받기
---------

Fess의 알림 대상은 [시스템] > [일반]의 "알림" 영역에 있는 세 항목으로 설정합니다.

- "알림 메일": 수신자 메일 주소(여러 개는 쉼표로 구분)
- "Slack Webhook URLs": Slack의 Incoming Webhook URL
- "Google Chat Webhook URLs": Google Chat의 Webhook URL

이 중 하나라도 설정하면 다음 세 종류의 알림이 같은 대상으로 전송됩니다.

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - 알림
     - 전송 조건
     - 추가로 필요한 설정
   * - 크롤링 완료(제목 ``[FESS] Crawler completed``)
     - 크롤링 작업이 끝날 때마다 성공 여부와 관계없이 전송됩니다. 상태(OK/FAIL)와 등록한 문서 수가 들어 있습니다
     - 없음
   * - OpenSearch 상태 변화(제목 ``[FESS] Status Change``)
     - 스케줄러 작업 "Search Engine Monitor"가 매분 OpenSearch에 조회하며, ``RED``\ 가 되었을 때와 ``RED``\ 에서 회복되었을 때 전송됩니다
     - 없음
   * - 로그 알림(제목 ``[FESS] ERROR Log Alert``)
     - Fess와 크롤러 등이 출력한 ERROR(또는 지정한 레벨 이상)의 로그를 작업 "Log Notification"이 5분마다 모아서 보냅니다
     - [일반]의 "Log Notification"을 활성화하고 "Log Notification Level"을 선택

OpenSearch에 연결할 수 없게 되면 "Search Engine Monitor" 작업 자체가 실패하며, 상태 변화 알림은 전송되지 않습니다.
연결 끊김은 앞 절의 ``/api/v2/health``\ 를 외부에서 모니터링하여 감지하십시오.

로그 알림의 기본 레벨은 ``ERROR``\ 입니다.
실패한 스케줄 작업은 ``WARN``\ (``Failed to execute job: ...``)으로 기록되므로, 작업 실패도 알고 싶다면 "Log Notification Level"을 ``WARN``\ 으로 설정합니다.
이 경우 다른 ``WARN``\ 도 모두 통지됩니다.

메일로 받으려면 SMTP 서버를 두 파일에 설정하고 Fess를 재시작합니다.

::

    mail.smtp.server.main.host.and.port=smtp.example.com:587

- ``fess_env_web.properties``: 로그 알림, 상태 변화 알림, [테스트 메일 보내기] 버튼에서 사용됩니다
- ``fess_env_crawler.properties``: 크롤링 완료 알림에서 사용됩니다(크롤링은 별도의 프로세스에서 동작하기 때문입니다)

파일 위치는 ZIP 버전에서는 ``app/WEB-INF/classes/``, RPM/DEB 버전에서는 ``/etc/fess/``\ 입니다.
설정 후 [일반]의 [테스트 메일 보내기]로 메일이 도착하는지 확인합니다.

Docker에서 빠르게 알림을 받고 싶다면, 파일을 편집할 필요가 없는 Slack이나 Google Chat의 Webhook이 간편합니다.
다만 [일반]의 설정은 ``fess01`` 컨테이너 안의 ``system.properties``\ 에 저장되므로, ``docker compose down``\ 으로 컨테이너를 다시 만들면 사라집니다(:doc:`guide-02`\ 의 중지와 재개에 관한 절 참조).
후술하는 백업에서 ``system.properties``\ 도 받아 둡니다.

검색 응답 시간과 크롤링 결과 확인하기
-------------------------------------

외부 모니터링과는 별도로, 관리 화면에서 다음 세 화면을 정기적으로 확인합니다.

- [시스템 정보] > [작업 로그]: "Default Crawler" 등 작업의 상태(OK/실패)와 결과. "Search Engine Monitor", "Log Notification"처럼 매분·몇 분마다 동작하는 작업은 여기에 기록되지 않습니다
- [시스템 정보] > [크롤링 정보]: 세션별 "크롤러 상태"와 "인덱스 크기 (웹/파일)", "인덱스 크기 (데이터 저장소)". 이전보다 크게 줄지 않았는지 확인합니다
- [시스템 정보] > [검색 로그]의 [성능] 탭: 응답 시간의 중앙값·p95·p99와 응답이 느린 검색어. 검색 로그를 보는 방법은 :doc:`guide-08`\ 에서 설명합니다

로그 읽기
=========

로그 파일의 종류
----------------

Fess는 처리별로 다른 파일에 로그를 출력합니다.
조사하려는 내용에 따라 열어 볼 파일을 고릅니다.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 파일
     - 내용
   * - ``fess.log``
     - Fess 본체(검색 화면·관리 화면·API·스케줄러)의 로그. 시작 실패, OpenSearch 연결 오류, 백업 가져오기 실패 등
   * - ``fess-crawler.log``
     - 크롤러 프로세스의 로그. URL별 가져오기 오류, 인증 실패, 크롤러 메모리 부족 등
   * - ``audit.log``
     - 로그인·로그아웃과 관리 작업의 감사 로그
   * - ``fess-suggest.log`` / ``fess-thumbnail.log``
     - 추천어 생성, 썸네일 생성 로그
   * - ``fess-llm.log``
     - AI 검색 모드(RAG)와 LLM 연동 로그
   * - ``searchlog.log``
     - 검색별 기록([일반]의 "검색 로그"가 활성화된 경우)
   * - ``server_*.log``
     - Tomcat 로그

위치는 설치 방법에 따라 다릅니다.

- ZIP 버전: Fess를 압축 해제한 디렉터리의 ``logs/``
- RPM/DEB 버전: ``/var/log/fess/``
- Docker: 컨테이너 안의 ``/var/log/fess/``. ``fess.log``\ ·\ ``fess-crawler.log``\ ·\ ``audit.log`` 등은 표준 출력으로도 나오므로 ``docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01``\ 로 읽을 수 있습니다. 컨테이너를 다시 만들면 사라집니다

어떤 설치 방법이든 [시스템 정보] > [로그 파일]에서 파일 이름을 클릭하면 다운로드할 수 있습니다.
서버에 로그인할 수 없는 담당자도 여기서 로그를 확인할 수 있습니다.

각 로그는 날짜가 바뀌거나 100MB를 넘으면 ``.log.gz``\ 로 압축되어 교체됩니다.
압축된 파일은 ``fess.log``\ 와 ``searchlog.log``\ 에서는 90일, ``audit.log``\ 에서는 360일이 지나면 자동으로 삭제됩니다.
반면 ``fess-crawler.log``\ ·\ ``fess-suggest.log``\ ·\ ``fess-thumbnail.log`` 등 크롤러나 자식 프로세스 로그의 압축 파일은 자동으로 삭제되지 않습니다.
로그 디렉터리의 용량을 모니터링하고 오래된 파일을 정기적으로 삭제하십시오.

자세히 조사할 때
----------------

기본적으로 ``fess.log``\ 에는 WARN 이상, ``fess-crawler.log``\ 에는 INFO 이상이 출력됩니다.
``fess.log``\ 를 더 자세하게 하려면 [시스템] > [일반]의 "로그 레벨"을 ``INFO``\ 나 ``DEBUG``\ 로 올립니다.
이 변경은 Fess를 재시작하면 원래대로 돌아갑니다.
크롤러의 로그 레벨은 작업 스크립트에서 정해집니다.
"Default Crawler"의 스크립트에는 ``logLevel("info")``\ 가 포함되어 있으므로, [시스템] > [스케줄러]에서 이를 ``logLevel("debug")``\ 로 바꾸면 다음 크롤링부터 자세한 로그가 출력됩니다.
조사가 끝나면 원래대로 되돌리십시오.
레벨을 상시 변경해 두는 방법은 `로그 설정 <https://fess.codelibs.org/ko/stable/config/admin-logging.html>`__\ 을 참조하십시오.

포럼 등에서 상담할 때는 [시스템 정보] > [유지보수]의 "진단"에 있는 [로그 다운로드]가 도움이 됩니다.
로그, ``system.properties``, ``fess_config.properties``, 설정 인덱스의 내용, OpenSearch의 상태를 묶은 zip 파일이 다운로드됩니다.
API 키나 ``app.cipher.key`` 등의 값은 ``XXXXXXXX``\ 로 치환되지만, 로그 본문과 설정 인덱스의 내용은 마스킹되지 않습니다.
외부에 전달하기 전에 내용을 확인하십시오.

백업하기
========

무엇이 어디에 있는가
--------------------

Fess의 데이터는 세 곳에 나뉘어 있습니다.
[시스템 정보] > [백업]으로 받을 수 있는 것은 이 중 첫 번째뿐입니다.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 데이터
     - 저장 위치
     - 백업 방법
   * - 크롤링 설정, 스케줄러, 라벨, 사용자, [일반]의 설정
     - OpenSearch의 설정 인덱스와 ``system.properties``
     - [시스템 정보] > [백업] 또는 관리 API
   * - 크롤링한 문서, 사전(동의어·불용어 등)
     - OpenSearch의 ``fess.*`` 인덱스와 ``configsync`` 인덱스
     - OpenSearch 스냅샷(사전만이라면 파일 복사도 가능)
   * - ``fess_config.properties``\ (``app.cipher.key`` 포함), 시작 설정, 설치한 플러그인
     - Fess 서버의 파일
     - 파일 복사 또는 구성 관리

크롤링한 문서는 설정만 복원하면 다시 크롤링하여 재생성할 수 있습니다.
다시 크롤링하는 데 시간이 너무 오래 걸리는 경우에만 스냅샷을 받습니다.

[백업]에서 받을 수 있는 파일
----------------------------

[시스템 정보] > [백업]에는 다음 파일이 나열됩니다.
이름을 클릭하면 파일을 하나씩 다운로드할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 파일
     - 내용
   * - ``fess_basic_config.bulk``
     - 크롤링 설정, 스케줄러, 라벨, 키 매치, 웹/파일 인증 등의 설정
   * - ``fess_config.bulk``
     - 위 내용에 더해 크롤링 정보, 장애 URL, 작업 로그, 사용자 태그 등
   * - ``fess_user.bulk``
     - 사용자, 역할, 그룹
   * - ``system.properties``
     - [시스템] > [일반]의 설정
   * - ``fess.json`` / ``doc.json``
     - 문서 인덱스의 설정과 매핑
   * - ``*.ndjson``
     - 검색 로그, 클릭 로그, 즐겨찾기, AI 채팅 로그, 검색 사용자. 다운로드는 할 수 있지만 업로드하여 복원할 수는 없습니다

설정을 복원하는 데 사용하는 것은 ``fess_basic_config.bulk``, ``fess_user.bulk``, ``system.properties``\ 의 세 파일입니다.
사용자 태그를 사용하는 경우에는 ``fess_config.bulk``\ 도 받아 둡니다.

``*.bulk``\ 에는 후술하는 인증 정보를 제외하고 설정 값이 암호화되지 않은 채 들어 있습니다.
기밀 파일로 보관하십시오.

cron으로 매일 받기
------------------

관리 API ``GET /api/admin/backup/file/<파일명>/``\ 로 화면과 같은 파일을 받을 수 있습니다.
토큰은 앞의 "리소스 모니터링"과 같은 절차로 만들고, 스크립트를 실행하는 사용자만 읽을 수 있는 파일에 저장합니다.

::

    $ sudo mkdir -p /etc/fess-backup
    $ sudo sh -c 'umask 077; echo "<토큰>" > /etc/fess-backup/token'

다음 스크립트는 날짜별 디렉터리에 파일을 저장하고, 30일보다 오래된 디렉터리를 삭제합니다(보존 기간은 예시입니다).

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail

    FESS_URL=http://localhost:8080
    FESS_TOKEN=$(cat /etc/fess-backup/token)
    BASE_DIR=/var/backups/fess
    BACKUP_DIR="${BASE_DIR}/$(date +%Y%m%d)"

    umask 077
    mkdir -p "${BACKUP_DIR}"
    for id in fess_basic_config.bulk fess_config.bulk fess_user.bulk system.properties fess.json doc.json; do
      curl -fsS -H "Authorization: Bearer ${FESS_TOKEN}" \
        -o "${BACKUP_DIR}/${id}" "${FESS_URL}/api/admin/backup/file/${id}/"
      test -s "${BACKUP_DIR}/${id}"
    done

    # Docker 구성인 경우: 사전 파일도 복사한다
    docker cp search01:/usr/share/opensearch/config/dictionary/. "${BACKUP_DIR}/dictionary"

    find "${BASE_DIR}" -mindepth 1 -maxdepth 1 -type d -mtime +30 -exec rm -rf {} +

요점은 다음과 같습니다.

- URL 끝의 ``/``\ 는 생략할 수 없습니다. 파일 이름에 점이 포함되어 있어, ``/``\ 가 없으면 정적 파일에 대한 요청으로 취급되어 404가 됩니다
- ``curl``\ 에 ``-f``\ 를 붙이지 않으면 404나 오류 응답도 파일에 저장되어 스크립트가 성공한 것처럼 보입니다. ``-f``\ 와 ``set -e``\ 로 실패하면 멈추도록 하고 있습니다
- ZIP 버전·RPM/DEB 버전에서는 ``docker cp`` 줄 대신 OpenSearch 쪽 사전 디렉터리(Fess의 ``FESS_DICTIONARY_PATH``\ 가 가리키는 위치)를 복사합니다

스크립트를 ``/usr/local/bin/fess-backup.sh``\ 에 저장하고 실행 권한을 부여한 뒤, root의 crontab에 등록합니다(매일 2시 30분에 실행하는 예입니다).

::

    30 2 * * * /usr/local/bin/fess-backup.sh

등록했으면 한 번 수동으로 실행합니다.
``fess_basic_config.bulk``\ 를 열어 ``{"index":{"_index":``\ 로 시작하는 줄과 설정 내용의 JSON 줄이 번갈아 나열되어 있는지 확인합니다.
같은 처리는 ``fessctl``\ 로도 작성할 수 있습니다(:doc:`guide-16` 참조).

app.cipher.key 기록해 두기
--------------------------

Fess 15.9는 웹 인증·파일 인증의 비밀번호와, 크롤링 설정·데이터 저장소 설정의 파라미터에 저장한 비밀번호나 시크릿을 ``fess_config.properties``\ 의 ``app.cipher.key``\ 로 암호화하여 저장합니다.
``*.bulk``\ 에도 암호화된 채로 들어갑니다.
다른 서버에 복원할 때는 같은 ``app.cipher.key``\ 를 설정해 두어야 합니다.
키가 다르면 복호화할 수 없어 ``fess-crawler.log``\ 에 ``CipherFailureException``\ 이 기록되며, 해당 인증 정보를 사용하는 크롤링은 실패합니다.

``fess_config.properties``\ 는 ZIP 버전에서는 ``app/WEB-INF/classes/``, RPM/DEB 버전에서는 ``/etc/fess/``\ 에 있습니다.
값을 변경한 경우에는 이 파일도 ``*.bulk``\ 와 마찬가지로 기밀로 취급하고, 별도의 장소에 보관하십시오.
Docker에서 값을 변경하려면 ``compose.yaml``\ 의 ``FESS_JAVA_OPTS``\ 에 ``-Dfess.config.app.cipher.key=<값>``\ 을 지정합니다.
이렇게 하면 컨테이너를 다시 만들어도 같은 키가 사용됩니다.

.. warning::

   인증 정보를 저장한 뒤에 ``app.cipher.key``\ 를 변경하면 그때까지 저장한 값을 복호화할 수 없게 됩니다.
   변경하려면 웹 인증·파일 인증이나 데이터 저장소의 인증 정보를 등록하기 전에 변경하십시오.
   이미 운영 중인 환경에서는 값을 변경하지 말고 기록해 둡니다.

문서 인덱스의 스냅샷
--------------------

다시 크롤링하지 않고 문서를 복원하려면 OpenSearch의 스냅샷을 사용합니다.
대상에는 ``fess*``\ 에 더해 사전을 보관하는 ``configsync`` 인덱스를 반드시 포함합니다.
``configsync``\ 가 없으면 새 OpenSearch에 복원했을 때 사전 파일이 없어 문서 인덱스를 열 수 없습니다.

스냅샷을 사용하려면 OpenSearch 쪽에 리포지토리 경로(``path.repo``)를 설정해 두어야 합니다.
docker-fess의 ``compose-opensearch3.yaml``\ 에는 설정되어 있지 않으므로, 사용할 경우 추가합니다.
리포지토리 등록, 스냅샷 생성, 복원 절차는 `인덱스 관리 <https://fess.codelibs.org/ko/stable/config/admin-index-backup.html>`__\ 에 있습니다.
복원은 Fess를 중지한 상태에서 수행하며, ``configsync``\ 를 먼저 복원해야 합니다.

복원하기
========

복원 전에 알아 둘 것
--------------------

[백업]에서의 복원은 OpenSearch의 내용을 통째로 바꾸는 작업이 아닙니다.

- 복원은 업로드로만 수행합니다. 관리 API는 다운로드 전용이며 복원용 API는 없습니다
- ``*.bulk``\ 의 각 설정은 서버에 같은 설정이 없거나, 서버의 것보다 새로운 경우에만 기록됩니다. 백업을 받은 후에 변경한 설정은 이전 내용으로 돌아가지 않습니다
- 백업을 받은 후에 만든 설정은 삭제되지 않고 남습니다

따라서 "실수로 바꾼 설정을 어제 상태로 되돌리는" 용도에는 맞지 않습니다.
새 서버로의 이전이나 다시 구축한 환경으로의 복원에 사용합니다.

다른 서버로 설정을 복원하는 절차
--------------------------------

1. 이전 대상에 같은 버전의 Fess를 설치하고, ``fess_config.properties``\ 의 ``app.cipher.key``\ 를 이전 원본과 같은 값으로 설정합니다
2. 이전 원본에서 사용하던 플러그인(데이터 저장소, SSO 등)을 설치하고 Fess를 재시작합니다
3. 관리 화면에 로그인하여 [시스템 정보] > [백업]을 엽니다
4. "벌크 파일"에서 ``fess_basic_config.bulk``\ 를 선택하고 [업로드]를 클릭합니다. "대량 프로세스를 시작했습니다."가 표시됩니다
5. 같은 방법으로 ``fess_user.bulk``\ 와 ``system.properties``\ 를 업로드합니다. 사용자 태그를 사용하는 경우에는 ``fess_config.bulk``\ 도 업로드합니다(이전 원본의 크롤링 정보와 작업 로그도 함께 가져옵니다)

가져오기는 백그라운드에서 수행됩니다.
잠시 기다린 뒤 다음 사항을 확인합니다.

- [크롤러] > [웹]·[파일 시스템]·[데이터 저장소]와 [시스템] > [스케줄러]에 이전 원본의 설정이 나열되어 있다
- [사용자] > [사용자]에 이전 원본의 사용자가 나열되어 있다
- [시스템] > [일반]의 알림 대상 등이 이전 원본의 값으로 되어 있다

마지막으로 사전을 복원하고 문서를 다시 만듭니다.

- 사전: [시스템] > [사전]에서 종류별 화면을 열고, 백업한 사전 파일을 업로드합니다. 그런 다음 [시스템 정보] > [유지보수]의 "문서 인덱스 다시 로드"를 실행합니다. 다시 로드하는 동안 짧은 시간이지만 검색할 수 없게 됩니다
- 문서: [시스템] > [스케줄러]에서 "Default Crawler"의 [지금 시작]을 클릭하여 다시 크롤링합니다. 스냅샷에서 복원하는 경우에는 앞서 설명한 절차를 따릅니다

크롤링이 끝나면 [시스템 정보] > [크롤링 정보]에서 등록 건수를 확인합니다.
인증이 있는 크롤링 설정에서 건수가 0인 경우에는 ``fess-crawler.log``\ 에 ``CipherFailureException``\ 이 없는지 확인합니다.
있다면 ``app.cipher.key``\ 가 이전 원본과 일치하지 않는 것입니다.

장애에 대응하기
===============

자주 발생하는 증상과 Fess에서 확인할 곳을 정리합니다.

검색 화면이 열리지 않거나 /api/v2/health가 503을 반환한다
---------------------------------------------------------

1. OpenSearch의 상태를 확인합니다. ``curl -s "http://localhost:9200/_cluster/health?pretty"``\ 의 ``status``\ 가 ``red``\ 이면 OpenSearch 쪽의 문제입니다. Docker에서는 ``docker compose -f compose.yaml -f compose-opensearch3.yaml logs search01``\ 을 확인합니다
2. OpenSearch는 정상인데 Fess가 응답하지 않는 경우에는 ``fess.log``\ 에서 시작 시의 오류를 확인합니다
3. 스냅샷에서 복원한 직후에 ``red``\ 가 되는 경우에는 ``configsync``\ 를 복원하지 않았을 가능성이 있습니다(앞서 설명)

크롤링이 실패하거나 등록 건수가 줄었다
--------------------------------------

1. [시스템 정보] > [작업 로그]에서 해당 작업의 행을 열고 "결과"를 확인합니다
2. [시스템 정보] > [크롤링 정보]에서 최신 세션의 "크롤러 상태"와 인덱스 크기를 이전과 비교합니다
3. [시스템 정보] > [장애 URL]에서 가져오지 못한 URL의 "종류", "로그", "오류 횟수"를 확인합니다. HTTP 404·403·410·401도 여기에 기록됩니다
4. 자세한 내용은 ``fess-crawler.log``\ 에 있습니다. 장애 URL 상세의 "스레드 이름"으로 검색하면 그 시점의 전후 로그를 따라갈 수 있습니다

``fess-crawler.log``\ 에 ``OutOfMemoryError``\ 가 있으면 크롤러 프로세스의 힙이 부족한 것입니다.
크롤러의 힙은 ``fess_config.properties``\ 의 ``jvm.crawler.options``\ (기본값 ``-Xmx512m``)로 정해지며, Fess 본체의 힙과는 별개입니다.
조정 방법은 :doc:`guide-14`\ 에서 설명합니다.

알림이 오지 않는다
------------------

메일의 경우 먼저 [일반]의 [테스트 메일 보내기]로 메일이 오는지 확인합니다.
크롤링 완료 메일만 오지 않는 경우에는 ``fess_env_crawler.properties``\ 의 SMTP 서버를 확인합니다.
Docker에서는 ``down``\ 과 ``up``\ 으로 컨테이너를 다시 만들어 [일반]의 설정이 사라지지 않았는지도 확인합니다.
로그 알림만 오지 않는 경우에는 "Log Notification"이 활성화되어 있는지, "Log Notification" 작업이 활성화되어 있는지, "Log Notification Level"(작업 실패는 ``WARN``)이 적절한지 확인합니다.
그 밖의 확인 항목은 `로그 통지 <https://fess.codelibs.org/ko/stable/config/admin-log-notification.html>`__\ 의 "문제 해결"에 있습니다.

검색이 느리다
-------------

1. [시스템 정보] > [검색 로그]의 [성능] 탭에서 느린 것이 특정 검색어인지 전체인지 확인합니다
2. ``/api/admin/stats``\ 의 ``jvm.memory.heap.percent``\ 와 ``jvm.gc``\ 의 누적 시간을 느려지기 전과 비교합니다

다음에 읽을 글
==============

- 설정을 스크립트나 ``fessctl``\ 로 관리하고 싶다: :doc:`guide-16`
- 힙을 조정하거나 OpenSearch·Fess를 여러 대로 늘리고 싶다: :doc:`guide-14`
- SSO나 감사 로그 등으로 접근 보호를 강화하고 싶다: :doc:`guide-15`
- 검색 로그로 검색 품질을 개선하고 싶다: :doc:`guide-08`

참고 자료
=========

- `Health API <https://fess.codelibs.org/ko/stable/api/api-health.html>`__
- `Stats API <https://fess.codelibs.org/ko/stable/api/admin/api-admin-stats.html>`__
- `로그 통지 <https://fess.codelibs.org/ko/stable/config/admin-log-notification.html>`__
- `로그 설정 <https://fess.codelibs.org/ko/stable/config/admin-logging.html>`__
- `로그 파일 <https://fess.codelibs.org/ko/stable/admin/log-guide.html>`__
- `백업 <https://fess.codelibs.org/ko/stable/admin/backup-guide.html>`__
- `Backup API <https://fess.codelibs.org/ko/stable/api/admin/api-admin-backup.html>`__
- `인덱스 관리 <https://fess.codelibs.org/ko/stable/config/admin-index-backup.html>`__
- `장애 URL <https://fess.codelibs.org/ko/stable/admin/failureurl-guide.html>`__
- `유지보수 <https://fess.codelibs.org/ko/stable/admin/maintenance-guide.html>`__
