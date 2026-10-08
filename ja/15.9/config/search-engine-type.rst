==================
検索エンジンの種別
==================

概要
====

|Fess| は OpenSearch にデータを保存します。 ``search_engine.type`` は、接続先の OpenSearch がどのようなものかを |Fess| に伝える設定です。この設定によって、作成するインデックスの定義と、利用できる機能が決まります。

既定値の ``default`` は、CodeLibs の 4 つのプラグイン（ ``opensearch-analysis-fess`` 、 ``opensearch-analysis-extension`` 、 ``opensearch-minhash`` 、 ``opensearch-configsync`` ）を導入した OpenSearch を前提にします（ :doc:`../install/install` を参照）。プラグインを導入できないマネージドサービスなど、これらのプラグインを含まない素の OpenSearch に接続する場合は、 ``vanilla`` を指定します。

種別
====

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 値
     - 説明
   * - ``default``
     - CodeLibs のプラグインを導入した OpenSearch。既定値です。
   * - ``vanilla``
     - CodeLibs のプラグインを含まない素の OpenSearch。15.9 で追加されました。インデックスの定義は ``fess_indices/_vanilla/`` から読み込まれます。15.8 以前の |Fess| はこの値を認識しないため、15.8 以前では ``cloud`` を指定してください。
   * - ``aws``
     - ``vanilla`` と同じです。Amazon OpenSearch Service で使うための種別です（ :ref:`search-engine-type-aws` を参照）。
   * - ``cloud``
     - ``vanilla`` の非推奨の別名です。起動時に警告をログに出力します。 ``vanilla`` に変更してください。
   * - その他の値
     - ``default`` と同じ扱いです。ただし、 ``fess_indices/_<種別>/`` にある定義ファイルが、 ``fess_indices/`` にある同名のファイルより優先されます。

|Fess| はプラグインの有無を自動では判定しません。種別は利用者が指定します。初回の起動前に設定してください。インデックスの定義はインデックスを作成するときに適用されるため、あとから値を変更しても、作成済みのインデックスは変わりません。

プラグインなしでは使えない機能
==============================

``vanilla`` と ``aws`` （非推奨の ``cloud`` を含む）では、次の機能は使えません。これらに依存する管理画面の項目は表示されません。

* **辞書管理**: [システム > 辞書] は表示されません。辞書の管理画面と辞書の管理用 API （ ``/api/admin/dict/`` ）も使えません。メンテナンスの「辞書の初期化」と「ドキュメントインデックスのリロード」も表示されません。アナライザーは辞書ファイルではなく、インデックスの定義に含まれるルールを使います。
* **検索結果の重複の折り畳み**: 「全般」の「重複結果の折り畳み」は表示されず、常に無効になります。
* **重複文書の検出**: 同じ内容の文書を見つけるための内容の署名が計算されません。ドキュメントレポートの「重複文書」タブは表示されません（「休眠文書」は使えます）。類似文書を探す検索パラメーター ``sdh`` は無視されます。
* **アナライザー**: 日本語・韓国語・簡体字中国語は、CodeLibs のトークナイザーではなく、OpenSearch 標準の Kuromoji・Nori・SmartCN のアナライザーで分割されます。このため、 ``default`` とは分割結果が異なります。ベトナム語（ ``*_vi`` フィールド）と繁体字中国語（ ``*_zh-tw`` フィールド）は、語を一切登録しない空のアナライザーになります。これらの言語の文書も、言語に依存しない ``content`` フィールドと ``title`` フィールドには登録されます。

必要な OpenSearch プラグイン
============================

``vanilla`` と ``aws`` のインデックス定義は、OpenSearch の公式プラグインが提供するアナライザーとベクトルのフィールド型を使います。接続先の OpenSearch に次のプラグインが必要です。

* ``analysis-kuromoji``
* ``analysis-nori``
* ``analysis-smartcn``
* ``opensearch-knn`` （k-NN）

CodeLibs のプラグインは不要です。自分で運用している OpenSearch には、 ``bin/opensearch-plugin install analysis-nori`` のように ``opensearch-plugin install`` で導入します。Amazon OpenSearch Service については :ref:`search-engine-type-aws` を参照してください。

種別が ``vanilla`` または ``aws`` の場合、\ |Fess| は起動時に導入済みのプラグインを一覧します（ ``GET /_cat/plugins`` ）。上のプラグインが 1 つでも欠けていると、欠けているプラグインを示す警告を 1 件ログに出力し、そのまま起動を続けます。サービス側がこの API を許可していないなどでリクエストが失敗した場合は、確認を省略します。

種別の設定
==========

Docker
------

``compose.yaml`` の ``fess01`` サービスに、環境変数 ``SEARCH_ENGINE_TYPE`` を指定します。

::

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "SEARCH_ENGINE_TYPE=vanilla"

``vanilla`` は |Fess| 15.9 以降のイメージで指定できます。それより前のイメージでは ``SEARCH_ENGINE_TYPE=cloud`` を指定してください。そのほかの Docker の設定は :doc:`../install/install-docker` を参照してください。

Docker 以外
-----------

``bin/fess.in.sh`` は ``SEARCH_ENGINE_TYPE`` を読み込みません。次のどちらかの方法で指定します。

* ``fess_config.properties`` に ``search_engine.type`` を書きます（ZIP 版は ``app/WEB-INF/classes/fess_config.properties`` 、RPM/DEB 版は ``/etc/fess/fess_config.properties`` ）。
* ZIP 版の ``bin/fess.in.sh`` （Windows は ``bin\fess.in.bat`` ）で、 ``FESS_JAVA_OPTS`` に JVM オプションを追加します。

::

    # fess_config.properties
    search_engine.type=vanilla

    # bin/fess.in.sh
    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.config.search_engine.type=vanilla"

    REM bin\fess.in.bat
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.config.search_engine.type=vanilla

変更後は |Fess| を再起動します。クローラーなどのジョブのプロセスには |Fess| から設定が引き継がれるため、個別に指定する必要はありません。

接続の設定
==========

OpenSearch への接続は、ほかの種別と同じ方法で設定します。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 設定
     - 説明
   * - ``search_engine.http.url``
     - OpenSearch の HTTP エンドポイント。環境変数 ``SEARCH_ENGINE_HTTP_URL`` を指定した場合は、そちらが優先されます。
   * - ``search_engine.username`` / ``search_engine.password``
     - HTTP Basic 認証のユーザー名とパスワード。両方を指定した場合にだけ使われます。Docker では環境変数 ``SEARCH_ENGINE_USERNAME`` と ``SEARCH_ENGINE_PASSWORD`` で指定します。
   * - ``search_engine.http.ssl.certificate_authorities``
     - HTTPS のエンドポイントのサーバー証明書を検証するための CA 証明書ファイル（X.509）のパス。Java が標準で信頼している CA が発行した証明書であれば不要です。

``fess_config.properties`` の項目は、 ``FESS_JAVA_OPTS`` に ``-Dfess.config.<項目名>`` と指定して上書きすることもできます（ :doc:`../install/install-docker` を参照）。

.. _search-engine-type-aws:

Amazon OpenSearch Service
=========================

Amazon OpenSearch Service のドメインを使う場合は、 ``search_engine.type`` に ``aws`` を指定します（ ``vanilla`` でも同じ動作です）。

前提条件
--------

* ドメインの OpenSearch が 3.x であること。\ |Fess| は起動時にエンジンを確認し、OpenSearch 3 以外の場合は起動しません。
* 「必要な OpenSearch プラグイン」に挙げたプラグインがドメインで使えること。Amazon OpenSearch Service では、Nori はオプションのパッケージです。\ |Fess| を起動する前に、ドメインに関連付けてください。
* エンドポイントが HTTPS であること。
* きめ細かなアクセスコントロールを有効にし、\ |Fess| がサインインする内部ユーザーを作成すること（HTTP Basic 認証）。IAM の認証情報によるリクエストの署名（SigV4）にはまだ対応していないため、IAM で署名したリクエストしか受け付けないドメインは使えません。

設定例
------

::

    search_engine.type=aws
    search_engine.http.url=https://<domain-endpoint>:443
    search_engine.username=<internal-user-name>
    search_engine.password=<password>

起動時の確認
------------

* 種別が ``aws`` の場合も、「必要な OpenSearch プラグイン」で説明したプラグインの確認が行われます。Nori の関連付けを忘れていると、 ``fess.log`` に警告が出力されます。
* ドメインが HTTP 401 または 403 でリクエストを拒否した場合、\ |Fess| は警告をログに出力します。これが原因で起動に失敗したときのエラーメッセージには、ユーザー名、パスワード、ドメインのアクセスポリシーの確認を促す案内が含まれます。

DNS キャッシュの TTL
--------------------

マネージドサービスのエンドポイントは、時間がたつと別の IP アドレスに解決されることがあります。JVM は DNS の解決結果をキャッシュするため、キャッシュ時間を短くしておくと、アドレスの変更に |Fess| が追従できます。 ``-Dsun.net.inetaddr.ttl=5`` （秒）を次の 2 か所に指定します。

1. |Fess| 本体: ``FESS_JAVA_OPTS`` に追加します。

   ::

       FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dsun.net.inetaddr.ttl=5"

2. ジョブのプロセス: クローラー、サジェスト、チャンク、サムネイルの各プロセスは、\ |Fess| が別の JVM として起動するため、 ``FESS_JAVA_OPTS`` を引き継ぎません。 ``fess_config.properties`` の ``jvm.crawler.options`` 、 ``jvm.suggest.options`` 、 ``jvm.chunk.options`` 、 ``jvm.thumbnail.options`` の末尾に、同じオプションを追加します。これらの値は 1 行に 1 つのオプションを書き、各行の末尾は ``\n\`` です。

   ::

       jvm.crawler.options=\
       -Djava.awt.headless=true\n\
       ...
       -Dsun.net.inetaddr.ttl=5\n\

   既存の行の後ろにこの行を追加します。ほかの 3 項目も同様に追加してください。

Docker では、 ``FESS_JAVA_OPTS`` を Compose ファイルの環境変数で指定します。 ``jvm.*.options`` を変更するには、変更した ``fess_config.properties`` をマウントします（ :doc:`../install/install-docker` を参照）。
