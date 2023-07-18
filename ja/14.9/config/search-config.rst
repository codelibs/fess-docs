==============
検索関連の設定
==============

以下で説明している設定は fess_config.properties で指定します。
変更後は |Fess| の再起動が必要です。

ファジー検索
============

4文字以上はファジー検索が適用されており、1文字違いもヒットします。
この設定を無効にする場合は、 `-1` を指定します。
::

    query.boost.fuzzy.min.length=-1

検索時のタイムアウト値
======================

検索時のタイムアウト値を指定することができます。
初期値は10秒です。
::

    query.timeout=10000

検索時の最大文字数
==================

検索時の最大文字数を指定することができます。
初期値は1000文字です。
::

    query.max.length=1000

検索時のタイムアウトのログ出力
==============================

検索時、タイムアウトした場合のログ出力設定です。
初期値は `true(有効)` です。
::

    query.timeout.logging=true

ヒット件数表示
==============

10,000 件以上のヒット件数表示が必要な場合に指定します。
初期値では、10,000万件以上ヒットする場合に以下のような表示になります。

`xxxxx の検索結果 約 10,000 件以上 1 - 10 件目 (4.94 秒)`

::
    
    query.track.total.hits=10000

位置情報検索時のインデックス名
==============================

位置情報検索時のインデックス名を指定します。
初期値は `location` です。
::

    query.geo.fields=location

リクエストパラメータの言語指定
==============================

リクエストパラメータで言語指定する場合のパラメーター名を指定します。
例えばリクエストパラメーターとして、 `browser_lang=en` のようにURLで渡すと、画面の表示言語が英語に切り替わります。
::

    query.browser.lang.parameter.name=browser_lang

前方一致検索の指定
==================

完全一致での検索時に `〜\*` で指定した場合、前方一致検索として検索します。
初期値は `true(有効)` です。
::

    query.replace.term.with.prefix.query=true

ハイライトの文字列
==================

ここで指定した文字列で文を区切り、自然な形のハイライト表示を実現します。
指定する文字列は、uを開始区切り文字としてUnicodeの文字にします。
::

    query.highlight.terminal.chars=u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61

初期値は以下で設定されています。(デコード変換したものです)

``! , . ? ։ ؟ ۔ ܀ ܁ ܂ । ၊ ။ ። ፧ ፨ ᙮ ᠃ ᠉ ‼ ‽ ⁇ ⁈ ⁉ 。 ﹒ ﹗ ！ ． ？ ｡``

ハイライトのフラグメント
========================

OpenSearchから取得するハイライトのフラグメントの文字数や、フラグメント数を指定します。
::

    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

ハイライト生成方法
==================

OpenSearchのハイライトの生成方法を指定します。
::

    query.highlight.type=fvh

ハイライト対象のタグ
====================

ハイライト対象の開始と終了のタグを指定します。
::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>

OpenSearchのハイライターに渡す値
================================

OpenSearchのハイライターに渡す値を指定します。
::

    query.highlight.boundary.chars=u0009u000Au0013u0020
    query.highlight.boundary.max.scan=20
    query.highlight.boundary.scanner=chars
    query.highlight.encoder=default

..
    TODO
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
        query.max.search.result.offset=100000
        query.additional.default.fields=


レスポンスに追加するフィールド名
================================

通常の検索、またはAPI検索時のレスポンスに追加するフィールド名を指定します。
::

    query.additional.response.fields=
    query.additional.api.response.fields=

..
    TODO
        query.additional.scroll.response.fields=
        query.additional.cache.response.fields=
        query.additional.highlighted.fields=


フィールド名の追加
==================

検索フィールド名や、ファセットのフィールド名を追加する際に指定します。
::

    query.additional.search.fields=
    query.additional.facet.fields=

..
    TODO
        query.additional.sort.fields=
        query.additional.analyzed.fields=
        query.additional.not.analyzed.fields=


検索結果をGSA互換のXML形式で取得する際の設定
============================================

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

..
    TODO
        query.gsa.meta.prefix=MT_
        query.gsa.index.field.charset=charset
        query.gsa.index.field.content_type.=content_type
        query.collapse.max.concurrent.group.results=4
        query.collapse.inner.hits.name=similar_docs
        query.collapse.inner.hits.size=0
        query.collapse.inner.hits.sorts=
        query.default.languages=
        query.json.default.preference=_query
        query.gsa.default.preference=_query
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
        query.boost.title=0.5
        query.boost.title.lang=1.0
        query.boost.content=0.05
        query.boost.content.lang=0.1
        query.boost.important_content=-1.0
        query.boost.important_content.lang=-1.0
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
        query.prefix.expansions=50
        query.prefix.slop=0
        query.fuzzy.prefix_length=0
        query.fuzzy.expansions=50
        query.fuzzy.transpositions=true
        query.facet.fields=label
        query.facet.fields.size=100
        query.facet.fields.min_doc_count=1
        query.facet.fields.sort=count.desc
        query.facet.fields.missing=
        query.facet.queries=\
        query.boost.title
        query.boost.title.lang
        query.boost.content
        query.boost.content.lang
        query.boost.important_content
        query.boost.important_content.lang
        query.boost.fuzzy.min.length
        query.boost.fuzzy.title
        query.boost.fuzzy.title.fuzziness
        query.boost.fuzzy.title.expansions
        query.boost.fuzzy.title.prefix_length
        query.boost.fuzzy.title.transpositions
        query.boost.fuzzy.content
        query.boost.fuzzy.content.fuzziness
        query.boost.fuzzy.content.expansions
        query.boost.fuzzy.content.prefix_length
        query.boost.fuzzy.content.transpositions
        query.prefix.expansions
        query.prefix.slop
        query.fuzzy.prefix_length
        query.fuzzy.expansions
        query.fuzzy.transpositions
        query.facet.fields
        query.facet.fields.size
        query.facet.fields.min_doc_count
        query.facet.fields.sort
        query.facet.fields.missing
        query.facet.queries

