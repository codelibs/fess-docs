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

|Fess| 에서는 다음 Rank Fusion 알고리즘을 지원합니다:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 알고리즘
     - 설명
   * - RRF (Reciprocal Rank Fusion)
     - 순위의 역수를 사용한 융합 알고리즘
   * - Score Fusion
     - 스코어 정규화 및 가중 평균에 의한 융합
   * - Borda Count
     - 투표 기반 랭킹 융합

RRF (Reciprocal Rank Fusion)
----------------------------

RRF는 각 결과의 순위 역수를 합산하여 스코어를 계산합니다.

계산식::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: 상수 파라미터 (기본값: 60)
- ``rank(d)``: 각 검색 결과에서 문서 d의 순위

설정
====

fess_config.properties
----------------------

기본 설정::

    # Rank Fusion 활성화
    rank.fusion.enabled=true

    # 사용할 알고리즘
    rank.fusion.algorithm=rrf

    # RRF의 k 파라미터
    rank.fusion.rrf.k=60

    # 융합 대상 검색 유형
    rank.fusion.search.types=keyword,semantic

알고리즘별 설정
----------------

RRF 설정::

    rank.fusion.algorithm=rrf
    rank.fusion.rrf.k=60

Score Fusion 설정::

    rank.fusion.algorithm=score
    rank.fusion.score.normalize=true
    rank.fusion.score.weights=0.7,0.3

Borda Count 설정::

    rank.fusion.algorithm=borda
    rank.fusion.borda.top_n=100

하이브리드 검색과의 연계
==========================

Rank Fusion은 키워드 검색과 시맨틱 검색을 결합한
하이브리드 검색에서 특히 효과적입니다.

설정 예
--------

::

    # 하이브리드 검색 활성화
    search.hybrid.enabled=true

    # 키워드 검색과 시맨틱 검색 결과를 융합
    rank.fusion.enabled=true
    rank.fusion.algorithm=rrf
    rank.fusion.rrf.k=60

    # 각 검색 유형의 가중치
    search.hybrid.keyword.weight=0.6
    search.hybrid.semantic.weight=0.4

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

커스텀 스코어링
-----------------

여러 스코어 요소를 결합하는 예::

    # 기본 검색 스코어 + 날짜 부스트 + 인기도
    rank.fusion.enabled=true
    rank.fusion.algorithm=score
    rank.fusion.score.factors=relevance,recency,popularity
    rank.fusion.score.weights=0.5,0.3,0.2

성능 고려 사항
===============

메모리 사용량
--------------

- 여러 검색 결과를 보유하므로 메모리 사용량이 증가
- ``rank.fusion.max.results`` 로 융합 대상 최대 건수를 제한

::

    # 융합 대상 최대 결과 수
    rank.fusion.max.results=1000

처리 시간
----------

- 여러 검색을 실행하므로 응답 시간이 증가
- 병렬 실행으로 최적화 고려

::

    # 병렬 실행 활성화
    rank.fusion.parallel=true
    rank.fusion.thread.pool.size=4

캐시
------

- 빈번한 쿼리에 대해 캐시를 활용

::

    # Rank Fusion 결과 캐시
    rank.fusion.cache.enabled=true
    rank.fusion.cache.size=1000
    rank.fusion.cache.expire=300

문제 해결
==========

검색 결과가 기대와 다름
-------------------------

**증상**: Rank Fusion 후 결과가 기대와 다름

**확인 사항**:

1. 각 검색 유형의 결과를 개별적으로 확인
2. 가중치가 적절한지 확인
3. k 파라미터 값을 조정

검색이 느림
------------

**증상**: Rank Fusion 활성화 시 검색이 느려짐

**해결 방법**:

1. 병렬 실행 활성화::

       rank.fusion.parallel=true

2. 융합 대상 결과 수 제한::

       rank.fusion.max.results=500

3. 캐시 활성화::

       rank.fusion.cache.enabled=true

메모리 부족
------------

**증상**: OutOfMemoryError 발생

**해결 방법**:

1. 융합 대상 최대 결과 수 줄이기
2. JVM 힙 크기 늘리기
3. 불필요한 검색 유형 비활성화

참고 정보
==========

- :doc:`scripting-overview` - 스크립팅 개요
- :doc:`../admin/search-settings` - 검색 설정 가이드
- :doc:`llm-overview` - LLM 통합 가이드 (시맨틱 검색)
