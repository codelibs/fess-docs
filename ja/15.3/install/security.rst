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
2. 「システム」→「ユーザー」をクリック
3. ``admin`` ユーザーを選択
4. 強力なパスワードを設定
5. 「更新」ボタンをクリック

**推奨パスワードポリシー:**

- 最低 12 文字以上
- 英大文字、英小文字、数字、記号を含む
- 辞書にある単語を避ける
- 定期的に変更する（90日ごとを推奨）

OpenSearch のセキュリティプラグイン有効化
--------------------------------------

開発環境では ``plugins.security.disabled: true`` を設定していますが、本番環境では必ずセキュリティプラグインを有効にしてください。

.. warning::

   ``plugins.security.disabled: true`` は開発環境でのみ使用してください。
   本番環境でこの設定を使用すると、OpenSearch への認証なしでアクセス可能になり、深刻なセキュリティリスクとなります。

**手順:**

1. ``opensearch.yml`` から以下の行を削除またはコメントアウト::

       # plugins.security.disabled: true

2. セキュリティプラグインの設定::

       plugins.security.allow_default_init_securityindex: true
       plugins.security.authcz.admin_dn:
         - CN=admin,OU=SSL,O=Test,L=Test,C=DE

3. TLS/SSL証明書の設定

4. OpenSearch を再起動

5. |Fess| の設定を更新して、OpenSearch の認証情報を追加::

       SEARCH_ENGINE_HTTP_URL=https://opensearch:9200
       SEARCH_ENGINE_USERNAME=admin
       SEARCH_ENGINE_PASSWORD=<strong_password>

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

``system.properties`` に以下を追加::

    server.ssl.enabled=true
    server.ssl.key-store=/path/to/keystore.p12
    server.ssl.key-store-password=<password>
    server.ssl.key-store-type=PKCS12

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

ロールベースアクセス制御 (RBAC)
-----------------------------

|Fess| は複数のユーザーロールをサポートしています。最小権限の原則に従って、ユーザーに必要最小限の権限のみを付与してください。

**ロールの種類:**

- **管理者**: すべての権限
- **一般ユーザー**: 検索のみ
- **クローラー管理者**: クロール設定の管理
- **検索結果編集者**: 検索結果の編集

**手順:**

1. 管理画面で「システム」→「ロール」をクリック
2. 必要なロールを作成
3. 「システム」→「ユーザー」でユーザーにロールを割り当て

監査ログの有効化
--------------

システムの操作履歴を記録するために、監査ログを有効にしてください。

設定ファイル（``log4j2.xml``）で監査ログを有効化::

    <Logger name="org.codelibs.fess.audit" level="info" additivity="false">
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

機密情報のマスキング
------------------

クロール対象に機密情報が含まれる場合、インデックス化の前にマスキングすることを検討してください。

|Fess| のスクリプト機能を使用して、特定のパターンをマスキングできます。

例: クレジットカード番号のマスキング::

    # Groovy スクリプトで置換
    content = content.replaceAll(/\d{4}-\d{4}-\d{4}-\d{4}/, "****-****-****-****")

セキュリティベストプラクティス
============================

最小権限の原則
------------

- Fess および OpenSearch を root ユーザーで実行しない
- 専用のユーザーアカウントで実行
- 必要最小限のファイルシステム権限を付与

ネットワーク分離
--------------

- |Fess| と OpenSearch を別のネットワークセグメントに配置
- 内部通信には VPN またはプライベートネットワークを使用
- DMZ に |Fess| の Web インターフェースのみを配置

定期的なセキュリティ監査
----------------------

- アクセスログを定期的に確認
- 異常なアクセスパターンを検出
- 定期的に脆弱性スキャンを実施

セキュリティヘッダーの設定
------------------------

Nginx または Apache でセキュリティヘッダーを設定してください::

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
- [ ] OpenSearch のセキュリティプラグインを有効化済み
- [ ] HTTPS を有効化済み
- [ ] デフォルトのポート番号を変更（オプション）

ネットワークセキュリティ
----------------------

- [ ] ファイアウォールで不要なポートを閉鎖済み
- [ ] 管理画面へのアクセスを IP 制限済み（可能な場合）
- [ ] OpenSearch へのアクセスを内部ネットワークのみに制限済み

アクセス制御
----------

- [ ] ロールベースアクセス制御を設定済み
- [ ] 不要なユーザーアカウントを削除済み
- [ ] パスワードポリシーを設定済み

監視とログ
--------

- [ ] 監査ログを有効化済み
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
