=============================
Bang 检索（在其他网站上搜索）
=============================

Bang 会把搜索发送到其他网站，而不是在 |Fess| 中搜索。它的用法与 DuckDuckGo 的 bang 相同：在检索词中加入 ``!`` 和一个简短的触发词，|Fess| 就会把检索词的其余部分发送到该触发词所代表的网站。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 检索词
     - 发送到
   * - ``airplane !g``
     - Google，搜索 ``airplane``
   * - ``!w Ohm's law``
     - Wikipedia，搜索 ``Ohm's law``
   * - ``!g``
     - Google 首页
   * - ``airplane !unknown``
     - |Fess| 中的普通检索（``!`` 表示 NOT，请参阅 :doc:`search-not`）

Bang 由 ``fess-webapp-bangs`` 插件提供，需要 |Fess| 15.10 或更高版本。请在管理界面的[系统 > 插件]中，或使用 ``bin/fess-setup install plugin fess-webapp-bangs`` 安装（请参阅 :doc:`../admin/plugin-guide`），然后重启 |Fess|。

Bang 的识别条件
===============

- Bang 是 ``!`` 后接触发词，需作为独立的词书写。触发词不区分大小写。
- Bang 会从检索词中移除，检索词的其余部分会被发送到该 bang 的 URL。
- 检索词中包含多个已定义的 bang 时，只有第一个生效。
- 未定义的触发词不是 bang。``!unknown`` 照常检索，并排除词 ``unknown``。
- ``-g`` 和 ``NOT g`` 仍然排除词 ``g``。只有 ``!g`` 是 bang。

搜索页面和 ``/api/v2/search`` 支持重定向：API 返回 ``redirect_url`` （请参阅 :doc:`../api/api-search`），|Fess| 自带的 ``bootstrap`` 主题会跳转到该 URL。其他主题需要进行同样的处理。

聊天、MCP、v1 API 和经典 JSON API、管理界面的搜索等无法重定向的调用方，不会把搜索发送到其他网站。它们会移除 bang，并检索检索词的其余部分。

定义 Bang
=========

Bang 通过系统属性 ``bangs.definitions`` 定义。可以写在 ``app/WEB-INF/conf/system.properties`` 中，也可以作为 ``-Dfess.system.bangs.definitions=...`` 传入。对 ``system.properties`` 的修改无需重启 |Fess| 即可生效。

值是以空白分隔的 ``触发词=URL`` 条目列表。URL 中的 ``{query}`` 会被替换为经过 URL 编码的其余检索词：

::

    bangs.definitions=g=https://www.google.com/search?q={query} w=https://en.wikipedia.org/wiki/Special:Search?search={query}

- 触发词不能包含空白、 ``(`` 、 ``)`` 、 ``!`` 、 ``"`` 、 ``=`` 或 ``:`` 。
- 只接受绝对 URL 的 ``http`` 或 ``https`` 。
- 不符合这些规则的条目不会被使用。|Fess| 日志中会输出警告，其他条目保持有效。
- 同一个触发词被定义两次时，使用第一个定义。
- 值为空时，所有 bang 都会被关闭。

未设置 ``bangs.definitions`` 时，可以使用以下 5 个 bang：

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 触发词
     - 网站
   * - ``g``
     - Google
   * - ``b``
     - Bing
   * - ``ddg``
     - DuckDuckGo
   * - ``w``
     - Wikipedia（英文）
   * - ``gh``
     - GitHub

设置 ``bangs.definitions`` 后，这个列表会被替换。若想保留默认的 bang 并再增加一个，请写出所需的全部条目。

相关主题
========

- :doc:`search-not` - NOT 检索
- :doc:`special-char` - 特殊字符与转义
- :doc:`../api/api-search` - 检索 API
