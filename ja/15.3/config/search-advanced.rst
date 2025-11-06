===========
検索関連の設定
===========

以下で説明している設定は fess_config.properties で指定します。
変更後は |Fess| の再起動が必要です。

ファジー検索
=========

4文字以上はファジー検索が適用されており、1文字違いもヒットします。
この設定を無効にする場合は、 `-1` を指定します。
::

    query.boost.fuzzy.min.length=-1

検索時のタイムアウト値
=================

検索時のタイムアウト値を指定することができます。
初期値は10秒です。
::

    query.timeout=10000

検索時の最大文字数
==============

検索時の最大文字数を指定することができます。
初期値は1000文字です。
::

    query.max.length=1000

検索時のタイムアウトのログ出力
=======================

検索時、タイムアウトした場合のログ出力設定です。
初期値は `true(有効)` です。
::

    query.timeout.logging=true

ヒット件数表示
===========

10,000 件以上のヒット件数表示が必要な場合に指定します。
初期値では、10,000万件以上ヒットする場合に以下のような表示になります。

`xxxxx の検索結果 約 10,000 件以上 1 - 10 件目 (4.94 秒)`

::
    
    query.track.total.hits=10000

位置情報検索時のインデックス名
=======================

位置情報検索時のインデックス名を指定します。
初期値は `location` です。
::

    query.geo.fields=location

リクエストパラメータの言語指定
=======================

リクエストパラメータで言語指定する場合のパラメーター名を指定します。
例えばリクエストパラメーターとして、 `browser_lang=en` のようにURLで渡すと、画面の表示言語が英語に切り替わります。
::

    query.browser.lang.parameter.name=browser_lang

前方一致検索の指定
==============

完全一致での検索時に `〜\*` で指定した場合、前方一致検索として検索します。
初期値は `true(有効)` です。
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

レスポンスに追加するフィールド名
========================

通常の検索、またはAPI検索時のレスポンスに追加するフィールド名を指定します。
::

    query.additional.response.fields=
    query.additional.api.response.fields=

フィールド名の追加
==============

検索フィールド名や、ファセットのフィールド名を追加する際に指定します。
::

    query.additional.search.fields=
    query.additional.facet.fields=

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
