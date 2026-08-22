================================================
하이브리드 검색과 Rank Fusion(시맨틱 + 키워드)
================================================

개요
====

|Fess|\ 의 **하이브리드 검색**\ 은 기존 키워드 검색(BM25)과 **시맨틱(벡터) 검색**\ 을 결합하고, 두 결과 집합을 **Rank Fusion**\ 으로 병합하여 더 정확하고 관련성 높은 랭킹을 제공합니다. Rank Fusion은 여러 검색기의 결과를 하나의 최적화된 랭킹으로 통합합니다.

|Fess| 15.9\ 에서는 시맨틱 검색(콘텐츠 청킹 + 벡터 검색)이 코어 기능으로 제공됩니다. 이를
활성화하면 시맨틱 서처가 자동으로 Rank Fusion에 등록됩니다. 설정 방법은 :doc:`search-semantic`
을 참조하세요.

|Fess| 의 Rank Fusion 기능은 여러 검색 결과를 통합하여
보다 정확한 검색 결과를 제공합니다.

Rank Fusion이란
================

Rank Fusion은 여러 검색 알고리즘이나 스코어링 방법(예: 키워드/BM25 검색과 시맨틱/벡터 검색)의 결과를
결합하여 단일 최적화된 랭킹을 생성하는 기술입니다.

주요 장점:

- 서로 다른 알고리즘의 장점을 결합
- 검색 정확도 향상
- 다양한 검색 결과 제공

지원 알고리즘
==============

|Fess| 에서는 RRF (Reciprocal Rank Fusion) 알고리즘을 지원합니다.

RRF (Reciprocal Rank Fusion)
----------------------------

RRF는 각 검색 결과에서 문서의 순위 역수를 합산하여 스코어를 계산합니다.
여러 검색기(searcher)에서 가져온 문서는 각각의 스코어가 더해집니다.

계산식::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: 순위의 영향도를 조정하는 상수 파라미터 (기본값: 20)
- ``rank(d)``: 각 검색 결과에서 문서 d의 순위 (0부터 시작)
- ``Σ``: 문서 d가 등장한 모든 검색기에 걸친 합계

.. note::

   융합 알고리즘은 RRF로 고정되어 있으며, 다른 알고리즘으로 전환하는 설정은 없습니다.
   또한 검색기별 가중치도 지원하지 않습니다. 각 검색기의 기여도는 동일한 가중치로
   합산됩니다. 랭킹 경향을 조정할 수 있는 것은 ``rank.fusion.rank_constant`` 뿐입니다.

설정
====

fess_config.properties
----------------------

기본 설정::

    # 윈도우 사이즈 (융합 대상 결과 수)
    # 주의: paging.search.page.max.size × 2 이상이어야 합니다.
    # 설정값이 이 최소값보다 작으면 최소값이 자동으로 사용됩니다.
    rank.fusion.window_size=200

    # RRF의 rank_constant (k 파라미터)
    rank.fusion.rank_constant=20

    # 병렬 처리 스레드 수 (0 이하인 경우 availableProcessors × 3 ÷ 2 + 1 이 사용됩니다)
    rank.fusion.threads=-1

    # 스코어 필드명 (융합 후 스코어를 저장하는 필드)
    rank.fusion.score_field=rf_score

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - 프로퍼티
     - 기본값
     - 설명
   * - ``rank.fusion.window_size``
     - ``200``
     - 융합 대상으로 각 검색기에서 가져오는 결과의 최대 건수. ``paging.search.page.max.size × 2`` (기본값은 ``200``) 이상이어야 하며, 작은 값이 설정된 경우 자동으로 최소값으로 올려집니다(시작 시 WARN 로그가 출력됩니다).
   * - ``rank.fusion.rank_constant``
     - ``20``
     - RRF 계산식의 상수 ``k``. 값을 크게 할수록 상위 순위와 하위 순위 간의 스코어 차이가 작아집니다.
   * - ``rank.fusion.threads``
     - ``-1``
     - 여러 검색기를 병렬 실행하는 고정 스레드 풀의 스레드 수. ``0`` 이하를 지정하면 ``availableProcessors × 3 ÷ 2 + 1`` 이 자동으로 사용됩니다(정수 연산이므로 소수점 이하는 버림. 예: 4코어 → 7, 5코어 → 8).
   * - ``rank.fusion.score_field``
     - ``rf_score``
     - 융합 후 스코어를 저장하는 결과 문서의 필드명.

.. note::

   **설정 반영 시점**

   위 4개 설정은 모두 변경 사항을 반영하려면 |Fess|\ 를 재시작해야 합니다.
   ``fess_config.properties`` 에서 읽어들인 값은 JVM 내에 캐시되므로, 가동 중에 파일을
   수정해도 반영되지 않습니다.

   참고로 ``rank.fusion.window_size`` 는 시작 시 한 번만, ``rank.fusion.threads`` 는
   스레드 풀을 생성하는 시점에 읽힙니다. 스레드 풀은 ``default`` 이외의 검색기(시맨틱 서처 등)가
   등록될 때 생성되므로, 시맨틱 검색이 비활성화되어 있으면 스레드 풀 자체가 생성되지 않습니다.

JVM 시스템 프로퍼티
-------------------

사용할 검색기는 JVM 시스템 프로퍼티로 지정합니다.
``fess.in.sh`` 에 다음과 같이 작성합니다::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Drank.fusion.searchers=default,semantic_chunk"

``fess.in.bat`` 의 경우에는 다음과 같이 작성합니다::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Drank.fusion.searchers=default,semantic_chunk

이 프로퍼티의 동작은 다음과 같습니다:

- ``fess_config.properties`` 가 아닌 JVM 옵션으로 설정합니다. 키 이름은
  ``rank.fusion.searchers`` 그 자체를 지정하세요. 다른 설정에서 흔히 사용되는
  ``-Dfess.config.`` 나 ``-Dfess.system.`` 을 붙인 형식(``-Dfess.config.rank.fusion.searchers``
  등)은 인식되지 않습니다.
- JVM 옵션 대신 관리 화면의 "시스템 > 일반"에 있는 "시스템 속성" 칸에
  ``rank.fusion.searchers=default,semantic_chunk`` 와 같이 한 줄로 기술할 수도 있습니다.
  다만 이 칸의 값은 같은 이름의 시스템 프로퍼티가 아직 설정되어 있지 않은 경우에만 적용됩니다.
  따라서 ``-D`` 로 이미 지정되어 있으면 JVM 옵션이 우선하며, 한 번 적용된 값을 변경하려면
  |Fess|\ 를 재시작해야 합니다.
- ``default`` 는 표준 키워드 검색을 수행하는 검색기로 항상 사용할 수 있습니다.
- 검색기 이름은 구현 클래스명에서 끝의 ``Searcher`` 를 제거한 뒤 스네이크 케이스 소문자로 변환한
  형태입니다(``SemanticChunkSearcher`` → ``semantic_chunk``). 코어에 통합된 시맨틱
  서처(:doc:`search-semantic`)는 ``semantic_chunk`` 라는 이름으로 등록됩니다.
- 이 프로퍼티를 지정하지 않으면 등록된 모든 검색기가 사용됩니다. 지정한 이름 중 어느 것도 등록된 검색기와 일치하지 않으면 ``default`` 검색기만 사용됩니다. 코어에 통합된 시맨틱 서처(:doc:`search-semantic`)를 사용하는 경우, 일반적으로는 이 프로퍼티 자체를 설정할 필요가 없습니다.
- Rank Fusion에 의한 결과 융합은 사용 가능한 검색기가 2개 이상인 경우에 실행됩니다. 검색기가 1개뿐인 경우에는 융합이 수행되지 않고 일반 검색 결과가 반환됩니다.

.. warning::

   |Fess| 15.7 이전 버전에서 ``fess-webapp-semantic-search`` 플러그인을 사용하고 있었다면, 이
   프로퍼티를 ``-Drank.fusion.searchers=default,semantic`` 으로 설정하라는 안내를 받았을 수
   있습니다. 그 플러그인은 자신의 검색기를 ``semantic`` 이라는 이름으로 등록했는데, 이는 15.9에서
   도입된 코어 통합 검색기의 이름인 ``semantic_chunk`` 와는 **다른 검색기**\ 입니다. 이 15.7
   시절의 설정을 그대로 15.9로 가져오면 허용 목록에 ``semantic_chunk`` 가 결코 포함되지 않으므로,
   코어에 통합된 시맨틱 검색(콘텐츠 청킹 + 벡터 검색)은 **전혀 동작하지 않습니다** — |Fess|\ 는
   아무런 표시 없이 일반 키워드 검색 결과만 계속 반환합니다(시작 시에는 경고 로그가 남지만,
   요청별 제외 자체는 DEBUG 레벨로만 로그에 남습니다). 설정에 ``default,semantic`` 이 지정되어
   있다면 이 설정을 제거하거나 ``semantic_chunk`` 를 추가하세요. 자세한 내용은
   :doc:`search-semantic` 의 "15.7 이전 버전에서 업그레이드하는 경우의 마이그레이션"을
   참조하세요.

하이브리드 검색과의 연계
==========================

Rank Fusion은 키워드 검색과 시맨틱 검색을 결합한
하이브리드 검색에서 특히 효과적입니다.
시맨틱 검색을 사용하려면 콘텐츠 청킹 기능을 설정한 뒤
``content_chunker.search.enabled=true`` 를 설정하세요.

.. warning::

   ``content_chunker.enabled`` 나 ``content_chunker.search.enabled`` 등
   ``content_chunker.*`` 설정은 ``fess_config.properties`` 가 아니라
   **시스템 프로퍼티**\ 입니다. ``conf/system.properties`` 에 작성하거나
   ``-Dfess.system.content_chunker.search.enabled=true`` 와 같이 JVM 옵션으로
   지정하세요. ``fess_config.properties`` 에 작성해도 반영되지 않습니다.
   또한 ``content_chunker.search.enabled`` 는 시작 시에만 평가되므로
   활성화한 뒤에는 |Fess|\ 를 재시작해야 합니다.

자세한 내용은 :doc:`search-semantic` 을 참조하세요.

융합 결과 확인
===============

Rank Fusion이 실제로 동작하고 있는지는 검색 결과에 부여되는 다음 두 가지 필드로 확인할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 필드
     - 내용
   * - ``searcher``
     - 해당 문서를 가져온 검색기 이름의 배열(예: ``["default", "semantic_chunk"]``). 양쪽이 모두 포함되어 있으면 키워드 검색과 시맨틱 검색 양쪽에서 히트했다는 의미입니다.
   * - ``rf_score``
     - RRF로 산출한 융합 후 스코어. 필드명은 ``rank.fusion.score_field`` 로 변경할 수 있습니다.

둘 다 검색 시 동적으로 부여되는 값이며 인덱스에는 저장되지 않습니다.
또한 기본적으로는 ``/api/v2/search`` 응답에 포함되지 않으므로, 확인하려면
``fess_config.properties`` 에 다음을 설정하고 |Fess|\ 를 재시작하세요::

    query.additional.api.response.fields=rf_score,searcher

.. note::

   ``query.additional.api.response.fields`` 는 v2 검색 API 응답에 포함해도 되는
   필드의 허용 목록에 항목을 추가하는 설정입니다. ``role`` 이나 ``virtual_host`` 등
   접근 제어용 필드를 추가하면 접근 제어 정보가 검색 API 응답에 노출되므로
   추가하지 마세요.

히트 건수에 대한 영향
======================

Rank Fusion이 실행되면 반환되는 총 히트 건수는 메인 검색기(맨 앞에 등록된
``default`` 검색기)의 건수 그대로가 아니라 다음과 같이 보정됩니다::

    총 히트 건수 = 메인 검색기의 총 히트 건수 + 보정값

보정값은 융합 후 상위 ``window_size ÷ 2`` 건 중에서 메인 검색기의 상위
``window_size ÷ 2`` 건에 포함되어 있지 않았던 문서의 건수입니다. 즉, 시맨틱 검색만
찾아낸 문서의 수만큼 건수가 늘어납니다.
그래서 같은 쿼리라도 하이브리드 검색의 활성화 여부에 따라 히트 건수가 달라질 수 있습니다.

또한 메인 검색기의 총 히트 건수가 개략값(하한값)으로 반환되는 경우에는 이 보정이 수행되지 않습니다.

사용 예
========

기본 하이브리드 검색
----------------------

1. 키워드 검색으로 BM25 스코어 계산
2. 시맨틱 검색으로 벡터 유사도 계산
3. RRF로 양쪽 결과를 융합
4. 최종 랭킹 생성

검색 플로우::

    User Query
        ↓
    ┌──────────────────┬──────────────────┐
    │  Keyword Search  │ Semantic Search  │
    │    (BM25)        │  (Vector)        │
    └────────┬─────────┴────────┬─────────┘
             ↓                  ↓
         Rank List 1        Rank List 2
             └────────┬─────────┘
                      ↓
              Rank Fusion (RRF)
                      ↓
              Final Ranking

성능 고려 사항
===============

메모리 사용량
--------------

- 여러 검색 결과를 보유하므로 메모리 사용량이 증가합니다.
- ``rank.fusion.window_size`` 로 융합 대상 최대 건수를 제한할 수 있습니다. 메인 검색기(맨 앞의 ``default`` 검색기)는 최대 ``window_size`` 건, 그 외의 검색기는 각각 ``window_size ÷ 검색기 수`` 건을 가져옵니다(``검색기 수`` 는 메인 검색기를 포함한 총 개수이며, 나눗셈은 버림입니다).
- 예를 들어 검색기가 2개(``default`` 와 ``semantic_chunk``)이고 ``window_size=200`` 인 경우, 메인 검색기가 200건, 시맨틱 서처가 100건을 가져오므로 보유되는 문서는 최대 300건이 됩니다.

::

    # 융합 대상 윈도우 사이즈
    rank.fusion.window_size=200

.. warning::

   ``rank.fusion.window_size`` 는 ``paging.search.page.max.size × 2`` 보다 작을 수 없습니다.
   ``paging.search.page.max.size`` 가 기본값 ``100`` 인 경우 하한은 ``200`` 이 되며, 이는
   ``rank.fusion.window_size`` 의 기본값과 동일합니다. 즉 **기본 구성에서는 window_size 를
   기본값보다 작게 설정할 수 없습니다**. 더 작은 값을 설정해도 시작 시 WARN 로그가 출력되고
   ``200`` 으로 올려집니다. 실제로 더 작게 하려면 ``paging.search.page.max.size`` 를 먼저
   낮춰야 하지만, 이렇게 하면 검색 화면이나 API에서 한 페이지에 요청할 수 있는 최대 건수도
   함께 낮아집니다.

처리 시간
----------

- 여러 검색을 실행하므로 응답 시간이 증가합니다.
- ``rank.fusion.threads`` 로 병렬 실행 스레드 수를 설정합니다.

::

    # 병렬 실행 스레드 수 (0 이하인 경우 availableProcessors × 3 ÷ 2 + 1)
    rank.fusion.threads=-1

.. note::

   검색기 실행에는 타임아웃이 설정되어 있지 않습니다. 응답을 반환하지 않는 검색기가 있으면
   검색 요청은 그 검색기가 완료될 때까지 대기합니다.

검색기 장애 시 동작
====================

검색기 중 하나가 예외로 실패한 경우, 해당 검색기의 결과는 비어 있는 것으로 처리되며
WARN 로그를 출력한 뒤 나머지 검색기의 결과만으로 융합이 계속 진행됩니다.
검색 요청 자체는 오류가 되지 않습니다.

다만 쿼리 구문 오류(``InvalidQueryException``)와 페이징 상한 초과
(``ResultOffsetExceededException``)는 예외이며, 이들은 그대로 오류로 반환됩니다.
또한 융합이 수행되지 않는 깊은 페이지(``시작 위치 × 2`` 가 ``rank.fusion.window_size``
이상이 되는 위치)에서는 메인 검색기에서 발생한 예외가 그대로 검색 요청의 오류가 됩니다.

시맨틱 서처는 임베딩 프로바이더에 연결할 수 없는 경우나 임베딩 처리에 실패한 경우
결과를 비어 있는 상태로 반환합니다. 이 경우에도 오류가 되지 않고 키워드 검색만의 결과가 됩니다.

문제 해결
==========

검색 결과가 기대와 다름
-------------------------

**증상**: Rank Fusion 후 결과가 기대와 다름

**확인 사항**:

1. ``searcher`` 필드를 확인합니다("융합 결과 확인" 참조). 모든 문서가 ``["default"]`` 만
   포함하고 있다면 시맨틱 서처가 결과를 반환하지 않은 것입니다.
2. 시맨틱 검색이 건너뛰어지지 않았는지 확인합니다. 검색 구문(``"`` ``:`` ``AND`` 등)을
   포함하는 쿼리 외에, 라벨·정렬·패싯에 의한 필터링, 위치 정보 검색, 유사 문서 검색에서는
   시맨틱 서처가 결과를 반환하지 않고 키워드 검색만의 결과가 됩니다.
   건너뛰는 조건에 대한 자세한 내용은 :doc:`search-semantic` 을 참조하세요.
3. 각 검색 유형의 결과를 개별적으로 확인
4. ``rank.fusion.rank_constant`` 값을 조정
5. 깊은 페이지(``시작 위치 × 2`` 가 ``rank.fusion.window_size`` 이상이 되는 위치. 기본값에서는
   101번째 이후)에서는 융합이 수행되지 않고 메인 검색기만으로 검색됩니다. 더 많은 페이지에서
   융합 결과를 사용하려면 ``rank.fusion.window_size`` 를 크게 늘려 주세요.

검색이 느림
------------

**증상**: Rank Fusion 활성화 시 검색이 느려짐

**해결 방법**:

1. ``rank.fusion.threads`` 를 조정::

       rank.fusion.threads=4

2. ``rank.fusion.window_size`` 를 줄이기. 다만 하한(``paging.search.page.max.size × 2``)
   보다 작게 할 수 없으므로, 기본 구성에서는 다음 두 가지를 세트로 설정합니다::

       paging.search.page.max.size=50
       rank.fusion.window_size=100

   한 페이지에 요청할 수 있는 최대 건수도 함께 낮아진다는 점에 주의하세요. 설정 후에는 재시작이 필요합니다.

메모리 부족
------------

**증상**: OutOfMemoryError 발생

**해결 방법**:

1. "검색이 느림"과 동일한 절차로 ``rank.fusion.window_size`` 를 줄이기
2. JVM 힙 크기 늘리기

참고 정보
==========

- :doc:`search-semantic` - 시맨틱 검색(콘텐츠 청킹) 설정
- :doc:`scripting-overview` - 스크립팅 개요
- :doc:`search-advanced` - 고급 검색 설정
- :doc:`llm-overview` - LLM 통합 가이드 (시맨틱 검색)
