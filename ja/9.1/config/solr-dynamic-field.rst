======================
ダイナミックフィールド
======================

Solr のダイナミックフィールド
=============================

Solr
は対象ドキュメントを項目(フィールド)ごとに登録するためにスキーマを定義されています。 |Fess| 
で利用する Solr のスキーマは solr/core1/conf/schema.xml
に定義されています。title や content
など標準のフィールドと、自由にフィールド名を定義できるダイナミックフィールドが定義されています。詳細なパラメータ値については
Solr のドキュメントを参照してください。

利用方法
========

ダイナミックフィールドを利用する場面が多いのはデータベースクロールなどでデータストアクロール設定で登録するなどだと思います。データベースクロールでダイナミックフィールドに登録する方法は、スクリプトに
other\_t = hoge のように記述することで hoge カラムのデータを Solr の
other\_t フィールドに入れることができます。

次にダイナミックフィールドに保存されたデータを検索するためには
webapps/fess/WEB-INF/classes/app.dicon
に利用するフィールドを追加する必要があります。以下のように other\_t
を追加します。

::

        <component name="queryHelper" class="jp.sf.fess.helper.impl.QueryHelperImpl">
            <property name="searchFields">new String[]{"url", "host", "site",
                "title", "content", "contentLength", "lastModified", "mimetype",
                "label", "segment", "other_t" }</property>
        </component>

また、ダイナミックフィールドに保存されたデータを Solr
から取り出すためには利用するフィールドを追加する必要があります。以下のように
other\_t を追加します。

::

        <component name="queryHelper" class="jp.sf.fess.helper.impl.QueryHelperImpl">
           <property name="responseFields">new String[]{"id", "score", "boost",
                "contentLength", "host", "site", "lastModified", "mimetype",
                "tstamp", "title", "digest", "url", "other_t" }</property>
        </component>

上記の設定で Solr から値を取得できているので、ページ上に表示するために
JSP
ファイルを編集します。管理画面にログインして、デザインを表示します。検索結果の表示は検索結果ページ（コンテンツ）で表示されるので、この
JSP ファイルを編集します。other\_t の値を表示したい箇所で
${f:h(doc.other\_t)} とすることで登録した値を表示することができます。
