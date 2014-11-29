======================
レプリケーションの設定
======================

レプリケーションの設定について
==============================

インデックスのレプリケーションは Solr
のレプリケーション機能で設定します。クロールおよびインデックス作成用の
|Fess| と検索用 |Fess| の 2
台のサーバーを構築することで、インデックス作成時にかかる負荷を分散することができます。

構築方法
========

インデックス作成用 |Fess| の構築
------------------------------

|Fess| をダウンロードして、インストールします。ここでは、MasterServer
という名前のホストにインストールしたとします。\ ``/opt/fess_master/``
にインストールしたとします。solr/core1/conf/solrconfig.xml
を以下のように編集します。

::

    ...
    <requestHandler name="/replication" >
        <lst name="master">
            <str name="replicateAfter">startup</str>
            <str name="replicateAfter">optimize</str>
            <str name="backupAfter">optimize</str>
            <str name="confFiles">schema.xml,stopwords.txt,stopwords_ja.txt,elevate.xml,
                stoptags_ja.txt,synonyms.txt,mapping_ja.txt,mapping-FoldToASCII.txt,
                mapping-ISOLatin1Accent.txt,protwords.txt,compositePOS.txt,spellings.txt,
                currency.xml</str>
        </lst>
        <str name="maxNumberOfBackups">1</str>
    </requestHandler>
    ...

|Fess| 
の起動後、通常の構築と同様にクロール設定を登録します。インデックス作成用
|Fess| の構築手順は通常の構築手順と特に変わりません。

検索用 |Fess| の構築
------------------

|Fess| をダウンロードして、インストールします。\ ``/opt/fess_slave/``
にインストールしたとします。solr/core1/conf/solrconfig.xml
を以下のように編集します。

::

    ...
    <requestHandler name="/replication" >
        <lst name="slave">
            <str name="masterUrl">http://MasterServer:8080/solr/core1/replication</str>
            <str name="pollInterval">00:00:60</str>
            <str name="compression">internal</str>
            <str name="httpConnTimeout">5000</str>
            <str name="httpReadTimeout">10000</str>
            <str name="httpBasicAuthUser">solradmin</str>
            <str name="httpBasicAuthPassword">solradmin</str>
         </lst>
    </requestHandler>
    ...

|Fess| を起動します。

インデックスの同期
------------------

上記までの設定で、インデックス作成用 |Fess| がクロール後、最適化
(optimize) されると、検索用 |Fess| にインデックスがコピーされます。
