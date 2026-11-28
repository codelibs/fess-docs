===============================================
OpenSearch Dashboards로 검색 로그 깊이 분석하기
===============================================

들어가며
========

Fess 15.9에서는 관리 화면의 [시스템 정보] > [검색 로그]에서 제로 히트율, 클릭률, 클릭 순위 분포, 응답 시간, 요일·시간대별 검색 수, 역할·그룹별 검색 수를 확인할 수 있습니다.
각 표는 CSV로 다운로드할 수 있습니다.
문제가 있는 검색어를 찾아 동의어나 키 매치로 개선하는 흐름은 :doc:`guide-08`\ 에서 설명합니다.

한편 이 화면에서는 다음과 같은 집계를 할 수 없습니다.

- 366일을 넘는 기간의 추이(화면의 "사용자 지정" 기간은 최대 366일입니다)
- 역할별이나 라벨별로 어떤 검색어가 제로 히트가 되는지
- 검색어마다 실제로 어떤 URL이 열렸는지
- 직접 정한 관점의 그래프를 모아 둔 대시보드

검색 로그와 클릭 로그는 OpenSearch 인덱스에 저장되어 있으므로 OpenSearch Dashboards에서 직접 집계할 수 있습니다.
이 글에서는 docker-fess의 Compose 파일로 OpenSearch Dashboards를 기동하고, Fess에 포함된 대시보드를 가져오고, 로그 필드를 확인한 다음, 위의 4가지 집계를 만드는 데까지 설명합니다.

시작하기 전에: 접근 제한
========================

docker-fess의 OpenSearch Dashboards는 OpenSearch 쪽과 마찬가지로 보안 플러그인을 제거한 구성입니다.
포트 5601에 접근할 수 있는 사람은 로그인 없이 검색 로그의 모든 필드(사용자 ID, IP 주소 등)를 읽을 수 있습니다.
게다가 Dev Tools에서 Fess의 사용자나 설정 인덱스를 포함한 모든 인덱스를 변경하거나 삭제할 수 있습니다.

따라서 포트 5601(과 9200)은 관리자의 단말에서만 접근할 수 있도록 해 주십시오.
관리자가 아닌 사람에게 검색 로그 집계를 보여 주고 싶다면 OpenSearch Dashboards를 공개하지 말고, Fess의 [사용자] > [역할]에서 ``admin-searchlog-view``\ 라는 이름의 역할을 만들어 그 사람에게 할당합니다.
이 역할로는 [시스템 정보] > [검색 로그]를 열람할 수 있으며, 로그를 삭제할 수는 없습니다.

OpenSearch Dashboards 기동하기
==============================

:doc:`guide-02`\ 의 절차로 ``compose.yaml``\ 과 ``compose-opensearch3.yaml``\ 을 둔 디렉터리에 Dashboards용 파일을 추가합니다.
``compose-dashboards3.yaml``\ 은 ``dashboards/`` 디렉터리의 Dockerfile로 이미지를 빌드하므로 파일 3개가 필요합니다.

::

    $ cd fess-docker
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-dashboards3.yaml
    $ mkdir dashboards
    $ curl -L -o dashboards/Dockerfile https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/dashboards/Dockerfile
    $ curl -L -o dashboards/opensearch_dashboards.yml https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/dashboards/opensearch_dashboards.yml

3개의 Compose 파일을 지정하여 기동합니다.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-dashboards3.yaml up -d

처음 ``up``\ 할 때 ``opensearch-dashboards:3.9.0``\ 에서 ``securityDashboards`` 플러그인을 제거한 이미지가 빌드됩니다.
컨테이너는 네트워크 ``search_net`` 위에서 ``OPENSEARCH_HOSTS='["http://search01:9200"]'``\ 에 연결하고 포트 5601을 공개합니다.

브라우저에서 ``http://localhost:5601``\ 을 열어 홈 화면이 표시되면 기동된 것입니다.
중지하거나 상태를 확인할 때도 ``-f``\ 로 3개의 파일을 지정해 주십시오.
대시보드 등의 저장된 객체는 OpenSearch의 ``.kibana`` 인덱스에 저장되므로, ``down -v``\ 로 볼륨을 지우면 함께 사라집니다.

포함된 대시보드 가져오기
========================

Fess에는 검색 로그용 대시보드 정의 ``fess_log.ndjson``\ 이 포함되어 있습니다.
Docker의 경우 컨테이너에서 꺼냅니다.
ZIP 버전에서는 압축을 푼 디렉터리의 ``extension/kibana/fess_log.ndjson``\ 에 있습니다.

::

    $ docker cp fess01:/usr/share/fess/extension/kibana/fess_log.ndjson .

GitHub의 ``https://raw.githubusercontent.com/codelibs/fess/fess-15.9.0/src/main/assemblies/extension/kibana/fess_log.ndjson``\ 에서도 같은 파일을 받을 수 있습니다.

1. 왼쪽 메뉴의 [Dashboards Management]를 열고 [Saved objects]를 선택합니다
2. [Import]를 클릭하고 ``fess_log.ndjson``\ 을 선택하여 가져옵니다
3. 왼쪽 메뉴의 [Dashboards]에서 ``fess_log`` 대시보드를 엽니다

가져오면 인덱스 패턴 ``fess_log*``\ (시간 필드는 ``requestedAt``), 6개의 시각화, ``fess_log`` 대시보드가 등록됩니다.
인덱스 패턴도 포함되어 있으므로 미리 ``fess_log*``\ 를 수동으로 만들 필요는 없습니다.
수동으로 만든 뒤에 가져오면 같은 이름의 패턴이 2개가 됩니다.

포함된 대시보드의 집계 방식에 주의하기
--------------------------------------

``fess_log*``\ 는 ``fess_log``\ 로 시작하는 모든 인덱스에 걸쳐 있으며, 포함된 시각화는 인덱스로 범위를 좁히지 않습니다.
15.9의 클릭 로그에는 검색어(``searchWord``)와 ``requestedAt``\ 이 들어가므로, 예를 들어 "search-term-rank"의 건수에는 검색 횟수와 클릭 횟수가 합산됩니다.
AI 검색 모드를 사용하는 경우에는 채팅 로그(``fess_log.chat_log``)도 건수와 응답 시간에 섞입니다.

검색만 세고 싶다면 대시보드 상단의 검색 바에 다음 조건을 입력한 다음 확인해 주십시오.

::

    _index : "fess_log.search_log"

또한 ``fess_log*``\ 에 저장된 필드 목록은 이전 버전의 것이어서 ``rank`` 등의 새 필드를 포함하지 않습니다.
직접 집계를 만들 때는 다음 절의 인덱스 패턴을 사용합니다.

집계용 인덱스 패턴 만들기
=========================

검색 로그와 클릭 로그를 각각 별도의 인덱스 패턴으로 만들어 두면 섞일 걱정이 없고, 현재의 필드를 모두 선택할 수 있습니다.

1. [Dashboards Management] > [Index patterns]에서 [Create index pattern]을 클릭합니다
2. "Index pattern name"에 ``fess_log.search_log``\ 를 입력하고 [Next step]을 클릭합니다
3. "Time field"에서 ``requestedAt``\ 을 선택하고 [Create index pattern]을 클릭합니다
4. 같은 절차로 ``fess_log.click_log``\ (시간 필드는 ``requestedAt``)도 만듭니다

나중에 필드가 늘어난 경우(예를 들어 라벨로 범위를 좁힌 검색이 처음 기록되었을 때)에는 인덱스 패턴 화면에서 [Refresh field list]를 클릭합니다.

시간 처리
---------

Fess는 날짜와 시간을 UTC로 저장합니다.
OpenSearch Dashboards는 기본적으로 브라우저의 시간대로 표시하며, 날짜 구분도 이를 따릅니다.
다른 시간대로 보고 싶다면 [Dashboards Management] > [Advanced settings]의 ``dateFormat:tz``\ 를 사용하는 시간대(예: ``Asia/Tokyo``)로 바꿉니다.

Fess의 [검색 로그] 화면은 서버의 시간대로 날짜를 구분합니다.
docker-fess 컨테이너는 기본적으로 UTC이므로, 일별 수치를 양쪽에서 대조하면 날짜 구분이 다른 만큼 어긋날 수 있습니다.

로그 필드
=========

검색 로그(``fess_log.search_log``)는 검색 1회당 1건입니다.
집계에 자주 사용하는 필드는 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 유형
     - 내용
   * - ``queryId``
     - keyword
     - 검색마다의 ID. 클릭 로그의 ``queryId``\ 와 대응합니다
   * - ``searchWord``
     - keyword
     - 검색어. 라벨로 범위를 좁힌 검색에서는 ``신청 label:"hr"``\ 처럼 조건도 포함합니다
   * - ``searchField.*``
     - keyword
     - 검색어를 필드별로 나눈 것. 일반 검색어는 ``searchField._default``, 라벨로 좁히는 조건은 ``searchField.label``\ 에 들어갑니다
   * - ``requestedAt``
     - date
     - 검색한 일시(UTC로 저장)
   * - ``hitCount``
     - long
     - 히트 건수. ``0``\ 이 제로 히트입니다
   * - ``responseTime`` / ``queryTime``
     - long
     - 검색 전체의 처리 시간과 OpenSearch에서의 검색 시간(밀리초)
   * - ``queryOffset`` / ``queryPageSize``
     - integer
     - 가져오기 시작 위치와 1페이지당 건수. 2페이지 이후라면 ``queryOffset``\ 이 0보다 커집니다
   * - ``accessType``
     - keyword
     - ``json``, ``gsa``, ``admin``, ``other``, ``web`` 중 하나. 표준 테마의 검색 화면은 ``/api/v2/search``\ 를 호출하므로 ``json``\ 이 되며, 관리 화면의 [시스템 정보] > [검색]에서 한 검색은 ``admin``\ 입니다
   * - ``user`` / ``roles``
     - keyword
     - 로그인 사용자의 ID와 검색에 사용된 역할 목록. ``roles`` 값은 첫 1글자로 종류를 나타내며, ``R``\ 이 역할, ``2``\ 가 그룹, ``1``\ 이 사용자입니다(예: ``Rguest``)
   * - ``userSessionId`` / ``clientIp`` / ``userAgent`` / ``referer`` / ``virtualHost``
     - keyword
     - 이용자를 식별하는 Cookie 값, IP 주소, 브라우저, 참조 페이지, 가상 호스트

클릭 로그(``fess_log.click_log``)는 검색 결과의 링크가 ``/go/``\ 를 거쳐 열렸을 때 기록됩니다.
다만 브라우저가 Fess 세션을 가지고 있지 않은(유효한 세션 Cookie를 보내지 않는) 요청에서는 기록되지 않습니다.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 유형
     - 내용
   * - ``queryId``
     - keyword
     - 클릭한 검색의 ``queryId``
   * - ``url`` / ``docId``
     - keyword
     - 열린 문서의 URL과 문서 ID
   * - ``rank``
     - integer
     - 검색 결과 전체에서의 순위(1위가 1). 2페이지의 첫 번째 결과라면 11입니다
   * - ``order``
     - integer
     - 페이지 안에서의 위치(맨 앞이 0). 순위 집계에는 ``rank``\ 를 사용합니다
   * - ``searchWord`` / ``accessType``
     - keyword
     - 클릭한 검색에서 복사한 검색어와 액세스 타입. 검색 로그와 결합하지 않아도 검색어별로 집계할 수 있습니다
   * - ``requestedAt`` / ``queryRequestedAt``
     - date
     - 클릭한 일시와 클릭한 검색의 일시

``searchWord``, ``accessType``, ``rank``\ 가 클릭 로그에 들어가는 것은 15.9부터입니다.
그 이전에 기록된 클릭에는 이 필드들이 없습니다.

집계 레시피
===========

여기서는 처음에 든 "화면에서는 할 수 없는 집계" 4가지를 만듭니다.
첫 번째는 Visualize로 만들고, 나머지는 왼쪽 메뉴의 [Dev Tools]에서 검색 API로 실행합니다.

검색어별로 열린 URL
-------------------

검색어마다 어떤 문서가 몇 위에서 열렸는지를 표로 만듭니다.
키 매치나 문서 부스트의 후보를 고를 때 사용할 수 있습니다.

1. 왼쪽 메뉴의 [Visualize]에서 [Create visualization]을 클릭하고 "Data Table"을 선택합니다
2. 소스로 ``fess_log.click_log``\ 를 선택합니다
3. Metrics의 [Add]로 Metric을 추가하고, "Aggregation"에 "Average", "Field"에 ``rank``\ 를 선택합니다
4. Buckets의 [Add] > [Split rows]에서 "Aggregation"에 "Terms", "Field"에 ``searchWord``, "Size"에 20을 지정합니다
5. [Split rows]를 한 번 더 추가하고 "Terms", "Field"에 ``url``, "Size"에 5를 지정합니다
6. [Update]를 클릭하고 오른쪽 위에서 기간을 선택한 다음 저장합니다

평균 순위가 큰 조합은 이용자가 아래쪽까지 찾아 내려가서 연 문서입니다.

역할별 제로 히트 검색어
-----------------------

부서마다 역할을 나누어 두었다면 어느 부서의 검색에서 무엇을 찾지 못하고 있는지 확인합니다.

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [
            { "term": { "hitCount": 0 } },
            { "range": { "requestedAt": { "gte": "now-90d/d" } } }
          ]
        }
      },
      "aggs": {
        "roles": {
          "terms": { "field": "roles", "size": 20, "exclude": "1.*" },
          "aggs": {
            "words": { "terms": { "field": "searchWord", "size": 10 } }
          }
        }
      }
    }

``exclude``\ 로 ``1``\ 로 시작하는 값(개별 사용자)을 제외하고 역할과 그룹만 나열합니다.
한 번의 검색은 그 이용자의 모든 역할과 그룹에 각각 집계됩니다.
로그인하지 않은 검색은 ``Rguest``\ 에 들어갑니다.

라벨별 검색 수와 제로 히트 수
-----------------------------

검색 화면에서 라벨을 선택하여 검색한 횟수와 그중 제로 히트인 횟수를 라벨별로 셉니다.

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": { "range": { "requestedAt": { "gte": "now-90d/d" } } },
      "aggs": {
        "labels": {
          "terms": { "field": "searchField.label", "size": 20 },
          "aggs": {
            "zero_hit": { "filter": { "term": { "hitCount": 0 } } }
          }
        }
      }
    }

라벨로 범위를 좁힌 검색이 한 건도 기록되지 않았다면 ``searchField.label`` 필드가 아직 없으므로 ``labels`` 버킷은 비어 있습니다.

월별 제로 히트율(2년치)
-----------------------

화면의 기간 상한을 넘어 제로 히트율(건수가 아닌 비율)의 장기 추이를 봅니다.

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [ { "range": { "requestedAt": { "gte": "now-2y/d" } } } ],
          "must_not": [ { "term": { "accessType": "admin" } } ]
        }
      },
      "aggs": {
        "per_month": {
          "date_histogram": {
            "field": "requestedAt",
            "calendar_interval": "month",
            "time_zone": "Asia/Tokyo"
          },
          "aggs": {
            "zero_hit": { "filter": { "term": { "hitCount": 0 } } },
            "zero_hit_rate": {
              "bucket_script": {
                "buckets_path": { "zero": "zero_hit>_count", "total": "_count" },
                "script": "params.zero / params.total"
              }
            }
          }
        }
      }
    }

월별 버킷에 검색 수(``doc_count``), 제로 히트 수(``zero_hit.doc_count``), 제로 히트율(``zero_hit_rate.value``, 0~1)이 반환됩니다.
``time_zone``\ 에 의해 월 구분은 지정한 시간대(여기서는 ``Asia/Tokyo``\ 이며, 사용하는 시간대로 바꾸십시오) 기준이 되며, 관리 화면에서 한 검색은 ``must_not``\ 으로 제외합니다.
2년치 로그가 남아 있는지는 다음 절의 보존 기간 설정에 따라 다릅니다.

보존 기간과 개인 정보
=====================

기본적으로 검색 로그는 계속 남습니다.
[시스템] > [일반]의 "이전 검색 로그 삭제"가 기본적으로 ``-1``\ (삭제하지 않음)로 되어 있기 때문입니다.
일수를 지정하면 매일 0시에 실행되는 작업 "Log Purger"가 그 일수보다 오래된 검색 로그를 삭제합니다.
클릭 로그, 즐겨찾기 로그, 채팅 로그도 같은 일수로 삭제됩니다.
이용자 기록은 별도의 설정 "이전 사용자 로그 삭제"로 관리하며, 이것도 기본값은 ``-1``\ 입니다.

장기 추이를 보고 싶은 기간과 조직 내 개인 정보 취급 규정을 모두 고려하여 일수를 정해 주십시오.
검색 로그에는 로그인 사용자의 ID(``user``, ``roles``\ 에서 ``1``\ 로 시작하는 값), IP 주소, User-Agent가 들어갑니다.
또한 기본적으로 검색 결과에 표시된 문서의 URL과 제목도 ``documents`` 필드에 기록됩니다(``logging.search.docs.enabled=true``).
OpenSearch Dashboards에서는 이것들이 모두 보이므로 앞에서 설명한 접근 제한을 지켜 주십시오.

잘 되지 않을 때
===============

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 증상
     - 확인할 사항
   * - Discover나 시각화에 데이터가 나오지 않는다
     - 오른쪽 위의 기간에 로그가 있는 일시가 포함되어 있는지. 검색한 뒤 로그가 기록되기까지 1분 정도 걸릴 수 있습니다(매분 실행되는 작업 "Log Aggregator"가 기록합니다)
   * - ``rank``\ 나 ``searchField.label``\ 을 선택할 수 없다
     - ``fess_log*``\ 를 사용하고 있지 않은지. 전용 인덱스 패턴을 만들거나 [Refresh field list]를 클릭한다
   * - 건수가 [검색 로그] 화면보다 많다
     - ``fess_log*``\ 로 클릭이나 채팅 로그까지 세고 있지 않은지. 액세스 타입으로 좁히는 조건과 날짜 구분의 시간대가 같은지
   * - 클릭 건수가 적다
     - 링크가 ``/go/``\ 를 거치지 않거나, [일반]의 "검색 로그"가 비활성화되어 있거나, 브라우저가 Fess 세션 없이 ``/go/``\ 를 열고 있다. :doc:`guide-08`\ 의 전제 조건도 확인한다

다음에 읽을 글
==============

- 찾아낸 검색어를 동의어나 키 매치로 개선하고 싶다: :doc:`guide-08`
- 역할이나 그룹 설계를 재검토하고 싶다: :doc:`guide-05`
- 모니터링과 백업을 포함한 운영 체계를 갖추고 싶다: :doc:`guide-10`
- 전사 도입의 단계마다 무엇을 측정할지 정하고 싶다: :doc:`guide-23`

참고 자료
=========

- `검색 로그 <https://fess.codelibs.org/ko/stable/admin/searchlog-guide.html>`__
- `검색 로그 시각화 설정 <https://fess.codelibs.org/ko/stable/config/admin-opensearch-dashboards.html>`__
- `일반 <https://fess.codelibs.org/ko/stable/admin/general-guide.html>`__
- `Docker 설치 (상세) <https://fess.codelibs.org/ko/stable/install/install-docker.html>`__
- `docker-fess의 Compose 파일(GitHub) <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose>`__
- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__
