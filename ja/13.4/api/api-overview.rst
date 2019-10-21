==================
APIの概要
==================


|Fess| の提供するAPI
==================

このドキュメントでは、 |Fess| が提供するAPIについて説明します。
APIを利用することで、既存のウェブシステムなどでも、|Fess| を検索サーバーとして使うことができます。

APIの種類
==================

.. TODO: favorite, favorites

|Fess| はいくつかのAPIを提供していますが、どのAPIを使用するかは
``http://<Server Name>/json/?type=popularword``
のように ``type`` パラメータに値を与えることで指定します。
``type`` パラメータに設定できる値は以下の通りです。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - search
     - 検索結果を取得するAPI。 このAPIを利用する際は ``type`` パラメータを省略することもできます。
   * - popularword
     - 人気ワードを取得するAPI。
   * - label
     - 作成済みのラベルのリストを取得するAPI。
   * - ping
     - サーバーの状態を取得するAPI。

表: APIの種類
