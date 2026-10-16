==============
検索フォームの配置
==============

検索フォームの配置方法
=================

既存のサイトに検索フォームを配置することで、|Fess| の検索結果に誘導することができます。
ここでは https://search.n2sm.co.jp/ に |Fess| を構築し、既存サイトの各ページに検索フォームを置く例で説明します。

検索フォーム
---------

ページ内で検索フォームを置きたい箇所に以下のコードを配置してください。

::

    <form id="searchForm" method="get" action="https://search.n2sm.co.jp/search/">
    <input id="query" type="text" name="q" maxlength="1000" autocomplete="off">
    <input type="submit" name="search" value="検索">
    </form>

サイトのデザインに合わせて、class属性でクラス名を追加するなどしてCSSで必要に応じて調整してください。
https://search.n2sm.co.jp/ のURLは構築した |Fess| サーバのURLに変更して利用してください。

検索キーワードは ``q`` パラメーターとして |Fess| の検索ページ（ ``/search/`` ）に送信されます。
``maxlength`` には、 |Fess| 側のキーワード長の上限である ``query.max.length`` （初期値は ``1000`` ）に合わせた値を指定してください。


サジェスト
--------

配置した検索フォームにサジェスト機能を設定することもできます。
設定する場合は以下のコードを</body>の前に追加してください。

::

    <script type="text/javascript" src="https://search.n2sm.co.jp/js/jquery-3.7.1.min.js"></script>
    <script type="text/javascript" src="https://search.n2sm.co.jp/js/suggestor.js"></script>
    <script>
    $(function() {
      $('#query').suggestor({
        ajaxinfo : {
          url : 'https://search.n2sm.co.jp/api/v2/suggest-words',
          fn :  ["_default", "content", "title"],
          num : 10
        },
        boxCssInfo: {
          border: "1px solid rgba(82, 168, 236, 0.5)",
          "box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
          "background-color": "#fff",
          "z-index": "10000"
        },
        minterm: 2,
        adjustWidthVal : 11,
        searchForm : $('#searchForm')
      });
    });
    </script>

既にサイトでjQueryを利用している場合はjQueryのscript要素は追加する必要はありません。

サジェストは |Fess| のサジェストAPI（ ``/api/v2/suggest-words`` ）を利用します。
``url`` は構築した |Fess| サーバのURLに合わせて変更してください。

``suggestor`` に指定できる主なオプションは以下のとおりです。

.. list-table:: suggestor の主なオプション
   :header-rows: 1
   :widths: 25 75

   * - オプション
     - 説明
   * - ``ajaxinfo.url``
     - サジェストAPIのURL。 |Fess| サーバの ``/api/v2/suggest-words`` を指定します。
   * - ``ajaxinfo.fn``
     - サジェスト対象とするフィールド名の配列。初期値の ``["_default", "content", "title"]`` のまま利用できます。
   * - ``ajaxinfo.num``
     - 表示する候補の最大件数。
   * - ``ajaxinfo.lang``
     - サジェスト候補を絞り込む言語（省略可能）。
   * - ``minterm``
     - サジェストを開始する最小の入力文字数。
   * - ``adjustWidthVal``
     - サジェスト表示領域の幅を入力欄の幅に加算して調整する値（ピクセル）。
   * - ``searchForm``
     - 候補を選択したときに送信する検索フォームの要素。
   * - ``boxCssInfo``
     - サジェスト表示領域に適用するCSS。
   * - ``listSelectedCssInfo``
     - 選択中の候補に適用するCSS（省略可能）。
   * - ``listDeselectedCssInfo``
     - 非選択の候補に適用するCSS（省略可能）。

"z-index"で指定する値は、他の要素と重ならない値を指定してください。

.. note::
    検索フォームを |Fess| サーバとは異なるドメインのページに配置する場合、サジェストAPIへのリクエストはクロスオリジン通信になります。
    |Fess| は初期設定で ``api.cors.allow.origin=*`` を許可しているため、そのまま利用できます。
    アクセスを制限したい場合は ``fess_config.properties`` の ``api.cors.allow.origin`` を変更してください。

.. note::
    ``/api/v2/suggest-words`` は |Fess| 本体が提供するAPIです。
    以前のバージョンで利用していた ``/api/v1/suggest-words`` は |Fess| 本体からは提供されなくなり、利用するには ``fess-webapp-v1-api`` プラグインのインストールが必要です。
    新規に構築する場合は ``/api/v2/suggest-words`` を利用してください。
