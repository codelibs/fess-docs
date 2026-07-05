==================================
Rank Fusion 설정
==================================

개요
====

|Fess| 의 Rank Fusion 기능은 여러 검색 결과를 통합하여
보다 정확한 검색 결과를 제공합니다.

Rank Fusion이란
================

Rank Fusion은 여러 검색 알고리즘이나 스코어링 방법의 결과를
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

    # 병렬 처리 스레드 수 (0 이하인 경우 availableProcessors × 1.5 + 1 이 사용됩니다)
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
     - 융합 대상으로 각 검색기에서 가져오는 결과의 최대 건수. ``paging.search.page.max.size × 2`` (기본값은 ``200``) 이상이어야 하며, 작은 값이 설정된 경우 자동으로 최소값으로 올려집니다.
   * - ``rank.fusion.rank_constant``
     - ``20``
     - RRF 계산식의 상수 ``k``. 값을 크게 할수록 상위 순위와 하위 순위 간의 스코어 차이가 작아집니다.
   * - ``rank.fusion.threads``
     - ``-1``
     - 여러 검색기를 병렬 실행할 때의 스레드 수. ``0`` 이하를 지정하면 ``availableProcessors × 1.5 + 1`` 이 자동으로 사용됩니다.
   * - ``rank.fusion.score_field``
     - ``rf_score``
     - 융합 후 스코어를 저장하는 결과 문서의 필드명.

JVM 시스템 프로퍼티
-------------------

사용할 검색기는 JVM 시스템 프로퍼티로 지정합니다.
``fess.in.sh`` (또는 ``fess.in.bat``) 에 다음과 같이 작성합니다::

    # 사용할 검색기 지정 (쉼표 구분)
    -Drank.fusion.searchers=default,semantic

이 프로퍼티의 동작은 다음과 같습니다:

- ``fess_config.properties`` 가 아닌 JVM 옵션으로 설정합니다.
- ``default`` 는 표준 키워드 검색을 수행하는 검색기로 항상 사용할 수 있습니다.
- ``semantic`` 은 시맨틱 검색(벡터 검색)을 수행하는 검색기로, Semantic Search 플러그인(``fess-webapp-semantic-search``)을 도입한 경우에 사용할 수 있습니다.
- 이 프로퍼티를 지정하지 않으면 등록된 모든 검색기가 사용됩니다. 지정한 이름 중 어느 것도 등록된 검색기와 일치하지 않으면 ``default`` 검색기만 사용됩니다.
- Rank Fusion에 의한 결과 융합은 사용 가능한 검색기가 2개 이상인 경우에 실행됩니다. 검색기가 1개뿐인 경우에는 융합이 수행되지 않고 일반 검색 결과가 반환됩니다.

하이브리드 검색과의 연계
==========================

Rank Fusion은 키워드 검색과 시맨틱 검색을 결합한
하이브리드 검색에서 특히 효과적입니다.
시맨틱 검색을 사용하려면 Semantic Search 플러그인(``fess-webapp-semantic-search``)을 도입하고
``-Drank.fusion.searchers`` 에 ``semantic`` 을 추가해야 합니다.

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
- ``rank.fusion.window_size`` 로 융합 대상 최대 건수를 제한할 수 있습니다. 메인 검색기(맨 앞의 ``default`` 검색기)는 최대 ``window_size`` 건, 그 외의 검색기는 각각 ``window_size ÷ 검색기 수`` 건을 가져옵니다.

::

    # 융합 대상 윈도우 사이즈
    rank.fusion.window_size=200

처리 시간
----------

- 여러 검색을 실행하므로 응답 시간이 증가합니다.
- ``rank.fusion.threads`` 로 병렬 실행 스레드 수를 설정합니다.

::

    # 병렬 실행 스레드 수 (0 이하인 경우 availableProcessors × 1.5 + 1)
    rank.fusion.threads=-1

문제 해결
==========

검색 결과가 기대와 다름
-------------------------

**증상**: Rank Fusion 후 결과가 기대와 다름

**확인 사항**:

1. 각 검색 유형의 결과를 개별적으로 확인
2. ``rank.fusion.rank_constant`` 값을 조정
3. ``rank.fusion.window_size`` 값을 조정
4. 깊은 페이지(``시작 위치 × 2`` 가 ``rank.fusion.window_size`` 이상이 되는 위치)에서는 융합이 수행되지 않고 메인 검색기만으로 검색됩니다. 더 많은 페이지에서 융합 결과를 사용하려면 ``rank.fusion.window_size`` 를 크게 늘려 주세요.

검색이 느림
------------

**증상**: Rank Fusion 활성화 시 검색이 느려짐

**해결 방법**:

1. ``rank.fusion.window_size`` 를 줄이기::

       rank.fusion.window_size=100

2. ``rank.fusion.threads`` 를 조정::

       rank.fusion.threads=4

메모리 부족
------------

**증상**: OutOfMemoryError 발생

**해결 방법**:

1. ``rank.fusion.window_size`` 를 줄이기
2. JVM 힙 크기 늘리기

참고 정보
==========

- :doc:`scripting-overview` - 스크립팅 개요
- :doc:`search-advanced` - 고급 검색 설정
- :doc:`llm-overview` - LLM 통합 가이드 (시맨틱 검색)
