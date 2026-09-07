================================
用开源方案实现文件服务器全文检索
================================

前言
====

随着各部门不断增加文件服务器，"那份资料放在哪里"逐渐变得无人知晓。Windows 搜索只能在单个共享文件夹内工作，服务器一多就无法横跨；NAS 自带的全文检索功能也止步于设备本身。

解决这个问题的方法之一，是在文件服务器前面架设一台全文检索服务器。本页整理了把开源全文检索服务器 Fess 放到这个位置之前，需要事先确认的要点。

适用读者
========

- 为公司内部文件服务器或 NAS 的检索而困扰的人
- 正在考察全文检索，想知道开源方案是否够用的人
- 希望在不改动现有访问权限的前提下引入检索的人

Fess 以 Apache License 2.0 公开，无需许可费用。

可以检索放在哪里的文件
======================

Fess 的文件爬取支持以下协议。在管理界面的 [爬虫] > [文件系统] 中，作为爬取起始 URL 指定。

.. list-table:: 支持的协议
   :header-rows: 1
   :widths: 12 33 55

   * - 协议
     - URL 格式
     - 主要用途
   * - ``file``
     - ``file:///home/share/documents/``
     - 运行 Fess 的服务器上的目录，已挂载的 NAS 也包含在内
   * - ``smb``
     - ``smb://fileserver.example.com/share/``
     - Windows 文件共享，支持 SMB 2.0.2 到 SMB 3.1.1
   * - ``smb1``
     - ``smb1://fileserver.example.com/share/``
     - 只能使用 SMB1/CIFS 的老旧设备
   * - ``ftp``
     - ``ftp://fileserver.example.com/pub/``
     - FTP 服务器
   * - ``s3``
     - ``s3://bucket-name/prefix/``
     - Amazon S3 以及兼容 S3 的对象存储
   * - ``gcs``
     - ``gcs://bucket-name/prefix/``
     - Google Cloud Storage

启用哪些协议由配置项 ``crawler.file.protocols`` 管理，默认值为 ``file,smb,smb1,ftp,s3,gcs`` 。

检索 Windows 文件共享时通常使用 ``smb`` 。``smb1`` 是为只能使用 SMB1 的老旧 NAS 和打印服务器保留的；出于安全原因，SMB1 在 Windows 上也已默认停用，因此不应作为新建环境的选择。

原有的访问权限被原样继承
========================

在文件服务器上引入检索时，最大的顾虑是"不该被看到的文档出现在检索结果里"。如果人事和财务的共享文件夹出现在全体员工的检索结果中，那么排序做得再好，这套检索系统也无法使用。

Fess 通过\ **把文件服务器一侧的访问权限原样带入检索**\ 来解决这个问题。

工作原理
--------

1. 爬取时，Fess 读取每个文件的 ACL（访问控制列表）
2. 把被允许和被拒绝的账户与组，记录为该文档的"角色"
3. 检索时与登录用户所持有的角色进行比对，只返回有权限的文档

允许和拒绝都会被处理，内部通过 ``(allow)`` 和 ``(deny)`` 前缀加以区分。从 ACL 中取出角色的行为默认启用。

.. list-table:: 与权限继承相关的配置项
   :header-rows: 1
   :widths: 38 14 48

   * - 配置项
     - 默认值
     - 说明
   * - ``smb.role.from.file``
     - ``true``
     - 从通过 SMB 爬取的文件的 ACL 中取得角色
   * - ``file.role.from.file``
     - ``true``
     - 从本地文件系统的权限中取得角色
   * - ``ftp.role.from.file``
     - ``true``
     - 从通过 FTP 爬取的文件中取得角色
   * - ``smb.available.sid.types``
     - ``1,2,4:2,5:1``
     - 采用为角色的 SID 种类，用于调整用户与组的处理方式

需要先确认的前提
----------------

要让这套机制完整生效，\ **检索一方的用户也必须持有相同的角色**\ 。文档一侧记录的是"属于这个组就可以读"，因此如果检索用户无法把自己所属的组告知 Fess，就没有可供比对的对象。

因此，要实现继承权限的检索，\ **与 Active Directory 或 LDAP 的对接是前提**\ 。也就是让 Fess 的登录使用与文件服务器认证相同的目录服务。

反过来说，如果只针对全体员工都可以查看的共享文件夹，则不必进行这项对接。这一点往往是划定首次引入范围的分界线。

能读取到哪些文件格式的内容
==========================

Fess 利用 Apache Tika 从文件内容中提取文本。检索对象不只是文件名，还包括正文，因此"想不起标题的资料"也能找到。

主要支持的格式如下。

- MS Office（doc、xls、ppt、docx、xlsx、pptx 等）
- PDF
- 文本、HTML、XML
- 富文本（rtf）
- 源代码（js、c、h、java 等）
- 压缩文件（gz、tar、zip 等，会解压后把内容一并纳入对象）

完整列表请参阅 `搜索对象文件 <https://fess.codelibs.org/zh-cn/supported-files.html>`__ 。

扫描件、纯图片 PDF 这类本身不含文本的文件，无法通过这种方式读取内容。是否需要 OCR，建议先确认目标文件夹的实际情况再判断。

架构与规模
==========

Fess 使用 OpenSearch 存放检索索引。规模较小时，Fess 与 OpenSearch 部署在同一台服务器上即可运行；当对象文件增多后，可以把 OpenSearch 拆分为集群。

估算规模时，只看文件数量并不准确。确认以下几点会更有把握。

- 目标文件夹的总容量，以及其中含有文本的文件所占比例
- 更新频率（每天变化还是每月数次），这会影响爬取间隔的设计
- 单个文件的大小，过大的文件可以通过配置排除在爬取对象之外

引入步骤
========

1. **先跑起来** — 按照 `快速构建指南 <https://fess.codelibs.org/zh-cn/quick-start.html>`__ 的步骤启动 Fess。使用 Docker Compose 只需几分钟就能进入可检索状态
2. **创建爬取配置** — 在管理界面的 [爬虫] > [文件系统] 中登记目标 URL 和爬取间隔
3. **设置认证信息** — 在 [爬虫] > [文件认证] 中登记访问共享文件夹所用的账户
4. **设计权限与标签** — 需要按部门筛选就设置标签，需要按权限区分展示就设置角色

按步骤搭建的示例见 `第4回 统一检索分散的文件 <https://fess.codelibs.org/zh-cn/articles/guide-04.html>`__ ，其中完整说明了如何把多台文件服务器和公司内部网站汇集到一个检索框中查找。

小结
====

- Fess 是可以把文件服务器（SMB/CIFS、FTP、本地、S3、GCS）纳入全文检索对象的开源检索服务器
- 通过 SMB 爬取的文件，其 ACL 中记录的访问权限会直接用于检索结果的区分展示，且该行为默认启用
- 要实现继承权限的检索，与 Active Directory 或 LDAP 的对接是前提
- 借助 Apache Tika，Office 文档和 PDF 的正文也会成为检索对象
- 可以从小规模起步，随着对象增多再把 OpenSearch 扩展为集群

参考资料
========

- `爬虫配置：Web、文件服务器、数据库爬取 <https://fess.codelibs.org/zh-cn/stable/config/crawler-basic.html>`__
- `基于角色的访问控制 <https://fess.codelibs.org/zh-cn/stable/config/security-role.html>`__
- `搜索对象文件 <https://fess.codelibs.org/zh-cn/supported-files.html>`__
- `快速构建指南 <https://fess.codelibs.org/zh-cn/quick-start.html>`__
- `管理界面指南 <https://fess.codelibs.org/zh-cn/stable/admin/index.html>`__
