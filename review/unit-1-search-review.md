# Unit 1: 検索関連ドキュメント レビューレポート

## 概要

以下の6ファイルについて、ソースコード（`repos/fess/src/main/resources/fess_config.properties`、`repos/fess/src/main/java/org/codelibs/fess/mylasta/direction/FessConfig.java`、関連Javaクラス）と照合してレビューを実施した。

- `ja/15.6/config/search-basic.rst`
- `ja/15.6/config/search-advanced.rst`
- `ja/15.6/config/search-form-integration.rst`
- `ja/15.6/config/search-geosearch.rst`
- `ja/15.6/config/search-scroll.rst`
- `ja/15.6/config/rank-fusion.rst`

**全体的な評価**: プロパティ名やデフォルト値は概ね正確であり、`fess_config.properties` との一致も良好。ただし、壊れたドキュメント内部リンクやセルフリファレンスなどの問題が検出された。

---

## 問題点

### [CRITICAL] 重大な問題

**該当なし** - 存在しないプロパティ名や完全に間違った参照先は検出されなかった。

### [MAJOR] 主要な問題

#### M1: rank-fusion.rst - 存在しないドキュメントへのリンク

- **ファイル**: `rank-fusion.rst` 行 161
- **内容**: `:doc:`../admin/search-settings` - 検索設定ガイド`
- **問題**: `ja/15.6/admin/search-settings.rst` は存在しない。`ja/15.6/admin/` 配下に該当ファイルがなく、ビルド時にリンクエラーが発生する。
- **推奨**: `../admin/general-guide` など、実在するファイルへの参照に修正するか、該当行を削除する。

#### M2: search-scroll.rst - セルフリファレンス（自己参照リンク）

- **ファイル**: `search-scroll.rst` 行 370
- **内容**: `:doc:`search-scroll` - 検索関連の設定`
- **問題**: 自分自身を参照している。「検索関連の設定」という説明文から判断すると、`search-advanced` を参照すべき。
- **推奨**: `:doc:`search-advanced` - 検索関連の設定` に修正する。

### [MINOR] 軽微な問題

#### m1: search-basic.rst - ファジー検索の説明がやや不正確

- **ファイル**: `search-basic.rst` 行 119
- **内容**: 「デフォルトでは、4文字以上のキーワードに対して自動的にファジー検索が適用されます。」
- **問題**: ソースコード（`TermQueryCommand.java` 行 261-262）を確認すると、`query.boost.fuzzy.min.length=4` が条件として使用されている。ただし「自動的に適用」という表現は、ファジー検索が常に追加の検索として実行されるものであり、メインの検索がファジーに切り替わるわけではない。混乱を招く可能性がある。
- **影響**: 低。検索品質に影響しない。

#### m2: search-basic.rst - 検索ログのインデックス名の記載

- **ファイル**: `search-basic.rst` 行 178
- **内容**: 「検索ログは OpenSearch の `fess_log` インデックスに保存され」
- **補足**: `fess_config.properties` の `index.log.index=fess_log` と一致しているが、実際にはプレフィックス付き（`fess_log.search_log` 等）の複数インデックスに分散されている。簡略化した記述としては許容範囲。

#### m3: search-advanced.rst - GSA関連プロパティの記載が不完全

- **ファイル**: `search-advanced.rst` 行 151-169
- **問題**: `fess_config.properties` に存在する以下のGSA関連プロパティが記載されていない:
  - `query.gsa.meta.prefix=MT_`
  - `query.gsa.index.field.charset=charset`
  - `query.gsa.index.field.content_type.=content_type`
  - `query.gsa.default.preference=_query`
- **影響**: 低。GSA互換機能を使うユーザーが詳細な設定を行う場合に情報不足となる可能性。

#### m4: search-advanced.rst - ハイライト関連プロパティの記載が不完全

- **ファイル**: `search-advanced.rst` 行 96-131
- **問題**: `fess_config.properties` に存在する以下のハイライト関連プロパティが記載されていない:
  - `query.highlight.force.source=false`
  - `query.highlight.fragmenter=span`
  - `query.highlight.fragment.offset=-1`
  - `query.highlight.no.match.size=0`
  - `query.highlight.order=score`
  - `query.highlight.phrase.limit=256`
  - `query.highlight.content.description.fields=hl_content,digest`
  - `query.highlight.boundary.position.detect=true`
  - `query.highlight.text.fragment.type=query`
  - `query.highlight.text.fragment.size=3`
  - `query.highlight.text.fragment.prefix.length=5`
  - `query.highlight.text.fragment.suffix.length=5`
- **影響**: 低。上級者向けの設定であり、基本的な使用には影響しない。

#### m5: search-geosearch.rst - APIエンドポイントの記載

- **ファイル**: `search-geosearch.rst` 行 205
- **内容**: `fetch('/json/?q=店舗&geo.location.point=...')` 
- **補足**: 旧API形式（`/json/`）が使用されている。同ファイルの他の箇所では `/api/v1/documents` 形式が使用されており、一貫性がない。ただし `/json/` も後方互換で動作するため、機能上の問題はない。

---

## ファイル別詳細

### search-basic.rst

**検証したプロパティ:**

| プロパティ名 | fess_config.properties | デフォルト値一致 | 備考 |
|---|---|---|---|
| `query.track.total.hits` | 存在する（行 720） | 記載値100000は変更例であり、デフォルト10000は正しく示唆されている | OK |
| `query.highlight.tag.pre` | 存在する（行 738） | `<strong>` - 一致 | OK |
| `query.highlight.tag.post` | 存在する（行 740） | `</strong>` - 一致 | OK |
| `query.highlight.fragment.size` | 存在する（行 732） | `60` - 一致 | OK |
| `query.highlight.number.of.fragments` | 存在する（行 734） | `2` - 一致 | OK |
| `query.timeout` | 存在する（行 716） | `10000` - 一致 | OK |
| `query.max.length` | 存在する（行 714） | `1000` - 一致 | OK |
| `query.boost.title` | 存在する（行 888） | 参照のみ（トラブルシューティング） | OK |
| `query.boost.content` | 存在する（行 892） | 参照のみ（トラブルシューティング） | OK |

**結論**: プロパティ名、デフォルト値ともに正確。設定ファイルの参照先（`fess_config.properties`）も正しい。

### search-advanced.rst

**検証したプロパティ:**

| プロパティ名 | fess_config.properties | デフォルト値一致 | 備考 |
|---|---|---|---|
| `query.boost.fuzzy.min.length` | 存在する（行 900） | `4`（暗黙的に示唆）、`-1`は無効化例 | OK |
| `query.timeout` | 存在する（行 716） | `10000` - 一致 | OK |
| `query.max.length` | 存在する（行 714） | `1000` - 一致 | OK |
| `query.timeout.logging` | 存在する（行 718） | `true` - 一致 | OK |
| `query.track.total.hits` | 存在する（行 720） | `10000` - 一致 | OK |
| `query.geo.fields` | 存在する（行 722） | `location` - 一致 | OK |
| `query.browser.lang.parameter.name` | 存在する（行 724） | `browser_lang` - 一致 | OK |
| `query.replace.term.with.prefix.query` | 存在する（行 726） | `true` - 一致 | OK |
| `query.highlight.terminal.chars` | 存在する（行 730） | 値が完全一致 | OK |
| `query.highlight.fragment.size` | 存在する（行 732） | `60` - 一致 | OK |
| `query.highlight.number.of.fragments` | 存在する（行 734） | `2` - 一致 | OK |
| `query.highlight.type` | 存在する（行 736） | `fvh` - 一致 | OK |
| `query.highlight.tag.pre` | 存在する（行 738） | `<strong>` - 一致 | OK |
| `query.highlight.tag.post` | 存在する（行 740） | `</strong>` - 一致 | OK |
| `query.highlight.boundary.chars` | 存在する（行 742） | 値が一致 | OK |
| `query.highlight.boundary.max.scan` | 存在する（行 744） | `20` - 一致 | OK |
| `query.highlight.boundary.scanner` | 存在する（行 746） | `chars` - 一致 | OK |
| `query.highlight.encoder` | 存在する（行 748） | `default` - 一致 | OK |
| `query.additional.response.fields` | 存在する（行 778） | 空文字 - 一致 | OK |
| `query.additional.api.response.fields` | 存在する（行 780） | 空文字 - 一致 | OK |
| `query.additional.search.fields` | 存在する（行 788） | 空文字 - 一致 | OK |
| `query.additional.facet.fields` | 存在する（行 790） | 空文字 - 一致 | OK |
| `query.gsa.response.fields` | 存在する（行 798） | `UE,U,T,RK,S,LANG` - 一致 | OK |
| `query.gsa.default.lang` | 存在する（行 800） | `en` - 一致 | OK |
| `query.gsa.default.sort` | 存在する（行 802） | 空文字 - 一致 | OK |

**結論**: すべてのプロパティ名、デフォルト値が正確。設定ファイルの参照先も正しい。ハイライトおよびGSA関連の一部プロパティが未記載（m3, m4参照）。

### search-form-integration.rst

**検証内容:**

- jQuery バージョン `3.7.1` - ソースコード（`src/main/webapp/js/jquery-3.7.1.min.js`）と一致
- `suggestor.js` - ソースコード（`src/main/webapp/js/suggestor.js`）に存在確認
- Suggest API エンドポイント `api/v1/suggest-words` - ソースコード（`SearchApiManager.java` 行 169）で確認
- 設定プロパティの直接的な参照なし

**結論**: 問題なし。HTMLコード例も現在のFessの実装と整合している。

### search-geosearch.rst

**検証したプロパティ:**

| プロパティ名 | fess_config.properties | デフォルト値一致 | 備考 |
|---|---|---|---|
| `query.geo.fields` | 存在する（行 722） | `location` - 一致 | OK |

**追加確認:**

- `location` フィールドの `geo_point` 型定義 - `src/main/resources/fess_indices/fess/doc.json` で確認（行 557-558）
- `app/WEB-INF/classes/fess_indices/fess/doc.json` のパス表記 - ランタイム時のパスとして正確
- リクエストパラメータ `geo.location.point`、`geo.location.distance` はAPIの実装と整合

**結論**: プロパティ、設定値ともに正確。旧API形式の混在（m5参照）のみ軽微な問題。

### search-scroll.rst

**検証したプロパティ:**

| プロパティ名 | fess_config.properties | デフォルト値一致 | 備考 |
|---|---|---|---|
| `api.search.scroll` | 存在する（行 226） | `false`（ドキュメントでは`true`に変更する例） | OK |
| `query.additional.scroll.response.fields` | 存在する（行 782） | 空文字（ドキュメントはカスタマイズ例を表示） | OK |

**追加確認:**

- APIエンドポイント `api/v1/documents/all` - `SearchApiManager.java` 行 152 で確認
- NDJSON形式 `application/x-ndjson` - `SearchApiManager.java` 行 266 で確認
- `scroll` パラメータのデフォルト値 `1m` - `SearchEngineClient.java` 行 228 で確認
- セルフリファレンス問題（M2参照）

**結論**: プロパティ、API仕様ともに正確。セルフリファレンスリンクの修正が必要（M2参照）。

### rank-fusion.rst

**検証したプロパティ:**

| プロパティ名 | fess_config.properties | デフォルト値一致 | 備考 |
|---|---|---|---|
| `rank.fusion.window_size` | 存在する（行 980） | `200` - 一致 | OK |
| `rank.fusion.rank_constant` | 存在する（行 982） | `20` - 一致 | OK |
| `rank.fusion.threads` | 存在する（行 984） | `-1` - 一致 | OK |
| `rank.fusion.score_field` | 存在する（行 986） | `rf_score` - 一致 | OK |

**追加確認:**

- FessConfig.java での定数定義確認済み（行 1225-1234）
- 壊れたリンク問題（M1参照）

**結論**: すべてのプロパティ名、デフォルト値が正確。壊れたドキュメントリンクの修正が必要（M1参照）。

---

## 推奨事項

1. **[優先度: 高]** `rank-fusion.rst` の `../admin/search-settings` リンクを実在するファイルに修正する（M1）
2. **[優先度: 高]** `search-scroll.rst` のセルフリファレンスを `search-advanced` に修正する（M2）
3. **[優先度: 低]** `search-advanced.rst` のGSA関連セクションに不足プロパティを追記する（m3）
4. **[優先度: 低]** `search-advanced.rst` のハイライト関連セクションに上級者向けプロパティの参照を追記する（m4）
5. **[優先度: 低]** `search-geosearch.rst` のGoogleマップ連携例で旧API形式 `/json/` を `/api/v1/documents` に統一する（m5）
