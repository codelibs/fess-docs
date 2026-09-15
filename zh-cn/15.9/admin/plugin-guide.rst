========
插件
========

概述
====

插件配置页面用于管理插件。

管理方法
======

显示方法
------

要打开下图所示的已安装插件列表页面,请单击左侧菜单中的[系统 > 插件]。

|image0|

要卸载,请单击"删除"按钮。

安装
---------

要安装新插件,请单击"安装"按钮。

|image1|

在下拉菜单中选择要安装的插件,然后单击"安装"按钮,即可开始安装。

从命令行安装
============

使用 ``bin/fess-setup`` 可以从命令行安装插件。

::

    $ bin/fess-setup install plugin fess-script-groovy

未指定版本时,将从仓库中选择适用于此 |Fess| 的最新版本,因此每次执行可能安装不同的版本。要固定版本,请在插件名称后用冒号分隔指定版本。

::

    $ bin/fess-setup install plugin fess-script-groovy:15.9.0 fess-ds-git:15.9.0

插件是各自单独发布的,同时安装的插件版本不一定相同。请为每个插件分别指定。未指定版本的插件将使用 ``--version`` 的值。

::

    $ bin/fess-setup install plugin fess-script-groovy fess-ds-git:15.9.1 --version 15.9.0

新版本安装完成后,将删除同一插件的旧版本。如果指定的版本不存在,将以退出码 1 结束,因此即使写入 Dockerfile 等构建步骤,也不会在缺少插件的情况下继续。

``bin/fess-setup list plugins`` 显示为此 |Fess| 发布的插件以及其中已安装的插件, ``list installed`` 不访问仓库即可显示已安装的插件, ``upgrade plugins`` 将所有已安装的插件以适合此 |Fess| 的版本重新安装, ``remove plugin`` 删除插件。安装、升级或删除插件后,请重启 |Fess|\ 。所有命令和选项请参阅 :doc:`../install/fess-setup`\ 。

.. |image0| image:: ../../../resources/images/en/15.9/admin/plugin-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/plugin-2.png
