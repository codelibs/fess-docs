====================
fess-setup コマンド
====================

``bin/fess-setup`` （Windows では ``bin\fess-setup.bat`` ）は、 |Fess| の ZIP パッケージに同梱されているコマンドです。 |Fess| に必要でありながら配布物に含まれていないもの、つまり |Fess| が必要とするプラグインを入れた OpenSearch、Playwright クローラが使う Node.js、 |Fess| のプラグイン、静的テーマを導入します。インストール状態の診断もできます。

|Fess| のディレクトリで実行します。引数を付けずに実行すると、コマンドの一覧を表示します。

::

    $ cd /path/to/fess-15.9.0
    $ bin/fess-setup <command> [options]

終了コード
==========

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - コード
     - 意味
   * - ``0``
     - コマンドが成功しました。
   * - ``1``
     - コマンドが失敗しました。ダウンロードに失敗した、指定したバージョンが存在しない、このプラットフォーム向けの OpenSearch が配布されていない、 ``check`` が問題を検出した、などの場合です。
   * - ``2``
     - コマンドラインの誤りです。未知のコマンドを指定した、プラグイン名などの引数が不足している、などの場合です。

OpenSearch と Node.js の導入
============================

install opensearch
------------------

::

    $ bin/fess-setup install opensearch [--dest <dir>] [--version <version>] [--keep-bundled-plugins]

この |Fess| が対応するバージョンの OpenSearch を |Fess| のディレクトリの ``opensearch/`` にダウンロードし、 |Fess| が必要とする 4 つのプラグイン（ ``opensearch-analysis-fess`` 、 ``opensearch-analysis-extension`` 、 ``opensearch-minhash`` 、 ``opensearch-configsync`` ）を導入したうえで、その ``config/opensearch.yml`` に次の設定を追記します。

- ``configsync.config_path`` （値はその OpenSearch の ``config/dictionary`` ディレクトリ）
- ``plugins.security.disabled: true``

また、 |Fess| が使用しない同梱プラグイン ``opensearch-security-analytics`` と ``opensearch-performance-analyzer`` を削除します。Docker イメージの OpenSearch と同じ構成です。配布物に含まれないプラグインは何もせずに進みます。

``opensearch.yml`` にすでにある設定は追記しません。また、 ``plugins.security.*`` の設定が 1 つでもある場合は ``plugins.security.disabled: true`` を追記しません。OpenSearch のディレクトリがすでにある場合はダウンロードを省略するため、既存のインストールに対して再実行すると、足りない設定だけが追記されます。

コマンドは追記した設定を表示し、続けて ``bin/fess.in.sh`` がこの OpenSearch を自動で見つけられるかどうかを表示します。 |Fess| のディレクトリの ``opensearch/`` の下で ``config/dictionary`` ディレクトリを持つ OpenSearch がこれ 1 つだけであれば見つけられます。このとき ``bin/fess.in.sh`` （Windows では ``bin\fess.in.bat`` ）が ``FESS_DICTIONARY_PATH`` をそのディレクトリに設定するため、同じホストで動かす OpenSearch であれば、ほかに設定は必要ありません。見つけられない場合は、設定すべき ``SEARCH_ENGINE_HTTP_URL`` と ``FESS_DICTIONARY_PATH`` の値を表示します。設定方法は :doc:`install-linux` または :doc:`install-windows` を参照してください。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - オプション
     - 説明
   * - ``--dest <dir>``
     - OpenSearch の展開先を、 |Fess| のディレクトリの ``opensearch/`` の代わりに指定します。 ``bin/fess.in.sh`` は、このディレクトリの外にある OpenSearch を探しません。
   * - ``--version <version>``
     - 導入する OpenSearch のバージョンです。プラグインも同じバージョンで導入されます。
   * - ``--keep-bundled-plugins``
     - 同梱プラグイン（ ``opensearch-security-analytics`` 、 ``opensearch-performance-analyzer`` ）を削除せず、配布物のまま残します。

OpenSearch の公式配布は Linux 向けと Windows 向けだけです。macOS などほかのプラットフォームでは、何もダウンロードせずに終了コード ``1`` で終了し、Homebrew で OpenSearch を導入して ``install opensearch-plugins`` でプラグインを入れる方法か、Docker を使う方法を案内します。

.. warning::

   ``plugins.security.disabled: true`` を設定した OpenSearch は、認証なしでリクエストを受け付けます。OpenSearch は ``network.host`` を設定しない限りループバックアドレスでのみ待ち受けます。それ以外のアドレスで待ち受ける前に、代わりにセキュリティプラグインを設定してください。詳細は :doc:`security` を参照してください。

install opensearch-plugins
--------------------------

::

    $ bin/fess-setup install opensearch-plugins --opensearch-home <dir> [--version <version>]

すでにある OpenSearch に、 |Fess| が必要とする 4 つのプラグインを導入します。その OpenSearch の ``bin/opensearch-plugin install`` を 4 回実行する代わりに使えます。 ``--opensearch-home`` には OpenSearch のインストールディレクトリを指定します（必須）。 ``--version`` はプラグインのバージョンで、OpenSearch のバージョンと一致させる必要があります。

このコマンドは ``opensearch.yml`` を変更しません。 ``configsync.config_path`` などの設定は、 :doc:`install-linux` または :doc:`install-windows` に従って追加してください。

install nodejs
--------------

::

    $ bin/fess-setup install nodejs [--dest <dir>] [--version <version>]

Playwright クローラが必要とする Node.js を、 |Fess| のディレクトリの ``nodejs/`` にダウンロードします。 ``bin/fess.in.sh`` （Windows では ``bin\fess.in.bat`` ）がこれを見つけて ``PLAYWRIGHT_NODEJS_PATH`` を設定します。 ``--dest`` で |Fess| のディレクトリの外に展開した場合は、代わりに ``bin/fess.in.sh`` に追加する ``PLAYWRIGHT_NODEJS_PATH`` の行を表示します。 ``--version`` で別のバージョンの Node.js を指定できます。Playwright クローラについては :doc:`../config/crawler-advanced` を参照してください。

プラグインの管理
================

以下のコマンドは、 |Fess| のプラグインディレクトリ ``app/WEB-INF/plugin`` を操作します。プラグインを導入、更新、削除した後は |Fess| を再起動してください。プラグインは管理画面の「システム > プラグイン」ページからも管理できます。 :doc:`../admin/plugin-guide` を参照してください。

``install plugin`` 、 ``list plugins`` 、 ``upgrade plugins`` には ``--repository <url>`` を指定できます。指定すると、バージョンの一覧、jar、チェックサムをすべてその 1 つの Maven リポジトリ（社内のミラーなど）から取得し、既定のリリースリポジトリ、スナップショットリポジトリ、GitHub は使用しません。

install plugin
--------------

::

    $ bin/fess-setup install plugin <name>[:<version>]... [--version <version>] [--repository <url>]

``fess-script-groovy`` や ``fess-ds-git`` などの |Fess| プラグインを 1 つ以上導入します。バージョンを付けない名前には、この |Fess| 向けにビルドされた最新のバージョンが導入されます。 ``<name>:<version>`` でそのプラグインのバージョンを固定でき、 ``--version`` はバージョンを付けなかった名前すべてに使われます。新しいバージョンの導入が完了した後に、同じプラグインの以前のバージョンが削除されます。

jar はプラグインの GitHub リリースから取得し、リリースに該当するファイルがない場合は Maven リポジトリから取得します。いずれも Maven リポジトリが公開している SHA-1 チェックサムで検証します。 |Fess| の開発版では、同じ系列のスナップショットビルドも導入対象になり、そちらが優先されます。

使用例は :doc:`../admin/plugin-guide` を参照してください。

list plugins
------------

::

    $ bin/fess-setup list plugins [--repository <url>]

この |Fess| 向けに公開されているプラグインを一覧表示し、導入済みのものには ``(installed: <version>)`` を付けます。導入済みでもリポジトリに公開されていないプラグイン（ローカルでビルドした jar など）は、別に一覧表示します。 |Fess| の開発版では、スナップショットリポジトリも参照します。

list installed
--------------

::

    $ bin/fess-setup list installed

導入済みのプラグインとそのバージョンを、リポジトリに問い合わせずに一覧表示します。

upgrade plugins
---------------

::

    $ bin/fess-setup upgrade plugins [--repository <url>]

導入済みのすべてのプラグインを、この |Fess| に合うバージョンで導入し直します。すでにそのバージョンになっているプラグインはそのままです。 ``app/WEB-INF/plugin`` のプラグインは特定の |Fess| のリリース向けにビルドされているため、 |Fess| をアップグレードした後に実行してください。

remove plugin
-------------

::

    $ bin/fess-setup remove plugin <name>...

指定したプラグインの jar を削除します。導入されていない名前はその旨を表示するだけで、終了コードには影響しません。

テーマの管理
============

これらのコマンドは |Fess| のインストールディレクトリの ``app/themes`` を対象とします。テーマをインストールまたは削除したあとは |Fess| を再起動するか、[システム > テーマ] ページの [再読み込み] をクリックしてください。テーマは同じページからアップロードすることもできます。 :doc:`../admin/theme-guide` を参照してください。

テーマのバージョンは、そのテーマが対象とする |Fess| の系列を表します。つまり ``15.9.0`` は |Fess| 15.9 用のテーマです。そのためバージョンを付けずに名前だけを指定すると、プラグインの場合と同じように、この |Fess| 用に作られたテーマが選ばれます。

install theme
-------------

::

    $ bin/fess-setup install theme <name>[:<version>]... [--version <version>] [--repository <url>]

``docuforge`` や ``voicebox`` などの静的テーマをインストールします。バージョンを付けない名前は、この |Fess| 用に作られた最新のものをインストールします。 ``<name>:<version>`` はそのテーマのバージョンを固定し、 ``--version`` は自分のバージョンを持たないすべての名前に適用されます。

アーカイブは Maven リポジトリが公開している SHA-1 チェックサムと照合され、 ``app/themes/<name>`` に展開されます。同じ名前ですでにインストールされているテーマは、管理画面から置き換えた場合と同じ期間バックアップとして保持されます（既定 7 日、 ``theme.upload.attic.retention.days`` ）。

ダウンロード・展開・マニフェストの検査は、インストール済みのものに手を触れる前にすべて行われます。そのため、インストールに失敗してもすでにあるテーマはそのまま残ります。 ``theme.yml`` が別のテーマを名乗っているアーカイブは拒否されます。

list themes
-----------

::

    $ bin/fess-setup list themes [--repository <url>]

この |Fess| 向けに公開されているテーマを一覧表示し、インストール済みのものには ``(installed: <version>)`` を付けます。インストールされているがリポジトリの一覧に無いテーマは、別に表示されます。

この一覧はリポジトリのディレクトリ索引から読み取ります。索引は定期的に生成されるため、読み取れないことがあります。その場合は試みた URL を報告したうえで、インストール済みのテーマは引き続き表示します。索引に載っているかどうかにかかわらず、名前を指定すればテーマはインストールできます。

remove theme
------------

::

    $ bin/fess-setup remove theme <name>...

指定したテーマを ``app/themes`` から削除します。それぞれ保持期間のあいだバックアップとして残ります。インストールされていない名前は報告されますが、終了コードは変わりません。

削除したテーマがデフォルトテーマだった場合、別のテーマを選ぶまで |Fess| は同梱の ``bootstrap`` テーマにフォールバックします。

インストール状態の確認
======================

list
----

::

    $ bin/fess-setup list

``install`` でダウンロードするコンポーネント（ ``opensearch`` と ``nodejs`` ）を、それぞれのバージョンとともに表示します。

check
-----

::

    $ bin/fess-setup check [--url <engine url>] [--playwright]

インストール状態を診断し、確認項目ごとに ``OK`` 、 ``WARN`` 、 ``FAIL`` のいずれかを付けて 1 行ずつ表示します。

- 検索エンジン: 接続できるか、バージョン（ノード間でバージョンが異なる場合は警告）、 |Fess| が必要とする 4 つのプラグインが導入されているか、 ``configsync`` が応答するか
- |Fess| : プラグインディレクトリが存在して書き込めるか、導入済みの各プラグイン（別の |Fess| のリリース向けのものと、2 つのバージョンが導入されているものは失敗）、 |Fess| のディレクトリの ``nodejs/`` に Node.js が導入されているか

検索エンジンの URL は ``--url`` 、指定がなければ環境変数 ``SEARCH_ENGINE_HTTP_URL`` 、それもなければ ``http://localhost:9200`` です。 ``bin/fess-setup`` は ``bin/fess.in.sh`` を読まないため、OpenSearch がほかの場所にある場合は ``--url`` を指定してください。Node.js がないことは報告されるだけですが、 ``--playwright`` を指定すると失敗として扱われます。

失敗した項目がなければ、警告があっても終了コード ``0`` で終了します。失敗した項目があれば終了コード ``1`` で終了します。
