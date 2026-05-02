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

|Fess| ではRRF（Reciprocal Rank Fusion）アルゴリズムをサポートしています。

RRF (Reciprocal Rank Fusion)
----------------------------

RRFは、各結果の順位の逆数を合計してスコアを計算します。

計算式::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: 定数パラメーター（デフォルト: 20）
- ``rank(d)``: ドキュメントdの各検索結果での順位（0始まり）

設定
====

fess_config.properties
----------------------

基本設定::

    # ウィンドウサイズ（融合対象の結果数）
    # 注: paging.search.page.max.size × 2 以上である必要があります。
    # 設定値がこの最小値を下回る場合、最小値が自動的に使用されます。
    rank.fusion.window_size=200

    # RRFのrank_constant（kパラメーター）
    rank.fusion.rank_constant=20

    # 並列処理のスレッド数（-1の場合、availableProcessors * 1.5 + 1）
    rank.fusion.threads=-1

    # スコアフィールド名
    rank.fusion.score_field=rf_score

JVMシステムプロパティ
---------------------

以下のプロパティは ``fess.in.sh`` (または ``fess.in.bat``) でJVMオプションとして設定します::

    # 使用するサーチャーの指定（カンマ区切り）
    -Drank.fusion.searchers=default,semantic

ハイブリッド検索との連携
========================

Rank Fusionは、キーワード検索とセマンティック検索を組み合わせた
ハイブリッド検索で特に効果を発揮します。

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

パフォーマンス考慮事項
======================

メモリ使用量
------------

- 複数の検索結果を保持するため、メモリ使用量が増加
- ``rank.fusion.window_size`` で融合対象の最大件数を制限

::

    # 融合対象のウィンドウサイズ
    rank.fusion.window_size=200

処理時間
--------

- 複数の検索を実行するため、レスポンス時間が増加
- ``rank.fusion.threads`` で並列実行のスレッド数を設定

::

    # 並列実行のスレッド数（-1の場合、availableProcessors * 1.5 + 1）
    rank.fusion.threads=-1

トラブルシューティング
======================

検索結果が期待と異なる
----------------------

**症状**: Rank Fusion後の結果が期待と異なる

**確認事項**:

1. 各検索タイプの結果を個別に確認
2. ``rank.fusion.rank_constant`` の値を調整
3. ``rank.fusion.window_size`` の値を調整

検索が遅い
----------

**症状**: Rank Fusion有効時に検索が遅くなる

**解決方法**:

1. ``rank.fusion.window_size`` を減らす::

       rank.fusion.window_size=100

2. ``rank.fusion.threads`` を調整::

       rank.fusion.threads=4

メモリ不足
----------

**症状**: OutOfMemoryError が発生する

**解決方法**:

1. ``rank.fusion.window_size`` を減らす
2. JVMヒープサイズを増やす

参考情報
========

- :doc:`scripting-overview` - スクリプティング概要
- :doc:`search-advanced` - 検索の詳細設定
- :doc:`llm-overview` - LLM統合ガイド（セマンティック検索）
