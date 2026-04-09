============================================================
第16回：搜索基础设施自动化 -- 使用 CI/CD 流水线和 Infrastructure as Code 进行管理
============================================================

前言
====

当搜索系统的配置通过手动方式管理时，环境的重现变得困难，配置错误的风险也会增加。
引入现代 DevOps 理念，将搜索基础设施也作为代码进行管理和自动化吧。

本文介绍将 Fess 的配置作为代码进行管理并自动化部署的方法。

目标读者
========

- 希望自动化搜索系统运维的人员
- 希望将 DevOps/IaC 方法应用于搜索基础设施的人员
- 具备 Docker 和 CI/CD 基础知识的人员

Infrastructure as Code 的应用
==============================

以下是 Fess 环境中作为"代码"管理的对象。

.. list-table:: IaC 管理对象
   :header-rows: 1
   :widths: 25 35 40

   * - 对象
     - 管理方法
     - 版本管理
   * - Docker 配置
     - compose.yaml
     - Git
   * - Fess 设置
     - 备份文件 / 管理 API
     - Git
   * - 词典数据
     - 通过管理 API 导出
     - Git
   * - OpenSearch 设置
     - 配置文件
     - Git

使用 Docker Compose 定义环境
================================

生产环境的 Docker Compose 文件
-------------------------------

在第2回使用的基本配置基础上进行扩展，定义适合生产环境的配置。

.. code-block:: yaml

    services:
      fess:
        image: ghcr.io/codelibs/fess:15.5.1
        environment:
          - SEARCH_ENGINE_HTTP_URL=http://opensearch:9200
          - FESS_DICTIONARY_PATH=/usr/share/opensearch/config/dictionary/
        ports:
          - "8080:8080"
        depends_on:
          opensearch:
            condition: service_healthy
        restart: unless-stopped

      opensearch:
        image: ghcr.io/codelibs/fess-opensearch:3.6.0
        environment:
          - discovery.type=single-node
          - OPENSEARCH_JAVA_OPTS=-Xmx4g -Xms4g
          - DISABLE_INSTALL_DEMO_CONFIG=true
          - DISABLE_SECURITY_PLUGIN=true
          - FESS_DICTIONARY_PATH=/usr/share/opensearch/config/dictionary/
        volumes:
          - opensearch-data:/usr/share/opensearch/data
          - opensearch-dictionary:/usr/share/opensearch/config/dictionary
        healthcheck:
          test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
          interval: 30s
          timeout: 10s
          retries: 3
          start_period: 90s
        restart: unless-stopped

    volumes:
      opensearch-data:
      opensearch-dictionary:

要点如下。

- 健康检查定义：在 OpenSearch 准备就绪后再启动 Fess
- 卷持久化：数据持久化
- 重启策略：故障时自动恢复
- JVM 堆的显式设置

使用管理 API 实现配置自动化
===============================

通过使用 Fess 的管理 API，无需通过 GUI 即可以编程方式操作配置。

导出设置
--------

导出当前的 Fess 设置，并作为代码保存。

可以在管理界面的 [系统信息] > [备份] 中进行导出。
也可以使用管理 API 通过脚本进行导出。

导入设置
--------

使用保存的配置文件将设置应用到新的 Fess 环境。
这样可以方便地重建或复制环境。

fessctl CLI 的使用
===================

fessctl 是 Fess 的命令行工具。
在管理界面中执行的大部分操作都可以通过命令行完成。

主要操作
--------

- 创建、更新和删除爬虫设置（Web、文件系统、数据存储）
- 执行调度任务
- 管理用户、角色和组
- 管理关键词匹配、标签、权重提升等搜索设置

通过使用 CLI，可以将配置变更脚本化并集成到 CI/CD 流水线中。

构建 CI/CD 流水线
====================

配置变更工作流
----------------

按照以下工作流管理搜索系统的配置变更。

1. **变更**：修改配置文件，在 Git 分支中管理
2. **评审**：通过 Pull Request 评审变更内容
3. **测试**：在预发布环境中验证行为
4. **部署**：将设置应用到生产环境

GitHub Actions 自动化示例
---------------------------

当配置文件的变更被合并后，自动反映到生产环境的示例。

.. code-block:: yaml

    name: Deploy Fess Config
    on:
      push:
        branches: [main]
        paths:
          - 'fess-config/**'
          - 'dictionary/**'

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4

          - name: Apply dictionary updates
            run: |
              # 将词典文件传输到 Fess 服务器
              scp dictionary/* fess-server:/opt/fess/dictionary/

          - name: Verify Fess health
            run: |
              # 通过健康检查 API 确认 Fess 运行状态
              curl -s https://fess.example.com/api/v1/health

备份自动化
===========

定期备份也应实现自动化。

备份脚本
--------

使用 cron 或 CI/CD 的调度功能定期进行备份。

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail

    BACKUP_DIR="/backup/fess/$(date +%Y%m%d)"
    mkdir -p "${BACKUP_DIR}"

    # 获取 Fess 备份文件列表
    curl -s -o "${BACKUP_DIR}/fess-backup-files.json" \
      -H "Authorization: Bearer ${FESS_TOKEN}" \
      "https://fess.example.com/api/admin/backup/files"

    # 下载配置数据（例：fess_config.bulk）
    curl -s -o "${BACKUP_DIR}/fess_config.bulk" \
      -H "Authorization: Bearer ${FESS_TOKEN}" \
      "https://fess.example.com/api/admin/backup/file/fess_config.bulk"

    # 删除旧备份（超过30天）
    find /backup/fess -type d -mtime +30 -exec rm -rf {} +

    echo "Backup completed: ${BACKUP_DIR}"

环境重建步骤
=============

为灾难恢复或测试环境搭建，将完全重建环境的步骤文档化。

1. 使用 Docker Compose 启动容器
2. 等待 OpenSearch 健康检查返回 green/yellow
3. 导入 Fess 设置（通过管理 API 或恢复功能）
4. 部署词典文件
5. 执行爬虫任务
6. 验证运行（搜索测试）

将此步骤脚本化后，可以快速重建环境。

总结
====

本文介绍了使用 DevOps 方法管理 Fess 搜索基础设施的方法。

- 使用 Docker Compose 将环境定义代码化
- 使用管理 API 和 fessctl 实现配置自动化
- 使用 CI/CD 流水线实现配置变更的自动部署
- 备份自动化和环境重建步骤

从"阅读手册手动配置"进化到"执行代码自动部署"，让搜索基础设施的运维更上一层楼。

下一回将介绍通过插件开发扩展 Fess。

参考资料
========

- `Fess 管理 API <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__
