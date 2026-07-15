==================================
Ingestプラグイン
==================================

概要
====

Ingestプラグインは、ドキュメントがインデックスに登録される直前に
データを加工・変換する機能を提供します。クロールで取得した各ドキュメントは、
インデックスへ送信される前に登録済みの Ingester を通過します。

用途
====

- テキストの正規化（全角/半角変換、空白の整形など）
- メタデータやカスタムフィールドの追加
- センシティブ情報のマスキング
- 値の変換（例: エンコードされたベクトル埋め込みのデコード）

Ingester クラス
===============

Ingest機能は ``org.codelibs.fess.ingest.Ingester`` 抽象クラスを継承して
実装します。``Ingester`` には、クロールの種類や処理ステージに応じて
呼び出される ``process`` メソッドが用意されています。デフォルト実装は
いずれも受け取った ``target`` をそのまま返す（何もしない）ため、
必要なメソッドだけをオーバーライドします。

- ``protected Map<String, Object> process(Map<String, Object> target)``

  2つの ``Map`` 版メソッドの共通の委譲先です。これをオーバーライドすると、
  データストアクロールとWeb/ファイルクロール（インデックス登録時）の
  両方のドキュメントに適用されます。多くの用途では、このメソッドだけを
  オーバーライドすれば十分です。

- ``public Map<String, Object> process(Map<String, Object> target, DataStoreParams params)``

  データストアクロール時に呼び出されます。デフォルトでは
  ``process(target)`` に委譲します。

- ``public Map<String, Object> process(Map<String, Object> target, AccessResult<String> accessResult)``

  Web/ファイルクロールのインデックス登録時に呼び出されます。
  デフォルトでは ``process(target)`` に委譲します。

- ``public ResultData process(ResultData target, ResponseData responseData)``

  Web/ファイルクロールのレスポンス処理時（アクセス結果を保存する前）に
  呼び出されます。デフォルトでは ``target`` をそのまま返します。

実行順序（priority）
--------------------

複数の Ingester が登録されている場合は、``priority`` フィールドの昇順
（値が小さいものが先）に実行されます。デフォルト値は ``99`` です。
コンストラクタで直接設定するか、``setPriority(int)`` で変更できます。

.. code-block:: java

    public int getPriority()
    public void setPriority(final int priority)

実装例
======

``process(Map<String, Object>)`` をオーバーライドし、コンテンツを正規化して
カスタムフィールドを追加する例です:

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import java.util.Map;

    import org.codelibs.fess.ingest.Ingester;

    public class ExampleIngester extends Ingester {

        public ExampleIngester() {
            // 実行順序を設定（値が小さいほど先に実行。デフォルトは 99）
            setPriority(50);
        }

        @Override
        protected Map<String, Object> process(final Map<String, Object> target) {
            // コンテンツの正規化
            final Object content = target.get("content");
            if (content instanceof String) {
                target.put("content", ((String) content).trim().replaceAll("\\s+", " "));
            }

            // カスタムフィールドの追加
            target.put("ingested_by", ExampleIngester.class.getSimpleName());

            // 加工したドキュメントを返す
            return target;
        }
    }

.. note::

    ``process`` メソッドで ``null`` を返すとインデックス登録に失敗します。
    ドキュメントをスキップする仕組みはないため、必ず ``target`` を返してください。

登録
====

Ingester は DIコンテナ経由で登録します。プラグインには ``fess_ingest++.xml``
を含めます。ファイル名末尾の ``++`` は、|Fess| 本体の ``fess_ingest.xml``
（Ingester を管理する ``ingestFactory`` を定義）へ設定を追記するマージ規約です。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleIngester"
                   class="org.codelibs.fess.ingest.example.ExampleIngester">
            <postConstruct name="register"/>
        </component>
    </components>

``<postConstruct name="register"/>`` により、コンポーネント生成後に
``Ingester#register()`` が呼び出され、``ingestFactory`` に自身が登録されます。

Ingest機能に関する ``fess_config.properties`` の設定項目はありません。
有効・無効はプラグインの導入有無で、実行順序は ``priority`` で制御します。

実行フロー
==========

Ingester は、加工されたドキュメントがインデックスへ送信される直前に、
以下の箇所で ``priority`` の昇順に呼び出されます:

- **データストアクロール**: ドキュメントを送信する直前に
  ``process(Map, DataStoreParams)`` が呼び出されます。
- **Web/ファイルクロール（レスポンス処理時）**: クロール結果を保存する前に
  ``process(ResultData, ResponseData)`` が呼び出されます。
- **Web/ファイルクロール（インデックス登録時）**: ドキュメントを送信する直前に
  ``process(Map, AccessResult)`` が呼び出されます。

いずれの箇所でも、ある Ingester が例外をスローした場合は警告ログを出力して
処理を継続します（そのドキュメントのインデックス登録は中断されません）。

.. note::

    Ingester はクローラの実行環境（``ingestFactory``）に登録されるため、
    クロール処理の一部として動作します。

参考実装
========

実装の参考として、以下のプラグインが GitHub の
`CodeLibs <https://github.com/codelibs>`__ で公開されています:

- ``fess-ingest-example`` - 最小構成のサンプル実装
- ``fess-webapp-multimodal`` - ベクトル埋め込みをデコードする ``EmbeddingIngester`` を含むプラグイン

参考情報
========

- :doc:`plugin-architecture` - プラグインアーキテクチャ
