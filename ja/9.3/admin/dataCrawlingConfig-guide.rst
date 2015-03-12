==================================
データストアのクロールに関する設定
==================================

概要
====

|Fess| 
ではデータベースやCSVなどのデータソースをクロール対象とすることができます。ここでは、そのために必要なデータストアの設定について説明します。

設定方法
========

表示方法
--------

管理者アカウントでログイン後、メニューのデータストアをクリックします。

|image0|

設定項目
========

設定名
------

クロール設定の名前を指定します。

ハンドラ名
----------

データストアを処理するハンドラ名です。
データベースをクロールする場合はDatabaseDataStoreを選択し、CSVファイルを対象としてクロールする場合はCsvDataStoreを選択してください。

パラメータ
----------

データストアに関するパラメータを指定します。

スクリプト
----------

データストアから取得した値をどのフィールドに設定するかなどを指定します。
OGNL式が記述することができます。

ブースト値
----------

この設定でクロールしたときのドキュメントのブースト値を指定します。

ロール
------

ロール検索を利用する場合、このクロール設定のロールを指定します。

ラベル
------

このクロール設定でクロールしたときのラベルを指定します。

状態
----

このクロール設定を利用するかどうかを指定します。


表示パラメータ
==============

検索結果に latitude\_s のような項目値を表示する場合は
webapps/fess/WEB-INF/classes/app.dicon に以下のように設定してください。
追加後は searchResults.jsp などで ${doc.latitude\_s}
とすることで表示されます。

::

        <component name="queryHelper" class="jp.sf.fess.helper.impl.QueryHelperImpl">
            <property name="responseFields">new String[]{"id", "score", "boost",
                "contentLength", "host", "site", "lastModified", "mimetype",
                "tstamp", "title", "digest", "url", "latitude_s","longitude_s" }</property>
        </component>


DatabaseDataStore
=================

データベースクロールについて説明します。

例として、以下のようなテーブルが MySQL の testdb
というデータベースにあり、ユーザ名 hoge 、パスワード fuga
で接続することができるとして、説明を行います。

::

    CREATE TABLE doc (
        id BIGINT NOT NULL AUTO_INCREMENT,
        title VARCHAR(100) NOT NULL,
        content VARCHAR(255) NOT NULL,
        latitude VARCHAR(20),
        longitude VARCHAR(20),
        versionNo INTEGER NOT NULL,
        PRIMARY KEY (id)
    );

ここでは、データは以下のようなものを入れておきます．

::

    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 1', 'コンテンツ 1 です．', '37.77493', ' -122.419416', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 2', 'コンテンツ 2 です．', '34.701909', '135.494977', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 3', 'コンテンツ 3 です．', '-33.868901', '151.207091', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 4', 'コンテンツ 4 です．', '51.500152', '-0.126236', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 5', 'コンテンツ 5 です．', '35.681382', '139.766084', 1);

パラメータ
----------

パラメータの設定例は以下のようになります。

::

    driver=com.mysql.jdbc.Driver
    url=jdbc:mysql://localhost:3306/testdb?useUnicode=true&characterEncoding=UTF-8
    username=hoge
    password=fuga
    sql=select * from doc

パラメータは「キー=値」形式となっています。キーの説明は以下です。

+------------+-----------------------------------+
| driver     | ドライバクラス名                  |
+------------+-----------------------------------+
| url        | URL                               |
+------------+-----------------------------------+
| username   | DBに接続する際のユーザ名          |
+------------+-----------------------------------+
| password   | DBに接続する際のパスワード        |
+------------+-----------------------------------+
| sql        | クロール対象を得るための SQL 文   |
+------------+-----------------------------------+

Table: DB用設定パラメータ例


スクリプト
----------

スクリプトの設定例は以下のようになります。

::

    url="http://localhost/" + id
    host="localhost"
    site="localhost"
    title=title
    content=content
    cache=content
    digest=content
    anchor=
    contentLength=content.length()
    lastModified=@jp.sf.fess.taglib.FessFunctions@formatDate(new java.util.Date(@System@currentTimeMillis()))
    location=latitude + "," + longitude
    latitude_s=latitude
    longitude_s=longitude

パラメータは「キー=値」形式になっています。キーの説明は以下です。

値の側は、OGNL
で記述します。文字列はダブルクォーテーションで閉じてください。データベースのカラム名でアクセスすれば、その値になります。

+-----------------+--------------------------------------------------------------+
| url             | URL(検索結果に表示されるリンク)                              |
+-----------------+--------------------------------------------------------------+
| host            | ホスト名                                                     |
+-----------------+--------------------------------------------------------------+
| site            | サイトパス                                                   |
+-----------------+--------------------------------------------------------------+
| title           | タイトル                                                     |
+-----------------+--------------------------------------------------------------+
| content         | コンテンツ(インデックス対象文字列)                           |
+-----------------+--------------------------------------------------------------+
| cache           | コンテンツのキャッシュ(インデックス対象ではない)             |
+-----------------+--------------------------------------------------------------+
| digest          | 検索結果に表示されるダイジェスト部分                         |
+-----------------+--------------------------------------------------------------+
| anchor          | コンテンツに含まれるリンク(普通は指定する必要はありません)   |
+-----------------+--------------------------------------------------------------+
| contentLength   | コンテンツの長さ                                             |
+-----------------+--------------------------------------------------------------+
| lastModified    | コンテンツの最終更新日                                       |
+-----------------+--------------------------------------------------------------+

Table: スクリプトの設定内容


ドライバ
--------

データベースに接続する際にはドライバが必要となります。webapps/fess/WEB-INF/cmd/lib
に jar ファイルを置いてください。

CsvDataStore
=================

CSVファイルを対象としたクロールについて説明します。

たとえば、/home/taro/csv ディレクトリに test.csv ファイルを以下のような内容で生成しておきます。
ファイルのエンコーディングは Shift_JIS にしておきます。

::

    1,タイトル 1,テスト1です。
    2,タイトル 2,テスト2です。
    3,タイトル 3,テスト3です。
    4,タイトル 4,テスト4です。
    5,タイトル 5,テスト5です。
    6,タイトル 6,テスト6です。
    7,タイトル 7,テスト7です。
    8,タイトル 8,テスト8です。
    9,タイトル 9,テスト9です。


パラメータ
----------

パラメータの設定例は以下のようになります。

::

    directories=/home/taro/csv
    fileEncoding=Shift_JIS

パラメータは「キー=値」形式となっています。キーの説明は以下です。

+-------------+----------------------------------------------------+
| directories | CSVファイルが含まれるディレクトリ (.csvまたは.tsv) |
+-------------+----------------------------------------------------+
| files       | CSVファイル (直接指定する場合)                     |
+-------------+----------------------------------------------------+
| fileEncoding | CSVファイルのエンコーディング                     |
+-------------+----------------------------------------------------+
| separatorCharacter | 区切り文字                                  |
+-------------+----------------------------------------------------+

Table: CSVファイル用設定パラメータ例


スクリプト
----------

スクリプトの設定例は以下のようになります。

::

    url="http://localhost/" + cell1
    host="localhost"
    site="localhost"
    title=cell2
    content=cell3
    cache=cell3
    digest=cell3
    anchor=
    contentLength=cell3.length()
    lastModified=new java.util.Date()

パラメータは「キー=値」形式になっています。
キーはデータベースクロールの場合と同様です。


.. |image0| image:: ../../../resources/images/ja/9.3/admin/dataStoreCrawling-1.png
