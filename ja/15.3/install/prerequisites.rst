============
システム要件
============

このページでは、 |Fess| を実行するために必要なハードウェアおよびソフトウェア要件について説明します。

ハードウェア要件
==============

最小要件
--------

以下は、評価および開発環境での最小要件です：

- CPU: 2コア以上
- メモリ: 4GB以上
- ディスク容量: 10GB以上の空き容量

推奨要件
--------

本番環境では、以下のスペックを推奨します：

- CPU: 4コア以上
- メモリ: 8GB以上（インデックスサイズに応じて増設）
- ディスク容量:

  - システム領域: 20GB以上
  - データ領域: インデックスサイズの3倍以上（レプリカを含む）

- ネットワーク: 1Gbps以上

.. note::

   インデックスサイズが大きくなる場合や、高頻度のクロールを実行する場合は、
   メモリとディスク容量を適切に増設してください。

ソフトウェア要件
==============

オペレーティングシステム
--------------------

|Fess| は以下のオペレーティングシステムで動作します：

**Linux**

- Red Hat Enterprise Linux 8 以降
- CentOS 8 以降
- Ubuntu 20.04 LTS 以降
- Debian 11 以降
- その他の Linux ディストリビューション（Java 21 が実行可能な環境）

**Windows**

- Windows Server 2019 以降
- Windows 10 以降

**その他**

- macOS 11 (Big Sur) 以降（開発環境のみ推奨）
- Docker が実行可能な環境

必須ソフトウェア
--------------

インストール方法により、以下のソフトウェアが必要です：

TAR.GZ/ZIP/RPM/DEB 版
~~~~~~~~~~~~~~~~~~~~

- **Java 21**: `Eclipse Temurin <https://adoptium.net/temurin>`__ を推奨

  - OpenJDK 21 以降
  - Eclipse Temurin 21 以降

- **OpenSearch 3.3.0**: 本番環境では必須（組み込み版は非推奨）

  - 対応バージョン: OpenSearch 3.3.0
  - その他のバージョンではプラグインの互換性に注意が必要

Docker 版
~~~~~~~~~

- **Docker**: 20.10 以降
- **Docker Compose**: 2.0 以降

ネットワーク要件
==============

必要なポート
----------

|Fess| が使用する主なポートは以下の通りです：

.. list-table::
   :header-rows: 1
   :widths: 15 15 50

   * - ポート
     - プロトコル
     - 用途
   * - 8080
     - HTTP
     - |Fess| Web インターフェース（検索画面・管理画面）
   * - 9200
     - HTTP
     - OpenSearch HTTP API（|Fess| から OpenSearch への通信）
   * - 9300
     - TCP
     - OpenSearch トランスポート通信（クラスター構成時）

.. warning::

   本番環境では、外部からポート 9200 および 9300 への直接アクセスを制限することを強く推奨します。
   これらのポートは |Fess| と OpenSearch 間の内部通信にのみ使用されるべきです。

ファイアウォール設定
------------------

|Fess| を外部からアクセス可能にする場合、ポート 8080 を開放する必要があります。

**Linux (firewalld の場合)**

::

    $ sudo firewall-cmd --permanent --add-port=8080/tcp
    $ sudo firewall-cmd --reload

**Linux (iptables の場合)**

::

    $ sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
    $ sudo iptables-save

ブラウザー要件
============

|Fess| の管理画面および検索画面には、以下のブラウザーを推奨します：

- Google Chrome（最新版）
- Mozilla Firefox（最新版）
- Microsoft Edge（最新版）
- Safari（最新版）

.. note::

   Internet Explorer はサポートされていません。

前提条件チェックリスト
====================

インストール前に、以下の項目を確認してください：

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 確認項目
     - 状態
   * - ハードウェア要件を満たしているか
     - □
   * - Java 21 がインストールされているか（Docker 版以外）
     - □
   * - Docker がインストールされているか（Docker 版）
     - □
   * - 必要なポートが利用可能か
     - □
   * - ファイアウォール設定が適切か
     - □
   * - ディスク容量に十分な空きがあるか
     - □
   * - ネットワーク接続が正常か（外部サイトのクロールを行う場合）
     - □

次のステップ
==========

システム要件を確認したら、ご利用の環境に応じたインストール手順に進んでください：

- :doc:`install-linux` - Linux (TAR.GZ/RPM/DEB) 向けインストール
- :doc:`install-windows` - Windows (ZIP) 向けインストール
- :doc:`install-docker` - Docker 向けインストール
- :doc:`install` - インストール方法の概要
