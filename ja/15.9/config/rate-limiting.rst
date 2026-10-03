==================================
レート制限の設定
==================================

概要
====

|Fess| には、システムの安定性とパフォーマンスを維持するためのレート制限機能があります。
この機能により、過度なリクエストからシステムを保護し、公平なリソース配分を実現できます。

レート制限は以下の場面で適用されます:

- 検索APIやAI検索モードAPIを含む全HTTPリクエスト（``RateLimitFilter``）
- クローラーのリクエスト（クロール設定による制御）

HTTPリクエストのレート制限
==========================

|Fess| へのHTTPリクエスト数をIPアドレス単位で制限できます。
この制限は検索API、AI検索モードAPI、管理画面などすべてのHTTPリクエストに適用されます。

設定
----

``app/WEB-INF/classes/fess_config.properties``:

::

    # レート制限を有効にする（デフォルト: false）
    rate.limit.enabled=true

    # ウィンドウあたりの最大リクエスト数（デフォルト: 100）
    rate.limit.requests.per.window=100

    # ウィンドウサイズ（ミリ秒）（デフォルト: 60000）
    rate.limit.window.ms=60000

動作
----

- レート制限を超えたリクエストは HTTP 429 (Too Many Requests) を返します
- 制限超過によってブロックされているIP、およびブロックIPリストに含まれるIPからのリクエストは HTTP 403 (Forbidden) を返します
- 応答の本文は JSON です（429 は ``{"error":"rate_limit_exceeded",...,"retry_after":60}`` 、403 は ``{"error":"ip_blocked",...}`` ）。429 には ``Retry-After`` ヘッダーが付きます
- 制限はIPアドレス単位で適用されます
- IPごとに最初のリクエストからウィンドウが開始し、ウィンドウ期間経過後にカウントがリセットされます（固定ウィンドウ方式）
- 制限超過時はIPが ``rate.limit.block.duration.ms`` の期間ブロックされます

AI検索モードのレート制限
====================

AI検索モード機能にはLLM APIのコストとリソース消費を制御するためのレート制限があります。
AI検索モードには上記のHTTPリクエストレート制限に加えて、AI検索モード固有のレート制限も設定できます。

AI検索モード固有のレート制限設定については :doc:`rag-chat` を参照してください。

.. note::
   AI検索モードのレート制限は、LLMプロバイダー側のレート制限とは別に適用されます。
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

robots.txtの処理は ``app/WEB-INF/classes/fess_config.properties`` の
``crawler.ignore.robots.txt`` で制御します（デフォルト: ``false``）。
``true`` に設定すると、Crawl-delay を含む robots.txt の処理が無効になります。

::

    # robots.txtを無視する（デフォルト: false）
    crawler.ignore.robots.txt=false

Crawl-delay は接続先（オリジン）ごとに適用され、上限は 60 秒です。待機は URL 単位で行われるため、差分クロールで 1 つの URL に送る HEAD と GET は続けて送信されます。クロール設定の「間隔」は、これとは別に次の URL までの待機時間として働きます。

robots.txt は RFC 9309 に従って解釈されます。 ``Allow:`` と ``Disallow:`` は最も長く一致した規則が優先され、開始 URL も robots.txt で確認されます。robots.txt で拒否された URL は ``fess-crawler.log`` に INFO で記録され、障害 URL には登録されません。

429/503 応答時のバックオフ
--------------------------

サーバーが ``429 Too Many Requests`` または ``503 Service Unavailable`` を返した場合、そのオリジンへのアクセスを一時的に止め、その URL を最大 3 回まで再試行します。待機時間は、 ``Retry-After`` ヘッダーがあればその値、なければ 10 秒から始まる指数関数的な時間（最大 5 分）です。最後の再試行にも失敗すると、 ``fess-crawler.log`` に WARN が出力されます。

robots.txt を取得できない場合
-----------------------------

robots.txt の取得が 5xx、429、タイムアウトなどで失敗した場合、そのオリジンの URL はバックオフが終わるまでキューに戻されます。最初の失敗の後、3 回の再試行にも失敗すると、そのクロールの間はそのオリジンのすべての URL がクロール対象外になり、 ``fess-crawler.log`` に WARN が 1 回出力されます。15.8 以前は、取得できなかった robots.txt はすべて許可として扱われていました。この動作に戻すには、ウェブクロール設定の「設定パラメーター」に次を指定します。

::

    client.robotsTxtAllowOnUnavailable=true

robots.txt の処理そのものを無効にするには、 ``client.robotsTxtEnabled=false`` （クロール設定ごと）または ``crawler.ignore.robots.txt=true`` を使います。

レート制限の全設定項目
======================

``app/WEB-INF/classes/fess_config.properties`` で設定可能なすべてのプロパティです。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rate.limit.enabled``
     - レート制限を有効にする
     - ``false``
   * - ``rate.limit.requests.per.window``
     - ウィンドウあたりの最大リクエスト数
     - ``100``
   * - ``rate.limit.window.ms``
     - ウィンドウサイズ（ミリ秒）
     - ``60000``
   * - ``rate.limit.block.duration.ms``
     - 制限超過時のIPブロック期間（ミリ秒）
     - ``300000``
   * - ``rate.limit.retry.after.seconds``
     - Retry-Afterヘッダー値（秒）
     - ``60``
   * - ``rate.limit.whitelist.ips``
     - レート制限から除外するIPアドレス（カンマ区切り）
     - ``127.0.0.1,::1``
   * - ``rate.limit.blocked.ips``
     - ブロックするIPアドレス（カンマ区切り）
     - （空）
   * - ``rate.limit.trusted.proxies``
     - 信頼するプロキシIP（X-Forwarded-For/X-Real-IPの取得元）
     - ``127.0.0.1,::1``
   * - ``rate.limit.cleanup.interval``
     - クリーンアップ間隔（リクエスト数、予約済み）
     - ``1000``

.. note::
   ``rate.limit.cleanup.interval`` は将来の拡張のために予約されている設定項目です。
   現在の実装では、リクエストカウンターおよびブロックIPの情報は内部キャッシュの
   有効期限（``rate.limit.window.ms`` および ``rate.limit.block.duration.ms``）に
   基づいて自動的にクリーンアップされるため、この設定値は使用されません。

高度なレート制限設定
====================

カスタムレート制限
------------------

特定の条件に基づいて異なるレート制限ロジックを適用する場合は、
カスタムコンポーネントの実装が必要です。

::

    // RateLimitHelperのカスタマイズ例
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean allowRequest(String ip) {
            // カスタムロジック
        }
    }

除外設定
========

特定のIPアドレスをレート制限から除外したり、ブロックしたりできます。

::

    # ホワイトリストIP（レート制限から除外、カンマ区切り）
    rate.limit.whitelist.ips=127.0.0.1,::1,192.168.1.100

    # ブロックIPリスト（常にブロック、カンマ区切り）
    rate.limit.blocked.ips=203.0.113.50

    # 信頼するプロキシIP（カンマ区切り）
    rate.limit.trusted.proxies=127.0.0.1,::1

.. note::
   リバースプロキシを使用している場合は、``rate.limit.trusted.proxies`` に
   プロキシのIPアドレスを設定してください。信頼するプロキシからのリクエストのみ、
   X-Forwarded-ForおよびX-Real-IPヘッダーからクライアントIPを取得します。

監視とアラート
==============

レート制限の状況を監視するための設定:

ログ出力
--------

レート制限が適用された場合、ログに記録されます:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

トラブルシューティング
======================

正当なリクエストがブロックされる
--------------------------------

**原因**: 制限値が厳しすぎる

**解決方法**:

1. ``rate.limit.requests.per.window`` を増やす
2. 特定のIPをホワイトリストに追加（``rate.limit.whitelist.ips``）
3. ウィンドウサイズ（``rate.limit.window.ms``）を調整

レート制限が効かない
--------------------

**原因**: 設定が正しく反映されていない

**確認事項**:

1. ``rate.limit.enabled=true`` が設定されているか
2. 設定ファイルが正しく読み込まれているか
3. |Fess| を再起動したか

パフォーマンスへの影響
----------------------

レート制限のチェック自体がパフォーマンスに影響する場合:

1. ホワイトリストを活用して信頼できるIPのチェックをスキップ
2. レート制限を無効にする（``rate.limit.enabled=false``）

参考情報
========

- :doc:`rag-chat` - AI検索モード機能の設定
- :doc:`../admin/webconfig-guide` - Webクロール設定ガイド
- :doc:`../api/api-overview` - API概要
