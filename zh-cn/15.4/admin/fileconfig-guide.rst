============
文件抓取
============

概述
====

在文件抓取配置页面中，您可以管理对文件系统或共享网络文件夹中的文件进行抓取的配置。

管理方式
======

显示方式
------

要打开文件抓取配置的列表页面，请点击左侧菜单中的 [爬虫 > 文件系统]。

|image0|

点击配置名称即可进行编辑。

创建配置
-------

点击新建按钮即可打开文件抓取配置页面。

|image1|

配置项
------

名称
::::

配置的名称。

路径
::::

在此路径中，指定开始抓取的位置（例如：file:/、smb://、s3://、gcs://）。

包含在抓取中的路径
:::::::::::::::::

与此项中指定的正则表达式（Java格式）匹配的路径将成为 |Fess| 爬虫的抓取对象。

排除在抓取外的路径
:::::::::::::::::::::

与此项中指定的正则表达式（Java格式）匹配的路径将不会成为 |Fess| 爬虫的抓取对象。

包含在搜索中的路径
::::::::::::::

与此项中指定的正则表达式（Java格式）匹配的路径将成为搜索对象。

排除在搜索外的路径
::::::::::::::::::

与此项中指定的正则表达式（Java格式）匹配的路径将不会成为搜索对象。

配置参数
::::::::::::

可以指定抓取配置信息。

深度
::::

指定要抓取的文件系统结构的深度。

最大访问数
:::::::::::

指定要索引的路径数量。

线程数
::::::::

指定用于此配置的线程数量。

间隔
::::

指定线程每次抓取路径时的等待时间。

权重值
::::::::

权重值是指通过此配置索引的文档的优先级。

权限
:::::::::::

指定此配置的权限。
权限的指定方法为，例如，要向属于developer组的用户显示搜索结果，需指定为{group}developer。
按用户指定为{user}用户名，按角色指定为{role}角色名，按组指定为{group}组名。

虚拟主机
::::::::

指定虚拟主机的主机名。
详细信息请参阅 :doc:`配置指南的虚拟主机 <../config/virtual-host>`。

状态
::::

当此配置启用时，默认爬虫作业将包含此配置进行抓取。

说明
::::

可以输入说明。

删除配置
--------

点击列表页面中的配置名称，然后点击删除按钮将显示确认画面。点击删除按钮后配置将被删除。

示例
==

抓取本地文件
--------------------

如果要抓取 /home/share 下的文件，配置如下所示。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - 名称
     - 值
   * - 名称
     - Share 目录
   * - 路径
     - file:/home/share

其他参数使用默认设置即可。

抓取Windows共享文件夹
---------------------------

如果要抓取 \\SERVER\SharedFolder 下的文件，配置如下所示。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - 名称
     - 值
   * - 名称
     - 共享文件夹
   * - 路径
     - smb://SERVER/SharedFolder/

如果访问共享文件夹需要用户名/密码，则需要从左侧菜单中的 [爬虫 > 文件认证] 创建文件认证配置。
此时的配置如下所示。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - 名称
     - 值
   * - 主机名
     - SERVER
   * - 协议
     - SAMBA
   * - 用户名
     - (请输入)
   * - 密码
     - (请输入)

抓取 Amazon S3 存储桶
---------------------

如果要抓取 my-bucket 存储桶中的文件，配置如下所示。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - 名称
     - 值
   * - 名称
     - S3 存储桶
   * - 路径
     - s3://my-bucket/

访问 S3 需要认证凭据。在"配置参数"中添加以下内容：

::

    client.endpoint=https://s3.ap-northeast-1.amazonaws.com
    client.accessKey=您的访问密钥
    client.secretKey=您的私密密钥
    client.region=ap-northeast-1

抓取 Google Cloud Storage 存储桶
---------------------------------

如果要抓取 my-gcs-bucket 存储桶中的文件，配置如下所示。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - 名称
     - 值
   * - 名称
     - GCS 存储桶
   * - 路径
     - gcs://my-gcs-bucket/

访问 GCS 需要认证凭据。在"配置参数"中添加以下内容：

::

    client.projectId=您的项目ID
    client.credentialsFile=/path/to/service-account.json


.. |image0| image:: ../../../resources/images/en/15.4/admin/fileconfig-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/fileconfig-2.png
.. pdf            :height: 940 px
