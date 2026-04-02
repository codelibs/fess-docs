# Unit 2: クローラー関連ドキュメント レビューレポート

## 概要

Fess 15.6のクローラー関連ドキュメント3ファイルについて、ソースコード(`repos/fess`)と照合してレビューを実施した。

**対象ファイル:**
- `ja/15.6/config/crawler-basic.rst` - クローラー基本設定
- `ja/15.6/config/crawler-advanced.rst` - クローラー詳細設定
- `ja/15.6/config/crawler-thumbnail.rst` - サムネイル画像の設定

**照合先ソース:**
- `repos/fess/src/main/resources/fess_config.properties`
- `repos/fess/src/main/webapp/WEB-INF/conf/system.properties`
- `repos/fess/src/main/java/org/codelibs/fess/mylasta/direction/FessConfig.java`
- `repos/fess/src/main/java/org/codelibs/fess/thumbnail/impl/CommandGenerator.java`
- `repos/fess/src/main/java/org/codelibs/fess/crawler/transformer/FessTransformer.java`
- `repos/fess/src/main/resources/crawler/contentlength.xml`

## 問題点

### [CRITICAL] 重大な問題

**(C1) `thumbnail.command.timeout` / `thumbnail.command.destroy.timeout` の設定ファイル誤記**

- **ファイル:** `crawler-thumbnail.rst` (行249-253)
- **問題:** ドキュメントではこれらのプロパティを `fess_config.properties` で設定するように記述しているが、実際には `system.properties` (DynamicProperties) 経由で読み込まれる。
- **根拠:** `CommandGenerator.java` (行91, 95) で `fessConfig.getSystemProperty("thumbnail.command.timeout")` を使用しており、`getSystemProperty()` は `system.properties` を参照する。`fess_config.properties` には該当キーが存在しない。
- **影響:** ユーザーが `fess_config.properties` に設定しても反映されない。
- **修正案:** `thumbnail.command.timeout` と `thumbnail.command.destroy.timeout` は管理画面の「全般の設定」または `system.properties` で設定する旨を明記する。

### [MAJOR] 主要な問題

**(M1) `crawler.document.max.site.length` の説明が不正確**

- **ファイル:** `crawler-advanced.rst` (行82)
- **問題:** 「ドキュメントサイトの最大行数」と記述されているが、実際には「サイト名の最大文字数」である。
- **根拠:** `FessConfig.java` (行3178) のコメントは "Maximum length of site name in documents." であり、`FessTransformer.java` (行245) では `StringUtils.abbreviate(value, maxSiteLength)` で文字数による切り詰めを行っている。「行数」ではなく「文字数」が正しい。
- **修正案:** 「ドキュメントサイトの最大文字数」または「サイト名フィールドの最大長」に修正。

**(M2) `crawler.document.space.chars` のUnicodeエスケープ表記の不一致**

- **ファイル:** `crawler-advanced.rst` (行173)
- **問題:** ドキュメントでは `\u0009\u000A...` (バックスラッシュ付き) と表記しているが、`fess_config.properties` の実際の値は `u0009u000A...` (バックスラッシュなし)。
- **根拠:** `fess_config.properties` 行323: `crawler.document.space.chars=u0009u000Au000Bu000C...`
- **影響:** ユーザーがドキュメントの表記をそのままコピーして設定すると、期待通りに動作しない可能性がある。
- **修正案:** 実際のプロパティファイルの値に合わせてバックスラッシュを除去する。

**(M3) `crawler.document.fullstop.chars` のUnicodeエスケープ表記の不一致**

- **ファイル:** `crawler-advanced.rst` (行175)
- **問題:** M2と同じ。ドキュメントは `\u002e\u06d4\u2e3c\u3002` だが、実際は `u002eu06d4u2e3cu3002`。
- **修正案:** M2と同様にバックスラッシュを除去する。

**(M4) JVMクローラーオプションのデフォルト値が大幅に省略されている**

- **ファイル:** `crawler-advanced.rst` (行715-719)
- **問題:** ドキュメントのデフォルト設定例は6つのオプションのみだが、実際の `fess_config.properties` には約30のJVMオプションが含まれている（jcifs SMBタイムアウト、Netty設定、Log4j設定、G1GC詳細設定、PDFBox設定など）。
- **根拠:** `fess_config.properties` 行49-88に完全なデフォルト値がある。
- **影響:** ユーザーがドキュメントの例でJVMオプションを上書きすると、省略されたオプション（特にSMBタイムアウトやNetty設定）が失われ、予期しない動作を引き起こす可能性がある。
- **修正案:** デフォルト値の全体を示すか、「上記は主要なオプションの抜粋です。完全なデフォルト値は `fess_config.properties` を参照してください。カスタマイズ時は必要なオプションのみ変更し、他は維持してください。」と注記を追加する。

**(M5) `crawler.data.serializer` プロパティが未記載**

- **ファイル:** `crawler-advanced.rst`
- **問題:** `fess_config.properties` に `crawler.data.serializer=kryo` (行303) が存在するが、ドキュメントのどこにも記載がない。
- **根拠:** `FessConfig.java` にも `CRAWLER_DATA_SERIALIZER` 定数が定義されている。
- **影響:** シリアライズ方式を変更したいユーザーがプロパティの存在を知ることができない。
- **修正案:** 「全般設定」セクションにプロパティの説明を追加する。

**(M6) `thumbnail.generator.targets` と `thumbnail.system.monitor.interval` が未記載**

- **ファイル:** `crawler-thumbnail.rst`
- **問題:** `fess_config.properties` に以下のサムネイル関連プロパティが存在するが、ドキュメントに記載がない:
  - `thumbnail.generator.targets=all` (行1208)
  - `thumbnail.system.monitor.interval=60` (行1212)
- **根拠:** `FessConfig.java` に両方の定数とアクセサメソッドが定義されている。
- **修正案:** サムネイル設定セクションにこれらのプロパティを追加する。

### [MINOR] 軽微な問題

**(m1) `contentlength.xml` の例示がデフォルトファイルの内容と異なる**

- **ファイル:** `crawler-basic.rst` (行322-339)
- **問題:** ドキュメントの設定例にはPDF用のエントリ (`application/pdf`, 5MB) が含まれているが、実際の `contentlength.xml` にはデフォルトでこのエントリは存在しない。ドキュメントでは「PDFファイルを5MBまで処理する設定を追加しています」と説明しているものの、XMLブロック全体がデフォルト設定のように見える形式で記述されている。
- **修正案:** デフォルトのXMLを先に示し、PDF追加部分はカスタマイズ例として明確に分離する。

**(m2) `crawler-basic.rst` のログファイルパスがデフォルトと異なる可能性**

- **ファイル:** `crawler-basic.rst` (行195, 519)
- **問題:** ログパスを `/var/log/fess/fess_crawler.log` と記述しているが、これはRPM/DEBパッケージインストール時のパスであり、zip/tar.gz展開の場合は `logs/` ディレクトリ配下になる。
- **修正案:** パッケージ形態による違いがある旨を注記する、または `${FESS_LOG_PATH}` を使用する。

**(m3) `crawler-basic.rst` でプロキシ設定パラメーター名の表記ゆれの可能性**

- **ファイル:** `crawler-basic.rst` (行421-424)
- **問題:** `client.proxyUsername` / `client.proxyPassword` が記載されているが、これはfess-crawlerの設定パラメーターであり、fess本体の設定ファイルではない。動作はするが、fess-crawler側のドキュメントとの整合性を確認する必要がある。
- **影響:** 軽微。クロール設定の「設定パラメーター」欄に記述する旨は正しく記述されている。

**(m4) `crawler-thumbnail.rst` のサムネイルジョブ無効化手順で `thumbnail.crawler.enabled` のデフォルト値に言及がない**

- **ファイル:** `crawler-thumbnail.rst` (行379-382)
- **問題:** `thumbnail.crawler.enabled` のデフォルト値が `true` であることが明記されていない。ユーザーが現在の設定を把握しにくい。
- **修正案:** 「デフォルト値は `true`（有効）です」を追記する。

**(m5) `crawler-advanced.rst` の設定ファイルパス表記の不統一**

- **ファイル:** `crawler-advanced.rst` (行23)
- **問題:** メイン設定ファイルのパスとして `/etc/fess/fess_config.properties` と `app/WEB-INF/classes/fess_config.properties` の両方を記載しているが、前者はパッケージインストール時、後者は展開インストール時のパスである。これ自体は正しいが、他のセクションではパス指定なしでファイル名のみ (`fess_config.properties`) で参照しており、統一性がない。
- **修正案:** 初出で両パスを説明した後は `fess_config.properties` で統一する旨を明記するか、各所で一貫した表記を使用する。

## ファイル別詳細

### crawler-basic.rst

| # | プロパティ | 存在 | デフォルト値 | 設定ファイル | 問題 |
|---|-----------|------|-------------|-------------|------|
| 1 | `crawler.document.max.alphanum.term.size` | OK | 20 (一致) | fess_config.properties (正) | なし |
| 2 | `crawler.document.max.symbol.term.size` | OK | 10 (一致) | fess_config.properties (正) | なし |
| 3 | `crawler.ignore.robots.txt` | OK | false (一致) | fess_config.properties (正) | なし |
| 4 | `crawler.crawling.data.encoding` | OK | UTF-8 (一致) | fess_config.properties (正) | なし |
| 5 | `crawler.document.file.name.encoding` | OK | 空 (一致) | fess_config.properties (正) | なし |
| 6 | `client.maxContentLength` | N/A | クロール設定パラメーター | N/A | なし |
| 7 | `client.proxyHost` etc. | N/A | クロール設定パラメーター | N/A | なし |
| 8 | `client.userAgent` | N/A | クロール設定パラメーター | N/A | なし |

**総評:** プロパティ値は概ね正確。ログパスの環境依存、contentlength.xmlの例示がやや紛らわしい点が改善点。

### crawler-advanced.rst

| # | プロパティ | 存在 | デフォルト値 | 問題 |
|---|-----------|------|-------------|------|
| 1 | `crawler.default.script` | OK | groovy (一致) | なし |
| 2 | `crawler.http.thread_pool.size` | OK | 0 (一致) | なし |
| 3 | `crawler.document.max.site.length` | OK | 100 (一致) | 説明が「最大行数」ではなく「最大文字数」 (M1) |
| 4 | `crawler.document.site.encoding` | OK | UTF-8 (一致) | なし |
| 5 | `crawler.document.unknown.hostname` | OK | unknown (一致) | なし |
| 6 | `crawler.document.use.site.encoding.on.english` | OK | false (一致) | なし |
| 7 | `crawler.document.append.data` | OK | true (一致) | なし |
| 8 | `crawler.document.append.filename` | OK | false (一致) | なし |
| 9 | `crawler.document.max.alphanum.term.size` | OK | 20 (一致) | なし |
| 10 | `crawler.document.max.symbol.term.size` | OK | 10 (一致) | なし |
| 11 | `crawler.document.duplicate.term.removed` | OK | false (一致) | なし |
| 12 | `crawler.document.space.chars` | OK | 値不一致 | Unicodeエスケープ表記が異なる (M2) |
| 13 | `crawler.document.fullstop.chars` | OK | 値不一致 | Unicodeエスケープ表記が異なる (M3) |
| 14 | `crawler.web.protocols` | OK | http,https (一致) | なし |
| 15 | `crawler.file.protocols` | OK | 一致 | なし |
| 16 | `crawler.data.env.param.key.pattern` | OK | 一致 | なし |
| 17 | `crawler.ignore.robots.txt` | OK | false (一致) | なし |
| 18 | `crawler.ignore.robots.tags` | OK | false (一致) | なし |
| 19 | `crawler.ignore.content.exception` | OK | true (一致) | なし |
| 20 | `crawler.failure.url.status.codes` | OK | 404 (一致) | なし |
| 21 | `crawler.system.monitor.interval` | OK | 60 (一致) | なし |
| 22 | `crawler.hotthread.*` (6項目) | OK | すべて一致 | なし |
| 23 | `crawler.metadata.content.excludes` | OK | 一致 | なし |
| 24 | `crawler.metadata.name.mapping` | OK | 一致 | なし |
| 25 | `crawler.document.html.*` (XPath等) | OK | すべて一致 | なし |
| 26 | `crawler.document.html.pruned.tags` | OK | 一致 | なし |
| 27 | `crawler.document.html.max.digest.length` | OK | 120 (一致) | なし |
| 28 | `crawler.document.html.default.lang` | OK | 空 (一致) | なし |
| 29 | `crawler.document.html.default.*.patterns` (4項目) | OK | 一致 | なし |
| 30 | `crawler.document.file.*` (全項目) | OK | すべて一致 | なし |
| 31 | `crawler.document.cache.*` (4項目) | OK | すべて一致 | なし |
| 32 | `crawler.document.mimetype.extension.overrides` | OK | 空 (一致) | なし |
| 33 | `jvm.crawler.options` | OK | 一部のみ記載 | 大幅に省略 (M4) |
| - | `crawler.data.serializer` | 未記載 | kryo | 欠落 (M5) |

**総評:** プロパティの存在とデフォルト値は大部分正確。主要な問題は説明文の不正確さ(M1)とUnicode表記の不一致(M2, M3)。

### crawler-thumbnail.rst

| # | プロパティ | 存在 | デフォルト値 | 問題 |
|---|-----------|------|-------------|------|
| 1 | `thumbnail.html.image.min.width` | OK | 100 (一致) | なし |
| 2 | `thumbnail.html.image.min.height` | OK | 100 (一致) | なし |
| 3 | `thumbnail.html.image.max.aspect.ratio` | OK | 3.0 (一致) | なし |
| 4 | `thumbnail.html.image.thumbnail.width` | OK | 100 (一致) | なし |
| 5 | `thumbnail.html.image.thumbnail.height` | OK | 100 (一致) | なし |
| 6 | `thumbnail.html.image.format` | OK | png (一致) | なし |
| 7 | `thumbnail.html.image.xpath` | OK | //IMG (一致) | なし |
| 8 | `thumbnail.html.image.exclude.extensions` | OK | 一致 | なし |
| 9 | `thumbnail.generator.interval` | OK | 0 (一致) | なし |
| 10 | `thumbnail.command.timeout` | system.properties | 30000 (一致) | 設定ファイル誤記 (C1) |
| 11 | `thumbnail.command.destroy.timeout` | system.properties | 5000 (一致) | 設定ファイル誤記 (C1) |
| 12 | `thumbnail.crawler.enabled` | OK | true | デフォルト値の明記なし (m4) |
| - | `thumbnail.generator.targets` | 未記載 | all | 欠落 (M6) |
| - | `thumbnail.system.monitor.interval` | 未記載 | 60 | 欠落 (M6) |

**総評:** サムネイル設定の大部分は正確。最も重大な問題は `thumbnail.command.timeout` / `thumbnail.command.destroy.timeout` の設定ファイル指定が誤っている点(C1)。

## 推奨事項

1. **最優先 (C1):** `thumbnail.command.timeout` と `thumbnail.command.destroy.timeout` は `system.properties` 経由であることを修正する。`fess_config.properties` のセクションから分離し、管理画面またはsystem.propertiesで設定する旨を記載する。

2. **高優先 (M1):** `crawler.document.max.site.length` の説明を「最大行数」から「最大文字数」に訂正する。

3. **高優先 (M2, M3):** `crawler.document.space.chars` と `crawler.document.fullstop.chars` のUnicodeエスケープ表記を実際のプロパティファイルと一致させる(`\u` -> `u`)。

4. **中優先 (M4):** JVMオプションのデフォルト値について、省略されている旨を明記し、カスタマイズ時の注意点を追加する。

5. **中優先 (M5, M6):** 未記載プロパティ (`crawler.data.serializer`, `thumbnail.generator.targets`, `thumbnail.system.monitor.interval`) を追加する。

6. **低優先 (m1-m5):** 軽微な問題は次回のドキュメント更新時にあわせて修正する。
