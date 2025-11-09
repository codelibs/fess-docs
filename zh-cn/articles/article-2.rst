====================================================================
使用Fess创建基于Elasticsearch的搜索服务器 ～ 基于角色的搜索篇
====================================================================

前言
========

本文将介绍 Fess 的特色功能之一——基于角色的搜索功能。

本文使用 Fess 15.3.0 进行说明。
关于 Fess 的构建方法,请参考\ `导入篇 <https://fess.codelibs.org/ja/articles/article-1.html>`__\ 。

目标读者
========

-  希望在门户网站等需要认证的系统中构建搜索系统的人员

-  希望构建按浏览权限进行搜索的环境的人员

必要环境
==========

本文内容已在以下环境中进行了验证。

-  Ubuntu 22.04

-  OpenJDK 21

基于角色的搜索
================

Fess 的基于角色的搜索是根据认证用户的认证信息来区分搜索结果的功能。
例如,拥有销售部角色的销售担当 A 在搜索结果中会显示销售部角色的信息,而没有销售部角色的技术担当 B 即使搜索也不会显示这些信息。
通过使用此功能,可以在门户或单点登录环境中实现按登录用户所属部门或职位进行的搜索。

Fess 的基于角色的搜索默认情况下可以根据 Fess 管理的用户信息来区分搜索结果。
除此之外,还可以与 LDAP 或 Active Directory 的认证信息联动使用。
此外,除了这些认证系统,还可以从以下位置获取角色信息。

1. 请求参数

2. 请求头

3. Cookie

4. J2EE 的认证信息

使用方法如下:在门户服务器或代理型单点登录系统中,认证时通过 Cookie 将认证信息保存到 Fess 运行的域和路径,从而可以将角色信息传递给 Fess。
此外,在反向代理型单点登录系统中,访问 Fess 时在请求参数或请求头中附加认证信息,Fess 就可以获取角色信息。
通过这种方式与各种认证系统联动,可以为每个用户区分搜索结果。

使用基于角色搜索的设置
====================================

假设已安装 Fess 15.3.0。
如果尚未安装,请参考\ `导入篇 <https://fess.codelibs.org/ja/articles/article-1.html>`__\ 进行安装。

本次将说明使用 Fess 用户管理功能的角色搜索。

设置概要
----------

本次将创建销售部(sales)和技术部(eng)两个角色。然后让 taro 用户属于 sales 角色,可以获得 \https://www.n2sm.net/ 的搜索结果,让 hanako 用户属于 eng 角色,可以获得 \https://fess.codelibs.org/ 的搜索结果。

创建角色
------------

首先访问管理界面。
\http://localhost:8080/admin/

从 用户 > 角色 > 新建 输入名称「sales」,创建 sales 角色。
同样创建 eng 角色。

角色列表
|image0|


创建爬虫用角色
----------------------

点击 用户 > 角色 > sales > 创建新的爬虫用角色。
在名称中输入「销售部」,值保持「sales」不变,点击 [创建]。
然后在 爬虫 > 角色 的列表中会添加销售部的设置。

同样,将 eng 角色的爬虫用角色名称注册为「技术部」。

爬虫用角色列表
|image1|


创建用户
--------------

从 用户 > 用户 > 新建 按照下图的设置创建 taro 用户和 hanako 用户。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * -
     - 太郎
     - 花子
   * - 用户名
     - taro
     - hanako
   * - 密码
     - taro
     - hanako
   * - 角色
     - sales
     - eng


确认注册用户
------------------

通过本次设置,可以使用 admin、taro、hanako 三个用户登录 Fess。
请依次确认可以登录。
访问 \http://localhost:8080/admin/,使用 admin 用户登录后会正常显示管理界面。
然后退出 admin 用户。点击管理界面右上角的按钮。

退出按钮
|image2|

输入用户名和密码,使用 taro 或 hanako 登录。
登录成功后,会显示 \http://localhost:8080/ 的搜索界面。

添加爬取设置
------------------

注册爬取对象。
本次将设置为销售部角色的用户只能搜索 \https://www.n2sm.net/,技术部角色的用户只能搜索 \https://fess.codelibs.org/。
要注册这些爬取设置,请点击 爬虫 > 网络 > 新建,创建网络爬取设置。
本次按照以下设置。其他保持默认值。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * -
     - N2SM
     - Fess
   * - 名称
     - N2SM
     - Fess
   * - URL
     - \https://www.n2sm.net/
     - \https://fess.codelibs.org/
   * - 作为爬取对象的 URL
     - \https://www.n2sm.net/.*
     - \https://fess.codelibs.org/.*
   * - 最大访问数
     - 10
     - 10
   * - 间隔
     - 3000 毫秒
     - 3000 毫秒
   * - 角色
     - 销售部
     - 技术部

开始爬取
--------------

注册爬取设置后,从 系统 > 调度器 > Default Crawler 点击 [立即开始]。等待爬取完成。

搜索
----

爬取完成后,访问 \http://localhost:8080/,在未登录状态下搜索「fess」等词,确认没有显示搜索结果。
然后使用 taro 用户登录,同样进行搜索。
taro 用户拥有 sales 角色,因此只会显示 \https://www.n2sm.net/ 的搜索结果。

sales 角色的搜索界面
|image3|

退出 taro 用户,使用 hanako 用户登录。
与之前相同进行搜索,hanako 用户拥有 eng 角色,因此只会显示 \https://fess.codelibs.org/ 的搜索结果。

eng 角色的搜索界面
|image4|

总结
======

本文介绍了 Fess 的安全功能之一——基于角色的搜索。
虽然主要说明了使用 J2EE 认证信息的基于角色的搜索,但由于向 Fess 传递认证信息的实现是通用的,因此可以对应各种认证系统。
由于可以按用户属性区分搜索结果,因此也可以实现公司内部门户网站或共享文件夹等需要按浏览权限进行搜索的系统。

参考资料
========

-  `Fess <https://fess.codelibs.org/ja/>`__

.. |image0| image:: ../../resources/images/en/article/3/role-1.png
.. |image1| image:: ../../resources/images/en/article/3/role-2.png
.. |image2| image:: ../../resources/images/en/article/3/logout.png
.. |image3| image:: ../../resources/images/en/article/3/search-by-sales.png
.. |image4| image:: ../../resources/images/en/article/3/search-by-eng.png
