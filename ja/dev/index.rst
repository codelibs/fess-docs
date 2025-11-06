====================================
オープンソース全文検索サーバー - |Fess| 開発ガイド
====================================

このガイドでは、|Fess| の開発に参加するために必要な情報を提供します。
初めて |Fess| の開発に取り組む方から、経験豊富な開発者まで、幅広い方々を対象としています。

.. contents:: 目次
   :local:
   :depth: 2

対象読者
========

このガイドは、以下のような方々を対象としています：

- |Fess| の機能追加や改善に貢献したい開発者
- |Fess| のコードを理解したい技術者
- |Fess| をカスタマイズして利用したい方
- オープンソースプロジェクトへの参加に興味がある方

必要な前提知識
============

|Fess| の開発に参加するには、以下の知識が役立ちます：

**必須**

- Java プログラミングの基礎知識（Java 21 以降）
- Git および GitHub の基本的な使い方
- Maven の基本的な使い方

**推奨**

- LastaFlute フレームワークの知識
- DBFlute の知識
- OpenSearch/Elasticsearch の知識
- Web アプリケーション開発の経験

開発ガイドの構成
==============

このガイドは、以下のセクションで構成されています。

:doc:`getting-started`
    |Fess| 開発の概要と、開発を始めるための最初のステップを説明します。
    開発に必要な技術スタックや、プロジェクトの全体像を理解できます。

:doc:`setup`
    開発環境のセットアップ手順を詳しく説明します。
    Java、IDE、OpenSearch などの必要なツールのインストールから、
    |Fess| のソースコードの取得と実行まで、ステップバイステップで解説します。

:doc:`architecture`
    |Fess| のアーキテクチャとコード構造について説明します。
    主要なパッケージ、モジュール、デザインパターンを理解することで、
    効率的に開発を進めることができます。

:doc:`workflow`
    |Fess| 開発の標準的なワークフローを説明します。
    機能追加、バグ修正、コードレビュー、テストなど、
    開発作業の進め方を学べます。

:doc:`building`
    |Fess| のビルド方法とテスト方法について説明します。
    ビルドツールの使い方、単体テストの実行、
    配布パッケージの作成方法などを解説します。

:doc:`contributing`
    |Fess| プロジェクトへの貢献方法について説明します。
    プルリクエストの作成、コーディング規約、
    コミュニティとのコミュニケーション方法などを学べます。

クイックスタート
==============

|Fess| の開発を今すぐ始めたい場合は、以下の手順に従ってください：

1. **システム要件の確認**

   開発には以下のツールが必要です：

   - Java 21 以降
   - Maven 3.x 以降
   - Git
   - IDE（Eclipse、IntelliJ IDEA など）

2. **ソースコードの取得**

   .. code-block:: bash

       git clone https://github.com/codelibs/fess.git
       cd fess

3. **OpenSearch プラグインのダウンロード**

   .. code-block:: bash

       mvn antrun:run

4. **実行**

   IDE から ``org.codelibs.fess.FessBoot`` を実行するか、
   Maven から実行します：

   .. code-block:: bash

       mvn compile exec:java

詳細は :doc:`setup` を参照してください。

開発環境の選択肢
==============

|Fess| の開発は、以下のいずれかの環境で行うことができます：

ローカル開発環境
--------------

最も一般的な開発環境です。自分のマシンに開発ツールをインストールし、
IDE を使用して開発します。

**メリット:**

- 高速なビルドと実行
- IDE の機能をフルに活用できる
- オフラインでも作業可能

**デメリット:**

- 初期セットアップに時間がかかる
- 環境の違いによる問題が発生する可能性

Docker を使用した開発環境
------------------------

Docker コンテナを使用して、一貫性のある開発環境を構築できます。

**メリット:**

- 環境の一貫性が保たれる
- セットアップが簡単
- クリーンな状態に戻しやすい

**デメリット:**

- Docker の知識が必要
- パフォーマンスがやや低下する場合がある

詳細は :doc:`setup` を参照してください。

よくある質問
==========

Q: 開発に必要な最小限のスペックは？
--------------------------------

A: 以下を推奨します：

- CPU: 4コア以上
- メモリ: 8GB以上
- ディスク: 20GB以上の空き容量

Q: どの IDE を使用すればよいですか？
---------------------------------

A: Eclipse、IntelliJ IDEA、VS Code など、お好みの IDE を使用できます。
このガイドでは主に Eclipse を例に説明していますが、
他の IDE でも同様に開発できます。

Q: LastaFlute や DBFlute の知識は必須ですか？
------------------------------------------

A: 必須ではありませんが、あると開発がスムーズに進みます。
基本的な使い方は本ガイドでも説明していますが、
詳細は各フレームワークの公式ドキュメントを参照してください。

Q: 初めてのコントリビューションは何から始めればよいですか？
------------------------------------------------------

A: 以下のような比較的簡単な作業から始めることをお勧めします：

- ドキュメントの改善
- テストの追加
- バグ修正
- 既存機能の小さな改善

詳細は :doc:`contributing` を参照してください。

関連リソース
==========

公式リソース
----------

- `Fess 公式サイト <https://fess.codelibs.org/ja/>`__
- `GitHub リポジトリ <https://github.com/codelibs/fess>`__
- `Issue トラッカー <https://github.com/codelibs/fess/issues>`__
- `Discussions <https://github.com/codelibs/fess/discussions>`__

技術ドキュメント
--------------

- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
- `OpenSearch <https://opensearch.org/docs/latest/>`__

コミュニティ
----------

- `Fess コミュニティフォーラム <https://discuss.codelibs.org/c/FessJA>`__
- `Twitter: @codelibs <https://twitter.com/codelibs>`__

次のステップ
==========

開発を始めるには、:doc:`getting-started` から読み始めることをお勧めします。

.. toctree::
   :maxdepth: 2
   :caption: 目次:

   getting-started
   setup
   architecture
   workflow
   building
   contributing
