==================================
Rank Fusion設定
==================================

概要
====

|Fess| のRank Fusion機能は、複数の検索結果を統合して
より精度の高い検索結果を提供します。

Rank Fusionとは
======================

Rank Fusionは、複数の検索アルゴリズムやスコアリング手法の結果を
組み合わせて、単一の最適化されたランキングを生成する技術です。

主な利点：

- 異なるアルゴリズムの長所を組み合わせる
- 検索精度の向上
- 多様な検索結果の提供

対応アルゴリズム
================

|Fess| では以下のRank Fusionアルゴリズムをサポートしています：

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - アルゴリズム
     - 説明
   * - RRF (Reciprocal Rank Fusion)
     - 順位の逆数を使用した融合アルゴリズム
   * - Score Fusion
     - スコアの正規化と加重平均による融合
   * - Borda Count
     - 投票ベースのランキング融合

RRF (Reciprocal Rank Fusion)
----------------------------

RRFは、各結果の順位の逆数を合計してスコアを計算します。

計算式::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: 定数パラメーター（デフォルト: 60）
- ``rank(d)``: ドキュメントdの各検索結果での順位

設定
====

fess_config.properties
----------------------

基本設定::

    # Rank Fusionの有効化
    rank.fusion.enabled=true

    # 使用するアルゴリズム
    rank.fusion.algorithm=rrf

    # RRFのkパラメーター
    rank.fusion.rrf.k=60

    # 融合対象の検索タイプ
    rank.fusion.search.types=keyword,semantic

アルゴリズム別設定
------------------

RRF設定::

    rank.fusion.algorithm=rrf
    rank.fusion.rrf.k=60

Score Fusion設定::

    rank.fusion.algorithm=score
    rank.fusion.score.normalize=true
    rank.fusion.score.weights=0.7,0.3

Borda Count設定::

    rank.fusion.algorithm=borda
    rank.fusion.borda.top_n=100

ハイブリッド検索との連携
========================

Rank Fusionは、キーワード検索とセマンティック検索を組み合わせた
ハイブリッド検索で特に効果を発揮します。

設定例
------

::

    # ハイブリッド検索の有効化
    search.hybrid.enabled=true

    # キーワード検索とセマンティック検索の結果を融合
    rank.fusion.enabled=true
    rank.fusion.algorithm=rrf
    rank.fusion.rrf.k=60

    # 各検索タイプの重み付け
    search.hybrid.keyword.weight=0.6
    search.hybrid.semantic.weight=0.4

使用例
======

基本的なハイブリッド検索
------------------------

1. キーワード検索でBM25スコアを計算
2. セマンティック検索でベクトル類似度を計算
3. RRFで両方の結果を融合
4. 最終的なランキングを生成

検索フロー::

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

カスタムスコアリング
--------------------

複数のスコア要素を組み合わせる例::

    # 基本検索スコア + 日付ブースト + 人気度
    rank.fusion.enabled=true
    rank.fusion.algorithm=score
    rank.fusion.score.factors=relevance,recency,popularity
    rank.fusion.score.weights=0.5,0.3,0.2

パフォーマンス考慮事項
======================

メモリ使用量
------------

- 複数の検索結果を保持するため、メモリ使用量が増加
- ``rank.fusion.max.results`` で融合対象の最大件数を制限

::

    # 融合対象の最大結果数
    rank.fusion.max.results=1000

処理時間
--------

- 複数の検索を実行するため、レスポンス時間が増加
- 並列実行による最適化を検討

::

    # 並列実行の有効化
    rank.fusion.parallel=true
    rank.fusion.thread.pool.size=4

キャッシュ
----------

- 頻繁なクエリに対してはキャッシュを活用

::

    # Rank Fusion結果のキャッシュ
    rank.fusion.cache.enabled=true
    rank.fusion.cache.size=1000
    rank.fusion.cache.expire=300

トラブルシューティング
======================

検索結果が期待と異なる
----------------------

**症状**: Rank Fusion後の結果が期待と異なる

**確認事項**:

1. 各検索タイプの結果を個別に確認
2. 重み付けが適切か確認
3. kパラメーターの値を調整

検索が遅い
----------

**症状**: Rank Fusion有効時に検索が遅くなる

**解決方法**:

1. 並列実行を有効化::

       rank.fusion.parallel=true

2. 融合対象の結果数を制限::

       rank.fusion.max.results=500

3. キャッシュを有効化::

       rank.fusion.cache.enabled=true

メモリ不足
----------

**症状**: OutOfMemoryError が発生する

**解決方法**:

1. 融合対象の最大結果数を減らす
2. JVMヒープサイズを増やす
3. 不要な検索タイプを無効化

参考情報
========

- :doc:`scripting-overview` - スクリプティング概要
- :doc:`../admin/search-settings` - 検索設定ガイド
- :doc:`llm-overview` - LLM統合ガイド（セマンティック検索）
