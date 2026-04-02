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

RRF는 각 결과의 순위 역수를 합산하여 스코어를 계산합니다.

계산식::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: 상수 파라미터 (기본값: 20)
- ``rank(d)``: 각 검색 결과에서 문서 d의 순위

설정
====

fess_config.properties
----------------------

기본 설정::

    # 윈도우 사이즈 (융합 대상 결과 수)
    rank.fusion.window_size=200

    # RRF의 rank_constant (k 파라미터)
    rank.fusion.rank_constant=20

    # 병렬 처리 스레드 수 (-1은 기본값)
    rank.fusion.threads=-1

    # 스코어 필드명
    rank.fusion.score_field=rf_score

하이브리드 검색과의 연계
==========================

Rank Fusion은 키워드 검색과 시맨틱 검색을 결합한
하이브리드 검색에서 특히 효과적입니다.

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

- 여러 검색 결과를 보유하므로 메모리 사용량이 증가
- ``rank.fusion.window_size`` 로 융합 대상 최대 건수를 제한

::

    # 융합 대상 윈도우 사이즈
    rank.fusion.window_size=200

처리 시간
----------

- 여러 검색을 실행하므로 응답 시간이 증가
- ``rank.fusion.threads`` 로 병렬 실행 스레드 수를 설정

::

    # 병렬 실행 스레드 수 (-1은 기본값)
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
