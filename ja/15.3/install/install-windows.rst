====================================
Windows へのインストール (詳細手順)
====================================

このページでは、Windows 環境への |Fess| のインストール手順を説明します。
ZIP パッケージを使用したインストール方法について記載しています。

.. warning::

   本番環境では、組み込み OpenSearch での稼働は推奨しません。
   必ず外部の OpenSearch サーバーを構築してください。

前提条件
========

- :doc:`prerequisites` に記載されているシステム要件を満たしていること
- Java 21 がインストールされていること
- OpenSearch 3.3.0 を利用可能な状態にすること（または新規インストール）
- Windows の環境変数 ``JAVA_HOME`` が適切に設定されていること

Java のインストール確認
====================

コマンドプロンプトまたは PowerShell を開き、以下のコマンドで Java のバージョンを確認します。

コマンドプロンプトの場合::

    C:\> java -version

PowerShell の場合::

    PS C:\> java -version

Java 21 以降が表示されることを確認してください。

環境変数の設定
============

1. ``JAVA_HOME`` 環境変数の設定

   Java がインストールされているディレクトリを ``JAVA_HOME`` として設定します。

   例::

       JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.1.12-hotspot

2. ``PATH`` 環境変数への追加

   ``%JAVA_HOME%\bin`` を ``PATH`` 環境変数に追加します。

.. tip::

   環境変数の設定方法：

   1. 「スタート」メニューから「設定」を開く
   2. 「システム」→「バージョン情報」→「システムの詳細設定」をクリック
   3. 「環境変数」ボタンをクリック
   4. 「システム環境変数」または「ユーザー環境変数」で設定

ステップ 1: OpenSearch のインストール
===================================

OpenSearch のダウンロード
-----------------------

1. `Download OpenSearch <https://opensearch.org/downloads.html>`__ から Windows 用の ZIP パッケージをダウンロードします。

2. ダウンロードした ZIP ファイルを任意のディレクトリに展開します。

   例::

       C:\opensearch-3.3.0

   .. note::

      パスに日本語や空白文字が含まれないディレクトリを選択することを推奨します。

OpenSearch プラグインのインストール
---------------------------------

コマンドプロンプトを**管理者権限で**開き、以下のコマンドを実行します。

::

    C:\> cd C:\opensearch-3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.0

.. important::

   プラグインのバージョンは OpenSearch のバージョンと一致させる必要があります。
   上記の例では、すべて 3.3.0 を指定しています。

OpenSearch の設定
---------------

``config\opensearch.yml`` をテキストエディタで開き、以下の設定を追加します。

::

    # 設定同期用のパス（絶対パスで指定）
    configsync.config_path: C:/opensearch-3.3.0/data/config/

    # セキュリティプラグインの無効化（開発環境のみ）
    plugins.security.disabled: true

.. warning::

   **セキュリティに関する重要な注意**

   ``plugins.security.disabled: true`` は、開発環境やテスト環境でのみ使用してください。
   本番環境では、OpenSearch のセキュリティプラグインを有効にし、適切な認証・認可設定を行ってください。
   詳細は :doc:`security` を参照してください。

.. note::

   Windows の場合、パスの区切り文字は ``\`` ではなく ``/`` を使用してください。
   ``C:\opensearch-3.3.0\data\config\`` ではなく ``C:/opensearch-3.3.0/data/config/`` と記述します。

.. tip::

   その他の推奨設定::

       cluster.name: fess-cluster
       node.name: fess-node-1
       network.host: 0.0.0.0
       discovery.type: single-node

ステップ 2: Fess のインストール
=============================

Fess のダウンロード
-----------------

1. `ダウンロードサイト <https://fess.codelibs.org/ja/downloads.html>`__ から Windows 用の ZIP パッケージをダウンロードします。

2. ダウンロードした ZIP ファイルを任意のディレクトリに展開します。

   例::

       C:\fess-15.3.0

   .. note::

      パスに日本語や空白文字が含まれないディレクトリを選択することを推奨します。

Fess の設定
----------

``bin\fess.in.bat`` をテキストエディタで開き、以下の設定を追加または変更します。

::

    set SEARCH_ENGINE_HTTP_URL=http://localhost:9200
    set FESS_DICTIONARY_PATH=C:/opensearch-3.3.0/data/config/

.. note::

   - OpenSearch を別のホストで実行している場合は、``SEARCH_ENGINE_HTTP_URL`` を適切なホスト名または IP アドレスに変更してください。
   - パスの区切り文字は ``/`` を使用してください。

インストールの確認
----------------

設定ファイルが正しく編集されたことを確認します。

コマンドプロンプトで::

    C:\> findstr "SEARCH_ENGINE_HTTP_URL" C:\fess-15.3.0\bin\fess.in.bat
    C:\> findstr "FESS_DICTIONARY_PATH" C:\fess-15.3.0\bin\fess.in.bat

ステップ 3: 起動
==============

起動手順については、:doc:`run` を参照してください。

Windows サービスとしての登録（オプション）
=======================================

|Fess| と OpenSearch を Windows サービスとして登録することで、システム起動時に自動的に起動するように設定できます。

.. note::

   Windows サービスとして登録するには、サードパーティツール（NSSM など）を使用する必要があります。
   詳細な手順は、各ツールのドキュメントを参照してください。

NSSM を使用した例
----------------

1. `NSSM (Non-Sucking Service Manager) <https://nssm.cc/download>`__ をダウンロードして展開します。

2. OpenSearch をサービスとして登録::

       C:\> nssm install OpenSearch C:\opensearch-3.3.0\bin\opensearch.bat

3. Fess をサービスとして登録::

       C:\> nssm install Fess C:\fess-15.3.0\bin\fess.bat

4. サービスの依存関係を設定（Fess は OpenSearch に依存）::

       C:\> sc config Fess depend= OpenSearch

5. サービスの起動::

       C:\> net start OpenSearch
       C:\> net start Fess

ファイアウォール設定
==================

Windows Defender ファイアウォールで、必要なポートを開放します。

1. 「コントロールパネル」→「Windows Defender ファイアウォール」→「詳細設定」を開く

2. 「受信の規則」で新しい規則を作成

   - 規則の種類: ポート
   - プロトコルおよびポート: TCP、8080
   - 操作: 接続を許可する
   - 名前: Fess Web Interface

または、PowerShell で実行::

    PS C:\> New-NetFirewallRule -DisplayName "Fess Web Interface" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow

トラブルシューティング
====================

ポート番号の競合
--------------

ポート 8080 または 9200 が既に使用されている場合、以下のコマンドで確認できます::

    C:\> netstat -ano | findstr :8080
    C:\> netstat -ano | findstr :9200

使用中のポート番号を変更するか、競合しているプロセスを停止してください。

パスの長さ制限
------------

Windows では、パスの長さに制限があります。可能な限り短いパスにインストールすることを推奨します。

例::

    C:\opensearch  (推奨)
    C:\Program Files\opensearch-3.3.0  (非推奨 - パスが長い)

Java が認識されない
-----------------

``java -version`` コマンドでエラーが表示される場合：

1. ``JAVA_HOME`` 環境変数が正しく設定されているか確認
2. ``PATH`` 環境変数に ``%JAVA_HOME%\bin`` が含まれているか確認
3. コマンドプロンプトを再起動して設定を反映

次のステップ
==========

インストールが完了したら、以下のドキュメントを参照してください：

- :doc:`run` - |Fess| の起動と初回セットアップ
- :doc:`security` - 本番環境でのセキュリティ設定
- :doc:`troubleshooting` - トラブルシューティング

よくある質問
==========

Q: Windows Server での運用は推奨されますか？
------------------------------------------

A: はい、Windows Server での運用は可能です。
ただし、本番環境では Linux サーバーでの運用を推奨します。
Windows Server で運用する場合は、Windows サービスとして登録し、適切な監視を設定してください。

Q: 64 ビット版と 32 ビット版の違いは？
------------------------------------

A: |Fess| および OpenSearch は 64 ビット版のみをサポートしています。
32 ビット版の Windows では動作しません。

Q: パスに日本語が含まれる場合の対処法は？
--------------------------------------

A: 可能な限り、日本語や空白文字が含まれないパスにインストールしてください。
どうしても日本語パスを使用する必要がある場合は、設定ファイルでパスを適切にエスケープする必要があります。
