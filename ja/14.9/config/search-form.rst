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


サジェスト
--------

配置した検索フォームにサジェスト機能を設定することもできます。
設定する場合は以下のコードを</body>の前に追加してください。

::

    <script type="text/javascript" src="https://search.n2sm.co.jp/js/jquery-3.4.1.min.js"></script>
    <script type="text/javascript" src="https://search.n2sm.co.jp/js/suggestor.js"></script>
    <script>
    $(function() {
      $('#query').suggestor({
        ajaxinfo : {
          url : 'https://search.n2sm.co.jp/suggest',
          fn : '_default,content,title',
          num : 10
        },
        boxCssInfo: {
          border: "1px solid rgba(82, 168, 236, 0.5)",
          "-webkit-box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
          "-moz-box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
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

"z-index"で指定する値は、他の要素と重ならない値を指定してください。
