==================
検索フォームの配置
==================

検索フォームの配置方法
======================

既存のサイトに検索フォームを配置することで、|Fess| の検索結果に誘導することができます。
ここでは https://search.n2sm.co.jp/ に |Fess| を構築し、既存サイトの各ページに検索フォームを置く例で説明します。

検索フォーム
------------

ページ内で検索フォームを置きたい箇所に以下のコードを配置してください。

::

    <form id="searchForm" method="get" action="https://search.n2sm.co.jp//search/">
    <input id="query" type="text" name="q" maxlength="1000" autocomplete="off">
    <input type="submit" name="search" value="検索">
    </form>

サイトのデザインに合わせて、class属性でクラス名を追加するなどしてCSSで必要に応じて調整してください。
https://search.n2sm.co.jp/ のURLは構築した |Fess| サーバのURLに変更して利用してください。


サジェスト
---------

配置した検索フォームにサジェスト機能を設定することもできます。
設定する場合は以下のコードを</body>の前に追加してください。

::

    <script type="text/javascript" src="https://search.n2sm.co.jp/js/jquery-2.2.4.min.js"></script>
    <script type="text/javascript" src="https://search.n2sm.co.jp/js/suggestor.js"></script>
    <script>
    $(function() {
      $('#query').suggestor({
        ajaxinfo : {
          url : 'https://search.n2sm.co.jp/suggest',
          fn : '_default,content,title',
          num : 10
        },
        minturm: 2,
        adjustWidthVal : 11,
        searchForm : $('#searchForm')
      });
    });
    </script>

既にサイトでjQueryを利用している場合はjQueryのscript要素は追加する必要はありません。


