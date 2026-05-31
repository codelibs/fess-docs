========
APIの概要
========


|Fess| の提供するAPI
==================

このドキュメントでは、 |Fess| が提供する Web API (v2) について説明します。
APIを利用することで、既存のウェブシステムやシングルページアプリケーション (SPA) などからも、 |Fess| を検索サーバーとして利用できます。

.. note::

   |Fess| 15.7 では、API が **v2** に刷新されました。従来の ``/api/v1`` の
   JSON 検索 API およびチャット API は廃止され、 ``/api/v2`` に統合されています。
   ``/api/v1`` を利用していたクライアントは ``/api/v2`` へ移行してください。

ベースURL
========

|Fess| の v2 API エンドポイントは以下のベースURLで提供されます。

::

    http://<Server Name>/api/v2/

例えば、ローカル環境で動作している場合は次のようになります。

::

    http://localhost:8080/api/v2/

レスポンスエンベロープ
==================

v2 のすべての JSON レスポンスは、共通のエンベロープ構造で返されます。

::

    {
      "response": {
        "status": 0,
        ...
      }
    }

``response.status`` は処理結果を表し、v1 の規約を踏襲しています。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: status の値

   * - 0
     - 成功
   * - 1
     - クライアントエラー
   * - 9
     - システムエラー

表: status の値

なお、 ``response.status >= 1`` であることと HTTP ステータスコードが ``400`` 以上であることは常に一致します。

フィールド名
----------

リクエストボディ・レスポンスボディ・SSE イベントデータを含め、すべての JSON のキーは ``snake_case`` で統一されています。

エラーレスポンス
==============

エラー時には、エンベロープに ``error`` オブジェクトが追加されます。

::

    {
      "response": {
        "status": 1,
        "error": {
          "code": "invalid_request",
          "message": "..."
        }
      }
    }

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: error の要素

   * - code
     - 安定したエラーコード（ ``snake_case`` ）。クライアントはこの値を基にローカライズすることを推奨します。
   * - message
     - 人間が読めるエラーメッセージ（英語）。表示の際はクライアント側で ``code`` を基にローカライズしてください。

表: error の要素

エラーコードと HTTP ステータスコード
-------------------------------

``error.code`` に応じて、既定の HTTP ステータスコードが決まります。

.. tabularcolumns:: |p{5cm}|p{3cm}|p{7cm}|
.. list-table:: エラーコード一覧

   * - error.code
     - HTTPステータス
     - 説明
   * - ``invalid_request``
     - 400
     - リクエストが不正です。
   * - ``auth_required``
     - 401
     - 認証が必要、または認証情報が不正です。
   * - ``forbidden``
     - 403
     - 許可されていません（CSRF トークンの欠落・失効など）。
   * - ``not_found``
     - 404
     - リソースが見つかりません。
   * - ``method_not_allowed``
     - 405
     - HTTP メソッドが許可されていません。 ``Allow`` ヘッダーに対応メソッドが列挙されます。
   * - ``not_acceptable``
     - 406
     - 受理できないリクエストです。
   * - ``conflict``
     - 409
     - リソースの競合が発生しました。
   * - ``payload_too_large``
     - 413
     - リクエストボディがサイズ上限を超えています。
   * - ``unsupported_media_type``
     - 415
     - サポートされていない ``Content-Type`` です（多くのエンドポイントは ``application/json`` を要求します）。
   * - ``rate_limited``
     - 429
     - レート制限を超えました。 ``Retry-After`` ヘッダーに待機すべき秒数が示されます。
   * - ``internal_error``
     - 500
     - サーバー内部でエラーが発生しました。
   * - ``service_unavailable``
     - 503
     - サービスを一時的に利用できません。

表: エラーコード一覧

.. note::

   ``method_not_allowed`` のレスポンスには、対応する HTTP メソッドを列挙した
   ``Allow`` ヘッダーが付与されます。

認証とセッション
==============

v2 API はセッションベースの認証を採用しています。
ログインは ``POST /auth/login`` で行い、成功するとセッションが確立され、CSRF トークンが発行されます。
現在の認証状態は ``GET /auth/me`` で確認できます。詳細は :doc:`api-auth` を参照してください。

ログインが不要な検索などのエンドポイントは、匿名のまま利用できます（ ``app.login.required`` などの設定に依存します）。

CSRF トークン
-----------

状態を変更するリクエスト（ ``POST`` / ``PUT`` / ``DELETE`` ）には、 ``X-Fess-CSRF-Token`` ヘッダーが必要です。
CSRF トークンは以下の方法で取得できます。

- ``POST /auth/login`` のレスポンスの ``csrf_token`` フィールド
- ``GET /ui/config`` のレスポンス（ ``csrf_required=true`` の場合の ``csrf_token`` フィールド）

トークンは、ログイン・ログアウト・パスワード変更のたびにローテーションされます。

.. note::

   CSRF の検証は認証よりも **先** に行われます。そのため、セッションも有効な
   CSRF トークンも持たない状態変更リクエストは、 ``401 auth_required`` ではなく
   ``403 forbidden`` を受け取ります。 ``/auth/login`` はログイン前にトークンが
   存在しないため、CSRF 検証の対象外です。

ストリーミング形式
==============

一部のエンドポイントは、通常の JSON ではなくストリーミング形式でレスポンスを返します。

.. tabularcolumns:: |p{4cm}|p{4cm}|p{7cm}|
.. list-table:: ストリーミング形式

   * - エンドポイント
     - Content-Type
     - 説明
   * - ``/chat/stream``
     - ``text/event-stream``
     - Server-Sent Events (SSE)。詳細は :doc:`api-chat` を参照してください。
   * - ``/documents/all``
     - ``application/x-ndjson``
     - NDJSON（各行が ``{"data":{...}}`` 形式の1ドキュメント。ストリーム途中で失敗した場合のみ、最終行が ``{"error":{...}}`` になります）。詳細は :doc:`api-search` を参照してください。

表: ストリーミング形式

APIの種類
========

|Fess| は以下の v2 API を提供しています。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - search
     - ドキュメントの検索、ラベル一覧、全件取得（スクロール）を行う API。
   * - suggest
     - サジェストワードを取得する API。
   * - popularword
     - 人気ワードを取得する API。
   * - related
     - 関連クエリ・関連コンテンツを取得する API。
   * - monitor
     - サーバー（検索エンジンクラスター）の状態を取得する API。
   * - auth
     - 認証・セッション操作（ログイン、ログアウト、認証状態取得、パスワード変更）を行う API。
   * - ui
     - SPA 向けの初期設定（UI 設定）を取得する API。
   * - favorite
     - お気に入りドキュメントを操作する API。
   * - click
     - 検索結果のクリックを記録する API。
   * - cache
     - キャッシュされたドキュメント本文を取得する API。
   * - chat
     - AI 検索モード（RAG チャット）機能を利用する API。

表: APIの種類
