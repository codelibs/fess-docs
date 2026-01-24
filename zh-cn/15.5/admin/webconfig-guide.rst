===========
网页爬取
===========

概述
====

网页爬取配置页面用于配置网页爬取的相关设置。

管理方法
======

显示方法
------

要打开下图所示的网页爬取配置列表页面,请点击左侧菜单中的[爬虫 > 网页]。

|image0|

点击配置名称即可进行编辑。

创建配置
--------

点击创建按钮可打开网页爬取配置页面。

|image1|

配置项
------

名称
::::

配置名称。

URL
::::

爬取的起始URL。

爬取对象URL
:::::::::::::::::

与此项中指定的正则表达式(Java格式)匹配的URL将成为 |Fess| 爬虫的爬取对象。

从爬取对象中排除的URL
:::::::::::::::::::::

与此项中指定的正则表达式(Java格式)匹配的URL将从 |Fess| 爬虫的爬取对象中排除。

搜索对象URL
::::::::::::::

与此项中指定的正则表达式(Java格式)匹配的URL将成为搜索对象。

从搜索对象中排除的URL
::::::::::::::::::

与此项中指定的正则表达式(Java格式)匹配的URL将从搜索对象中排除。

配置参数
::::::::::::

可以指定爬取配置信息。

深度
::::

可以指定爬取文档中包含的链接时的跟踪深度。

最大访问数
:::::::::::

被索引的URL数量。

用户代理
:::::::::::::::

|Fess| 爬虫的名称。

线程数
::::::::

此配置中用于爬取的线程数。

间隔
::::

爬取URL时每个线程的时间间隔。

权重值
::::::::

此配置中被索引文档的权重。

权限
:::::::::::

指定此配置的权限。
权限的指定方法为,例如,要让属于developer组的用户显示搜索结果,需指定{group}developer。
按用户指定为{user}用户名,按角色指定为{role}角色名,按组指定为{group}组名。

虚拟主机
::::::::

指定虚拟主机的主机名。
详情请参阅 :doc:`../config/virtual-host`。

状态
::::

如果启用,则默认爬虫的计划任务将包含此配置。

说明
::::

可以输入说明。

删除配置
--------

在列表页面点击配置名称,然后点击删除按钮将显示确认画面。点击删除按钮后配置将被删除。

示例
==

爬取 fess.codelibs.org
-----------------------------

要创建爬取 https://fess.codelibs.org/ 下页面的网页爬取配置,请使用如下配置值。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - 配置项
     - 配置值
   * - 名称
     - Fess
   * - URL
     - https://fess.codelibs.org/
   * - 爬取对象URL
     - https://fess.codelibs.org/.*

其他配置值使用默认值。

爬取需要网页认证的站点
------------------------

Fess 支持对 BASIC 认证、DIGEST 认证和 NTLM 认证的站点进行爬取。
有关网页认证的详细信息,请参阅网页认证页面。

Redmine
:::::::

要创建爬取受密码保护的Redmine(例如 https://<server>/)页面的网页爬取配置,请使用如下配置值。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - 配置项
     - 配置值
   * - 名称
     - Redmine
   * - URL
     - https://<server>/my/page
   * - 爬取对象URL
     - https://<server>/.*
   * - 配置参数
     - client.robotsTxtEnabled=false (可选)

之后,使用如下配置值创建网页认证配置。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - 配置项
     - 配置值
   * - 方案
     - Form
   * - 用户名
     - (Account for crawling)
   * - 密码
     - (Password for the account)
   * - 参数
     - | encoding=UTF-8
       | token_method=GET
       | token_url=https://<server>/login
       | token_pattern=name="authenticity_token"[^>]+value="([^"]+)"
       | token_name=authenticity_token
       | login_method=POST
       | login_url=https://<server>/login
       | login_parameters=username=${username}&password=${password}
   * - 网页认证
     - Redmine


XWiki
:::::

要创建爬取XWiki(例如 https://<server>/xwiki/)页面的网页爬取配置,请使用如下配置值。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - 配置项
     - 配置值
   * - 名称
     - XWiki
   * - URL
     - https://<server>/xwiki/bin/view/Main/
   * - 爬取对象URL
     - https://<server>/.*
   * - 配置参数
     - client.robotsTxtEnabled=false (可选)

之后,使用如下配置值创建网页认证配置。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - 配置项
     - 配置值
   * - 方案
     - Form
   * - 用户名
     - (Account for crawling)
   * - 密码
     - (Password for the account)
   * - 参数
     - | encoding=UTF-8
       | token_method=GET
       | token_url=http://<server>/xwiki/bin/login/XWiki/XWikiLogin
       | token_pattern=name="form_token" +value="([^"]+)"
       | token_name=form_token
       | login_method=POST
       | login_url=http://<server>/xwiki/bin/loginsubmit/XWiki/XWikiLogin
       | login_parameters=j_username=${username}&j_password=${password}
   * - 网页认证
     - XWiki


.. |image0| image:: ../../../resources/images/en/15.5/admin/webconfig-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/webconfig-2.png
.. pdf            :height: 940 px
