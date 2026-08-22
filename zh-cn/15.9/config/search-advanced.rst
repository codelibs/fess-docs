===========
搜索相关配置
===========

以下说明的配置在 fess_config.properties 中指定。
变更后需要重启 |Fess|\ 。

模糊搜索
=========

对4个字符以上应用模糊搜索，1个字符差异也会命中。
要禁用此配置，请指定 ``-1``\ 。
::

    query.boost.fuzzy.min.length=-1

初始值为 ``4``\ 。模糊搜索的详细配置请参阅后文"关联度（提升值）的配置"。

搜索超时值
==========

可以以毫秒为单位指定搜索时的超时值。
初始值为10秒（10000毫秒）。
::

    query.timeout=10000

搜索最大字符数
==============

可以指定搜索查询的最大字符数。
超过此值的搜索查询将不被受理。
初始值为1000个字符。
::

    query.max.length=1000

搜索超时日志输出
================

搜索时超时情况下的日志输出配置。
初始值为 ``true``\ （启用）。
::

    query.timeout.logging=true

命中数量显示
============

指定精确统计命中数量的上限。
初始值下，命中10,000条以上时会显示如下内容。

``xxxxx 的搜索结果 约 10,000 条以上 1 - 10 条 (4.94 秒)``

如需显示超过10,000条的精确命中数量，请指定更大的值。
::

    query.track.total.hits=10000

.. note::
   设置较大的值可能会影响搜索性能。请根据使用情况设置适当的值。

搜索结果最大偏移量
==================

指定搜索结果中可获取的偏移量（搜索起始位置）的上限。
当指定的偏移量超过此值时，搜索将返回错误。
此值作为分页跳转到较深页面时的上限值。
初始值为100000。
::

    query.max.search.result.offset=100000

OR搜索再搜索阈值
================

当普通搜索的命中数量不超过此处指定的值时，将搜索运算符切换为OR并重新搜索。
通过此功能，即使AND搜索命中数量较少，也可以补充搜索结果。
初始值为 ``-1``，此功能默认禁用。
::

    query.orsearch.min.hit.count=-1

位置信息搜索字段名
==================

指定位置信息搜索时的目标字段名。
指定多个字段时请用逗号分隔。
初始值为 ``location``\ 。
::

    query.geo.fields=location

位置信息搜索的使用方法请参阅 :doc:`search-geosearch`。

请求参数语言指定
================

指定通过请求参数指定语言时的参数名。
例如，通过URL传递请求参数 ``browser_lang=en`` 时，页面显示语言会切换为英语。
::

    query.browser.lang.parameter.name=browser_lang

搜索默认语言
============

以逗号分隔指定搜索时的默认目标语言。
如果设置了值，将优先于请求参数和浏览器语言使用。
初始值为空（未指定），使用请求参数或浏览器语言。
::

    query.default.languages=

语言代码映射
============

指定搜索时使用的语言代码规范化映射。
将浏览器或请求传入的语言代码转换为 |Fess| 内部使用的语言代码。
通常无需更改。初始值中已定义主要语言的映射。
::

    query.language.mapping=\
    ar=ar\n\
    bg=bg\n\
    ...

前方一致搜索指定
================

当搜索词末尾带有 ``*`` 时（例如：``搜索*``），将该词作为前方一致查询进行搜索。
初始值为 ``true``\ （启用）。指定 ``false`` 时，末尾带有 ``*`` 的词语将直接作为原文搜索。
::

    query.replace.term.with.prefix.query=true

高亮字符串
==========

用此处指定的字符串分隔句子，实现自然的高亮显示。
指定的字符串以u为起始分隔符，转换为Unicode字符。
::

    query.highlight.terminal.chars=u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61

初始值设置如下。（解码转换后的内容）

``! , . ? ։ ؟ ۔ ܀ ܁ ܂ । ၊ ။ ። ፧ ፨ ᙮ ᠃ ᠉ ‼ ‽ ⁇ ⁈ ⁉ 。 ﹒ ﹗ ！ ． ？ ｡``

高亮片段
========

指定从OpenSearch获取的高亮片段字符数和片段数。
::

    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

高亮生成方法
============

指定OpenSearch的高亮生成方法。
::

    query.highlight.type=fvh

高亮目标标签
============

指定高亮目标的开始和结束标签。
::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>

传递给OpenSearch高亮器的值
==========================

指定传递给OpenSearch高亮器的值。
::

    query.highlight.boundary.chars=u0009u000Au0013u0020
    query.highlight.boundary.max.scan=20
    query.highlight.boundary.scanner=chars
    query.highlight.encoder=default

高亮高级设置
============

用于控制高亮详细行为的配置。
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

添加到响应的字段名
==================

指定添加到普通搜索或API搜索响应中的字段名。
分别对应普通搜索、API（JSON/GSA）搜索、滚动搜索、缓存显示时的响应。
::

    query.additional.response.fields=
    query.additional.api.response.fields=
    query.additional.scroll.response.fields=
    query.additional.cache.response.fields=

滚动搜索响应字段的详细信息请参阅 :doc:`search-scroll`。

添加字段名
==========

用于添加搜索字段名、分面字段名、排序目标字段名等时指定。
::

    query.additional.default.fields=
    query.additional.search.fields=
    query.additional.facet.fields=
    query.additional.sort.fields=
    query.additional.highlighted.fields=
    query.additional.analyzed.fields=
    query.additional.not.analyzed.fields=

各配置的含义如下。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 配置
     - 说明
   * - ``query.additional.default.fields``
     - 添加到未指定字段的查询中作为默认搜索目标的字段。
   * - ``query.additional.search.fields``
     - 添加到可通过字段指定进行搜索的字段。
   * - ``query.additional.facet.fields``
     - 添加到可用作分面的字段。
   * - ``query.additional.sort.fields``
     - 添加到可用作排序目标的字段。
   * - ``query.additional.highlighted.fields``
     - 添加到作为高亮目标的字段。
   * - ``query.additional.analyzed.fields``
     - 添加到由Analyzer进行解析处理的字段。
   * - ``query.additional.not.analyzed.fields``
     - 添加到不由Analyzer进行解析的字段。

相似文档折叠（collapse）
========================

这是使用 ``content_minhash_bits`` 字段对相似（近似重复）文档进行折叠显示的collapse功能配置。
``query.collapse.inner.hits.name`` 是在搜索结果中存储相似文档的字段名，
``query.collapse.inner.hits.size`` 是每组获取的相似文档数量（``0`` 表示不获取），
``query.collapse.inner.hits.sorts`` 是获取相似文档时的排序条件，
``query.collapse.max.concurrent.group.results`` 是组获取时的最大并发请求数。
::

    query.collapse.max.concurrent.group.results=4
    query.collapse.inner.hits.name=similar_docs
    query.collapse.inner.hits.size=0
    query.collapse.inner.hits.sorts=

搜索偏好
========

在JSON格式的API搜索时，指定传递给OpenSearch的偏好值（决定搜索分片的值）。
指定 ``_query`` 时，搜索查询的哈希值将用作偏好值，相同查询会被分配到相同的分片。
初始值为 ``_query``\ 。
::

    query.json.default.preference=_query

关联度（提升值）的配置
======================

指定搜索时关联度（评分）计算中使用的提升值。
带有 ``.lang`` 的配置是针对语言专属字段（例如：``content_ja``）的提升值。
::

    query.boost.title=0.5
    query.boost.title.lang=1.0
    query.boost.content=0.05
    query.boost.content.lang=0.1
    query.boost.important_content=-1.0
    query.boost.important_content.lang=-1.0

模糊搜索的提升值及行为通过以下配置指定。
``query.boost.fuzzy.min.length`` 是应用模糊搜索的最小字符数（``-1`` 表示禁用）。
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

查询类型配置
============

指定搜索时使用的查询种类及其详细行为。
``query.default.query_type`` 是默认使用的查询类型，
``query.dismax.tie_breaker`` 是dismax查询的tie breaker值，
``query.bool.minimum_should_match`` 是bool查询的minimum_should_match值（为空时不指定）。
::

    query.default.query_type=bool
    query.dismax.tie_breaker=0.1
    query.bool.minimum_should_match=

前缀搜索与模糊搜索的详细配置
=============================

指定前缀查询及模糊查询的详细行为。
::

    query.prefix.expansions=50
    query.prefix.slop=0
    query.fuzzy.prefix_length=0
    query.fuzzy.expansions=50
    query.fuzzy.transpositions=true

分面配置
========

指定分面搜索的默认行为。
``query.facet.fields`` 是分面目标字段，
``query.facet.fields.size`` 是获取分面数量的上限，
``query.facet.fields.min_doc_count`` 是分面中显示的最小文档数，
``query.facet.fields.sort`` 是分面的排序顺序，
``query.facet.fields.missing`` 是分配给不存在值的文档的值。
::

    query.facet.fields=label
    query.facet.fields.size=100
    query.facet.fields.min_doc_count=1
    query.facet.fields.sort=count.desc
    query.facet.fields.missing=

以GSA兼容XML格式获取搜索结果的配置
===================================

用于以GSA兼容XML格式获取搜索结果。

指定使用GSA兼容XML格式时添加到响应的字段名。
    ::

        query.gsa.response.fields=UE,U,T,RK,S,LANG

指定使用GSA兼容XML格式时的语言。
    ::

        query.gsa.default.lang=en

指定使用GSA兼容XML格式时的默认排序。
    ::

        query.gsa.default.sort=

指定使用GSA兼容XML格式时的元数据前缀。
    ::

        query.gsa.meta.prefix=MT_

指定使用GSA兼容XML格式时的charset字段。
    ::

        query.gsa.index.field.charset=charset

指定使用GSA兼容XML格式时的content_type字段。
    ::

        query.gsa.index.field.content_type.=content_type

指定使用GSA兼容XML格式时的默认preference。
    ::

        query.gsa.default.preference=_query
