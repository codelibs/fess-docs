============================
パスのエンコーディングの変更
============================

パスのエンコーディングの変更
============================

html以外のファイルで、参照元とファイル名の文字コードが異なる場合、検索結果のリンクの文字列が文字化けします。

たとえば、テスト.txt というファイルの中身がUTF-8
で書かれていて、ファイル名が Shift\_JIS
の場合、リンクの文字列が文字化けします。

設定方法
--------

例えば下記のように
webapps/fess/WEB-INF/classes/s2robot\_transformer.dicon
を修正することで、パスを Shift\_JIS で解決するようになります。

::

    <component name="fessFileTransformer" class="jp.sf.fess.transformer. |Fess| FileTransformer" instance="singleton">
       <property name="name">"fessFileTransformer"</property>
       <property name="ignoreEmptyContent">true</property>
       <property name="encoding">"Shift_JIS"</property>
    </component>
