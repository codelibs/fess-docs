=============
Analyzerの設定
=============

Analyzerについて
================

検索のためのインデックスを作成する際、索引として登録するために文書を切り分ける必要があります。
|Fess| では、文書を単語に分解する機能を Analyzer として登録しています。
Analyzer は CharFilter、Tokenizer および TokenFilter により構成されます。

基本的に、Analyzer によって切り分けられた単位よりも小さいものは、検索を行ってもヒットしません。
たとえば、「東京都に住む」という文を考えます。
この文が「東京都」「に」「住む」というように Analyzer によって分割されたとします。
この場合、「東京都」という語で検索を行った場合はヒットします。
しかし、「京都」という語で検索を行った場合はヒットしません。

|Fess| では言語ごとに専用の Analyzer を用意しています。
インデックス内のフィールド名のサフィックス（例: ``content_ja`` 、 ``content_en`` ）によって、適用される言語別の Analyzer が自動的に切り替わります。

Analyzerの定義ファイル
======================

Analyzer は専用の管理画面を持たず、設定ファイルを直接編集することで変更します。
関連するファイルは ``app/WEB-INF/classes/fess_indices/`` 配下に配置されています。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - ファイル
     - 内容
   * - ``fess_indices/fess.json``
     - ドキュメントインデックスの設定。CharFilter、Tokenizer、TokenFilter および Analyzer の定義を含みます。
   * - ``fess_indices/fess/doc.json``
     - ドキュメントインデックスのマッピング。\ ``*_ja`` や ``*_en`` のようなフィールド名のパターンごとに、適用する Analyzer を割り当てます。
   * - ``fess_indices/fess/<言語>/``
     - 言語ごとの辞書ファイル（例: ``ja/kuromoji.txt`` 、 ``ko/nori.txt`` 、 ``en/protwords.txt`` 、 ``en/stemmer_override.txt`` 、各言語の ``stopwords.txt`` ）。
   * - ``fess_indices/fess/mapping.txt`` 、 ``fess_indices/fess/synonym.txt``
     - 全言語で共有される文字マッピング辞書および類義語辞書。

Analyzer そのものの定義（Tokenizer や TokenFilter の組み合わせ）は ``fess.json`` で行い、どのフィールドにどの Analyzer を適用するかは ``fess/doc.json`` で指定します。

.. note::
   Amazon OpenSearch Service などのマネージドサービスを利用する場合は、``fess_indices/_aws/fess.json`` や ``fess_indices/_cloud/fess.json`` のように、検索エンジンの種別に対応した設定ファイルが優先して使用されます。

Analyzerの登録
==============

Analyzer の設定は、|Fess| の起動時に検索用インデックスが存在しない場合に、上記の設定ファイルを基にインデックスを作成して登録されます。
インデックスはタイムスタンプ付きの名前（例: ``fess.20240101120000000`` ）で作成され、``fess.search`` および ``fess.update`` のエイリアスが割り当てられます。

設定ファイル内の ``${fess.dictionary.path}`` などのプレースホルダーは、インデックス作成時に実際の値へ置き換えられます。
辞書ファイルの配置先は、システムプロパティ ``fess.dictionary.path`` で変更できます。

既存のインデックスがある場合、定義済みの設定が再利用されます。
そのため、Analyzer の定義を変更した場合、その変更を反映するにはインデックスを作り直す必要があります。

辞書による調整
==============

Analyzer が参照する辞書は、管理画面から編集できます。

* :doc:`../admin/kuromoji-guide` - 日本語形態素解析のユーザー辞書
* :doc:`../admin/synonym-guide` - 類義語辞書
* :doc:`../admin/mapping-guide` - 文字マッピング
* :doc:`../admin/stopwords-guide` - ストップワード
* :doc:`../admin/protwords-guide` - 保護語
* :doc:`../admin/stemmeroverride-guide` - ステミングの上書き

Analyzer の構成方法は OpenSearch の Analyzer のドキュメントを参照してください。

注意事項
========

Analyzer の設定は検索に大きな影響を与えます。
Analyzer の変更をする場合は、Lucene の Analyzer の動きを理解した上で実施するか、商用サポートにご相談ください。
