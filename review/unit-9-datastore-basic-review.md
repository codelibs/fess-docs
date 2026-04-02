# Unit 9: データストア（基本）ドキュメント レビューレポート

## 概要

以下のドキュメントファイルをソースコードと照合してレビューした。

- `ja/15.6/config/datastore/ds-overview.rst`
- `ja/15.6/config/datastore/ds-database.rst`
- `ja/15.6/config/datastore/ds-csv.rst`
- `ja/15.6/config/datastore/ds-json.rst`
- `ja/15.6/config/datastore/ds-elasticsearch.rst`
- `ja/15.6/config/datastore/ds-git.rst`
- `ja/15.6/config/datastore/index.rst`

照合対象のソースコード:
- `repos/fess-ds-db/src/main/java/.../DatabaseDataStore.java`
- `repos/fess-ds-csv/src/main/java/.../CsvDataStore.java` / `CsvListDataStore.java`
- `repos/fess-ds-json/src/main/java/.../JsonDataStore.java`
- `repos/fess-ds-elasticsearch/src/main/java/.../ElasticsearchDataStore.java` / `ElasticsearchListDataStore.java`
- `repos/fess-ds-git/src/main/java/.../GitDataStore.java`
- `repos/fess/src/main/java/.../ds/AbstractDataStore.java`

## 問題点

### [CRITICAL] 重大な問題

#### C1: CSVコネクタ - セルインデックスが0始まりと記載されているが、実際は1始まり

**ファイル**: `ds-csv.rst` 130-134行目

**ドキュメントの記述**:
```
url="https://example.com/product/" + data.cell0
title=data.cell1
content=data.cell2
price=data.cell3
```

**ソースコードの実態** (`CsvDataStore.java` 301行目):
```java
key = CELL_PREFIX + Integer.toString(i + 1);
```

`CELL_PREFIX` は `"cell"` で、ループ変数 `i` は0から始まるが `i + 1` で格納されるため、セルは `cell1`, `cell2`, `cell3`, ... の1始まりとなる。ドキュメントの `cell0` は存在しない。

**影響**: ヘッダーなしCSVを使用するユーザーがドキュメント通りに設定すると、データが正しくマッピングされない。

#### C2: CSVコネクタ - has_header_lineのデフォルト値が誤り

**ファイル**: `ds-csv.rst` 103行目

**ドキュメントの記述**: `has_header_line` のデフォルトは `true`

**ソースコードの実態** (`CsvDataStore.java` 211-220行目):
```java
protected boolean hasHeaderLine(final DataStoreParams paramMap) {
    final String value = paramMap.getAsString(HAS_HEADER_LINE_PARAM);
    if (StringUtil.isBlank(value)) {
        return false;
    }
    ...
}
```

デフォルトは `false`（ヘッダー行なし）である。

**影響**: ユーザーが `has_header_line` を省略した場合、ヘッダー行がデータとして処理される。

#### C3: Gitコネクタ - `delete_old_docs` パラメータはソースコードに存在しない

**ファイル**: `ds-git.rst` 69行目, 104行目, 260-270行目

**ドキュメントの記述**: `delete_old_docs=false` / `delete_old_docs=true` というパラメータが記載されている。

**ソースコードの実態**: `GitDataStore.java` にはこのパラメータの定数定義も参照コードも存在しない。ファイル削除はGitのDiffEntryの `ChangeType.DELETE` を検出して自動的に行われ、 `base_url` が設定されている場合にドキュメントが削除される。

**影響**: ユーザーが存在しないパラメータを設定しても何の効果もない。削除の動作はbase_urlの有無に依存する。

#### C4: Elasticsearch/OpenSearchコネクタ - スクリプトでの `data.` プレフィックスの記述が誤り

**ファイル**: `ds-elasticsearch.rst` 130-147行目, 150-156行目

**ドキュメントの記述**:
```
url=data.url
title=data.title
content=data.content
```
`data.<field_name>` でアクセスすると記載されている。

**ソースコードの実態** (`ElasticsearchDataStore.java` 189-199行目):
```java
resultMap.put("index", hit.getIndex());
resultMap.put("id", hit.getId());
...
resultMap.put("source", hit.getSourceAsMap());
```

ドキュメントのフィールドは `source` キーに格納されるため、スクリプトでアクセスするには `source.url`, `source.title` のように `source.` プレフィックスを使用する必要がある。また `data._id` ではなく `id`, `data._index` ではなく `index` でアクセスする。

**影響**: ドキュメント通りにスクリプトを設定すると、フィールドにアクセスできずデータが取得できない。

### [MAJOR] 主要な問題

#### M1: データベースコネクタ - パラメータ一覧に `fetch_size` が重複して記載

**ファイル**: `ds-database.rst` 101-117行目

パラメータ一覧テーブルで `fetch_size` が2回記載されている（101行目と117行目）。

#### M2: データベースコネクタ - ドキュメントに記載されていないパラメータがある

**ファイル**: `ds-database.rst`

ソースコードには以下のパラメータが存在するがドキュメントに記載がない:
- `default_mimetype`: BLOB/InputStreamカラムの抽出時に使用するデフォルトMIMEタイプ
- `column_label.<field>`: カラムラベルとフィールドの対応付け（BLOB処理時のMIMEタイプ/ファイル名推定用）
- `info.<key>`: JDBC接続時の追加プロパティ（例: `info.useSSL=false`）

#### M3: データベースコネクタ - スクリプトでのアクセス方法が `data.` プレフィックスではない

**ファイル**: `ds-database.rst` 123-131行目, 135行目

**ドキュメントの記述**:
```
url="https://example.com/articles/" + data.id
title=data.title
```
`data.<column_name>` でアクセスすると記載。

**ソースコードの実態**: `DatabaseDataStore.java` の `ResultSetParamMap` は、SQLの結果セットのカラムラベルを直接キーとして格納する（389行目）。スクリプトの評価は `AbstractDataStore.convertValue` で行われ、`paramMap` にキーが含まれていればそのまま値を返す。したがって `data.` プレフィックスなしで `id`, `title` として直接アクセスする。

#### M4: CSVコネクタ - ドキュメントに記載されていない多数のパラメータがある

**ファイル**: `ds-csv.rst`

ソースコードに存在するがドキュメントに記載されていないパラメータ:
- `escape_character`: エスケープ文字
- `skip_lines`: スキップする行数
- `ignore_line_patterns`: 無視する行の正規表現パターン
- `ignore_empty_lines`: 空行を無視するか
- `ignore_trailing_whitespaces`: 末尾の空白を無視するか
- `ignore_leading_whitespaces`: 先頭の空白を無視するか
- `null_string`: null値とみなす文字列
- `break_string`: 改行の置換文字列
- `escape_disabled`: エスケープ文字を無効にするか
- `quote_disabled`: 引用符を無効にするか

#### M5: CSVコネクタ - スクリプトでのアクセス方法が `data.` プレフィックスではない

**ファイル**: `ds-csv.rst` 119-134行目, 139-140行目

`data.<列名>` / `data.cell<N>` と記載されているが、CSVの場合はカラム名やcellNがresultMapに直接格納されるため、`data.` プレフィックスなしで直接参照する。

#### M6: JSONコネクタ - JSONファイル形式の説明が不正確

**ファイル**: `ds-json.rst` 156-176行目

**ドキュメントの記述**: 「配列形式のJSONファイルまたはJSONL形式のファイルを読み込みます」

**ソースコードの実態** (`JsonDataStore.java` 170-178行目):
```java
for (String line; (line = br.readLine()) != null;) {
    ...
    final Map<String, Object> source = objectMapper.readValue(line, ...);
```

ファイルを1行ずつ読み込み、各行をJSONオブジェクトとしてパースしている。つまりJSONL形式のみ対応であり、配列形式の複数行JSONファイルは処理できない。配列形式の場合は全体が1行に収まっている場合を除いて正しく動作しない。

#### M7: JSONコネクタ - スクリプトでのアクセスに `data.` プレフィックスは不要

**ファイル**: `ds-json.rst` 113-149行目

`data.<フィールド名>` と記載されているが、JSONの場合もフィールドがresultMapに直接展開される（179-181行目: `resultMap.putAll(source)`）ため、`data.` プレフィックスなしで直接参照する。

#### M8: Gitコネクタ - ドキュメントに記載されていないパラメータが多数ある

**ファイル**: `ds-git.rst`

ソースコードに存在するがドキュメントに記載されていないパラメータ:
- `username`: Git認証用ユーザー名（URIに埋め込む方法のみ記載）
- `password`: Git認証用パスワード
- `commit_id`: 対象コミットID（デフォルト: HEAD）
- `ref_specs`: refspec設定（デフォルト: `+refs/heads/*:refs/heads/*`）
- `default_extractor`: デフォルトの抽出器（デフォルト: `tikaExtractor`）
- `cache_threshold`: キャッシュの閾値（デフォルト: 1000000）
- `max_size`: 最大ファイルサイズ（デフォルト: 10000000）
- `include_pattern`: URLフィルタの包含パターン
- `exclude_pattern`: URLフィルタの除外パターン
- `repository_path`: 永続的なリポジトリのローカルパス

#### M9: Gitコネクタ - ブランチ指定方法が誤り

**ファイル**: `ds-git.rst` 466-471行目

**ドキュメントの記述**:
```
uri=https://github.com/company/repo.git#develop
```
`#` の後にブランチ名を指定するとされている。

**ソースコードの実態**: URIはそのまま `git.fetch().setRemote(uri)` に渡される。ブランチ切替は `commit_id` パラメータで行い、refspecは `ref_specs` パラメータで制御する。`#` によるブランチ指定の機能はソースコードに存在しない。

#### M10: Elasticsearch/OpenSearchコネクタ - ドキュメントに記載されていないパラメータがある

**ファイル**: `ds-elasticsearch.rst`

ソースコードに存在するがドキュメントに記載されていないパラメータ:
- `preference`: シャードの選択設定（デフォルト: `_local`）
- `timeout`: リクエストのタイムアウト（デフォルト: `1m`）
- `delete.processed.doc`: 処理済みドキュメントを削除するか（デフォルト: `false`）

#### M11: Gitコネクタ - スクリプトでの変数名が不正確

**ファイル**: `ds-git.rst` 109-121行目

ドキュメントの `author.toExternalString()` は正確ではない。ソースでは `author` に `PersonIdent` オブジェクトが格納され、`committer` も別途利用可能。また `content_length` ではなく `contentLength` が正しい変数名。

### [MINOR] 軽微な問題

#### m1: 概要ドキュメント - パフォーマンスチューニングのパラメータが一般的すぎる

**ファイル**: `ds-overview.rst` 236-253行目

`batch.size`, `interval`, `thread.size`, `timeout` といったパラメータが記載されているが、これらは全コネクタ共通のパラメータではなく、コネクタごとに異なるパラメータ名を持つ。共通で利用できるのは `readInterval`（AbstractDataStoreで定義）のみ。

#### m2: 概要ドキュメント - 認証パラメータ名が一般的

**ファイル**: `ds-overview.rst` 199-233行目

`client.id`, `client.secret`, `refresh.token` 等のOAuth関連パラメータが記載されているが、これらはコネクタごとに異なるため、一般的な説明として誤解を招く可能性がある。

#### m3: 概要ドキュメント - ログ設定のパスが不正確

**ファイル**: `ds-overview.rst` 285行目

`app/WEB-INF/classes/log4j2.xml` と記載されているが、Docker環境やインストール方式によってパスが異なる場合がある。

#### m4: 概要ドキュメント - プラグインインストールコマンド

**ファイル**: `ds-overview.rst` 127-130行目

`./bin/fess-plugin` コマンドが記載されているが、このコマンドの存在は未確認。管理画面またはJARファイル配置が標準的な方法。

#### m5: データベースコネクタ - 接続プーリングの説明が不正確

**ファイル**: `ds-database.rst` 203-211行目

`datasource.class` や `pool.size` というパラメータが記載されているが、`DatabaseDataStore.java` のソースでは `DriverManager.getConnection()` を使用しており、接続プーリング機能は実装されていない。

#### m6: CSVコネクタ - CsvListDataStoreハンドラの記載がない

**ファイル**: `ds-csv.rst`

`CsvListDataStore` という別のハンドラが存在し、ファイルリストとしてCSVを処理する機能を提供するが、ドキュメントに記載がない。

#### m7: Elasticsearch/OpenSearchコネクタ - ElasticsearchListDataStoreハンドラの記載がない

**ファイル**: `ds-elasticsearch.rst`

`ElasticsearchListDataStore` という別のハンドラが存在するが、ドキュメントに記載がない。

#### m8: データベースコネクタ - `:last_crawl_date` 記法

**ファイル**: `ds-database.rst` 147-150行目

SQLクエリ例で `:last_crawl_date` というパラメータバインド記法が使用されているが、`DatabaseDataStore` はPreparedStatementではなくStatementを使用しており、パラメータバインドはサポートされていない。

## ファイル別詳細

### ds-overview.rst
- 全体構成は良好で、利用可能なコネクタの一覧が分かりやすい
- パフォーマンスチューニングと認証の一般的な説明はコネクタ固有の実装と乖離がある
- プラグインインストール方法は管理画面経由の手順が正確

### ds-database.rst
- ハンドラ名 `DatabaseDataStore` は正確
- パラメータ名（`driver`, `url`, `username`, `password`, `sql`, `fetch_size`）はソースコードと一致
- `fetch_size` の重複記載を修正すべき
- スクリプトでの `data.` プレフィックスの記述を修正すべき
- BLOB/バイナリカラムの処理機能の記載が欠落

### ds-csv.rst
- ハンドラ名 `CsvDataStore` は正確
- パラメータ名（`files`, `file_encoding`, `has_header_line`, `separator_character`, `quote_character`, `directories`）はソースコードと一致
- セルインデックスの開始番号の誤り（0始まり→1始まり）は重大
- `has_header_line` のデフォルト値の誤りは重大
- 多数の追加パラメータの記載が欠落

### ds-json.rst
- ハンドラ名 `JsonDataStore` は正確
- パラメータ名（`files`, `directories`, `fileEncoding`）はソースコードと一致
- 配列形式JSONの対応可否について誤解を招く記述
- JSONLのみ対応であることを明記すべき

### ds-elasticsearch.rst
- ハンドラ名 `ElasticsearchDataStore` は正確
- パラメータ名（`settings.fesen.http.url`, `settings.fesen.username`, `settings.fesen.password`, `index`, `size`, `scroll`, `query`, `fields`）はソースコードと一致
- スクリプトでの `data.` プレフィックスが誤り（`source.` を使用すべき）

### ds-git.rst
- ハンドラ名 `GitDataStore` は正確
- パラメータ名（`uri`, `base_url`, `extractors`, `prev_commit_id`）はソースコードと一致
- `delete_old_docs` パラメータは存在しない
- ブランチ指定の `#` 記法は存在しない
- 重要なパラメータ（`commit_id`, `username`, `password`, `include_pattern`, `exclude_pattern`等）の記載が欠落

### index.rst
- toctreeの構成は正確で、すべてのドキュメントが適切にリンクされている
- 問題なし

## 推奨事項

1. **最優先**: CSVコネクタのセルインデックス開始番号を `cell0` から `cell1` に修正する
2. **最優先**: CSVコネクタの `has_header_line` デフォルト値を `false` に修正する
3. **最優先**: Elasticsearch/OpenSearchコネクタのスクリプト例を `source.` プレフィックスに修正する
4. **最優先**: Gitコネクタの `delete_old_docs` パラメータの記述を削除し、削除動作の正しい説明に置き換える
5. **高優先度**: 各コネクタのスクリプトでの `data.` プレフィックスの記述を実際のアクセス方法に合わせて修正する
6. **高優先度**: JSONコネクタの対応形式をJSONL（1行1JSONオブジェクト）のみであることを明記する
7. **高優先度**: Gitコネクタのブランチ指定方法を `commit_id` パラメータの説明に修正する
8. **中優先度**: 各コネクタのドキュメントに欠落しているパラメータを追加する
9. **中優先度**: データベースコネクタの接続プーリングの説明を削除または修正する
10. **低優先度**: 概要ドキュメントのパフォーマンスチューニングセクションを、各コネクタの実際のパラメータに合わせて修正する
