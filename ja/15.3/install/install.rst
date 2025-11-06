====================
インストール方法の選択
====================

このページでは、 |Fess| のインストール方法の概要について説明します。
ご利用の環境に応じて、適切なインストール方法を選択してください。

.. warning::

   **本番環境での重要な注意事項**

   本番環境や負荷検証などでは、組み込み OpenSearch での稼働は推奨しません。
   必ず外部の OpenSearch サーバーを構築してください。

前提条件の確認
============

インストールを開始する前に、システム要件を確認してください。

詳細は :doc:`prerequisites` を参照してください。

インストール方法の比較
====================

|Fess| は、以下の方法でインストールできます。ご利用の環境と用途に応じて選択してください。

.. list-table::
   :header-rows: 1
   :widths: 15 25 30 30

   * - 方法
     - 対象 OS
     - 推奨用途
     - 詳細ドキュメント
   * - Docker
     - Linux, Windows, macOS
     - 開発・評価環境、迅速なセットアップ
     - :doc:`install-docker`
   * - TAR.GZ
     - Linux, macOS
     - カスタマイズが必要な環境
     - :doc:`install-linux`
   * - RPM
     - RHEL, CentOS, Fedora
     - 本番環境（RPM ベース）
     - :doc:`install-linux`
   * - DEB
     - Debian, Ubuntu
     - 本番環境（DEB ベース）
     - :doc:`install-linux`
   * - ZIP
     - Windows
     - Windows 環境での開発・本番
     - :doc:`install-windows`

各インストール方法の特徴
======================

Docker 版
--------

**メリット:**

- 最も迅速にセットアップ可能
- 依存関係の管理が不要
- 開発環境の構築に最適
- コンテナの起動・停止が容易

**デメリット:**

- Docker の知識が必要

**推奨環境:** 開発環境、評価環境、POC、本番環境

詳細: :doc:`install-docker`

Linux パッケージ版 (TAR.GZ/RPM/DEB)
---------------------------------

**メリット:**

- ネイティブ環境での高いパフォーマンス
- システムサービスとして管理可能（RPM/DEB）
- 細かいカスタマイズが可能

**デメリット:**

- Java と OpenSearch の手動インストールが必要
- 設定の手間がかかる

**推奨環境:** 本番環境、カスタマイズが必要な環境

詳細: :doc:`install-linux`

Windows 版 (ZIP)
---------------

**メリット:**

- Windows ネイティブ環境で動作
- インストーラー不要

**デメリット:**

- Java と OpenSearch の手動インストールが必要
- 設定の手間がかかる

**推奨環境:** Windows 環境での開発・評価、Windows Server での本番運用

詳細: :doc:`install-windows`

インストールの基本的な流れ
========================

すべてのインストール方法で、基本的な流れは同じです。

1. **システム要件の確認**

   :doc:`prerequisites` を参照して、システム要件を満たしていることを確認します。

2. **ソフトウェアのダウンロード**

   `ダウンロードサイト <https://fess.codelibs.org/ja/downloads.html>`__ から |Fess| をダウンロードします。

   Docker 版の場合は、Docker Compose ファイルを取得します。

3. **OpenSearch のセットアップ**

   Docker 版以外の場合、OpenSearch を個別にセットアップする必要があります。

   - OpenSearch 3.3.0 のインストール
   - 必須プラグインのインストール
   - 設定ファイルの編集

4. **Fess のセットアップ**

   - Fess のインストール
   - 設定ファイルの編集（OpenSearch への接続情報など）

5. **起動と確認**

   - サービスの起動
   - ブラウザーでアクセスして動作確認

   詳細は :doc:`run` を参照してください。

必要なコンポーネント
==================

|Fess| を実行するには、以下のコンポーネントが必要です。

Fess 本体
--------

全文検索システムの本体です。Web インターフェース、クローラー、インデクサーなどの機能を提供します。

OpenSearch
----------

検索エンジンとして OpenSearch を使用します。

- **対応バージョン**: OpenSearch 3.3.0
- **必須プラグイン**:

  - opensearch-analysis-fess
  - opensearch-analysis-extension
  - opensearch-minhash
  - opensearch-configsync

.. important::

   OpenSearch のバージョンとプラグインのバージョンは一致させる必要があります。
   バージョンの不一致は、起動エラーや予期しない動作の原因となります。

Java (Docker 版以外)
-------------------

TAR.GZ/ZIP/RPM/DEB 版の場合、Java 21 以降が必要です。

- 推奨: `Eclipse Temurin <https://adoptium.net/temurin>`__
- OpenJDK 21 以降も使用可能

.. note::

   Docker 版の場合、Java は Docker イメージに含まれているため、別途インストールする必要はありません。

次のステップ
==========

システム要件を確認し、適切なインストール方法を選択してください。

1. :doc:`prerequisites` - システム要件の確認
2. インストール方法の選択:

   - :doc:`install-docker` - Docker でのインストール
   - :doc:`install-linux` - Linux へのインストール
   - :doc:`install-windows` - Windows へのインストール

3. :doc:`run` - |Fess| の起動と初回セットアップ
4. :doc:`security` - セキュリティ設定（本番環境の場合）

よくある質問
==========

Q: OpenSearch は必須ですか？
--------------------------

A: はい、必須です。|Fess| は検索エンジンとして OpenSearch を使用します。
Docker 版の場合は自動的にセットアップされますが、その他の方法では手動でインストールする必要があります。

Q: 以前のバージョンからアップグレードできますか？
----------------------------------------------

A: はい、可能です。詳細は :doc:`upgrade` を参照してください。

Q: 複数のサーバーで構成できますか？
---------------------------------

A: はい、可能です。Fess と OpenSearch を別々のサーバーで実行することができます。
また、OpenSearch をクラスター構成にすることで、高可用性とパフォーマンスの向上が可能です。

ダウンロード
==========

|Fess| および関連コンポーネントは、以下からダウンロードできます：

- **Fess**: `ダウンロードサイト <https://fess.codelibs.org/ja/downloads.html>`__
- **OpenSearch**: `Download OpenSearch <https://opensearch.org/downloads.html>`__
- **Java (Adoptium)**: `Adoptium <https://adoptium.net/>`__
- **Docker**: `Get Docker <https://docs.docker.com/get-docker/>`__

バージョン情報
============

このドキュメントは、以下のバージョンを対象としています：

- **Fess**: 15.3.0
- **OpenSearch**: 3.3.0
- **Java**: 21 以降
- **Docker**: 20.10 以降
- **Docker Compose**: 2.0 以降

以前のバージョンのドキュメントについては、各バージョンのドキュメントを参照してください。
