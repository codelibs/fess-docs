========
追加词汇
========

概述
====

本节介绍如何配置建议词汇的附加候选项。建议会根据搜索词显示，您可以添加更多词汇。

管理方法
======

显示方法
------

要打开下图所示的追加词汇配置列表页面，请点击左侧菜单中的 [建议 > 提升词]。

|image0|

要编辑配置，请点击配置名称。

创建配置
--------

要打开追加词汇配置页面，请点击新建按钮。

|image1|

配置项目
------

单词
::::

指定要显示为建议候选项的词汇。

读音
::::

指定建议候选词汇的读音。

权限
:::::::::::

为词汇设置角色信息。
只有具有配置角色的用户才能在建议中看到该词汇。
按用户指定为{user}用户名，按角色指定为{role}角色名，按组指定为{group}组名。

标签
:::::

为词汇设置标签。
如果选择了配置标签以外的标签，该词汇将不会显示在建议中。

提升值
::::::::

为词汇设置提升值。

.. note::
   注册、编辑或删除的追加词汇（包括通过上传 CSV）不会立即反映到建议中。当重建建议索引的“Suggest Indexer”作业运行时（默认每天 12:00 运行）才会生效。要立即生效，请在 [系统 > 调度器] 中单击“Suggest Indexer”，然后单击“立即开始”按钮。

删除配置
--------

点击列表页面中的配置名称，然后点击删除按钮将显示确认屏幕。
点击删除按钮后，配置将被删除。


下载
=========

以CSV格式下载已注册的词汇。

|image2|

CSV内容
--------

第1行是标题行。
第2行及以后记录追加词汇。

::

"SuggestWord","Reading","Permissions","Labels","Boost"
"fess","ふぇす","{role}role1","label1","100"

上传
=========

以CSV格式注册词汇。

|image3|

CSV内容
--------

第1行是标题行。
第2行及以后描述追加词汇。

::

"SuggestWord","Reading","Permissions","Labels","Boost"
"fess","ふぇす","{role}role1","label1","100"

.. note::
   在 Permissions 列中，请使用 ``{role}``、``{user}``、``{group}`` 之一作为前缀，例如 ``{role}role1``（多个值以逗号分隔）。像 ``role1`` 这样没有前缀的值不会被视为角色，该词汇也不会建议给拥有该角色的用户。


.. |image0| image:: ../../../resources/images/en/15.10/admin/elevateword-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/elevateword-2.png
.. |image2| image:: ../../../resources/images/en/15.10/admin/elevateword-3.png
.. |image3| image:: ../../../resources/images/en/15.10/admin/elevateword-4.png
