===========
搜索相关配置
===========

以下说明的配置在 fess_config.properties 中指定。
变更后需要重启 |Fess|。

模糊搜索
=========

对4个字符以上应用模糊搜索,1个字符差异也会命中。
要禁用此配置,请指定 ``-1``。
::

    query.boost.fuzzy.min.length=-1

搜索超时值
=================

可以指定搜索时的超时值。
初始值为10秒。
::

    query.timeout=10000

搜索最大字符数
==============

可以指定搜索时的最大字符数。
初始值为1000个字符。
::

    query.max.length=1000

搜索超时日志输出
=======================

搜索时超时的日志输出配置。
初始值为 ``true(启用)``。
::

    query.timeout.logging=true

命中数量显示
===========

需要显示 10,000 条以上命中数量时指定。
初始值下,命中 10,000 条以上时会显示如下。

``xxxxx 的搜索结果 约 10,000 条以上 1 - 10 条 (4.94 秒)``

::

    query.track.total.hits=10000

位置信息搜索索引名
=======================

指定位置信息搜索时的索引名。
初始值为 ``location``。
::

    query.geo.fields=location

请求参数语言指定
=======================

指定通过请求参数指定语言时的参数名。
例如,通过 URL 传递请求参数 ``browser_lang=en`` 时,页面显示语言会切换为英语。
::

    query.browser.lang.parameter.name=browser_lang

前方一致搜索指定
==============

完全匹配搜索时用 ``〜\*`` 指定的情况下,作为前方一致搜索进行搜索。
初始值为 ``true(启用)``。
::

    query.replace.term.with.prefix.query=true

高亮字符串
==============

用这里指定的字符串分隔句子,实现自然的高亮显示。
指定的字符串以 u 作为起始分隔符转换为 Unicode 字符。
::

    query.highlight.terminal.chars=u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61

初始值设置如下。(解码转换后的内容)

``! , . ? ։ ؟ ۔ ܀ ܁ ܂ । ၊ ။ ። ፧ ፨ ᙮ ᠃ ᠉ ‼ ‽ ⁇ ⁈ ⁉ 。 ﹒ ﹗ ！ ． ？ ｡``

高亮片段
==================

指定从 OpenSearch 获取的高亮片段字符数和片段数。
::

    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

高亮生成方法
==============

指定 OpenSearch 的高亮生成方法。
::

    query.highlight.type=fvh

高亮对象标签
===============

指定高亮对象的开始和结束标签。
::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>

传递给 OpenSearch 高亮器的值
===========================

指定传递给 OpenSearch 高亮器的值。
::

    query.highlight.boundary.chars=u0009u000Au0013u0020
    query.highlight.boundary.max.scan=20
    query.highlight.boundary.scanner=chars
    query.highlight.encoder=default

添加到响应的字段名
========================

指定添加到普通搜索或 API 搜索响应中的字段名。
::

    query.additional.response.fields=
    query.additional.api.response.fields=

添加字段名
==============

添加搜索字段名或分面字段名时指定。
::

    query.additional.search.fields=
    query.additional.facet.fields=

以 GSA 兼容 XML 格式获取搜索结果的配置
===================================

用于以 GSA 兼容 XML 格式获取搜索结果。

指定使用 GSA 兼容 XML 格式时添加到响应的字段名。
    ::

        query.gsa.response.fields=UE,U,T,RK,S,LANG

指定使用 GSA 兼容 XML 格式时的语言。
    ::

        query.gsa.default.lang=en

指定使用 GSA 兼容 XML 格式时的默认排序。
    ::

        query.gsa.default.sort=
