==========
UI設定API
==========

概要
====

UI設定APIは、シングルページアプリケーション (SPA) が必要とする初期設定（テーマ、機能フラグ、ページネーション上限、CSRF が必要な場合は新しい CSRF トークン）を返します。
このエンドポイントはログイン前に匿名で呼び出されます。

共通のレスポンスエンベロープおよびエラーモデルについては :doc:`api-overview` を参照してください。

UI設定の取得
==========

リクエスト
--------

==================  ====================================================
HTTPメソッド         GET
エンドポイント        ``/api/v2/ui/config``
==================  ====================================================

SPA が必要とする初期設定を返します。

レスポンス
--------

成功時（HTTP 200, UiConfigResponse）には、以下のような共通エンベロープ形式のレスポンスが返ります（一部抜粋）。

.. code-block:: json

    {
      "response": {
        "status": 0,
        "site_name": "Fess",
        "login_required": false,
        "locales": ["en", "ja"],
        "theme": {
          "name": "default",
          "display_name": "Default Theme",
          "version": "1.0.0",
          "supported_locales": ["en", "ja"]
        },
        "features": {
          "user_favorite": false,
          "popular_word": true,
          "suggest_search_log": true,
          "suggest_documents": true,
          "login_required": false,
          "eoled": false,
          "development_mode": false,
          "search_log_enabled": true,
          "thumbnail_enabled": true,
          "display_label_type": false,
          "clipboard_copy_icon": true,
          "eol_link": "",
          "installation_link": "https://fess.codelibs.org/15.7/install/",
          "login_link": true,
          "rag_chat_enabled": false
        },
        "page_size_default": 20,
        "page_size_max": 100,
        "sort_options": [
          {"value": "", "label_key": "labels.search_result_sort_score_desc"}
        ],
        "num_options": [10, 20, 30, 40, 50, 100],
        "lang_options": [
          {"value": "all", "label_key": "labels.searchoptions_all_langs"},
          {"value": "ja", "label_key": "labels.lang_ja"}
        ],
        "label_options": [],
        "notifications": {
          "search_top": "",
          "advance_search": "",
          "login": ""
        },
        "facet_views": [],
        "filetype_options": [
          {"value": "html", "label_key": "labels.facet_filetype_html"}
        ],
        "csrf_required": true,
        "csrf_token": "0c1f2e3d4a5b6c7d8e9f"
      }
    }

``response`` の各要素については以下の通りです。すべてのフィールドは必須です。

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: レスポンス情報
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 型
     - 説明
   * - ``site_name``
     - string
     - サイト名。アクティブなテーマがマニフェストを同梱する場合はその表示名（ ``display_name`` ）、それ以外は ``Fess`` になります。
   * - ``login_required``
     - boolean
     - ログインが必要かどうか。
   * - ``locales``
     - string[]
     - 利用可能なロケールの配列。
   * - ``theme``
     - object
     - アクティブなテーマ記述子。詳細は後述の表を参照してください。
   * - ``features``
     - object
     - 機能フラグ。詳細は後述の表を参照してください。
   * - ``page_size_default``
     - integer
     - デフォルトのページサイズ。
   * - ``page_size_max``
     - integer
     - ページサイズの最大値。
   * - ``sort_options``
     - object[]
     - 検索UI用のソートオプション。詳細は後述の表を参照してください。
   * - ``num_options``
     - integer[]
     - 選択可能なページサイズの配列。 ``page_size_max`` を超えない値に絞られます。
   * - ``lang_options``
     - object[]
     - 言語フィルターのオプション。詳細は後述の表を参照してください。
   * - ``label_options``
     - object[]
     - 設定済みラベルのオプション。詳細は後述の表を参照してください。
   * - ``notifications``
     - object
     - 特定ビューの上部に表示する HTML 通知スニペット。詳細は後述の表を参照してください。
   * - ``facet_views``
     - object[]
     - 設定済みのファセットクエリビューグループ。詳細は後述の表を参照してください。
   * - ``filetype_options``
     - object[]
     - 高度な検索フォーム用のファイルタイプファセットオプション。詳細は後述の表を参照してください。
   * - ``csrf_required``
     - boolean
     - CSRF トークンが必要かどうか。
   * - ``csrf_token``
     - string
     - ``csrf_required`` が ``false`` のとき空文字列、それ以外は現在のセッションに紐づく新しいトークン。

theme
~~~~~

``theme`` は常に存在しますが、リクエストにカスタムテーマが紐づかないときは空オブジェクトになります。
マニフェスト由来のキー（ ``display_name`` / ``version`` / ``supported_locales`` ）は、アクティブなテーマがマニフェストを同梱する場合のみ存在します。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: theme
   :header-rows: 1
   :widths: 28 15 57

   * - フィールド
     - 型
     - 説明
   * - ``name``
     - string
     - テーマ名。
   * - ``display_name``
     - string
     - テーマの表示名。
   * - ``version``
     - string
     - テーマのバージョン。
   * - ``supported_locales``
     - string[]
     - テーマがサポートするロケールの配列。

features
~~~~~~~~

すべてのフィールドが必須です。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: features
   :header-rows: 1
   :widths: 28 15 57

   * - フィールド
     - 型
     - 説明
   * - ``user_favorite``
     - boolean
     - ユーザーお気に入り機能が有効かどうか。
   * - ``popular_word``
     - boolean
     - 人気ワード機能が有効かどうか。
   * - ``suggest_search_log``
     - boolean
     - 検索ログによるサジェストが有効かどうか。
   * - ``suggest_documents``
     - boolean
     - ドキュメントによるサジェストが有効かどうか。
   * - ``login_required``
     - boolean
     - ログインが必要かどうか。
   * - ``eoled``
     - boolean
     - この |Fess| ビルドが EOL に達したかどうか。
   * - ``development_mode``
     - boolean
     - 組み込み（開発用）検索エンジンを使用中のとき ``true`` になります。
   * - ``search_log_enabled``
     - boolean
     - 検索ログが有効かどうか。
   * - ``thumbnail_enabled``
     - boolean
     - サムネイルが有効かどうか。
   * - ``display_label_type``
     - boolean
     - ラベルが1つ以上設定されているとき ``true`` になります。
   * - ``clipboard_copy_icon``
     - boolean
     - クリップボードコピーアイコンを表示するかどうか。
   * - ``eol_link``
     - string
     - 解決済みの EOL 情報 URL。EOL でない、または解決できないときは空文字列です。
   * - ``installation_link``
     - string
     - 解決済みのインストールガイド URL。解決できないときは空文字列です。
   * - ``login_link``
     - boolean
     - ログインリンクを表示すべきかどうか。
   * - ``rag_chat_enabled``
     - boolean
     - RAG チャット機能が利用可能かどうか。

sort_options
~~~~~~~~~~~~

検索UI用のソートオプションの配列です。
各要素は ``value`` と ``label_key`` を持ちます。
``click_count.*`` の項目は検索ログが有効なときのみ、 ``favorite_count.*`` の項目はユーザーお気に入りが有効なときのみ存在します。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: sort_options の要素
   :header-rows: 1
   :widths: 28 15 57

   * - フィールド
     - 型
     - 説明
   * - ``value``
     - string
     - ソート値。
   * - ``label_key``
     - string
     - ラベルキー。

num_options
~~~~~~~~~~~

選択可能なページサイズの整数配列です。 ``page_size_max`` を超えない値に絞られます。

lang_options
~~~~~~~~~~~~

言語フィルターのオプションの配列です。
各要素は ``value`` と ``label_key`` を持ちます。
先頭は ``all`` センチネルで、続いてサポート言語コードごとに1項目が並びます。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: lang_options の要素
   :header-rows: 1
   :widths: 28 15 57

   * - フィールド
     - 型
     - 説明
   * - ``value``
     - string
     - 言語値。
   * - ``label_key``
     - string
     - ラベルキー。

label_options
~~~~~~~~~~~~~

設定済みラベルのオプションの配列です。ラベルが未定義のときは空配列になります。
各要素は ``value`` と ``name`` を持ちます。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: label_options の要素
   :header-rows: 1
   :widths: 28 15 57

   * - フィールド
     - 型
     - 説明
   * - ``value``
     - string
     - ラベル値。
   * - ``name``
     - string
     - ラベル名。

notifications
~~~~~~~~~~~~~

特定ビューの上部に表示する HTML 通知スニペットです。空文字列はそのビューに通知がないことを意味します。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: notifications
   :header-rows: 1
   :widths: 28 15 57

   * - フィールド
     - 型
     - 説明
   * - ``search_top``
     - string
     - 検索トップに表示する通知。
   * - ``advance_search``
     - string
     - 高度な検索に表示する通知。
   * - ``login``
     - string
     - ログインに表示する通知。

facet_views
~~~~~~~~~~~

設定済みのファセットクエリビューグループの配列です。未定義のときは空配列になります。
各要素は ``group_name`` と ``queries`` を持ちます。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: facet_views の要素
   :header-rows: 1
   :widths: 28 15 57

   * - フィールド
     - 型
     - 説明
   * - ``group_name``
     - string
     - グループ名。
   * - ``queries``
     - object[]
     - そのグループのファセットクエリの配列。各要素は ``label_key`` （string）と ``value`` （string）を持ちます。

filetype_options
~~~~~~~~~~~~~~~~

高度な検索フォーム用のファイルタイプファセットオプションの配列です。
各要素は ``value`` と ``label_key`` を持ちます。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: filetype_options の要素
   :header-rows: 1
   :widths: 28 15 57

   * - フィールド
     - 型
     - 説明
   * - ``value``
     - string
     - ファイルタイプ値。
   * - ``label_key``
     - string
     - ラベルキー。

エラーレスポンス
------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: エラーレスポンス
   :header-rows: 1
   :widths: 25 75

   * - ステータスコード
     - 説明
   * - 405 Method Not Allowed
     - サポートされていない HTTP メソッドが指定された場合。
   * - 500 Internal Server Error
     - サーバー内部エラーが発生した場合。
