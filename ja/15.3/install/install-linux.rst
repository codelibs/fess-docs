==================================
Linux へのインストール (詳細手順)
==================================

このページでは、Linux 環境への |Fess| のインストール手順を説明します。
TAR.GZ、RPM、DEB の各パッケージ形式に対応しています。

.. warning::

   本番環境では、組み込み OpenSearch での稼働は推奨しません。
   必ず外部の OpenSearch サーバーを構築してください。

前提条件
========

- :doc:`prerequisites` に記載されているシステム要件を満たしていること
- Java 21 がインストールされていること
- OpenSearch 3.3.2 を利用可能な状態にすること（または新規インストール）

インストール方法の選択
====================

Linux 環境では、以下のインストール方法から選択できます：

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 方式
     - 推奨環境
     - 特徴
   * - TAR.GZ
     - 開発環境、カスタマイズが必要な環境
     - 任意のディレクトリに展開可能
   * - RPM
     - RHEL、CentOS、Fedora 系
     - systemd によるサービス管理が可能
   * - DEB
     - Debian、Ubuntu 系
     - systemd によるサービス管理が可能

TAR.GZ 版でのインストール
========================

ステップ 1: OpenSearch のインストール
----------------------------------

1. OpenSearch のダウンロード

   `Download OpenSearch <https://opensearch.org/downloads.html>`__ から TAR.GZ 版をダウンロードします。

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.tar.gz
       $ tar -xzf opensearch-3.3.2-linux-x64.tar.gz
       $ cd opensearch-3.3.2

   .. note::

      この例では OpenSearch 3.3.2 を使用しています。
      バージョンは |Fess| の対応バージョンを確認してください。

2. OpenSearch プラグインのインストール

   |Fess| が必要とするプラグインをインストールします。

   ::

       $ cd /path/to/opensearch-3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.1
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.1
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.1

   .. important::

      プラグインのバージョンは OpenSearch のバージョンと一致させる必要があります。
      上記の例では、すべて 3.3.2 を指定しています。

3. OpenSearch の設定

   ``config/opensearch.yml`` に以下の設定を追加します。

   ::

       # 設定同期用のパス（絶対パスで指定）
       configsync.config_path: /path/to/opensearch-3.3.2/data/config/

       # セキュリティプラグインの無効化（開発環境のみ）
       plugins.security.disabled: true

   .. warning::

      **セキュリティに関する重要な注意**

      ``plugins.security.disabled: true`` は、開発環境やテスト環境でのみ使用してください。
      本番環境では、OpenSearch のセキュリティプラグインを有効にし、適切な認証・認可設定を行ってください。
      詳細は :doc:`security` を参照してください。

   .. tip::

      クラスター名やネットワーク設定など、その他の設定は環境に応じて調整してください。
      設定例::

          cluster.name: fess-cluster
          node.name: fess-node-1
          network.host: 0.0.0.0
          discovery.type: single-node

ステップ 2: Fess のインストール
-----------------------------

1. Fess のダウンロードと展開

   `ダウンロードサイト <https://fess.codelibs.org/ja/downloads.html>`__ から TAR.GZ 版をダウンロードします。

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.tar.gz
       $ tar -xzf fess-15.3.2.tar.gz
       $ cd fess-15.3.2

2. Fess の設定

   ``bin/fess.in.sh`` を編集し、OpenSearch への接続情報を設定します。

   ::

       $ vi bin/fess.in.sh

   以下の設定を追加または変更します::

       # OpenSearch の HTTP エンドポイント
       SEARCH_ENGINE_HTTP_URL=http://localhost:9200

       # 辞書ファイルの配置パス（OpenSearch の configsync.config_path と同じ）
       FESS_DICTIONARY_PATH=/path/to/opensearch-3.3.2/data/config/

   .. note::

      OpenSearch を別のホストで実行している場合は、
      ``SEARCH_ENGINE_HTTP_URL`` を適切なホスト名または IP アドレスに変更してください。
      例: ``SEARCH_ENGINE_HTTP_URL=http://192.168.1.100:9200``

3. インストールの確認

   設定ファイルが正しく編集されたことを確認します::

       $ grep "SEARCH_ENGINE_HTTP_URL" bin/fess.in.sh
       $ grep "FESS_DICTIONARY_PATH" bin/fess.in.sh

ステップ 3: 起動
--------------

起動手順については、:doc:`run` を参照してください。

RPM 版でのインストール
====================

RPM 版は、Red Hat Enterprise Linux、CentOS、Fedora などの RPM ベースの Linux ディストリビューションで使用します。

ステップ 1: OpenSearch のインストール
----------------------------------

1. OpenSearch RPM のダウンロードとインストール

   `Download OpenSearch <https://opensearch.org/downloads.html>`__ から RPM パッケージをダウンロードしてインストールします。

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.rpm
       $ sudo rpm -ivh opensearch-3.3.2-linux-x64.rpm

   または、リポジトリを追加してインストールすることもできます。
   詳細は `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/rpm/>`__ を参照してください。

2. OpenSearch プラグインのインストール

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.1

3. OpenSearch の設定

   ``/etc/opensearch/opensearch.yml`` に以下の設定を追加します。

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   追加する設定::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      本番環境では ``plugins.security.disabled: true`` を使用しないでください。
      :doc:`security` を参照して、適切なセキュリティ設定を行ってください。

ステップ 2: Fess のインストール
-----------------------------

1. Fess RPM のインストール

   `ダウンロードサイト <https://fess.codelibs.org/ja/downloads.html>`__ から RPM パッケージをダウンロードしてインストールします。

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.rpm
       $ sudo rpm -ivh fess-15.3.2.rpm

2. Fess の設定

   ``/usr/share/fess/bin/fess.in.sh`` を編集します。

   ::

       $ sudo vi /usr/share/fess/bin/fess.in.sh

   以下の設定を追加または変更します::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

3. サービスの登録

   **chkconfig を使用する場合**::

       $ sudo /sbin/chkconfig --add opensearch
       $ sudo /sbin/chkconfig --add fess

   **systemd を使用する場合**（推奨）::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

ステップ 3: 起動
--------------

起動手順については、:doc:`run` を参照してください。

DEB 版でのインストール
====================

DEB 版は、Debian、Ubuntu などの DEB ベースの Linux ディストリビューションで使用します。

ステップ 1: OpenSearch のインストール
----------------------------------

1. OpenSearch DEB のダウンロードとインストール

   `Download OpenSearch <https://opensearch.org/downloads.html>`__ から DEB パッケージをダウンロードしてインストールします。

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.deb
       $ sudo dpkg -i opensearch-3.3.2-linux-x64.deb

   または、リポジトリを追加してインストールすることもできます。
   詳細は `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/debian/>`__ を参照してください。

2. OpenSearch プラグインのインストール

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.1

3. OpenSearch の設定

   ``/etc/opensearch/opensearch.yml`` に以下の設定を追加します。

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   追加する設定::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      本番環境では ``plugins.security.disabled: true`` を使用しないでください。
      :doc:`security` を参照して、適切なセキュリティ設定を行ってください。

ステップ 2: Fess のインストール
-----------------------------

1. Fess DEB のインストール

   `ダウンロードサイト <https://fess.codelibs.org/ja/downloads.html>`__ から DEB パッケージをダウンロードしてインストールします。

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.deb
       $ sudo dpkg -i fess-15.3.2.deb

2. Fess の設定

   ``/usr/share/fess/bin/fess.in.sh`` を編集します。

   ::

       $ sudo vi /usr/share/fess/bin/fess.in.sh

   以下の設定を追加または変更します::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

3. サービスの登録

   systemd を使用してサービスを有効化します::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

ステップ 3: 起動
--------------

起動手順については、:doc:`run` を参照してください。

インストール後の確認
==================

インストールが完了したら、以下を確認してください：

1. **設定ファイルの確認**

   - OpenSearch の設定ファイル（opensearch.yml）
   - Fess の設定ファイル（fess.in.sh）

2. **ディレクトリのパーミッション**

   設定で指定したディレクトリが存在し、適切な権限が設定されていることを確認します。

   TAR.GZ 版の場合::

       $ ls -ld /path/to/opensearch-3.3.2/data/config/

   RPM/DEB 版の場合::

       $ sudo ls -ld /var/lib/opensearch/data/config/

3. **Java のバージョン確認**

   ::

       $ java -version

   Java 21 以降がインストールされていることを確認します。

次のステップ
==========

インストールが完了したら、以下のドキュメントを参照してください：

- :doc:`run` - |Fess| の起動と初回セットアップ
- :doc:`security` - 本番環境でのセキュリティ設定
- :doc:`troubleshooting` - トラブルシューティング

よくある質問
==========

Q: OpenSearch のバージョンは他のバージョンでも動作しますか？
---------------------------------------------------------

A: |Fess| は特定のバージョンの OpenSearch に依存しています。
プラグインの互換性を確保するため、推奨されるバージョン（3.3.2）を使用することを強く推奨します。
他のバージョンを使用する場合は、プラグインのバージョンも適切に調整する必要があります。

Q: 複数の Fess インスタンスで同じ OpenSearch を共有できますか？
--------------------------------------------------------------

A: 可能ですが、推奨されません。各 Fess インスタンスには専用の OpenSearch クラスターを用意することを推奨します。
複数の Fess インスタンスで OpenSearch を共有する場合は、インデックス名の衝突に注意してください。

Q: OpenSearch をクラスター構成にする方法は？
------------------------------------------

A: OpenSearch の公式ドキュメント `Cluster formation <https://opensearch.org/docs/latest/tuning-your-cluster/cluster/>`__ を参照してください。
クラスター構成にする場合は、``discovery.type: single-node`` の設定を削除し、適切なクラスター設定を追加する必要があります。
