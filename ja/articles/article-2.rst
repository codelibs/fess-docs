====================================================================
Fess で作る Elasticsearch ベースの検索サーバー 〜 ロールベース検索編
====================================================================

はじめに
========

本記事では Fess の特徴的な機能の一つでもあるロールベース検索機能についてご紹介します。

本記事では Fess 10.0.2 を利用して説明します。
Fess の構築方法については\ `導入編 <https://fess.codelibs.org/ja/articles/article-1.html>`__\ を参照してください。

対象読者
========

-  ポータルサイトなどの認証があるシステムで検索システムを構築してみたい方

-  閲覧権限ごとに検索する環境を構築したい方

必要な環境
==========

この記事の内容に関しては次の環境で、動作確認を行っています。

-  Ubuntu 14.04

-  JDK 1.8.0\_74

ロールベース検索
================

Fess のロールベース検索とは、認証されたユーザーの認証情報を元に検索結果を出し分ける機能です。
たとえば、営業部ロールを持つ営業担当者Aは検索結果に営業部ロールの情報が表示されるが、営業部ロールを持たない技術担当者Bは検索してもそれが表示されません。
この機能を利用することで、ポータルやシングルサインオン環境でログインしているユーザーの所属する部門別や役職別などに検索を実現することができます。

Fess のロールベース検索はデフォルトでは Fess で管理するユーザー情報を元に検索結果の出し分けを行うことができます。
それ以外にも LDAP や Active Directory の認証情報と連携して利用することもできます。
また、それらの認証システム以外にもロール情報を以下の場所から取得できます。

1. リクエストパラメータ

2. リクエストヘッダー

3. クッキー

4. J2EE の認証情報

利用方法としては、ポータルサーバーやエージェント型シングルサインオンシステムでは認証時に Fess の稼働しているドメインとパスに対してクッキーで認証情報を保存することで、ロール情報を Fess に渡すことができます。
また、リバースプロキシ型シングルサインオンシステムでは Fess へのアクセス時にリクエストパラメータやリクエストヘッダーに認証情報を付加することで、 Fess でロール情報を取得することができます。
このように様々な認証システムと連携することで、ユーザーごとに検索結果を出し分けることができます。

ロールベース検索を利用するための設定
====================================

Fess 10.0.2 がインストールしてあるものとします。
まだ、インストールしていない場合は、\ `導入編 <https://fess.codelibs.org/ja/articles/article-1.html>`__\ を参考にしてインストールしてください。

今回は、Fess のユーザー管理機能を用いたロール検索を説明します。

設定の概要
----------

今回は、営業部（sales）と技術部（eng）の2つのロールを作成します。 そしてtaroユーザーはsalesロールに属し\https://www.n2sm.net/ の検索結果を得られるようし、hanakoユーザーはengロールに属し、\https://fess.codelibs.org/ の検索結果を得られるようする。

ロールの作成
------------

まず管理画面にアクセスします。
\http://localhost:8080/admin/

ユーザー > ロール > 新規作成 から 名前に｢sales｣と入力し、salesロールを作成します。
同様にengロールも作成します。

ロールの一覧
|image0|


クローラ用ロールの作成
----------------------

ユーザー > ロール > sales > 新しいクローラ用ロールの作成 を押下します。
名前に ｢営業部｣と入力し、値は｢sales｣のままで[作成]を押下します。
すると クローラ > ロール の一覧に営業部の設定が追加されます。

同様に engロールのクローラ用ロールの名前を｢技術部｣として登録します。

クローラ用ロールの一覧
|image1|


ユーザーの作成
--------------

ユーザー > ユーザー > 新規作成 からtaroユーザーとhanakoユーザーを下図の設定で作成します。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - 
     - 太郎
     - 花子
   * - ユーザー名
     - taro
     - hanako
   * - パスワード
     - taro
     - hanako
   * - ロール
     - sales
     - eng


登録ユーザーの確認
------------------

今回の設定でadmin、taro、hanakoの3つユーザーで Fess にログインできる状態になっています。
順にログインできることを確認してください。
\http://localhost:8080/admin/ にアクセスして、adminユーザーでログインすると通常通り管理画面が表示されます。
次にadminユーザーをログアウトします。管理画面右上のボタンをクリックしてください。

ログアウトボタン
|image2|

ユーザー名とパスワードを入力してtaroやhanakoでログインしてください。
ログインが成功すると、\http://localhost:8080/ の検索画面が表示されます。

クロール設定の追加
------------------

クロール対象を登録します。
今回は営業部ロールのユーザーは\https://www.n2sm.net/ だけを検索でき、技術部ロールのユーザーは\https://fess.codelibs.org/ だけを検索できるようにします。
これらのクロール設定を登録するため、クローラ > ウェブ > 新規作成 をクリックして、ウェブクロール設定を作成してください。
今回は下記のような設定にします。他はデフォルトです。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - 
     - N2SM
     - Fess
   * - 名前
     - N2SM
     - Fess
   * - URL
     - \https://www.n2sm.net/
     - \https://fess.codelibs.org/
   * - クロール対象とするURL
     - \https://www.n2sm.net/.*
     - \https://fess.codelibs.org/.*
   * - 最大アクセス数
     - 10
     - 10
   * - 間隔
     - 3000ミリ秒
     - 3000ミリ秒
   * - ロール
     - 営業部
     - 技術部

クロールの開始
--------------

クロール設定登録後、システム > スケジューラ > Default Crawler から[今すぐ開始]を押下します。クロールが完了するまでしばらく待ちます。

検索
----

クロール完了後、\http://localhost:8080/ にアクセスして、ログインしていない状態で「fess」などの単語を検索して、検索結果が表示されないことを確認してください。
次にtaroユーザーでログインして、同様に検索してください。
taroユーザーはsalesロールを持つため、\https://www.n2sm.net/ の検索結果だけが表示されます。

salesロールでの検索画面
|image3|

taroユーザーをログアウトして、hanakoユーザーでログインしてください。
先ほどと同様に検索すると、hanakoユーザーはengロールを持つので、\https://fess.codelibs.org/ の検索結果だけが表示されます。

engロールでの検索画面
|image4|

まとめ
======

(TODO)Fess のセキュリティー機能の一つであるロールベース検索についてご紹介しました。
J2EEの認証情報を用いたロールベース検索を中心に説明しましたが、 Fess への認証情報の受け渡しは汎用的な実装であるので様々な認証システムに対応できると思います。
ユーザーの属性ごとに検索結果を出し分けることができるので、社内ポータルサイトや共有フォルダなどの閲覧権限ごとに検索が必要なシステムも実現することが可能です。

次回は、 Fess の提供しているAjax機能についてご紹介します。

参考資料
========

-  `Fess <https://fess.codelibs.org/ja/>`__

.. |image0| image:: ../../resources/images/ja/article/3/role-1.png
.. |image1| image:: ../../resources/images/ja/article/3/role-2.png
.. |image2| image:: ../../resources/images/ja/article/3/logout.png
.. |image3| image:: ../../resources/images/ja/article/3/search-by-sales.png
.. |image4| image:: ../../resources/images/ja/article/3/search-by-eng.png
