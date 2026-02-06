============================
Fess ユースケース・活用事例
============================

はじめに
========

Fess は様々な業種・規模の組織で活用されています。
このページでは、Fess の代表的なユースケースと活用事例を紹介します。

.. note::

   以下の事例は、Fess の一般的な活用パターンを示すものです。
   実際の導入事例については、`商用サポート <../support-services.html>`__ にお問い合わせください。

----

業種別ユースケース
================

製造業
------

**課題**: 設計図面、技術文書、品質管理ドキュメントが複数のファイルサーバーに分散し、必要な情報を見つけるのに時間がかかる。

**Fess による解決**:

- ファイルサーバー上の CAD 図面、PDF 技術文書、Office ドキュメントを一元検索
- 製品型番、図面番号、プロジェクト名などでの横断検索
- アクセス権限に基づいた検索結果の表示（ロールベース検索）

**構成例**:

.. code-block:: text

    [ファイルサーバー群]  →  [Fess]  →  [社内ポータル]
         │                    │
         ├─ 設計図面          ├─ OpenSearch クラスター
         ├─ 技術文書          └─ Active Directory 連携
         └─ 品質記録

**関連機能**:

- `ファイルサーバーのクロール <https://fess.codelibs.org/ja/15.5/config/config-filecrawl.html>`__
- `ロールベース検索 <https://fess.codelibs.org/ja/15.5/config/config-role.html>`__
- `サムネイル表示 <https://fess.codelibs.org/ja/15.5/admin/admin-general.html>`__

金融・保険業
-----------

**課題**: コンプライアンス文書、契約書、社内規程が膨大で、監査対応や問い合わせ対応に時間がかかる。

**Fess による解決**:

- 社内規程、マニュアル、FAQ の横断検索
- 契約書・申請書類のテキスト検索
- 過去の問い合わせ履歴からのナレッジ検索

**セキュリティ対応**:

- LDAP/Active Directory 連携による認証
- SAML によるシングルサインオン
- アクセストークンによる API 認証

**関連機能**:

- `LDAP 認証 <https://fess.codelibs.org/ja/15.5/config/config-security.html>`__
- `SAML 認証 <https://fess.codelibs.org/ja/15.5/config/config-saml.html>`__

教育機関
-------

**課題**: 研究論文、講義資料、学内文書が各部門のサーバーに分散し、情報共有が困難。

**Fess による解決**:

- 学内ポータルからの統合検索
- 研究論文リポジトリの検索
- 講義資料・シラバスの検索

**構成例**:

- 学内 Web サイトのクロール
- 論文リポジトリ（DSpace 等）との連携
- Google Drive / SharePoint 上の資料検索

**関連機能**:

- `Web クロール <https://fess.codelibs.org/ja/15.5/config/config-webcrawl.html>`__
- `Google Drive クロール <https://fess.codelibs.org/ja/15.5/config/config-crawl-gsuite.html>`__

IT・ソフトウェア業
-----------------

**課題**: ソースコード、ドキュメント、Wiki、チケット管理システムの情報が分散し、開発効率が低下。

**Fess による解決**:

- GitHub/GitLab リポジトリのコード検索
- Confluence/Wiki ページの検索
- Slack/Teams メッセージの検索

**開発者向け機能**:

- 検索 API による既存システムとの統合
- コードハイライト表示
- ファイルタイプによるフィルタリング

**関連機能**:

- `Git リポジトリのクロール <https://fess.codelibs.org/ja/15.5/config/config-crawl-git.html>`__
- `Confluence クロール <https://fess.codelibs.org/ja/15.5/config/config-crawl-atlassian.html>`__
- `Slack クロール <https://fess.codelibs.org/ja/15.5/config/config-crawl-slack.html>`__

----

規模別ユースケース
================

中小企業（〜100名）
------------------

**特徴**: 限られた IT リソースで、簡単に導入・運用したい。

**推奨構成**:

- Docker Compose による簡単導入
- 単一サーバー構成（Fess + OpenSearch）
- 必要メモリ: 8GB 以上

**導入手順**:

.. code-block:: bash

    # 5分で導入完了
    mkdir fess && cd fess
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml
    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**コスト感**:

- ソフトウェア費用: 無料（オープンソース）
- サーバー費用のみ（クラウド or オンプレミス）

中堅企業（100〜1000名）
---------------------

**特徴**: 複数部門での利用、ある程度の可用性が必要。

**推奨構成**:

- Fess サーバー 2台（冗長化）
- OpenSearch クラスター 3ノード
- ロードバランサーによる負荷分散
- Active Directory 連携

**検索対象の目安**:

- ドキュメント数: 〜500万件
- 同時検索ユーザー: 〜100名

**関連機能**:

- `クラスター構成 <https://fess.codelibs.org/ja/15.5/install/clustering.html>`__
- `バックアップ・リストア <https://fess.codelibs.org/ja/15.5/admin/admin-backup.html>`__

大企業（1000名以上）
------------------

**特徴**: 大規模データ、高可用性、セキュリティ要件が厳しい。

**推奨構成**:

- Fess サーバー複数台（Kubernetes 上で運用）
- OpenSearch クラスター（専用ノード構成）
- 専用のクロールサーバー
- 監視・ログ収集基盤との連携

**スケーラビリティ**:

- ドキュメント数: 数億件対応可能
- OpenSearch のシャード分割による水平スケール

**エンタープライズ機能**:

- 部門別のラベル管理
- 詳細なアクセスログ
- API 経由での他システム連携

.. note::

   大規模環境での導入は、`商用サポート <../support-services.html>`__ のご利用を推奨します。

----

技術的なユースケース
==================

社内 Wiki / ナレッジベース検索
-----------------------------

**概要**: Confluence、MediaWiki、社内 Wiki の横断検索を実現。

**メリット**:

- 複数の Wiki システムを一元検索
- 更新頻度に応じた自動クロール
- Wiki ページ内の添付ファイルも検索対象

**実装例**:

1. Confluence Data Store プラグインをインストール
2. 管理画面から接続情報を設定
3. クロールスケジュールを設定（毎日など）

ファイルサーバー統合検索
-----------------------

**概要**: Windows ファイルサーバー、NAS 上のドキュメントを検索。

**対応プロトコル**:

- SMB/CIFS（Windows 共有フォルダ）
- NFS
- ローカルファイルシステム

**セキュリティ**:

- NTLM 認証によるアクセス制御
- ファイルの ACL を検索結果に反映

**構成ポイント**:

- クロール専用アカウントの作成
- 大量ファイルの場合は段階的クロール
- ネットワーク帯域の考慮

Web サイト内検索（サイトサーチ）
-----------------------------

**概要**: 公開 Web サイトに検索機能を追加。

**導入方法**:

1. **JavaScript 埋め込み方式**

   Fess Site Search (FSS) を利用して、数行の JavaScript で検索窓を追加

2. **API 連携方式**

   検索 API を利用して、独自の検索 UI を構築

**FSS の利用例**:

.. code-block:: html

    <script>
    (function() {
      var fess = document.createElement('script');
      fess.type = 'text/javascript';
      fess.async = true;
      fess.src = 'https://your-fess-server/js/fess-ss.min.js';
      fess.charset = 'utf-8';
      fess.setAttribute('id', 'fess-ss');
      fess.setAttribute('fess-url', 'https://your-fess-server/json');
      document.body.appendChild(fess);
    })();
    </script>
    <fess:search></fess:search>

データベース検索
--------------

**概要**: RDB 内のデータを検索可能にする。

**対応データベース**:

- MySQL / MariaDB
- PostgreSQL
- Oracle
- SQL Server

**ユースケース**:

- 顧客マスター検索
- 製品カタログ検索
- FAQ データベース検索

**実装手順**:

1. Database Data Store プラグインを設定
2. SQL クエリでクロール対象を指定
3. フィールドマッピングを設定

----

まとめ
=====

Fess は、その柔軟な設計により、様々な業種・規模・ユースケースに対応できます。

**導入を検討される方へ**:

1. まずは `クイックスタート <../quick-start.html>`__ で Fess を体験
2. 必要な機能を `ドキュメント <../documentation.html>`__ で確認
3. 本格導入の際は `商用サポート <../support-services.html>`__ にご相談

**関連リソース**:

- `掲載記事一覧 <../articles.html>`__ - 詳細な技術記事
- `ディスカッションフォーラム <https://discuss.codelibs.org/c/FessJA/>`__ - コミュニティサポート
- `GitHub <https://github.com/codelibs/fess>`__ - ソースコードとイシュー管理

