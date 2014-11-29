============================
索引文字列抽出についての設定
============================

索引文字列抽出について
======================

検索のためのインデックスを作成する際、索引として登録するために文書を切り分ける必要があります。このために使用されるのが、トークナイザーです。

基本的に、トークナイザーによって切り分けられた単位よりも小さいものは、検索を行ってもヒットしません。例えば、「東京都に住む」という文を考えます。いま、この文が「東京都」「に」「住む」というようにトークナイザーによって分割されたとします。この場合、「東京都」という語で検索を行った場合はヒットします。しかし、「京都」という語で検索を行った場合はヒットしません。そのためトークナイザーの選択は重要です。

|Fess| の場合デフォルトでは StandardTokenizer+CJKBigramFilter
が使用されていますが、schema.xml の analyzer
部分を設定することでトークナイザーを変更することができます。

CJKBigramFilterについて
-----------------------

StandardTokenizer+CJKBigramFilter
は日本語のようなマルチバイトの文字列に対しては bi-gram
、つまり二文字ずつインデックスを作成します。この場合、1文字の語を検索することはできません。

StandardTokenizerについて
-------------------------

StandardTokenizer は日本語のようなマルチバイトの文字列に対しては
uni-gram
、つまり一文字ずつインデックスを作成します。そのため、検索漏れが少なくなります。また、CJKTokenizerの場合、1文字のクエリを検索することができませんが、StandardTokenizerを使用すると検索可能になります。しかし、インデックスサイズが増えるので注意してください。

下記の例のように solr/core1/conf/schema.xml の analyzer
部分を変更することで、StandardTokenizer を使用できます。

::

    <schema name="fess" version="1.4">
      <types>
        <fieldType name="text" class="solr.TextField" positionIncrementGap="100">
          <analyzer type="index">
            <charFilter class="solr.MappingCharFilterFactory" mapping="mapping_ja.txt"/>
            <tokenizer class="solr.StandardTokenizerFactory"/>
      :
          </analyzer>
          <analyzer type="query">
            <charFilter class="solr.MappingCharFilterFactory" mapping="mapping_ja.txt"/>
            <tokenizer class="solr.StandardTokenizerFactory"/>
      :

また、webapps/fess/WEB-INF/classes/app.diconでデフォルトで有効になっているuseBigramをfalseに変更します。

::

      :
        <component name="queryHelper" class="jp.sf.fess.helper.impl.QueryHelperImpl">
            <property name="useBigram">true</property>
      :

設定後、 |Fess| を再起動します。
