===========
検索関連の設定
===========

以下で説明している設定は fess_config.properties で指定します。
変更後は |Fess| の再起動が必要です。

ファジー検索
=========

4文字以上はファジー検索が適用されており、1文字違いもヒットします。
この設定を無効にする場合は、 ``-1`` を指定します。
::

    query.boost.fuzzy.min.length=-1

初期値は ``4`` です。ファジー検索の詳細な設定については後述の「関連度(ブースト)の設定」を参照してください。

検索時のタイムアウト値
=================

検索時のタイムアウト値をミリ秒で指定することができます。
初期値は10秒(10000ミリ秒)です。
::

    query.timeout=10000

検索時の最大文字数
==============

検索クエリの最大文字数を指定することができます。
この値を超える長さの検索クエリは受け付けられません。
初期値は1000文字です。
::

    query.max.length=1000

検索時のタイムアウトのログ出力
=======================

検索時、タイムアウトした場合のログ出力設定です。
初期値は ``true`` (有効)です。
::

    query.timeout.logging=true

ヒット件数表示
===========

正確に計上するヒット件数の上限を指定します。
初期値では、10,000件以上ヒットする場合に以下のような表示になります。

``xxxxx の検索結果 約 10,000 件以上 1 - 10 件目 (4.94 秒)``

10,000 件を超える正確なヒット件数の表示が必要な場合に、より大きな値を指定します。
::

    query.track.total.hits=10000

.. note::
   大きな値を設定すると検索パフォーマンスに影響する可能性があります。利用状況に応じて適切な値を設定してください。

検索結果の最大オフセット
==================

検索結果として取得できるオフセット(検索開始位置)の上限を指定します。
この値を超えるオフセットが指定された場合、検索はエラーになります。
ページングで深いページまで遷移する場合の上限値として機能します。
初期値は100000です。
::

    query.max.search.result.offset=100000

OR検索による再検索のしきい値
=====================

通常の検索でのヒット件数がここで指定した値以下の場合に、検索演算子を OR に切り替えて再検索を行います。
これにより、AND検索でヒット件数が少ない場合でも結果を補完できます。
初期値は ``-1`` で、この機能は無効です。
::

    query.orsearch.min.hit.count=-1

位置情報検索時のフィールド名
=====================

位置情報検索時に対象とするフィールド名を指定します。
複数のフィールドを指定する場合はカンマ区切りで指定します。
初期値は ``location`` です。
::

    query.geo.fields=location

位置情報検索の利用方法については :doc:`search-geosearch` を参照してください。

リクエストパラメータの言語指定
=======================

リクエストパラメータで言語指定する場合のパラメーター名を指定します。
例えばリクエストパラメーターとして、 ``browser_lang=en`` のようにURLで渡すと、画面の表示言語が英語に切り替わります。
::

    query.browser.lang.parameter.name=browser_lang

検索対象のデフォルト言語
==================

検索時に対象とするデフォルトの言語をカンマ区切りで指定します。
値が設定されている場合、リクエストパラメータやブラウザの言語よりも優先して使用されます。
初期値は空(未指定)で、リクエストパラメータまたはブラウザの言語が使用されます。
::

    query.default.languages=

言語コードのマッピング
=================

検索時に使用する言語コードの正規化マッピングを指定します。
ブラウザやリクエストから渡された言語コードを、 |Fess| が内部で使用する言語コードへ変換します。
通常は変更する必要はありません。初期値には主要な言語のマッピングが定義されています。
::

    query.language.mapping=\
    ar=ar\n\
    bg=bg\n\
    ...

前方一致検索の指定
==============

検索語の末尾に ``*`` を付けた場合(例: ``検索*``)、その語句を前方一致クエリとして検索します。
初期値は ``true`` (有効)です。 ``false`` を指定すると、 ``*`` を末尾に持つ語句もそのまま検索します。
::

    query.replace.term.with.prefix.query=true

ハイライトの文字列
==============

ここで指定した文字列で文を区切り、自然な形のハイライト表示を実現します。
指定する文字列は、uを開始区切り文字としてUnicodeの文字にします。
::

    query.highlight.terminal.chars=u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61

初期値は以下で設定されています。(デコード変換したものです)

``! , . ? ։ ؟ ۔ ܀ ܁ ܂ । ၊ ။ ። ፧ ፨ ᙮ ᠃ ᠉ ‼ ‽ ⁇ ⁈ ⁉ 。 ﹒ ﹗ ！ ． ？ ｡``

ハイライトのフラグメント
==================

OpenSearchから取得するハイライトのフラグメントの文字数や、フラグメント数を指定します。
::

    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

ハイライト生成方法
==============

OpenSearchのハイライトの生成方法を指定します。
::

    query.highlight.type=fvh

ハイライト対象のタグ
===============

ハイライト対象の開始と終了のタグを指定します。
::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>

OpenSearchのハイライターに渡す値
===========================

OpenSearchのハイライターに渡す値を指定します。
::

    query.highlight.boundary.chars=u0009u000Au0013u0020
    query.highlight.boundary.max.scan=20
    query.highlight.boundary.scanner=chars
    query.highlight.encoder=default

ハイライトの高度な設定
==================

ハイライトの詳細な動作を制御するための設定です。
::

    query.highlight.force.source=false
    query.highlight.fragmenter=span
    query.highlight.fragment.offset=-1
    query.highlight.no.match.size=0
    query.highlight.order=score
    query.highlight.phrase.limit=256
    query.highlight.content.description.fields=hl_content,digest
    query.highlight.boundary.position.detect=true
    query.highlight.text.fragment.type=query
    query.highlight.text.fragment.size=3
    query.highlight.text.fragment.prefix.length=5
    query.highlight.text.fragment.suffix.length=5

レスポンスに追加するフィールド名
========================

通常の検索、またはAPI検索時のレスポンスに追加するフィールド名を指定します。
それぞれ、通常の検索、API(JSON/GSA)検索、スクロール検索、キャッシュ表示時のレスポンスに対応します。
::

    query.additional.response.fields=
    query.additional.api.response.fields=
    query.additional.scroll.response.fields=
    query.additional.cache.response.fields=

スクロール検索のレスポンスフィールドの詳細については :doc:`search-scroll` を参照してください。

フィールド名の追加
==============

検索フィールド名や、ファセットのフィールド名、ソート対象のフィールド名などを追加する際に指定します。
::

    query.additional.default.fields=
    query.additional.search.fields=
    query.additional.facet.fields=
    query.additional.sort.fields=
    query.additional.highlighted.fields=
    query.additional.analyzed.fields=
    query.additional.not.analyzed.fields=

それぞれの設定の意味は以下のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 設定
     - 説明
   * - ``query.additional.default.fields``
     - フィールド指定のないクエリで検索対象とするデフォルトフィールドに追加します。
   * - ``query.additional.search.fields``
     - フィールド指定して検索できるフィールドに追加します。
   * - ``query.additional.facet.fields``
     - ファセットとして利用できるフィールドに追加します。
   * - ``query.additional.sort.fields``
     - ソート対象として利用できるフィールドに追加します。
   * - ``query.additional.highlighted.fields``
     - ハイライト対象とするフィールドに追加します。
   * - ``query.additional.analyzed.fields``
     - Analyzer による解析対象として扱うフィールドに追加します。
   * - ``query.additional.not.analyzed.fields``
     - Analyzer による解析を行わないフィールドに追加します。

類似ドキュメントの折りたたみ(collapse)
================================

類似(ニアデュプリケート)ドキュメントを ``content_minhash_bits`` フィールドで折りたたんで表示する collapse 機能の設定です。
``query.collapse.inner.hits.name`` は検索結果中で類似ドキュメントを格納するフィールド名、
``query.collapse.inner.hits.size`` は1グループあたりに取得する類似ドキュメント数(``0`` は取得しない)、
``query.collapse.inner.hits.sorts`` は類似ドキュメント取得時のソート条件、
``query.collapse.max.concurrent.group.results`` はグループ取得時の最大同時リクエスト数を表します。
::

    query.collapse.max.concurrent.group.results=4
    query.collapse.inner.hits.name=similar_docs
    query.collapse.inner.hits.size=0
    query.collapse.inner.hits.sorts=

検索プリファレンス
==============

JSON形式のAPI検索時に、OpenSearchへ渡すプリファレンス(検索するシャードを決める値)を指定します。
``_query`` を指定すると、検索クエリのハッシュ値がプリファレンスとして使用され、同一クエリが同じシャードに振り分けられます。
初期値は ``_query`` です。
::

    query.json.default.preference=_query

関連度(ブースト)の設定
==================

検索時の関連度(スコア)計算に使用するブースト値を指定します。
``.lang`` が付く設定は、言語別フィールド(例: ``content_ja``)に対するブースト値です。
::

    query.boost.title=0.5
    query.boost.title.lang=1.0
    query.boost.content=0.05
    query.boost.content.lang=0.1
    query.boost.important_content=-1.0
    query.boost.important_content.lang=-1.0

ファジー検索のブースト値や挙動は以下で指定します。
``query.boost.fuzzy.min.length`` はファジー検索を適用する最小文字数(``-1`` で無効)です。
::

    query.boost.fuzzy.min.length=4
    query.boost.fuzzy.title=0.01
    query.boost.fuzzy.title.fuzziness=AUTO
    query.boost.fuzzy.title.expansions=10
    query.boost.fuzzy.title.prefix_length=0
    query.boost.fuzzy.title.transpositions=true
    query.boost.fuzzy.content=0.005
    query.boost.fuzzy.content.fuzziness=AUTO
    query.boost.fuzzy.content.expansions=10
    query.boost.fuzzy.content.prefix_length=0
    query.boost.fuzzy.content.transpositions=true

クエリタイプの設定
==============

検索時に使用するクエリの種類や、その詳細な挙動を指定します。
``query.default.query_type`` は標準で使用するクエリタイプ、
``query.dismax.tie_breaker`` は dismax クエリの tie breaker 値、
``query.bool.minimum_should_match`` は bool クエリの minimum_should_match 値(空の場合は未指定)です。
::

    query.default.query_type=bool
    query.dismax.tie_breaker=0.1
    query.bool.minimum_should_match=

プレフィックス検索とファジー検索の詳細設定
==============================

プレフィックスクエリおよびファジークエリの詳細な挙動を指定します。
::

    query.prefix.expansions=50
    query.prefix.slop=0
    query.fuzzy.prefix_length=0
    query.fuzzy.expansions=50
    query.fuzzy.transpositions=true

ファセットの設定
============

ファセット検索のデフォルト動作を指定します。
``query.facet.fields`` はファセット対象のフィールド、
``query.facet.fields.size`` は取得するファセット数の上限、
``query.facet.fields.min_doc_count`` はファセットに表示する最小ドキュメント数、
``query.facet.fields.sort`` はファセットのソート順、
``query.facet.fields.missing`` は値が存在しないドキュメントに割り当てる値です。
::

    query.facet.fields=label
    query.facet.fields.size=100
    query.facet.fields.min_doc_count=1
    query.facet.fields.sort=count.desc
    query.facet.fields.missing=

検索結果をGSA互換のXML形式で取得する際の設定
===================================

検索結果をGSA互換のXML形式で取得する際に使用します。

GSA互換のXML形式を使用する時のレスポンスに追加するフィールド名を指定。
    ::

        query.gsa.response.fields=UE,U,T,RK,S,LANG

GSA互換のXML形式を使用する時の言語を指定。
    ::

        query.gsa.default.lang=en

GSA互換のXML形式を使用する時のデフォルトのソートを指定。
    ::

        query.gsa.default.sort=

GSA互換のXML形式を使用する時のメタデータのプレフィックスを指定。
    ::

        query.gsa.meta.prefix=MT_

GSA互換のXML形式を使用する時のcharsetフィールドを指定。
    ::

        query.gsa.index.field.charset=charset

GSA互換のXML形式を使用する時のcontent_typeフィールドを指定。
    ::

        query.gsa.index.field.content_type.=content_type

GSA互換のXML形式を使用する時のデフォルトのpreferenceを指定。
    ::

        query.gsa.default.preference=_query
