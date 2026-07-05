==================
セキュリティ設定
==================

このページでは、本番環境で |Fess| を安全に運用するために推奨されるセキュリティ設定について説明します。

.. danger::

   **セキュリティは非常に重要です**

   本番環境では、このページに記載されている全てのセキュリティ設定を実施することを強く推奨します。
   セキュリティ設定を怠ると、不正アクセス、データ漏洩、システムの侵害などのリスクが高まります。

必須のセキュリティ設定
====================

管理者パスワードの変更
--------------------

デフォルトの管理者パスワード（``admin`` / ``admin``）は必ず変更してください。

**手順:**

1. 管理画面にログイン: http://localhost:8080/admin
2. 「ユーザー」→「ユーザー」をクリック
3. ``admin`` ユーザーを選択
4. 強力なパスワードを設定
5. 「更新」ボタンをクリック

.. note::

   一度 ``admin`` から変更したパスワードは、``admin`` のような単純な文字列には戻せません（``password.invalid.admin.passwords`` により管理者パスワードのブラックリストが設定されています）。また、初回起動前であれば ``fess_config.properties`` の ``index.user.initial_password`` で ``admin`` ユーザーの初期パスワードを変更できます。

**推奨パスワードポリシー:**

|Fess| はパスワードの最小・最大文字数と文字種の要件を強制する機能を備えています。``fess_config.properties`` で以下のプロパティを設定してください（括弧内は既定値）。

- ``password.min.length`` （既定値: ``8``）: 最小文字数。12 以上を推奨します。
- ``password.max.length`` （既定値: ``100``）: 最大文字数。
- ``password.require.uppercase`` （既定値: ``false``）: 英大文字を必須にする。
- ``password.require.lowercase`` （既定値: ``false``）: 英小文字を必須にする。
- ``password.require.digit`` （既定値: ``false``）: 数字を必須にする。
- ``password.require.special.char`` （既定値: ``false``）: 記号を必須にする。

.. note::

   既定では最小文字数は ``8`` で、文字種の要件はすべて無効です。パスワード強度を高めるには、上記のプロパティを明示的に設定してください。なお、|Fess| にはパスワードの有効期限（定期変更の強制）機能はありません。定期的なパスワード変更を運用ルールとする場合は、手動で対応してください。

OpenSearch のセキュリティプラグイン有効化
--------------------------------------

**手順:**

1. ``opensearch.yml`` から以下の行を削除またはコメントアウト::

       # plugins.security.disabled: true

2. セキュリティプラグインの設定::

       plugins.security.allow_default_init_securityindex: true
       plugins.security.authcz.admin_dn:
         - CN=admin,OU=SSL,O=Test,L=Test,C=DE

3. TLS/SSL証明書の設定

4. OpenSearch を再起動

5. |Fess| 側で OpenSearch への接続情報を設定します。

   接続先 URL は環境変数 ``SEARCH_ENGINE_HTTP_URL`` で指定します（``bin/fess.in.sh`` またはサービスの環境設定ファイルを編集します。既定値は ``fess_config.properties`` の ``search_engine.http.url``）::

       SEARCH_ENGINE_HTTP_URL=https://opensearch:9200

   認証情報は ``fess_config.properties`` の以下のプロパティで指定します（``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD`` という環境変数は存在しません）::

       search_engine.username=admin
       search_engine.password=<strong_password>

詳細は `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__ を参照してください。

HTTPS の有効化
------------

HTTP 通信は暗号化されていないため、盗聴や改ざんのリスクがあります。本番環境では必ず HTTPS を使用してください。

**方法 1: リバースプロキシの使用（推奨）**

Nginx または Apache を |Fess| の前段に配置し、HTTPS 終端を行います。

Nginx の設定例::

    server {
        listen 443 ssl http2;
        server_name your-fess-domain.com;

        ssl_certificate /path/to/cert.pem;
        ssl_certificate_key /path/to/key.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

**方法 2: Fess 自体で HTTPS を設定**

``tomcat_config.properties`` に以下を追加::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.SSLEnabled=true
    tomcat.certificateKeystoreFile=[キーストアファイルのパス]
    tomcat.certificateKeystorePassword=[キーストアファイル作成時に指定したパスワード]
    tomcat.certificateKeyAlias=[証明書のエイリアス]
    tomcat.sslProtocol=[SSL プロトコル（例: TLS）]
    tomcat.enabledProtocols=有効なプロトコル一覧（カンマ区切り）（例: TLSv1.2,TLSv1.1,TLSv1）

推奨のセキュリティ設定
====================

ファイアウォール設定
------------------

必要なポートのみを開放し、不要なポートは閉じてください。

**開放すべきポート:**

- **8080** (または HTTPS の 443): |Fess| Web インターフェース（外部からのアクセスが必要な場合）
- **22**: SSH（管理用、信頼できる IP アドレスからのみ）

**閉じるべきポート:**

- **9200, 9300**: OpenSearch（内部通信のみ、外部からのアクセスを遮断）

Linux (firewalld) の設定例::

    $ sudo firewall-cmd --permanent --add-service=http
    $ sudo firewall-cmd --permanent --add-service=https
    $ sudo firewall-cmd --permanent --remove-service=opensearch  # カスタムサービスの場合
    $ sudo firewall-cmd --reload

IP アドレス制限::

    $ sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="8080" protocol="tcp" accept'

アクセス制御の設定
----------------

管理画面へのアクセスを特定の IP アドレスに制限することを検討してください。

Nginx でのアクセス制限例::

    location /admin {
        allow 192.168.1.0/24;
        deny all;

        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
    }

ロールとアクセス制御
------------------

|Fess| には、あらかじめ 2 つのロールが用意されています。

- ``admin``: 管理画面を含むすべての操作が可能な管理者ロール
- ``guest``: 未ログイン（匿名）ユーザーに割り当てられるロール

これら以外のロールは、管理画面から自由に作成できます。|Fess| のロールは名前のみを持つタグであり、主に検索結果へのアクセス制御（どのドキュメントを表示できるか）に使用されます。ロール自体に「クロール設定の管理」「検索結果の編集」といった個別の管理権限が紐づくわけではありません。

最小権限の原則に従い、管理者ロール（``admin``）は管理業務を行うユーザーにのみ付与し、一般の検索ユーザーには付与しないでください。

**手順:**

1. 管理画面で「ユーザー」→「ロール」をクリック
2. 必要なロールを作成
3. 「ユーザー」→「ユーザー」でユーザーにロールを割り当て

監査ログ
------

認証や管理操作などのシステムの操作履歴は、監査ログとしてデフォルトで記録されます。監査ログは ``log4j2.xml`` に定義された ``fess.log.audit`` ロガーによって出力され、既定の出力先は ``audit.log`` です。

デフォルトで有効になっているため、追加の設定は不要です。出力先やログレベルをカスタマイズする場合は、``log4j2.xml`` の以下の定義を編集してください::

    <Logger name="fess.log.audit" additivity="false" level="info">
        <AppenderRef ref="AuditFile"/>
    </Logger>

定期的なセキュリティアップデート
------------------------------

|Fess| および OpenSearch のセキュリティアップデートを定期的に適用してください。

**推奨手順:**

1. セキュリティ情報を定期的に確認

   - `Fess リリース情報 <https://github.com/codelibs/fess/releases>`__
   - `OpenSearch セキュリティアドバイザリ <https://opensearch.org/security.html>`__

2. テスト環境でアップデートを検証
3. 本番環境にアップデートを適用

データ保護
========

バックアップの暗号化
------------------

バックアップデータには機密情報が含まれる可能性があります。バックアップファイルを暗号化して保存してください。

暗号化バックアップの例::

    $ tar czf fess-backup.tar.gz /var/lib/opensearch /etc/fess
    $ gpg --symmetric --cipher-algo AES256 fess-backup.tar.gz

セキュリティベストプラクティス
============================

最小権限の原則
------------

- Fess および OpenSearch を root ユーザーで実行しない
- 専用のユーザーアカウントで実行
- 必要最小限のファイルシステム権限を付与

ネットワーク分離
--------------

- OpenSearch をプライベートネットワークに配置
- 内部通信には VPN またはプライベートネットワークを使用
- DMZ に |Fess| の Web インターフェースのみを配置

定期的なセキュリティ監査
----------------------

- アクセスログを定期的に確認
- 異常なアクセスパターンを検出
- 定期的に脆弱性スキャンを実施

セキュリティヘッダーの設定
------------------------

必要に応じて、Nginx または Apache でセキュリティヘッダーを設定してください::

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'" always;

セキュリティチェックリスト
========================

本番環境にデプロイする前に、以下のチェックリストを確認してください：

基本設定
--------

- [ ] 管理者パスワードを変更済み
- [ ] HTTPS を有効化済み
- [ ] デフォルトのポート番号を変更（オプション）

ネットワークセキュリティ
----------------------

- [ ] ファイアウォールで不要なポートを閉鎖済み
- [ ] 管理画面へのアクセスを IP 制限済み（可能な場合）
- [ ] OpenSearch へのアクセスを内部ネットワークのみに制限済み

アクセス制御
----------

- [ ] ロールとアクセス権限を適切に設定済み（管理者ロールを必要なユーザーのみに付与）
- [ ] 不要なユーザーアカウントを削除済み
- [ ] パスワードポリシーを設定済み

監視とログ
--------

- [ ] 監査ログが有効になっていることを確認済み
- [ ] ログの保存期間を設定済み
- [ ] ログ監視の仕組みを構築済み（可能な場合）

バックアップとリカバリ
--------------------

- [ ] 定期的なバックアップスケジュールを設定済み
- [ ] バックアップデータを暗号化済み
- [ ] リストア手順を検証済み

アップデートとパッチ管理
----------------------

- [ ] セキュリティアップデートの通知を受信する仕組みを構築済み
- [ ] アップデート手順を文書化済み
- [ ] テスト環境でアップデートを検証する体制を構築済み

セキュリティインシデント対応
==========================

セキュリティインシデントが発生した場合の対応手順：

1. **インシデントの検知**

   - ログの確認
   - 異常なアクセスパターンの検出
   - システムの挙動異常の確認

2. **初期対応**

   - 影響範囲の特定
   - 被害の拡大防止（該当サービスの停止など）
   - 証拠の保全

3. **調査と分析**

   - ログの詳細分析
   - 侵入経路の特定
   - 漏洩した可能性のあるデータの特定

4. **復旧**

   - 脆弱性の修正
   - システムの復旧
   - 監視の強化

5. **事後対応**

   - インシデントレポートの作成
   - 再発防止策の実施
   - 関係者への報告

参考情報
======

- `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__
- `OWASP Top 10 <https://owasp.org/www-project-top-ten/>`__
- `CIS Benchmarks <https://www.cisecurity.org/cis-benchmarks/>`__

セキュリティに関する質問や問題がある場合は、以下にお問い合わせください：

- Issues: https://github.com/codelibs/fess/issues
- 商用サポート: https://www.n2sm.net/
