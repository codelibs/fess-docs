==================================
レート制限の設定
==================================

概要
====

|Fess| には、システムの安定性とパフォーマンスを維持するためのレート制限機能があります。
この機能により、過度なリクエストからシステムを保護し、公平なリソース配分を実現できます。

レート制限は以下の場面で適用されます:

- 検索API
- RAGチャットAPI
- クローラーのリクエスト

検索APIのレート制限
===================

検索APIへのリクエスト数を制限できます。

設定
----

``app/WEB-INF/conf/system.properties``:

::

    # レート制限を有効にする
    api.rate.limit.enabled=true

    # IPアドレスごとの1分あたりの最大リクエスト数
    api.rate.limit.requests.per.minute=60

    # レート制限のウィンドウサイズ（秒）
    api.rate.limit.window.seconds=60

動作
----

- レート制限を超えたリクエストは HTTP 429 (Too Many Requests) を返します
- 制限はIPアドレス単位で適用されます
- 制限値はスライディングウィンドウ方式でカウントされます

RAGチャットのレート制限
=======================

RAGチャット機能にはLLM APIのコストとリソース消費を制御するためのレート制限があります。

設定
----

``app/WEB-INF/conf/system.properties``:

::

    # チャットのレート制限を有効にする
    rag.chat.rate.limit.enabled=true

    # 1分あたりの最大リクエスト数
    rag.chat.rate.limit.requests.per.minute=10

.. note::
   RAGチャットのレート制限は、LLMプロバイダー側のレート制限とは別に適用されます。
   両方の制限を考慮して設定してください。

クローラーのレート制限
======================

クローラーがターゲットサイトに過度な負荷をかけないよう、リクエスト間隔を設定できます。

Webクロール設定
---------------

管理画面の「クローラー」→「ウェブ」で以下を設定:

- **リクエスト間隔**: リクエスト間の待機時間（ミリ秒）
- **スレッド数**: 並列クロールスレッド数

推奨設定:

::

    # 一般的なサイト
    intervalTime=1000
    numOfThread=1

    # 大規模サイト（許可がある場合）
    intervalTime=500
    numOfThread=3

robots.txtの尊重
----------------

|Fess| はデフォルトでrobots.txtのCrawl-delay指示を尊重します。

::

    # robots.txtの例
    User-agent: *
    Crawl-delay: 10

高度なレート制限設定
====================

カスタムレート制限
------------------

特定のユーザーやロールに対して異なる制限を適用する場合は、
カスタムコンポーネントの実装が必要です。

::

    // RateLimitHelperのカスタマイズ例
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean isAllowed(String key) {
            // カスタムロジック
        }
    }

バースト制限
------------

短時間の突発的なリクエストを許容しつつ、継続的な高負荷を防ぐ設定:

::

    # バースト許容量
    api.rate.limit.burst.size=20

    # 持続的な制限
    api.rate.limit.sustained.requests.per.second=1

除外設定
========

特定のIPアドレスやユーザーをレート制限から除外できます。

::

    # 除外IPアドレス（カンマ区切り）
    api.rate.limit.excluded.ips=192.168.1.100,10.0.0.0/8

    # 除外ロール
    api.rate.limit.excluded.roles=admin

監視とアラート
==============

レート制限の状況を監視するための設定:

ログ出力
--------

レート制限が適用された場合、ログに記録されます:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

メトリクス
----------

レート制限に関するメトリクスは、システム統計APIで取得できます:

::

    GET /api/admin/stats

トラブルシューティング
======================

正当なリクエストがブロックされる
--------------------------------

**原因**: 制限値が厳しすぎる

**解決方法**:

1. ``requests.per.minute`` を増やす
2. 特定のIPを除外リストに追加
3. ウィンドウサイズを調整

レート制限が効かない
--------------------

**原因**: 設定が正しく反映されていない

**確認事項**:

1. ``api.rate.limit.enabled=true`` が設定されているか
2. 設定ファイルが正しく読み込まれているか
3. |Fess| を再起動したか

パフォーマンスへの影響
----------------------

レート制限のチェック自体がパフォーマンスに影響する場合:

1. レート制限のストレージをRedisなどに変更
2. チェック頻度を調整

参考情報
========

- :doc:`rag-chat` - RAGチャット機能の設定
- :doc:`../admin/webconfig-guide` - Webクロール設定ガイド
- :doc:`../api/api-overview` - API概要
