========================================================
Fess で作る Elasticsearch ベースの検索サーバー 〜 API 編
========================================================

はじめに
========

今回は Fess が提供するAPIを利用して、クライアントサイド（ブラウザ側）で検索とその結果の表示を行う方法をご紹介します。
APIを利用することで、既存のウェブシステムにも Fess を検索サーバーとして利用して、HTMLだけの変更で組み込むことも可能になります。

本記事では Fess 13.2.0 を利用して説明します。
Fess の構築方法については\ `導入編 <https://fess.codelibs.org/ja/articles/article-1.html>`__\ を参照してください。

対象読者
========

-  既存のウェブシステムに検索機能を加えたい方

必要な環境
==========

この記事の内容に関しては次の環境で、動作確認を行っています。

-  Google Chrome 76

JSON API
========

Fess は通常のHTMLによる検索表現以外に、APIとしてJSONによる検索結果の応答が可能です。
APIを利用することで、 Fess サーバーを構築しておき、既存のシステムから検索結果だけを問い合わせにいくことも簡単に実現できます。
検索結果を開発言語に依存しない形式で扱えるので、 Fess をJava以外のシステムにも統合しやすいと思います。

Fess の提供しているAPIがどのような応答を返してくるのかについては `JSON応答 <https://fess.codelibs.org/ja/13.2/api/api-search.html>`__ を参照してください。

Fess は内部の検索エンジンとして Elasticsearch を利用しています。
ElasticsearchもJSONによるAPIを提供していますが Fess のAPIは異なるものです。
ElasticsearchのAPIでなく、 Fess のAPIを利用するメリットは、 Fess のAPIを利用することで検索ログの管理や閲覧権限の制御など、様々な Fess 固有の機能を利用できることが挙げられます。
ドキュメントクロールの仕組みをゼロから独自に開発したい場合はElasticsearchを利用するのが良いと思いますが、簡単に検索機能を追加したいということであれば Fess を利用して多くの開発コストを削減できます。

JSON APIを利用した検索サイトの構築
==================================

今回は Fess のAPIを利用したサイトを構築する方法を説明します。
Fess サーバーとのやりとりにはJSON応答を利用します。
今回利用する Fess サーバーは Fess プロジェクトでデモ用として公開している Fess サーバーを利用しています。
もし、独自の Fess サーバーを利用したい場合は Fess 10.0.0以降のバージョンをインストールしてください。

JSONとCORS
-----------

JSONでアクセスする際にはSame-Originポリシーに注意する必要があります。
これにより、ブラウザで表示するHTMLを出力するサーバーと Fess サーバーが同じドメインに存在する場合はJSONを利用することができますが、異なる場合はCORS(Cross-Origin Resource Sharing)を利用する必要があります。
今回はHTMLが置いてあるサーバーと Fess サーバーが異なるドメインにある場合で話を進めます。
FessはCORSに対応しており、設定値はapp/WEB-INF/classes/fess_config.propertiesで設定可能です。 デフォルトでは以下が設定されています。

::

    api.cors.allow.origin=*
    api.cors.allow.methods=GET, POST, OPTIONS, DELETE, PUT
    api.cors.max.age=3600
    api.cors.allow.headers=Origin, Content-Type, Accept, Authorization, X-Requested-With
    api.cors.allow.credentials=true

今回はデフォルトの設定を利用しますが、設定を変更した場合はFessを再起動をしてください。


作成するファイル
----------------

今回はHTML上でJavaScriptを利用して検索処理を実装します。
JavaScriptのライブラリとしてjQueryを利用しています。
作成するファイルは以下のものになります。

-  検索フォームと検索結果を表示するHTMLファイル「index.html」

- Fess サーバーと通信するJSファイル「fess.js」

今回の構築例では以下の機能を実装しています。

-  検索ボタンで検索リクエストの送信

-  検索結果の一覧

-  検索結果のページング処理

HTMLファイルの作成
------------------

まず、検索フォームと検索結果を表示するHTMLを作成します。
今回は理解しやすいようにCSSでデザインを調整などせずにシンプルなタグ構成にしてあります。
利用するHTMLファイルは以下のものになります。

index.htmlの内容
::

    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>検索サイト</title>
    </head>
    <body>
    <div id="header">
      <form id="searchForm">
        <input id="searchQuery" type="text" name="query" size="30"/>
        <input id="searchButton" type="submit" value="検索"/>
        <input id="searchStart" type="hidden" name="start" value="0"/>
        <input id="searchNum" type="hidden" name="num" value="20"/>
      </form>
    </div>
    <div id="subheader"></div>
    <div id="result"></div>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script type="text/javascript" src="fess.js"></script>
    </body>
    </html>

bodyタグ以下を見ていくと、まずはid属性がheaderのdivタグの箇所で、検索入力欄と検索ボタンが配置しています。
また、hiddenフォームで表示開始位置（start）と表示件数（num）を保持しています。
検索リクエスト送信後にJavaScriptでstartとnumの値は更新されます。
ただし、表示件数は1ページあたりの表示件数であり、今回のサンプルコードでは表示件数を変更する機能はないので、numの値は変更されていません。

次のsubheaderのdivタグの箇所で検索にヒットした件数などの情報が表示されます。
resultのdivタグでは検索結果およびページングリンクが表示されます。

最後にjQueryのJSファイルと今回作成した「fess.js」のJavaScriptを読み込みます。
jQueryのJSファイルを「index.html」と同じディレクトリに保存しても構いませんが、今回はGoogleのCDN経由で取得するようにしています。

JSファイルの作成
----------------

次に Fess サーバーと通信し、検索結果を表示するJSファイル「fess.js」を作成します。
以下の内容で「fess.js」を作成して、「index.html」と同じディレクトリに配置します。

fess.jsの内容
::

    $(function(){
        // (1) Fess の URL
        var baseUrl = "http://SERVERNAME:8080/json/?q=";
        // (2) 検索ボタンのjQueryオブジェクト
        var $searchButton = $('#searchButton');

        // (3) 検索処理関数
        var doSearch = function(event){
          // (4) 表示開始位置、表示件数の取得
          var start = parseInt($('#searchStart').val()),
              num = parseInt($('#searchNum').val());
          // 表示開始位置のチェック
          if(start < 0) {
            start = 0;
          }
          // 表示件数のチェック
          if(num < 1 || num > 100) {
            num = 20;
          }
          // (5) 表示ページ情報の取得
          switch(event.data.navi) {
            case -1:
              // 前のページの場合
              start -= num;
              break;
            case 1:
              // 次のページの場合
              start += num;
              break;
            default:
            case 0:
              start = 0;
              break;
          }
          // 検索フィールドの値をトリムして格納
          var searchQuery = $.trim($('#searchQuery').val());
          // (6) 検索フォームが空文字チェック
          if(searchQuery.length != 0) {
            var urlBuf = [];
            // (7) 検索ボタンを無効にする
            $searchButton.attr('disabled', true);
            // (8) URL の構築
            urlBuf.push(baseUrl, encodeURIComponent(searchQuery),
              '&start=', start, '&num=', num);
            // (9) 検索リクエスト送信
            $.ajax({
              url: urlBuf.join(""),
              dataType: 'json',
            }).done(function(data) {
              // 検索結果処理
              var dataResponse = data.response;
              // (10) ステータスチェック
              if(dataResponse.status != 0) {
                alert("検索中に問題が発生しました。管理者にご相談ください。");
                return;
              }

              var $subheader = $('#subheader'),
                  $result = $('#result'),
                  record_count = dataResponse.record_count,
                  offset = 0,
                  buf = [];
              if(record_count == 0) { // (11) 検索結果がない場合
                // サブヘッダー領域に出力
                $subheader[0].innerHTML = "";
                // 結果領域に出力
                buf.push("<b>", dataResponse.q, "</b>に一致する情報は見つかりませんでした。");
                $result[0].innerHTML = buf.join("");
              } else { // (12) 検索にヒットした場合
                var page_number = dataResponse.page_number,
                    startRange = dataResponse.start_record_number,
                    endRange = dataResponse.end_record_number,
                    i = 0,
                    max;
                offset = startRange - 1;
                // (13) サブヘッダーに出力
                buf.push("<b>", dataResponse.q, "</b> の検索結果 ",
                  record_count, " 件中 ", startRange, " - ",
                  endRange, " 件目 (", dataResponse.exec_time,
                    " 秒)");
                $subheader[0].innerHTML = buf.join("");

                // (14) 検索結果領域のクリア
                $result.empty();

                // 検索結果の出力
                var $resultBody = $("<ol/>");
                var results = dataResponse.result;
                for(i = 0, max = results.length; i < max; i++) {
                  buf = [];
                  buf.push('<li><h3 class="title">', '<a href="',
                    results[i].url_link, '">', results[i].title,
                    '</a></h3><div class="body">', results[i].content_description,
                    '<br/><cite>', results[i].site, '</cite></div></li>');
                  $(buf.join("")).appendTo($resultBody);
                }
                $resultBody.appendTo($result);

                // (15) ページ番号情報の出力
                buf = [];
                buf.push('<div id="pageInfo">', page_number, 'ページ目<br/>');
                if(dataResponse.prev_page) {
                  // 前のページへのリンク
                  buf.push('<a id="prevPageLink" href="#">&lt;&lt;前ページへ</a> ');
                }
                if(dataResponse.next_page) {
                  // 次のページへのリンク
                  buf.push('<a id="nextPageLink" href="#">次ページへ&gt;&gt;</a>');
                }
                buf.push('</div>');
                $(buf.join("")).appendTo($result);
              }
              // (16) ページ情報の更新
              $('#searchStart').val(offset);
              $('#searchNum').val(num);
              // (17) ページ表示を上部に移動
              $(document).scrollTop(0);
            }).always(function() {
              // (18) 検索ボタンを有効にする
              $searchButton.attr('disabled', false);
            });
          }
          // (19) サブミットしないので false を返す
          return false;
        };

        // (20) 検索入力欄でEnterキーが押されたときの処理
        $('#searchForm').submit({navi:0}, doSearch);
        // (21) 前ページリンクが押されたときの処理
        $('#result').on("click", "#prevPageLink", {navi:-1}, doSearch)
        // (22) 次ページリンクが押されたときの処理
          .on("click", "#nextPageLink", {navi:1}, doSearch);
      });

「fess.js」の処理はHTMLファイルのDOMが構築された後に実行されます。
まずはじめに、1で 構築した Fess サーバーのURLを指定しています。

2は検索ボタンのjQueryオブジェクトを保存しておきます。
何度か検索ボタンのjQueryオブジェクトを利用するため、変数に保持して再利用します。

3では検索処理関数を定義しています。 この関数の内容は次の節で説明します。

20は検索フォームがサブミットされたときのイベントを登録します。
検索ボタンが押下されたときや検索入力欄でEnterキーが押下されたときに20で登録された処理が実行されます。
イベントが発生したときに検索処理関数doSearchを呼び出します。
naviの値は検索処理関数を呼び出す際に渡され、その値はページング処理をするために利用されます。

21と22でページング処理で追加されるリンクがクリックされたときのイベントを登録します。
これらのリンクは動的に追加されるのでdelegateによりイベントを登録する必要があります。
これらのイベントにおいても20と同様に検索処理関数を呼び出します。

検索処理関数doSearch
--------------------

3の検索処理関数doSearchについて説明します。

4で表示開始位置と表示件数を取得します。
これらの値はheader領域の検索フォームでhiddenの値として保存されています。
表示開始位置は0以上、表示件数は1から100までの値を想定しているので、それ以外の値が取得される場合はデフォルト値を設定します。

5ではdoSearchがイベント登録されたときに渡されたパラメータnaviの値を判定して、表示開始位置を修正します。
ここでは、-1が前のページヘの移動、1が次のページの移動、それ以外は先頭ページへの移動に変更されます。

6は検索入力欄の値が入力されていれば検索を実行し、空であれば何もせずに処理を終了するための判定をします。

7でダブルサブミット防止のために Fess サーバーへ問い合わせ中の間は検索ボタンを無効にします。

8ではAjaxのリクエストを送るためのURLを組み立てます。
1のURLに検索語、表示開始位置、表示件数を結合します。

9でAjaxのリクエストを送信します。
リクエストが正常に返ってくると、successの関数が実行されます。
successの引数には Fess サーバーから返却された検索結果のオブジェクトが渡されます。

まず、10でレスポンスのステータスの内容を確認しています。
正常に検索リクエストが処理された場合は0が設定されています。
Fess のJSON応答の詳細は\ `Fess サイト <https://fess.codelibs.org/ja/13.2/api/api-search.html>`__\ を確認してください。

検索リクエストが正常に処理され、検索結果がヒットしなかった場合は11の条件文内でsubheader領域の内容を空にして、result領域で検索結果がヒットしなかった旨のメッセージを表示します。

検索結果がヒットした場合、12の条件文内では検索結果の処理を行います。
13ではsubheader領域に表示件数や実行時間のメッセージを設定します。
14は検索結果をresult領域に追加していきます。
検索結果はdata.response.resultに配列として格納されています。
results[i].〜でアクセスすることで検索結果ドキュメントのフィールド値を取得することができます。

15で現在表示しているページ番号と、前のページと次のページへのリンクをresult領域に追加します。
16では検索フォームのhiddenに現在の表示開始位置と表示件数を保存します。
表示開始位置と表示件数は次回の検索リクエスト時に再度利用されます。

次に17でページの表示位置を変更します。
次のページヘのリンクをクリックされたときに、ページ自体は更新されないため、scrollTopによりページ先頭に移動します。

18では検索処理が完了後に検索ボタンを有効にします。
リクエストが成功しても失敗しても実行されるようにcompleteで呼ばれるようにします。

19は検索処理関数が呼ばれたあとに、フォームやリンクが送信されないようにfalseを返しています。
これによりページ遷移が発生するのを防ぎます。

実行
----

「index.html」にブラウザでアクセスします。
次のように検索フォームが表示されます。

検索フォーム
|image1|

適当な検索語を入力して、検索ボタンを押下すると検索結果が表示されます。
デフォルトの表示件数は20件ですが、ヒットした検索件数が多い場合には検索結果一覧の下に次のページへのリンクが表示されます。

検索結果
|image2|

まとめ
======

Fess のJSON APIを利用してjQueryベースのクライアント検索サイトを構築してみました。
JSON APIを利用することでブラウザベースのアプリケーションに限らず、別のアプリケーションから呼び出して Fess を利用するシステムも構築できます。

参考資料
========

-  `Fess <https://fess.codelibs.org/ja/>`__

-  `jQuery <http://jquery.com/>`__

.. |image0| image:: ../../resources/images/ja/article/4/sameorigin.png
.. |image1| image:: ../../resources/images/ja/article/4/searchform.png
.. |image2| image:: ../../resources/images/ja/article/4/searchresult.png
