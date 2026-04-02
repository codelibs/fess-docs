# Unit 7: セットアップ・導入ドキュメント レビューレポート

## 概要

対象ファイル:
- `ja/15.6/config/setup-memory.rst` - メモリ設定
- `ja/15.6/config/setup-port-network.rst` - ポートとネットワーク設定
- `ja/15.6/config/setup-windows-service.rst` - Windowsサービスへの登録
- `ja/15.6/config/intro.rst` - はじめに
- `ja/15.6/config/index.rst` - 設定ガイド目次

検証対象ソースコード:
- `repos/fess/src/main/assemblies/files/fess.in.sh`
- `repos/fess/src/main/assemblies/files/fess.in.bat`
- `repos/fess/src/main/assemblies/files/service.bat`
- `repos/fess/src/main/assemblies/files/tomcat_config.properties`
- `repos/fess/src/main/resources/fess_config.properties`

## 問題点

### [CRITICAL] 重大な問題

なし

### [MAJOR] 主要な問題

#### M1: Fessウェブアプリケーションのデフォルトメモリサイズの記載漏れ (setup-memory.rst)

ドキュメントでは`FESS_HEAP_SIZE`環境変数のみ紹介しているが、実際のデフォルト値がLinuxとWindowsで異なることが記載されていない。

- **Linux** (`fess.in.sh`): `FESS_MIN_MEM=256m`, `FESS_MAX_MEM=2g`
- **Windows** (`fess.in.bat`): `FESS_MIN_MEM=256m`, `FESS_MAX_MEM=1g`
- **Windowsサービス** (`service.bat`): `FESS_MIN_MEM=256m`, `FESS_MAX_MEM=1g`

`FESS_HEAP_SIZE`を設定すると`-Xms`と`-Xmx`の両方が同じ値に設定されるが、未設定時のデフォルトでは`-Xms`と`-Xmx`が異なる値であることが説明されていない。また、`FESS_MIN_MEM`/`FESS_MAX_MEM`環境変数で個別に設定できることも未記載。

#### M2: Windows環境でのポート変更・コンテキストパスの環境変数非対応 (setup-port-network.rst)

ドキュメントの「環境変数による設定」セクション(58-60行目)で`FESS_PORT`環境変数によるポート設定を説明しているが、この仕組みは**Linux** (`fess.in.sh`)にのみ実装されている。

- `fess.in.sh`: `FESS_PORT`環境変数を参照し`-Dfess.port`に変換する処理あり
- `fess.in.bat`: `-Dfess.port=8080`がハードコードされており、`FESS_PORT`環境変数は参照されない
- `service.bat`: `FESS_PARAMS`内に`-Dfess.port=8080`がハードコードされている

同様に、`FESS_CONTEXT_PATH`環境変数もLinuxのみ対応。ドキュメントではWindows環境での制限が明記されていない。

#### M3: コンテキストパスの設定方法が不正確 (setup-port-network.rst, 92行目)

ドキュメントでは以下のように記載:
```
FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.context.path=/search"
```

実際のソースコード(`fess.in.sh`)では、環境変数`FESS_CONTEXT_PATH`を設定するのが正しい方法:
```
export FESS_CONTEXT_PATH=/search
```

`FESS_JAVA_OPTS`に直接追加すると、デフォルト値(`/`)の後に重複して設定されてしまう可能性がある。

#### M4: OpenSearchのメモリ設定で非推奨の環境変数を記載 (setup-memory.rst, 176行目)

ドキュメントでは`OPENSEARCH_HEAP_SIZE`環境変数を紹介しているが、OpenSearch 2.x以降ではこの環境変数は非推奨。OpenSearchの公式ドキュメントでは`OPENSEARCH_JAVA_OPTS`または`config/jvm.options`での設定を推奨している。

### [MINOR] 軽微な問題

#### m1: クローラーのJVMオプション説明で`-XX:MaxGCPauseMillis=60000`の意味が不正確 (setup-memory.rst, 145行目)

ドキュメントでは「GC停止時間の目標値(60秒)」と記載しているが、60000msは「GC一時停止の最大目標時間」であり、実質的に制限を緩くする設定。通常のアプリケーションでは200ms程度が一般的であり、60秒は非常に大きい値であることの補足がない。

#### m2: fess_config.propertiesの設定ファイルパスの説明が不完全 (setup-memory.rst, 101行目)

クローラーメモリ設定で「`app/WEB-INF/classes/fess_config.properties` または `/etc/fess/fess_config.properties`」と記載しているが、RPM/DEBパッケージ以外のインストール方法(ZIP/tar.gz展開)の場合のパスについて明確でない。

#### m3: `http.proxy.port`のデフォルト値の記載漏れ (setup-port-network.rst)

`fess_config.properties`のHTTPプロキシ設定の例で、`http.proxy.port=8080`と例示しているが、実際のソースコードでもデフォルト値は`8080`に設定されている。これがデフォルト値であることを明記すべき。

#### m4: Windowsサービスドキュメントでservice.batのポート変更方法の記載漏れ (setup-windows-service.rst)

`service.bat`内の`FESS_PARAMS`にも`-Dfess.port=8080`がハードコードされているため、ポートを変更する場合は`fess.in.bat`だけでなく`service.bat`の`FESS_PARAMS`も変更する必要がある。ドキュメントではこの点に言及がない。

#### m5: intro.rstの内容が一般的すぎる

`intro.rst`はFess 15.6固有の情報を含まず、バージョンに関わらず同一の内容。設定ガイドの前提条件（Java 21+、OpenSearchのバージョン等）が記載されていない。

#### m6: Java GCチューニングのリンクがJava 11向け (setup-memory.rst, 414行目)

参考情報のリンク`https://docs.oracle.com/en/java/javase/11/gctuning/`がJava 11向け。Fess 15.6はJava 21+を要件としているため、Java 21向けのリンクに更新すべき。

## ファイル別詳細

### setup-memory.rst

| 項目 | 結果 |
|------|------|
| `FESS_HEAP_SIZE`環境変数 | ソースで確認済み（fess.in.sh:18-20, fess.in.bat:24-26） |
| `jvm.crawler.options`のデフォルト値 `-Xms128m -Xmx512m` | ソースで確認済み（fess_config.properties:57-58） |
| `jvm.suggest.options`のデフォルト値 `-Xms128m -Xmx256m` | ソースで確認済み（fess_config.properties:98-99） |
| `jvm.thumbnail.options`のデフォルト値 `-Xms128m -Xmx256m` | ソースで確認済み（fess_config.properties:130-131） |
| クローラーJVMオプション `-XX:MaxMetaspaceSize=128m` | ソースで確認済み（fess_config.properties:59） |
| クローラーJVMオプション `-XX:+UseG1GC` | ソースで確認済み（fess_config.properties:67） |
| クローラーJVMオプション `-XX:MaxGCPauseMillis=60000` | ソースで確認済み（fess_config.properties:70） |
| クローラーJVMオプション `-XX:-HeapDumpOnOutOfMemoryError` | ソースで確認済み（fess_config.properties:64） |
| OpenSearch APIポート `9201` | ソースで確認済み（fess_config.properties:17） |
| 参考リンク先ドキュメント | 存在確認済み |

### setup-port-network.rst

| 項目 | 結果 |
|------|------|
| デフォルトポート 8080 | ソースで確認済み（fess.in.sh:114, fess.in.bat:115） |
| OpenSearch HTTPポート 9201 | ソースで確認済み（fess_config.properties:17） |
| OpenSearch Transportポート 9301 | ソース内に直接的な定義なし（OpenSearch側の設定） |
| `FESS_PORT`環境変数 | Linux版のみ対応（fess.in.sh:113-114）。Windows版は非対応 |
| `fess.port`システムプロパティ | ソースで確認済み |
| `fess.context.path`システムプロパティ | ソースで確認済み |
| `FESS_CONTEXT_PATH`環境変数 | Linux版のみ対応（fess.in.sh:116-117） |
| `http.fileupload.max.size`デフォルト 262144000 | ソースで確認済み（fess_config.properties:286） |
| `http.fileupload.threshold.size`デフォルト 262144 | ソースで確認済み（fess_config.properties:288） |
| `http.fileupload.max.file.count`デフォルト 10 | ソースで確認済み（fess_config.properties:290） |
| `search_engine.http.url`デフォルト http://localhost:9201 | ソースで確認済み（fess_config.properties:17） |
| `search_engine.heartbeat_interval`デフォルト 10000 | ソースで確認済み（fess_config.properties:25） |
| `search_engine.http.ssl.certificate_authorities` | ソースで確認済み（fess_config.properties:19） |
| `search_engine.username` / `search_engine.password` | ソースで確認済み（fess_config.properties:21-23） |
| `virtual.host.headers` | ソースで確認済み（fess_config.properties:275） |
| `http.proxy.host` / `http.proxy.port` | ソースで確認済み（fess_config.properties:278-280） |
| `http.proxy.username` / `http.proxy.password` | ソースで確認済み（fess_config.properties:282-284） |
| `FESS_PROXY_HOST`等の環境変数 | ソースで確認済み（fess.in.sh:56-68, fess.in.bat:58-69） |
| クローラー用プロキシ `client.proxyHost`等 | fess-crawlerのHcHttpClient.javaで確認済み |

### setup-windows-service.rst

| 項目 | 結果 |
|------|------|
| `SEARCH_ENGINE_HOME`の設定 | ソースで確認済み（fess.in.bat:105） |
| `fess.port`の設定 | ソースで確認済み（fess.in.bat:115） |
| `service.bat install`コマンド | ソースで確認済み（service.bat:54） |
| サービスID `fess-service-x64` | ソースで確認済み（service.bat:29） |
| `opensearch-service.bat install`コマンド | OpenSearch側の機能（Fessソースでは確認対象外） |

### intro.rst

一般的な導入テキストのみ。技術的な設定値は含まれないため、ソースコードとの照合は不要。

### index.rst

目次構成のみ。参照先の各rstファイルは存在を確認済み。

## 推奨事項

1. **[M1対応]** `setup-memory.rst`にLinux/Windowsのデフォルトメモリ値の違いと、`FESS_MIN_MEM`/`FESS_MAX_MEM`環境変数の説明を追記する。
2. **[M2対応]** `setup-port-network.rst`の環境変数セクションに、`FESS_PORT`と`FESS_CONTEXT_PATH`がLinux環境のみで有効であること、Windows環境では`fess.in.bat`を直接編集する必要があることを明記する。
3. **[M3対応]** コンテキストパスの設定方法を`FESS_CONTEXT_PATH`環境変数の利用に修正する。
4. **[M4対応]** OpenSearchのメモリ設定セクションで`OPENSEARCH_HEAP_SIZE`の代わりに`config/jvm.options`での設定を主たる方法として推奨する。
5. **[m4対応]** `setup-windows-service.rst`にサービス登録時のポート変更方法（`service.bat`の`FESS_PARAMS`の編集）を追記する。
6. **[m6対応]** Java GCチューニングのリンクをJava 21向けに更新する。
7. **[m5対応]** `intro.rst`にFess 15.6の前提条件（Java 21+、OpenSearch 2.x等）を追記することを検討する。
