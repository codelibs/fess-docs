============
UI 配置 API
============

概述
====

UI 配置 API 返回单页应用程序（SPA）所需的初始配置（主题、功能开关、分页上限，以及在需要 CSRF 时返回新的 CSRF 令牌）。
本端点在登录前以匿名方式调用。

有关公共响应信封及错误模型，请参阅 :doc:`api-overview`。

获取 UI 配置
============

请求
----

==================  ====================================================
HTTP 方法            GET
端点                 ``/api/v2/ui/config``
==================  ====================================================

返回 SPA 所需的初始配置。

响应
----

成功时（HTTP 200，UiConfigResponse），返回如下公共信封格式的响应（部分摘录）。

.. code-block:: json

    {
      "response": {
        "status": 0,
        "site_name": "Fess",
        "login_required": false,
        "locales": ["en", "ja"],
        "theme": {
          "name": "default",
          "display_name": "Default Theme",
          "version": "1.0.0",
          "supported_locales": ["en", "ja"]
        },
        "features": {
          "user_favorite": false,
          "popular_word": true,
          "suggest_search_log": true,
          "suggest_documents": true,
          "login_required": false,
          "eoled": false,
          "development_mode": false,
          "search_log_enabled": true,
          "thumbnail_enabled": true,
          "display_label_type": false,
          "clipboard_copy_icon": true,
          "eol_link": "",
          "installation_link": "https://fess.codelibs.org/15.7/install/",
          "login_link": true,
          "rag_chat_enabled": false
        },
        "page_size_default": 20,
        "page_size_max": 100,
        "sort_options": [
          {"value": "", "label_key": "labels.search_result_sort_score_desc"}
        ],
        "num_options": [10, 20, 30, 40, 50, 100],
        "lang_options": [
          {"value": "all", "label_key": "labels.searchoptions_all_langs"},
          {"value": "ja", "label_key": "labels.lang_ja"}
        ],
        "label_options": [],
        "notifications": {
          "search_top": "",
          "advance_search": "",
          "login": ""
        },
        "facet_views": [],
        "filetype_options": [
          {"value": "html", "label_key": "labels.facet_filetype_html"}
        ],
        "csrf_required": true,
        "csrf_token": "0c1f2e3d4a5b6c7d8e9f"
      }
    }

``response`` 各元素说明如下。所有字段均为必填。

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: 响应信息
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 类型
     - 说明
   * - ``site_name``
     - string
     - 站点名称。当活动主题包含清单时为其显示名称（\ ``display_name``\ ），否则为 ``Fess``\ 。
   * - ``login_required``
     - boolean
     - 是否需要登录。
   * - ``locales``
     - string[]
     - 可用的语言区域数组。
   * - ``theme``
     - object
     - 当前活动主题描述符。详见下方表格。
   * - ``features``
     - object
     - 功能开关。详见下方表格。
   * - ``page_size_default``
     - integer
     - 默认每页条数。
   * - ``page_size_max``
     - integer
     - 每页条数的最大值。
   * - ``sort_options``
     - object[]
     - 搜索 UI 的排序选项。详见下方表格。
   * - ``num_options``
     - integer[]
     - 可选的每页条数数组。限定在不超过 ``page_size_max`` 的值。
   * - ``lang_options``
     - object[]
     - 语言过滤器选项。详见下方表格。
   * - ``label_options``
     - object[]
     - 已配置标签的选项。详见下方表格。
   * - ``notifications``
     - object
     - 在特定视图顶部显示的 HTML 通知片段。详见下方表格。
   * - ``facet_views``
     - object[]
     - 已配置的分面查询视图组。详见下方表格。
   * - ``filetype_options``
     - object[]
     - 高级搜索表单用的文件类型分面选项。详见下方表格。
   * - ``csrf_required``
     - boolean
     - 是否需要 CSRF 令牌。
   * - ``csrf_token``
     - string
     - 当 ``csrf_required`` 为 ``false`` 时为空字符串，否则为与当前会话绑定的新令牌。

theme
~~~~~

``theme`` 始终存在，但当请求未关联自定义主题时为空对象。
来自清单的键（\ ``display_name`` / ``version`` / ``supported_locales``\ ）仅在活动主题包含清单时存在。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: theme
   :header-rows: 1
   :widths: 28 15 57

   * - 字段
     - 类型
     - 说明
   * - ``name``
     - string
     - 主题名称。
   * - ``display_name``
     - string
     - 主题显示名称。
   * - ``version``
     - string
     - 主题版本。
   * - ``supported_locales``
     - string[]
     - 主题支持的语言区域数组。

features
~~~~~~~~

所有字段均为必填。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: features
   :header-rows: 1
   :widths: 28 15 57

   * - 字段
     - 类型
     - 说明
   * - ``user_favorite``
     - boolean
     - 用户收藏功能是否启用。
   * - ``popular_word``
     - boolean
     - 热门词功能是否启用。
   * - ``suggest_search_log``
     - boolean
     - 基于搜索日志的建议功能是否启用。
   * - ``suggest_documents``
     - boolean
     - 基于文档的建议功能是否启用。
   * - ``login_required``
     - boolean
     - 是否需要登录。
   * - ``eoled``
     - boolean
     - 此 |Fess| 构建版本是否已达到 EOL。
   * - ``development_mode``
     - boolean
     - 使用内置（开发用）搜索引擎时为 ``true``\ 。
   * - ``search_log_enabled``
     - boolean
     - 搜索日志是否启用。
   * - ``thumbnail_enabled``
     - boolean
     - 缩略图是否启用。
   * - ``display_label_type``
     - boolean
     - 配置了一个或多个标签时为 ``true``\ 。
   * - ``clipboard_copy_icon``
     - boolean
     - 是否显示剪贴板复制图标。
   * - ``eol_link``
     - string
     - 已解析的 EOL 信息 URL。未到 EOL 或无法解析时为空字符串。
   * - ``installation_link``
     - string
     - 已解析的安装指南 URL。无法解析时为空字符串。
   * - ``login_link``
     - boolean
     - 是否应显示登录链接。
   * - ``rag_chat_enabled``
     - boolean
     - RAG 聊天功能是否可用。

sort_options
~~~~~~~~~~~~

搜索 UI 的排序选项数组。
每个元素包含 ``value`` 和 ``label_key``\ 。
``click_count.*`` 项仅在搜索日志启用时存在，\ ``favorite_count.*`` 项仅在用户收藏启用时存在。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: sort_options 的元素
   :header-rows: 1
   :widths: 28 15 57

   * - 字段
     - 类型
     - 说明
   * - ``value``
     - string
     - 排序值。
   * - ``label_key``
     - string
     - 标签键。

num_options
~~~~~~~~~~~

可选的每页条数整数数组。限定在不超过 ``page_size_max`` 的值。

lang_options
~~~~~~~~~~~~

语言过滤器选项的数组。
每个元素包含 ``value`` 和 ``label_key``\ 。
首项为 ``all`` 哨兵，之后每种支持的语言代码各对应一项。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: lang_options 的元素
   :header-rows: 1
   :widths: 28 15 57

   * - 字段
     - 类型
     - 说明
   * - ``value``
     - string
     - 语言值。
   * - ``label_key``
     - string
     - 标签键。

label_options
~~~~~~~~~~~~~

已配置标签选项的数组。未定义标签时为空数组。
每个元素包含 ``value`` 和 ``name``\ 。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: label_options 的元素
   :header-rows: 1
   :widths: 28 15 57

   * - 字段
     - 类型
     - 说明
   * - ``value``
     - string
     - 标签值。
   * - ``name``
     - string
     - 标签名称。

notifications
~~~~~~~~~~~~~

在特定视图顶部显示的 HTML 通知片段。空字符串表示该视图无通知。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: notifications
   :header-rows: 1
   :widths: 28 15 57

   * - 字段
     - 类型
     - 说明
   * - ``search_top``
     - string
     - 在搜索顶部显示的通知。
   * - ``advance_search``
     - string
     - 在高级搜索中显示的通知。
   * - ``login``
     - string
     - 在登录页面显示的通知。

facet_views
~~~~~~~~~~~

已配置的分面查询视图组数组。未定义时为空数组。
每个元素包含 ``group_name`` 和 ``queries``\ 。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: facet_views 的元素
   :header-rows: 1
   :widths: 28 15 57

   * - 字段
     - 类型
     - 说明
   * - ``group_name``
     - string
     - 组名称。
   * - ``queries``
     - object[]
     - 该组的分面查询数组。每个元素包含 ``label_key``\ （string）和 ``value``\ （string）。

filetype_options
~~~~~~~~~~~~~~~~

高级搜索表单用的文件类型分面选项数组。
每个元素包含 ``value`` 和 ``label_key``\ 。

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: filetype_options 的元素
   :header-rows: 1
   :widths: 28 15 57

   * - 字段
     - 类型
     - 说明
   * - ``value``
     - string
     - 文件类型值。
   * - ``label_key``
     - string
     - 标签键。

错误响应
--------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应
   :header-rows: 1
   :widths: 25 75

   * - 状态码
     - 说明
   * - 405 Method Not Allowed
     - 指定了不支持的 HTTP 方法时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。
