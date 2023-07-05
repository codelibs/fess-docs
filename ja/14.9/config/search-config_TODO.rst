==============
検索関連の設定
==============

以下で説明している設定は fess_config.properties で指定します。
変更後は |Fess| の再起動が必要です。

ファジー検索
============

4文字以上はファジー検索が適用されており、1文字違いもヒットします。
この設定を無効にする場合は、 -1 を指定します。
::

    query.boost.fuzzy.min.length=-1

検索時のタイムアウト値
======================

検索時のタイムアウト値を指定することができます。
初期値は10秒です。

::

    query.timeout=10000

.. TODO 以下は未掲載です。一旦全ての項目を載せていますが、掲載しなくてよいものは削除していくイメージです。
.. すぐに書けそうなところはまでは書きました。

検索時の最大文字数
======================

検索時の最大文字数を指定することができます。
初期値は`1000文字`です。
::

    query.max.length=1000

検索時のタイムアウトのログ出力
==============================

検索時、タイムアウトした場合のログ出力設定です。
初期値は`true(有効)`です。
::

    query.timeout.logging=true

ヒット件数表示
==========================

10,000 件以上のヒット件数表示が必要な場合に指定します。
初期値では、10,000万件以上ヒットする場合に以下のような表示になります。
```
query の検索結果 約 10,000 件以上 1 - 10 件目 (4.94 秒)
```
::
    
    query.track.total.hits=10000

位置情報検索時のインデックス名
===============================

位置情報検索時のインデックス名を指定します。
初期値は`location`です。
::

    query.geo.fields=location

リクエストパラメータの言語指定
==============================

リクエストパラメータで言語指定する場合のパラメーター名を指定します。
例えばリクエストパラメーターとして、`browser_lang=en` のようにURLで渡すと、画面の表示言語が英語に切り替わります。
::

    query.browser.lang.parameter.name=browser_lang

前方一致検索の指定
===========================

完全一致での検索時に`〜\*`で指定した場合、前方一致検索として検索します。
初期値は`true(有効)`です。
::

    query.replace.term.with.prefix.query=true


ハイライトの文字列
===========================

ここで指定した文字列で文を区切り、自然な形のハイライト表示を実現します。
指定する文字列は、uを開始区切り文字としてUnicodeの文字にします。

::

    query.highlight.terminal.chars=u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61

初期値をデコード変換すると以下になります。

``! , . ? ։ ؟ ۔ ܀ ܁ ܂ । ၊ ။ ። ፧ ፨ ᙮ ᠃ ᠉ ‼ ‽ ⁇ ⁈ ⁉ 。 ﹒ ﹗ ！ ． ？ ｡``

ハイライトのフラグメント文字数
==============================

Elasticsearchから取得するハイライトのフラグメント文字数を指定します。
::

    query.highlight.fragment.size=60

ハイライトのフラグメント数
===========================

Elasticsearchから取得するハイライトのフラグメントの数を指定します。
::

    query.highlight.number.of.fragments=2

ハイライト生成方法
===========================

Elasticsearchのハイライトの生成方法を指定します。
::

    query.highlight.type=fvh

ハイライト対象のタグの開始
===========================


::

    query.highlight.tag.pre=<strong>

ハイライト対象のタグの終了
===========================

::

    query.highlight.tag.post=</strong>

ハイライタのパラメーターのboundary_chars
=========================================

Elasticsearchのハイライタのパラメーターのboundary_charsに渡す値。

::

    query.highlight.boundary.chars=u0009u000Au0013u0020

ハイライタのパラメーターのboundary_max_scan
============================================

Elasticsearchのハイライタのパラメーターのboundary_max_scanに渡す値。
::

    query.highlight.boundary.max.scan=20

ハイライタのパラメーターのboundary_scanner
===========================================

Elasticsearchのハイライタのパラメーターのboundary_scannerに渡す値。

::

    query.highlight.boundary.scanner=chars

ハイライタのパラメーターのencoder
==================================

Elasticsearchのハイライタのパラメーターのencoderに渡す値。

::

    query.highlight.encoder=default

TODO
===========================

::

    query.highlight.force.source=false

TODO
===========================

::

    query.highlight.fragmenter=span
    
TODO
===========================

::

    query.highlight.fragment.offset=-1

TODO
===========================

::

    query.highlight.no.match.size=0

TODO
===========================

::

    query.highlight.order=score

TODO
===========================

::

    query.highlight.phrase.limit=256

TODO
===========================

::

    query.highlight.content.description.fields=hl_content,digest

TODO
===========================

::

    query.highlight.boundary.position.detect=true

TODO
===========================

::

    query.highlight.text.fragment.type=query

TODO
===========================

::

    query.highlight.text.fragment.size=3

TODO
===========================

::

    query.highlight.text.fragment.prefix.length=5

TODO
===========================

::

    query.highlight.text.fragment.suffix.length=5

TODO
===========================

::

    query.max.search.result.offset=100000

TODO
===========================

::

    query.additional.default.fields=

レスポンスに追加するフィールド名
================================

レスポンスに追加するフィールド名を指定します。
::

    query.additional.response.fields=

API検索時のレスポンスに追加するフィールド名
===========================================

API検索時のレスポンスに追加するフィールド名を指定します。
::

    query.additional.api.response.fields=

TODO
===========================

::

    query.additional.scroll.response.fields=

TODO
===========================

::

    query.additional.cache.response.fields=

TODO
===========================

::

    query.additional.highlighted.fields=

検索フィールド名の追加
===========================

検索フィールド名を指定します。
::

    query.additional.search.fields=

ファセットフィールド名の追加
============================

ファセットのフィールド名を指定します。
::

    query.additional.facet.fields=

TODO
===========================

::

    query.additional.sort.fields=

TODO
===========================

::

    query.additional.analyzed.fields=

TODO
===========================

::

    query.additional.not.analyzed.fields=

GSA互換のXML形式でレスポンスに追加するフィールド名の追加
========================================================

GSA互換のXML形式を使用する時のレスポンスに追加するフィールド名を指定します。

::

    query.gsa.response.fields=UE,U,T,RK,S,LANG

GSA互換のXML形式で使用する言語
===============================

GSA互換のXML形式を使用する時の言語を指定します。

::

    query.gsa.default.lang=en

GSA互換のXML形式で使用するデフォルトソート
============================================

GSA互換のXML形式を使用する時のデフォルトのソートを指定します。
::

    query.gsa.default.sort=

TODO
===========================

::

    query.gsa.meta.prefix=MT_

TODO
===========================

::

    query.gsa.index.field.charset=charset

TODO
===========================

::

    query.gsa.index.field.content_type.=content_type

TODO
===========================

::

    query.collapse.max.concurrent.group.results=4

TODO
===========================

::

    query.collapse.inner.hits.name=similar_docs

TODO
===========================

::

    query.collapse.inner.hits.size=0

TODO
===========================

::

    query.collapse.inner.hits.sorts=

TODO
===========================

::

    query.default.languages=

TODO
===========================

::

    query.json.default.preference=_query

TODO
===========================

::

    query.gsa.default.preference=_query

TODO
===========================

::

    query.language.mapping=\
    ar=ar\n\
    bg=bg\n\
    bn=bn\n\
    ca=ca\n\
    ckb-iq=ckb-iq\n\
    ckb_IQ=ckb-iq\n\
    cs=cs\n\
    da=da\n\
    de=de\n\
    el=el\n\
    en=en\n\
    en-ie=en-ie\n\
    en_IE=en-ie\n\
    es=es\n\
    et=et\n\
    eu=eu\n\
    fa=fa\n\
    fi=fi\n\
    fr=fr\n\
    gl=gl\n\
    gu=gu\n\
    he=he\n\
    hi=hi\n\
    hr=hr\n\
    hu=hu\n\
    hy=hy\n\
    id=id\n\
    it=it\n\
    ja=ja\n\
    ko=ko\n\
    lt=lt\n\
    lv=lv\n\
    mk=mk\n\
    ml=ml\n\
    nl=nl\n\
    no=no\n\
    pa=pa\n\
    pl=pl\n\
    pt=pt\n\
    pt-br=pt-br\n\
    pt_BR=pt-br\n\
    ro=ro\n\
    ru=ru\n\
    si=si\n\
    sq=sq\n\
    sv=sv\n\
    ta=ta\n\
    te=te\n\
    th=th\n\
    tl=tl\n\
    tr=tr\n\
    uk=uk\n\
    ur=ur\n\
    vi=vi\n\
    zh-cn=zh-cn\n\
    zh_CN=zh-cn\n\
    zh-tw=zh-tw\n\
    zh_TW=zh-tw\n\
    zh=zh\n\

TODO
===========================

::

    query.boost.title=0.5

TODO
===========================

::

    query.boost.title.lang=1.0

TODO
===========================

::

    query.boost.content=0.05

TODO
===========================

::

    query.boost.content.lang=0.1

TODO
===========================

::

    query.boost.important_content=-1.0

TODO
===========================

::

    query.boost.important_content.lang=-1.0

TODO
===========================

::

    query.boost.fuzzy.min.length=4

TODO
===========================

::

    query.boost.fuzzy.title=0.01

TODO
===========================

::

    query.boost.fuzzy.title.fuzziness=AUTO

TODO
===========================

::

    query.boost.fuzzy.title.expansions=10

TODO
===========================

::

    query.boost.fuzzy.title.prefix_length=0

TODO
===========================

::

    query.boost.fuzzy.title.transpositions=true

TODO
===========================

::

    query.boost.fuzzy.content=0.005

TODO
===========================

::

    query.boost.fuzzy.content.fuzziness=AUTO

TODO
===========================

::

    query.boost.fuzzy.content.expansions=10

TODO
===========================

::

    query.boost.fuzzy.content.prefix_length=0

TODO
===========================

::

    query.boost.fuzzy.content.transpositions=true


TODO
===========================

::

    query.prefix.expansions=50

TODO
===========================

::

    query.prefix.slop=0

TODO
===========================

::

    query.fuzzy.prefix_length=0

TODO
===========================

::

    query.fuzzy.expansions=50

TODO
===========================

::

    query.fuzzy.transpositions=true

# facet

TODO
===========================

::

    query.facet.fields=label

TODO
===========================

::

    query.facet.fields.size=100

TODO
===========================

::

    query.facet.fields.min_doc_count=1

TODO
===========================

::

    query.facet.fields.sort=count.desc

TODO
===========================

::

    query.facet.fields.missing=

TODO
===========================

::

    query.facet.queries=\


TODO
===========================

::

    query.boost.title

TODO
===========================

::

    query.boost.title.lang

TODO
===========================

::

    query.boost.content

TODO
===========================

::

    query.boost.content.lang

TODO
===========================

::

    query.boost.important_content

TODO
===========================

::

    query.boost.important_content.lang

TODO
===========================

::

    query.boost.fuzzy.min.length

TODO
===========================

::

    query.boost.fuzzy.title

TODO
===========================

::

    query.boost.fuzzy.title.fuzziness

TODO
===========================

::

    query.boost.fuzzy.title.expansions

TODO
===========================

::

    query.boost.fuzzy.title.prefix_length

TODO
===========================

::

    query.boost.fuzzy.title.transpositions

TODO
===========================

::

    query.boost.fuzzy.content

TODO
===========================

::

    query.boost.fuzzy.content.fuzziness

TODO
===========================

::

    query.boost.fuzzy.content.expansions

TODO
===========================

::

    query.boost.fuzzy.content.prefix_length

TODO
===========================

::

    query.boost.fuzzy.content.transpositions


TODO
===========================

::

    query.prefix.expansions

TODO
===========================

::

    query.prefix.slop

TODO
===========================

::

    query.fuzzy.prefix_length

TODO
===========================

::

    query.fuzzy.expansions

TODO
===========================

::

    query.fuzzy.transpositions



TODO
===========================

::

    query.facet.fields

TODO
===========================

::

    query.facet.fields.size

TODO
===========================

::

    query.facet.fields.min_doc_count

TODO
===========================

::

    query.facet.fields.sort

TODO
===========================

::

    query.facet.fields.missing

TODO
===========================

::

    query.facet.queries

