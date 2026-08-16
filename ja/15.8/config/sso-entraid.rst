===============================
Microsoft Entra IDによるSSO設定
===============================

概要
====

|Fess| では、Microsoft Entra ID（旧Azure AD）を使用したシングルサインオン（SSO）認証をサポートしています。
Entra ID認証を使用することで、Microsoft 365環境のユーザー情報やグループ情報を |Fess| のロールベース検索と連携できます。

Entra ID認証の仕組み
--------------------

Entra ID認証では、|Fess| がOAuth 2.0/OpenID Connectのクライアントとして動作し、Microsoft Entra IDと連携して認証を行います。

1. ユーザーが |Fess| のSSOエンドポイント（``/sso/``）にアクセス
2. |Fess| がEntra IDの認可エンドポイントにリダイレクト
3. ユーザーがEntra IDで認証（Microsoftサインイン）
4. Entra IDが認可コードを |Fess| にリダイレクト
5. |Fess| が認可コードを使用してアクセストークンを取得
6. ユーザーがログイン
7. バックグラウンドで |Fess| がMicrosoft Graph APIを使用してユーザーのグループ・ロール情報を取得し、完了後にロールベース検索に適用

.. note::
   |Fess| 15.8 以降は認可エンドポイントに ``response_mode=query`` を要求するため、手順4の認可レスポンスはGETで返されます。
   15.7 以前はクロスサイトのPOSTで返されており、|Fess| の既定値である ``tomcat.sameSiteCookies = lax``
   ではセッションクッキーが送信されないため、``tomcat.sameSiteCookies = none`` への変更が回避策として必要でした。
   この回避策のためだけに ``none`` を設定していた場合は、既定値に戻せます。

ロールベース検索との連携については、:doc:`security-role` を参照してください。

前提条件
========

Entra ID認証を設定する前に、以下の前提条件を確認してください。

- |Fess| 15.8 以降がインストールされていること
- Microsoft Entra ID（Azure AD）テナントが利用可能であること
- |Fess| がHTTPSでアクセス可能であること（本番環境では必須）
- Entra ID側でアプリケーションを登録できる権限があること

基本設定
========

SSO機能の有効化
---------------

Entra ID認証を有効にするには、``app/WEB-INF/conf/system.properties`` に以下の設定を追加します。

::

    sso.type=entraid

必須設定
--------

Entra IDから取得した情報を設定します。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``entraid.tenant``
     - テナントID（例: ``xxx.onmicrosoft.com``）
     - （必須）
   * - ``entraid.client.id``
     - アプリケーション（クライアント）ID
     - （必須）
   * - ``entraid.client.secret``
     - クライアントシークレットの値
     - （必須）
   * - ``entraid.reply.url``
     - リダイレクトURI（コールバックURL）
     - リクエストURLを使用

.. note::
   ``entraid.*`` プレフィックスの代わりに、レガシーの ``aad.*`` プレフィックスも使用できます（後方互換性）。

オプション設定
--------------

必要に応じて以下の設定を追加できます。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``entraid.authority``
     - 認証サーバーURL
     - ``https://login.microsoftonline.com/``
   * - ``entraid.state.ttl``
     - State有効期限（秒）
     - ``3600``
   * - ``entraid.response.mode``
     - 認可レスポンスの受け取り方法。\ ``query`` または ``form_post`` を指定します。
     - ``query``
   * - ``entraid.default.groups``
     - デフォルトグループ（カンマ区切り）。すべてのEntra IDユーザーに適用されます。
     - （なし）
   * - ``entraid.default.roles``
     - デフォルトロール（カンマ区切り）。すべてのEntra IDユーザーに適用されます。
     - （なし）
   * - ``entraid.permission.fields``
     - 権限値として追加で使用するグループ/ロールのフィールド（カンマ区切り）。グループ/ロールのID（GUID）は常に権限として使用され、ここで指定したフィールド（例: ``mail``）の値が追加されます。指定できるのは、値が文字列であるフィールドだけです。``securityEnabled`` は真偽値、``groupTypes`` は配列としてMicrosoft Graphから返るため権限値にはできず、これらを指定した場合は無視され、該当のフィールド名を示す警告がログに出力されます。
     - ``mail``
   * - ``entraid.use.ds``
     - ドメインサービス連携。\ ``true`` の場合、``name@domain`` 形式の権限値から、ドメイン部を除いたローカル部（``name``）も権限として追加します。これはグループ・ロールだけでなく、サインインしたユーザー自身にも適用され、UPNのローカル部がユーザーレベルの権限として追加されます。そのため ``false`` にすると、グループの権限だけでなくこのユーザーレベルの権限も追加されなくなります。
     - ``true``

.. note::

   グループ/ロールのID（GUID）は常に権限になりますが、\ ``mail`` を持つのはメールが有効なグループだけです。
   Microsoft 365グループはメールが有効なため、グループ名も権限として登録されます。
   一方、\ **セキュリティグループはメールが有効ではないため、既定値のままではGUIDしか権限になりません**\ 。
   ファイルシステムのアクセス権をセキュリティグループ名で指定している場合、権限が一致せず検索結果に出ません。

   この場合は、すべてのグループが持つ ``displayName`` を追加してください。

   .. code-block:: properties

      entraid.permission.fields=mail,displayName

   ``displayName`` はドメインで修飾されず一意でもないため、既定値には含めていません。
   たとえばEntra ID側に ``Administrators`` という名前のグループがあると、
   Windowsの組み込みグループ ``Administrators`` を指定した文書にも一致します。
   追加する際は、既存のアクセス権で使われている名前と衝突しないことを確認してください。

.. note::
   既定の ``query`` では、認可コードがコールバックURLのクエリ文字列に含まれます。
   ``form_post`` を指定すると認可コードはURLに現れないため、ブラウザの履歴や、
   フロントエンドのプロキシ・WAFのアクセスログにも残りません。
   ただし ``form_post`` はクロスサイトのPOSTになるため、``tomcat.sameSiteCookies = none`` が必要です。
   設定していない場合はセッションクッキーが送信されず、ログインに失敗します。
   さらに ``none`` はブラウザが ``Secure`` 属性付きCookieに対してのみ受け入れるため、
   ``form_post`` を使うには |Fess| をHTTPSで提供する必要があります。
   HTTPのままでは、``none`` を設定してもブラウザがセッションCookie自体を保存しないため、やはりログインできません。
   通常は既定値のまま使用してください。
   ``query`` と ``form_post`` 以外を指定した場合は、警告を出力して ``query`` として扱います。

.. warning::

   ``entraid.default.groups`` と ``entraid.default.roles`` は、ユーザーごとに切り替えられない
   単一のグローバル設定です。\ |Fess| はログイン時にすべてのEntra IDユーザーへこれらを適用し、
   その後の解決のたびに再適用するため、Microsoft Graphの結果によって取り消されることはありません。
   特に、\ |Fess| の管理者ロール（同梱の ``authentication.admin.roles`` では ``admin``\ ）を
   ``entraid.default.roles`` に設定してはいけません。テナント内のすべてのユーザーに、
   管理画面への永続的なアクセス権を与えてしまいます。

Entra ID側での設定
==================

Azure Portalでのアプリ登録
--------------------------

1. `Azure Portal <https://portal.azure.com/>`_ にサインイン

2. **Microsoft Entra ID** を選択

3. 左メニューの **管理** → **アプリの登録** → **新規登録** をクリック

4. アプリケーションを登録:

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - 設定項目
        - 設定値
      * - 名前
        - 任意の名前（例: Fess SSO）
      * - サポートされているアカウントの種類
        - 「この組織ディレクトリのみに含まれるアカウント」
      * - プラットフォームの選択
        - Web
      * - リダイレクトURI
        - ``https://<Fessのホスト>/sso/``

5. **登録** をクリック

クライアントシークレットの作成
------------------------------

1. アプリの詳細ページで **証明書とシークレット** をクリック

2. **新しいクライアントシークレット** をクリック

3. 説明と有効期限を設定して **追加** をクリック

4. 生成された **値** をコピーして保存（この値は再表示されません）

.. warning::
   クライアントシークレットの値は、作成直後のみ表示されます。
   別の画面に遷移する前に必ず記録してください。

APIアクセス許可の設定
---------------------

1. 左メニューの **APIのアクセス許可** をクリック

2. **アクセス許可の追加** をクリック

3. **Microsoft Graph** を選択

4. **委任されたアクセス許可** を選択

5. 以下のアクセス許可を追加:

   - ``User.Read`` - サインインしたユーザーの所属グループ（``/me/memberOf``）の取得に必要。アプリ登録の作成時に既定で付与されます
   - ``GroupMember.Read.All`` - グループ名などのグループ属性の取得、およびネストされたグループの解決に必要

6. **アクセス許可の追加** をクリック

7. **「<テナント名>に管理者の同意を与えます」** をクリック

.. note::
   管理者の同意は、テナント管理者権限が必要です。

.. note::
   ``GroupMember.Read.All`` の代わりに ``Group.Read.All`` や ``Directory.Read.All`` を付与しても、
   グループ属性の取得とネストされたグループの解決は動作します。
   一方、\ ``/me/memberOf`` は ``Group.Read.All`` では認可されないため、
   いずれの場合も ``User.Read`` は必要です。

.. note::
   上記のアクセス許可では、ディレクトリロールの ``displayName`` はMicrosoft Graphから返されません。
   そのため、\ ``entraid.permission.fields`` に ``displayName`` を指定しても、
   ディレクトリロールから権限になるのはロールのID（GUID）だけです。
   ロール名を権限値として使用する場合は、\ ``RoleManagement.Read.Directory``
   （または ``Directory.Read.All``\ ）も付与してください。

.. note::
   |Fess| はトークン取得時に ``https://graph.microsoft.com/.default`` スコープを要求します。
   15.8 以降は、認可エンドポイントにも ``openid profile offline_access https://graph.microsoft.com/.default``
   を要求し、同じ範囲の同意を求めます。
   これは、アプリ登録で構成・同意済みのすべてのアクセス許可が使用されることを意味します。
   そのため、グループ情報を取得するには、上記のアクセス許可をアプリ登録に追加し、
   管理者の同意を与えておく必要があります。

取得する情報
------------

以下の情報をFessの設定に使用します。

- **アプリケーション（クライアント）ID**: 概要ページの「アプリケーション (クライアント) ID」
- **テナントID**: 概要ページの「ディレクトリ (テナント) ID」または ``xxx.onmicrosoft.com`` 形式
- **クライアントシークレットの値**: 証明書とシークレットで作成した値

グループ・ロールマッピング
==========================

Entra ID認証では、Microsoft Graph APIを使用してユーザーが所属するグループおよびロールを自動的に取得します。
取得したグループIDおよびグループ名は、|Fess| のロールベース検索に使用できます。

ネストされたグループ
--------------------

|Fess| は、ユーザーが直接所属するグループだけでなく、そのグループが所属する親グループ（ネストされたグループ）も取得します。
直接所属するグループの取得と親グループの探索は、いずれもログイン後の同一のバックグラウンド処理として実行されるため、ログイン自体がMicrosoft Graphによって遅延することはありません。
親グループの取得にはMicrosoft Graphの ``getMemberGroups`` を使用します。これは推移的に解決されるため、直接所属するグループ1件につき1回の呼び出しで、その上位にあるすべての親グループが階層の深さに関わらず返ります。取得結果は一定時間キャッシュされます。
このバックグラウンド処理が完了すると、ユーザーの権限が再計算されます。

デフォルトグループの設定
------------------------

すべてのEntra IDユーザーに共通のグループを付与する場合:

::

    entraid.default.groups=authenticated_users,entra_users

設定例
======

最小構成（検証環境向け）
------------------------

以下は、検証環境で動作確認を行うための最小限の設定例です。

::

    # SSO有効化
    sso.type=entraid

    # Entra ID設定
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=http://localhost:8080/sso/

推奨構成（本番環境向け）
------------------------

以下は、本番環境で使用する際の推奨設定例です。

::

    # SSO有効化
    sso.type=entraid

    # Entra ID設定
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=https://fess.example.com/sso/

    # デフォルトグループ（オプション）
    entraid.default.groups=authenticated_users

レガシー設定（後方互換性）
--------------------------

以前のバージョンとの互換性のため、``aad.*`` プレフィックスも使用できます。
各 ``entraid.*`` プロパティが未設定の場合に、対応する ``aad.*`` プロパティの値が使用されます。
また、``sso.type=aad`` も ``sso.type=entraid`` と同等に扱われます。

::

    # SSO有効化（sso.type=aad も使用可能）
    sso.type=entraid

    # レガシー設定キー
    aad.tenant=yourcompany.onmicrosoft.com
    aad.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    aad.client.secret=your-client-secret-value
    aad.reply.url=https://fess.example.com/sso/

トラブルシューティング
======================

よくある問題と解決方法
----------------------

認証後にFessに戻れない
~~~~~~~~~~~~~~~~~~~~~~

- Azure Portalのアプリ登録でリダイレクトURIが正しく設定されているか確認してください
- ``entraid.reply.url`` の値がAzure Portalの設定と完全に一致しているか確認してください
- プロトコル（HTTP/HTTPS）が一致しているか確認してください
- リダイレクトURIの末尾に ``/`` が含まれているか確認してください
- ``entraid.response.mode`` に ``form_post`` を指定している場合は、``tomcat.sameSiteCookies = none``
  が設定されているか、かつ |Fess| をHTTPSで提供しているかを確認してください。既定値の ``lax`` のままでは、
  コールバックのクロスサイトPOSTにブラウザがセッションCookieを送信しません。``none`` を設定しても
  HTTPのままでは、``none`` が ``Secure`` 属性を要求するためブラウザがそのCookie自体を保存しません。
  いずれの場合もその場で1回だけログインに失敗し、ブラウザはログイン画面に戻って
  「SSOログイン処理に失敗しました。」を表示します。ログには
  ``Failed to process SSO login: could not validate state`` という警告が出力されます

認証エラーが発生する
~~~~~~~~~~~~~~~~~~~~

- テナントID、クライアントID、クライアントシークレットが正しく設定されているか確認してください
- クライアントシークレットの有効期限が切れていないか確認してください
- APIアクセス許可に管理者の同意が与えられているか確認してください

グループ情報が取得できない
~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``User.Read`` と ``GroupMember.Read.All`` のアクセス許可が付与されているか確認してください
  （``GroupMember.Read.All`` は ``Group.Read.All`` や ``Directory.Read.All`` でも代用できますが、\ ``/me/memberOf`` には ``User.Read`` が必要です）
- 管理者の同意が与えられているか確認してください
- ユーザーがEntra ID上でグループに所属しているか確認してください
- ネストされた親グループを解決できない場合は、\ ``Not allowed to read the parent groups of ...`` という警告がログに出力されます。この場合は ``GroupMember.Read.All`` を付与してください
- |Fess| はグループ・ロールの権限解決をログイン完了後にバックグラウンドで実行するため、ログイン自体がMicrosoft Graphの応答を待つことはありません。解決が完了するまでの間、ユーザーが保持するのは、ユーザー自身のユーザーレベルの権限と、\ ``entraid.default.groups``\ ・\ ``entraid.default.roles``\ に設定したグループ・ロールだけです。どちらも未設定（同梱の既定値）の場合、この間の検索は1件もヒットしません。\ ``role.search.default.permissions`` は既定で空であり、同梱の ``role.search.default.display.permissions`` のまま作成したクロール設定でクロールした文書には ``{role}guest`` が付与されますが、ログイン済みユーザーはこのロールを持たないためです。この時間は、最大で約1秒のスケジューリング遅延に加えて、Microsoft Graphの呼び出しそのもの（直接所属の取得で1回、さらにネストしたグループをたどるために直接所属グループごとに1回ずつを順番に実行。キャッシュが未作成の場合）だけかかるため、ユーザーが所属するグループ数に応じて長くなります。この間、検索画面には、グループ・ロール権限を読み込み中である旨と、しばらくしてから再検索するよう促すメッセージが表示されます
- 解決が完全には成功しなかった場合は、検索画面に、グループ・ロール権限をすべて取得できなかった旨と、いったんログアウトしてからログインし直すよう、また繰り返し発生する場合は管理者に問い合わせるよう促すメッセージが表示されます。「すべて」は意図的な表現です。直接所属の取得とネストしたグループの探索の両方が成功しない限り解決は失敗として扱われるため、直接所属のグループは取得できていても親グループを取得できなかったユーザーにも、このメッセージが表示されます。ただし1つだけ例外があり、それは前項で説明した状況です。``GroupMember.Read.All`` が付与されておらず、Microsoft Graphがネストされたグループの取得を ``Authorization_RequestDenied`` で拒否した場合、\ |Fess| はこれを失敗ではなく「そのグループに親グループは無い」という回答として扱います。この場合、親グループの権限が欠けているにもかかわらず解決は成功として扱われ、\ **このメッセージは表示されません**\ 。手がかりはログに出力される ``Not allowed to read the parent groups of ...`` の警告だけですので、ネストされたグループを使用している場合は、この警告が出ていないかを確認してください。部分的にしか解決できない主な原因はスロットリングです。Microsoft Graphが1回でもHTTP 429または503を返すと、\ |Fess| は ``Retry-After`` ヘッダーが要求する時間（解釈できる値がない場合は60秒、最大60分）待機し、その間は直接所属の取得が成功していても、\ |Fess| 全体でネストしたグループの取得がスキップされます。ただし、失敗が最終的なものになるとは限りません。アクセストークンが更新されるたびに解決が再実行され、その後成功すればメッセージは消え、欠けていた権限も回復します。すぐに再試行したい場合は、いったんログアウトしてからログインし直してください（ログインしたままSSOのログインURLを開いても、検索画面にリダイレクトされるだけです）

デバッグ設定
------------

問題を調査する際は、|Fess| のログレベルを調整することで、Entra ID関連の詳細なログを出力できます。

``app/WEB-INF/classes/log4j2.xml`` で、以下のロガーを追加してログレベルを変更できます。

::

    <Logger name="org.codelibs.fess.sso.entraid" level="DEBUG"/>

参考情報
========

- :doc:`security-role` - ロールベース検索の設定について
- :doc:`sso-saml` - SAML認証によるSSO設定について
- :doc:`sso-oidc` - OpenID Connect認証によるSSO設定について
