# Unit 5: セキュリティ関連ドキュメント レビューレポート

## 概要

以下の3ファイルについて、ソースコード（fess 15.6）と照合してレビューを実施した。

- `ja/15.6/config/security-role.rst` - ロールベース検索の設定
- `ja/15.6/config/security-virtual-host.rst` - 仮想ホスト
- `ja/15.6/config/ldap-integration.rst` - LDAP統合ガイド

検証対象ソースコード:
- `fess_config.properties` - 静的デフォルト設定
- `system.properties` - 動的ランタイム設定
- `FessConfig.java` - 設定定数・アクセサ
- `FessProp.java` - プロパティアクセスロジック
- `Constants.java` - 定数定義
- `LdapManager.java` - LDAP接続ロジック

## 問題点

### [CRITICAL] 重大な問題

#### C1: `ldap.security.principal` の説明が誤っている (ldap-integration.rst 60行目)

ドキュメントでは `ldap.security.principal` を「バインドDN（サービスアカウント）」として記述しているが、ソースコード上では `ldap.security.principal` はユーザー認証時のバインドDNテンプレート（`uid=%s,ou=People,...` のような書式文字列）である。

- `FessProp.java` 694行目: `String.format(getSystemProperty(Constants.LDAP_SECURITY_PRINCIPAL, ...), value)` -- ユーザー名を埋め込むフォーマット文字列として使用
- `LdapManager.java` 164行目: `fessConfig.getLdapSecurityPrincipal(username)` -- ユーザー認証時に使用

管理用のサービスアカウントバインドDNは `ldap.admin.security.principal` である（`Constants.java` 668行目、`FessProp.java` 706行目）。

**影響**: この設定を誤ると、LDAP認証が正しく動作しない。ドキュメントに従って設定したユーザーは認証に失敗する可能性が高い。

#### C2: LDAP基本設定の必須プロパティが不足 (ldap-integration.rst)

ドキュメントの「基本設定」セクションに以下の重要なプロパティが記載されていない:

- `ldap.initial.context.factory` - system.propertiesでデフォルト `com.sun.jndi.ldap.LdapCtxFactory` が設定されている
- `ldap.security.authentication` - system.propertiesでデフォルト `simple` が設定されている
- `ldap.admin.user.filter` - ユーザー検索フィルター（fess_config.propertiesでデフォルト `uid=%s`）
- `ldap.admin.user.base.dn` - ユーザー検索ベースDN
- `ldap.admin.role.base.dn` - ロール検索ベースDN
- `ldap.admin.group.base.dn` - グループ検索ベースDN

これらはLDAP管理機能（ユーザー/ロール/グループの同期）に必須のプロパティであり、`fess_config.properties` にデフォルト値が定義されている。

### [MAJOR] 主要な問題

#### M1: `ldap.account.filter` と `ldap.admin.user.filter` の混同 (ldap-integration.rst 71行目)

ドキュメントでは `ldap.account.filter=uid=%s` を「アカウントフィルター（ユーザー認証時の検索フィルター）」として記載しているが、実際にはもう一つ `ldap.admin.user.filter`（fess_config.propertiesでデフォルト `uid=%s`）がある。これらは異なる用途である:

- `ldap.account.filter` - ユーザー認証時の検索フィルター（system.properties経由）
- `ldap.admin.user.filter` - LDAP管理画面でのユーザー検索フィルター（fess_config.properties）

ドキュメントではこの区別が説明されていない。

#### M2: `ldap.group.filter` のプレースホルダー記法が不正確 (ldap-integration.rst 79行目)

ドキュメントでは `ldap.group.filter=(member={0})` と記載しているが、ソースコードでは `Constants.LDAP_GROUP_FILTER` は `getSystemProperty` 経由で取得され、そのまま文字列として使用される。`{0}` というプレースホルダーの解決方法はLdapManager内の実装に依存するため、実際の記法を確認する必要がある。

#### M3: デバッグ設定のファイルパスが不正確 (ldap-integration.rst 225行目)

ドキュメントでは `app/WEB-INF/classes/log4j2.xml` と記載しているが、実際のlog4j2.xmlは `src/main/resources/log4j2.xml`（開発時）である。デプロイ済み環境では `WEB-INF/classes/log4j2.xml` に配置されるが、docの `app/` プレフィックスは不正確。正しくは `app/WEB-INF/classes/log4j2.xml` ではなく、実際のデプロイパスに応じた記述が必要。

#### M4: 多数のLDAP設定プロパティが未記載 (ldap-integration.rst)

`fess_config.properties` には以下の重要な運用プロパティが定義されているが、ドキュメントに記載がない:

- `ldap.admin.sync.password` (デフォルト: true) - パスワード同期
- `ldap.auth.validation` (デフォルト: true) - 認証バリデーション
- `ldap.max.username.length` (デフォルト: -1) - ユーザー名最大長
- `ldap.ignore.netbios.name` (デフォルト: true) - NetBIOS名の無視
- `ldap.group.name.with.underscores` (デフォルト: false) - グループ名のアンダースコア
- `ldap.lowercase.permission.name` (デフォルト: false) - パーミッション名の小文字化
- `ldap.allow.empty.permission` (デフォルト: true) - 空パーミッションの許可
- `ldap.samaccountname.group` (デフォルト: false) - sAMAccountNameによるグループ
- `ldap.role.search.user.enabled` (デフォルト: true) - ユーザーロール検索
- `ldap.role.search.group.enabled` (デフォルト: true) - グループロール検索
- `ldap.role.search.role.enabled` (デフォルト: true) - ロールロール検索
- `ldap.admin.role.object.classes` - ロールオブジェクトクラス
- `ldap.admin.group.object.classes` - グループオブジェクトクラス
- `ldap.admin.user.object.classes` - ユーザーオブジェクトクラス
- `ldap.attr.*` 系の属性マッピング（約30個）

特にActive Directory環境では `ldap.samaccountname.group` や `ldap.ignore.netbios.name` が重要。

#### M5: security-role.rst が設定プロパティに全く触れていない

`security-role.rst` はロールベース検索の概念と管理画面での操作を説明しているが、関連する設定プロパティの記載が一切ない。以下のプロパティは `fess_config.properties` に存在する:

- `role.search.default.permissions` - デフォルトパーミッション
- `role.search.default.display.permissions` - デフォルト表示パーミッション（デフォルト: `{role}guest`）
- `role.search.guest.permissions` - ゲストパーミッション（デフォルト: `{role}guest`）
- `role.search.user.prefix` - ユーザープレフィックス（デフォルト: `1`）
- `role.search.group.prefix` - グループプレフィックス（デフォルト: `2`）
- `role.search.role.prefix` - ロールプレフィックス（デフォルト: `R`）
- `role.search.denied.prefix` - 拒否プレフィックス（デフォルト: `D`）

### [MINOR] 軽微な問題

#### m1: security-virtual-host.rst の設定プロパティ未記載

`virtual.host.headers` プロパティ（`fess_config.properties` 275行目、デフォルト: 空文字列）が存在するが、ドキュメントには管理画面での設定方法のみ記載されている。プロパティベースの設定方法が記載されていない。

#### m2: LDAP設定ファイルパスの表記揺れ (ldap-integration.rst 40行目)

ドキュメントでは設定ファイルパスを `app/WEB-INF/conf/system.properties` と記載しているが、Fessのデプロイ構成によってパスが異なる。ソースコード上は `src/main/webapp/WEB-INF/conf/system.properties` であり、実行時は `webapps/ROOT/WEB-INF/conf/system.properties` となる。`app/` プレフィックスはFessのインストールディレクトリからの相対パスとして正しいかどうか確認が必要。

#### m3: security-role.rst に設定ファイルへの言及がない

ロールベース検索の設定方法として管理画面の操作のみが記載されているが、リクエストパラメーター、リクエストヘッダー、クッキーからロール情報を取得する場合の具体的な設定方法が記載されていない。

#### m4: ldap-integration.rst の参考情報リンク

`sso-spnego.rst` と `user-guide.rst` へのリンクは存在するファイルを指しており、問題なし。

## ファイル別詳細

### security-role.rst

- **文書の品質**: 概要説明として適切だが、設定プロパティの記載がなく、設定ガイドとしては不十分
- **ソースコードとの整合性**: 概念的な記述に誤りはないが、`role.search.*` プロパティ群の記載がない
- **推奨**: `fess_config.properties` 内の `role.search.*` プロパティの説明セクションを追加

### security-virtual-host.rst

- **文書の品質**: 管理画面での設定手順は明確
- **ソースコードとの整合性**: `virtual.host.headers` プロパティの存在は触れられていないが、管理画面経由の設定方法は正しい
- **推奨**: `virtual.host.headers` プロパティの説明を追加

### ldap-integration.rst

- **文書の品質**: 構成は良好だが、プロパティの説明に重大な誤りがある
- **ソースコードとの整合性**: 複数の問題あり（C1, C2, M1-M4）
- **推奨**: `ldap.security.principal` と `ldap.admin.security.principal` の区別を明確化し、管理用プロパティ群を追加記載

## 推奨事項

1. **最優先**: ldap-integration.rst の `ldap.security.principal` の説明を修正し、`ldap.admin.security.principal` との違いを明確にする（C1）
2. **高優先**: LDAP管理用プロパティ（`ldap.admin.*`）のセクションを追加する（C2, M4）
3. **高優先**: security-role.rst に `role.search.*` プロパティの設定リファレンスを追加する（M5）
4. **中優先**: `ldap.account.filter` と `ldap.admin.user.filter` の違いを説明する（M1）
5. **中優先**: Active Directory固有の設定プロパティ（`ldap.samaccountname.group`, `ldap.ignore.netbios.name` 等）の説明を追加する（M4）
6. **低優先**: security-virtual-host.rst に `virtual.host.headers` プロパティの説明を追加する（m1）
