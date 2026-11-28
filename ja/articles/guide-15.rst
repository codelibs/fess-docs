==================================
SSO とアクセス保護で検索基盤を守る
==================================

はじめに
========

社内の検索基盤には、権限で守られた文書が集まります。
利用者に Fess 専用のパスワードを配るのではなく、社内の ID 基盤（IdP）でログインさせ、そのグループで検索結果を絞り込みたい、というのが多くの導入現場での要件です。

本記事では、Fess 15.9 で次の設定を行い、動いていることを確かめるところまでを説明します。

- Entra ID・OpenID Connect・SAML・SPNEGO のいずれかでシングルサインオン（SSO）する
- 「ログインが必要」で、ログインしていない利用者に検索させない
- TLS を終端するリバースプロキシの背後で、Fess に HTTPS を正しく認識させる
- アクセストークンと監査ログ・検索ログの保持期間を見直す

ロールやグループをどう設計し、クロール設定のパーミッションにどう書くかは :doc:`guide-05` で扱います。

SSO はプラグインで提供される
============================

Fess 15.9 では、SSO の認証処理が本体から 4 つのプラグインに分かれました。

.. list-table::
   :header-rows: 1
   :widths: 16 18 18 22 26

   * - 方式
     - プラグイン
     - 「SSOタイプ」（``sso.type``）
     - ユーザー名の出どころ
     - グループ・ロールの出どころ
   * - Microsoft Entra ID
     - ``fess-sso-entraid``
     - Entra ID（``entraid``）
     - サインインしたアカウントのユーザー名（通常は UPN）
     - Microsoft Graph で取得したグループ・ロール
   * - OpenID Connect
     - ``fess-sso-oidc``
     - OpenID Connect（``oic``）
     - ID Token の ``email`` クレーム
     - ID Token の ``groups`` クレーム。ロールは「デフォルトロール」のみ
   * - SAML 2.0
     - ``fess-sso-saml``
     - SAML（``saml``）
     - アサーションの NameID
     - 「グループ属性名」（既定 ``memberOf``）と「ロール属性名」の属性値
   * - SPNEGO（Kerberos）
     - ``fess-sso-spnego``
     - SPNEGO（``spnego``）
     - Kerberos プリンシパルの ``@`` より前
     - ［全般］の LDAP 設定で取得したグループ

OpenID Connect だけは、プラグイン名（``oidc``）と ``sso.type`` の値（``oic``）が異なります。

どの方式も、手順は共通です。

1. プラグインを入れて Fess を再起動する
2. IdP 側に Fess を登録する。戻り先（リダイレクト URI・ACS URL）は ``https://<Fessのホスト>/sso/`` です
3. 管理画面の［システム］>［全般］で、方式ごとのセクションに IdP の情報を入力し、「SSOタイプ」を選んで更新する
4. ブラウザーで ``https://<Fessのホスト>/sso/`` を開き、IdP を経由してログインできることを確かめる

プラグインを入れる
------------------

Docker イメージ（``ghcr.io/codelibs/fess:15.9.0``）には 4 つの SSO プラグインが入っています（``-slim`` の付くイメージには入っていません）。
ZIP・DEB・RPM 版には同梱されないため、［システム］>［プラグイン］の［インストール］から入れるか、次のコマンドで入れます。

::

    $ bin/fess-setup install plugin fess-sso-entraid

導入・削除の後は Fess を再起動します。
プラグインは Fess と同じマイナーバージョン（15.9.x）を使ってください。

プラグインがないまま「SSOタイプ」を選ぶと、 ``/sso/`` はログイン画面に戻るだけになり、 ``fess.log`` に ``No SSO authenticator is registered as ...`` という WARN が 1 回出ます。

設定の保存先
------------

［全般］で入力した値は ``system.properties`` に保存されます（ZIP 版は ``app/WEB-INF/conf/`` 、DEB・RPM 版は ``/etc/fess/``）。
OpenID Connect・SAML・Entra ID の項目はログイン処理のたびに読まれるので、保存すれば再起動なしで使われます。
SPNEGO の項目はプロセス全体で共有されるため、変更後に再起動が必要です。

Docker の ``fess01`` コンテナにはボリュームがなく、 ``docker compose down`` の後に ``up`` すると［全般］の設定が消えます。
コンテナを作り直す前に、［システム情報］>［バックアップ］から ``system.properties`` をダウンロードし、作り直した後に同じ画面からアップロードして戻します。

Entra ID で SSO する
====================

Microsoft 365 を使っている組織では、 ``fess-sso-entraid`` が手軽です。
グループはログイン後に Microsoft Graph から取得されるため、IdP 側でグループクレームを設定する必要はありません。

Entra ID 側の設定
-----------------

Azure Portal の「アプリの登録」で新規登録し、次のように設定します。

- サポートされているアカウントの種類: この組織ディレクトリのみに含まれるアカウント
- リダイレクト URI: プラットフォーム「Web」で ``https://fess.example.com/sso/`` （末尾の ``/`` まで一致させます）
- 「証明書とシークレット」でクライアントシークレットを作成し、値を控える（作成直後しか表示されません）
- 「API のアクセス許可」で Microsoft Graph の委任されたアクセス許可 ``User.Read`` と ``GroupMember.Read.All`` を追加し、管理者の同意を与える

``GroupMember.Read.All`` がないと、入れ子になった親グループを取得できず、 ``fess.log`` に ``Not allowed to read the parent groups of ...`` という警告が出ます。

Fess 側の設定
-------------

［システム］>［全般］の「Entra ID」セクションに入力します。

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 項目
     - キー
     - 値
   * - テナント (IDまたはドメイン)
     - ``entraid.tenant``
     - ディレクトリ（テナント）ID、または ``yourcompany.onmicrosoft.com``
   * - クライアントID
     - ``entraid.client.id``
     - アプリケーション（クライアント）ID
   * - クライアントシークレット
     - ``entraid.client.secret``
     - 作成したシークレットの値
   * - 応答URL
     - ``entraid.reply.url``
     - ``https://fess.example.com/sso/``

最後に「システム」セクションの「SSOタイプ」で「Entra ID」を選び、［更新］を押します。

グループと文書のパーミッションを一致させる
------------------------------------------

Entra ID から得たグループとロールは、その ID（GUID）が必ずパーミッションになります。
加えて、「パーミッションフィールド」（``entraid.permission.fields`` 、既定 ``mail``）に挙げた属性の値もパーミッションになります。

セキュリティグループはメールが無効なので、既定のままでは GUID しかパーミッションになりません。
ファイルサーバーの ACL がグループ名で書かれている場合は、「パーミッションフィールド」を ``mail,displayName`` にします。
ただし ``displayName`` は一意ではないため、Windows の組み込みグループ（``Administrators`` など）と同じ名前のグループがあると、その文書にも一致します。

クロール設定のパーミッションには、取得される値をそのまま ``{group}`` 付きで書きます（例: ``{group}sales@example.com``）。

.. warning::

   「デフォルトロール」（``entraid.default.roles``）はテナントの全ユーザーに付きます。
   ここに ``admin`` を入れると、全員が管理画面に入れるようになります。

OpenID Connect・SAML・SPNEGO で SSO する
========================================

OpenID Connect
--------------

Keycloak や Okta などの OpenID Connect プロバイダーとは ``fess-sso-oidc`` で連携します。
プロバイダー側では、Fess を Web アプリケーション（クライアント）として登録し、リダイレクト URI を ``https://fess.example.com/sso/`` にします。

［全般］の「OpenID Connect」セクションに入力する主な項目は次のとおりです。

- 認証サーバーURL（``oic.auth.server.url``）とトークンサーバーURL（``oic.token.server.url``）: プロバイダーの ``/.well-known/openid-configuration`` にある値を個別に入力します。トークンサーバーURL は ``https`` でなければなりません（``localhost`` ・ ``127.x.x.x`` ・ ``::1`` だけは ``http`` 可）
- クライアントID・クライアントシークレット
- スコープ: ``openid email`` 。ユーザー名は ``email`` クレームから取るため、 ``email`` が必要です
- ベースURL（``oic.base.url``）: ``https://fess.example.com`` 。リダイレクトURL を空にすると ``{ベースURL}/sso/`` になります

グループは ID Token の ``groups`` クレームの値がそのままパーミッションになります。
Entra ID のように親グループをたどることはないため、入れ子のグループが必要ならプロバイダー側でクレームに含めます。
ロールはクレームから取らず、「デフォルトロール」の値だけが付きます。

発行者（``iss``）を検証する ``oic.issuer`` は［全般］に項目がなく、 ``system.properties`` に直接書きます。

SAML
----

``fess-sso-saml`` では、Fess が SP として動きます。
IdP はアサーションをクロスサイトの POST で返すため、既定の ``tomcat.sameSiteCookies = lax`` のままではログインが完了しません。
``tomcat_config.properties`` で次のように変え、Fess を再起動します。

::

    tomcat.sameSiteCookies = none

``none`` は HTTPS でしか使えません。
HTTP のままではログインできなくなるので、先に後述の HTTPS 設定を済ませます。

［全般］の「SAML」セクションに次を入力します。

- SPベースURL（``saml.sp.base.url``）: ``https://fess.example.com`` 。これから SP の Entity ID（``{SPベースURL}/sso/metadata``）と ACS URL（``{SPベースURL}/sso/``）が決まります
- IdPエンティティID・IdP SSO URL・IdP X.509証明書: IdP の管理画面から写します。証明書は ``-----BEGIN CERTIFICATE-----`` の行を除いた Base64 を 1 行で入れます
- グループ属性名（既定 ``memberOf``）・ロール属性名: IdP が送る属性名に合わせます

IdP のメタデータ URL を読み込む機能はありません。
逆に、Fess の SP メタデータは ``https://fess.example.com/sso/metadata`` から取得でき、IdP に読み込ませられます。
ユーザー名は NameID になり、NameID の形式は既定でメールアドレス形式です。
ログインは Fess の ``/sso/`` から始める SP-Initiated のみで、IdP のポータルのタイルから始めるログインは拒否されます。

本番では、 ``system.properties`` に ``saml.security.want_assertions_signed=true`` を追加し、アサーションの署名を必須にします。
署名や暗号化の設定は［全般］に項目がなく、JVM のシステムプロパティでも指定できないため、ファイルに直接書きます。

.. warning::

   「ロール属性名」を設定すると、IdP が送った値がそのまま Fess のロールになります。
   管理者ロールは ``authentication.admin.roles=admin`` なので、IdP が ``admin`` を送ったユーザーは管理者になります。

SPNEGO（Windows 統合認証）
--------------------------

ドメインに参加した Windows からパスワードを入力せずにログインさせるには、``fess-sso-spnego`` を使います。
AD への SPN 登録（``setspn -S HTTP/<Fessのホスト名> <サービスアカウント>``）、 ``app/WEB-INF/classes/`` への ``krb5.conf`` と ``auth_login.conf`` の作成、ブラウザーのイントラネット設定が必要です。
グループは［全般］の「LDAP」セクションの設定で AD から取得します。
手順は `Windows統合認証によるSSO設定 <https://fess.codelibs.org/ja/stable/config/sso-spnego.html>`__ に沿って進め、［全般］の SPNEGO 項目を変えたら再起動します。

SSO が動いていることを確かめる
==============================

まず、ログアウトした状態で ``https://fess.example.com/sso/`` を開き、IdP のログイン画面に移ることを確かめます。

ログインしたら、同じブラウザーで ``https://fess.example.com/api/v2/auth/me`` を開きます。

::

    {"response":{"status":0,"authenticated":true,"user":{"user_id":"taro@example.com", ...
      "groups":[...],"permissions":[...],"admin":false,"permission_state":"RESOLVED"}}}

``groups`` に期待するグループが入っているか、 ``admin`` が意図どおりかを確認します。
Entra ID ではグループの取得がログイン後に行われるため、直後は ``permission_state`` が ``PENDING`` になり、取得が済むと ``RESOLVED`` に変わります。

監査ログ ``audit.log`` にも、 ``LOGIN`` の行がユーザー名とパーミッション付きで記録されます。

ログインに失敗すると、ログイン画面に戻り、「SSOログイン処理に失敗しました。」と表示されます。
原因は ``fess.log`` の WARN（``Failed to process SSO login`` など）に出ます。

SSO の設定を誤っても、 ``/login/`` からローカルの ``admin`` ユーザーでログインして直せます。

.. note::

   ログインしたユーザーには ``{role}guest`` が付きません。
   既定の ``{role}guest`` だけを持つクロール設定の文書は、SSO でログインした利用者の検索結果から消えます。
   パーミッションの組み立て方は :doc:`guide-05` を参照してください。

ログインしていない利用者に検索させない
======================================

［システム］>［全般］の「ログインが必要」を有効にすると、ログインしていない利用者は検索できなくなります。

- SSO が使える状態（プラグインがあり「SSOタイプ」が選ばれている）なら、同梱の ``bootstrap`` テーマの検索画面を開いた利用者は自動的に ``/sso/`` へ送られ、IdP でログインした後に元の検索に戻ります
- SSO がない場合は、検索画面にログインダイアログが表示されます
- ``/api/v2/`` の検索 API も匿名では使えなくなり、アクセストークンを付けた呼び出しだけが通ります

「ログインが必要」を有効にしない場合でも、SSO が使える状態で「ログインリンク表示」が有効なら、検索画面のログインリンクの行き先が ``/sso/`` になります。

HTTPS で公開する
================

リバースプロキシで TLS を終端する
---------------------------------

Nginx などで TLS を終端し、Fess には HTTP で転送する構成では、Fess が受け取るリクエストは ``http://`` に見えます。
このままだと SAML のアサーション検証（``Destination`` の照合）が失敗し、SPNEGO の Basic 認証フォールバックも提示されません。

``tomcat_config.properties`` で、外部から見えるスキームとポートを Fess に伝えます。
このファイルは ZIP 版では ``lib/classes/`` 、DEB・RPM 版と Docker イメージでは ``/etc/fess/`` にあります。

::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.proxyPort=443

プロキシ側では、 ``Host`` ヘッダーを元のまま Fess に渡します（Nginx なら ``proxy_set_header Host $host;``）。
Fess はリクエスト URL のホスト名を ``Host`` ヘッダーから組み立てるためです。

あわせて、 ``fess_config.properties`` の ``session.cookie.secure=true`` でセッション Cookie に ``Secure`` 属性を付けます。
既定（空）では Tomcat の判断に任せますが、TLS をプロキシで終端する本番環境では ``true`` を明示します。
SAML で ``tomcat.sameSiteCookies = none`` を使う場合も、 ``SameSite=None`` の Cookie には ``Secure`` 属性が必要です。

どちらのファイルも、変更後に Fess の再起動が必要です。

Fess で直接 TLS を受ける
------------------------

プロキシを置かない場合は、 ``tomcat_config.properties`` に ``tomcat.SSLEnabled=true``、``tomcat.certificateKeystoreFile``、``tomcat.certificateKeystorePassword``、``tomcat.certificateKeyAlias`` などを設定します。
設定例は `セキュリティ設定 <https://fess.codelibs.org/ja/stable/install/security.html>`__ を参照してください。

OpenSearch のポートを閉じる
---------------------------

docker-fess の ``compose-opensearch3.yaml`` は、セキュリティプラグインが無効な OpenSearch をホストのポート 9200 で公開します。
Fess はコンテナ間のネットワーク（``http://search01:9200``）で接続するため、共有サーバーでは ``search01`` の ``ports`` を外してかまいません。

アクセストークンを管理する
==========================

業務システムから API を呼ぶためのトークンは、［システム］>［アクセストークン］で作ります。
API の呼び出し方は :doc:`guide-11` で扱うので、ここでは安全に運用するための点だけを挙げます。

- 検索用のトークンには、そのシステムに見せてよい文書のパーミッション（例: ``{group}sales``）だけを付けます
- ``{role}admin-api`` を付けたトークンは、文書の登録だけでなく、Admin API のすべてのエンドポイントを使えます。「登録だけ」のような狭い権限はありません
- 「有効期限」を設定し、期限が来たら作り直します。不要になったトークンは削除します
- トークンはサーバー側に置き、ブラウザーで動く JavaScript には埋め込みません
- 「パラメーター名」は空のままにします。設定すると、URL パラメーターでパーミッションを追加できるようになります
- トークンを発行できる ``admin-accesstoken`` ロールと、値を表示できる ``admin-accesstoken-view`` ロールは、管理者と同等に扱います

ログを残す期間を決める
======================

ログファイルの場所と監視は :doc:`guide-10` で扱います。
ここでは、セキュリティ上の確認に使う記録と、その保持期間を整理します。

監査ログ（``audit.log``）には、ログイン（``LOGIN``）、ログイン失敗（``LOGIN_FAILURE``）、ログアウト（``LOGOUT``）、管理画面と Admin API へのアクセス（``ACCESS``）、権限不足による拒否（``ACCESS_DENIED``）などが 1 行ずつ記録されます。
ファイルは ZIP 版では ``logs/`` 、DEB・RPM 版と Docker イメージでは ``/var/log/fess/`` に出力され、［システム情報］>［ログファイル］からもダウンロードできます。
既定の形式は LTSV で、Docker イメージでは ECS 形式の JSON です。
ローテートしたファイルは 360 日で削除されます（``log4j2.xml`` の ``backup.audit.max.age``）。

誰が何を検索したかは、OpenSearch に保存される検索ログで、［システム情報］>［検索ログ］から確認できます。
［全般］の「以前の検索ログを削除」の既定は ``-1`` で、検索ログを削除せずに持ち続けます。
この日数はクリックログ、お気に入りログ、チャットログにも適用されます。
社内の規程で保持期間が決まっている場合は、その日数を入れてください。

複数台で動かす場合
==================

Fess 15.9 のログインセッションは、各 Fess プロセスのメモリ上にあります。
SSO の途中で使う値（OpenID Connect の ``state`` や SAML の AuthnRequest ID）もセッションに入るため、ロードバランサーの背後に複数台を置く場合は、同じ利用者を同じ Fess に振り分けるスティッキーセッションを有効にします。
複数台構成そのものは :doc:`guide-14` を参照してください。

なお、セッションを OpenSearch に保存して複数台で共有する機能と、ローカルユーザーのパスキーログインは 15.10 以降の機能です。

次に読む記事
============

- ロールとグループの設計、クロール設定のパーミッションの書き方: :doc:`guide-05`
- アクセストークンを使った API 連携: :doc:`guide-11`
- ログの場所、監視、バックアップ: :doc:`guide-10`
- 複数台構成への拡張: :doc:`guide-14`
- ファイルサーバーの ACL を検索結果に反映する: :doc:`file-server-search`

参考資料
========

- `Microsoft Entra IDによるSSO設定 <https://fess.codelibs.org/ja/stable/config/sso-entraid.html>`__
- `OpenID ConnectによるSSO設定 <https://fess.codelibs.org/ja/stable/config/sso-oidc.html>`__
- `SAML認証によるSSO設定 <https://fess.codelibs.org/ja/stable/config/sso-saml.html>`__
- `Windows統合認証によるSSO設定 <https://fess.codelibs.org/ja/stable/config/sso-spnego.html>`__
- `全般 <https://fess.codelibs.org/ja/stable/admin/general-guide.html>`__
- `アクセストークン <https://fess.codelibs.org/ja/stable/admin/accesstoken-guide.html>`__
- `セキュリティ設定 <https://fess.codelibs.org/ja/stable/install/security.html>`__
- `ログ設定 <https://fess.codelibs.org/ja/stable/config/admin-logging.html>`__
