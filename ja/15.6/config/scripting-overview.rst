==================================
スクリプティング概要
==================================

概要
====

|Fess| では、様々な場面でスクリプトを使用してカスタムロジックを実装できます。
スクリプトを活用することで、クロール時のデータ加工、検索結果のカスタマイズ、
スケジュールジョブの実行などを柔軟に制御できます。

対応スクリプト言語
==================

|Fess| は以下のスクリプト言語をサポートしています:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - 言語
     - 識別子
     - 説明
   * - Groovy
     - ``groovy``
     - デフォルトのスクリプト言語。Java互換で強力な機能を提供
   * - JavaScript
     - ``javascript``
     - Web開発者に馴染みのある言語

.. note::
   Groovyが最も広く使用されており、本ドキュメントの例はGroovyで記述しています。

スクリプトの使用場面
====================

データストア設定
----------------

データストアコネクタでは、取得したデータをインデックスフィールドにマッピングするために
スクリプトを使用します。

::

    url="https://example.com/article/" + data.id
    title=data.name
    content=data.description
    lastModified=data.updated_at

パスマッピング
--------------

URLの正規化やパスの変換にスクリプトを使用できます。

::

    # URLを変換
    url.replaceAll("http://", "https://")

スケジュールジョブ
------------------

スケジュールジョブでは、カスタムの処理ロジックをGroovyスクリプトで記述できます。

::

    return container.getComponent("crawlJob").execute();

基本的な構文
============

変数アクセス
------------

::

    # データストアのデータにアクセス
    data.fieldName

    # システムコンポーネントにアクセス
    container.getComponent("componentName")

文字列操作
----------

::

    # 連結
    title + " - " + category

    # 置換
    content.replaceAll("old", "new")

    # 分割
    tags.split(",")

条件分岐
--------

::

    # 三項演算子
    data.status == "active" ? "有効" : "無効"

    # nullチェック
    data.description ?: "説明なし"

日付操作
--------

::

    # 現在日時
    new Date()

    # フォーマット
    new java.text.SimpleDateFormat("yyyy-MM-dd").format(data.date)

利用可能なオブジェクト
======================

スクリプト内で使用可能な主なオブジェクト:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - オブジェクト
     - 説明
   * - ``data``
     - データストアから取得したデータ
   * - ``container``
     - DIコンテナ（コンポーネントへのアクセス）
   * - ``systemHelper``
     - システムヘルパー
   * - ``fessConfig``
     - |Fess| の設定

セキュリティ
============

.. warning::
   スクリプトは強力な機能を持つため、信頼できるソースからのみ使用してください。

- スクリプトはサーバー上で実行されます
- ファイルシステムやネットワークへのアクセスが可能です
- 管理者権限を持つユーザーのみがスクリプトを編集できるようにしてください

パフォーマンス
==============

スクリプトのパフォーマンスを最適化するためのヒント:

1. **複雑な処理を避ける**: スクリプトはドキュメントごとに実行されます
2. **外部リソースへのアクセスを最小化**: ネットワーク呼び出しは遅延の原因になります
3. **キャッシュを活用**: 繰り返し使用する値はキャッシュを検討

デバッグ
========

スクリプトのデバッグには、ログ出力を活用します:

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("script")
    logger.info("data.id = {}", data.id)

ログレベルの設定:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="script" level="DEBUG"/>

参考情報
========

- :doc:`scripting-groovy` - Groovyスクリプトガイド
- :doc:`../admin/dataconfig-guide` - データストア設定ガイド
- :doc:`../admin/scheduler-guide` - スケジューラー設定ガイド
