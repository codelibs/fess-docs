==================
クローラ関連の設定
==================

単語の長さの上限の設定
======================

英数字だけの単語や連続する記号は、不要なインデックスの増加やクロールパフォーマンスの劣化を引き起こします。
そのため、|Fess| ではデフォルトで連続する英数字は20文字以上、連続する記号文字は10文字以上のものは切り捨ててインデクシングします。
それ以上の長さの単語での検索が必要な場合は、fess_config.properties の以下の設定を変更してください。

::

    crawler.document.max.alphanum.term.size=20
    crawler.document.max.symbol.term.size=10

ファイルサイズの設定
====================

クロールするファイルサイズ上限を指定することができます。
上限には

* ファイルを取得するサイズの上限
* ファイルの種類ごとにインデクシングするファイルサイズの上限

があります。

まず、ファイルを取得するサイズの上限はクローラ設定の設定パラメータにclient.maxContentLengthで指定します。
10Mバイト以上のファイルを取得しない場合は以下のように指定します。
デフォルトでは特に制限はありません。

::

    client.maxContentLength=10485760

次に、ファイルの種類ごとの制限については、デフォルトでは HTML ファイルは 2.5M バイト、それ以外は 10M バイトまで処理します。
扱うファイルサイズを変更したい場合は app/WEB-INF/classes/crawler/contentlength.xml を編集します。
標準の contentlength.xml は以下の通りです。

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
            "http://dbflute.org/meta/lastadi10.dtd">
    <components namespace="fessCrawler">
            <include path="crawler/container.xml" />

            <component name="contentLengthHelper"
                    class="org.codelibs.fess.crawler.helper.ContentLengthHelper" instance="singleton">
                    <property name="defaultMaxLength">10485760</property><!-- 10M -->
                    <postConstruct name="addMaxLength">
                            <arg>"text/html"</arg>
                            <arg>2621440</arg><!-- 2.5M -->
                    </postConstruct>
            </component>
    </components>

デフォルト値を変更したい場合は defaultMaxLength の値を変更します。
扱うファイルサイズはコンテンツタイプごとに指定できます。
HTMLファイルであれば、text/html と扱うファイルサイズの上限を記述します。

扱うファイルサイズの上限値を変更する場合は、使用するヒープメモリ量にも注意してください。

プロキシの設定
==============

イントラネット内から外部サイトをクロールするような場合は、ファイアフォールにクロールがブロックされてしまうかもしれません。
そのような場合にはクローラ用のプロキシを設定してください。

設定方法
--------

管理画面のクロール設定で、設定パラメータに以下のように指定して保存します。

::

    client.proxyHost=プロキシサーバー名(ex. 192.168.1.1)
    client.proxyPort=プロキシサーバーのポート(ex. 8080)
