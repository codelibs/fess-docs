==============================
バング検索（別のサイトで検索）
==============================

バング(bang)は、|Fess| で検索する代わりに、別のサイトへ検索を送る機能です。DuckDuckGo のバングと同じ使い方で、検索語に ``!`` と短いトリガー語を加えると、|Fess| は残りの検索語をそのトリガー語が表すサイトへ送ります。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 検索語
     - 送り先
   * - ``airplane !g``
     - Google で ``airplane`` を検索
   * - ``!w Ohm's law``
     - Wikipedia で ``Ohm's law`` を検索
   * - ``!g``
     - Google のトップページ
   * - ``airplane !unknown``
     - |Fess| での通常の検索(``!`` は NOT の意味です。:doc:`search-not` を参照)

バングは ``fess-webapp-bangs`` プラグインが提供します。|Fess| 15.10 以降が必要です。管理画面の [システム > プラグイン] か ``bin/fess-setup install plugin fess-webapp-bangs`` でインストールし(:doc:`../admin/plugin-guide` を参照)、|Fess| を再起動します。

バングとして扱われる条件
========================

- バングは ``!`` にトリガー語を続けたもので、独立した単語として記述します。トリガー語は大文字・小文字を区別しません。
- バングは検索語から取り除かれ、残りの検索語がバングの URL に送られます。
- 定義済みのバングが検索語に複数含まれる場合は、最初の 1 つだけが有効です。
- 定義されていないトリガー語はバングではありません。``!unknown`` は通常どおり検索され、単語 ``unknown`` を除外します。
- ``-g`` や ``NOT g`` はこれまでどおり単語 ``g`` を除外します。バングになるのは ``!g`` だけです。

検索画面と ``/api/v2/search`` はリダイレクトに対応しています。API は ``redirect_url`` を返し(:doc:`../api/api-search` を参照)、|Fess| に同梱の ``bootstrap`` テーマはその URL へ移動します。ほかのテーマでは同様の処理が必要です。

チャット、MCP、v1 API・クラシック JSON API、管理画面の検索など、リダイレクトできない呼び出し元では、別サイトへ検索を送りません。バングを取り除き、残りの検索語で検索します。

バングの定義
============

バングはシステムプロパティ ``bangs.definitions`` で定義します。``app/WEB-INF/conf/system.properties`` に記述するか、``-Dfess.system.bangs.definitions=...`` として渡します。``system.properties`` の変更は、|Fess| を再起動しなくても反映されます。

値は ``トリガー語=URL`` の空白区切りのリストです。URL の中の ``{query}`` は、URL エンコードした残りの検索語に置き換えられます。

::

    bangs.definitions=g=https://www.google.com/search?q={query} w=https://en.wikipedia.org/wiki/Special:Search?search={query}

- トリガー語には、空白、``(``、``)``、``!``、``"``、``=``、``:`` を含められません。
- 受け付けるのは、絶対 URL の ``http`` または ``https`` だけです。
- この規則に合わない項目は使われません。|Fess| のログに警告が出力され、ほかの項目は有効なままです。
- 同じトリガー語を 2 回定義した場合は、最初の定義が使われます。
- 値を空にすると、すべてのバングが無効になります。

``bangs.definitions`` を設定していない場合は、次の 5 つのバングが使えます。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - トリガー語
     - サイト
   * - ``g``
     - Google
   * - ``b``
     - Bing
   * - ``ddg``
     - DuckDuckGo
   * - ``w``
     - Wikipedia(英語)
   * - ``gh``
     - GitHub

``bangs.definitions`` を設定すると、この一覧は置き換わります。既定のバングを残したまま 1 つ足したい場合は、必要な項目をすべて記述してください。

関連項目
========

- :doc:`search-not` - NOT 検索の書き方
- :doc:`special-char` - 特殊文字とエスケープ
- :doc:`../api/api-search` - 検索 API
