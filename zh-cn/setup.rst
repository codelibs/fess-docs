================
安装步骤
================

安装方法
================

Fess 提供 ZIP 归档、RPM/DEB 包、Docker 镜像的分发包。
使用 Docker 可以在 Windows 和 Mac 等环境中轻松设置 Fess。

.. note::

   本页面说明在 **Windows 上使用 Docker 的安装步骤**。Linux 或 macOS 用户也可以按照类似步骤进行安装，但 Docker Desktop 的安装方式因平台而异。
   详情请参考 `Docker <https://docs.docker.com/get-docker/>`_ 的文档。

构建运营环境时，请务必参考 :doc:`15.6/install/index`。
有关系统要求，请参阅 :doc:`15.6/install/prerequisites`。

.. warning::

   **生产环境的重要注意事项**

   在生产环境或负载验证等情况下，不推荐使用内置的 OpenSearch 运行。
   请务必构建外部的 OpenSearch 服务器。

设置流程概述
------------

按照以下顺序进行操作：

1. 安装 Docker Desktop
2. 配置操作系统（调整 vm.max_map_count）
3. 下载 Fess 启动文件
4. 启动 Fess 并验证运行

安装 Docker Desktop
============================

如果未安装 Docker Desktop，请按以下步骤安装。

下载
------------

在 `Docker Desktop <https://www.docker.com/products/docker-desktop/>`__ 下载对应操作系统的安装程序。

运行安装程序
--------------------

双击下载的安装程序，开始安装。

确认已选中"Install required Windows components for WSL 2"或
"Install required Enable Hyper-V Windows Features"，
然后点击 OK 按钮。

|image0|

安装完成后，点击"close"按钮关闭画面。

|image1|

启动 Docker Desktop
---------------------

点击 Windows 菜单中的"Docker Desktop"启动。

|image2|

启动 Docker Desktop 后，会显示使用条款，勾选"I accept the terms"后点击"Accept"按钮。

会出现开始教程的提示，这里点击"Skip tutorial"跳过。
点击"Skip tutorial"后会显示 Dashboard。

|image3|

设置
====

为了能够将 OpenSearch 作为 Docker 容器运行，需要在操作系统端调整"vm.max_map_count"的值。
根据使用的环境设置方法有所不同，各自的设置方法请参考"` Set vm.max_map_count to at least 262144 <https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#_set_vm_max_map_count_to_at_least_262144>`_ "。

设置 Fess
==================

创建启动文件
------------------

创建一个合适的文件夹，下载 `compose.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml>`_ 和 `compose-opensearch3.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml>`_。

.. note::

   ``compose-opensearch3.yaml`` 是用于使用 OpenSearch 3.x 的附加配置文件。
   与 ``compose.yaml`` 组合使用。

也可以使用 curl 命令获取，如下所示：

.. code-block:: bash

    curl -o compose.yaml https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -o compose-opensearch3.yaml https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml

启动 Fess
----------

使用 docker compose 命令启动 Fess。

打开命令提示符，移动到 compose.yaml 文件所在的文件夹，执行以下命令：

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   启动可能需要几分钟时间。
   可以使用以下命令查看日志：

   .. code-block:: bash

       docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

   使用 ``Ctrl+C`` 可以结束日志显示。


操作确认
========

.. note::

   启动完成后，在浏览器中访问以下 URL 确认运行状态：

   - **搜索页面：** http://localhost:8080/
   - **管理界面：** http://localhost:8080/admin/

默认管理员账户的用户名/密码为 admin/admin。

.. warning::

   **关于安全的重要注意事项**

   请务必更改默认密码。
   特别是在生产环境中，强烈建议在首次登录后立即更改密码。

管理员账户由应用服务器管理。
在 Fess 的管理界面中，将在应用服务器上通过 fess 角色认证的用户判断为管理员。

其他
======

停止 Fess
----------

要停止 Fess，在启动 Fess 的文件夹中执行以下命令：

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml stop

要停止并删除容器：

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   使用 ``down`` 命令同时删除卷时，需要添加 ``-v`` 选项。
   在这种情况下，所有数据都会被删除，请注意。

   .. code-block:: bash

       docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

更改管理员密码
----------------------

可以在管理界面的用户编辑页面更改密码。

1. 访问 http://localhost:8080/admin/ 并登录。
2. 从右上角菜单选择"用户"。
3. 打开管理员用户（admin）的编辑页面，更改密码。

下一步
======

Fess 设置完成后，请参考以下文档进一步使用 Fess：

- :doc:`15.6/install/run` — Fess 启动·停止·配置详情
- :doc:`15.6/admin/index` — 管理员指南（爬虫设置、用户管理等）
- :doc:`15.6/user/index` — 用户指南（如何搜索）

如果遇到问题，请参考 :doc:`15.6/install/troubleshooting`。

.. |image0| image:: ../resources/images/en/install/dockerdesktop-1.png
.. |image1| image:: ../resources/images/en/install/dockerdesktop-2.png
.. |image2| image:: ../resources/images/en/install/dockerdesktop-3.png
.. |image3| image:: ../resources/images/en/install/dockerdesktop-4.png
